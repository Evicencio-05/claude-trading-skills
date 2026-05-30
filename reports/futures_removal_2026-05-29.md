# Futures Scope Removal — 2026-05-29

## Decision

- [x] decisions.md entry added ([2026-05-29] equity-only roadmap)

## Archived

| File | New path |
|------|----------|
| `project-docs/phase-1-audit.md` | `project-docs/archive/phase-1-audit.md` |
| `project-docs/phase-1b-robinhood-research.md` | `project-docs/archive/phase-1b-robinhood-research.md` |
| `project-docs/phase-2-futures-skills.md` | `project-docs/archive/phase-2-futures-skills.md` |
| `project-docs/phase-3-learning-loop.md` | `project-docs/archive/phase-3-learning-loop.md` |
| `project-docs/phase-4-backtesting.md` | `project-docs/archive/phase-4-backtesting.md` |
| `project-docs/phase-5-live-execution.md` | `project-docs/archive/phase-5-live-execution.md` |
| `project-docs/reference/lucid-rules.md` | `project-docs/archive/reference/lucid-rules.md` |

Stubs at old paths: `phase-1b-robinhood-research.md`, `phase-2-futures-skills.md`, `reference/lucid-rules.md`.

## New phase docs

| Phase | File | Status |
|-------|------|--------|
| 1 — Research + Co-pilot | `project-docs/phase-1-research-copilot.md` | Created (active) |
| 2 — Learning Loop | `project-docs/phase-2-learning-loop.md` | Created |
| 3 — Agentic Execution | `project-docs/phase-3-agentic-execution.md` | Created |

## Router updates

| File | Updated? |
|------|----------|
| `PROJECT.md` | Yes — single goal, 3-phase table, equity non-negotiables |
| `LOAD_GUIDE.md` | Yes — 3 phases only, archive in never-load |
| `.cursor/rules/project-router.mdc` | Yes — Robinhood gates, Phase 3 autonomous gate |
| `project-docs/STATUS.md` | Yes — Phase 1 pointer, exit progress |
| `PENDING_WORK.md` | Yes — removed futures deferred section |
| `project-docs/playbook.md` | Yes — Lucid section removed |
| `project-docs/reference/risk-register.md` | Yes — equity/Agentic risks only |
| `project-docs/reference/cost-discipline.md` | Yes — Tradovate/Lucid removed |
| `project-docs/reference/existing-skills-map.md` | Yes — futures gaps removed |
| `project-docs/reference/tech-stack.md` | Yes — equity structure |
| `project-docs/audit/skills_audit.md` | Yes — futures stack removed |
| `.cursor/prompts/remove-futures-equity-focus.md` | Yes — prompt saved |
| `.cursor/prompts/README.md` | Yes — index row added |
| `AGENTS.md` | No change needed (no futures refs) |

## Grep residual check

| Pattern | Remaining hits in active tree | Action taken |
|---------|-------------------------------|--------------|
| `Lucid` / `lucid` | Stubs (`phase-2-futures-skills.md`, `lucid-rules.md`); `PROJECT.md` out-of-scope line; `decisions.md` historical + removal entry; prompt file | Acceptable — stubs and decision log |
| `Tradovate` | `decisions.md` out-of-scope entry only | Acceptable |
| `phase-1b` | Archive + stub only | Links redirect |
| `futures-setup` | None in active project-docs | — |
| `skills/*/SKILL.md` | Generic methodology mentions (e.g. technical-analyst) | Not edited per plan |

**Note:** `project-docs/audit/skills_audit_detail.md` retains historical dual-rating notes mentioning futures — load per-skill only; not in routine router path.

## Phase 1 exit checklist (unchanged criteria)

| Criterion | Status |
|-----------|--------|
| FMP Starter + vcp on watchlist | Partial |
| 14 days pre_market + posture log | 11/14 |
| 5+ deep/update on watchlist | 6 tickers; 3 stale |
| 10+ trades logged, ≥2 types | ❌ |
| 3+ Agentic co-pilot MCP trades | ❌ |
| IRA logged via MCP | ❌ |
| 2+ portfolio_review reports | 1/2 |
| Anthropic &lt;$20, pre-commit | Open |
