"""Build structured pre-market summary from breadth/uptrend/sector artifacts."""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

from report_paths import find_latest_same_day_artifact, logs_dir

SCHEMA_VERSION = 1

_JSON_PATH_RE = re.compile(
    r"(?:JSON report saved to:|JSON Report:)\s*(?P<path>\S+\.json)",
    re.IGNORECASE,
)
_SECTOR_RISK_RE = re.compile(r"\*\*(RISK-[A-Z]+)\*\*\s*\(score:\s*(\d+)/100\)")
_SECTOR_CYCLE_RE = re.compile(r"\*\*(Early|Mid|Late|Recession)\*\*\s*\(confidence:")
_SECTOR_RANK_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|")
_SECTOR_OVERBOUGHT_RE = re.compile(r"^-\s+(.+):\s*(.+)$")


def _rel(path: Path | None, repo_root: Path) -> str | None:
    if path is None:
        return None
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def parse_path_from_stdout(output: str, kind: str = "json") -> Path | None:
    """Extract artifact path from skill stdout (json kind only today)."""
    if kind != "json":
        return None
    for line in output.splitlines():
        match = _JSON_PATH_RE.search(line)
        if match:
            return Path(match.group("path"))
    return None


def _load_json(path: Path | None) -> dict | None:
    if path is None or not path.exists() or path.suffix.lower() != ".json":
        return None
    try:
        data = json.loads(path.read_text())
        return data if isinstance(data, dict) else None
    except (json.JSONDecodeError, OSError):
        return None


def _component_pair(data: dict | None, strongest_key: str, weakest_key: str) -> tuple[Any, Any]:
    if not data:
        return None, None
    composite = data.get("composite") or {}
    return composite.get(strongest_key), composite.get(weakest_key)


def extract_breadth_summary(data: dict | None) -> dict[str, Any]:
    if not data:
        return {"score": None, "zone": None}
    composite = data.get("composite") or {}
    strongest, weakest = _component_pair(data, "strongest_health", "weakest_health")
    return {
        "score": composite.get("composite_score"),
        "zone": composite.get("zone"),
        "exposure_guidance": composite.get("exposure_guidance"),
        "guidance": composite.get("guidance"),
        "strongest": strongest,
        "weakest": weakest,
        "active_warnings": composite.get("active_warnings") or [],
        "actions": composite.get("actions") or [],
    }


def extract_uptrend_summary(data: dict | None) -> dict[str, Any]:
    if not data:
        return {"score": None, "zone": None}
    composite = data.get("composite") or {}
    strongest, weakest = _component_pair(data, "strongest_component", "weakest_component")
    warnings = composite.get("active_warnings") or []
    warning_labels = [w.get("label") for w in warnings if isinstance(w, dict) and w.get("label")]
    return {
        "score": composite.get("composite_score"),
        "zone": composite.get("zone"),
        "exposure_guidance": composite.get("exposure_guidance"),
        "guidance": composite.get("guidance"),
        "strongest": strongest,
        "weakest": weakest,
        "active_warnings": warnings,
        "warning_summary": "; ".join(warning_labels) if warning_labels else "none",
        "actions": composite.get("actions") or [],
    }


def extract_sector_summary(text: str | None) -> dict[str, Any]:
    if not text:
        return {"leading_sector": None, "cycle_phase": None}

    risk_match = _SECTOR_RISK_RE.search(text)
    cycle_match = _SECTOR_CYCLE_RE.search(text)

    top_sectors: list[dict[str, str]] = []
    in_ranking = False
    for line in text.splitlines():
        if "Sector Ranking" in line:
            in_ranking = True
            continue
        if in_ranking and line.startswith("| ---"):
            continue
        if in_ranking and line.startswith("| Rank"):
            continue
        row = _SECTOR_RANK_ROW_RE.match(line.strip())
        if row and in_ranking:
            rank, sector, ratio = row.group(1), row.group(2).strip(), row.group(3).strip()
            top_sectors.append({"rank": rank, "sector": sector, "ratio": ratio})
            if len(top_sectors) >= 3:
                in_ranking = False

    overbought: list[str] = []
    in_overbought = False
    for line in text.splitlines():
        if line.startswith("**Overbought**"):
            in_overbought = True
            continue
        if in_overbought and line.startswith("---"):
            break
        if in_overbought:
            ob = _SECTOR_OVERBOUGHT_RE.match(line.strip())
            if ob:
                overbought.append(f"{ob.group(1).strip()}: {ob.group(2).strip()}")

    leading = top_sectors[0]["sector"] if top_sectors else None
    return {
        "leading_sector": leading,
        "cycle_phase": cycle_match.group(1) if cycle_match else None,
        "risk_regime": risk_match.group(1) if risk_match else None,
        "risk_score": int(risk_match.group(2)) if risk_match else None,
        "top_sectors": top_sectors,
        "overbought": overbought,
    }


def determine_posture(
    breadth_score: float | None,
    macro_events: str,
    urgent_flags: list[str],
    as_of: date,
) -> tuple[str, str]:
    """Rule-based posture from playbook.md."""
    if breadth_score is None:
        return "UNKNOWN", "N/A"

    has_macro_today = macro_events != "none" and as_of.isoformat() in macro_events
    has_urgent = len(urgent_flags) > 0

    if has_urgent or breadth_score < 40:
        return "REDUCE_ONLY", "30%"
    if breadth_score < 60 or has_macro_today:
        return "CAUTIOUS", "50%"
    return "NEW_ENTRY_ALLOWED", "70%"


def build_synthesis(
    *,
    breadth_score: float | None,
    as_of: date,
    macro_events: str,
    urgent_flags: list[str],
    watch_flags: list[str] | None = None,
    breadth_summary: dict[str, Any],
    uptrend_summary: dict[str, Any],
    sector_summary: dict[str, Any],
) -> dict[str, Any]:
    watch_flags = watch_flags or []
    posture, ceiling = determine_posture(breadth_score, macro_events, urgent_flags, as_of)

    risk_flags: list[str] = []
    if macro_events != "none" and as_of.isoformat() in macro_events:
        risk_flags.append(f"Macro event today: {macro_events.splitlines()[0][:80]}")
    for flag in urgent_flags:
        risk_flags.append(flag)
    for w in uptrend_summary.get("active_warnings") or []:
        if isinstance(w, dict) and w.get("label"):
            risk_flags.append(w["label"])
    for w in breadth_summary.get("active_warnings") or []:
        if isinstance(w, dict) and w.get("label"):
            risk_flags.append(w["label"])
    if sector_summary.get("overbought"):
        risk_flags.append(f"Overbought sectors: {', '.join(sector_summary['overbought'][:2])}")

    actions: list[str] = []
    for source in (uptrend_summary, breadth_summary):
        for action in source.get("actions") or []:
            if action and action not in actions:
                actions.append(action)
            if len(actions) >= 5:
                break
        if len(actions) >= 5:
            break

    b = breadth_score if breadth_score is not None else "N/A"
    u = uptrend_summary.get("score", "N/A")
    sector = sector_summary.get("leading_sector") or "N/A"
    headline = (
        f"{posture.replace('_', ' ').title()} — breadth {b}/100, uptrend {u}/100, "
        f"leading sector {sector}."
    )

    return {
        "posture": posture,
        "ceiling": ceiling,
        "headline": headline,
        "risk_flags": risk_flags,
        "actions": actions,
        "watch_flag_count": len(watch_flags),
    }


def resolve_artifacts(
    repo_root: Path,
    as_of: date,
    *,
    breadth_stdout: str | None = None,
    uptrend_stdout: str | None = None,
    sector_stdout: str | None = None,
) -> dict[str, Path | None]:
    keys = ("market_breadth", "uptrend_analysis", "sector_rotation")
    stdouts = (breadth_stdout, uptrend_stdout, sector_stdout)
    resolved: dict[str, Path | None] = {}
    for key, stdout in zip(keys, stdouts, strict=True):
        path = find_latest_same_day_artifact(repo_root, key, as_of)
        if path is None and stdout:
            parsed = parse_path_from_stdout(stdout)
            if parsed and parsed.exists():
                path = parsed
        resolved[key] = path
    return resolved


def build_market_context_summary(
    repo_root: Path,
    *,
    as_of: date,
    macro_events: str,
    urgent_flags: list[str],
    watch_flags: list[str],
    breadth_stdout: str | None = None,
    uptrend_stdout: str | None = None,
    sector_stdout: str | None = None,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    artifacts = resolve_artifacts(
        repo_root,
        as_of,
        breadth_stdout=breadth_stdout,
        uptrend_stdout=uptrend_stdout,
        sector_stdout=sector_stdout,
    )

    breadth_path = artifacts["market_breadth"]
    uptrend_path = artifacts["uptrend_analysis"]
    sector_path = artifacts["sector_rotation"]

    breadth_data = _load_json(breadth_path)
    uptrend_data = _load_json(uptrend_path)

    sector_text: str | None = None
    if sector_path and sector_path.exists():
        try:
            sector_text = sector_path.read_text()
        except OSError:
            sector_text = None

    breadth_summary = extract_breadth_summary(breadth_data)
    uptrend_summary = extract_uptrend_summary(uptrend_data)
    sector_summary = extract_sector_summary(sector_text)

    breadth_score = breadth_summary.get("score")
    try:
        breadth_float = float(breadth_score) if breadth_score is not None else None
    except (TypeError, ValueError):
        breadth_float = None

    synthesis = build_synthesis(
        breadth_score=breadth_float,
        as_of=as_of,
        macro_events=macro_events,
        urgent_flags=urgent_flags,
        watch_flags=watch_flags,
        breadth_summary=breadth_summary,
        uptrend_summary=uptrend_summary,
        sector_summary=sector_summary,
    )

    ts = generated_at or datetime.now()
    return {
        "schema_version": SCHEMA_VERSION,
        "as_of": as_of.isoformat(),
        "generated_at": ts.isoformat(timespec="seconds"),
        "sources": {
            "breadth": _rel(breadth_path, repo_root),
            "uptrend": _rel(uptrend_path, repo_root),
            "sector": _rel(sector_path, repo_root),
        },
        "breadth": breadth_summary,
        "uptrend": uptrend_summary,
        "sector": sector_summary,
        "synthesis": synthesis,
        "position_flags": {"urgent": urgent_flags, "watch": watch_flags},
        "macro_events": macro_events,
    }


def format_market_context_markdown(summary: dict[str, Any]) -> str:
    b = summary.get("breadth") or {}
    u = summary.get("uptrend") or {}
    s = summary.get("sector") or {}
    syn = summary.get("synthesis") or {}
    flags = summary.get("position_flags") or {}
    urgent = flags.get("urgent") or []
    watch = flags.get("watch") or []
    all_flags = urgent + watch
    flags_str = "\n".join(all_flags) if all_flags else "none"
    sources = summary.get("sources") or {}
    macro = summary.get("macro_events") or "none"

    actions_md = ""
    for action in syn.get("actions") or []:
        actions_md += f"- {action}\n"
    if not actions_md:
        actions_md = "- No specific actions extracted.\n"

    risk_md = ""
    for rf in syn.get("risk_flags") or []:
        risk_md += f"- {rf}\n"
    if not risk_md:
        risk_md = "- None flagged.\n"

    return f"""# Pre-Market Report — {summary.get("as_of", "")}
*Generated: {summary.get("generated_at", "")}*

## Executive Summary

```
Posture:         {syn.get("posture", "UNKNOWN")}
Ceiling:         {syn.get("ceiling", "N/A")}
Headline:        {syn.get("headline", "")}

Breadth:         {b.get("score", "N/A")}/100 ({b.get("zone", "N/A")})
Uptrend:         {u.get("score", "N/A")}/100 ({u.get("zone", "N/A")})
Uptrend warning: {u.get("warning_summary", "none")}
Leading sector:  {s.get("leading_sector", "N/A")}
Cycle phase:     {s.get("cycle_phase", "N/A")}
Macro events:    {macro if macro != "none" else "none"}
Flags:           {flags_str if flags_str != "none" else "none"}
```

### Synthesis

{syn.get("headline", "")}

**Risk flags:**
{risk_md}
**Actions:**
{actions_md}

## Position Flags

{flags_str if flags_str != "none" else "No urgent or watch flags."}

## Artifact Links

| Report | Path |
|--------|------|
| Breadth | `{sources.get("breadth") or "not found"}` |
| Uptrend | `{sources.get("uptrend") or "not found"}` |
| Sector | `{sources.get("sector") or "not found"}` |

*Raw skill stdout omitted — open artifact files for full detail.*
"""


def market_context_json_path(repo_root: Path, as_of: date) -> Path:
    return logs_dir(repo_root) / f"market_context_{as_of.isoformat()}.json"


def market_context_md_path(repo_root: Path, as_of: date) -> Path:
    return logs_dir(repo_root) / f"market_context_{as_of.isoformat()}.md"


def write_market_context(
    repo_root: Path,
    summary: dict[str, Any],
    *,
    as_of: date,
) -> tuple[Path, Path]:
    logs_dir(repo_root).mkdir(parents=True, exist_ok=True)
    json_path = market_context_json_path(repo_root, as_of)
    md_path = market_context_md_path(repo_root, as_of)
    json_path.write_text(json.dumps(summary, indent=2, default=str) + "\n")
    md_path.write_text(format_market_context_markdown(summary))
    return json_path, md_path
