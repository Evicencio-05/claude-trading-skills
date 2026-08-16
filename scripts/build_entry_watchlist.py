#!/usr/bin/env python3
"""Build daily entry watchlist JSON + markdown from conviction tiers."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from conviction_tiers import (  # noqa: E402
    build_entry_watchlist_payload,
    format_entry_watchlist_markdown,
)
from report_paths import logs_dir
from research_watchlist import get_repo_root


def main() -> int:
    parser = argparse.ArgumentParser(description="Build entry watchlist report")
    parser.add_argument(
        "--as-of",
        type=str,
        default=None,
        help="Date YYYY-MM-DD (default: today)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory (default: reports/logs)",
    )
    args = parser.parse_args()

    as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    repo_root = get_repo_root()
    out_dir = Path(args.output_dir) if args.output_dir else logs_dir(repo_root)
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = build_entry_watchlist_payload(repo_root, as_of)
    date_str = as_of.isoformat()
    json_path = out_dir / f"entry_watchlist_{date_str}.json"
    md_path = out_dir / f"entry_watchlist_{date_str}.md"

    json_path.write_text(json.dumps(payload, indent=2, default=str))
    md_path.write_text(format_entry_watchlist_markdown(payload))

    counts = payload.get("counts") or {}
    print(
        f"Wrote {json_path.relative_to(repo_root)} "
        f"(A={counts.get('A', 0)} B={counts.get('B', 0)} "
        f"C={counts.get('C', 0)} D={counts.get('D', 0)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
