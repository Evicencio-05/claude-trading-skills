# CANSLIM Stock Screener Report - Phase 3 (Full CANSLIM)
**Generated:** 2026-05-31 13:44:24 UTC
**Phase:** 3.1 (7 components - FULL CANSLIM with multi-period RS) (Components: C, A, N, S, L, I, M)
**Stocks Analyzed:** 1
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
| 1 | HPE | 42.5 | Below Average | Market Leader | 99 |

---

## Top 1 CANSLIM Candidates

### 1. HPE - Hewlett Packard Enterprise Company
**Price:** $43.06 | **Market Cap:** $0.0B | **Sector:** Technology
**Composite Score:** 42.5/100 (Below Average)

#### Component Breakdown

| Component | Score | Details |
|-----------|-------|---------|
| 🅲 Current Earnings | 0/100 | EPS: -28.9%, Revenue: +19.1% |
| 🅰 Annual Growth | 0/100 | 3yr CAGR: None, unknown |
| 🅽 Newness | 60/100 | -3.4% from 52wk high  |
| 🅂 Supply/Demand | 60/100 | Up/Down Volume Ratio: 1.24  |
| 🅻 Leadership | 100/100 | 3m/6m/12m: +94.5%/+99.9%/+143.8% (rel +84.3%/+88.6%/+115.6%) | RS: 99 (Market Leader) |
| 🅸 Institutional | 0/100 | N/A holders, N/A ownership  |
| 🅼 Market Direction | 90/100 | Strong Uptrend |

#### Interpretation
**Rating:** Below Average - Fails one or more key thresholds

**Guidance:** Monitor, do not buy

**Weakest Component:** C (0/100)

---

---

## Summary Statistics
- **Total Stocks Screened:** 1
- **Exceptional (90+):** 0 stocks
- **Strong (80-89):** 0 stocks
- **Above Average (70-79):** 0 stocks
- **Average (60-69):** 0 stocks
- **Below Average (<60):** 1 stocks

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
