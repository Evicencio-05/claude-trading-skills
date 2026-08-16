# Uptrend Analyzer Report

**Generated:** 2026-07-27 06:24:06
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **21.1/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Lower |
| **Zone Proximity** | **Near boundary: +1.1 points from 20 (above)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -10 (raw: 31.1/100) |
| **Active Warnings** | 3: LATE CYCLE WARNING, HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (44/100) |
| **Weakest Component** | Sector Rotation (28/100) |
| **Data Quality** | Complete (5/5 components) |
| **Confidence** | High (moderate, Both regime coverage) |

> **Guidance:** Weak breadth environment. Prioritize capital preservation over gains.

---

## Active Warnings

### LATE CYCLE WARNING
> Commodity sectors leading both cyclical and defensive groups. Historically associated with late-cycle inflation or sector rotation preceding broader market weakness.

- Favor lower end of exposure range (e.g. 80% if guidance is 80-100%)
- New entries limited to A-grade setups only
- Tighten stops on commodity/cyclical positions
- Monitor for commodity rollover as potential broad market lead indicator

### HIGH SELECTIVITY WARNING
> Wide spread between strongest and weakest sectors indicates highly selective market. Breadth may be masking narrowing leadership.

- Concentrate on sectors with ratio above 10MA
- Avoid lagging sectors even if trend is nominally 'up'
- Reduce position count to highest-conviction ideas

### SECTOR DIVERGENCE WARNING
> Significant divergence detected within sector groups. Some sectors within the same group are moving in opposite directions, suggesting hidden risk beneath the averages.

- Verify individual sector trends before entering positions
- Avoid sectors diverging from their group majority
- Monitor for group convergence or further deterioration

---

## Current Market Snapshot

| Metric | Value |
|--------|-------|
| Uptrend Ratio | 22.4% |
| 10-Day MA | 23.9% |
| Trend | down |
| Slope | -0.0044 |
| Distance from 37% (Overbought) | -14.6pp |
| Distance from 9.7% (Oversold) | +12.7pp |
| Date | 2026-07-24 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 29 | 8.7 | VERY WEAK: 22.4% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | █░░░ 29 | 7.2 | NARROW: 4/11 sectors uptrending, spread 50.8% |
| 3 | **Sector Rotation** | 15% | █░░░ 28 | 4.2 | DEFENSIVE TILT: Defensive leads by 5.5pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | █░░░ 33 | 6.6 | WEAK MOMENTUM: slope=-0.0045, strong decelerating |
| 5 | **Historical Context** | 10% | ██░░ 44 | 4.4 | NEAR MEDIAN: 22.4% at 44.5th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 22.4%
- **10-Day MA:** 23.9%
- **Trend:** down
- **Slope:** -0.0044
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 4/11
- **Count Score:** 40/100
- **Spread:** 50.8% (score: 13/100)
- **Overbought (>37%):** 2 sectors (Energy, Real Estate)
- **Oversold (<9.7%):** 1 sectors (Technology)

### 3. Sector Rotation

- **Cyclical Avg:** 16.5%
- **Defensive Avg:** 22.0%
- **Commodity Avg:** 39.9%
- **Cyclical-Defensive Gap:** -5.5pp
- **Late Cycle Warning:** YES (commodity penalty: -10)
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0644, spread=0.1675
    - Trend dissenter: Industrials (up vs majority down)
  - **Defensive Divergence:** std=0.1069, spread=0.259
    - Outlier: Real Estate (deviation: +0.1625)
    - Trend dissenter: Real Estate (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 8.6% | Down | -0.0117 |
| Consumer Cyclical | 16.7% | Down | -0.0020 |
| Communication Services | 10.3% | Down | -0.0129 |
| Financial | 25.4% | Down | -0.0080 |
| Industrials | 21.8% | Up | +0.0041 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 12.5% | Down | -0.0035 |
| Consumer Defensive | 12.4% | Down | -0.0120 |
| Healthcare | 25.0% | Down | -0.0225 |
| Real Estate | 38.3% | Up | +0.0133 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 59.4% | Up | +0.0318 |
| Basic Materials | 20.4% | Up | +0.0102 |


### 4. Momentum

- **Raw Slope:** -0.0044
- **Smoothed Slope (EMA(3)):** -0.0045 (score: 46/100)
- **Acceleration (10v10):** -0.005603 (strong_decelerating, score: 10/100)
- **Sector Slope Breadth:** 4/11 positive (score: 36/100)

### 5. Historical Context

- **Current Ratio:** 22.4%
- **Percentile Rank:** 44.5th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.8%
- **30-Day Avg:** 26.7%
- **90-Day Avg:** 24.1%
- **Data Points:** 765 (2023-08-11 to 2026-07-24)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 59.4% | 95/160 | 42.6% | Up | +0.0318 | Overbought |
| 2 | Real Estate | 38.3% | 54/141 | 33.8% | Up | +0.0133 | Overbought |
| 3 | Financial | 25.4% | 154/607 | 28.9% | Down | -0.0080 | Normal |
| 4 | Healthcare | 25.0% | 104/416 | 33.4% | Down | -0.0225 | Normal |
| 5 | Industrials | 21.8% | 85/390 | 19.0% | Up | +0.0041 | Normal |
| 6 | Basic Materials | 20.4% | 30/147 | 13.8% | Up | +0.0102 | Normal |
| 7 | Consumer Cyclical | 16.7% | 46/276 | 18.1% | Down | -0.0020 | Normal |
| 8 | Utilities | 12.5% | 10/80 | 14.4% | Down | -0.0035 | Normal |
| 9 | Consumer Defensive | 12.4% | 15/121 | 15.8% | Down | -0.0120 | Normal |
| 10 | Communication Services | 10.3% | 11/107 | 19.3% | Down | -0.0129 | Normal |
| 11 | Technology | 8.6% | 35/406 | 13.3% | Down | -0.0117 | Oversold |

---

## Recommended Actions

**Zone:** Cautious (Cautious-Lower)
**Exposure Guidance:** Defensive (30-60%)

- Significant cash allocation (40-70%)
- Only hold strongest leaders in uptrending sectors
- Tight stops on all positions
- Consider defensive sector allocation
- No new aggressive entries

---

## Methodology

This analysis uses Monty's Uptrend Ratio Dashboard data to assess market breadth health.
The dashboard tracks ~2,800 US stocks across 11 sectors, measuring the percentage in uptrends.

**5-Component Scoring System (0-100, higher = healthier):**

1. **Market Breadth (30%):** Overall uptrend ratio level and trend direction
2. **Sector Participation (25%):** Number of uptrending sectors and spread uniformity
3. **Sector Rotation (15%):** Cyclical vs Defensive vs Commodity balance
4. **Momentum (20%):** Slope direction, acceleration, and sector slope breadth
5. **Historical Context (10%):** Percentile rank in historical distribution

**Key Thresholds (Monty's Dashboard):** Overbought = 37%, Oversold = 9.7%

For detailed methodology, see `references/uptrend_methodology.md`.

---

**Disclaimer:** This analysis is for educational and informational purposes only. Not investment advice. Past patterns may not predict future outcomes. Conduct your own research and consult a financial advisor before making investment decisions.
