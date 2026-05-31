"""Same-day artifact resolution for deep-research PASS 0 preflight."""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

from report_paths import (
    ARTIFACT_PREFIXES,
    breakout_planner_run_hint,
    find_latest_same_day,
    find_screener_for_ticker,
    logs_dir,
    screener_run_hint,
)
from research_watchlist import get_repo_root, load_watchlist_config

BATCH_PREFIXES = ARTIFACT_PREFIXES


def _rel(path: Path, repo_root: Path) -> str:
    return str(path.relative_to(repo_root))


def market_context_path(repo_root: Path, as_of: date) -> Path | None:
    path = logs_dir(repo_root) / f"market_context_{as_of.isoformat()}.md"
    return path if path.exists() else None


def load_watchlist_symbols(watchlist_path: Path | None = None) -> list[str]:
    """Return sorted tickers with watching=true from research watchlist config."""
    if watchlist_path is None:
        watchlist_path = get_repo_root() / "config" / "research_watchlist.yaml"
    config = load_watchlist_config(watchlist_path)
    return sorted(t for t, cfg in config.items() if cfg.get("watching"))


def extract_ticker_row(json_path: Path, ticker: str) -> dict | None:
    """Return the screener result row for *ticker*, if present."""
    try:
        data = json.loads(json_path.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    symbol = ticker.upper()
    rows: list[dict] = []
    for key in ("results", "all_results"):
        chunk = data.get(key)
        if isinstance(chunk, list):
            rows.extend(chunk)
    for row in rows:
        if str(row.get("symbol", "")).upper() == symbol:
            return row
    return None


def _artifact_reuse(path: Path | None, repo_root: Path, **extra: Any) -> dict[str, Any]:
    if path is None:
        return {"action": "run", **extra}
    entry: dict[str, Any] = {"action": "reuse", "path": _rel(path, repo_root)}
    entry.update(extra)
    return entry


def _artifact_run(reason: str | None = None, run_hint: str | None = None) -> dict[str, Any]:
    entry: dict[str, Any] = {"action": "run"}
    if reason:
        entry["reason"] = reason
    if run_hint:
        entry["run_hint"] = run_hint
    return entry


def build_preflight_manifest(
    ticker: str,
    as_of: date,
    *,
    force_refresh: bool = False,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Build PASS 0 manifest describing reuse vs run for batch artifacts."""
    root = repo_root or get_repo_root()
    watchlist_symbols = load_watchlist_symbols(root / "config" / "research_watchlist.yaml")
    watchlist_arg = " ".join(watchlist_symbols) if watchlist_symbols else ticker.upper()

    ctx_path = market_context_path(root, as_of)
    fred_path = logs_dir(root) / f"fred_calendar_{as_of.isoformat()}.json"

    artifacts: dict[str, dict[str, Any]] = {}

    if force_refresh:
        artifacts["market_context"] = _artifact_run(
            run_hint="uv run python3 scripts/pre_market.py",
        )
        for key in BATCH_PREFIXES:
            if key in ("vcp_screener", "canslim_screener"):
                artifacts[key] = _artifact_run(run_hint=screener_run_hint(key, watchlist_arg))
            elif key == "breakout_trade_planner":
                continue
            else:
                artifacts[key] = _artifact_run()
        artifacts["breakout_trade_planner"] = _artifact_run(
            run_hint=breakout_planner_run_hint(),
        )
        artifacts["fred_calendar"] = _artifact_run(
            run_hint=(
                f"python3 scripts/fred_calendar.py --output "
                f"reports/logs/fred_calendar_{as_of.isoformat()}.json"
            ),
        )
    else:
        if ctx_path:
            artifacts["market_context"] = _artifact_reuse(ctx_path, root)
        else:
            artifacts["market_context"] = _artifact_run(
                reason="no same-day market context",
                run_hint="uv run python3 scripts/pre_market.py",
            )

        breadth_path = find_latest_same_day(root, "market_breadth", as_of)
        uptrend_path = find_latest_same_day(root, "uptrend_analysis", as_of)
        if ctx_path and breadth_path is None:
            breadth_path = ctx_path  # embedded in market_context markdown
        if ctx_path and uptrend_path is None:
            uptrend_path = ctx_path

        artifacts["market_breadth"] = _artifact_reuse(breadth_path, root)
        artifacts["uptrend_analysis"] = _artifact_reuse(uptrend_path, root)
        artifacts["market_top"] = _artifact_reuse(
            find_latest_same_day(root, "market_top", as_of),
            root,
        )
        artifacts["exposure_posture"] = _artifact_reuse(
            find_latest_same_day(root, "exposure_posture", as_of),
            root,
        )

        if fred_path.exists():
            artifacts["fred_calendar"] = _artifact_reuse(fred_path, root)
        elif ctx_path:
            artifacts["fred_calendar"] = _artifact_reuse(ctx_path, root)
        else:
            artifacts["fred_calendar"] = _artifact_run(
                reason="no same-day FRED output or market context",
                run_hint=(
                    f"python3 scripts/fred_calendar.py --output "
                    f"reports/logs/fred_calendar_{as_of.isoformat()}.json"
                ),
            )

        for screener_key in ("vcp_screener", "canslim_screener"):
            screener_path = find_screener_for_ticker(
                root, screener_key, ticker, as_of, watchlist_symbols
            )
            if screener_path:
                row = extract_ticker_row(screener_path, ticker)
                artifacts[screener_key] = _artifact_reuse(
                    screener_path,
                    root,
                    ticker_row=row,
                )
            else:
                artifacts[screener_key] = _artifact_run(
                    reason="no same-day screener covering ticker",
                    run_hint=screener_run_hint(screener_key, watchlist_arg),
                )

        artifacts["theme_detector"] = _artifact_reuse(
            find_latest_same_day(root, "theme_detector", as_of),
            root,
        )
        artifacts["breakout_trade_planner"] = _artifact_reuse(
            find_latest_same_day(root, "breakout_trade_planner", as_of),
            root,
        )

    counts = {"reuse": 0, "run": 0}
    for entry in artifacts.values():
        counts[entry["action"]] = counts.get(entry["action"], 0) + 1

    return {
        "ticker": ticker.upper(),
        "as_of": as_of.isoformat(),
        "generated_at": datetime.now().astimezone().isoformat(),
        "force_refresh": force_refresh,
        "watchlist_symbols": watchlist_symbols,
        "summary": counts,
        "artifacts": artifacts,
    }
