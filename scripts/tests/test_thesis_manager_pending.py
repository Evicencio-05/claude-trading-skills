"""Tests for pending-ingest → ACTIVE thesis promotion in utils.py."""

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


def _pending_stock() -> dict:
    return {
        "key": "TE|stock",
        "ticker": "TE",
        "asset_type": "stock",
        "direction": "long",
        "account": "robinhood_taxable",
        "size": 5,
        "avg_cost": 12.5,
        "synced_at": "2026-05-20T09:00:00",
        "status": "PENDING_THESIS",
    }


def _thesis_data() -> dict:
    return utils.build_thesis_data(
        ticker="TE",
        thesis_type="growth_momentum",
        thesis_text="Taxable swing position on TE.",
        confidence=3,
        stop_text="10",
        target_text="18",
        avg_cost=12.5,
    )


@pytest.fixture
def state_dir(tmp_path: Path) -> Path:
    d = tmp_path / "theses"
    d.mkdir()
    return d


def test_register_pending_promotes_to_active(
    state_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(utils, "get_state_dir", lambda: state_dir)
    monkeypatch.setattr(utils, "get_repo_root", lambda: state_dir.parent)

    thesis_id = utils.register_pending_position(_thesis_data(), _pending_stock())
    thesis = thesis_store.get(state_dir, thesis_id)

    assert thesis["status"] == "ACTIVE"
    assert thesis["entry"]["actual_price"] == 12.5
    assert thesis["position"]["account_type"] == "robinhood_taxable"
    assert thesis["position"]["shares"] == 5


def test_register_pending_ira_ineligible_raises(
    state_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(utils, "get_state_dir", lambda: state_dir)
    pending = _pending_stock()
    pending["account"] = "ira_robinhood"
    pending["asset_type"] = "options"
    pending["strategy"] = "iron_condor"

    with pytest.raises(ValueError, match="IRA"):
        utils.register_pending_position(_thesis_data(), pending)


@pytest.mark.parametrize("reason", utils.EXIT_REASONS)
def test_finalize_thesis_all_exit_reasons(
    state_dir: Path, monkeypatch: pytest.MonkeyPatch, reason: str
) -> None:
    monkeypatch.setattr(utils, "get_state_dir", lambda: state_dir)

    td = utils.build_thesis_data(
        ticker="TE",
        thesis_type="growth_momentum",
        thesis_text="Close test thesis.",
        confidence=3,
        stop_text="",
        target_text="",
        avg_cost=10.0,
    )
    thesis_id = utils.register_pending_position(td, _pending_stock())
    result = utils.finalize_thesis(thesis_id, reason, 11.0, date(2026, 5, 28))

    assert result["status"] in ("CLOSED", "INVALIDATED")
    exit_block = result.get("exit") or {}
    if result["status"] == "CLOSED":
        assert exit_block.get("exit_reason") == reason
    else:
        assert exit_block.get("exit_reason") is not None


def test_finalize_thesis_entry_ready_terminates(
    state_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(utils, "get_state_dir", lambda: state_dir)

    td = utils.build_thesis_data(
        ticker="IDEA",
        thesis_type="mean_reversion",
        thesis_text="Idea only — not opened.",
        confidence=2,
        stop_text="",
        target_text="",
        avg_cost=0.0,
    )
    thesis_id = utils.register_thesis(td)
    utils.transition_thesis(thesis_id, "ENTRY_READY", "planned entry")

    result = utils.finalize_thesis(thesis_id, "time_stop", 0.0, date(2026, 5, 28))
    assert result["status"] == "INVALIDATED"
