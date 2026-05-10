#!/usr/bin/env python3
"""
FRED Economic Calendar — free-tier replacement for economic-calendar-fetcher.

FMP's /stable/economics-calendar endpoint silently returns [] on free tier
(post-Aug 2025 accounts). This script covers FOMC, CPI, NFP, PPI, and
GDP release dates using FRED API (key is free: fred.stlouisfed.org/docs/api/api_key.html).

FOMC dates are hard-coded for 2026 (from federalreserve.gov — announced ~1 year
in advance) so the script returns meeting dates even without a FRED key.

Usage:
  python3 scripts/fred_calendar.py
  python3 scripts/fred_calendar.py --from 2026-06-01 --to 2026-08-31 --format text
  python3 scripts/fred_calendar.py --api-key YOUR_KEY --output reports/calendar.json
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

# FOMC announcement dates for 2026 (second day of each meeting).
# Source: federalreserve.gov/monetarypolicy/fomccalendars.htm
# Update this list annually.
FOMC_2026 = [
    "2026-01-28",
    "2026-03-18",
    "2026-05-07",
    "2026-06-17",
    "2026-07-29",
    "2026-09-16",
    "2026-10-28",
    "2026-12-09",
]

# FRED release IDs for key US macro data (BLS-published series).
# FRED API docs: fred.stlouisfed.org/docs/api/fred/release_dates.html
FRED_RELEASES = {
    "CPI (Consumer Price Index)": {
        "release_id": 10,
        "impact": "High",
    },
    "Employment Situation (NFP)": {
        "release_id": 50,
        "impact": "High",
    },
    "PPI (Producer Price Index)": {
        "release_id": 99,
        "impact": "Medium",
    },
    "GDP Advance Estimate": {
        "release_id": 53,
        "impact": "High",
    },
    "Retail Sales": {
        "release_id": 78,
        "impact": "Medium",
    },
}

FRED_BASE = "https://api.stlouisfed.org/fred"


def fetch_fred_release_dates(
    release_id: int, from_date: str, to_date: str, api_key: str
) -> list[str]:
    params = {
        "release_id": release_id,
        "realtime_start": from_date,
        "realtime_end": to_date,
        "include_release_dates_with_no_data": "true",
        "api_key": api_key,
        "file_type": "json",
    }
    url = f"{FRED_BASE}/release/dates?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return [d["date"] for d in data.get("release_dates", [])]
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"  FRED release {release_id} HTTP {e.code}: {body[:120]}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"  FRED release {release_id} error: {e}", file=sys.stderr)
        return []


def build_events(from_date: str, to_date: str, api_key: str | None) -> list[dict]:
    events = []

    # FOMC dates — always available (hard-coded, no API needed)
    for date in FOMC_2026:
        if from_date <= date <= to_date:
            events.append(
                {
                    "date": date,
                    "event": "FOMC Rate Decision",
                    "country": "US",
                    "currency": "USD",
                    "impact": "High",
                    "source": "Federal Reserve (hard-coded)",
                    "previous": None,
                    "estimate": None,
                    "actual": None,
                }
            )

    # FRED-sourced releases (require API key)
    if api_key:
        for event_name, meta in FRED_RELEASES.items():
            dates = fetch_fred_release_dates(meta["release_id"], from_date, to_date, api_key)
            for date in dates:
                events.append(
                    {
                        "date": date,
                        "event": event_name,
                        "country": "US",
                        "currency": "USD",
                        "impact": meta["impact"],
                        "source": f"FRED release {meta['release_id']}",
                        "previous": None,
                        "estimate": None,
                        "actual": None,
                    }
                )
    else:
        print(
            "Note: FRED_API_KEY not set — showing FOMC dates only.\n"
            "  Get a free key at fred.stlouisfed.org/docs/api/api_key.html\n"
            "  Then: export FRED_API_KEY=your_key",
            file=sys.stderr,
        )

    events.sort(key=lambda e: e["date"])
    return events


def format_text(events: list[dict], from_date: str, to_date: str) -> str:
    high_count = sum(1 for e in events if e["impact"] == "High")
    lines = [
        f"Economic Calendar (FRED) — {from_date} to {to_date}",
        f"Total: {len(events)} events  |  High impact: {high_count}",
        "=" * 70,
    ]
    for e in events:
        lines.append(f"\nDate: {e['date']}")
        lines.append(f"Event: {e['event']}  [{e['impact']}]")
        lines.append(f"Country: {e['country']}  |  Currency: {e['currency']}")
        if e.get("source"):
            lines.append(f"Source: {e['source']}")
        lines.append("-" * 70)
    if not events:
        lines.append("\n(No events found for this date range)")
    return "\n".join(lines)


def main() -> None:
    today = datetime.now().date()
    default_to = today + timedelta(days=30)

    parser = argparse.ArgumentParser(
        description="Fetch FOMC/CPI/NFP dates from FRED (free-tier replacement for economic-calendar-fetcher)"
    )
    parser.add_argument("--from", dest="from_date", default=today.strftime("%Y-%m-%d"))
    parser.add_argument("--to", dest="to_date", default=default_to.strftime("%Y-%m-%d"))
    parser.add_argument(
        "--api-key",
        dest="api_key",
        help="FRED API key (overrides FRED_API_KEY env var)",
    )
    parser.add_argument("--format", choices=["json", "text"], default="text")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("FRED_API_KEY")

    print(
        f"Fetching economic calendar {args.from_date} to {args.to_date}...",
        file=sys.stderr,
    )
    events = build_events(args.from_date, args.to_date, api_key)
    print(f"Found {len(events)} events", file=sys.stderr)

    if args.format == "json":
        output = json.dumps(events, indent=2, ensure_ascii=False)
    else:
        output = format_text(events, args.from_date, args.to_date)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
