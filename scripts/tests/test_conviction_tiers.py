"""Tests for conviction tier assignment and dashboard enrichment."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest
import yaml
from conviction_tiers import (
    apply_tier_a_cap,
    compute_tier_for_ticker,
    enrich_dashboard_rows,
    is_buy_verdict,
    is_negative_verdict,
    parse_quick_glance,
    screener_is_strong,
    tier_order_key,
)
from research_watchlist import load_watchlist_config

QUICK_GLANCE_SAMPLE = """\
## Quick Glance

**Verdict:** **Buy on pullback** — quality name.
**Confidence:** **High** — solid data.
"""

QUICK_GLANCE_WATCH = """\
**Verdict:** **Watch** — wait for base.
**Confidence:** **Low** — thin coverage.
"""


def test_parse_quick_glance_buy():
    parsed = parse_quick_glance(QUICK_GLANCE_SAMPLE)
    assert "buy" in parsed["verdict"].lower()
    assert parsed["research_confidence"] == "High"


def test_parse_quick_glance_watch():
    parsed = parse_quick_glance(QUICK_GLANCE_WATCH)
    assert is_negative_verdict(parsed["verdict"])
    assert parsed["research_confidence"] == "Low"


def test_is_buy_verdict_variants():
    assert is_buy_verdict("**Buy on pullback** — reason")
    assert is_buy_verdict("Strong Buy — leader")
    assert not is_buy_verdict("Watch — wait")
    assert not is_buy_verdict("Avoid — broken")


def test_screener_is_strong_canslim():
    row = {"symbol": "GOOGL", "composite_score": 66.7, "rating": "Above Average"}
    assert screener_is_strong("canslim_screener", row) is True


def test_screener_is_strong_earnings():
    row = {"symbol": "X", "grade": "A", "composite_score": 80}
    assert screener_is_strong("earnings_trade_analyzer", row) is True
    row_b = {"symbol": "Y", "grade": "C"}
    assert screener_is_strong("earnings_trade_analyzer", row_b) is False


def test_tier_d_invalidated():
    result = compute_tier_for_ticker(
        ticker="XYZ",
        watching=True,
        thesis_status="INVALIDATED",
        confidence_score=None,
        days_stale=0,
        verdict="Buy",
        research_confidence="High",
        screener_strong=False,
        screener_summary="",
        market_gate="NEW_ENTRY_ALLOWED",
        tier_pin=None,
        has_report=True,
    )
    assert result.tier == "D"
    assert "invalidated" in " ".join(result.tier_reasons).lower()


def test_tier_d_not_watching_no_thesis():
    result = compute_tier_for_ticker(
        ticker="XYZ",
        watching=False,
        thesis_status="—",
        confidence_score=None,
        days_stale=None,
        verdict=None,
        research_confidence=None,
        screener_strong=False,
        screener_summary="",
        market_gate="NEW_ENTRY_ALLOWED",
        tier_pin=None,
        has_report=False,
    )
    assert result.tier == "D"


def test_tier_c_missing_report():
    result = compute_tier_for_ticker(
        ticker="DRAM",
        watching=True,
        thesis_status="—",
        confidence_score=None,
        days_stale=None,
        verdict=None,
        research_confidence=None,
        screener_strong=False,
        screener_summary="",
        market_gate="REDUCE_ONLY",
        tier_pin=None,
        has_report=False,
    )
    assert result.tier == "C"
    assert result.tier_score >= 0


def test_tier_a_entry_ready_high_confidence():
    result = compute_tier_for_ticker(
        ticker="VECO",
        watching=True,
        thesis_status="ENTRY_READY",
        confidence_score=0.8,
        days_stale=3,
        verdict="Buy on pullback",
        research_confidence="High",
        screener_strong=True,
        screener_summary="CANSLIM 70",
        market_gate="NEW_ENTRY_ALLOWED",
        tier_pin=None,
        has_report=True,
    )
    assert result.tier == "A"
    assert result.tier_score > 50


def test_tier_a_blocked_by_cash_priority():
    result = compute_tier_for_ticker(
        ticker="VECO",
        watching=True,
        thesis_status="ENTRY_READY",
        confidence_score=1.0,
        days_stale=1,
        verdict="Buy",
        research_confidence="High",
        screener_strong=True,
        screener_summary="",
        market_gate="CASH_PRIORITY",
        tier_pin=None,
        has_report=True,
    )
    assert result.tier == "B"
    assert any("cash_priority" in r.lower() for r in result.tier_reasons)


def test_tier_b_entry_ready_low_confidence():
    result = compute_tier_for_ticker(
        ticker="ABC",
        watching=True,
        thesis_status="ENTRY_READY",
        confidence_score=0.6,
        days_stale=5,
        verdict="Buy",
        research_confidence="Medium",
        screener_strong=False,
        screener_summary="",
        market_gate="NEW_ENTRY_ALLOWED",
        tier_pin=None,
        has_report=True,
    )
    assert result.tier == "B"


def test_tier_pin_floor_to_a():
    result = compute_tier_for_ticker(
        ticker="PIN",
        watching=True,
        thesis_status="IDEA",
        confidence_score=None,
        days_stale=5,
        verdict="Watch",
        research_confidence="Low",
        screener_strong=False,
        screener_summary="",
        market_gate="NEW_ENTRY_ALLOWED",
        tier_pin="A",
        has_report=True,
    )
    assert result.tier == "A"
    assert any("tier_pin" in r for r in result.tier_reasons)


def test_apply_tier_a_cap_demotes_overflow():
    rows = []
    for i in range(6):
        rows.append(
            {
                "ticker": f"T{i}",
                "tier": "A",
                "tier_score": 100 - i,
                "tier_reasons": [],
                "tier_a_capped": False,
            }
        )
    capped = apply_tier_a_cap(rows, cap=5)
    a_count = sum(1 for r in capped if r["tier"] == "A")
    assert a_count == 5
    demoted = [r for r in capped if r.get("tier_a_capped")]
    assert len(demoted) == 1
    assert demoted[0]["tier"] == "B"


def test_tier_order_key_sort():
    rows = [{"tier": "C", "tier_score": 10}, {"tier": "A", "tier_score": 5}]
    assert tier_order_key(rows[0]) > tier_order_key(rows[1])


@pytest.fixture
def tier_env(tmp_path: Path):
    state_dir = tmp_path / "state" / "theses"
    state_dir.mkdir(parents=True)
    research_dir = tmp_path / "reports" / "research"
    research_dir.mkdir(parents=True)
    watchlist_path = tmp_path / "config" / "research_watchlist.yaml"
    watchlist_path.parent.mkdir(parents=True)
    watchlist_path.write_text(
        yaml.dump(
            {
                "FOCUS": {"watching": True, "notes": "", "tier_pin": "A"},
                "PROBE": {"watching": True, "notes": ""},
            }
        )
    )
    (research_dir / "FOCUS_2026-05-31.md").write_text(QUICK_GLANCE_SAMPLE)
    thesis = {
        "ticker": "FOCUS",
        "status": "ENTRY_READY",
        "thesis_id": "th_focus_grw_20260531_abcd",
        "confidence_score": 0.8,
        "thesis_type": "growth_momentum",
        "thesis_statement": "test",
        "created_at": "2026-05-31T10:00:00-04:00",
        "updated_at": "2026-05-31T10:00:00-04:00",
        "status_history": [],
        "origin": {"skill": "manual"},
    }
    (state_dir / "th_focus.yaml").write_text(yaml.dump(thesis))
    exposure_dir = tmp_path / "reports" / "market" / "exposure"
    exposure_dir.mkdir(parents=True)
    (exposure_dir / "exposure_posture_2026-05-31_120000.json").write_text(
        json.dumps({"recommendation": "NEW_ENTRY_ALLOWED", "composite_score": 60})
    )
    return {
        "root": tmp_path,
        "state_dir": state_dir,
        "research_dir": research_dir,
        "watchlist_path": watchlist_path,
    }


def test_enrich_dashboard_rows_adds_tier(tier_env):
    base_rows = [
        {
            "ticker": "FOCUS",
            "last_report_date": "2026-05-31",
            "days_stale": 0,
            "report_path": tier_env["research_dir"] / "FOCUS_2026-05-31.md",
            "thesis_status": "ENTRY_READY",
            "watching": True,
            "eligibility": ["watchlist"],
            "queue_status": None,
            "prefetch_available": False,
            "prefetch_path": None,
            "ui_status": "fresh",
            "badge": "OK",
            "notes": "",
        }
    ]
    enriched = enrich_dashboard_rows(
        base_rows,
        tier_env["root"],
        date(2026, 5, 31),
        state_dir=tier_env["state_dir"],
        watchlist_path=tier_env["watchlist_path"],
    )
    assert enriched[0]["tier"] in ("A", "B")
    assert "tier_score" in enriched[0]
    assert "tier_reasons" in enriched[0]


def test_load_watchlist_config_tier_pin(tmp_path: Path):
    path = tmp_path / "watchlist.yaml"
    path.write_text("AAA:\n  watching: true\n  tier_pin: B\n  notes: ''\n")
    cfg = load_watchlist_config(path)
    assert cfg["AAA"]["tier_pin"] == "B"
