# Project Status

**Last updated:** 2026-05-28
**Active phase:** Phase 1B — Robinhood Research + Co-Pilot Trading
**Phase doc:** [phase-1b-robinhood-research.md](phase-1b-robinhood-research.md)
**Reprioritization:** [decisions.md](../decisions.md) [2026-05-28] — futures Phase 2 deferred

## This Week's Focus

- [ ] **Activate FMP Starter ($29/mo)** — approved verbally; enables batch vcp/canslim/earnings screeners
- [ ] **Weekly research cadence** — `commands/review-portfolio.md` (FPS stale &gt;14d); next full deep-research candidate: FPS
- [ ] **Robinhood co-pilot** — portfolio review + `ingest-pending` + `log-positions` for TE (taxable); first Agentic trade after user confirm
- [ ] **IRA thesis logging** — MCP read + four questions for open IRA positions
- [ ] **Close expired theses** — POWL, TSLA, PENG per PENDING_WORK

## Open Blockers

| ID | Issue | Status |
|----|-------|--------|
| P1 | API keys in non-interactive shells | FIXED 2026-05-10 |
| P2 | exposure-coach schema mismatch | FIXED 2026-05-10 |
| P3 | vcp-screener on free FMP (batch/ETFs) | **Partial** — single-ticker universe works; FMP Starter for full S&P500 pipeline |
| P4 | economic-calendar-fetcher | Workaround: `scripts/fred_calendar.py` |

## Monthly Spend

Current: $0 | Cap: $30/mo | FMP Starter pending activation

## Robinhood MCP (verified 2026-05-28)

```bash
uv run python3 scripts/robinhood_mcp.py accounts      # OK
uv run python3 scripts/robinhood_mcp.py positions --all  # OK (TE taxable)
```

Account map: [config/robinhood_accounts.yaml](../config/robinhood_accounts.yaml) | [decisions.md](../decisions.md)

## Infrastructure

- [x] `pre-market.timer` active (next trigger weekdays 8 AM ET)
- [x] `robinhood-sync.timer` enabled
- [x] MCP hybrid CLI + Cursor URL
- [x] Phase 1 audit complete (Tier 1–2)

## Phase 1B Exit Criteria Progress

| Criterion | Status |
|-----------|--------|
| FMP Starter + vcp on watchlist | Partial — vcp ran on MRAM; Starter not billed yet |
| 14 days pre_market + posture log | In progress (13+ days in posture_history) |
| 5+ deep/update on watchlist | In progress (MRAM/MU/P May 27; FPS stale May 13) |
| 10+ trades logged, ≥2 types | ❌ ~1–2 effective; many theses pre-1B |
| 3+ Agentic co-pilot MCP trades | ❌ 0 — awaiting user confirm |
| IRA logged via MCP | ❌ |
| 2+ portfolio_review reports | 1 started 2026-05-28 |
| Phase 1: Anthropic &lt;$20, pre-commit | Open |

## Phase 1 Exit (carryover)

- [x] skills_audit.md Tier 1–2
- [x] 8+ Tier 1 skills rated
- [ ] 10+ trades logged (≥2 types)
- [x] 10+ days market context
- [x] 3+ deep-research tickers
- [x] Lucid eval + one trade
- [ ] Anthropic spend &lt; $20
- [ ] Pre-commit clean

## Recent Changes

- Phase 1B kickoff: roadmap reprioritized; futures Phase 2 deferred
- `phase-1b-robinhood-research.md` created
- Pre-market run 2026-05-28: breadth 42.4, posture CAUTIOUS 50%
