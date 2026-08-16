# Uptrend Analyzer Report

**Generated:** 2026-07-21 13:23:55
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **27.6/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Lower |
| **Zone Proximity** | **Near boundary: +7.6 points from 20 (above)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -7 (raw: 34.6/100) |
| **Active Warnings** | 2: LATE CYCLE WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (48/100) |
| **Weakest Component** | Market Breadth (Overall) (30/100) |
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

### SECTOR DIVERGENCE WARNING
> Significant divergence detected within sector groups. Some sectors within the same group are moving in opposite directions, suggesting hidden risk beneath the averages.

- Verify individual sector trends before entering positions
- Avoid sectors diverging from their group majority
- Monitor for group convergence or further deterioration

---

## Current Market Snapshot

| Metric | Value |
|--------|-------|
| Uptrend Ratio | 23.1% |
| 10-Day MA | 25.3% |
| Trend | down |
| Slope | -0.0067 |
| Distance from 37% (Overbought) | -13.9pp |
| Distance from 9.7% (Oversold) | +13.4pp |
| Date | 2026-07-20 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 30 | 9.0 | WEAK: 23.1% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | █░░░ 35 | 8.8 | NARROW: 3/11 sectors uptrending, spread 35.6% |
| 3 | **Sector Rotation** | 15% | █░░░ 39 | 5.8 | DEFENSIVE TILT: Defensive leads by 3.4pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | █░░░ 31 | 6.2 | WEAK MOMENTUM: slope=-0.0049, strong decelerating |
| 5 | **Historical Context** | 10% | ██░░ 48 | 4.8 | NEAR MEDIAN: 23.1% at 47.6th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 23.1%
- **10-Day MA:** 25.3%
- **Trend:** down
- **Slope:** -0.0067
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 3/11
- **Count Score:** 20/100
- **Spread:** 35.6% (score: 58/100)
- **Overbought (>37%):** 2 sectors (Energy, Real Estate)
- **Oversold (<9.7%):** 1 sectors (Basic Materials)

### 3. Sector Rotation

- **Cyclical Avg:** 20.1%
- **Defensive Avg:** 23.4%
- **Commodity Avg:** 27.4%
- **Cyclical-Defensive Gap:** -3.4pp
- **Late Cycle Warning:** YES (commodity penalty: -5)
- **Divergence Warning:** YES (penalty: -5)
  - **Defensive Divergence:** std=0.0961, spread=0.2357
    - Trend dissenter: Consumer Defensive (down vs majority up)
    - Trend dissenter: Healthcare (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 14.3% | Down | -0.0037 |
| Consumer Cyclical | 18.7% | Down | -0.0035 |
| Communication Services | 20.9% | Down | -0.0054 |
| Financial | 29.3% | Down | -0.0083 |
| Industrials | 17.1% | Down | -0.0121 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 13.8% | Up | +0.0026 |
| Consumer Defensive | 15.3% | Down | -0.0089 |
| Healthcare | 27.4% | Down | -0.0238 |
| Real Estate | 37.3% | Up | +0.0049 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 45.2% | Up | +0.0311 |
| Basic Materials | 9.6% | Down | -0.0058 |


### 4. Momentum

- **Raw Slope:** -0.0067
- **Smoothed Slope (EMA(3)):** -0.0049 (score: 45/100)
- **Acceleration (10v10):** -0.007088 (strong_decelerating, score: 10/100)
- **Sector Slope Breadth:** 3/11 positive (score: 27/100)

### 5. Historical Context

- **Current Ratio:** 23.1%
- **Percentile Rank:** 47.6th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.8%
- **30-Day Avg:** 27.0%
- **90-Day Avg:** 23.7%
- **Data Points:** 761 (2023-08-11 to 2026-07-20)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 45.2% | 71/157 | 30.0% | Up | +0.0311 | Overbought |
| 2 | Real Estate | 37.3% | 53/142 | 30.7% | Up | +0.0049 | Overbought |
| 3 | Financial | 29.3% | 179/610 | 31.8% | Down | -0.0083 | Normal |
| 4 | Healthcare | 27.4% | 115/420 | 42.0% | Down | -0.0238 | Normal |
| 5 | Communication Services | 20.9% | 23/110 | 23.5% | Down | -0.0054 | Normal |
| 6 | Consumer Cyclical | 18.7% | 52/278 | 18.3% | Down | -0.0035 | Normal |
| 7 | Industrials | 17.1% | 67/392 | 17.9% | Down | -0.0121 | Normal |
| 8 | Consumer Defensive | 15.3% | 18/118 | 19.1% | Down | -0.0089 | Normal |
| 9 | Technology | 14.3% | 59/413 | 16.2% | Down | -0.0037 | Normal |
| 10 | Utilities | 13.8% | 11/80 | 14.2% | Up | +0.0026 | Normal |
| 11 | Basic Materials | 9.6% | 14/146 | 10.5% | Down | -0.0058 | Oversold |

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
