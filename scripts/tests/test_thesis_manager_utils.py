"""Tests for thesis-manager pure helpers in tools/thesis-manager/utils.py."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TM_DIR = ROOT / "tools" / "thesis-manager"
sys.path.insert(0, str(TM_DIR))

import utils  # noqa: E402

# ── fmt_account ───────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("", "—"),
        ("robinhood_taxable", "robinhood_taxable"),
        ("https://api.robinhood.com/accounts/abc123/", "rh:abc123"),
        ("https://api.robinhood.com/accounts/abc123", "rh:abc123"),
    ],
)
def test_fmt_account(raw: str, expected: str) -> None:
    assert utils.fmt_account(raw) == expected


# ── IRA eligibility ───────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("account", "strategy", "eligible"),
    [
        ("ira_robinhood", "long_call", True),
        ("ira_robinhood", "long_put", True),
        ("ira_robinhood", "", True),
        ("ira_robinhood", "short_call", False),
        ("ira_robinhood", "iron_condor", False),
        ("robinhood_taxable", "iron_condor", True),
        ("lucid_eval", "long_call", True),
    ],
)
def test_ira_options_eligible(account: str, strategy: str, eligible: bool) -> None:
    assert utils.ira_options_eligible(account, strategy) is eligible


def test_ira_badge_html_taxable_returns_none() -> None:
    assert utils.ira_badge_html("robinhood_taxable", "long_call") is None


def test_ira_badge_html_ira_ineligible_contains_warning() -> None:
    html = utils.ira_badge_html("ira_robinhood", "iron_condor")
    assert html is not None
    assert "NOT IRA Eligible" in html


# ── days_to_expiry ────────────────────────────────────────────────────────────


def test_days_to_expiry_past() -> None:
    assert utils.days_to_expiry("2026-05-20", as_of=date(2026, 5, 28)) == -8


def test_days_to_expiry_today() -> None:
    assert utils.days_to_expiry("2026-05-28", as_of=date(2026, 5, 28)) == 0


def test_days_to_expiry_invalid_returns_none() -> None:
    assert utils.days_to_expiry("not-a-date") is None
    assert utils.days_to_expiry(None) is None


# ── parse_price ───────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("12.50", 12.5),
        ("$12.50", 12.5),
        ("  $ 3.25 ", 3.25),
        ("below $50", None),
        ("", None),
    ],
)
def test_parse_price(text: str, expected: float | None) -> None:
    assert utils.parse_price(text) == expected


# ── build_thesis_data ─────────────────────────────────────────────────────────


def test_build_thesis_data_numeric_stop_target() -> None:
    td = utils.build_thesis_data(
        ticker="aapl",
        thesis_type="growth_momentum",
        thesis_text="Momentum thesis",
        confidence=4,
        stop_text="150",
        target_text="$200",
        avg_cost=175.0,
        strategy="long_call",
    )
    assert td["ticker"] == "AAPL"
    assert td["confidence_score"] == 0.8
    assert td["exit"]["stop_loss"] == 150.0
    assert td["exit"]["take_profit"] == 200.0
    assert td["kill_criteria"] == []
    assert td["setup_type"] == "long_call"


def test_build_thesis_data_text_stop_becomes_kill_criteria() -> None:
    td = utils.build_thesis_data(
        ticker="MU",
        thesis_type="earnings_drift",
        thesis_text="Earnings drift",
        confidence=3,
        stop_text="Close below 50 DMA",
        target_text="",
        avg_cost=0.0,
    )
    assert td["exit"]["stop_loss"] is None
    assert td["kill_criteria"] == ["Close below 50 DMA"]


# ── validate_thesis_submit ────────────────────────────────────────────────────


def test_validate_thesis_submit_happy_path() -> None:
    td = utils.build_thesis_data(
        ticker="MRAM",
        thesis_type="pivot_breakout",
        thesis_text="Breakout setup",
        confidence=3,
        stop_text="40",
        target_text="55",
        avg_cost=45.0,
    )
    assert utils.validate_thesis_submit(td) == []


def test_validate_thesis_submit_missing_statement() -> None:
    td = utils.build_thesis_data(
        ticker="MRAM",
        thesis_type="pivot_breakout",
        thesis_text="   ",
        confidence=3,
        stop_text="",
        target_text="",
        avg_cost=0.0,
    )
    errors = utils.validate_thesis_submit(td)
    assert any("thesis_statement" in e for e in errors)


def test_validate_thesis_submit_invalid_type() -> None:
    td = utils.build_thesis_data(
        ticker="MRAM",
        thesis_type="flow_play",
        thesis_text="Invalid type",
        confidence=3,
        stop_text="",
        target_text="",
        avg_cost=0.0,
    )
    errors = utils.validate_thesis_submit(td)
    assert any("thesis_type" in e for e in errors)


def test_validate_thesis_submit_invalid_confidence() -> None:
    td = utils.build_thesis_data(
        ticker="MRAM",
        thesis_type="pivot_breakout",
        thesis_text="Valid",
        confidence=0,
        stop_text="",
        target_text="",
        avg_cost=0.0,
    )
    errors = utils.validate_thesis_submit(td, confidence=0)
    assert any("confidence" in e for e in errors)


def test_validate_thesis_submit_ira_ineligible() -> None:
    errors = utils.validate_thesis_submit(
        {},
        account="ira_robinhood",
        strategy="iron_condor",
    )
    assert any("IRA" in e for e in errors)


# ── pending helpers ───────────────────────────────────────────────────────────


def test_pending_duplicate_tickers() -> None:
    open_theses = [
        {"ticker": "AAPL", "status": "ACTIVE"},
        {"ticker": "MU", "status": "ENTRY_READY"},
    ]
    pending = [
        {"ticker": "AAPL", "status": "PENDING_THESIS"},
        {"ticker": "TE", "status": "PENDING_THESIS"},
    ]
    assert utils.pending_duplicate_tickers(open_theses, pending) == {"AAPL"}


def test_position_from_pending_stock() -> None:
    pos = utils.position_from_pending(
        {
            "ticker": "TE",
            "asset_type": "stock",
            "account": "robinhood_taxable",
            "size": 10,
            "avg_cost": 5.5,
            "synced_at": "2026-05-28T10:00:00",
        }
    )
    assert pos["account_type"] == "robinhood_taxable"
    assert pos["shares"] == 10
    assert pos["raw_source"]["asset_type"] == "stock"


def test_position_from_pending_options() -> None:
    pos = utils.position_from_pending(
        {
            "ticker": "HOOD",
            "asset_type": "options",
            "account": "ira_robinhood",
            "strategy": "long_call",
            "contracts": 2,
            "strike": 25,
            "expiry": "2026-06-20",
            "option_type": "call",
        }
    )
    assert pos["shares"] == 2
    assert pos["raw_source"]["expiry"] == "2026-06-20"
    assert pos["raw_source"]["strike"] == 25


def test_mark_pending_ingested() -> None:
    positions = [
        {"key": "a", "status": "PENDING_THESIS"},
        {"key": "b", "status": "PENDING_THESIS"},
    ]
    updated = utils.mark_pending_ingested(positions, "a", "th_aapl_20260528_abcd")
    assert updated[0]["status"] == "INGESTED"
    assert updated[0]["thesis_id"] == "th_aapl_20260528_abcd"
    assert updated[1]["status"] == "PENDING_THESIS"


def test_load_pending_ingest_missing_returns_empty(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(utils, "get_repo_root", lambda: tmp_path)
    assert utils.load_pending_ingest() == []


def test_load_pending_ingest_corrupt_returns_empty(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = tmp_path / "state"
    state.mkdir()
    (state / "pending_ingest.json").write_text("{not json")
    monkeypatch.setattr(utils, "get_repo_root", lambda: tmp_path)
    assert utils.load_pending_ingest() == []
