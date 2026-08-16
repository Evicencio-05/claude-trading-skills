# CANSLIM Stock Screener Report - Phase 3 (Full CANSLIM)
**Generated:** 2026-05-31 18:24:48 UTC
**Phase:** 3.1 (7 components - FULL CANSLIM with multi-period RS) (Components: C, A, N, S, L, I, M)
**Stocks Analyzed:** 3
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
| 1 | META | 49.9 | Below Average | Laggard | 25 |
| 2 | DOCN | 42.5 | Below Average | Market Leader | 99 |
| 3 | GFS | 39.5 | Weak | Market Leader | 99 |

---

## Top 3 CANSLIM Candidates

### 1. META - Meta Platforms, Inc.
**Price:** $632.51 | **Market Cap:** $0.0B | **Sector:** Communication Services
**Composite Score:** 49.9/100 (Below Average)

#### Component Breakdown

| Component | Score | Details |
|-----------|-------|---------|
| 🅲 Current Earnings | 100/100 | EPS: +60.4%, Revenue: +33.1% |
| 🅰 Annual Growth | 72/100 | 3yr CAGR: 40.6%, erratic |
| 🅽 Newness | 40/100 | -20.6% from 52wk high  |
| 🅂 Supply/Demand | 40/100 | Up/Down Volume Ratio: 0.90  |
| 🅻 Leadership | 20/100 | 3m/6m/12m: -3.2%/-0.2%/-1.9% (rel -13.4%/-11.4%/-30.1%) | RS: 25 (Laggard) |
| 🅸 Institutional | 0/100 | N/A holders, N/A ownership  |
| 🅼 Market Direction | 90/100 | Strong Uptrend |

#### Interpretation
**Rating:** Below Average - Fails one or more key thresholds

**Guidance:** Monitor, do not buy

**Weakest Component:** I (0/100)

**Warnings:**
- ⚠️ Revenue CAGR significantly lags EPS CAGR - growth may be buyback-driven rather than organic

---

### 2. DOCN - DigitalOcean Holdings, Inc.
**Price:** $156.05 | **Market Cap:** $0.0B | **Sector:** Technology
**Composite Score:** 42.5/100 (Below Average)

#### Component Breakdown

| Component | Score | Details |
|-----------|-------|---------|
| 🅲 Current Earnings | 0/100 | EPS: -59.5%, Revenue: +22.4% |
| 🅰 Annual Growth | 0/100 | 3yr CAGR: None, unknown |
| 🅽 Newness | 60/100 | -6.0% from 52wk high  |
| 🅂 Supply/Demand | 60/100 | Up/Down Volume Ratio: 1.16  |
| 🅻 Leadership | 100/100 | 3m/6m/12m: +167.8%/+245.6%/+458.6% (rel +157.6%/+234.3%/+430.4%) | RS: 99 (Market Leader) |
| 🅸 Institutional | 0/100 | N/A holders, N/A ownership  |
| 🅼 Market Direction | 90/100 | Strong Uptrend |

#### Interpretation
**Rating:** Below Average - Fails one or more key thresholds

**Guidance:** Monitor, do not buy

**Weakest Component:** C (0/100)

---

### 3. GFS - GLOBALFOUNDRIES Inc.
**Price:** $79.97 | **Market Cap:** $0.0B | **Sector:** Technology
**Composite Score:** 39.5/100 (Weak)

#### Component Breakdown

| Component | Score | Details |
|-----------|-------|---------|
| 🅲 Current Earnings | 0/100 | EPS: -50.0%, Revenue: +3.1% |
| 🅰 Annual Growth | 0/100 | 3yr CAGR: None, unknown |
| 🅽 Newness | 60/100 | -13.6% from 52wk high  |
| 🅂 Supply/Demand | 40/100 | Up/Down Volume Ratio: 0.95  |
| 🅻 Leadership | 100/100 | 3m/6m/12m: +60.4%/+126.7%/+116.7% (rel +50.2%/+115.5%/+88.5%) | RS: 99 (Market Leader) |
| 🅸 Institutional | 0/100 | N/A holders, N/A ownership  |
| 🅼 Market Direction | 90/100 | Strong Uptrend |

#### Interpretation
**Rating:** Weak - Does not meet CANSLIM criteria

**Guidance:** Avoid

**Weakest Component:** C (0/100)

---

---

## Summary Statistics
- **Total Stocks Screened:** 3
- **Exceptional (90+):** 0 stocks
- **Strong (80-89):** 0 stocks
- **Above Average (70-79):** 0 stocks
- **Average (60-69):** 0 stocks
- **Below Average (<60):** 3 stocks

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
