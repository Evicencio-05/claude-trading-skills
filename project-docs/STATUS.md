# Project Status

**Last updated:** 2026-05-29
**Active phase:** Phase 1 — Research + Co-Pilot Trading
**Phase doc:** [phase-1-research-copilot.md](phase-1-research-copilot.md)
**Roadmap:** Equity-only — [decisions.md](../decisions.md) [2026-05-29]

## This Week's Focus

- [ ] **Activate FMP Starter ($29/mo)** — approved verbally; enables batch vcp/canslim/earnings screeners
- [ ] **Update research — stale watchlist** — FPS, INO, VECO (&gt;14d); `commands/review-portfolio.md` weekly
- [ ] **Robinhood co-pilot** — `ingest-pending` + `log-positions` for TE (taxable); first Agentic trade after user confirm
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
- [ ] `robinhood-sync.timer` — **inactive** (not enabled in user systemd; install per [launchd/README.md](../launchd/README.md))
- [x] MCP hybrid CLI + Cursor URL
- [x] Phase 1 audit complete (Tier 1–2) — see [archive/phase-1-audit.md](archive/phase-1-audit.md)

## Phase 1 Exit Criteria Progress

| Criterion | Status |
|-----------|--------|
| FMP Starter + vcp on watchlist | Partial — vcp ran on MRAM; Starter not billed yet |
| 14 days pre_market + posture log | **11/14** unique days (`reports/logs/posture_history.log`) |
| 5+ deep/update on watchlist | 6 tickers total; **3 current** (MRAM/MU/P 2026-05-27); **3 stale** (FPS, INO, VECO) |
| 10+ trades logged, ≥2 types | ❌ ~1–2 effective; 16 theses pre-Phase 1 legacy |
| 3+ Agentic co-pilot MCP trades | ❌ 0 — awaiting user confirm |
| IRA logged via MCP | ❌ |
| 2+ portfolio_review reports | **1/2** — `portfolio_review_2026-05-28.md` |
| Anthropic &lt;$20, pre-commit | Open |

## Recent Changes

- Futures scope removed; 3-phase equity roadmap ([decisions.md](../decisions.md) 2026-05-29)
- `phase-1-research-copilot.md`, `phase-2-learning-loop.md`, `phase-3-agentic-execution.md` created
- Superseded docs archived under `project-docs/archive/`
- Pre-market run 2026-05-28: breadth 42.4, posture CAUTIOUS 50%
