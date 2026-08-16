# Project Status

**Last updated:** 2026-08-16
**Active phase:** Phase 1 — TA Confluence + Co-Pilot Trading
**Phase doc:** [phase-1-research-copilot.md](phase-1-research-copilot.md)
**Operator cadence:** [trading-pipeline-checklist.md](trading-pipeline-checklist.md)
**Roadmap:** Equity TA-first — [decisions.md](../decisions.md) [2026-08-16]

## This Week's Focus

- [x] **TA-first source foundations** — `tradewhisperer-charts`, `gex-vex-maps`, `operator-charts`
- [x] **All three input contracts filled** — TW charts/lists · Skylit GEX/VEX · operator S/R+fib+VP+SMA
- [x] **Fusion workflow** — `ta-confluence` (candle_first / map_first + judgment)
- [x] **Agentic co-pilot command** — `agentic-copilot-trade` + `config/agentic_copilot.yaml.example`
- [x] **Charter rewrite** — TA-first product + Phase 2 learning loop reframed (2026-08-16)
- [ ] Habit: confluence sessions when TW lists + maps + operator charts available
- [ ] Seed playbook TA setups + charting coach notes from live sessions
- [ ] **First Agentic trade filled** — user must reply **confirm** on presented plan (workflow ready)
- [ ] Deep-research only on PLAY / verge (not default)

## Open Blockers

| ID | Issue | Status |
|----|-------|--------|
| P1 | API keys in non-interactive shells | FIXED 2026-05-10 |
| P2 | exposure-coach schema mismatch | FIXED 2026-05-10 |
| P3 | vcp-screener watchlist universe | **Fixed** — use `--universe`; full S&P 500 needs FMP Premium ($69/mo) |
| P4 | economic-calendar-fetcher | Workaround: `scripts/fred_calendar.py` |

## Monthly Spend

Current: ~$29/mo (FMP Starter) | Cap: $30/mo | Premium ($69/mo) not approved

## Robinhood MCP (verified 2026-05-30)

```bash
uv run python3 scripts/robinhood_mcp.py accounts      # OK (3 accounts)
uv run python3 scripts/robinhood_mcp.py positions --all  # OK
```

Account map: [config/robinhood_accounts.yaml](../config/robinhood_accounts.yaml) | [decisions.md](../decisions.md)

## Infrastructure

- [x] `pre-market.timer` active (next trigger weekdays 8 AM ET)
- [ ] `robinhood-sync.timer` — **inactive** (not enabled in user systemd; install per [launchd/README.md](../launchd/README.md))
- [x] MCP hybrid CLI + Cursor URL
- [x] Phase 1 audit complete (Tier 1–2) — see [archive/phase-1-audit.md](archive/phase-1-audit.md)
- [x] Operator checklist — [trading-pipeline-checklist.md](trading-pipeline-checklist.md) (daily / weekly / per-trade)
- [x] TA-first charter + Phase 2 rewrite — 2026-08-16

## Phase 1 Exit Criteria Progress

| Criterion | Status |
|-----------|--------|
| TA intakes + `ta-confluence` | **Done** — 2026-08-09 |
| FMP Starter + optional watchlist tools | **Done** — 2026-05-31 (backup, not primary KPI) |
| 14 days pre_market + posture log | **12/14** unique days (`reports/logs/posture_history.log`) |
| Regular three-source confluence habit | In progress — lists through 2026-08-14 on disk |
| 10+ trades logged, ≥2 types | ❌ 17 theses total (10 ACTIVE legacy + TE); not 10+ effective Phase 1 trades |
| 3+ Agentic co-pilot MCP trades | **0/3 filled** — `/agentic-copilot-trade` ready; awaiting user confirm |
| IRA logged via MCP | ❌ |
| 2+ portfolio_review reports | **1/2** — `portfolio_review_2026-05-28.md` |
| Deep-research gated (PLAY/verge/ask) | Charter rule live 2026-08-16 — enforce in sessions |
| Anthropic &lt;$20, pre-commit | Open |

## Recent Changes

- Charter + Phase 2 rewritten TA-first (pattern → playbook → postmortem) — 2026-08-16
- TA-first intakes + `ta-confluence` + `agentic-copilot-trade` (2026-08-09)
- TW list intakes + overlap through 2026-08-14
- `report_paths` same-day discovery for ticker-stem chart filenames (2026-08-09)
- FMP Starter verified + stable API fmp_client fixes (2026-05-31)
- Docs synced to evidence 2026-05-30 ([docs_sync_2026-05-30.md](../reports/meta/docs_sync_2026-05-30.md))
- Futures scope removed; 3-phase equity roadmap ([decisions.md](../decisions.md) 2026-05-29)
