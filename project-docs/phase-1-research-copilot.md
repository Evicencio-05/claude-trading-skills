# Phase 1 — TA Confluence + Co-Pilot Trading

**Duration:** active from 2026-05-29; TA-first pivot 2026-08-09; charter A+C scope 2026-08-16  
**Goal:** Reliable three-source TA → confluence → thesis → co-pilot execution on Robinhood Agentic (C); thesis logging for **A + C only**. Fundamentals / deep-research are gated optional backup.

**Operator cadence:** [trading-pipeline-checklist.md](trading-pipeline-checklist.md) — daily TA + posture, weekly broker snapshot, per-trade Agentic steps.

**Prerequisites:** Phase 1 audit complete ([STATUS.md](STATUS.md), [skills_audit.md](audit/skills_audit.md)). TA intakes + `ta-confluence` shipped 2026-08-09.

> Filename kept as `phase-1-research-copilot.md` for stable links. Content is TA Confluence + Co-pilot.

---

## Why this phase exists

TA intakes, confluence fusion, and Agentic co-pilot workflows are built. This phase makes them **production habit**: lists + maps + operator charts → judgment → logged A/C theses → confirmed Agentic fills — before the Phase 2 learning loop. Deep research and FMP screeners remain gated backup — not the daily product.

---

## Workstreams (parallel)

### 1. Three-source TA pipeline (primary)

| Item | Target |
|------|--------|
| TW lists | Ingest when posted → `tradewhisperer-charts` (`list_tw_*`); HTF via `tw_list_resolve.py` |
| GEX/VEX | Paste maps → `gex-vex-maps` (no scrape; screenshots only) |
| Operator charts | Markup → `operator-charts` before any PLAY |
| Confluence | `ta-confluence` (candle_first or map_first) → PLAY / WATCH / NO_TRADE + judgment |
| Prediction log | v1.5 after real sessions — [.cursor/skills/ta-confluence/references/prediction_log_v15.md](../.cursor/skills/ta-confluence/references/prediction_log_v15.md) |
| Posture context | Daily `pre_market.py` (zero LLM) — filter size, not idea source |
| Cadence | Checklist § Daily / Weekly / TA session |

Ask for missing artifacts before forcing a score. Period **list** color required for PLAY. Lists older than 3 trading days cap at WATCH. NO_TRADE is success.

**Commands:** [ta-confluence.md](../commands/ta-confluence.md) · [tradewhisperer-charts.md](../commands/tradewhisperer-charts.md) · [gex-vex-maps.md](../commands/gex-vex-maps.md) · [operator-charts.md](../commands/operator-charts.md)

### 2. Thesis discipline (A + C only)

| Item | Target |
|------|--------|
| Accounts | Log `robinhood_agentic` (C) and `robinhood_taxable` (A) only |
| IRA (B) | **Do not log** — no four-questions cadence |
| Trade count | Agentic fills + A positions via `trader-memory-core` (link confluence artifact when from TA) |
| Thesis source | Prefer confluence briefs; link artifacts |
| Pending | Close/log expired A/C theses as needed (TSLA, PENG historically) |
| Rules | Never write `state/theses/` directly — `thesis_store.py` / thesis-manager only |

### 3. Optional backup research (gated)

| Item | When |
|------|------|
| Deep-research / update-research | **PLAY** verdict, or **verge of confluence** with user OK, or explicit ask |
| FMP screeners (`vcp`, canslim, earnings) | Optional shortlist aid — not daily center of gravity |
| Watchlist / preflight | Keep available; do not treat as Phase 1 primary KPI |

### 4. Robinhood co-pilot (Agentic C only)

See checklist § [Per-trade co-pilot](trading-pipeline-checklist.md#per-trade-co-pilot-agentic-only). Prefer plans that cite confluence + invalidation across TW / maps / operator domains.

**Never MCP trade:** IRA (`ira_robinhood`), taxable (`robinhood_taxable`). Taxable sync stays on `robinhood_sync.py`.

### 5. Cost & hygiene

- Anthropic spend tracking toward exit (&lt;$20)
- Pre-commit clean on commit
- New subscriptions → [decisions.md](../decisions.md) first
- Prefer local scripts / existing TA skills over LLM-heavy synthesis

---

## Exit criteria (Phase 1 → Phase 2)

Progress: [STATUS.md](STATUS.md).

- [x] TA intakes + `ta-confluence` + `agentic-copilot-trade` shipped
- [ ] Live full-stack confluence sessions (TW lists D+W + GEX/VEX + operator chart; same-day preferred)
- [ ] Prediction / process log v1.5 filled from real sessions
- [ ] 3+ co-pilot trades on Agentic (C) via MCP (user-confirmed each), preferably from PLAY confluence
- [ ] A+C trades logged via `trader-memory-core` (IRA not required)
- [ ] `reports/portfolio/portfolio_review_*.md` for 2+ dates (A+C focus)
- [ ] Anthropic spend cap met; pre-commit clean
- [ ] Deep-research not used as default daily work (PLAY / verge / explicit only)

*Legacy note:* “5+ deep-research on watchlist” and “IRA positions logged” are no longer Phase 1 exit gates.

**Not exit criteria:** deep-research count, FPS staleness, IRA logging, FMP Premium S&P universe.

---

## Explicitly NOT in Phase 1

- Autonomous MCP order placement (Phase 3 gate)
- MCP trades on IRA or taxable
- IRA thesis logging / four-questions
- Fundamentals-first daily pipeline as the product
- Upstream `skills/<name>/` rewrites except fixes in [decisions.md](../decisions.md)
- Full Phase 2 playbook distill automation (seed notes only)
- Prioritizing parked FMP/CI research debt over TA path

---

## References

- [trading-pipeline-checklist.md](trading-pipeline-checklist.md)
- [commands/ta-confluence.md](../commands/ta-confluence.md)
- [robinhood-mcp-integration.md](reference/robinhood-mcp-integration.md)
- [playbook.md](playbook.md)
- Standing session prompt: [`.cursor/prompts/ta-first-session.md`](../.cursor/prompts/ta-first-session.md)
- [PENDING_WORK.md](../PENDING_WORK.md)

---

## When ready to advance

Update `PROJECT.md` Active Phase to Phase 2. Read [phase-2-learning-loop.md](phase-2-learning-loop.md).
