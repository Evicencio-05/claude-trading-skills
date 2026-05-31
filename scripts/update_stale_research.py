#!/usr/bin/env python3
"""
update_stale_research.py — Zero-LLM staleness scan for deep-research reports.

Finds eligible tickers (open positions + watchlist), flags stale reports,
writes a queue JSON for synthesis workflows, and optionally prefetches
scriptable market data.

Usage:
    uv run python3 scripts/update_stale_research.py --dry-run
    uv run python3 scripts/update_stale_research.py
    uv run python3 scripts/update_stale_research.py --prefetch
    uv run python3 scripts/update_stale_research.py --threshold 14 --ticker MRAM

Exit codes:
    0 — success, no stale tickers
    1 — error
    2 — stale tickers found (needs update or deep research)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from research_watchlist import (  # noqa: E402
    build_staleness_rows,
    eligibility_for_tickers,
    eligible_tickers,
    get_repo_root,
    resolve_exclude_path_for_filter,
)

REPO = get_repo_root()
STATE_DIR = REPO / "state" / "theses"
RESEARCH_DIR = REPO / "reports" / "research"
LOGS_DIR = REPO / "reports" / "logs"
PREFETCH_DIR = LOGS_DIR / "research_prefetch"
QUEUE_PATH = REPO / "state" / "research_update_queue.json"
WATCHLIST_PATH = REPO / "config" / "research_watchlist.yaml"
WATCHLIST_EXAMPLE = REPO / "config" / "research_watchlist.yaml.example"
SCRIPTS = REPO / "scripts"


def resolve_watchlist_path() -> Path:
    if WATCHLIST_PATH.exists():
        return WATCHLIST_PATH
    return WATCHLIST_EXAMPLE


def stale_rows(all_rows: list[dict]) -> list[dict]:
    return [r for r in all_rows if r["needs_update"]]


def format_table(rows: list[dict]) -> str:
    header = f"{'Ticker':<8} {'Last Report':<12} {'Days':<6} {'Status':<20} {'Eligibility'}"
    lines = [header, "-" * len(header)]
    for row in rows:
        days = str(row["days_stale"]) if row["days_stale"] is not None else "-"
        last = row["last_report"] or "-"
        lines.append(f"{row['ticker']:<8} {last:<12} {days:<6} {row['status']:<20} {row['reason']}")
    return "\n".join(lines)


def cursor_lines(rows: list[dict]) -> list[str]:
    lines: list[str] = []
    for row in rows:
        ticker = row["ticker"]
        if row["status"] == "needs_deep_research":
            lines.append(f"Follow commands/deep-research.md for {ticker}")
        elif row["status"] == "needs_update":
            lines.append(f"Follow commands/update-research.md for {ticker}")
    return lines


def write_summary(rows: list[dict], as_of: date, threshold: int, path: Path) -> None:
    stale = stale_rows(rows)
    lines = [
        f"# Research Staleness Scan — {as_of.isoformat()}",
        "",
        f"**Threshold:** {threshold} calendar days",
        f"**Eligible tickers:** {len(rows)}",
        f"**Needs action:** {len(stale)}",
        "",
        "## All Eligible Tickers",
        "",
        "```",
        format_table(rows),
        "```",
        "",
    ]
    if stale:
        lines.extend(["## Stale / Missing Reports", ""])
        lines.extend(f"- **{r['ticker']}** — {r['status']} ({r['reason']})" for r in stale)
        lines.extend(["", "## Cursor / Agent Commands", ""])
        lines.extend(f"- `{line}`" for line in cursor_lines(stale))
    else:
        lines.append("All eligible tickers are current.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def write_queue(
    rows: list[dict],
    as_of: date,
    threshold: int,
    prefetch_paths: dict[str, str | None],
) -> None:
    tickers = []
    for row in stale_rows(rows):
        tickers.append(
            {
                "ticker": row["ticker"],
                "last_report": row["last_report"],
                "days_stale": row["days_stale"],
                "eligibility": row["eligibility"],
                "status": row["status"],
                "prefetch_path": prefetch_paths.get(row["ticker"]),
            }
        )
    payload = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "threshold_days": threshold,
        "tickers": tickers,
    }
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text(json.dumps(payload, indent=2) + "\n")


def _parse_market_posture(markdown: str) -> dict[str, str]:
    for heading in ("## Executive Summary", "## Market Posture"):
        block_match = re.search(rf"{re.escape(heading)}\s+```(.*?)```", markdown, re.DOTALL)
        if block_match:
            fields: dict[str, str] = {}
            for line in block_match.group(1).splitlines():
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip()
            return fields
    return {}


def _posture_from_summary(summary: dict) -> dict[str, str]:
    syn = summary.get("synthesis") or {}
    b = summary.get("breadth") or {}
    u = summary.get("uptrend") or {}
    s = summary.get("sector") or {}
    flags = summary.get("position_flags") or {}
    all_flags = (flags.get("urgent") or []) + (flags.get("watch") or [])
    macro = summary.get("macro_events") or "none"
    return {
        "Posture": syn.get("posture", ""),
        "Ceiling": syn.get("ceiling", ""),
        "Headline": syn.get("headline", ""),
        "Breadth": f"{b.get('score', 'N/A')}/100 ({b.get('zone', 'N/A')})",
        "Uptrend": f"{u.get('score', 'N/A')}/100",
        "Uptrend warning": u.get("warning_summary", "none"),
        "Leading sector": s.get("leading_sector") or "N/A",
        "Cycle phase": s.get("cycle_phase") or "N/A",
        "Macro events": macro if macro != "none" else "none",
        "Flags": "\n".join(all_flags) if all_flags else "none",
    }


def load_market_context(as_of: date) -> dict | None:
    json_path = LOGS_DIR / f"market_context_{as_of.isoformat()}.json"
    if json_path.exists():
        try:
            summary = json.loads(json_path.read_text())
            if isinstance(summary, dict):
                return {
                    "path": str(json_path.relative_to(REPO)),
                    "posture": _posture_from_summary(summary),
                    "summary": summary,
                }
        except (json.JSONDecodeError, OSError):
            pass

    md_path = LOGS_DIR / f"market_context_{as_of.isoformat()}.md"
    if not md_path.exists():
        return None
    text = md_path.read_text()
    return {"path": str(md_path.relative_to(REPO)), "posture": _parse_market_posture(text)}


def run_fred_calendar(days: int = 7) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "fred_calendar.py"), "--days", str(days)],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    if result.returncode != 0:
        return f"ERROR: {result.stderr.strip() or result.stdout.strip()}"
    return result.stdout.strip()


def fetch_fmp_quote(ticker: str) -> dict | None:
    api_key = os.environ.get("FMP_API_KEY")
    if not api_key:
        return None
    try:
        import requests
    except ImportError:
        return {"error": "requests not installed"}

    urls = [
        (
            "https://financialmodelingprep.com/stable/quote",
            {"symbol": ticker, "apikey": api_key},
        ),
        (
            f"https://financialmodelingprep.com/api/v3/quote/{ticker}",
            {"apikey": api_key},
        ),
    ]
    for url, params in urls:
        try:
            resp = requests.get(url, params=params, timeout=15)
            if resp.status_code == 403:
                continue
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, list) and data:
                return data[0]
            if isinstance(data, dict) and data:
                return data
        except Exception as exc:  # noqa: BLE001
            return {"error": str(exc)}
    return {"error": "quote unavailable"}


def prefetch_ticker(ticker: str, as_of: date) -> tuple[dict, Path]:
    payload: dict = {
        "ticker": ticker,
        "fetched_at": datetime.now().astimezone().isoformat(),
        "market_context": load_market_context(as_of),
        "fred_calendar": run_fred_calendar(),
        "quote": fetch_fmp_quote(ticker),
    }
    PREFETCH_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PREFETCH_DIR / f"{ticker}_{as_of.isoformat()}.json"
    out_path.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    return payload, out_path


def run_prefetch(rows: list[dict], as_of: date) -> dict[str, str | None]:
    paths: dict[str, str | None] = {}
    for row in stale_rows(rows):
        ticker = row["ticker"]
        try:
            _, out_path = prefetch_ticker(ticker, as_of)
            paths[ticker] = str(out_path.relative_to(REPO))
            print(f"  prefetched {ticker} -> {paths[ticker]}")
        except Exception as exc:  # noqa: BLE001
            print(f"  WARNING: prefetch failed for {ticker}: {exc}", file=sys.stderr)
            paths[ticker] = None
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan stale deep-research reports")
    parser.add_argument("--dry-run", action="store_true", help="Print table, no writes")
    parser.add_argument(
        "--prefetch", action="store_true", help="Fetch scriptable data for stale tickers"
    )
    parser.add_argument("--threshold", type=int, default=14, help="Staleness threshold in days")
    parser.add_argument("--ticker", help="Limit scan to a single ticker")
    parser.add_argument("--as-of", dest="as_of", help="Override as-of date (YYYY-MM-DD)")
    args = parser.parse_args()

    as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    watchlist_path = resolve_watchlist_path()
    exclude_path = resolve_exclude_path_for_filter()

    eligibility_map = eligibility_for_tickers(STATE_DIR, watchlist_path, exclude_path=exclude_path)
    tickers = eligible_tickers(STATE_DIR, watchlist_path, exclude_path=exclude_path)
    if args.ticker:
        ticker = args.ticker.upper()
        if ticker not in eligibility_map:
            print(
                f"ERROR: {ticker} is not eligible (no position/watchlist match)",
                file=sys.stderr,
            )
            return 1
        tickers = [ticker]

    rows = build_staleness_rows(
        tickers=tickers,
        research_dir=RESEARCH_DIR,
        as_of=as_of,
        threshold_days=args.threshold,
        eligibility_map=eligibility_map,
    )

    print(format_table(rows))
    print()
    stale = stale_rows(rows)
    print(f"Eligible: {len(rows)} | Needs action: {len(stale)}")

    if args.dry_run:
        if stale:
            print("\nCursor commands:")
            for line in cursor_lines(stale):
                print(f"  {line}")
        print("\n[DRY RUN — nothing written]")
        return 2 if stale else 0

    prefetch_paths: dict[str, str | None] = {}
    if args.prefetch and stale:
        print("\nPrefetching scriptable data...")
        prefetch_paths = run_prefetch(rows, as_of)

    write_queue(rows, as_of, args.threshold, prefetch_paths)
    summary_path = LOGS_DIR / f"research_staleness_{as_of.isoformat()}.md"
    write_summary(rows, as_of, args.threshold, summary_path)

    print(f"\nQueue: {QUEUE_PATH.relative_to(REPO)}")
    print(f"Summary: {summary_path.relative_to(REPO)}")
    return 2 if stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
