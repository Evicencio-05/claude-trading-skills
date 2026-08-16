# CANSLIM Stock Screener Report - Phase 3 (Full CANSLIM)
**Generated:** 2026-05-31 14:31:04 UTC
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
| 1 | GOOGL | 66.7 | Above Average | Market Leader | 95 |
| 2 | ASTS | 39.5 | Weak | Market Leader | 99 |

---

## Top 2 CANSLIM Candidates

### 1. GOOGL - Alphabet Inc. ✓
**Price:** $380.34 | **Market Cap:** $0.0B | **Sector:** Communication Services
**Composite Score:** 66.7/100 (Above Average)

#### Component Breakdown

| Component | Score | Details |
|-----------|-------|---------|
| 🅲 Current Earnings | 80/100 | EPS: +82.0%, Revenue: +21.8% |
| 🅰 Annual Growth | 66/100 | 3yr CAGR: 33.5%, stable |
| 🅽 Newness | 60/100 | -6.9% from 52wk high  |
| 🅂 Supply/Demand | 60/100 | Up/Down Volume Ratio: 1.05  |
| 🅻 Leadership | 95/100 | 3m/6m/12m: +24.1%/+18.9%/+121.3% (rel +13.9%/+7.6%/+93.1%) | RS: 95 (Market Leader) |
| 🅸 Institutional | 0/100 | N/A holders, N/A ownership  |
| 🅼 Market Direction | 90/100 | Strong Uptrend |

#### Interpretation
**Rating:** Above Average - Meets thresholds, one component weak

**Guidance:** Buy on pullback, conservative sizing (5-8% of portfolio)

**Weakest Component:** I (0/100)

**Warnings:**
- ⚠️ Revenue growth significantly lags EPS growth - investigate earnings quality (potential buyback-driven)
- ⚠️ Revenue CAGR significantly lags EPS CAGR - growth may be buyback-driven rather than organic

---

### 2. ASTS - AST SpaceMobile, Inc.
**Price:** $113.41 | **Market Cap:** $0.0B | **Sector:** Technology
**Composite Score:** 39.5/100 (Weak)

#### Component Breakdown

| Component | Score | Details |
|-----------|-------|---------|
| 🅲 Current Earnings | 0/100 | EPS: -230.0%, Revenue: +1952.2% |
| 🅰 Annual Growth | 0/100 | 3yr CAGR: None, unknown |
| 🅽 Newness | 40/100 | -15.3% from 52wk high  |
| 🅂 Supply/Demand | 60/100 | Up/Down Volume Ratio: 1.10  |
| 🅻 Leadership | 100/100 | 3m/6m/12m: +30.5%/+104.3%/+381.2% (rel +20.3%/+93.0%/+352.9%) | RS: 99 (Market Leader) |
| 🅸 Institutional | 0/100 | N/A holders, N/A ownership  |
| 🅼 Market Direction | 90/100 | Strong Uptrend |

#### Interpretation
**Rating:** Weak - Does not meet CANSLIM criteria

**Guidance:** Avoid

**Weakest Component:** C (0/100)

---

---

## Summary Statistics
- **Total Stocks Screened:** 2
- **Exceptional (90+):** 0 stocks
- **Strong (80-89):** 0 stocks
- **Above Average (70-79):** 0 stocks
- **Average (60-69):** 1 stocks
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
