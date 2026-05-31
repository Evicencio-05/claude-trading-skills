"""Tests for research_watchlist staleness helpers."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
import yaml
from research_watchlist import (
    apply_exclude,
    build_staleness_rows,
    days_stale,
    eligible_tickers,
    latest_report_date,
    load_exclude_config,
    load_watchlist_config,
    tickers_from_theses,
)


def _write_thesis(path: Path, ticker: str, status: str) -> None:
    path.write_text(
        yaml.dump({"ticker": ticker, "status": status, "thesis_id": f"th_{ticker.lower()}"})
    )


def _write_report(research_dir: Path, ticker: str, report_date: str) -> None:
    research_dir.mkdir(parents=True, exist_ok=True)
    (research_dir / f"{ticker}_{report_date}.md").write_text(f"# {ticker}\n")


@pytest.fixture
def tmp_env(tmp_path: Path):
    state_dir = tmp_path / "state" / "theses"
    state_dir.mkdir(parents=True)
    research_dir = tmp_path / "reports" / "research"
    watchlist_path = tmp_path / "config" / "research_watchlist.yaml"
    watchlist_path.parent.mkdir(parents=True)
    return {
        "root": tmp_path,
        "state_dir": state_dir,
        "research_dir": research_dir,
        "watchlist_path": watchlist_path,
        "exclude_path": tmp_path / "config" / "no_exclude.yaml",
    }


def test_load_watchlist_config(tmp_env):
    tmp_env["watchlist_path"].write_text(
        "MRAM:\n  watching: true\n  notes: swing\nFPS:\n  watching: false\n"
    )
    cfg = load_watchlist_config(tmp_env["watchlist_path"])
    assert cfg["MRAM"] == {"watching": True, "notes": "swing"}
    assert cfg["FPS"]["watching"] is False


def test_load_watchlist_config_missing_returns_empty(tmp_env):
    assert load_watchlist_config(tmp_env["watchlist_path"]) == {}


def test_tickers_from_theses(tmp_env):
    _write_thesis(tmp_env["state_dir"] / "a.yaml", "MRAM", "ACTIVE")
    _write_thesis(tmp_env["state_dir"] / "b.yaml", "MU", "ENTRY_READY")
    _write_thesis(tmp_env["state_dir"] / "c.yaml", "OLD", "CLOSED")
    found = tickers_from_theses(tmp_env["state_dir"], ("ACTIVE", "ENTRY_READY"))
    assert found == {"MRAM", "MU"}


def test_eligible_tickers_union_and_idea_rule(tmp_env):
    _write_thesis(tmp_env["state_dir"] / "a.yaml", "MRAM", "ACTIVE")
    _write_thesis(tmp_env["state_dir"] / "b.yaml", "SCNR", "IDEA")
    tmp_env["watchlist_path"].write_text(
        "FPS:\n  watching: true\nSCNR:\n  watching: true\nNOPE:\n  watching: true\n"
    )
    tickers = eligible_tickers(
        tmp_env["state_dir"],
        tmp_env["watchlist_path"],
        exclude_path=tmp_env["exclude_path"],
    )
    assert tickers == ["FPS", "MRAM", "NOPE", "SCNR"]


def test_eligible_ignores_idea_not_on_watchlist(tmp_env):
    _write_thesis(tmp_env["state_dir"] / "a.yaml", "SCNR", "IDEA")
    tmp_env["watchlist_path"].write_text("FPS:\n  watching: true\n")
    assert eligible_tickers(
        tmp_env["state_dir"],
        tmp_env["watchlist_path"],
        exclude_path=tmp_env["exclude_path"],
    ) == ["FPS"]


def test_latest_report_date_picks_newest(tmp_env):
    _write_report(tmp_env["research_dir"], "MRAM", "2026-05-10")
    _write_report(tmp_env["research_dir"], "MRAM", "2026-05-27")
    assert latest_report_date(tmp_env["research_dir"], "MRAM") == date(2026, 5, 27)


def test_latest_report_date_none_when_missing(tmp_env):
    assert latest_report_date(tmp_env["research_dir"], "XYZ") is None


def test_days_stale(tmp_env):
    assert days_stale(date(2026, 5, 13), date(2026, 5, 28)) == 15
    assert days_stale(None, date(2026, 5, 28)) is None


def test_build_staleness_rows(tmp_env):
    _write_report(tmp_env["research_dir"], "FPS", "2026-05-13")
    rows = build_staleness_rows(
        tickers=["FPS"],
        research_dir=tmp_env["research_dir"],
        as_of=date(2026, 5, 28),
        threshold_days=14,
        eligibility_map={"FPS": ["watchlist"]},
    )
    assert len(rows) == 1
    row = rows[0]
    assert row["ticker"] == "FPS"
    assert row["last_report"] == "2026-05-13"
    assert row["days_stale"] == 15
    assert row["eligibility"] == ["watchlist"]
    assert row["needs_update"] is True
    assert row["status"] == "needs_update"


def test_build_staleness_rows_no_report(tmp_env):
    rows = build_staleness_rows(
        tickers=["NEW"],
        research_dir=tmp_env["research_dir"],
        as_of=date(2026, 5, 28),
        threshold_days=14,
        eligibility_map={"NEW": ["position"]},
    )
    assert rows[0]["last_report"] is None
    assert rows[0]["days_stale"] is None
    assert rows[0]["needs_update"] is True
    assert rows[0]["status"] == "needs_deep_research"


def test_build_staleness_rows_current(tmp_env):
    _write_report(tmp_env["research_dir"], "MRAM", "2026-05-27")
    rows = build_staleness_rows(
        tickers=["MRAM"],
        research_dir=tmp_env["research_dir"],
        as_of=date(2026, 5, 28),
        threshold_days=14,
        eligibility_map={"MRAM": ["position"]},
    )
    assert rows[0]["needs_update"] is False
    assert rows[0]["status"] == "current"


def test_load_exclude_config(tmp_env):
    exclude_path = tmp_env["root"] / "config" / "research_exclude.yaml"
    exclude_path.parent.mkdir(parents=True, exist_ok=True)
    exclude_path.write_text("INO:\n  reason: not interested\n")
    cfg = load_exclude_config(exclude_path)
    assert cfg["INO"] == {"reason": "not interested"}


def test_apply_exclude(tmp_env):
    exclude_path = tmp_env["root"] / "config" / "research_exclude.yaml"
    exclude_path.parent.mkdir(parents=True, exist_ok=True)
    exclude_path.write_text("INO:\n  reason: x\n")
    assert apply_exclude(["MRAM", "INO", "MU"], exclude_path) == ["MRAM", "MU"]


def test_eligible_tickers_respects_exclude(tmp_env, monkeypatch):
    _write_thesis(tmp_env["state_dir"] / "a.yaml", "MRAM", "ACTIVE")
    _write_thesis(tmp_env["state_dir"] / "b.yaml", "INO", "ACTIVE")
    tmp_env["watchlist_path"].write_text("FPS:\n  watching: true\n")
    exclude_path = tmp_env["root"] / "config" / "research_exclude.yaml"
    exclude_path.parent.mkdir(parents=True, exist_ok=True)
    exclude_path.write_text("INO:\n  reason: dropped\n")

    import research_watchlist as rw

    monkeypatch.setattr(rw, "resolve_exclude_path_for_filter", lambda repo_root=None: exclude_path)

    tickers = eligible_tickers(tmp_env["state_dir"], tmp_env["watchlist_path"])
    assert tickers == ["FPS", "MRAM"]
