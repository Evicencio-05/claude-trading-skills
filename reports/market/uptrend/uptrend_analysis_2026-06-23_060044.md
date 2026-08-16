# Uptrend Analyzer Report

**Generated:** 2026-06-23 06:00:44
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **63.4/100** |
| **Zone** | 🟢 Bull |
| **Zone Detail** | Bull-Lower |
| **Zone Proximity** | **Near boundary: +3.4 points from 60 (above)** |
| **Exposure Guidance** | Normal Exposure, Lower End (80-90%) |
| **Warning Penalty** | -3 (raw: 66.4/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Participation (75/100) |
| **Weakest Component** | Market Breadth (Overall) (53/100) |
| **Data Quality** | Complete (5/5 components) |
| **Confidence** | High (moderate, Both regime coverage) |

> **Guidance:** Healthy market breadth supporting equity allocation. Standard position management. However, active warnings suggest operating at the conservative end of the range.
>
> Note: Score is in the Bull zone, but 1 warning(s) are active.
> Exposure guidance has been tightened. See Active Warnings below.

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
| Uptrend Ratio | 28.3% |
| 10-Day MA | 26.3% |
| Trend | up |
| Slope | +0.0081 |
| Distance from 37% (Overbought) | -8.7pp |
| Distance from 9.7% (Oversold) | +18.6pp |
| Date | 2026-06-22 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 53 | 15.9 | NEUTRAL: 28.3% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ███░ 75 | 18.8 | HEALTHY: 8/11 sectors uptrending, spread 31.5% |
| 3 | **Sector Rotation** | 15% | ███░ 72 | 10.8 | RISK-ON: Cyclical leads by 8.7pp |
| 4 | **Momentum** | 20% | ███░ 72 | 14.4 | POSITIVE MOMENTUM: slope=0.0075, accelerating |
| 5 | **Historical Context** | 10% | ███░ 66 | 6.6 | SLIGHTLY ABOVE: 28.3% at 65.7th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 28.3%
- **10-Day MA:** 26.3%
- **Trend:** up
- **Slope:** +0.0081
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 8/11
- **Count Score:** 80/100
- **Spread:** 31.5% (score: 67/100)
- **Overbought (>37%):** 1 sectors (Industrials)
- **Oversold (<9.7%):** 2 sectors (Energy, Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 28.9%
- **Defensive Avg:** 20.2%
- **Commodity Avg:** 15.1%
- **Cyclical-Defensive Gap:** 8.7pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0754, spread=0.2206
    - Outlier: Communication Services (deviation: -0.1331)
    - Trend dissenter: Communication Services (down vs majority up)
  - **Defensive Divergence:** std=0.1037, spread=0.2881
    - Trend dissenter: Utilities (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 33.7% | Up | +0.0057 |
| Consumer Cyclical | 26.8% | Up | +0.0058 |
| Communication Services | 15.6% | Down | -0.0017 |
| Financial | 30.8% | Up | +0.0108 |
| Industrials | 37.7% | Up | +0.0144 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 6.2% | Down | -0.0001 |
| Consumer Defensive | 17.1% | Up | +0.0011 |
| Healthcare | 35.0% | Up | +0.0173 |
| Real Estate | 22.4% | Up | +0.0028 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 7.4% | Down | -0.0128 |
| Basic Materials | 22.7% | Up | +0.0118 |


### 4. Momentum

- **Raw Slope:** +0.0081
- **Smoothed Slope (EMA(3)):** +0.0075 (score: 69/100)
- **Acceleration (10v10):** 0.002174 (accelerating, score: 75/100)
- **Sector Slope Breadth:** 8/11 positive (score: 73/100)

### 5. Historical Context

- **Current Ratio:** 28.3%
- **Percentile Rank:** 65.7th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.5%
- **30-Day Avg:** 23.6%
- **90-Day Avg:** 24.0%
- **Data Points:** 741 (2023-08-11 to 2026-06-22)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Industrials | 37.7% | 148/393 | 32.2% | Up | +0.0144 | Overbought |
| 2 | Healthcare | 35.0% | 141/403 | 28.6% | Up | +0.0173 | Normal |
| 3 | Technology | 33.7% | 137/407 | 30.0% | Up | +0.0057 | Normal |
| 4 | Financial | 30.8% | 187/607 | 28.3% | Up | +0.0108 | Normal |
| 5 | Consumer Cyclical | 26.8% | 74/276 | 27.5% | Up | +0.0058 | Normal |
| 6 | Basic Materials | 22.7% | 35/154 | 22.0% | Up | +0.0118 | Normal |
| 7 | Real Estate | 22.4% | 32/143 | 25.6% | Up | +0.0028 | Normal |
| 8 | Consumer Defensive | 17.1% | 20/117 | 18.8% | Up | +0.0011 | Normal |
| 9 | Communication Services | 15.6% | 17/109 | 19.2% | Down | -0.0017 | Normal |
| 10 | Energy | 7.4% | 12/162 | 12.4% | Down | -0.0128 | Oversold |
| 11 | Utilities | 6.2% | 5/81 | 6.6% | Down | -0.0001 | Oversold |

---

## Recommended Actions

**Zone:** Bull (Bull-Lower)
**Exposure Guidance:** Normal Exposure, Lower End (80-90%)

- Normal position sizing
- New entries on quality setups
- Standard stop-loss levels
- Monitor sector rotation for early warnings

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
