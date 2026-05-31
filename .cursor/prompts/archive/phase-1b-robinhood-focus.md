# Phase Reprioritization — Research Pipeline + Robinhood MCP Trading

## Goal
Defer **Futures skills (old Phase 2)** to a later phase, extend the current **stock/options research pipeline**, and stand up **co-pilot trading via Robinhood MCP** (Agentic account) — updating project docs to reflect the new roadmap without breaking single-source-of-truth conventions.

## Inputs
- **Futures defer until:** user specifies trigger (default: Phase 1B exit criteria met + 20+ logged stock/options trades)
- **Trading mode:** co-pilot only — user confirms every order (not Phase 5 autonomous)
- **Capital focus:** Portfolio A (~$250 taxable sync) + Portfolio C (~$50 Agentic MCP trades) + Portfolio B IRA read/log only

## Pre-flight
- [ ] Read `PROJECT.md`, `LOAD_GUIDE.md`, `project-docs/STATUS.md`, `PENDING_WORK.md`, `decisions.md`
- [ ] Read `.cursor/rules/robinhood-mcp.mdc` and `project-docs/reference/robinhood-mcp-integration.md`
- [ ] Read `project-docs/phase-1-audit.md` (remaining exit criteria) and `project-docs/phase-2-futures-skills.md` (what is being deferred)
- [ ] Verify MCP CLI works:
  ```bash
  uv run python3 scripts/robinhood_mcp.py accounts
  uv run python3 scripts/robinhood_mcp.py positions --all
  ```

## Phase A — Record the decision (docs first)

### 1. Log binding decision in `decisions.md`

Add entry under **Architecture** or new **Phase roadmap** section:

```
[YYYY-MM-DD] Futures Phase 2 deferred; Robinhood research + co-pilot trading prioritized.
Rationale: Phase 1 research pipeline not yet production-ready; Robinhood MCP hybrid
built but unused for live workflow; Lucid eval continues manually without new futures skills.
Decision: Active work = Phase 1B (research pipeline + Robinhood co-pilot). Old Phase 2
(futures skills) starts only after Phase 1B exit criteria met.
Revisit: Phase 1B exit checklist complete.
```

### 2. Create active phase doc

Write `project-docs/phase-1b-robinhood-research.md` with:

**Duration:** 4–6 weeks (starts immediately after this reprioritization)

**Goal:** Reliable daily research → thesis → co-pilot execution loop on Robinhood Agentic; complete Phase 1 exit gaps.

**Prerequisites:** Phase 1 audit largely done (see STATUS.md)

**Workstreams (parallel):**

| Stream | Deliverables |
|--------|--------------|
| **Research pipeline** | FMP Starter activated; vcp/canslim/earnings stack unblocked; `pre_market.py` → exposure-coach daily; `/deep-research` + `/update-research` on watchlist; stale report cadence via `review-portfolio` |
| **Thesis discipline** | All open positions in `trader-memory-core`; MCP `ingest-pending` + `log-positions` for IRA; 10+ trades across ≥2 types (stock, option, paper OK) |
| **Robinhood co-pilot** | Weekly `robinhood-portfolio-review`; pre-trade checklist; Agentic-only MCP orders with user confirmation; post-trade thesis update within same session |
| **Cost & hygiene** | Anthropic spend tracking; pre-commit clean; no new subscriptions without `decisions.md` entry |

**Exit criteria (Phase 1B → then revisit futures):**
- [ ] FMP Starter active; vcp-screener runs on at least one watchlist ticker
- [ ] 14 consecutive trading days: `pre_market.py` + posture log
- [ ] 5+ `/deep-research` or `/update-research` reports on active watchlist
- [ ] 10+ trades logged (real or paper) across ≥2 types via `trader-memory-core`
- [ ] 3+ co-pilot trades executed on Agentic via MCP (user-confirmed each)
- [ ] IRA positions logged (MCP read + `log-positions` four questions)
- [ ] `reports/portfolio/portfolio_review_*.md` exists for 2+ dates
- [ ] Phase 1 remaining exit items closed (spend, pre-commit)

**Explicitly NOT in Phase 1B:**
- Building `lucid-rules-engine`, `tradovate-integration`, or other futures skills from `phase-2-futures-skills.md`
- Autonomous order placement (Phase 5 gate)
- MCP trades on IRA or taxable accounts
- Upstream skill rewrites (fork policy)

### 3. Update router files (minimal, linked — no duplication)

| File | Change |
|------|--------|
| `PROJECT.md` | Active phase → Phase 1B; phase table: insert 1B row; mark old Phase 2 futures as **Deferred** with link to `phase-2-futures-skills.md` |
| `project-docs/STATUS.md` | Active phase, this week's focus, exit criteria progress for 1B |
| `LOAD_GUIDE.md` | Phase-conditional table: load `phase-1b-robinhood-research.md` when active |
| `.cursor/rules/project-router.mdc` | One-line active phase pointer if it hardcodes Phase 1 |
| `PENDING_WORK.md` | Reorder queue: research pipeline + MCP trading above futures; mark futures items Phase 3+ |
| `phase-2-futures-skills.md` | Top banner: `> DEFERRED — see decisions.md [date]. Do not start until Phase 1B exit.` |

**Do not renumber Phase 3–5 files** unless user explicitly asks — defer futures in place with banner + decision log.

## Phase B — Research pipeline improvements (execute in priority order)

### P0 — Unblock screeners
1. Confirm FMP Starter upgrade status with user; if approved, document activation steps in STATUS.md
2. Verify: `vcp-screener`, `earnings-trade-analyzer`, `economic-calendar-fetcher` OR confirm `fred_calendar.py` remains canonical per `decisions.md`
3. Run one end-to-end research pass on a live watchlist ticker using `commands/deep-research.md`

### P1 — Daily stack hardening
1. Confirm `pre_market.py` systemd timer healthy
2. Document watchlist → research → update cadence in `PENDING_WORK.md` (weekly `review-portfolio` + stale >14d alerts)

### P2 — Pipeline gaps (audit-driven)
1. Read `project-docs/audit/skills_audit.md` — fix or document top 3 gaps blocking *your* swing workflow
2. Prefer extending commands/skills wrappers over editing upstream `skills/` (fork policy)

## Phase C — Robinhood MCP co-pilot trading (read → plan → confirm → execute → log)

### Operating rules (non-negotiable)
- **Read:** all accounts via `robinhood_mcp.py` or skill `robinhood-portfolio-review`
- **Trade:** Agentic account only; user must confirm ticker, direction, size, order type before any MCP order tool
- **IRA (Portfolio B):** read + recommend with IRA-eligible flag; never MCP trade
- **Taxable (Portfolio A):** sync via `robinhood_sync.py`; no MCP trades
- **After every fill:** log to `trader-memory-core` same session (`log-positions` or thesis transition)

### First co-pilot trade checklist (template for each trade)
1. Run `robinhood-portfolio-review` — note buying power, existing exposure
2. Run `exposure-coach` + today's `pre_market` context — confirm new entry allowed
3. Run `position-sizer` for Agentic account size
4. Present trade plan: entry, stop, target, IRA eligibility N/A (Agentic), risk $
5. **Stop — wait for user "confirm"**
6. Execute via MCP only after confirmation
7. Log thesis + attach position via `trader-memory-core`

### Bootstrap sequence (first session)
1. Skill `robinhood-portfolio-review` → save report
2. Skill `log-positions` (MCP Source B) for any unlogged positions
3. Identify one small Agentic trade aligned with existing research (≤5% of Agentic equity)
4. Walk co-pilot checklist above — do not skip confirmation step

## Phase D — Deliverable

Write session summary to `reports/meta/phase_1b_kickoff_YYYY-MM-DD.md`:

```markdown
# Phase 1B Kickoff — YYYY-MM-DD

## Decision recorded
- [ ] decisions.md entry added
- [ ] phase-1b doc created
- [ ] Router files updated

## Research pipeline status
| Component | Status | Next action |

## Robinhood MCP status
| Account | Read | Trade | Logged in thesis_store |

## Phase 1 / 1B exit checklist
| Criterion | Done? |

## Deferred (futures)
- phase-2-futures-skills.md — revisit when: [criteria]
```

## Rules
- **Co-pilot, not autonomous** — contradicts Phase 5 gate if agent places orders without explicit user confirmation
- **Audit before building** — improve existing pipeline before new skills
- **Lucid eval** continues manually; no new futures skill development this phase
- **Cost discipline** — scripts first (`pre_market`, CLI MCP); justify LLM-heavy runs
- Doc changes only in Phase A unless user says to execute B/C in same session

## Do not
- Start `lucid-rules-engine`, `tradovate-integration`, or `/futures-setup` work
- Place MCP orders without user confirmation on each trade
- Trade IRA or taxable via MCP
- Rewrite upstream `skills/` except fixes listed in `decisions.md`
- Commit doc updates unless user explicitly asks
- Delete or archive `phase-2-futures-skills.md` — defer with banner only

## After run
Paste [prompt-complete.md](prompt-complete.md) with `phase-1b-robinhood-focus.md`.
