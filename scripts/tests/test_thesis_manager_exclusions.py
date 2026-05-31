"""Tests for ticker exclusion, archive, and removal helpers."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TM_DIR = ROOT / "tools" / "thesis-manager"
STORE_DIR = ROOT / "skills" / "trader-memory-core" / "scripts"
sys.path.insert(0, str(TM_DIR))
sys.path.insert(0, str(STORE_DIR))

import research_utils  # noqa: E402
import thesis_store  # noqa: E402
import utils  # noqa: E402


def _make_thesis_data(ticker: str = "TE") -> dict:
    return utils.build_thesis_data(
        ticker=ticker,
        thesis_type="growth_momentum",
        thesis_text="Test thesis for exclusion flows.",
        confidence=3,
        stop_text="10",
        target_text="20",
        avg_cost=12.0,
    )


@pytest.fixture
def repo_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='t'\n")
    state_dir = tmp_path / "state" / "theses"
    state_dir.mkdir(parents=True)
    research_dir = tmp_path / "reports" / "research"
    research_dir.mkdir(parents=True)
    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True)
    monkeypatch.setattr(utils, "get_repo_root", lambda: tmp_path)
    monkeypatch.setattr(research_utils, "get_repo_root", lambda: tmp_path)
    monkeypatch.setattr(utils, "get_state_dir", lambda: state_dir)
    return tmp_path


def test_save_and_load_exclude(repo_env: Path) -> None:
    research_utils.save_exclude({"INO": {"reason": "not interested"}})
    path = repo_env / "config" / "research_exclude.yaml"
    assert path.exists()
    loaded = research_utils.load_exclude_for_editor()
    assert loaded["INO"]["reason"] == "not interested"


def test_add_exclude_ticker_merges(repo_env: Path) -> None:
    research_utils.save_exclude({"MRAM": {"reason": "keep"}})
    research_utils.add_exclude_ticker("INO", "drop")
    loaded = research_utils.load_exclude_config(repo_env / "config" / "research_exclude.yaml")
    assert "MRAM" in loaded
    assert loaded["INO"]["reason"] == "drop"


def test_list_report_tickers_skips_excluded(
    repo_env: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    research_utils.save_exclude({"INO": {"reason": "x"}})
    (repo_env / "reports" / "research" / "INO_2026-05-10.md").write_text("# INO\n")
    (repo_env / "reports" / "research" / "MRAM_2026-05-10.md").write_text("# MRAM\n")
    exclude_path = repo_env / "config" / "research_exclude.yaml"
    monkeypatch.setattr(
        research_utils,
        "resolve_exclude_path_for_filter",
        lambda: exclude_path,
    )
    tickers = research_utils.list_report_tickers()
    assert tickers == ["MRAM"]


def test_archive_report(repo_env: Path) -> None:
    src = repo_env / "reports" / "research" / "INO_2026-05-10.md"
    src.write_text("# INO\n")
    dest = research_utils.archive_report(src)
    assert dest.parent == repo_env / "reports" / "archives"
    assert dest.exists()
    assert not src.exists()


def test_mark_pending_skipped() -> None:
    positions = [
        {"key": "XSP|options|1|2026-06-01|call", "ticker": "XSP", "status": "PENDING_THESIS"},
        {"key": "AAPL|stock", "ticker": "AAPL", "status": "PENDING_THESIS"},
    ]
    updated = utils.mark_pending_skipped(positions, "XSP|options|1|2026-06-01|call")
    assert updated[0]["status"] == "SKIPPED"
    assert updated[1]["status"] == "PENDING_THESIS"


def test_block_sync_key(repo_env: Path) -> None:
    utils.block_sync_key("XSP|options|1|2026-06-01|call")
    data = json.loads((repo_env / "state" / "synced_positions.json").read_text())
    assert "XSP|options|1|2026-06-01|call" in data["ingested_keys"]


def test_stop_tracking_invalidates_active(repo_env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    state_dir = repo_env / "state" / "theses"
    monkeypatch.setattr(utils, "get_state_dir", lambda: state_dir)
    tid = thesis_store.register(state_dir, _make_thesis_data("XSP"))
    thesis_store.transition(state_dir, tid, "ENTRY_READY", "ok")
    thesis_store.open_position(state_dir, tid, 5.0, "2026-03-01T10:00:00+00:00")
    result = utils.stop_tracking_thesis(tid, "hedge — not tracked")
    assert result["status"] == "INVALIDATED"
    assert result.get("outcome", {}).get("pnl_pct") is None


def test_delete_thesis_wrapper(repo_env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    state_dir = repo_env / "state" / "theses"
    monkeypatch.setattr(utils, "get_state_dir", lambda: state_dir)
    tid = thesis_store.register(state_dir, _make_thesis_data("OLD"))
    thesis_store.terminate(state_dir, tid, "INVALIDATED", "mistake")
    deleted = utils.delete_thesis(tid)
    assert deleted == tid
    assert not (state_dir / f"{tid}.yaml").exists()


def test_is_ticker_excluded(repo_env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    research_utils.save_exclude({"INO": {"reason": "x"}})
    exclude_path = repo_env / "config" / "research_exclude.yaml"
    import research_watchlist as rw

    monkeypatch.setattr(rw, "resolve_exclude_path_for_filter", lambda repo_root=None: exclude_path)
    monkeypatch.setattr(utils, "get_repo_root", lambda: repo_env)
    assert utils.is_ticker_excluded("INO") is True
    assert utils.is_ticker_excluded("MRAM") is False
