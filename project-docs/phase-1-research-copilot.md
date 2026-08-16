# Phase 1 — TA Confluence + Co-Pilot Trading

**Duration:** 4–6 weeks (active from 2026-05-29; charter reframed TA-first 2026-08-16)
**Goal:** Reliable three-source TA → confluence → thesis → co-pilot execution on Robinhood Agentic. Fundamentals / deep-research are optional backup only.

**Operator cadence:** [trading-pipeline-checklist.md](trading-pipeline-checklist.md) — daily, weekly, TA session, and per-trade steps.

**Prerequisites:** Phase 1 audit complete ([STATUS.md](STATUS.md), [skills_audit.md](audit/skills_audit.md)). TA intakes + `ta-confluence` shipped 2026-08-09.

---

## Why this phase exists

TA intakes, confluence fusion, and Agentic co-pilot workflows are built. This phase makes them **production habit**: lists + maps + operator charts → judgment → logged theses → confirmed Agentic fills — before the Phase 2 learning loop.

---

## Workstreams (parallel)

### 1. Three-source TA pipeline (primary)

| Item | Target |
|------|--------|
| TW lists | Ingest when posted → `tradewhisperer-charts` (`list_tw_*`); HTF via `tw_list_resolve.py` |
| GEX/VEX | Paste maps → `gex-vex-maps` (no scrape; screenshots only) |
| Operator charts | Markup → `operator-charts` before any PLAY |
| Confluence | `ta-confluence` (candle_first or map_first) → PLAY / WATCH / NO_TRADE + judgment |
| Cadence | Checklist § Daily / Weekly / TA session |

Ask for missing artifacts before forcing a score. Period **list** color required for PLAY. NO_TRADE is success.

### 2. Thesis discipline

| Item | Target |
|------|--------|
| Trade count | 10+ logged across ≥2 types (stock, option; paper OK) |
| Thesis source | Prefer confluence briefs; link artifacts |
| IRA | All open IRA positions in `trader-memory-core` via MCP + `log-positions` |
| Rules | Never write `state/theses/` directly — `thesis_store.py` / thesis-manager only |

### 3. Optional backup research (gated)

| Item | When |
|------|------|
| Deep-research / update-research | **PLAY** verdict, or **verge of confluence** with user OK, or explicit ask |
| FMP screeners (`vcp`, canslim, earnings) | Optional shortlist aid — not daily center of gravity |
| Watchlist / preflight | Keep available; do not treat as Phase 1 primary KPI |

### 4. Robinhood co-pilot (Agentic only)

See checklist § [Per-trade co-pilot](trading-pipeline-checklist.md#per-trade-co-pilot-agentic-only). Prefer plans that cite confluence + invalidation across TW / maps / operator domains.

**Never MCP trade:** IRA (`ira_robinhood`), taxable (`robinhood_taxable`). Taxable sync stays on `robinhood_sync.py`.

### 5. Cost & hygiene

- Anthropic spend tracking toward exit (&lt;$20)
- Pre-commit clean on commit
- New subscriptions → [decisions.md](../decisions.md) first
- Prefer local scripts / existing TA skills over LLM-heavy synthesis

---

## Exit criteria (Phase 1 → Phase 2)

Progress detail: [STATUS.md](STATUS.md) and [docs_sync_2026-05-30.md](../reports/meta/docs_sync_2026-05-30.md).

- [x] TA intakes + `ta-confluence` operational (2026-08-09)
- [x] FMP Starter active; watchlist tools available as optional backup (2026-05-31)
- [ ] 14 consecutive trading days: `pre_market.py` + posture log (**12/14** unique days as of 2026-05-30)
- [ ] Regular confluence sessions with all three sources when trading (spot-check recent `reports/charts/confluence/`)
- [ ] 10+ trades logged across ≥2 types via `trader-memory-core`
- [ ] 3+ co-pilot trades on Agentic via MCP (user-confirmed each), preferably from PLAY confluence
- [ ] IRA positions logged (MCP read + four questions)
- [ ] `reports/portfolio/portfolio_review_*.md` for 2+ dates
- [ ] Anthropic spend cap met; pre-commit clean
- [ ] Deep-research not used as default daily work (PLAY / verge / explicit only)

*Legacy note:* “5+ deep-research on watchlist” is no longer a Phase 1 exit gate; retained reports remain useful backup.

---

## Explicitly NOT in Phase 1

- Autonomous MCP order placement (Phase 3 gate)
- MCP trades on IRA or taxable
- Fundamentals-first daily pipeline as the product
- Upstream `skills/<name>/` rewrites except fixes in [decisions.md](../decisions.md)
- Full Phase 2 playbook distill automation (seed notes only)

---

## References

- [trading-pipeline-checklist.md](trading-pipeline-checklist.md)
- [commands/ta-confluence.md](../commands/ta-confluence.md)
- [robinhood-mcp-integration.md](reference/robinhood-mcp-integration.md)
- [playbook.md](playbook.md)
- Standing session prompt: [`.cursor/prompts/ta-first-session.md`](../.cursor/prompts/ta-first-session.md)

---

## When ready to advance

Update `PROJECT.md` Active Phase to Phase 2. Read [phase-2-learning-loop.md](phase-2-learning-loop.md).
