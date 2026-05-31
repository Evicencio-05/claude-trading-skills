#!/usr/bin/env python3
"""
research_preflight.py — PASS 0 manifest for deep-research (zero LLM).

Resolves same-day batch artifacts (market context, screeners, etc.) so
Pass 1 reuses cached outputs instead of re-running FMP-heavy skills.

Usage:
    uv run python3 scripts/research_preflight.py --ticker VECO
    uv run python3 scripts/research_preflight.py --ticker VECO --force-refresh
    uv run python3 scripts/research_preflight.py --ticker VECO --as-of 2026-05-31

Output:
    reports/logs/research_preflight_{TICKER}_{YYYY-MM-DD}.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from research_artifacts import build_preflight_manifest  # noqa: E402
from research_watchlist import get_repo_root  # noqa: E402


def _print_summary(manifest: dict) -> None:
    ticker = manifest["ticker"]
    as_of = manifest["as_of"]
    summary = manifest.get("summary", {})
    print(f"Preflight {ticker} @ {as_of}")
    print(f"  reuse: {summary.get('reuse', 0)}  run: {summary.get('run', 0)}")
    for name, entry in manifest.get("artifacts", {}).items():
        action = entry["action"]
        path = entry.get("path", "")
        suffix = f" -> {path}" if path else ""
        reason = entry.get("reason")
        if reason:
            suffix = f" ({reason}){suffix}"
        print(f"  {name}: {action}{suffix}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deep-research PASS 0 artifact manifest")
    parser.add_argument("--ticker", required=True, help="Ticker symbol")
    parser.add_argument("--as-of", dest="as_of", help="Override date (YYYY-MM-DD)")
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Mark all batch artifacts for re-run (ignore same-day cache)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Manifest output path (default: reports/logs/research_preflight_TICKER_DATE.json)",
    )
    args = parser.parse_args()

    as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    ticker = args.ticker.upper()
    repo = get_repo_root()

    manifest = build_preflight_manifest(
        ticker,
        as_of,
        force_refresh=args.force_refresh,
        repo_root=repo,
    )

    if args.output:
        out_path = Path(args.output)
    else:
        logs = repo / "reports" / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        out_path = logs / f"research_preflight_{ticker}_{as_of.isoformat()}.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2) + "\n")

    _print_summary(manifest)
    print(f"\nManifest: {out_path.relative_to(repo)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
