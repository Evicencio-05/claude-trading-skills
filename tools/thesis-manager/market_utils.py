"""Market context helpers for thesis-manager Market page."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

import utils

sys.path.insert(0, str(utils.get_repo_root() / "scripts"))
from report_paths import find_latest_same_day_artifact  # noqa: E402

_CONTEXT_DATE_RE = re.compile(r"^market_context_(20\d{2}-\d{2}-\d{2})\.(json|md)$")
_ARTIFACT_DATE_RE = re.compile(r"_(20\d{2}-\d{2}-\d{2})(?:_|\.|$)")


def _logs_dir() -> Path:
    return utils.get_repo_root() / "reports" / "logs"


def _resolve_path(relative_or_absolute: str | None) -> Path | None:
    if not relative_or_absolute:
        return None
    path = Path(relative_or_absolute)
    if not path.is_absolute():
        path = utils.get_repo_root() / path
    return path if path.exists() else None


def _rel_path(path: Path) -> str:
    try:
        return str(path.relative_to(utils.get_repo_root()))
    except ValueError:
        return str(path)


def _artifact_key_for_path(path: Path) -> str | None:
    name = path.name
    if name.startswith("market_breadth_"):
        return "market_breadth"
    if name.startswith("uptrend_analysis_"):
        return "uptrend_analysis"
    if name.startswith("sector_rotation_"):
        return "sector_rotation"
    return None


def _parse_artifact_date(path: Path) -> date | None:
    match = _ARTIFACT_DATE_RE.search(path.name)
    if not match:
        return None
    return date.fromisoformat(match.group(1))


def resolve_display_artifact(relative_or_absolute: str | None) -> Path | None:
    """Resolve a source path to the best human-readable report file (MD preferred)."""
    path = _resolve_path(relative_or_absolute)
    if path is None:
        return None
    if path.suffix.lower() == ".md":
        return path
    if path.suffix.lower() != ".json":
        return None

    md_sibling = path.with_suffix(".md")
    if md_sibling.exists():
        return md_sibling

    key = _artifact_key_for_path(path)
    as_of = _parse_artifact_date(path)
    if key and as_of:
        md_path = find_latest_same_day_artifact(
            utils.get_repo_root(), key, as_of, extensions=(".md",)
        )
        if md_path:
            return md_path

    return path


def format_artifact_json_as_markdown(data: dict, kind: str) -> str:
    """Build a concise markdown summary from breadth/uptrend JSON."""
    composite = data.get("composite") or {}
    lines = [f"# {kind.title()} Summary (from JSON)", ""]

    score = composite.get("composite_score", "N/A")
    zone = composite.get("zone", "N/A")
    lines.append(f"**Composite Score:** {score}/100")
    lines.append(f"**Zone:** {zone}")
    if composite.get("exposure_guidance"):
        lines.append(f"**Exposure Guidance:** {composite['exposure_guidance']}")
    if composite.get("guidance"):
        lines.append("")
        lines.append(f"> {composite['guidance']}")

    strongest = composite.get("strongest_health") or composite.get("strongest_component")
    weakest = composite.get("weakest_health") or composite.get("weakest_component")
    if strongest or weakest:
        lines.append("")
        lines.append("## Highlights")
        if strongest:
            lines.append(
                f"- **Strongest:** {strongest.get('label', 'N/A')} "
                f"({strongest.get('score', 'N/A')}/100)"
            )
        if weakest:
            lines.append(
                f"- **Weakest:** {weakest.get('label', 'N/A')} ({weakest.get('score', 'N/A')}/100)"
            )

    warnings = composite.get("active_warnings") or []
    if warnings:
        lines.append("")
        lines.append("## Warnings")
        for w in warnings:
            if isinstance(w, dict):
                label = w.get("label") or w.get("flag") or "Warning"
                desc = w.get("description") or ""
                lines.append(f"- **{label}** — {desc}".removesuffix(" — "))

    component_scores = composite.get("component_scores") or data.get("components") or {}
    if component_scores:
        lines.append("")
        lines.append("## Component Scores")
        lines.append("")
        lines.append("| Component | Score |")
        lines.append("|-----------|-------|")
        for _key, comp in component_scores.items():
            if not isinstance(comp, dict):
                continue
            label = comp.get("label") or _key.replace("_", " ").title()
            comp_score = comp.get("score", "N/A")
            lines.append(f"| {label} | {comp_score} |")

    return "\n".join(lines) + "\n"


def load_artifact_display(
    relative_or_absolute: str | None,
    kind: str,
) -> tuple[str | None, str, bool]:
    """Load report content for display.

    Returns (content, relative_path_label, is_json_summary).
    """
    resolved = resolve_display_artifact(relative_or_absolute)
    if resolved is None:
        return None, relative_or_absolute or "", False

    label = _rel_path(resolved)
    if resolved.suffix.lower() == ".md":
        try:
            return resolved.read_text(), label, False
        except OSError:
            return None, label, False

    try:
        data = json.loads(resolved.read_text())
        if not isinstance(data, dict):
            return None, label, True
        return format_artifact_json_as_markdown(data, kind), label, True
    except (json.JSONDecodeError, OSError):
        return None, label, True


def list_market_context_dates() -> list[date]:
    logs = _logs_dir()
    if not logs.exists():
        return []
    dates: set[date] = set()
    for path in logs.iterdir():
        match = _CONTEXT_DATE_RE.match(path.name)
        if match:
            dates.add(date.fromisoformat(match.group(1)))
    return sorted(dates, reverse=True)


def _parse_market_posture_md(text: str) -> dict | None:
    for heading in ("## Executive Summary", "## Market Posture"):
        block_match = re.search(rf"{re.escape(heading)}\s+```(.*?)```", text, re.DOTALL)
        if not block_match:
            continue
        fields: dict[str, str] = {}
        for line in block_match.group(1).splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
        syn = {
            "posture": fields.get("Posture", "UNKNOWN"),
            "ceiling": fields.get("Ceiling", "N/A"),
            "headline": fields.get("Headline", ""),
        }
        breadth_parts = (fields.get("Breadth") or "N/A").split("/")
        try:
            breadth_score = float(breadth_parts[0].strip())
        except (ValueError, IndexError):
            breadth_score = None
        uptrend_parts = (fields.get("Uptrend") or "N/A").split("/")
        try:
            uptrend_score = float(uptrend_parts[0].strip())
        except (ValueError, IndexError):
            uptrend_score = None
        return {
            "schema_version": 1,
            "as_of": fields.get("Date", ""),
            "synthesis": syn,
            "breadth": {"score": breadth_score, "zone": None},
            "uptrend": {
                "score": uptrend_score,
                "warning_summary": fields.get("Uptrend warning"),
            },
            "sector": {
                "leading_sector": fields.get("Leading sector"),
                "cycle_phase": fields.get("Cycle phase"),
            },
            "position_flags": {"urgent": [], "watch": []},
            "macro_events": fields.get("Macro events", "none"),
            "sources": {},
        }
    return None


def load_market_context(as_of: date | None = None) -> dict | None:
    """Load structured market context; prefer JSON for *as_of* (default: newest date)."""
    if as_of is None:
        dates = list_market_context_dates()
        if not dates:
            return None
        as_of = dates[0]

    json_path = _logs_dir() / f"market_context_{as_of.isoformat()}.json"
    if json_path.exists():
        try:
            data = json.loads(json_path.read_text())
            if isinstance(data, dict):
                data["_path"] = str(json_path)
                return data
        except (json.JSONDecodeError, OSError):
            pass

    md_path = _logs_dir() / f"market_context_{as_of.isoformat()}.md"
    if md_path.exists():
        try:
            parsed = _parse_market_posture_md(md_path.read_text())
            if parsed:
                parsed["as_of"] = as_of.isoformat()
                parsed["_path"] = str(md_path)
                return parsed
        except OSError:
            pass
    return None


def load_artifact_markdown(relative_or_absolute: str | None) -> str | None:
    """Deprecated: use load_artifact_display. Kept for backward compatibility."""
    content, _, _ = load_artifact_display(relative_or_absolute, "report")
    return content
