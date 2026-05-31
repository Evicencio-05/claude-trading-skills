"""Same-day artifact resolution for deep-research PASS 0 preflight."""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

from research_watchlist import get_repo_root, load_watchlist_config

BATCH_PREFIXES = {
    "market_breadth": "market_breadth_",
    "uptrend_analysis": "uptrend_analysis_",
    "market_top": "market_top_",
    "exposure_posture": "exposure_posture_",
    "vcp_screener": "vcp_screener_",
    "canslim_screener": "canslim_screener_",
    "theme_detector": "theme_detector_",
    "breakout_trade_planner": "breakout_trade_plan_",
}


def _rel(path: Path, repo_root: Path) -> str:
    return str(path.relative_to(repo_root))


def find_latest_same_day(reports_dir: Path, prefix: str, as_of: date) -> Path | None:
    """Return the newest JSON report for *prefix* on calendar day *as_of*."""
    if not reports_dir.exists():
        return None
    date_str = as_of.isoformat()
    matches = sorted(reports_dir.glob(f"{prefix}{date_str}_*.json"))
    return matches[-1] if matches else None


def market_context_path(logs_dir: Path, as_of: date) -> Path | None:
    path = logs_dir / f"market_context_{as_of.isoformat()}.md"
    return path if path.exists() else None


def load_watchlist_symbols(watchlist_path: Path | None = None) -> list[str]:
    """Return sorted tickers with watching=true from research watchlist config."""
    if watchlist_path is None:
        watchlist_path = get_repo_root() / "config" / "research_watchlist.yaml"
    config = load_watchlist_config(watchlist_path)
    return sorted(t for t, cfg in config.items() if cfg.get("watching"))


def _result_rows(data: dict) -> list[dict]:
    rows: list[dict] = []
    for key in ("results", "all_results"):
        chunk = data.get(key)
        if isinstance(chunk, list):
            rows.extend(chunk)
    return rows


def screener_covers_ticker(
    json_path: Path,
    ticker: str,
    watchlist_symbols: list[str],
) -> bool:
    """True when screener JSON already screened *ticker* (directly or via watchlist batch)."""
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
    reports_dir: Path,
    prefix: str,
    ticker: str,
    as_of: date,
    watchlist_symbols: list[str],
) -> Path | None:
    """Pick the newest same-day screener file that covers *ticker*."""
    if not reports_dir.exists():
        return None
    date_str = as_of.isoformat()
    matches = sorted(reports_dir.glob(f"{prefix}{date_str}_*.json"))
    for path in reversed(matches):
        if screener_covers_ticker(path, ticker, watchlist_symbols):
            return path
    return None


def extract_ticker_row(json_path: Path, ticker: str) -> dict | None:
    """Return the screener result row for *ticker*, if present."""
    try:
        data = json.loads(json_path.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    symbol = ticker.upper()
    for row in _result_rows(data):
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
    reports_dir = root / "reports"
    logs_dir = reports_dir / "logs"
    watchlist_symbols = load_watchlist_symbols(root / "config" / "research_watchlist.yaml")
    watchlist_arg = " ".join(watchlist_symbols) if watchlist_symbols else ticker.upper()

    ctx_path = market_context_path(logs_dir, as_of)
    fred_path = logs_dir / f"fred_calendar_{as_of.isoformat()}.json"

    artifacts: dict[str, dict[str, Any]] = {}

    if force_refresh:
        artifacts["market_context"] = _artifact_run(
            run_hint="uv run python3 scripts/pre_market.py",
        )
        for key, prefix in BATCH_PREFIXES.items():
            if key in ("vcp_screener", "canslim_screener"):
                skill_dir = "vcp-screener" if key == "vcp_screener" else "canslim-screener"
                script = "screen_vcp.py" if key == "vcp_screener" else "screen_canslim.py"
                artifacts[key] = _artifact_run(
                    run_hint=(
                        f"python3 skills/{skill_dir}/scripts/{script} "
                        f"--universe {watchlist_arg} --output-dir reports/"
                    ),
                )
            elif key != "breakout_trade_planner":
                artifacts[key] = _artifact_run()
        artifacts["breakout_trade_planner"] = _artifact_run(
            run_hint=(
                "python3 skills/breakout-trade-planner/scripts/plan_breakout_trades.py "
                "--input reports/vcp_screener_YYYY-MM-DD.json --output-dir reports/"
            ),
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

        breadth_path = find_latest_same_day(reports_dir, BATCH_PREFIXES["market_breadth"], as_of)
        uptrend_path = find_latest_same_day(reports_dir, BATCH_PREFIXES["uptrend_analysis"], as_of)
        if ctx_path and breadth_path is None:
            breadth_path = ctx_path  # embedded in market_context markdown
        if ctx_path and uptrend_path is None:
            uptrend_path = ctx_path

        artifacts["market_breadth"] = _artifact_reuse(breadth_path, root)
        artifacts["uptrend_analysis"] = _artifact_reuse(uptrend_path, root)
        artifacts["market_top"] = _artifact_reuse(
            find_latest_same_day(reports_dir, BATCH_PREFIXES["market_top"], as_of),
            root,
        )
        artifacts["exposure_posture"] = _artifact_reuse(
            find_latest_same_day(reports_dir, BATCH_PREFIXES["exposure_posture"], as_of),
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
            prefix = BATCH_PREFIXES[screener_key]
            skill_dir = screener_key.replace("_", "-")
            script = "screen_vcp.py" if screener_key == "vcp_screener" else "screen_canslim.py"
            screener_path = find_screener_for_ticker(
                reports_dir, prefix, ticker, as_of, watchlist_symbols
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
                    run_hint=(
                        f"python3 skills/{skill_dir}/scripts/{script} "
                        f"--universe {watchlist_arg} --output-dir reports/"
                    ),
                )

        artifacts["theme_detector"] = _artifact_reuse(
            find_latest_same_day(reports_dir, BATCH_PREFIXES["theme_detector"], as_of),
            root,
        )
        artifacts["breakout_trade_planner"] = _artifact_reuse(
            find_latest_same_day(reports_dir, BATCH_PREFIXES["breakout_trade_planner"], as_of),
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
