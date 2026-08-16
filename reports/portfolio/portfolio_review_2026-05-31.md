# Portfolio Review — 2026-05-31

**Source:** Robinhood Agentic MCP via `scripts/robinhood_mcp.py` (read-only)
**Market context:** [exposure_posture_2026-05-31_204112.md](../market/exposure/exposure_posture_2026-05-31_204112.md) — REDUCE_ONLY, 50% ceiling, narrow participation

## Account summary

| Account (last 4) | thesis_store key | Type | Total value | Equity | Options | Cash | Buying power | MCP trade |
|------------------|------------------|------|-------------|--------|---------|------|--------------|-----------|
| ••••9309 | `robinhood_taxable` | individual (default) | $56.63 | $42.80 | $13.00 | $0.83 | $0.83 | **No** |
| ••••7016 | `robinhood_agentic` | individual Agentic | $50.00 | $0.00 | $0.00 | $50.00 | $50.00 | **Yes** (user confirm each) |
| ••••3854 | `ira_robinhood` | Roth IRA | $170.15 | $0.00 | $170.00 | $0.15 | $0.15 | **No** |

Pending deposits (taxable): $5.00.

## Positions by account

### robinhood_taxable (••••9309)

| Ticker | Qty | Avg cost | Est. cost | Est. value | thesis_id |
|--------|-----|----------|-----------|------------|-----------|
| MSFW | 1.321090 | $31.30 | $41.35 | ~$42.80 | `th_msfw_grw_20260531_150c` |

**Options (~$13)** — portfolio API residual; **not tracked** (user deferred — not a blocker).

### robinhood_agentic (••••7016)

No open positions. **$50.00 cash** — full buying power available.

### ira_robinhood (••••3854)

No equity positions in MCP snapshot. **~$170 options** per portfolio API. Positions below are from trader-memory-core (manual/screenshot ingest); reconcile against app.

| Ticker | Strategy | Strike | Expiry | Contracts | thesis_id |
|--------|----------|--------|--------|-----------|-----------|
| HOOD | long call | $90 | 2026-06-18 | 1 | `th_hood_rev_20260509_738d` |
| DIS | long call | $109 | 2026-06-18 | 10 | `th_dis_grw_20260528_cc15` |
| DIS | long call | $120 | 2026-07-17 | 20 | `th_dis_grw_20260528_5e21` |
| VECO | long call | $75 | 2026-07-17 | 1 | `th_veco_grw_20260509_24d0` |
| NOK | long call | $25 | 2026-09-18 | 5 | `th_nok_grw_20260528_b7cd` |

## Options — IRA eligibility (Portfolio B)

| Ticker | Strategy | Expiry | IRA-eligible |
|--------|----------|--------|--------------|
| HOOD | long call | 2026-06-18 | **Yes** |
| DIS | long call | 2026-06-18 | **Yes** |
| DIS | long call | 2026-07-17 | **Yes** |
| VECO | long call | 2026-07-17 | **Yes** |
| NOK | long call | 2026-09-18 | **Yes** |

All logged IRA options are defined-risk long calls (permitted strategies).

## Untracked vs trader-memory-core

| Broker exposure | thesis_store | Action |
|-----------------|--------------|--------|
| MSFW (taxable equity) | `th_msfw_grw_20260531_150c` ACTIVE | **Tracked** |
| Taxable options (~$13) | Not tracked | **Deferred** — user chose not to pursue |
| IRA options (~$170) | 5 ACTIVE theses (HOOD, DIS×2, VECO, NOK) | **Tracked** — thesis backfills complete 2026-06-01 |

**Closed since last review (2026-05-28):** TE (taxable) — thesis `th_te_grw_20260529_034d` now CLOSED.

**Thesis store without broker equity match:** Expected — IRA/options positions are not returned by `get_equity_positions`.

## Notes

- **Concentration:** IRA is 100% options (~$170); taxable is MSFW + small options stub + minimal cash. Agentic is 100% cash.
- **Upcoming expiries:** HOOD and DIS ($109) both expire **2026-06-18** (~18 days). Review roll/exit plan before expiry week.
- **Review due soon (≤7 days):** MSFW, DIS (both), NOK — next_review_date 2026-06-07.
- **Posture gate:** REDUCE_ONLY / 50% ceiling — defer new Agentic entries unless user explicitly confirms a sized plan.
- **Co-pilot gate:** No MCP orders without explicit user **confirm** per trade.

## Next steps

1. ~~Confirm taxable ~$13 options~~ — deferred
2. Review HOOD + DIS ($109) roll/exit before 2026-06-18
3. Present Agentic trade plan only when user selects ticker + confirms sizing
