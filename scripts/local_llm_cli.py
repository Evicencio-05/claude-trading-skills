#!/usr/bin/env python3
"""CLI for local Ollama tasks — bulk text work off Cursor subscription tokens.

Usage:
    uv run python3 scripts/local_llm_cli.py health
    uv run python3 scripts/local_llm_cli.py complete --prompt path/to/prompt.txt
    uv run python3 scripts/local_llm_cli.py edge-hints   # JSON stdin → YAML stdout
    uv run python3 scripts/local_llm_cli.py retro-draft --evidence path.txt [--task-family slug]
    uv run python3 scripts/local_llm_cli.py commit-message
    uv run python3 scripts/local_llm_cli.py distill-suggest --retro path.md [--retro path2.md]

Exit codes:
    0 — success
    1 — usage / input error
    2 — Ollama unavailable
    3 — LLM call failed
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml
from local_llm import (
    LocalLLMError,
    build_commit_message_prompt,
    build_edge_hints_prompt,
    build_retro_draft_prompt,
    chat_or_raise,
    distill_suggest,
    get_repo_root,
    is_available,
    load_config,
    strip_code_fences,
)


def cmd_health(repo_root: Path) -> int:
    cfg = load_config(repo_root)
    if not is_available(cfg, repo_root):
        print(
            f"Ollama unavailable or model '{cfg['model']}' not found at {cfg['host']}",
            file=sys.stderr,
        )
        print("Run: ollama pull qwen2.5:7b", file=sys.stderr)
        return 2
    print(f"OK: {cfg['model']} @ {cfg['host']}")
    return 0


def cmd_complete(repo_root: Path, prompt_path: Path) -> int:
    if not prompt_path.is_file():
        print(f"Prompt file not found: {prompt_path}", file=sys.stderr)
        return 1
    prompt = prompt_path.read_text(encoding="utf-8")
    try:
        result = chat_or_raise(prompt, repo_root=repo_root, task="complete")
    except LocalLLMError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (OSError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"LLM call failed: {exc}", file=sys.stderr)
        return 3
    print(result)
    return 0


def _parse_hints_output(raw: str) -> dict | list:
    cleaned = strip_code_fences(raw)
    parsed = yaml.safe_load(cleaned)
    if parsed is None:
        raise ValueError("empty YAML from model")
    return parsed


def cmd_edge_hints(repo_root: Path) -> int:
    stdin_text = sys.stdin.read()
    if not stdin_text.strip():
        print("Expected JSON payload on stdin", file=sys.stderr)
        return 1
    try:
        payload = json.loads(stdin_text)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON stdin: {exc}", file=sys.stderr)
        return 1

    prompt = build_edge_hints_prompt(payload)
    try:
        raw = chat_or_raise(prompt, repo_root=repo_root, task="edge_hints")
        parsed = _parse_hints_output(raw)
    except LocalLLMError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (OSError, TimeoutError, json.JSONDecodeError, ValueError, yaml.YAMLError) as exc:
        print(f"edge-hints failed: {exc}", file=sys.stderr)
        return 3

    if isinstance(parsed, list):
        out = parsed
    elif isinstance(parsed, dict) and "hints" in parsed:
        out = parsed
    else:
        print("Model output must be a list or {hints: [...]}", file=sys.stderr)
        return 3

    print(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), end="")
    return 0


def cmd_retro_draft(repo_root: Path, evidence_path: Path, task_family: str) -> int:
    if not evidence_path.is_file():
        print(f"Evidence file not found: {evidence_path}", file=sys.stderr)
        return 1
    evidence = evidence_path.read_text(encoding="utf-8")
    prompt = build_retro_draft_prompt(evidence, task_family=task_family)
    try:
        result = chat_or_raise(prompt, repo_root=repo_root, task="retro_draft")
    except LocalLLMError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (OSError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"retro-draft failed: {exc}", file=sys.stderr)
        return 3
    print(result)
    return 0


def cmd_commit_message(repo_root: Path) -> int:
    result = subprocess.run(  # nosec B603 B607
        ["git", "diff", "--cached"],
        capture_output=True,
        text=True,
        cwd=repo_root,
        check=False,
    )
    diff = result.stdout.strip()
    if not diff:
        print("No staged changes (git diff --cached is empty)", file=sys.stderr)
        return 1

    prompt = build_commit_message_prompt(diff)
    try:
        message = chat_or_raise(prompt, repo_root=repo_root, task="commit_message")
    except LocalLLMError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (OSError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"commit-message failed: {exc}", file=sys.stderr)
        return 3
    print(message.strip())
    return 0


def cmd_distill_suggest(repo_root: Path, retro_paths: list[Path]) -> int:
    texts: list[str] = []
    for path in retro_paths:
        if not path.is_file():
            print(f"Retro not found: {path}", file=sys.stderr)
            return 1
        texts.append(path.read_text(encoding="utf-8"))

    learnings_path = repo_root / "state" / "prompt_learnings.yaml"
    learnings: dict = {}
    if learnings_path.exists():
        learnings = yaml.safe_load(learnings_path.read_text(encoding="utf-8")) or {}

    try:
        raw = distill_suggest(texts, learnings, repo_root=repo_root)
        cleaned = strip_code_fences(raw)
        print(cleaned)
    except LocalLLMError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (OSError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"distill-suggest failed: {exc}", file=sys.stderr)
        return 3
    return 0


def main(argv: list[str] | None = None) -> int:
    repo_root = get_repo_root()
    parser = argparse.ArgumentParser(description="Local Ollama CLI for bulk repo tasks.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("health", help="Check Ollama and model availability")

    complete_p = sub.add_parser("complete", help="Run a prompt file")
    complete_p.add_argument("--prompt", required=True, type=Path, help="Prompt text file")

    sub.add_parser(
        "edge-hints", help="JSON stdin → YAML hints stdout (edge-hint-extractor contract)"
    )

    retro_p = sub.add_parser("retro-draft", help="Draft prompt retro skeleton from evidence")
    retro_p.add_argument("--evidence", required=True, type=Path, help="Evidence text file")
    retro_p.add_argument("--task-family", default="custom", help="Task family slug")

    sub.add_parser("commit-message", help="Draft commit message from staged git diff")

    distill_p = sub.add_parser("distill-suggest", help="Suggest new learnings patterns from retros")
    distill_p.add_argument("--retro", action="append", required=True, type=Path, dest="retros")

    args = parser.parse_args(argv)

    if args.command == "health":
        return cmd_health(repo_root)
    if args.command == "complete":
        return cmd_complete(repo_root, args.prompt)
    if args.command == "edge-hints":
        return cmd_edge_hints(repo_root)
    if args.command == "retro-draft":
        return cmd_retro_draft(repo_root, args.evidence, args.task_family)
    if args.command == "commit-message":
        return cmd_commit_message(repo_root)
    if args.command == "distill-suggest":
        return cmd_distill_suggest(repo_root, args.retros)
    return 1


if __name__ == "__main__":
    sys.exit(main())
