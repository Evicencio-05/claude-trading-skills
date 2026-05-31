# Project Status

**Last updated:** 2026-05-31
**Active phase:** Phase 1 — Research + Co-Pilot Trading
**Phase doc:** [phase-1-research-copilot.md](phase-1-research-copilot.md)
**Operator cadence:** [trading-pipeline-checklist.md](trading-pipeline-checklist.md)
**Roadmap:** Equity-only — [decisions.md](../decisions.md) [2026-05-29]

## This Week's Focus

- [x] **FMP Starter ($29/mo)** — active 2026-05-31; stable API fixes applied ([verification report](../reports/meta/fmp_starter_verification_2026-05-31.md))
- [ ] **Update research — stale watchlist** — FPS (&gt;14d); `commands/review-portfolio.md` weekly
- [ ] **First Agentic trade** — user must reply **confirm** on presented plan
- [ ] **IRA thesis logging** — MCP read + four questions for open IRA positions
- [ ] **Close expired theses** — TSLA, PENG per PENDING_WORK

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

## Phase 1 Exit Criteria Progress

| Criterion | Status |
|-----------|--------|
| FMP Starter + vcp on watchlist | **Done** — 11-quote watchlist pass 2026-05-31 ([decisions.md](../decisions.md) [2026-05-31]) |
| 14 days pre_market + posture log | **12/14** unique days (`reports/logs/posture_history.log`) |
| 5+ deep/update on watchlist | HOOD/IBM/TSM/VECO @ 2026-05-31; MRAM/MU/P @ 2026-05-27; **FPS stale** |
| 10+ trades logged, ≥2 types | ❌ 17 theses total (10 ACTIVE legacy + TE); not 10+ effective Phase 1 trades |
| 3+ Agentic co-pilot MCP trades | ❌ 0 — awaiting user confirm |
| IRA logged via MCP | ❌ |
| 2+ portfolio_review reports | **1/2** — `portfolio_review_2026-05-28.md` |
| Anthropic &lt;$20, pre-commit | Open |

## Recent Changes

- FMP Starter verified + stable API fmp_client fixes (2026-05-31)
- Docs synced to evidence 2026-05-30 ([docs_sync_2026-05-30.md](../reports/meta/docs_sync_2026-05-30.md))
- TE thesis logged (`th_te_grw_20260529_034d`); POWL closed 2026-05-29
- Pre-market run 2026-05-29: breadth 42.4, posture CAUTIOUS 50%
- Trading pipeline checklist consolidated — [trading-pipeline-checklist.md](trading-pipeline-checklist.md)
- Futures scope removed; 3-phase equity roadmap ([decisions.md](../decisions.md) 2026-05-29)
