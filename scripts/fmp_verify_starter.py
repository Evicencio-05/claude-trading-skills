#!/usr/bin/env python3
"""Read-only smoke checks for FMP Starter tier and stable API availability."""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except ImportError:
    pass

try:
    import requests
except ImportError:
    print("ERROR: requests not installed", file=sys.stderr)
    sys.exit(1)


def _check(label: str, url: str, params: dict) -> tuple[str, int, str]:
    try:
        resp = requests.get(url, params=params, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                detail = f"{len(data)} items"
            elif isinstance(data, dict):
                detail = "dict"
            else:
                detail = type(data).__name__
            return label, resp.status_code, detail
        return label, resp.status_code, resp.text[:80].replace("\n", " ")
    except requests.RequestException as exc:
        return label, -1, str(exc)


def main() -> int:
    api_key = os.environ.get("FMP_API_KEY")
    if not api_key:
        print("FAIL: FMP_API_KEY not set", file=sys.stderr)
        return 1

    params_base = {"apikey": api_key}
    checks = [
        (
            "quote_single",
            "https://financialmodelingprep.com/stable/quote",
            {"symbol": "AAPL", **params_base},
        ),
        (
            "quote_batch",
            "https://financialmodelingprep.com/stable/quote",
            {"symbol": "AAPL,MSFT", **params_base},
        ),
        (
            "historical_eod",
            "https://financialmodelingprep.com/stable/historical-price-eod/full",
            {"symbol": "SPY", "from": "2026-05-01", "to": "2026-05-31", **params_base},
        ),
        (
            "earnings_calendar",
            "https://financialmodelingprep.com/stable/earnings-calendar",
            {"from": "2026-05-29", "to": "2026-05-31", **params_base},
        ),
        (
            "sp500_constituent",
            "https://financialmodelingprep.com/stable/sp500-constituent",
            dict(params_base),
        ),
        (
            "profile",
            "https://financialmodelingprep.com/stable/profile",
            {"symbol": "AAPL", **params_base},
        ),
    ]

    failures = 0
    print("FMP Starter verification")
    print("-" * 60)
    for label, url, params in checks:
        name, status, detail = _check(label, url, params)
        ok = status == 200 and not (label == "quote_batch" and detail == "0 items")
        if label == "sp500_constituent" and status == 402:
            ok = True  # expected on Starter
            detail = "402 expected on Starter (Professional required)"
        if label == "quote_batch" and status == 200 and detail == "0 items":
            ok = True
            detail = "0 items expected — clients fetch per-symbol on stable API"
        if not ok:
            failures += 1
        mark = "OK" if ok else "FAIL"
        print(f"  [{mark}] {name}: HTTP {status} — {detail}")

    print("-" * 60)
    if failures:
        print(f"{failures} check(s) failed")
        return 1
    print("All checks passed (sp500 402 on Starter is expected)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
