# CANSLIM Stock Screener Report - Phase 3 (Full CANSLIM)
**Generated:** 2026-05-31 08:13:21 UTC
**Phase:** 3.1 (7 components - FULL CANSLIM with multi-period RS) (Components: C, A, N, S, L, I, M)
**Stocks Analyzed:** 2
**Schema Version:** 3.1
**RS Benchmark:** ^GSPC

---

## Market Condition Summary
- **Trend:** strong_uptrend
- **M Score:** 90/100

---

## Summary Table

| # | Symbol | Score | Rating | RS Rating | RS % |
|---|--------|-------|--------|-----------|------|
| 1 | MU | 57.5 | Average | Market Leader | 99 |
| 2 | MRAM | 42.5 | Below Average | Market Leader | 99 |

---

## Top 2 CANSLIM Candidates

### 1. MU - Micron Technology, Inc.
**Price:** $971.00 | **Market Cap:** $0.0B | **Sector:** Technology
**Composite Score:** 57.5/100 (Average)

#### Component Breakdown

| Component | Score | Details |
|-----------|-------|---------|
| 🅲 Current Earnings | 100/100 | EPS: +762.7%, Revenue: +196.3% |
| 🅰 Annual Growth | 0/100 | 3yr CAGR: None, unknown |
| 🅽 Newness | 60/100 | -1.0% from 52wk high  |
| 🅂 Supply/Demand | 60/100 | Up/Down Volume Ratio: 1.03  |
| 🅻 Leadership | 100/100 | 3m/6m/12m: +135.3%/+321.7%/+903.1% (rel +125.2%/+310.4%/+874.9%) | RS: 99 (Market Leader) |
| 🅸 Institutional | 0/100 | N/A holders, N/A ownership  |
| 🅼 Market Direction | 90/100 | Strong Uptrend |

#### Interpretation
**Rating:** Average - Marginal CANSLIM candidate

**Guidance:** Watchlist only, consider 3-5% if high conviction

**Weakest Component:** A (0/100)

**Warnings:**
- ⚠️ Revenue growth significantly lags EPS growth - investigate earnings quality (potential buyback-driven)

---

### 2. MRAM - Everspin Technologies, Inc.
**Price:** $26.38 | **Market Cap:** $0.0B | **Sector:** Technology
**Composite Score:** 42.5/100 (Below Average)

#### Component Breakdown

| Component | Score | Details |
|-----------|-------|---------|
| 🅲 Current Earnings | 60/100 | EPS: +74.4%, Revenue: +13.2% |
| 🅰 Annual Growth | 0/100 | 3yr CAGR: None, unknown |
| 🅽 Newness | 20/100 | -48.8% from 52wk high  |
| 🅂 Supply/Demand | 40/100 | Up/Down Volume Ratio: 0.83  |
| 🅻 Leadership | 100/100 | 3m/6m/12m: +131.6%/+235.6%/+365.3% (rel +121.5%/+224.4%/+337.0%) | RS: 99 (Market Leader) |
| 🅸 Institutional | 0/100 | N/A holders, N/A ownership  |
| 🅼 Market Direction | 90/100 | Strong Uptrend |

#### Interpretation
**Rating:** Below Average - Fails one or more key thresholds

**Guidance:** Monitor, do not buy

**Weakest Component:** A (0/100)

**Warnings:**
- ⚠️ Revenue growth significantly lags EPS growth - investigate earnings quality (potential buyback-driven)

---

---

## Summary Statistics
- **Total Stocks Screened:** 2
- **Exceptional (90+):** 0 stocks
- **Strong (80-89):** 0 stocks
- **Above Average (70-79):** 0 stocks
- **Average (60-69):** 0 stocks
- **Below Average (<60):** 2 stocks

---

## Methodology

This Phase 3 implementation includes all 7 CANSLIM components (100% coverage):

- **C** (Current Earnings) - 15% weight: Quarterly EPS growth YoY
- **A** (Annual Growth) - 20% weight: 3-year EPS CAGR
- **N** (Newness) - 15% weight: Price position vs 52-week high
- **S** (Supply/Demand) - 15% weight: Volume accumulation/distribution
- **L** (Leadership) - 20% weight: Multi-period weighted Relative Strength (3m/6m/12m) vs configurable benchmark
- **I** (Institutional) - 10% weight: Institutional holder analysis
- **M** (Market Direction) - 5% weight: S&P 500 trend

Component weights follow William O'Neil's original CANSLIM methodology,
with L (Leadership/RS Rank) as the most weighted component alongside A (Annual Growth).

**Weighted RS Calculation (Phase 3.1):**

```
Weighted RS = 0.40 × rel_3m + 0.30 × rel_6m + 0.30 × rel_12m
(When some periods are missing, the weights are re-normalized over available periods.)
Default benchmark: ^GSPC. Override with --rs-benchmark SPY/QQQ/IWM/...
```

Fallback hierarchy when full multi-period data is not available:

1. **No benchmark** → score from weighted absolute stock performance with a 20% penalty (legacy fallback).
2. **Multi-period unavailable but >=50 bars of price history** → fall back to the legacy 365-day full-window absolute return as the scoring input. The 20% penalty still applies when no benchmark is present.
3. **<50 bars of price history** → score=0 with `error` set; no scoring is performed.

For detailed methodology, see `references/canslim_methodology.md`.

---

**Disclaimer:** This screener is for educational and informational purposes only. Not investment advice. Conduct your own research and consult a financial advisor before making investment decisions.
