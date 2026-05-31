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
    monkeypatch.setattr(research_utils, "excluded_ticker_set", lambda: set())
    return reports


def test_list_report_tickers_sorted(research_dir: Path) -> None:
    assert research_utils.list_report_tickers() == ["AAPL", "MRAM"]


def test_list_report_tickers_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    empty = tmp_path / "reports" / "research"
    empty.mkdir(parents=True)
    monkeypatch.setattr(research_utils, "_research_dir", lambda: empty)
    monkeypatch.setattr(research_utils, "excluded_ticker_set", lambda: set())
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


def test_escape_dollar_signs_fps_regression() -> None:
    line = (
        "- Large intangible base ($829M) generating heavy non-cash amortization — "
        "the gap between GAAP EPS ($0.06 TTM) and adjusted results is very wide"
    )
    escaped = research_utils.escape_dollar_signs_for_streamlit(line)
    assert escaped == (
        "- Large intangible base (\\$829M) generating heavy non-cash amortization — "
        "the gap between GAAP EPS (\\$0.06 TTM) and adjusted results is very wide"
    )


def test_escape_dollar_signs_pair_on_one_line() -> None:
    assert (
        research_utils.escape_dollar_signs_for_streamlit("Interest expense of $61M on $709M debt")
        == "Interest expense of \\$61M on \\$709M debt"
    )


def test_escape_dollar_signs_preserves_pre_escaped() -> None:
    assert research_utils.escape_dollar_signs_for_streamlit("\\$100") == "\\$100"


def test_escape_dollar_signs_skips_fenced_code_blocks() -> None:
    md = "Price $50\n```\n$foo$\n```\nDebt $709M"
    assert research_utils.escape_dollar_signs_for_streamlit(md) == (
        "Price \\$50\n```\n$foo$\n```\nDebt \\$709M"
    )
