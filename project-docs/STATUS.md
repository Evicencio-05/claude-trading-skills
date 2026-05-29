# Project Status

**Last updated:** 2026-05-28
**Phase 1 housekeeping completed:** 2026-05-10

## Active Phase

Phase 1 — Audit & Activate
Phase started: 2026-05-07
Target exit: ~2026-06-04 (4 weeks)

## This Week's Focus

- [ ] Upgrade FMP to Starter tier (approved, not activated)
- [ ] Log IRA positions via thesis-manager (human input)
- [ ] Robinhood MCP account discovery in Claude Code (paste results to decisions.md)
- [ ] Refresh ACCOUNT_MAP if taxable login changed

## Open Blockers

| ID | Issue | Status |
|----|-------|--------|
| P1 | API keys unavailable in non-interactive shells | FIXED 2026-05-10 |
| P2 | exposure-coach schema mismatch | FIXED 2026-05-10; verified 2026-05-28 |
| P3 | vcp-screener blocked on free FMP tier | FMP Starter upgrade pending |
| P4 | economic-calendar-fetcher blocked (silent empty response) | Workaround: scripts/fred_calendar.py |

## Monthly Spend

Current: $0 | Cap: $30/mo

## Key Decisions Pending

- FMP Starter ($29/mo) upgrade — approved, not yet activated
- Alpaca paper account setup — approved, not yet done
- Robinhood Agentic MCP: which accounts exposed (human discovery in Claude Code)

## Infrastructure (2026-05-28)

- [x] Cursor harness: `.cursor/rules/`, `.cursor/skills/`, AGENTS.md
- [x] PENDING_WORK.md task queue at repo root
- [x] pre_market systemd timer installed (`~/.config/systemd/user/`)
- [x] robinhood-sync systemd timer installed and enabled
- [x] exposure-coach verified with latest pre_market JSON (breadth=42, uptrend=54)
- [x] thesis-manager: compiles and Streamlit starts cleanly

## Open Blockers / Action Items

- [ ] Fill ACCOUNT_MAP in scripts/robinhood_sync.py if login/account IDs changed
- [ ] Complete Robinhood MCP account list → decisions.md
- [ ] First successful scheduled robinhood_sync after 2FA

## Phase 1 Exit Criteria Progress

- [x] skills_audit.md with dual ratings for all Tier 1-2 skills
- [x] At least 8 Tier 1 skills audited and rated
- [ ] 10+ trades logged across at least 2 different trade types
- [x] 10+ days of daily market context saved (13 rows in posture_history.log)
- [x] /deep-research run on at least 3 real tickers (MRAM, MU, P, VECO, INO, FPS, …)
- [x] At least one Lucid eval account opened and one trade taken
- [ ] Total Anthropic spend < $20
- [ ] Pre-commit hooks pass cleanly

## Recent Changes

- Handoff execution: PENDING_WORK.md, robinhood-sync systemd units, doc sync
- pre_market.py: 13+ daily posture log entries (May 14–28)
- Portfolio sizes updated: A ~$250, B ~$10K IRA, C ~$50 Agentic
- robinhood_sync.py: Portfolio A taxable only; B manual; C via MCP when available
