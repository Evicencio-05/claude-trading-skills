"""Tests for TradeWhisperer list color stack resolver."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest
import yaml
from report_paths import artifact_dir
from tw_list_resolve import (
    PERIODS,
    VS_BENCHMARK,
    color_for_ticker,
    compare_to_benchmark,
    find_list,
    htf_fight,
    load_list,
    load_sector_map,
    normalize_bucket,
    rank_overlap,
    resolve_benchmark,
    resolve_color_stack,
    score_overlap,
    shortlist,
    write_pending_stubs,
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


def test_score_overlap_prefers_3tf_aligned_trigger():
    trigger = score_overlap({"daily": "BLUE_GREEN", "weekly": "GREEN", "monthly": "GREEN"})
    continuation = score_overlap({"daily": "GREEN", "weekly": "GREEN", "monthly": "GREEN"})
    mixed = score_overlap({"daily": "GREEN", "weekly": "RED", "monthly": "GREEN"})
    partial = score_overlap({"daily": "BLUE", "weekly": "GREEN", "monthly": None})
    assert trigger["camp"] == "bull"
    assert trigger["all_three"] is True
    assert trigger["daily_trigger"] is True
    assert trigger["score"] > continuation["score"]
    assert continuation["score"] > partial["score"]
    assert mixed["camp"] == "mixed"
    assert mixed["score"] < partial["score"]


def test_score_overlap_bear_trigger():
    result = score_overlap({"daily": "PINK_RED", "weekly": "RED", "monthly": "RED"})
    assert result["camp"] == "bear"
    assert result["daily_trigger"] is True
    assert result["all_three"] is True


def _sector_map_payload() -> dict:
    return {
        "benchmarks": {
            "XLE": {"name": "Energy", "class": "sector"},
            "XLK": {"name": "Technology", "class": "sector"},
            "SPY": {"name": "S&P 500", "class": "index"},
        },
        "tickers": {
            "CVX": {"benchmark": "XLE", "class": "equity"},
            "XOM": {"benchmark": "XLE", "class": "equity"},
            "AAPL": {"benchmark": "XLK", "class": "equity"},
        },
        "pending": {},
    }


def test_load_sector_map_and_resolve_benchmark(tmp_path: Path):
    path = tmp_path / "tw_sector_map.yaml"
    path.write_text(yaml.safe_dump(_sector_map_payload()), encoding="utf-8")
    data = load_sector_map(path)
    assert resolve_benchmark(data, "CVX") == {
        "benchmark": "XLE",
        "class": "equity",
        "source": "tickers",
    }
    assert resolve_benchmark(data, "xle") == {
        "benchmark": "XLE",
        "class": "sector",
        "source": "benchmarks",
    }
    assert resolve_benchmark(data, "ZZZZ") is None


def test_compare_to_benchmark_statuses():
    ticker = {"daily": "BLUE_GREEN", "weekly": "GREEN", "monthly": "GREEN"}
    aligned = {"daily": "GREEN", "weekly": "GREEN", "monthly": "GREEN"}
    assert compare_to_benchmark(ticker, aligned) == "leading"

    same_trigger = {"daily": "BLUE_GREEN", "weekly": "GREEN", "monthly": "GREEN"}
    assert compare_to_benchmark(ticker, same_trigger) == "aligned"

    lag = {"daily": "BLUE", "weekly": "BLUE_GREEN", "monthly": "GREEN"}
    assert (
        compare_to_benchmark(
            {"daily": "GREEN", "weekly": "GREEN", "monthly": "GREEN"},
            lag,
        )
        in VS_BENCHMARK
    )

    divergent = {"daily": "RED", "weekly": "RED", "monthly": "RED"}
    assert compare_to_benchmark(ticker, divergent) == "divergent"
    assert compare_to_benchmark(ticker, None) == "benchmark_absent"
    assert compare_to_benchmark(ticker, {"daily": None, "weekly": None, "monthly": None}) == (
        "benchmark_absent"
    )


def test_compare_to_benchmark_leading_vs_lagging():
    # Ticker has daily trigger; bench is continuation only → leading
    assert (
        compare_to_benchmark(
            {"daily": "BLUE_GREEN", "weekly": "GREEN", "monthly": "GREEN"},
            {"daily": "GREEN", "weekly": "GREEN", "monthly": "GREEN"},
        )
        == "leading"
    )
    # Ticker continuation; bench has trigger → lagging
    assert (
        compare_to_benchmark(
            {"daily": "GREEN", "weekly": "GREEN", "monthly": "GREEN"},
            {"daily": "BLUE_GREEN", "weekly": "GREEN", "monthly": "GREEN"},
        )
        == "lagging"
    )


def test_write_pending_stubs(tmp_path: Path):
    path = tmp_path / "tw_sector_map.yaml"
    path.write_text(yaml.safe_dump(_sector_map_payload()), encoding="utf-8")
    added = write_pending_stubs(path, ["CVX", "NEWCO", "xle", "NEWCO"])
    assert added == ["NEWCO"]
    reloaded = load_sector_map(path)
    assert "NEWCO" in reloaded["pending"]
    assert reloaded["pending"]["NEWCO"]["benchmark"] is None
    assert reloaded["pending"]["NEWCO"]["class"] == "unknown"
    # Second pass is idempotent
    assert write_pending_stubs(path, ["NEWCO", "OTHER"]) == ["OTHER"]


def test_rank_overlap_with_sector_compare(tmp_path: Path):
    as_of = date(2026, 8, 10)
    _write_list(
        tmp_path,
        "daily",
        as_of.isoformat(),
        _list_payload(
            period="daily",
            as_of=as_of.isoformat(),
            buckets={
                "BLUE_GREEN": ["CVX", "XOM"],
                "GREEN": ["XLE", "ZZZZ"],
                "RED": ["AAPL"],
            },
        ),
    )
    _write_list(
        tmp_path,
        "weekly",
        as_of.isoformat(),
        _list_payload(
            period="weekly",
            as_of=as_of.isoformat(),
            buckets={"GREEN": ["CVX", "XOM", "XLE", "ZZZZ"], "RED": ["AAPL"]},
        ),
    )
    _write_list(
        tmp_path,
        "monthly",
        as_of.isoformat(),
        _list_payload(
            period="monthly",
            as_of=as_of.isoformat(),
            buckets={"GREEN": ["CVX", "XOM", "XLE"], "RED": ["AAPL"]},
        ),
    )
    map_path = tmp_path / "config" / "tw_sector_map.yaml"
    map_path.parent.mkdir(parents=True)
    map_path.write_text(yaml.safe_dump(_sector_map_payload()), encoding="utf-8")

    result = rank_overlap(
        tmp_path,
        as_of,
        bias="either",
        top=10,
        map_path=map_path,
    )
    tickers = [r["ticker"] for r in result["ranked"]]
    assert "CVX" in tickers
    assert "XOM" in tickers
    # Benchmarks themselves are excluded from ranked compare rows
    assert "XLE" not in tickers
    cvx = next(r for r in result["ranked"] if r["ticker"] == "CVX")
    assert cvx["benchmark"] == "XLE"
    assert cvx["vs_benchmark"] in ("aligned", "leading")
    assert cvx["benchmark_stack"]["daily"] == "GREEN"
    assert "ZZZZ" in result["unmapped"]


def test_cli_overlap_writes_artifacts(tmp_path: Path):
    as_of = date(2026, 8, 10)
    _write_list(
        tmp_path,
        "daily",
        as_of.isoformat(),
        _list_payload(
            period="daily",
            as_of=as_of.isoformat(),
            buckets={"BLUE_GREEN": ["CVX"], "GREEN": ["XLE"]},
        ),
    )
    _write_list(
        tmp_path,
        "weekly",
        as_of.isoformat(),
        _list_payload(
            period="weekly",
            as_of=as_of.isoformat(),
            buckets={"GREEN": ["CVX", "XLE"]},
        ),
    )
    _write_list(
        tmp_path,
        "monthly",
        as_of.isoformat(),
        _list_payload(
            period="monthly",
            as_of=as_of.isoformat(),
            buckets={"GREEN": ["CVX", "XLE"]},
        ),
    )
    map_path = tmp_path / "config" / "tw_sector_map.yaml"
    map_path.parent.mkdir(parents=True)
    map_path.write_text(yaml.safe_dump(_sector_map_payload()), encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            str(RESOLVE_SCRIPT),
            "overlap",
            "--as-of",
            as_of.isoformat(),
            "--bias",
            "either",
            "--top",
            "5",
            "--map",
            str(map_path),
            "--repo",
            str(tmp_path),
            "--write-pending",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    assert out["as_of"] == as_of.isoformat()
    assert "ranked" in out
    json_path = (
        artifact_dir(tmp_path, "tradewhisperer_charts") / f"overlap_tw_{as_of.isoformat()}.json"
    )
    md_path = json_path.with_suffix(".md")
    assert json_path.is_file()
    assert md_path.is_file()


def test_cli_map_lookup(tmp_path: Path):
    map_path = tmp_path / "tw_sector_map.yaml"
    map_path.write_text(yaml.safe_dump(_sector_map_payload()), encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable,
            str(RESOLVE_SCRIPT),
            "map-lookup",
            "CVX",
            "--map",
            str(map_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    assert out["ticker"] == "CVX"
    assert out["benchmark"] == "XLE"
