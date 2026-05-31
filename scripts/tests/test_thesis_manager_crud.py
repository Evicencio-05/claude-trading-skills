"""Tests for thesis-manager CRUD helpers and store wrappers."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TM_DIR = ROOT / "tools" / "thesis-manager"
STORE_DIR = ROOT / "skills" / "trader-memory-core" / "scripts"
sys.path.insert(0, str(TM_DIR))
sys.path.insert(0, str(STORE_DIR))

import thesis_store  # noqa: E402
import utils  # noqa: E402


def test_confidence_level_from_score() -> None:
    assert utils.confidence_level_from_score(0.8) == 4
    assert utils.confidence_level_from_score(None) == 3
    assert utils.confidence_level_from_score(0.2) == 1


def test_stop_display_numeric_and_text() -> None:
    assert utils.stop_display({"exit": {"stop_loss": 150.0}}) == "150.0"
    assert utils.stop_display({"kill_criteria": ["Close below 50 DMA"]}) == "Close below 50 DMA"
    assert utils.stop_display({}) == ""


def test_target_display() -> None:
    assert utils.target_display({"exit": {"take_profit": 200.0}}) == "200.0"
    assert utils.target_display({}) == ""


def test_build_update_fields_numeric_stop() -> None:
    fields = utils.build_update_fields(
        thesis_text="Updated thesis",
        confidence=4,
        stop_text="150",
        target_text="200",
        catalyst="Earnings beat",
        setup_type="manual",
        review_interval_days=14,
    )
    assert fields["thesis_statement"] == "Updated thesis"
    assert fields["confidence_score"] == 0.8
    assert fields["exit"]["stop_loss"] == 150.0
    assert fields["exit"]["take_profit"] == 200.0
    assert fields["kill_criteria"] == []
    assert fields["catalyst"] == "Earnings beat"
    assert fields["monitoring"]["review_interval_days"] == 14


def test_build_update_fields_text_stop_becomes_kill() -> None:
    fields = utils.build_update_fields(
        thesis_text="Thesis",
        confidence=3,
        stop_text="Break below pivot",
        target_text="",
    )
    assert fields["exit"]["stop_loss"] is None
    assert fields["kill_criteria"] == ["Break below pivot"]


def test_build_update_fields_outcome() -> None:
    fields = utils.build_update_fields(
        thesis_text="Thesis",
        confidence=3,
        stop_text="",
        target_text="",
        lessons_learned="Wait for confirmation",
        what_happened="Stopped out early",
    )
    assert fields["outcome"]["lessons_learned"] == "Wait for confirmation"
    assert fields["outcome"]["what_happened"] == "Stopped out early"


def test_validate_thesis_update_errors() -> None:
    fields = utils.build_update_fields(
        thesis_text="   ",
        confidence=3,
        stop_text="",
        target_text="",
    )
    errors = utils.validate_thesis_update(fields, confidence=3)
    assert any("thesis_statement" in e for e in errors)


@pytest.fixture
def state_dir(tmp_path: Path) -> Path:
    d = tmp_path / "theses"
    d.mkdir()
    return d


def test_get_thesis_and_update_round_trip(state_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(utils, "get_state_dir", lambda: state_dir)

    td = utils.build_thesis_data(
        ticker="CRUD",
        thesis_type="growth_momentum",
        thesis_text="Initial thesis",
        confidence=3,
        stop_text="10",
        target_text="20",
        avg_cost=12.0,
    )
    thesis_id = utils.register_thesis(td)
    loaded = utils.get_thesis(thesis_id)
    assert loaded["thesis_statement"] == "Initial thesis"

    update_fields = utils.build_update_fields(
        thesis_text="Revised thesis",
        confidence=5,
        stop_text="9",
        target_text="25",
        review_interval_days=7,
    )
    assert utils.validate_thesis_update(update_fields, confidence=5) == []
    updated = utils.update_thesis(thesis_id, update_fields)
    assert updated["thesis_statement"] == "Revised thesis"
    assert updated["confidence_score"] == 1.0
    assert updated["exit"]["stop_loss"] == 9.0
    assert updated["monitoring"]["review_interval_days"] == 7


def test_delete_thesis_terminal_only(state_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(utils, "get_state_dir", lambda: state_dir)

    td = utils.build_thesis_data(
        ticker="DEL",
        thesis_type="mean_reversion",
        thesis_text="Delete me",
        confidence=2,
        stop_text="",
        target_text="",
        avg_cost=0.0,
    )
    thesis_id = utils.register_thesis(td)
    with pytest.raises(ValueError, match="terminal"):
        utils.delete_thesis(thesis_id)

    utils.stop_tracking_thesis(thesis_id, "test invalidate")
    deleted_id = utils.delete_thesis(thesis_id)
    assert deleted_id == thesis_id
    with pytest.raises(FileNotFoundError):
        thesis_store.get(state_dir, thesis_id)


def test_sort_theses_for_display_newest_first() -> None:
    theses = [
        {"ticker": "B", "created_at": "2026-05-01T00:00:00+00:00"},
        {"ticker": "A", "created_at": "2026-05-28T00:00:00+00:00"},
    ]
    sorted_rows = utils.sort_theses_for_display(theses)
    assert sorted_rows[0]["ticker"] == "A"


def test_finalize_via_crud_path(state_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(utils, "get_state_dir", lambda: state_dir)

    td = utils.build_thesis_data(
        ticker="CLS",
        thesis_type="pivot_breakout",
        thesis_text="Close test",
        confidence=3,
        stop_text="",
        target_text="",
        avg_cost=50.0,
    )
    thesis_id = utils.register_thesis(td)
    utils.transition_thesis(thesis_id, "ENTRY_READY", "planned")
    thesis_store.open_position(
        state_dir,
        thesis_id,
        actual_price=50.0,
        actual_date=utils.format_exit_datetime(date(2026, 5, 1)),
        reason="test open",
        shares=10,
    )
    result = utils.finalize_thesis(thesis_id, "manual", 55.0, date(2026, 5, 28))
    assert result["status"] == "CLOSED"
    assert utils.delete_thesis(thesis_id) == thesis_id
