"""Tests for report_paths — canonical reports/ layout registry."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from report_paths import (
    ARTIFACT_KEYS,
    artifact_dir,
    default_output_dir,
    find_latest_same_day,
    find_latest_same_day_artifact,
    find_screener_for_ticker,
    logs_dir,
    reports_root,
)


def _write_json(path: Path, payload: dict) -> None:
    import json

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload))


@pytest.fixture
def tmp_repo(tmp_path: Path):
    return tmp_path


def test_artifact_dir_creates_subdirectory(tmp_repo):
    path = artifact_dir(tmp_repo, "market_breadth", mkdir=True)
    assert path == tmp_repo / "reports" / "market" / "breadth"
    assert path.is_dir()


@pytest.mark.parametrize(
    ("key", "rel"),
    [
        ("tradewhisperer_charts", ("reports", "charts", "tradewhisperer")),
        ("gex_vex_maps", ("reports", "charts", "gex_vex")),
        ("operator_charts", ("reports", "charts", "operator")),
        ("ta_confluence", ("reports", "charts", "confluence")),
    ],
)
def test_ta_chart_source_artifact_dirs(tmp_repo, key, rel):
    path = artifact_dir(tmp_repo, key, mkdir=True)
    assert path == tmp_repo.joinpath(*rel)
    assert path.is_dir()
    assert key in ARTIFACT_KEYS


def test_default_output_dir_matches_artifact_dir(tmp_repo):
    assert default_output_dir(tmp_repo, "vcp_screener") == artifact_dir(tmp_repo, "vcp_screener")


def test_find_latest_same_day_in_canonical_dir(tmp_repo):
    as_of = date(2026, 5, 31)
    breadth_dir = artifact_dir(tmp_repo, "market_breadth", mkdir=True)
    _write_json(breadth_dir / "market_breadth_2026-05-31_080928.json", {"score": 1})
    _write_json(breadth_dir / "market_breadth_2026-05-31_081301.json", {"score": 2})
    result = find_latest_same_day(tmp_repo, "market_breadth", as_of)
    assert result is not None
    assert result.name == "market_breadth_2026-05-31_081301.json"


def test_find_latest_same_day_legacy_pre_market_fallback(tmp_repo):
    as_of = date(2026, 5, 31)
    legacy = tmp_repo / "reports" / "pre_market"
    legacy.mkdir(parents=True)
    _write_json(legacy / "uptrend_analysis_2026-05-31_120000.json", {"score": 1})
    result = find_latest_same_day(tmp_repo, "uptrend_analysis", as_of)
    assert result is not None
    assert "pre_market" in str(result)


def test_find_latest_same_day_legacy_root_fallback(tmp_repo):
    as_of = date(2026, 5, 31)
    root = reports_root(tmp_repo)
    root.mkdir(parents=True)
    _write_json(root / "vcp_screener_2026-05-31_081301.json", {"results": []})
    result = find_latest_same_day(tmp_repo, "vcp_screener", as_of)
    assert result is not None
    assert result.parent == root


def test_find_latest_same_day_prefers_canonical_over_legacy(tmp_repo):
    as_of = date(2026, 5, 31)
    canonical = artifact_dir(tmp_repo, "market_top", mkdir=True)
    legacy = tmp_repo / "reports" / "pre_market"
    legacy.mkdir(parents=True)
    _write_json(canonical / "market_top_2026-05-31_090000.json", {"score": 1})
    _write_json(legacy / "market_top_2026-05-31_120000.json", {"score": 2})
    result = find_latest_same_day(tmp_repo, "market_top", as_of)
    assert result is not None
    assert "market/top" in str(result)


def test_find_screener_for_ticker_in_screener_dir(tmp_repo):
    as_of = date(2026, 5, 31)
    vcp_dir = artifact_dir(tmp_repo, "vcp_screener", mkdir=True)
    _write_json(
        vcp_dir / "vcp_screener_2026-05-31_081301.json",
        {"results": [], "metadata": {"funnel": {"universe": 2}}},
    )
    found = find_screener_for_ticker(tmp_repo, "vcp_screener", "VECO", as_of, ["MRAM", "VECO"])
    assert found is not None
    assert "screeners/vcp" in str(found)


def test_logs_dir(tmp_repo):
    assert logs_dir(tmp_repo) == tmp_repo / "reports" / "logs"


def test_all_batch_keys_have_dirs():
    for key in (
        "market_breadth",
        "uptrend_analysis",
        "market_top",
        "exposure_posture",
        "vcp_screener",
        "canslim_screener",
    ):
        assert key in ARTIFACT_KEYS


def test_find_latest_same_day_artifact_prefers_json_over_md(tmp_repo):
    as_of = date(2026, 5, 31)
    breadth_dir = artifact_dir(tmp_repo, "market_breadth", mkdir=True)
    md = breadth_dir / "market_breadth_2026-05-31_120000.md"
    js = breadth_dir / "market_breadth_2026-05-31_120000.json"
    md.write_text("# md")
    _write_json(js, {"score": 1})
    result = find_latest_same_day_artifact(tmp_repo, "market_breadth", as_of)
    assert result == js


def test_find_latest_same_day_artifact_finds_sector_date_only(tmp_repo):
    as_of = date(2026, 5, 29)
    sector_dir = artifact_dir(tmp_repo, "sector_rotation", mkdir=True)
    path = sector_dir / "sector_rotation_2026-05-29.md"
    path.write_text("# sector")
    result = find_latest_same_day_artifact(tmp_repo, "sector_rotation", as_of)
    assert result == path
