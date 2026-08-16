# Project Status

**Last updated:** 2026-08-16
**Active phase:** Phase 1 — TA + Co-Pilot Trading
**Phase doc:** [phase-1-research-copilot.md](phase-1-research-copilot.md) (retitled TA + Co-pilot; filename kept for links)
**Operator cadence:** [trading-pipeline-checklist.md](trading-pipeline-checklist.md)
**Roadmap:** Equity-only — [decisions.md](../decisions.md) [2026-05-29]
**Account scope:** Portfolio **C** (Agentic) + **A** (taxable individual). Portfolio **B** (IRA) — no thesis logging.

## This Week's Focus

- [x] **TA-first source foundations** — `tradewhisperer-charts`, `gex-vex-maps`, `operator-charts`
- [x] **All three input contracts filled** — TW charts/lists · Skylit GEX/VEX · operator S/R+fib+VP+SMA
- [x] **Fusion workflow** — `ta-confluence` (candle_first / map_first + judgment)
- [x] **Agentic co-pilot command** — `agentic-copilot-trade` + `config/agentic_copilot.yaml.example`
- [x] **Charter align** — TA-first + A+C logging scope (IRA logging discontinued)
- [x] Prediction log v1.5 **template + seed** — [prediction_log_v15.md](../.cursor/skills/ta-confluence/references/prediction_log_v15.md) · `reports/charts/confluence/prediction_log_2026-08-16.*`
- [x] TA smoke inventory — [ta_smoke_inventory_2026-08-16.md](../reports/meta/ta_smoke_inventory_2026-08-16.md)
- [ ] **Same-day live TA smoke** — fresh D+W lists + GEX/VEX + operator (no stale TW)
- [ ] **First Agentic trade filled** — user must reply **confirm** on presented plan
- [ ] Deep-research news strip — **parked** (not Phase 1 exit)

## Open Blockers

| ID | Issue | Status |
|----|-------|--------|
| P1 | API keys in non-interactive shells | FIXED 2026-05-10 |
| P2 | exposure-coach schema mismatch | FIXED 2026-05-10 |
| P3 | vcp-screener watchlist universe | **Fixed** — use `--universe`; full S&P 500 needs FMP Premium ($69/mo) |
| P4 | economic-calendar-fetcher | Workaround: `scripts/fred_calendar.py` (parked vs TA path) |

## Monthly Spend

Current: ~$29/mo (FMP Starter) | Cap: $30/mo | Premium ($69/mo) not approved

## Robinhood MCP (verified 2026-05-30)

```bash
uv run python3 scripts/robinhood_mcp.py accounts      # OK (3 accounts)
uv run python3 scripts/robinhood_mcp.py positions --all  # OK
```

Account map: [config/robinhood_accounts.yaml](../config/robinhood_accounts.yaml) | [decisions.md](../decisions.md)

| Portfolio | thesis_store | In scope |
|-----------|--------------|----------|
| C Agentic | `robinhood_agentic` | Trade + log |
| A taxable | `robinhood_taxable` | Sync + log |
| B Roth IRA | `ira_robinhood` | Discover only — **do not log** |

## Infrastructure

- [x] `pre-market.timer` active (next trigger weekdays 8 AM ET)
- [ ] `robinhood-sync.timer` — **inactive** (enable for Portfolio A cadence per [launchd/README.md](../launchd/README.md))
- [x] MCP hybrid CLI + Cursor URL
- [x] Phase 1 audit complete (Tier 1–2) — see [archive/phase-1-audit.md](archive/phase-1-audit.md)
- [x] Operator checklist — [trading-pipeline-checklist.md](trading-pipeline-checklist.md) (daily / weekly / per-trade)

## Phase 1 Exit Criteria Progress (TA-shaped, A+C)

| Criterion | Status |
|-----------|--------|
| TA intakes + `ta-confluence` shipped | **Done** — 2026-08-09 |
| Live full-stack confluence sessions | **Partial** — inventory [ta_smoke_inventory_2026-08-16.md](../reports/meta/ta_smoke_inventory_2026-08-16.md); same-day no-stale smoke still open |
| Prediction / process log v1.5 | **Template + seed done** — fill outcomes after taken trades |
| 3+ Agentic (C) co-pilot MCP trades | **0/3 filled** — `/agentic-copilot-trade` ready; awaiting user confirm |
| A+C trades logged via `trader-memory-core` | Open — log C fills + A sync; **IRA not required** |
| 2+ portfolio_review reports (A+C focus) | **1/2** — `portfolio_review_2026-05-28.md` |
| `pre_market` posture cadence | **Context** — 12/14 unique days (`reports/logs/posture_history.log`); not the main product |
| Anthropic &lt;$20, pre-commit | Open |
| Deep-research / FPS / IRA logging | **Not exit-blocking** (parked / discontinued) |

### Parked engineering (not TA path)

FMP `institutional-flow` v3 403, nine `fmp_client` forks, CI↔`run_all_tests.sh` honesty, theme-detector/canslim skips — see [PENDING_WORK.md](../PENDING_WORK.md) § Parked research debt. Touch only if they block commits or Agentic.

## Recent Changes

- Charter → TA-first; IRA logging discontinued; A+C scope (2026-08-16)
- TA-first intakes + `ta-confluence` + `agentic-copilot-trade` (2026-08-09)
- `report_paths` same-day discovery for ticker-stem chart filenames (2026-08-09)
- FMP Starter verified + stable API fmp_client fixes (2026-05-31)
- Docs synced to evidence 2026-05-30 ([docs_sync_2026-05-30.md](../reports/meta/docs_sync_2026-05-30.md))
- TE thesis logged (`th_te_grw_20260529_034d`); POWL closed 2026-05-29
- Pre-market run 2026-05-29: breadth 42.4, posture CAUTIOUS 50%
- Trading pipeline checklist consolidated — [trading-pipeline-checklist.md](trading-pipeline-checklist.md)
- Futures scope removed; 3-phase equity roadmap ([decisions.md](../decisions.md) 2026-05-29)
