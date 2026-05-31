# FMP Starter Verification Report

**Date:** 2026-05-31
**Tier:** Starter ($29.99/mo, 750 calls/day)
**Key:** Present in repo-root `.env` (not logged here)

## Endpoint matrix

| Endpoint | HTTP | Starter | Notes |
|----------|------|---------|-------|
| `stable/quote` (single symbol) | 200 | Yes | AAPL, MRAM, IBM, MU, P return prices |
| `stable/quote` (comma batch) | 200 | Broken shape | Returns `[]` — use per-symbol requests |
| `stable/historical-price-eod/full` | 200 | Yes | Used by market-top-detector |
| `stable/earnings-calendar` | 200 | Yes | 197 items (2-day window) |
| `stable/economic-calendar` | 200 | Yes | 581 items (7-day window) |
| `stable/profile` | 200 | Yes | CANSLIM sector/industry data |
| `stable/income-statement` | 200 | Yes | Quarterly/annual financials |
| `stable/sp500-constituent` | 402 | No | Requires **Professional ($79/mo)** |
| `api/v3/*` (legacy) | 403 | No | Blocked for new subscribers (post Aug 2025) |

## Workflow status (post-fix 2026-05-31)

| Workflow | Status |
|----------|--------|
| `market-top-detector` | Pass |
| `fred_calendar.py` | Pass |
| `update_stale_research --prefetch` quote | Pass |
| `vcp-screener --universe` | Pass (3 quotes MRAM/MU/P; 11 quotes watchlist) |
| `canslim-screener --universe` | Pass (MRAM/MU analyzed) |
| `earnings-trade-analyzer` | Pass (stable earnings-calendar; profiles via stable) |
| `vcp-screener` default S&P 500 | Blocked on Starter — use `--universe` or Professional tier |

## Re-verify

```bash
uv run python3 scripts/fmp_verify_starter.py
```
