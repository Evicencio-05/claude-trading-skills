# Phase 1 Housekeeping Summary

**Completed:** 2026-05-10
**Commits:** 13

---

## What Changed

### New Files Created

| File | Purpose |
|------|---------|
| `decisions.md` | Binding decisions log — Phase 1 API, architecture, portfolio decisions |
| `LOAD_GUIDE.md` | Session routing table — what to load, when, and what to skip |
| `project-docs/STATUS.md` | Current project state, blockers, exit criteria progress |
| `project-docs/playbook.md` | Operational rules from live trading, audit, and system operation |
| `project-docs/audit/skills_audit.md` | 528-line operational summary (ratings, workflow, FMP, progress, live run) |
| `project-docs/audit/skills_audit_detail.md` | Full per-skill audit entries (970 lines, load only when investigating a skill) |
| `examples/README.md` | Orientation note explaining examples/ is upstream reference only |
| `launchd/README.md` | Warning that launchd jobs are disabled until Phase 3 |
| `project-docs/housekeeping/housekeeping_phase1_summary.md` | This file |

### Modified Files

| File | Change |
|------|--------|
| `CLAUDE.md` | Router header prepended — do not load full file routinely |
| `PROJECT.md` | Current Status section replaced with one-line pointer to STATUS.md |
| `.gitignore` | Added comment explaining reports/ exclusion |
| `scripts/hooks/check_docs_completeness.py` | Removed docs/ja/ requirement (now checks en/ only) |

### Moved Files

| From | To |
|------|----|
| `PROJECT_VISION.md` | `docs/internal/UPSTREAM_VISION.md` |

### Deleted

| Item | Reason |
|------|--------|
| `PROJECT_VISION.ja.md` | Japanese upstream vision doc, never read |
| `README.ja.md` | Japanese upstream README, never read |
| `docs/ja/` (55 files) | Japanese docs site — unused, hook updated to not require them |
| `skill-packages/` (54 .skill files) | Distribution ZIPs — private fork, no distribution use case |
| `examples/weekly-trade-strategy/` (107 files) | Stale Nov 2025 skill copies — confusion risk |
| `skills_audit.md` (root) | Split into project-docs/audit/; root file deleted |
| Local `reports/` files (30+) | Moved to ~/trading-research/ or deleted (gitignored, not in repo) |

---

## What Was Kept (and Why)

| Kept | Reason |
|------|--------|
| `docs/en/` | 55 skill documentation pages — hook still checks these |
| `docs/internal/` | Design docs and revision history — Phase 3 reference |
| `examples/daily-market-dashboard/` | Phase 3 Streamlit build reference |
| `launchd/` (plist files) | Disabled but needed for Phase 3 setup |
| `state/` | Live trade thesis data — untouched per cardinal rules |
| All `skills/*/SKILL.md` | Upstream skill definitions — untouched per cardinal rules |
| All `skills/*/scripts/` | Upstream skill scripts — untouched per cardinal rules |

---

## What Was Deferred

| Item | Reason / Next Action |
|------|---------------------|
| `decisions.md` long-term maintenance | Add entries at end of each phase |
| `project-docs/playbook.md` setups | Populate after 10+ logged trades (Phase 1 exit criteria) |
| FMP Starter upgrade | Approved — activate before next live session |
| Alpaca paper account | Approved — set up before Phase 2 |
| docs/internal/kanchi-dividend-skills-runbook.md | Kept — dividend workflow not current priority |
| docs/internal/revisions/ (3 files) | Kept — upstream improvement history, not noise |

---

## Remaining Concerns

1. **skills_audit.md summary is 528 lines**, not ~200 as targeted. The First Live Run section
   (127 lines) plus Tier Key Observations push it above target. This is acceptable — the content
   is operational reference, not per-skill detail. The detail file (970 lines) stays separate.

2. **LOAD_GUIDE.md needs updating after each phase.** It references skills_audit.md at the new
   path — verify this is reflected in the guide (it is: `project-docs/audit/skills_audit.md`).

3. **pre-commit hook was modified** to remove docs/ja/ requirement. If the repo is ever
   contributed upstream, this hook change must be reverted before submission.

4. **~/trading-research/ is now the canonical reports location.** The reports/ directory in
   the repo remains gitignored but should be kept clean. Run `find reports/ -maxdepth 1 -type f`
   at each phase end to catch stray outputs.

---

## Recurring Phase-End Checklist (for future phases)

1. Check STATUS.md — what claims are stale?
2. Check playbook.md — any new rules from this phase?
3. Run: `git ls-files -o --exclude-standard` (find untracked files)
4. Run: `find reports/ -maxdepth 1 -name "*.md" -o -name "*.json"` (catch generated outputs)
5. Verify LOAD_GUIDE.md matches actual file structure
6. Pre-commit hooks pass on all files
7. Commit housekeeping changes
