#!/usr/bin/env python3
"""Ollama client for local bulk LLM tasks (zero API cost).

Usage:
    from local_llm import chat, is_available, load_config
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

DEFAULT_HOST = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen2.5:7b"
DEFAULT_TIMEOUT = 120
USAGE_LOG = "reports/logs/local_llm_usage.jsonl"


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_config(repo_root: Path | None = None) -> dict[str, Any]:
    """Load Ollama config from optional YAML + environment."""
    root = repo_root or get_repo_root()
    load_dotenv(root / ".env")

    cfg: dict[str, Any] = {
        "host": os.environ.get("OLLAMA_HOST", DEFAULT_HOST).rstrip("/"),
        "model": os.environ.get("OLLAMA_MODEL", DEFAULT_MODEL),
        "timeout_seconds": DEFAULT_TIMEOUT,
    }

    yaml_path = root / "config" / "local_llm.yaml"
    if yaml_path.exists():
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
        ollama = data.get("ollama", data)
        if isinstance(ollama, dict):
            cfg["host"] = str(ollama.get("host", cfg["host"])).rstrip("/")
            cfg["model"] = str(ollama.get("model", cfg["model"]))
            cfg["timeout_seconds"] = int(ollama.get("timeout_seconds", cfg["timeout_seconds"]))

    return cfg


def _request_json(url: str, payload: dict | None = None, timeout: int = 30) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(  # nosec B310
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST" if payload is not None else "GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310
        return json.loads(resp.read().decode("utf-8"))


def is_available(config: dict[str, Any] | None = None, repo_root: Path | None = None) -> bool:
    """Return True if Ollama is reachable and the configured model is present."""
    cfg = config or load_config(repo_root)
    host = cfg["host"]
    model = cfg["model"]
    timeout = min(int(cfg.get("timeout_seconds", DEFAULT_TIMEOUT)), 15)
    try:
        tags = _request_json(f"{host}/api/tags", timeout=timeout)
    except (OSError, urllib.error.URLError, JSONDecodeError, TimeoutError):
        return False

    models = tags.get("models", [])
    names = {m.get("name", "") for m in models if isinstance(m, dict)}
    # Ollama may report "qwen2.5:7b" or "qwen2.5:7b-latest"
    if model in names:
        return True
    base = model.split(":")[0] if ":" in model else model
    return any(n == model or n.startswith(f"{base}:") for n in names)


def log_usage(
    repo_root: Path,
    task: str,
    model: str,
    prompt_chars: int,
    response_chars: int,
) -> None:
    """Append one line to reports/logs/local_llm_usage.jsonl."""
    log_path = repo_root / USAGE_LOG
    log_path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "task": task,
        "model": model,
        "prompt_chars": prompt_chars,
        "response_chars": response_chars,
        "estimated_cost_usd": 0.0,
    }
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def chat(
    prompt: str,
    system: str | None = None,
    config: dict[str, Any] | None = None,
    repo_root: Path | None = None,
    task: str = "chat",
) -> str:
    """Send a chat completion request to Ollama /api/chat."""
    root = repo_root or get_repo_root()
    cfg = config or load_config(root)
    host = cfg["host"]
    model = cfg["model"]
    timeout = int(cfg.get("timeout_seconds", DEFAULT_TIMEOUT))

    messages: list[dict[str, str]] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    body = {
        "model": model,
        "messages": messages,
        "stream": False,
    }
    result = _request_json(f"{host}/api/chat", payload=body, timeout=timeout)
    content = ""
    message = result.get("message")
    if isinstance(message, dict):
        content = str(message.get("content", ""))
    log_usage(root, task, model, len(prompt), len(content))
    return content


class LocalLLMError(Exception):
    """Raised when local LLM call fails."""


def chat_or_raise(
    prompt: str,
    system: str | None = None,
    repo_root: Path | None = None,
    task: str = "chat",
) -> str:
    """Chat if Ollama available; raise LocalLLMError otherwise."""
    root = repo_root or get_repo_root()
    cfg = load_config(root)
    if not is_available(cfg, root):
        raise LocalLLMError(
            f"Ollama unavailable or model '{cfg['model']}' not found at {cfg['host']}"
        )
    return chat(prompt, system=system, config=cfg, repo_root=root, task=task)


def extract_json_from_text(text: str, required_keys: list[str]) -> dict | None:
    """Scan text for first JSON object containing any required key."""
    decoder = json.JSONDecoder()
    idx = 0
    while idx < len(text):
        pos = text.find("{", idx)
        if pos == -1:
            break
        try:
            obj, _end = decoder.raw_decode(text, pos)
            if isinstance(obj, dict) and any(k in obj for k in required_keys):
                return obj
            idx = pos + 1
        except JSONDecodeError:
            idx = pos + 1
    return None


def strip_code_fences(text: str) -> str:
    """Remove markdown code fences from model output."""
    text = text.strip()
    match = re.match(r"^```(?:yaml|json|markdown|md)?\s*\n?(.*?)\n?```\s*$", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text


def build_edge_hints_prompt(payload: dict[str, Any]) -> str:
    """Build prompt for edge-hint-extractor LLM contract."""
    return (
        "You are an equity edge research assistant. Given market context JSON, "
        "generate concise trading edge hints.\n\n"
        f"Context JSON:\n{json.dumps(payload, indent=2)}\n\n"
        "Output ONLY valid YAML in one of these forms:\n"
        "- A list of hint objects\n"
        '- Or {"hints": [ ... ]}\n\n'
        "Each hint must include at least: title, observation.\n"
        "Optional fields: hypothesis_type, preferred_entry_family, symbols, "
        "regime_bias, mechanism_tag.\n"
        "Do not include markdown fences or commentary."
    )


def build_retro_draft_prompt(evidence: str, task_family: str = "custom") -> str:
    """Build prompt for prompt-complete retro skeleton."""
    return (
        "Draft a prompt run retro report skeleton in markdown for a Cursor agent task.\n"
        f"Task family: {task_family}\n\n"
        "Evidence from the run:\n"
        f"{evidence}\n\n"
        "Include these sections with tables where shown:\n"
        "# Prompt Run Retro — YYYY-MM-DD\n"
        "**Task prompt:** inline\n"
        f"**Task family:** {task_family}\n"
        "**Goal verdict:** met | partial | failed\n\n"
        "## Verification matrix (table: Area | Status | Evidence)\n"
        "## Defect log (table: # | What went wrong | Root cause | Suggested fix)\n"
        "## Meta notes\n"
        "## Follow-ups\n\n"
        "Use normalized root_cause slugs (snake_case). English only. "
        "Do not invent file paths not present in evidence."
    )


def build_commit_message_prompt(diff: str) -> str:
    """Build prompt for commit message from staged diff."""
    return (
        "Write a concise git commit message (1-2 sentences, imperative mood, focus on why).\n"
        "Output ONLY the commit message text — no markdown fences, no subject/body labels.\n\n"
        f"Staged diff:\n{diff[:12000]}"
    )


def build_distill_suggest_prompt(retro_texts: list[str], learnings_summary: str) -> str:
    """Build prompt for optional LLM suggestions during prompt distill."""
    combined = "\n\n---\n\n".join(retro_texts[:5])
    return (
        "Review prompt run retros and existing learnings patterns. "
        "Suggest NEW pattern entries not already captured.\n\n"
        f"Existing patterns summary:\n{learnings_summary}\n\n"
        f"Retros:\n{combined[:8000]}\n\n"
        "Output ONLY valid YAML list of suggestions:\n"
        "- id: snake_case_id\n"
        "  root_cause: slug\n"
        "  fix: one line fix for prompt-engine\n"
        "  rationale: why promote\n"
        "Max 5 suggestions. No markdown fences."
    )


def distill_suggest(
    retro_texts: list[str],
    learnings: dict[str, Any],
    repo_root: Path | None = None,
) -> str:
    """Generate LLM suggestions for prompt learnings (review-only, not auto-applied)."""
    patterns = learnings.get("patterns", [])
    summary_lines = [f"- {p.get('id')}: seen={p.get('seen', 0)}" for p in patterns[:20]]
    learnings_summary = "\n".join(summary_lines) or "(no patterns yet)"
    prompt = build_distill_suggest_prompt(retro_texts, learnings_summary)
    return chat_or_raise(prompt, repo_root=repo_root, task="distill_suggest")
