"""Tests for distill_prompt_learnings.py."""

from __future__ import annotations

import importlib.util
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest
import yaml


@pytest.fixture(scope="module")
def distill_module():
    """Load distill_prompt_learnings.py as a module."""
    script_path = Path(__file__).resolve().parents[1] / "distill_prompt_learnings.py"
    spec = importlib.util.spec_from_file_location("distill_prompt_learnings", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load distill_prompt_learnings.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SAMPLE_RETRO = """\
# Prompt Run Retro — 2026-05-30

**Task prompt:** inline
**Task family:** thesis_manager_dev
**Goal verdict:** partial

## Verification matrix

| Area | Status | Evidence |
|------|--------|----------|
| Goal | partial | reports/meta/thesis_manager_improvements_2026-05-30.md |

## Defect log

| # | What went wrong | Root cause | Prompt fix |
|---|-----------------|------------|------------|
| 1 | Agent edited state/theses directly | direct state theses edit | Name thesis_store.py in Steps |
| 2 | Referenced Phase 1B | stale phase name | Read STATUS.md for phase |

## Meta notes (prompt-engine / library)

- none

## Follow-ups

- PENDING_WORK: none
"""


def _write_learnings(path: Path, data: dict | None = None) -> None:
    default = {
        "meta": {"last_distilled": None, "retro_files_processed": []},
        "patterns": [
            {
                "id": "thesis_store_gate",
                "seen": 0,
                "root_cause": "direct_state_theses_edit",
                "fix": "Thesis writes via thesis_store.py only",
                "in_prompt_engine": True,
                "promote_candidate": False,
            }
        ],
        "task_families": {
            "thesis_manager_dev": {"runs": 0, "last_run": None},
        },
        "promoted_durable": ["sync-phase-docs.md"],
        "meta_prompts": [
            "prompt-engine.md",
            "prompt-complete.md",
            "prompt-distill.md",
            "README.md",
        ],
        "promote_threshold": 3,
        "archive_age_days": 60,
        "durable_run_threshold": 2,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data or default, sort_keys=False), encoding="utf-8")


def test_slugify_root_cause(distill_module):
    assert (
        distill_module.slugify_root_cause("direct state theses edit") == "direct_state_theses_edit"
    )
    assert distill_module.slugify_root_cause("Stale Phase Name!") == "stale_phase_name"


def test_match_pattern_id(distill_module):
    patterns = [{"id": "thesis_store_gate", "root_cause": "direct_state_theses_edit"}]
    assert (
        distill_module.match_pattern_id("direct state theses edit", patterns) == "thesis_store_gate"
    )
    assert distill_module.match_pattern_id("unknown cause", patterns) is None


def test_parse_retro(distill_module):
    parsed = distill_module.parse_retro(SAMPLE_RETRO)
    assert parsed["task_family"] == "thesis_manager_dev"
    assert parsed["task_prompt"] == "inline"
    assert parsed["goal_verdict"] == "partial"
    assert len(parsed["defects"]) == 2
    assert parsed["defects"][0]["root_cause"] == "direct state theses edit"


def test_find_unprocessed_retros(distill_module, tmp_path: Path):
    reports = tmp_path / "reports"
    reports.mkdir()
    retro = reports / "prompt_run_retro_2026-05-30.md"
    retro.write_text(SAMPLE_RETRO, encoding="utf-8")
    learnings = {"meta": {"retro_files_processed": []}}
    found = distill_module.find_unprocessed_retros(reports, learnings)
    assert len(found) == 1
    assert found[0].name == "prompt_run_retro_2026-05-30.md"


def test_find_unprocessed_retros_skips_processed(distill_module, tmp_path: Path):
    reports = tmp_path / "reports"
    reports.mkdir()
    retro = reports / "prompt_run_retro_2026-05-30.md"
    retro.write_text(SAMPLE_RETRO, encoding="utf-8")
    learnings = {"meta": {"retro_files_processed": ["prompt_run_retro_2026-05-30.md"]}}
    assert distill_module.find_unprocessed_retros(reports, learnings) == []


def test_apply_retro_updates_patterns(distill_module):
    learnings = {
        "patterns": [
            {
                "id": "thesis_store_gate",
                "seen": 2,
                "root_cause": "direct_state_theses_edit",
                "fix": "Use thesis_store",
                "promote_candidate": False,
            }
        ],
        "task_families": {"thesis_manager_dev": {"runs": 0, "last_run": None}},
        "promote_threshold": 3,
    }
    parsed = distill_module.parse_retro(SAMPLE_RETRO)
    changes = distill_module.apply_retro(learnings, parsed, retro_date=date(2026, 5, 30))
    pattern = next(p for p in learnings["patterns"] if p["id"] == "thesis_store_gate")
    assert pattern["seen"] == 3
    assert pattern["promote_candidate"] is True
    assert learnings["task_families"]["thesis_manager_dev"]["runs"] == 1
    assert "thesis_store_gate" in changes["promoted_patterns"]


def test_apply_retro_idempotent_pattern_count(distill_module):
    learnings = {
        "patterns": [
            {
                "id": "thesis_store_gate",
                "seen": 5,
                "root_cause": "direct_state_theses_edit",
                "fix": "Use thesis_store",
                "promote_candidate": True,
            }
        ],
        "task_families": {"thesis_manager_dev": {"runs": 1, "last_run": "2026-05-29"}},
        "promote_threshold": 3,
    }
    parsed = distill_module.parse_retro(SAMPLE_RETRO)
    before_seen = learnings["patterns"][0]["seen"]
    distill_module.apply_retro(learnings, parsed, retro_date=date(2026, 5, 30))
    # Only defects matching known patterns increment; stale phase may add new pattern
    assert learnings["patterns"][0]["seen"] >= before_seen


def test_archive_candidates(distill_module, tmp_path: Path):
    import os
    import time

    prompts_dir = tmp_path / ".cursor" / "prompts"
    prompts_dir.mkdir(parents=True)
    old_path = prompts_dir / "thesis-manager-old.md"
    old_path.write_text("# old", encoding="utf-8")
    old_ts = time.mktime((date.today() - timedelta(days=90)).timetuple())
    os.utime(old_path, (old_ts, old_ts))
    (prompts_dir / "sync-phase-docs.md").write_text("# durable", encoding="utf-8")
    learnings = {
        "promoted_durable": ["sync-phase-docs.md"],
        "meta_prompts": ["prompt-engine.md", "README.md"],
        "archive_age_days": 60,
    }
    retro_refs: dict[str, date] = {}
    candidates = distill_module.archive_candidates(
        prompts_dir, learnings, retro_refs, as_of=date.today()
    )
    names = [p.name for p in candidates]
    assert "thesis-manager-old.md" in names
    assert "sync-phase-docs.md" not in names


def test_run_distill_end_to_end(distill_module, tmp_path: Path):
    repo = tmp_path
    reports = repo / "reports"
    reports.mkdir()
    state = repo / "state"
    state.mkdir()
    prompts = repo / ".cursor" / "prompts"
    prompts.mkdir(parents=True)
    archive = prompts / "archive"
    archive.mkdir()

    learnings_path = state / "prompt_learnings.yaml"
    _write_learnings(learnings_path)

    retro_path = reports / "prompt_run_retro_2026-05-30.md"
    retro_path.write_text(SAMPLE_RETRO, encoding="utf-8")

    (prompts / "orphan-prompt.md").write_text("# orphan", encoding="utf-8")

    result = distill_module.run_distill(
        repo,
        dry_run=False,
        since=None,
        output_dir=reports,
    )
    assert result["retros_processed"] == 1
    assert (reports / f"prompt_learning_digest_{date.today().isoformat()}.md").exists()

    updated = yaml.safe_load(learnings_path.read_text(encoding="utf-8"))
    assert "prompt_run_retro_2026-05-30.md" in updated["meta"]["retro_files_processed"]
    assert updated["task_families"]["thesis_manager_dev"]["runs"] == 1

    # Second run is idempotent for retro processing
    result2 = distill_module.run_distill(repo, dry_run=False, since=None, output_dir=reports)
    assert result2["retros_processed"] == 0


def test_run_distill_dry_run_no_writes(distill_module, tmp_path: Path):
    repo = tmp_path
    reports = repo / "reports"
    reports.mkdir()
    state = repo / "state"
    state.mkdir()
    learnings_path = state / "prompt_learnings.yaml"
    _write_learnings(learnings_path)
    (reports / "prompt_run_retro_2026-05-30.md").write_text(SAMPLE_RETRO, encoding="utf-8")

    before = learnings_path.read_text(encoding="utf-8")
    result = distill_module.run_distill(repo, dry_run=True, since=None, output_dir=reports)
    assert result["retros_processed"] == 1
    assert learnings_path.read_text(encoding="utf-8") == before
    assert not list(reports.glob("prompt_learning_digest_*.md"))


def test_run_distill_enable_llm_dry_run(distill_module, tmp_path: Path, monkeypatch):
    repo = tmp_path
    reports = repo / "reports"
    reports.mkdir()
    state = repo / "state"
    state.mkdir()
    learnings_path = state / "prompt_learnings.yaml"
    _write_learnings(learnings_path)
    (reports / "prompt_run_retro_2026-05-30.md").write_text(SAMPLE_RETRO, encoding="utf-8")

    scripts = Path(__file__).resolve().parents[1]
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    import local_llm as llm_mod

    monkeypatch.setattr(
        llm_mod,
        "distill_suggest",
        lambda texts, learnings, repo_root=None: "- id: test_pattern\n  fix: test",
    )

    before = learnings_path.read_text(encoding="utf-8")
    result = distill_module.run_distill(
        repo,
        dry_run=True,
        since=None,
        output_dir=reports,
        enable_llm=True,
    )
    assert result["retros_processed"] == 1
    assert result.get("llm_suggestions") is not None
    assert learnings_path.read_text(encoding="utf-8") == before
