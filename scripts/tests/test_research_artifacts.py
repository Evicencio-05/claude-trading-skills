"""Tests for research_artifacts preflight helpers."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest
from report_paths import (
    artifact_dir,
    find_latest_same_day,
    find_screener_for_ticker,
    screener_covers_ticker,
)
from research_artifacts import (
    build_preflight_manifest,
    load_watchlist_symbols,
    market_context_path,
)


def _write_screener(path: Path, symbols: list[str], universe: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "results": [{"symbol": s, "composite_score": 70} for s in symbols],
                "metadata": {"funnel": {"universe": universe}},
            }
        )
    )


@pytest.fixture
def tmp_repo(tmp_path: Path):
    logs = tmp_path / "reports" / "logs"
    logs.mkdir(parents=True)
    watchlist = tmp_path / "config" / "research_watchlist.yaml"
    watchlist.parent.mkdir(parents=True)
    watchlist.write_text("MRAM:\n  watching: true\nVECO:\n  watching: true\n")
    return {"root": tmp_path, "logs": logs, "watchlist": watchlist}


def test_find_latest_same_day_picks_latest_timestamp(tmp_repo):
    as_of = date(2026, 5, 31)
    vcp_dir = artifact_dir(tmp_repo["root"], "vcp_screener", mkdir=True)
    _write_screener(vcp_dir / "vcp_screener_2026-05-31_080928.json", ["A"], 1)
    _write_screener(vcp_dir / "vcp_screener_2026-05-31_081301.json", ["B"], 1)
    result = find_latest_same_day(tmp_repo["root"], "vcp_screener", as_of)
    assert result is not None
    assert result.name == "vcp_screener_2026-05-31_081301.json"


def test_find_latest_same_day_ignores_prior_day(tmp_repo):
    as_of = date(2026, 5, 31)
    vcp_dir = artifact_dir(tmp_repo["root"], "vcp_screener", mkdir=True)
    _write_screener(vcp_dir / "vcp_screener_2026-05-30_120000.json", ["A"], 1)
    assert find_latest_same_day(tmp_repo["root"], "vcp_screener", as_of) is None


def test_screener_covers_ticker_by_symbol(tmp_repo):
    path = tmp_repo["root"] / "vcp.json"
    _write_screener(path, ["VECO"], 1)
    assert screener_covers_ticker(path, "VECO", ["MRAM", "VECO"]) is True


def test_screener_covers_ticker_watchlist_batch_heuristic(tmp_repo):
    path = tmp_repo["root"] / "vcp.json"
    _write_screener(path, [], 2)
    assert screener_covers_ticker(path, "VECO", ["MRAM", "VECO"]) is True


def test_screener_covers_ticker_missing_coverage(tmp_repo):
    path = tmp_repo["root"] / "vcp.json"
    _write_screener(path, ["MRAM"], 1)
    assert screener_covers_ticker(path, "VECO", ["MRAM", "VECO"]) is False


def test_find_screener_for_ticker_prefers_covering_file(tmp_repo):
    as_of = date(2026, 5, 31)
    vcp_dir = artifact_dir(tmp_repo["root"], "vcp_screener", mkdir=True)
    _write_screener(vcp_dir / "vcp_screener_2026-05-31_080928.json", ["MRAM"], 1)
    _write_screener(vcp_dir / "vcp_screener_2026-05-31_081301.json", [], 2)
    found = find_screener_for_ticker(
        tmp_repo["root"], "vcp_screener", "VECO", as_of, ["MRAM", "VECO"]
    )
    assert found is not None
    assert found.name == "vcp_screener_2026-05-31_081301.json"


def test_market_context_path(tmp_repo):
    as_of = date(2026, 5, 31)
    assert market_context_path(tmp_repo["root"], as_of) is None
    ctx = tmp_repo["logs"] / "market_context_2026-05-31.md"
    ctx.write_text("# context\n")
    assert market_context_path(tmp_repo["root"], as_of) == ctx


def test_load_watchlist_symbols(tmp_repo):
    symbols = load_watchlist_symbols(tmp_repo["watchlist"])
    assert symbols == ["MRAM", "VECO"]


def test_preflight_manifest_reuses_market_context(tmp_repo):
    as_of = date(2026, 5, 31)
    (tmp_repo["logs"] / "market_context_2026-05-31.md").write_text("# Pre-Market\n")
    manifest = build_preflight_manifest("VECO", as_of, repo_root=tmp_repo["root"])
    assert manifest["artifacts"]["market_context"]["action"] == "reuse"
    assert manifest["artifacts"]["market_breadth"]["action"] == "reuse"
    assert manifest["artifacts"]["market_context"].get("run_hint") is None


def test_preflight_manifest_runs_market_context_when_missing(tmp_repo):
    as_of = date(2026, 5, 31)
    manifest = build_preflight_manifest("VECO", as_of, repo_root=tmp_repo["root"])
    assert manifest["artifacts"]["market_context"]["action"] == "run"
    assert "pre_market.py" in (manifest["artifacts"]["market_context"].get("run_hint") or "")


def test_preflight_manifest_reuses_vcp_when_covered(tmp_repo):
    as_of = date(2026, 5, 31)
    (tmp_repo["logs"] / "market_context_2026-05-31.md").write_text("# ctx\n")
    vcp_dir = artifact_dir(tmp_repo["root"], "vcp_screener", mkdir=True)
    _write_screener(vcp_dir / "vcp_screener_2026-05-31_081301.json", [], 2)
    manifest = build_preflight_manifest("VECO", as_of, repo_root=tmp_repo["root"])
    assert manifest["artifacts"]["vcp_screener"]["action"] == "reuse"


def test_preflight_manifest_runs_vcp_when_not_covered(tmp_repo):
    as_of = date(2026, 5, 31)
    manifest = build_preflight_manifest("VECO", as_of, repo_root=tmp_repo["root"])
    assert manifest["artifacts"]["vcp_screener"]["action"] == "run"


def test_force_refresh_marks_batch_run(tmp_repo):
    as_of = date(2026, 5, 31)
    (tmp_repo["logs"] / "market_context_2026-05-31.md").write_text("# ctx\n")
    vcp_dir = artifact_dir(tmp_repo["root"], "vcp_screener", mkdir=True)
    _write_screener(vcp_dir / "vcp_screener_2026-05-31_081301.json", [], 2)
    manifest = build_preflight_manifest(
        "VECO", as_of, force_refresh=True, repo_root=tmp_repo["root"]
    )
    assert manifest["artifacts"]["market_context"]["action"] == "run"
    assert manifest["artifacts"]["vcp_screener"]["action"] == "run"
