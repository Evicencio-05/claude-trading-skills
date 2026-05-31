"""Tests for market_context_extract — pre-market summary builder."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from market_context_extract import (
    build_market_context_summary,
    build_synthesis,
    extract_breadth_summary,
    extract_sector_summary,
    extract_uptrend_summary,
    format_market_context_markdown,
    parse_path_from_stdout,
)
from report_paths import find_latest_same_day_artifact

UPTREND_FIXTURE = {
    "composite": {
        "composite_score": 57.7,
        "zone": "Neutral",
        "exposure_guidance": "Reduced Exposure (60-80%)",
        "guidance": "Mixed signals. Participate selectively with tighter risk controls.",
        "actions": ["Reduce position sizes by 20-30%", "Tighten stop-losses"],
        "active_warnings": [
            {
                "flag": "divergence",
                "label": "SECTOR DIVERGENCE WARNING",
                "description": "Significant divergence detected.",
            }
        ],
        "strongest_component": {"label": "Sector Participation", "score": 77},
        "weakest_component": {"label": "Market Breadth (Overall)", "score": 41},
    }
}

BREADTH_FIXTURE = {
    "composite": {
        "composite_score": 42.4,
        "zone": "Neutral",
        "exposure_guidance": "60-75%",
        "guidance": "Mixed signals. Be selective with new positions.",
        "strongest_health": {"label": "Current Breadth Level & Trend", "score": 57},
        "weakest_health": {"label": "Bearish Signal Status", "score": 25},
    }
}

SECTOR_MD = """# Sector Rotation Analysis — 2026-05-29

## Risk Regime

**RISK-ON** (score: 70/100)

## Cycle Phase Estimate

**Mid** (confidence: low)

## Sector Ranking (by uptrend ratio)

| Rank | Sector | Ratio | Trend | Status |
|------|--------|-------|-------|--------|
| 1 | Technology | 39.7% | Up | Overbought |
| 2 | Industrials | 29.5% | Down | Normal |
| 3 | Basic Materials | 27.6% | Down | Normal |

## Overbought / Oversold

**Overbought** (ratio > 37%):
- Technology: 39.7%
"""


def test_extract_uptrend_summary_from_json():
    summary = extract_uptrend_summary(UPTREND_FIXTURE)
    assert summary["score"] == 57.7
    assert summary["zone"] == "Neutral"
    assert len(summary["active_warnings"]) == 1
    assert summary["strongest"]["label"] == "Sector Participation"


def test_extract_breadth_summary_from_json():
    summary = extract_breadth_summary(BREADTH_FIXTURE)
    assert summary["score"] == 42.4
    assert summary["weakest"]["score"] == 25


def test_extract_sector_summary_from_markdown():
    summary = extract_sector_summary(SECTOR_MD)
    assert summary["leading_sector"] == "Technology"
    assert summary["cycle_phase"] == "Mid"
    assert summary["risk_regime"] == "RISK-ON"
    assert len(summary["top_sectors"]) == 3
    assert summary["overbought"] == ["Technology: 39.7%"]


def test_build_synthesis_reduce_only_low_breadth():
    synth = build_synthesis(
        breadth_score=35,
        as_of=date(2026, 5, 31),
        macro_events="none",
        urgent_flags=[],
        breadth_summary={"guidance": "Weak breadth.", "actions": []},
        uptrend_summary={"guidance": "Caution.", "actions": ["Tighten stops"]},
        sector_summary={"leading_sector": "Utilities"},
    )
    assert synth["posture"] == "REDUCE_ONLY"
    assert synth["ceiling"] == "30%"
    assert "35" in synth["headline"] or "Weak" in synth["headline"]


def test_build_synthesis_cautious_macro_today():
    synth = build_synthesis(
        breadth_score=55,
        as_of=date(2026, 5, 31),
        macro_events="2026-05-31 CPI HIGH impact",
        urgent_flags=[],
        breadth_summary={"guidance": "Mixed.", "actions": []},
        uptrend_summary={"guidance": "Mixed.", "actions": []},
        sector_summary={"leading_sector": "Technology"},
    )
    assert synth["posture"] == "CAUTIOUS"
    assert synth["ceiling"] == "50%"
    assert any("macro" in f.lower() or "CPI" in f for f in synth["risk_flags"])


def test_build_synthesis_urgent_flags():
    synth = build_synthesis(
        breadth_score=70,
        as_of=date(2026, 5, 31),
        macro_events="none",
        urgent_flags=["[URGENT] NVDA | expires in 3d"],
        breadth_summary={"guidance": "Healthy.", "actions": []},
        uptrend_summary={"guidance": "Healthy.", "actions": []},
        sector_summary={"leading_sector": "Technology"},
    )
    assert synth["posture"] == "REDUCE_ONLY"


def test_build_market_context_summary(tmp_path: Path):
    repo = tmp_path
    breadth_dir = repo / "reports" / "market" / "breadth"
    uptrend_dir = repo / "reports" / "market" / "uptrend"
    sector_dir = repo / "reports" / "market" / "sector"
    breadth_dir.mkdir(parents=True)
    uptrend_dir.mkdir(parents=True)
    sector_dir.mkdir(parents=True)

    as_of = date(2026, 5, 31)
    breadth_path = breadth_dir / "market_breadth_2026-05-31_120000.json"
    uptrend_path = uptrend_dir / "uptrend_analysis_2026-05-31_120000.json"
    sector_path = sector_dir / "sector_rotation_2026-05-31.md"
    breadth_path.write_text(json.dumps(BREADTH_FIXTURE))
    uptrend_path.write_text(json.dumps(UPTREND_FIXTURE))
    sector_path.write_text(SECTOR_MD)

    summary = build_market_context_summary(
        repo,
        as_of=as_of,
        macro_events="none",
        urgent_flags=[],
        watch_flags=[],
    )
    assert summary["schema_version"] == 1
    assert summary["as_of"] == "2026-05-31"
    assert summary["breadth"]["score"] == 42.4
    assert summary["uptrend"]["score"] == 57.7
    assert summary["sector"]["leading_sector"] == "Technology"
    assert summary["synthesis"]["posture"] == "CAUTIOUS"


def test_format_market_context_markdown():
    summary = {
        "as_of": "2026-05-31",
        "generated_at": "2026-05-31T08:00:00",
        "sources": {
            "breadth": "reports/market/breadth/x.json",
            "uptrend": "reports/market/uptrend/y.json",
            "sector": "reports/market/sector/z.md",
        },
        "breadth": {"score": 42.4, "zone": "Neutral", "guidance": "Mixed."},
        "uptrend": {"score": 57.7, "zone": "Neutral", "guidance": "Mixed."},
        "sector": {"leading_sector": "Technology", "cycle_phase": "Mid"},
        "synthesis": {
            "posture": "CAUTIOUS",
            "ceiling": "50%",
            "headline": "Mixed market — proceed with caution.",
            "risk_flags": [],
            "actions": ["Tighten stop-losses"],
        },
        "position_flags": {"urgent": [], "watch": []},
        "macro_events": "none",
    }
    md = format_market_context_markdown(summary)
    assert "## Executive Summary" in md
    assert "CAUTIOUS" in md
    assert "Artifact Links" in md
    assert "Breadth Detail" not in md


def test_parse_path_from_stdout():
    out = "  JSON report saved to: reports/market/breadth/market_breadth_2026-05-31_120000.json\n"
    assert parse_path_from_stdout(out, "json") == Path(
        "reports/market/breadth/market_breadth_2026-05-31_120000.json"
    )


def test_find_latest_same_day_artifact_prefers_json(tmp_path: Path):
    as_of = date(2026, 5, 31)
    breadth_dir = tmp_path / "reports" / "market" / "breadth"
    breadth_dir.mkdir(parents=True)
    md = breadth_dir / "market_breadth_2026-05-31_120000.md"
    js = breadth_dir / "market_breadth_2026-05-31_120000.json"
    md.write_text("# md")
    js.write_text("{}")
    result = find_latest_same_day_artifact(tmp_path, "market_breadth", as_of)
    assert result == js


def test_find_latest_same_day_artifact_sector_date_only(tmp_path: Path):
    as_of = date(2026, 5, 29)
    sector_dir = tmp_path / "reports" / "market" / "sector"
    sector_dir.mkdir(parents=True)
    path = sector_dir / "sector_rotation_2026-05-29.md"
    path.write_text(SECTOR_MD)
    result = find_latest_same_day_artifact(tmp_path, "sector_rotation", as_of)
    assert result == path
