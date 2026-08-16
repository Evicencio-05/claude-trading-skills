# Uptrend Analyzer Report

**Generated:** 2026-06-04 07:03:00
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **46.2/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: +6.2 points from 40 (above)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 49.2/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (74/100) |
| **Weakest Component** | Market Breadth (Overall) (27/100) |
| **Data Quality** | Complete (5/5 components) |
| **Confidence** | High (moderate, Both regime coverage) |

> **Guidance:** Mixed signals. Participate selectively with tighter risk controls.

---

## Active Warnings

### SECTOR DIVERGENCE WARNING
> Significant divergence detected within sector groups. Some sectors within the same group are moving in opposite directions, suggesting hidden risk beneath the averages.

- Verify individual sector trends before entering positions
- Avoid sectors diverging from their group majority
- Monitor for group convergence or further deterioration

---

## Current Market Snapshot

| Metric | Value |
|--------|-------|
| Uptrend Ratio | 21.1% |
| 10-Day MA | 23.2% |
| Trend | down |
| Slope | -0.0004 |
| Distance from 37% (Overbought) | -15.9pp |
| Distance from 9.7% (Oversold) | +11.4pp |
| Date | 2026-06-03 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 27 | 8.1 | VERY WEAK: 21.1% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ██░░ 51 | 12.8 | MODERATE: 5/11 sectors uptrending, spread 31.4% |
| 3 | **Sector Rotation** | 15% | ███░ 74 | 11.1 | RISK-ON: Cyclical leads by 9.8pp |
| 4 | **Momentum** | 20% | ███░ 65 | 13.0 | POSITIVE MOMENTUM: slope=0.0018, strong accelerating |
| 5 | **Historical Context** | 10% | ██░░ 42 | 4.2 | NEAR MEDIAN: 21.1% at 42.1th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 21.1%
- **10-Day MA:** 23.2%
- **Trend:** down
- **Slope:** -0.0004
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 5/11
- **Count Score:** 40/100
- **Spread:** 31.4% (score: 67/100)
- **Overbought (>37%):** 1 sectors (Technology)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 23.8%
- **Defensive Avg:** 14.0%
- **Commodity Avg:** 21.5%
- **Cyclical-Defensive Gap:** 9.8pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.1084, spread=0.314
    - Outlier: Technology (deviation: +0.1765)
    - Trend dissenter: Communication Services (down vs majority up)
    - Trend dissenter: Financial (down vs majority up)
  - **Defensive Divergence:** std=0.0132, spread=0.0306
    - Trend dissenter: Utilities (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 41.5% | Up | +0.0119 |
| Consumer Cyclical | 21.4% | Up | +0.0116 |
| Communication Services | 16.8% | Down | -0.0043 |
| Financial | 10.1% | Down | -0.0077 |
| Industrials | 29.4% | Up | +0.0074 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 12.5% | Up | +0.0038 |
| Consumer Defensive | 12.9% | Down | -0.0034 |
| Healthcare | 15.6% | Down | -0.0054 |
| Real Estate | 15.1% | Down | -0.0059 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 18.2% | Down | -0.0396 |
| Basic Materials | 24.8% | Up | +0.0157 |


### 4. Momentum

- **Raw Slope:** -0.0004
- **Smoothed Slope (EMA(3)):** +0.0018 (score: 58/100)
- **Acceleration (10v10):** 0.0053 (strong_accelerating, score: 90/100)
- **Sector Slope Breadth:** 5/11 positive (score: 45/100)

### 5. Historical Context

- **Current Ratio:** 21.1%
- **Percentile Rank:** 42.1th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 24.9%
- **90-Day Avg:** 25.1%
- **Data Points:** 728 (2023-08-11 to 2026-06-03)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Technology | 41.5% | 173/417 | 38.1% | Up | +0.0119 | Overbought |
| 2 | Industrials | 29.4% | 113/384 | 27.6% | Up | +0.0074 | Normal |
| 3 | Basic Materials | 24.8% | 39/157 | 23.8% | Up | +0.0157 | Normal |
| 4 | Consumer Cyclical | 21.4% | 59/276 | 18.4% | Up | +0.0116 | Normal |
| 5 | Energy | 18.2% | 30/165 | 25.2% | Down | -0.0396 | Normal |
| 6 | Communication Services | 16.8% | 18/107 | 22.0% | Down | -0.0043 | Normal |
| 7 | Healthcare | 15.6% | 63/405 | 21.0% | Down | -0.0054 | Normal |
| 8 | Real Estate | 15.1% | 22/146 | 20.9% | Down | -0.0059 | Normal |
| 9 | Consumer Defensive | 12.9% | 15/116 | 13.2% | Down | -0.0034 | Normal |
| 10 | Utilities | 12.5% | 10/80 | 12.5% | Up | +0.0038 | Normal |
| 11 | Financial | 10.1% | 60/595 | 17.1% | Down | -0.0077 | Normal |

---

## Recommended Actions

**Zone:** Neutral (Neutral)
**Exposure Guidance:** Reduced Exposure (60-80%)

- Reduce position sizes by 20-30%
- Focus on strongest sectors only
- Tighten stop-losses
- Avoid low-quality setups
- Increase cash allocation gradually

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
