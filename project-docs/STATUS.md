# Project Status

**Last updated:** 2026-05-10
**Phase 1 housekeeping completed:** 2026-05-10

## Active Phase

Phase 1 — Audit & Activate
Phase started: 2026-05-07
Target exit: ~2026-06-04 (4 weeks)

## This Week's Focus

- [ ] Complete audit of remaining skills
- [ ] Set up Alpaca paper account
- [ ] Upgrade FMP to Starter tier
- [ ] First run of robinhood_sync.py (manual 2FA required)
      Fill ACCOUNT_MAP with your account IDs after first run
- [ ] Run /log-positions to add thesis to synced positions

## Open Blockers

| ID | Issue | Status |
|----|-------|--------|
| P1 | API keys unavailable in non-interactive shells | FIXED 2026-05-10 |
| P2 | exposure-coach schema mismatch | FIXED 2026-05-10 |
| P3 | vcp-screener blocked on free FMP tier | FMP Starter upgrade pending |
| P4 | economic-calendar-fetcher blocked (silent empty response) | Workaround: scripts/fred_calendar.py |

## Monthly Spend

Current: $0 | Cap: $30/mo

## Key Decisions Pending

- FMP Starter ($29/mo) upgrade — approved, not yet activated
- Alpaca paper account setup — approved, not yet done

## Open Blockers / Action Items

- [ ] Run: uv run scripts/pre_market.py --dry-run to verify
      output writes to reports/pre_market/ and reports/logs/
- [ ] Create robinhood-sync.service + robinhood-sync.timer
      (same pattern as pre-market systemd files)
- [ ] Fill ACCOUNT_MAP in scripts/robinhood_sync.py with
      account URL from first --dry-run output

## Phase 1 Exit Criteria Progress

- [x] skills_audit.md with dual ratings for all Tier 1-2 skills
- [x] At least 8 Tier 1 skills audited and rated
- [ ] 10+ trades logged across at least 2 different trade types
- [ ] 10+ days of daily market context saved
- [ ] /deep-research run on at least 3 real tickers
- [x] At least one Lucid eval account opened and one trade taken
- [ ] Total Anthropic spend < $20
- [ ] Pre-commit hooks pass cleanly

## Recent Changes

- pre_market.py outputs skill files to reports/pre_market/
  and posture/history logs to reports/logs/
- Scheduler is systemd (Arch Linux), not launchd (macOS)
- robinhood_sync.py confirmed: Portfolio A (taxable) only.
  Portfolio B (IRA) not reachable via unofficial API — manual
  logging via /log-positions
