"""Tests for thesis-manager research report listing/loading helpers."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TM_DIR = ROOT / "tools" / "thesis-manager"
sys.path.insert(0, str(TM_DIR))

import research_utils  # noqa: E402


@pytest.fixture
def research_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    reports = tmp_path / "reports" / "research"
    reports.mkdir(parents=True)
    (reports / "AAPL_2026-01-01.md").write_text("# AAPL\nOld report\n")
    (reports / "MRAM_2026-05-10.md").write_text("# MRAM May 10\n")
    (reports / "MRAM_2026-05-27.md").write_text("# MRAM May 27\nLatest content\n")
    monkeypatch.setattr(research_utils, "_research_dir", lambda: reports)
    return reports


def test_list_report_tickers_sorted(research_dir: Path) -> None:
    assert research_utils.list_report_tickers() == ["AAPL", "MRAM"]


def test_list_report_tickers_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    empty = tmp_path / "reports" / "research"
    empty.mkdir(parents=True)
    monkeypatch.setattr(research_utils, "_research_dir", lambda: empty)
    assert research_utils.list_report_tickers() == []


def test_list_reports_for_ticker_newest_first(research_dir: Path) -> None:
    entries = research_utils.list_reports_for_ticker("MRAM")
    assert len(entries) == 2
    assert entries[0]["date"] == date(2026, 5, 27)
    assert entries[1]["date"] == date(2026, 5, 10)
    assert entries[0]["path"].name == "MRAM_2026-05-27.md"


def test_list_reports_for_ticker_unknown(research_dir: Path) -> None:
    assert research_utils.list_reports_for_ticker("ZZZZ") == []


def test_load_report_markdown(research_dir: Path) -> None:
    path = research_dir / "MRAM_2026-05-27.md"
    text = research_utils.load_report_markdown(path)
    assert text == "# MRAM May 27\nLatest content\n"


def test_load_report_markdown_missing() -> None:
    assert research_utils.load_report_markdown(Path("/nonexistent/report.md")) is None
