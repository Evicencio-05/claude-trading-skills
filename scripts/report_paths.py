"""Canonical paths under reports/ — single source of truth for artifact layout."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from research_watchlist import get_repo_root

# Artifact key -> relative directory under repo root
ARTIFACT_DIRS: dict[str, str] = {
    "market_breadth": "reports/market/breadth",
    "uptrend_analysis": "reports/market/uptrend",
    "sector_rotation": "reports/market/sector",
    "market_top": "reports/market/top",
    "exposure_posture": "reports/market/exposure",
    "vcp_screener": "reports/screeners/vcp",
    "canslim_screener": "reports/screeners/canslim",
    "earnings_trade_analyzer": "reports/screeners/earnings",
    "pead_screener": "reports/screeners/pead",
    "theme_detector": "reports/screeners/theme",
    "breakout_trade_planner": "reports/screeners/breakout",
    "position_sizer": "reports/portfolio",
    "portfolio_review": "reports/portfolio",
    "prompt_retro": "reports/prompts",
    "prompt_digest": "reports/prompts",
    "meta": "reports/meta",
    "entry_watchlist": "reports/logs",
    "agentic_copilot_plan": "reports/logs",
    "tradewhisperer_charts": "reports/charts/tradewhisperer",
    "gex_vex_maps": "reports/charts/gex_vex",
    "operator_charts": "reports/charts/operator",
    "ta_confluence": "reports/charts/confluence",
}

# Filename prefix for glob matching (key -> prefix)
ARTIFACT_PREFIXES: dict[str, str] = {
    "market_breadth": "market_breadth_",
    "uptrend_analysis": "uptrend_analysis_",
    "sector_rotation": "sector_rotation_",
    "market_top": "market_top_",
    "exposure_posture": "exposure_posture_",
    "vcp_screener": "vcp_screener_",
    "canslim_screener": "canslim_screener_",
    "theme_detector": "theme_detector_",
    "breakout_trade_planner": "breakout_trade_plan_",
    "earnings_trade_analyzer": "earnings_trade_analyzer_",
    "pead_screener": "pead_screener_",
    "entry_watchlist": "entry_watchlist_",
    "agentic_copilot_plan": "agentic_copilot_plan_",
    # Chart intakes use ticker-stem names; see ARTIFACT_DATE_GLOBS.
    "tradewhisperer_charts": "tw_",
    "gex_vex_maps": "gex_",
    "operator_charts": "operator_",
    "ta_confluence": "confluence_",
}

# Extra same-day globs for keys whose filenames are not `{prefix}{date}*`.
# `{date}` is replaced with ISO YYYY-MM-DD; each pattern is tried per extension.
ARTIFACT_DATE_GLOBS: dict[str, tuple[str, ...]] = {
    "tradewhisperer_charts": (
        "*_tw_*_{date}*",
        "list_tw_*_{date}*",
        "overlap_tw_{date}*",
        "tw_{date}*",
    ),
    "gex_vex_maps": (
        "*_gex_{date}*",
        "*_vex_{date}*",
        "gex_{date}*",
        "vex_{date}*",
    ),
    "operator_charts": (
        "*_operator_{date}*",
        "operator_{date}*",
    ),
    "ta_confluence": (
        "*_confluence_{date}*",
        "session_confluence_*_{date}*",
        "confluence_{date}*",
    ),
    # Plans embed ticker between prefix and date: agentic_copilot_plan_AVGO_2026-06-02.json
    "agentic_copilot_plan": (
        "agentic_copilot_plan_*_{date}*",
        "agentic_copilot_plan_{date}*",
    ),
}

ARTIFACT_KEYS = frozenset(ARTIFACT_DIRS)

LEGACY_FLAT_DIRS = ("reports/pre_market", "reports")


def reports_root(repo_root: Path | None = None) -> Path:
    root = repo_root or get_repo_root()
    return root / "reports"


def logs_dir(repo_root: Path | None = None) -> Path:
    return reports_root(repo_root) / "logs"


def artifact_dir(repo_root: Path, key: str, *, mkdir: bool = False) -> Path:
    if key not in ARTIFACT_DIRS:
        raise KeyError(f"Unknown artifact key: {key}")
    path = repo_root / ARTIFACT_DIRS[key]
    if mkdir:
        path.mkdir(parents=True, exist_ok=True)
    return path


def default_output_dir(repo_root: Path | None, key: str) -> Path:
    root = repo_root or get_repo_root()
    return artifact_dir(root, key)


def search_dirs(repo_root: Path, key: str) -> list[Path]:
    """Ordered search locations: canonical dir, then legacy flat dirs."""
    dirs: list[Path] = [artifact_dir(repo_root, key)]
    for rel in LEGACY_FLAT_DIRS:
        legacy = repo_root / rel
        if legacy not in dirs:
            dirs.append(legacy)
    return dirs


def find_latest_same_day(
    repo_root: Path,
    key: str,
    as_of: date,
) -> Path | None:
    """Return newest JSON for *key* on calendar day *as_of* across search dirs."""
    result = find_latest_same_day_artifact(repo_root, key, as_of, extensions=(".json",))
    return result


def _same_day_patterns(
    key: str,
    as_of: date,
    extensions: tuple[str, ...],
) -> list[str] | None:
    """Build glob patterns for *key* on *as_of*, or None if key unknown."""
    prefix = ARTIFACT_PREFIXES.get(key)
    if prefix is None and key not in ARTIFACT_DATE_GLOBS:
        return None
    date_str = as_of.isoformat()
    patterns: list[str] = []
    for template in ARTIFACT_DATE_GLOBS.get(key, ()):
        filled = template.format(date=date_str)
        patterns.extend(f"{filled}{ext}" for ext in extensions)
    # Always include classic prefix+date forms when a prefix is registered.
    if prefix is not None:
        patterns.extend(f"{prefix}{date_str}_*{ext}" for ext in extensions)
        patterns.extend(f"{prefix}{date_str}{ext}" for ext in extensions)
    # De-dupe while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for pattern in patterns:
        if pattern not in seen:
            seen.add(pattern)
            unique.append(pattern)
    return unique


def find_latest_same_day_artifact(
    repo_root: Path,
    key: str,
    as_of: date,
    *,
    extensions: tuple[str, ...] = (".json", ".md"),
) -> Path | None:
    """Return newest artifact for *key* on calendar day *as_of*.

    Prefers JSON over markdown when timestamps tie. Searches canonical dir then legacy.
    Supports ticker-stem chart names via ARTIFACT_DATE_GLOBS (e.g. SPY_tw_1D_DATE).
    """
    patterns = _same_day_patterns(key, as_of, extensions)
    if not patterns:
        return None

    for directory in search_dirs(repo_root, key):
        if not directory.exists():
            continue
        best = _best_artifact_in_dir(directory, patterns)
        if best is not None:
            return best
    return None


def _pick_newest_artifact(candidates: list[Path]) -> Path:
    """Pick newest timestamp within a directory; prefer JSON when stems tie."""
    by_stem: dict[str, Path] = {}
    for path in candidates:
        stem = path.stem
        existing = by_stem.get(stem)
        if existing is None:
            by_stem[stem] = path
        elif path.suffix.lower() == ".json":
            by_stem[stem] = path
    return sorted(by_stem.values(), key=lambda p: p.name)[-1]


def _best_artifact_in_dir(directory: Path, patterns: list[str]) -> Path | None:
    candidates: list[Path] = []
    for pattern in patterns:
        candidates.extend(directory.glob(pattern))
    if not candidates:
        return None
    return _pick_newest_artifact(candidates)


def _result_rows(data: dict) -> list[dict]:
    rows: list[dict] = []
    for chunk_key in ("results", "all_results"):
        chunk = data.get(chunk_key)
        if isinstance(chunk, list):
            rows.extend(chunk)
    return rows


def screener_covers_ticker(
    json_path: Path,
    ticker: str,
    watchlist_symbols: list[str],
) -> bool:
    try:
        data = json.loads(json_path.read_text())
    except (json.JSONDecodeError, OSError):
        return False

    symbol = ticker.upper()
    for row in _result_rows(data):
        if str(row.get("symbol", "")).upper() == symbol:
            return True

    funnel = (data.get("metadata") or {}).get("funnel") or {}
    universe = funnel.get("universe", 0)
    if watchlist_symbols and universe >= len(watchlist_symbols):
        return True
    return False


def find_screener_for_ticker(
    repo_root: Path,
    key: str,
    ticker: str,
    as_of: date,
    watchlist_symbols: list[str],
) -> Path | None:
    prefix = ARTIFACT_PREFIXES.get(key)
    if prefix is None:
        return None
    date_str = as_of.isoformat()
    pattern = f"{prefix}{date_str}_*.json"
    candidates: list[Path] = []
    for directory in search_dirs(repo_root, key):
        if directory.exists():
            candidates.extend(sorted(directory.glob(pattern)))
    for path in reversed(candidates):
        if screener_covers_ticker(path, ticker, watchlist_symbols):
            return path
    return None


def screener_run_hint(key: str, watchlist_arg: str) -> str:
    if key == "vcp_screener":
        return (
            f"python3 skills/vcp-screener/scripts/screen_vcp.py "
            f"--universe {watchlist_arg} --output-dir reports/screeners/vcp"
        )
    if key == "canslim_screener":
        return (
            f"python3 skills/canslim-screener/scripts/screen_canslim.py "
            f"--universe {watchlist_arg} --output-dir reports/screeners/canslim"
        )
    return ""


def breakout_planner_run_hint() -> str:
    return (
        "python3 skills/breakout-trade-planner/scripts/plan_breakout_trades.py "
        "--input reports/screeners/vcp/vcp_screener_YYYY-MM-DD.json "
        "--output-dir reports/screeners/breakout"
    )
