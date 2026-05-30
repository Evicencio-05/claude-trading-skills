# Remove Futures — Equity-Only Project Refocus

## Goal
Permanently remove futures/Lucid/Tradovate scope from this fork and restructure the roadmap into three phases focused on stock research, market analysis, portfolio management, Robinhood Agentic co-pilot/autonomous trading, and the skills learning loop.

## Inputs
- **Archive location:** `project-docs/archive/` (default)
- **Active phase after rewrite:** Phase 1 — Research + Co-pilot (content from current `phase-1b-robinhood-research.md`)
- **Trading mode:** co-pilot until Phase 3 sub-phase criteria met; no autonomous orders before Phase 3B
- **Commit:** only if user explicitly asks

## Pre-flight
- [ ] Read `PROJECT.md`, `LOAD_GUIDE.md`, `project-docs/STATUS.md`, `PENDING_WORK.md`, `decisions.md`
- [ ] Read `.cursor/prompts/phase-1b-robinhood-focus.md` (prior deferral — supersede, do not duplicate defer banners)
- [ ] Read `.cursor/rules/robinhood-mcp.mdc`, `project-docs/reference/robinhood-mcp-integration.md`
- [ ] Grep repo for `Lucid`, `lucid`, `Tradovate`, `futures-setup`, `phase-2-futures` — build a removal checklist before editing

## Phase A — Record binding decision

### 1. Add to `decisions.md` under **Phase roadmap**

```
[YYYY-MM-DD] Futures scope removed permanently; equity-only roadmap.
Rationale: Project focus = US equity/options research, market analysis, Robinhood portfolio management, Agentic MCP trading, and skill learning loop. Lucid eval and futures skill build are out of scope.
Decision: Archive futures phase/reference docs. Collapse roadmap to 3 phases (Research+Co-pilot → Learning Loop → Agentic Execution). Supersedes [2026-05-28] defer entry.
Revisit: Never — unless user explicitly reopens futures in a new decision entry.
```

### 2. Archive futures artifacts (move, do not delete)

Move to `project-docs/archive/` with a one-line README in that folder listing archived files and date:

| Source | Notes |
|--------|-------|
| `project-docs/phase-2-futures-skills.md` | Full futures skill build plan |
| `project-docs/reference/lucid-rules.md` | Prop firm rules reference |
| `project-docs/phase-3-learning-loop.md` | After content extracted to new Phase 2 |
| `project-docs/phase-4-backtesting.md` | After equity backtest sections extracted |
| `project-docs/phase-5-live-execution.md` | After Agentic execution structure extracted |

Fix all internal links that pointed at archived paths → new phase docs or archive note.

## Phase B — Rewrite charter and routers

### 1. `PROJECT.md`
- **Single goal:** AI trading partner for US equities/options — research, market context, portfolio management, Robinhood Agentic execution, continuous learning
- Remove Goal B, Lucid/Tradovate operating constraints, 4:45 PM flatten, Lucid glossary terms
- Replace non-negotiables #2–5 (futures/Lucid) with equity equivalents: Robinhood MCP gates, Phase 3 autonomous gate, IRA rules
- New phase table (3 rows only):

| Phase | Doc | Focus |
|-------|-----|-------|
| **Phase 1** | `project-docs/phase-1-research-copilot.md` | Research pipeline + Robinhood co-pilot |
| Phase 2 | `project-docs/phase-2-learning-loop.md` | Behavioral patterns, playbook, skill improvement |
| Phase 3 | `project-docs/phase-3-agentic-execution.md` | Agentic MCP autonomous execution |

- Remove "both goals" session hygiene guidance; remove Lucid reference from reference table

### 2. `LOAD_GUIDE.md`
- Phase-conditional table: 3 phases only; remove Phase 2 futures deferred row and `lucid-rules.md` on-demand row
- Update "Key Operational Facts" — no futures defer language

### 3. `.cursor/rules/project-router.mdc`
- Remove non-negotiable #2 (Lucid sacred) and #4–5 (HFT/Lucid flatten) — keep Robinhood/Phase 3 execution gates
- Remove "Futures work → lucid-rules.md" from on-demand table
- Active phase pointer → Phase 1 doc

### 4. `AGENTS.md`
- Remove Tradovate/futures sync references if present

## Phase C — Write three new phase docs

### `phase-1-research-copilot.md`
Port from `phase-1b-robinhood-research.md`:
- Workstreams: research pipeline, thesis discipline, Robinhood co-pilot, cost/hygiene
- Exit criteria unchanged (FMP, 14d pre_market, 10+ trades, 3+ Agentic co-pilot, IRA logged)
- **Explicitly NOT:** any futures/Lucid/Tradovate work
- Advance to Phase 2 when exit criteria met

### `phase-2-learning-loop.md`
Port from archived `phase-3-learning-loop.md`:
- **Remove:** all futures setup sections, Lucid dashboard fields, `/futures-setup` hooks, futures behavioral patterns, "both workflows" language
- **Keep:** behavioral-pattern-detector (stock/options), personal playbook (stock/options only), research quality tracking, Streamlit dashboard (Robinhood), skill-improvement loop (3.6), Skylit decision
- **Fold in from archived Phase 4 (equity only):** use `backtest-expert` skill to validate playbook setups on historical equity data; quality gates (win rate, drawdown, walk-forward) — no ES/NQ data, no Lucid sim, no `lucid-rules-engine`
- Exit criteria: stock/options playbook 3+ setups, 30+ logged trades, research outcomes tracked, skill loop enabled — drop Lucid eval requirement

### `phase-3-agentic-execution.md`
Port structure from archived Phase 5, retarget to Robinhood Agentic MCP:
- **3A Co-pilot live:** user confirms every MCP order; 8+ weeks minimum
- **3B Autonomous test:** small Agentic allocation; executor reads hard limits from config (max position %, daily loss, cooldowns, news blackout) — **not** `lucid-rules-engine`
- **3C Scale:** gradual after 3B evidence
- Sync: `robinhood_sync.py` + MCP + `trader-memory-core` reconciliation
- Remove all Lucid/Tradovate/futures-executor references
- Prerequisites: Phase 2 exit met

Archive `phase-1b-robinhood-research.md` and `phase-1-audit.md` to `project-docs/archive/` after Phase 1 doc is written (audit remains historical reference).

## Phase D — Strip futures from operational docs

| File | Action |
|------|--------|
| `project-docs/playbook.md` | Remove "Lucid Trading Rules" section; account table: drop Tradovate row |
| `PENDING_WORK.md` | Remove "Deferred (futures)" section and futures queue items |
| `project-docs/STATUS.md` | Remove futures defer/Lucid eval exit items; update phase pointer and exit progress to Phase 1 |
| `project-docs/reference/risk-register.md` | Remove C1/C6 Lucid rows, M5 Tradovate, R1/R2 prop firm rows |
| `project-docs/reference/cost-discipline.md` | Remove `/futures-setup`, Tradovate/Lucid sections |
| `project-docs/reference/existing-skills-map.md` | Remove "Phase 2 build" futures gap table; remove futures translation section |
| `project-docs/audit/skills_audit.md` | Remove "Futures pre-session stack" and Lucid upgrade conditions |
| `.cursor/prompts/README.md` | Add row for this prompt |

**Do not edit** upstream `skills/*/SKILL.md` for generic instrument mentions unless a skill is futures-only (none exist as built skills).

## Phase E — Deliverable

Write `reports/futures_removal_YYYY-MM-DD.md`:

```markdown
# Futures Scope Removal — YYYY-MM-DD

## Decision
- [ ] decisions.md entry added

## Archived
| File | New path |

## New phase docs
| Phase | File | Status |

## Router updates
| File | Updated? |

## Grep residual check
| Pattern | Remaining hits in project-docs/ | Action taken |

## Phase 1 exit checklist (unchanged criteria)
| Criterion | Status |
```

## Rules
- **Archive, don't delete** futures docs — recoverable under `project-docs/archive/`
- **Single source of truth:** phase content lives in `project-docs/phase-*.md`; routers link, don't duplicate
- **Robinhood gates unchanged:** read all accounts; trade Agentic only; flag IRA-ineligible options
- **No autonomous MCP orders** until Phase 3B criteria documented in new phase doc
- **Supersede** `phase-1b-robinhood-focus.md` defer approach — futures is removed, not deferred
- On broken cross-links after archive: fix or add `> Archived — see project-docs/archive/` stub at old path

## Do not
- Build `lucid-rules-engine`, `tradovate-integration`, or `/futures-setup`
- Leave DEFERRED banners on futures docs in active tree — archive them
- Rewrite upstream `skills/` except fixes already in `decisions.md`
- Commit unless user explicitly asks
- Remove generic "works on futures charts" notes inside skill methodology references
