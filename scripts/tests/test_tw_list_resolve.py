"""Tests for TradeWhisperer list color stack resolver."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest
from report_paths import artifact_dir
from tw_list_resolve import (
    PERIODS,
    color_for_ticker,
    find_list,
    htf_fight,
    load_list,
    normalize_bucket,
    resolve_color_stack,
    shortlist,
)

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
RESOLVE_SCRIPT = SCRIPTS_DIR / "tw_list_resolve.py"


def _list_payload(
    *,
    period: str,
    as_of: str,
    buckets: dict[str, list[str]],
    ticker_index: dict[str, str] | None = None,
    bullish_pct: float = 60.0,
    bearish_pct: float = 40.0,
) -> dict:
    index = ticker_index
    if index is None:
        index = {}
        for color, tickers in buckets.items():
            for t in tickers:
                index[t.upper()] = normalize_bucket(color)
    return {
        "source": "tradewhisperer",
        "ticker": "MARKET",
        "as_of": as_of,
        "extracted": {
            "category": "list",
            "period": period,
            "as_of_list": as_of,
            "bullish_pct": bullish_pct,
            "bearish_pct": bearish_pct,
            "buckets": buckets,
            "ticker_index": index,
        },
    }


def _write_list(repo: Path, period: str, as_of: str, payload: dict) -> Path:
    tw_dir = artifact_dir(repo, "tradewhisperer_charts", mkdir=True)
    path = tw_dir / f"list_tw_{period}_{as_of}.json"
    path.write_text(json.dumps(payload))
    return path


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("BLUE", "BLUE"),
        ("blue-green", "BLUE_GREEN"),
        ("PINK-RED", "PINK_RED"),
        ("TRIM-OPTION", "TRIM_OPTION"),
        ("BLUE_GREEN", "BLUE_GREEN"),
        ("  pink  ", "PINK"),
    ],
)
def test_normalize_bucket(raw, expected):
    assert normalize_bucket(raw) == expected


def test_find_list_returns_newest_for_period(tmp_path: Path):
    as_of = date(2026, 8, 10)
    tw_dir = artifact_dir(tmp_path, "tradewhisperer_charts", mkdir=True)
    older = tw_dir / "list_tw_daily_2026-08-10.json"
    newer = tw_dir / "list_tw_daily_2026-08-10_b.json"
    older.write_text("{}")
    newer.write_text("{}")
    # weekly should not be selected
    (tw_dir / "list_tw_weekly_2026-08-10.json").write_text("{}")
    found = find_list(tmp_path, "daily", as_of)
    assert found == newer


def test_find_list_missing_returns_none(tmp_path: Path):
    artifact_dir(tmp_path, "tradewhisperer_charts", mkdir=True)
    assert find_list(tmp_path, "monthly", date(2026, 8, 10)) is None


def test_find_list_lookback_uses_latest_on_or_before(tmp_path: Path):
    """Weekly/monthly list titles often predate the session as_of."""
    tw_dir = artifact_dir(tmp_path, "tradewhisperer_charts", mkdir=True)
    (tw_dir / "list_tw_weekly_2026-08-07.json").write_text("{}")
    (tw_dir / "list_tw_weekly_2026-07-31.json").write_text("{}")
    (tw_dir / "list_tw_monthly_2026-07-31.json").write_text("{}")
    # Future weekly must not win
    (tw_dir / "list_tw_weekly_2026-08-14.json").write_text("{}")

    assert find_list(tmp_path, "weekly", date(2026, 8, 10)).name == (
        "list_tw_weekly_2026-08-07.json"
    )
    assert find_list(tmp_path, "monthly", date(2026, 8, 10)).name == (
        "list_tw_monthly_2026-07-31.json"
    )


def test_load_list_builds_index_from_buckets(tmp_path: Path):
    as_of = "2026-08-10"
    payload = _list_payload(
        period="daily",
        as_of=as_of,
        buckets={"BLUE-GREEN": ["cvx", "XOM"], "PINK": ["AMSC"]},
        ticker_index={},
    )
    # Force empty index so loader rebuilds
    payload["extracted"]["ticker_index"] = {}
    path = _write_list(tmp_path, "daily", as_of, payload)
    data = load_list(path)
    assert data["extracted"]["ticker_index"]["CVX"] == "BLUE_GREEN"
    assert data["extracted"]["ticker_index"]["XOM"] == "BLUE_GREEN"
    assert data["extracted"]["ticker_index"]["AMSC"] == "PINK"
    # buckets keys normalized
    assert "BLUE_GREEN" in data["extracted"]["buckets"]
    assert "BLUE-GREEN" not in data["extracted"]["buckets"]


def test_load_list_requires_buckets(tmp_path: Path):
    path = artifact_dir(tmp_path, "tradewhisperer_charts", mkdir=True) / "bad.json"
    path.write_text(json.dumps({"extracted": {"category": "list", "period": "daily"}}))
    with pytest.raises(ValueError, match="buckets"):
        load_list(path)


def test_color_for_ticker():
    data = _list_payload(
        period="daily",
        as_of="2026-08-10",
        buckets={"BLUE": ["CVX"], "GREEN": ["AAOI"]},
    )
    assert color_for_ticker(data, "cvx") == "BLUE"
    assert color_for_ticker(data, "MISSING") is None


def test_resolve_color_stack(tmp_path: Path):
    as_of = date(2026, 8, 10)
    _write_list(
        tmp_path,
        "daily",
        as_of.isoformat(),
        _list_payload(period="daily", as_of=as_of.isoformat(), buckets={"BLUE": ["UMAC"]}),
    )
    _write_list(
        tmp_path,
        "weekly",
        as_of.isoformat(),
        _list_payload(period="weekly", as_of=as_of.isoformat(), buckets={"GREEN": ["UMAC"]}),
    )
    # monthly absent
    stack = resolve_color_stack(tmp_path, "UMAC", as_of)
    assert stack["daily"] == "BLUE"
    assert stack["weekly"] == "GREEN"
    assert stack["monthly"] is None
    assert stack["sources"]["daily"].endswith("list_tw_daily_2026-08-10.json")
    assert stack["sources"]["weekly"].endswith("list_tw_weekly_2026-08-10.json")
    assert stack["sources"]["monthly"] is None


def test_shortlist_by_bias():
    data = _list_payload(
        period="daily",
        as_of="2026-08-10",
        buckets={
            "BLUE": ["A"],
            "BLUE_GREEN": ["B"],
            "GREEN": ["C"],
            "PINK": ["D"],
            "PINK_RED": ["E"],
            "RED": ["F"],
            "TRIM_OPTION": ["G"],
        },
    )
    assert shortlist(data, "long") == ["A", "B"]
    assert shortlist(data, "short") == ["D", "E"]
    assert shortlist(data, "either") == ["A", "B", "D", "E"]


def test_htf_fight_long_fierce_weekly_red():
    result = htf_fight(
        {"daily": "BLUE", "weekly": "RED", "monthly": None},
        "long",
    )
    assert result["fight"] is True
    assert result["fierce"] is True
    assert result["htf_absent"] is False
    assert result["score_guide"] == "zero"


def test_htf_fight_short_fierce_monthly_green():
    result = htf_fight(
        {"daily": "PINK", "weekly": None, "monthly": "GREEN"},
        "short",
    )
    assert result["fierce"] is True
    assert result["score_guide"] == "zero"


def test_htf_fight_absent_when_no_htf():
    result = htf_fight(
        {"daily": "BLUE", "weekly": None, "monthly": None},
        "long",
    )
    assert result["htf_absent"] is True
    assert result["fight"] is False
    assert result["score_guide"] == "full"


def test_htf_fight_aligned_stack():
    result = htf_fight(
        {"daily": "BLUE", "weekly": "GREEN", "monthly": "BLUE_GREEN"},
        "long",
    )
    assert result["fight"] is False
    assert result["fierce"] is False
    assert result["score_guide"] == "full"


def test_htf_fight_partial_mixed():
    # weekly continuation green ok; monthly pink start = mixed
    result = htf_fight(
        {"daily": "BLUE", "weekly": "GREEN", "monthly": "PINK"},
        "long",
    )
    assert result["fierce"] is False
    assert result["fight"] is True
    assert result["score_guide"] == "partial"


def test_cli_stack(tmp_path: Path):
    as_of = date(2026, 8, 10)
    _write_list(
        tmp_path,
        "daily",
        as_of.isoformat(),
        _list_payload(period="daily", as_of=as_of.isoformat(), buckets={"BLUE": ["CVX"]}),
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(RESOLVE_SCRIPT),
            "stack",
            "CVX",
            "--as-of",
            as_of.isoformat(),
            "--repo",
            str(tmp_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    assert out["ticker"] == "CVX"
    assert out["stack"]["daily"] == "BLUE"
    assert set(PERIODS) <= set(out["stack"])
