# Phase 1 — TA + Co-Pilot Trading

**Duration:** active from 2026-05-29; TA-first pivot 2026-08-09; charter A+C scope 2026-08-16  
**Goal:** Reliable TA session → confluence brief → co-pilot execution on Robinhood Agentic (C); thesis logging for **A + C only**.

**Operator cadence:** [trading-pipeline-checklist.md](trading-pipeline-checklist.md) — daily TA + posture, weekly broker snapshot, per-trade Agentic steps.

**Prerequisites:** Phase 1 audit complete ([STATUS.md](STATUS.md), [skills_audit.md](audit/skills_audit.md)). TA intakes + `ta-confluence` shipped.

> Filename kept as `phase-1-research-copilot.md` for stable links. Content is TA + Co-pilot.

---

## Why this phase exists

Chart intakes, confluence, and Robinhood MCP co-pilot are built. The gap is **live full-stack TA sessions**, **confirmed Agentic fills from PLAY**, and **A/C thesis discipline** before the learning loop (Phase 2). Deep research and FMP screeners remain available on demand — they are not the daily product.

---

## Workstreams (parallel)

### 1. TA pipeline (primary)

| Item | Target |
|------|--------|
| Intakes | TW **lists** (color SoT) + GEX/VEX + operator charts → `reports/charts/` |
| Resolve | `scripts/tw_list_resolve.py` shortlist / stack / overlap |
| Fusion | `/ta-confluence` candle_first or map_first → PLAY/WATCH/NO_TRADE |
| Prediction log | v1.5 after real sessions — [.cursor/skills/ta-confluence/references/prediction_log_v15.md](../.cursor/skills/ta-confluence/references/prediction_log_v15.md) |
| Posture context | Daily `pre_market.py` (zero LLM) — filter size, not idea source |

**Commands:** [ta-confluence.md](../commands/ta-confluence.md) · [tradewhisperer-charts.md](../commands/tradewhisperer-charts.md) · [gex-vex-maps.md](../commands/gex-vex-maps.md) · [operator-charts.md](../commands/operator-charts.md)

### 2. Thesis discipline (A + C only)

| Item | Target |
|------|--------|
| Accounts | Log `robinhood_agentic` (C) and `robinhood_taxable` (A) only |
| IRA (B) | **Do not log** — no four-questions cadence |
| Trade count | Agentic fills + A positions via `trader-memory-core` (link confluence artifact when from TA) |
| Pending | Close/log expired A/C theses as needed (TSLA, PENG historically) |
| Rules | Never write `state/theses/` directly — `thesis_store.py` / thesis-manager only |

### 3. Robinhood co-pilot (Agentic C only)

See checklist § [Per-trade co-pilot](trading-pipeline-checklist.md#per-trade-co-pilot-agentic-only).

**Never MCP trade:** IRA (`ira_robinhood`), taxable (`robinhood_taxable`). Taxable sync stays on `robinhood_sync.py`.

### 4. Optional research (on demand — not exit-blocking)

| Item | Notes |
|------|--------|
| Deep / update research | [commands/deep-research.md](../commands/deep-research.md) when fundamentals matter |
| Screeners | `--universe` watchlist on FMP Starter; Premium not required for Phase 1 |
| Watchlist | [config/research_watchlist.yaml](../config/research_watchlist.yaml) |

### 5. Cost & hygiene

- Anthropic spend tracking toward exit (&lt;$20)
- Pre-commit clean on commit
- New subscriptions → [decisions.md](../decisions.md) first

---

## Exit criteria (Phase 1 → Phase 2)

Progress: [STATUS.md](STATUS.md).

- [x] TA intakes + `ta-confluence` + `agentic-copilot-trade` shipped
- [ ] Live full-stack confluence sessions (TW lists D+W + GEX/VEX + operator chart)
- [ ] Prediction / process log v1.5 filled from real sessions
- [ ] 3+ co-pilot trades on Agentic (C) via MCP (user-confirmed each)
- [ ] A+C trades logged via `trader-memory-core` (IRA not required)
- [ ] `reports/portfolio/portfolio_review_*.md` for 2+ dates (A+C focus)
- [ ] Anthropic spend cap met; pre-commit clean

**Not exit criteria:** deep-research count, FPS staleness, IRA logging, FMP Premium S&P universe.

---

## Explicitly NOT in Phase 1

- Autonomous MCP order placement (Phase 3 gate)
- MCP trades on IRA or taxable
- IRA thesis logging / four-questions
- Upstream `skills/<name>/` rewrites except fixes in [decisions.md](../decisions.md)
- Prioritizing parked FMP/CI research debt over TA path

---

## References

- [trading-pipeline-checklist.md](trading-pipeline-checklist.md)
- [robinhood-mcp-integration.md](reference/robinhood-mcp-integration.md)
- [playbook.md](playbook.md)
- [PENDING_WORK.md](../PENDING_WORK.md)

---

## When ready to advance

Update `PROJECT.md` Active Phase to Phase 2. Read [phase-2-learning-loop.md](phase-2-learning-loop.md).
