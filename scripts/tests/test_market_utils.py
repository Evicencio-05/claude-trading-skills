"""Tests for thesis-manager market_utils artifact display helpers."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TM_DIR = ROOT / "tools" / "thesis-manager"
sys.path.insert(0, str(TM_DIR))
sys.path.insert(0, str(ROOT / "scripts"))

import market_utils  # noqa: E402

UPTREND_JSON = {
    "composite": {
        "composite_score": 57.7,
        "zone": "Neutral",
        "exposure_guidance": "Reduced Exposure (60-80%)",
        "guidance": "Mixed signals.",
        "active_warnings": [{"label": "SECTOR DIVERGENCE WARNING"}],
        "strongest_component": {"label": "Sector Participation", "score": 77},
        "weakest_component": {"label": "Market Breadth (Overall)", "score": 41},
        "component_scores": {
            "market_breadth": {"label": "Market Breadth", "score": 41},
        },
    }
}


@pytest.fixture
def tmp_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(market_utils.utils, "get_repo_root", lambda: tmp_path)
    return tmp_path


def test_resolve_display_artifact_sibling_md(tmp_repo: Path):
    breadth_dir = tmp_repo / "reports" / "market" / "breadth"
    breadth_dir.mkdir(parents=True)
    js = breadth_dir / "market_breadth_2026-05-31_120000.json"
    md = breadth_dir / "market_breadth_2026-05-31_120000.md"
    js.write_text("{}")
    md.write_text("# Full breadth report")
    resolved = market_utils.resolve_display_artifact(
        "reports/market/breadth/market_breadth_2026-05-31_120000.json"
    )
    assert resolved == md


def test_resolve_display_artifact_same_day_newer_md(tmp_repo: Path):
    breadth_dir = tmp_repo / "reports" / "market" / "breadth"
    breadth_dir.mkdir(parents=True)
    js = breadth_dir / "market_breadth_2026-05-31_130000.json"
    older_md = breadth_dir / "market_breadth_2026-05-31_120000.md"
    newer_md = breadth_dir / "market_breadth_2026-05-31_130000.md"
    js.write_text("{}")
    older_md.write_text("# older")
    newer_md.write_text("# newer")
    resolved = market_utils.resolve_display_artifact(
        "reports/market/breadth/market_breadth_2026-05-31_130000.json"
    )
    assert resolved == newer_md


def test_resolve_display_artifact_json_only_returns_json(tmp_repo: Path):
    breadth_dir = tmp_repo / "reports" / "market" / "breadth"
    breadth_dir.mkdir(parents=True)
    js = breadth_dir / "market_breadth_2026-05-31_120000.json"
    js.write_text(json.dumps(UPTREND_JSON))
    resolved = market_utils.resolve_display_artifact(
        "reports/market/breadth/market_breadth_2026-05-31_120000.json"
    )
    assert resolved == js


def test_format_artifact_json_as_markdown_uptrend():
    md = market_utils.format_artifact_json_as_markdown(UPTREND_JSON, "uptrend")
    assert "57.7/100" in md
    assert "SECTOR DIVERGENCE WARNING" in md
    assert "Component Scores" in md


def test_load_artifact_display_md_sector(tmp_repo: Path):
    sector_dir = tmp_repo / "reports" / "market" / "sector"
    sector_dir.mkdir(parents=True)
    md = sector_dir / "sector_rotation_2026-05-31.md"
    md.write_text("# Sector report")
    content, label, is_summary = market_utils.load_artifact_display(
        "reports/market/sector/sector_rotation_2026-05-31.md", "sector"
    )
    assert content == "# Sector report"
    assert "sector_rotation" in label
    assert is_summary is False


def test_load_artifact_display_json_fallback(tmp_repo: Path):
    breadth_dir = tmp_repo / "reports" / "market" / "breadth"
    breadth_dir.mkdir(parents=True)
    js = breadth_dir / "market_breadth_2026-05-31_120000.json"
    js.write_text(json.dumps(UPTREND_JSON))
    content, label, is_summary = market_utils.load_artifact_display(
        "reports/market/breadth/market_breadth_2026-05-31_120000.json", "breadth"
    )
    assert content is not None
    assert "57.7/100" in content
    assert is_summary is True
    assert label.endswith(".json")
