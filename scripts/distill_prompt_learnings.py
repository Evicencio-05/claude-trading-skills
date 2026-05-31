#!/usr/bin/env python3
"""Distill prompt run retros into state/prompt_learnings.yaml (zero LLM).

Processes reports/prompt_run_retro_*.md, aggregates defect patterns,
updates task_family run counts, archives stale one-shot prompts, and
writes a one-page digest.

Phase 2 extension (not implemented): optional LLM distill via claude -p
with --enable-llm and budget cap to propose prompt-engine.md edits.

Usage:
    uv run python3 scripts/distill_prompt_learnings.py --dry-run
    uv run python3 scripts/distill_prompt_learnings.py
    uv run python3 scripts/distill_prompt_learnings.py --since 2026-05-01

Exit codes:
    0 — success (including zero unprocessed retros)
    1 — error
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml

LEARNINGS_PATH = "state/prompt_learnings.yaml"
RETRO_GLOB = "prompt_run_retro_*.md"
DIGEST_PREFIX = "prompt_learning_digest_"
META_PROMPTS_DEFAULT = [
    "prompt-engine.md",
    "prompt-complete.md",
    "prompt-distill.md",
    "README.md",
]
PROMOTE_THRESHOLD_DEFAULT = 3
ARCHIVE_AGE_DAYS_DEFAULT = 60


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def slugify_root_cause(text: str) -> str:
    """Normalize root cause text to a stable slug."""
    slug = text.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    return slug.strip("_") or "unknown"


def match_pattern_id(root_cause: str, patterns: list[dict]) -> str | None:
    """Match a defect root cause to an existing pattern id."""
    slug = slugify_root_cause(root_cause)
    for pattern in patterns:
        existing = pattern.get("root_cause", "")
        if slug == existing or slug in existing or existing in slug:
            return pattern["id"]
    return None


def parse_markdown_table(section: str) -> list[dict[str, str]]:
    """Parse a simple markdown pipe table into row dicts."""
    lines = [ln.strip() for ln in section.splitlines() if ln.strip().startswith("|")]
    if len(lines) < 2:
        return []
    headers = [h.strip().lower() for h in lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < len(headers):
            cells.extend([""] * (len(headers) - len(cells)))
        rows.append(dict(zip(headers, cells, strict=False)))
    return rows


def parse_retro(content: str) -> dict:
    """Extract structured fields from a prompt run retro markdown file."""
    task_family = None
    task_prompt = None
    goal_verdict = None

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("**Task family:**"):
            task_family = stripped.removeprefix("**Task family:**").strip().strip("*")
        elif stripped.startswith("**Task prompt:**"):
            task_prompt = stripped.removeprefix("**Task prompt:**").strip().strip("*")
        elif stripped.startswith("**Goal verdict:**"):
            goal_verdict = stripped.removeprefix("**Goal verdict:**").strip().strip("*")

    defect_section = ""
    if "## Defect log" in content:
        defect_section = content.split("## Defect log", 1)[1]
        if "## " in defect_section:
            defect_section = defect_section.split("## ", 1)[0]

    defects: list[dict[str, str]] = []
    for row in parse_markdown_table(defect_section):
        root = row.get("root cause", "").strip()
        if root and root not in ("", "-", "..."):
            defects.append(
                {
                    "what": row.get("what went wrong", ""),
                    "root_cause": root,
                    "prompt_fix": row.get("prompt fix", ""),
                }
            )

    return {
        "task_family": task_family,
        "task_prompt": task_prompt,
        "goal_verdict": goal_verdict,
        "defects": defects,
    }


def load_learnings(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Learnings file not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid learnings YAML: {path}")
    data.setdefault("meta", {})
    data["meta"].setdefault("retro_files_processed", [])
    data.setdefault("patterns", [])
    data.setdefault("task_families", {})
    data.setdefault("promoted_durable", [])
    data.setdefault("meta_prompts", META_PROMPTS_DEFAULT)
    data.setdefault("promote_threshold", PROMOTE_THRESHOLD_DEFAULT)
    data.setdefault("archive_age_days", ARCHIVE_AGE_DAYS_DEFAULT)
    return data


def save_learnings(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def retro_date_from_name(name: str) -> date | None:
    match = re.search(r"prompt_run_retro_(\d{4}-\d{2}-\d{2})", name)
    if not match:
        return None
    return date.fromisoformat(match.group(1))


def find_unprocessed_retros(
    reports_dir: Path, learnings: dict, since: date | None = None
) -> list[Path]:
    processed = set(learnings.get("meta", {}).get("retro_files_processed", []))
    retros: list[Path] = []
    if not reports_dir.exists():
        return retros
    for path in sorted(reports_dir.glob(RETRO_GLOB)):
        if path.name in processed:
            continue
        retro_date = retro_date_from_name(path.name)
        if since and retro_date and retro_date < since:
            continue
        retros.append(path)
    return retros


def apply_retro(learnings: dict, parsed: dict, retro_date: date) -> dict:
    """Apply one retro to learnings; return summary of changes."""
    changes: dict = {
        "new_patterns": [],
        "promoted_patterns": [],
        "task_family_updated": None,
    }
    threshold = int(learnings.get("promote_threshold", PROMOTE_THRESHOLD_DEFAULT))
    patterns: list[dict] = learnings["patterns"]

    for defect in parsed.get("defects", []):
        root = defect["root_cause"]
        pid = match_pattern_id(root, patterns)
        if pid:
            pattern = next(p for p in patterns if p["id"] == pid)
            pattern["seen"] = int(pattern.get("seen", 0)) + 1
            if pattern["seen"] >= threshold and not pattern.get("promote_candidate"):
                pattern["promote_candidate"] = True
                changes["promoted_patterns"].append(pid)
        else:
            new_id = slugify_root_cause(root)[:48] or "unknown_cause"
            if any(p["id"] == new_id for p in patterns):
                new_id = f"{new_id}_{len(patterns)}"
            fix = defect.get("prompt_fix") or f"Avoid: {root}"
            patterns.append(
                {
                    "id": new_id,
                    "seen": 1,
                    "root_cause": slugify_root_cause(root),
                    "fix": fix,
                    "in_prompt_engine": False,
                    "promote_candidate": False,
                }
            )
            changes["new_patterns"].append(new_id)

    task_family = parsed.get("task_family")
    if task_family:
        families = learnings["task_families"]
        if task_family not in families:
            families[task_family] = {"runs": 0, "last_run": None}
        entry = families[task_family]
        entry["runs"] = int(entry.get("runs", 0)) + 1
        entry["last_run"] = retro_date.isoformat()
        changes["task_family_updated"] = task_family

        durable_threshold = int(learnings.get("durable_run_threshold", 2))
        promoted = learnings.get("promoted_durable", [])
        durable_name = entry.get("durable_prompt")
        if durable_name and entry["runs"] >= durable_threshold and durable_name not in promoted:
            promoted.append(durable_name)
            changes.setdefault("promoted_durable_added", []).append(durable_name)

    return changes


def collect_retro_prompt_refs(reports_dir: Path) -> dict[str, date]:
    """Map prompt filenames referenced in retros to latest retro date."""
    refs: dict[str, date] = {}
    if not reports_dir.exists():
        return refs
    for path in reports_dir.glob(RETRO_GLOB):
        retro_date = retro_date_from_name(path.name) or date.today()
        content = path.read_text(encoding="utf-8")
        parsed = parse_retro(content)
        task_prompt = parsed.get("task_prompt") or ""
        if task_prompt.endswith(".md") and task_prompt != "inline":
            name = Path(task_prompt).name
            refs[name] = max(refs.get(name, date.min), retro_date)
        for match in re.findall(r"\.cursor/prompts/([a-zA-Z0-9_-]+\.md)", content):
            refs[match] = max(refs.get(match, date.min), retro_date)
    return refs


def archive_candidates(
    prompts_dir: Path,
    learnings: dict,
    retro_refs: dict[str, date],
    as_of: date,
) -> list[Path]:
    """Return prompt files eligible for archive."""
    if not prompts_dir.exists():
        return []
    promoted = set(learnings.get("promoted_durable", []))
    meta = set(learnings.get("meta_prompts", META_PROMPTS_DEFAULT))
    archive_age = int(learnings.get("archive_age_days", ARCHIVE_AGE_DAYS_DEFAULT))
    cutoff = as_of - timedelta(days=archive_age)
    candidates: list[Path] = []

    for path in sorted(prompts_dir.glob("*.md")):
        if path.name in promoted or path.name in meta:
            continue
        last_ref = retro_refs.get(path.name)
        if last_ref and last_ref >= cutoff:
            continue
        mtime_date = date.fromtimestamp(path.stat().st_mtime)
        if mtime_date >= cutoff and last_ref is None:
            continue
        candidates.append(path)
    return candidates


def write_digest(
    output_dir: Path,
    as_of: date,
    summary: dict,
    learnings: dict,
    dry_run: bool,
) -> Path:
    digest_path = output_dir / f"{DIGEST_PREFIX}{as_of.isoformat()}.md"
    lines = [
        f"# Prompt Learning Digest — {as_of.isoformat()}",
        "",
        f"**Retros processed:** {summary['retros_processed']}",
        f"**New patterns:** {len(summary.get('new_patterns', []))}",
        f"**Promoted patterns (seen >= threshold):** {len(summary.get('promoted_patterns', []))}",
        f"**Archived prompts:** {len(summary.get('archived', []))}",
        f"**Action required:** {summary.get('action_required', 'none')}",
        "",
    ]

    if summary.get("promoted_patterns"):
        lines.append("## Newly promoted patterns")
        for pid in summary["promoted_patterns"]:
            pattern = next((p for p in learnings["patterns"] if p["id"] == pid), None)
            if pattern:
                lines.append(f"- **{pid}** (seen={pattern['seen']}): {pattern.get('fix', '')}")
        lines.append("")

    if summary.get("archived"):
        lines.append("## Archived to .cursor/prompts/archive/")
        for name in summary["archived"]:
            lines.append(f"- {name}")
        lines.append("")

    if summary.get("task_families_updated"):
        lines.append("## Task family run counts")
        for fam in summary["task_families_updated"]:
            entry = learnings["task_families"].get(fam, {})
            lines.append(f"- **{fam}**: runs={entry.get('runs', 0)}, last={entry.get('last_run')}")
        lines.append("")

    detail = summary.get("detail_lines", [])
    if detail:
        lines.append("## Detail")
        lines.extend(detail)
        lines.append("")

    content = "\n".join(lines)
    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
        digest_path.write_text(content, encoding="utf-8")
    return digest_path


def run_distill(
    repo_root: Path,
    dry_run: bool = False,
    since: date | None = None,
    output_dir: Path | None = None,
) -> dict:
    """Run full distill pipeline."""
    learnings_path = repo_root / LEARNINGS_PATH
    reports_dir = output_dir or (repo_root / "reports")
    prompts_dir = repo_root / ".cursor" / "prompts"
    archive_dir = prompts_dir / "archive"

    learnings = load_learnings(learnings_path)
    unprocessed = find_unprocessed_retros(reports_dir, learnings, since=since)
    retro_refs = collect_retro_prompt_refs(reports_dir)

    summary: dict = {
        "retros_processed": 0,
        "new_patterns": [],
        "promoted_patterns": [],
        "archived": [],
        "task_families_updated": [],
        "detail_lines": [],
        "action_required": "none",
    }

    for retro_path in unprocessed:
        content = retro_path.read_text(encoding="utf-8")
        parsed = parse_retro(content)
        retro_date = retro_date_from_name(retro_path.name) or date.today()
        changes = apply_retro(learnings, parsed, retro_date)

        summary["retros_processed"] += 1
        summary["new_patterns"].extend(changes.get("new_patterns", []))
        summary["promoted_patterns"].extend(changes.get("promoted_patterns", []))
        if changes.get("task_family_updated"):
            summary["task_families_updated"].append(changes["task_family_updated"])
        for item in changes.get("promoted_durable_added", []):
            summary["detail_lines"].append(f"Auto-added to promoted_durable: {item}")

        if not dry_run:
            learnings["meta"]["retro_files_processed"].append(retro_path.name)

    as_of = date.today()
    archive_list = archive_candidates(prompts_dir, learnings, retro_refs, as_of=as_of)
    for path in archive_list:
        summary["archived"].append(path.name)
        if not dry_run:
            archive_dir.mkdir(parents=True, exist_ok=True)
            dest = archive_dir / path.name
            if dest.exists():
                dest.unlink()
            shutil.move(str(path), str(dest))

    if summary["promoted_patterns"]:
        summary["action_required"] = "optional — review promoted patterns in digest"

    if not dry_run:
        learnings["meta"]["last_distilled"] = datetime.now().isoformat(timespec="seconds")
        save_learnings(learnings_path, learnings)

    digest_path = write_digest(reports_dir, as_of, summary, learnings, dry_run=dry_run)
    summary["digest_path"] = str(digest_path)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Distill prompt retros into learnings YAML.")
    parser.add_argument("--dry-run", action="store_true", help="Report only; do not write state")
    parser.add_argument(
        "--since", type=str, default=None, help="Only process retros on/after YYYY-MM-DD"
    )
    parser.add_argument("--output-dir", type=str, default=None, help="Reports output directory")
    args = parser.parse_args(argv)

    repo_root = get_repo_root()
    since = date.fromisoformat(args.since) if args.since else None
    output_dir = Path(args.output_dir) if args.output_dir else repo_root / "reports"

    try:
        summary = run_distill(repo_root, dry_run=args.dry_run, since=since, output_dir=output_dir)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    mode = "DRY-RUN" if args.dry_run else "DONE"
    print(
        f"{mode}: processed {summary['retros_processed']} retro(s); "
        f"digest={summary.get('digest_path')}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
