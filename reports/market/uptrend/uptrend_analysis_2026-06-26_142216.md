# Uptrend Analyzer Report

**Generated:** 2026-06-26 14:22:16
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **57.7/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: -2.3 points from 60 (below)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 60.7/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Momentum (69/100) |
| **Weakest Component** | Market Breadth (Overall) (54/100) |
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
| Uptrend Ratio | 28.7% |
| 10-Day MA | 27.6% |
| Trend | up |
| Slope | +0.0023 |
| Distance from 37% (Overbought) | -8.3pp |
| Distance from 9.7% (Oversold) | +19.0pp |
| Date | 2026-06-25 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 54 | 16.2 | NEUTRAL: 28.7% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ███░ 63 | 15.8 | HEALTHY: 6/11 sectors uptrending, spread 30.8% |
| 3 | **Sector Rotation** | 15% | ██░░ 55 | 8.2 | BALANCED: Cyclical-Defensive gap 1.4pp |
| 4 | **Momentum** | 20% | ███░ 69 | 13.8 | POSITIVE MOMENTUM: slope=0.0042, strong accelerating |
| 5 | **Historical Context** | 10% | ███░ 67 | 6.7 | SLIGHTLY ABOVE: 28.7% at 67.0th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 28.7%
- **10-Day MA:** 27.6%
- **Trend:** up
- **Slope:** +0.0023
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 6/11
- **Count Score:** 60/100
- **Spread:** 30.8% (score: 68/100)
- **Overbought (>37%):** 1 sectors (Healthcare)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 27.6%
- **Defensive Avg:** 26.2%
- **Commodity Avg:** 15.4%
- **Cyclical-Defensive Gap:** 1.4pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0553, spread=0.16
    - Trend dissenter: Financial (up vs majority down)
    - Trend dissenter: Industrials (up vs majority down)
  - **Defensive Divergence:** std=0.111, spread=0.3082
    - Trend dissenter: Real Estate (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 23.8% | Down | -0.0082 |
| Consumer Cyclical | 27.8% | Down | +0.0000 |
| Communication Services | 19.8% | Down | -0.0036 |
| Financial | 30.8% | Up | +0.0022 |
| Industrials | 35.8% | Up | +0.0055 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 11.1% | Up | +0.0062 |
| Consumer Defensive | 22.9% | Up | +0.0012 |
| Healthcare | 41.9% | Up | +0.0164 |
| Real Estate | 28.8% | Down | -0.0022 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 11.9% | Down | -0.0041 |
| Basic Materials | 18.8% | Up | +0.0018 |


### 4. Momentum

- **Raw Slope:** +0.0023
- **Smoothed Slope (EMA(3)):** +0.0042 (score: 63/100)
- **Acceleration (10v10):** 0.005155 (strong_accelerating, score: 90/100)
- **Sector Slope Breadth:** 6/11 positive (score: 55/100)

### 5. Historical Context

- **Current Ratio:** 28.7%
- **Percentile Rank:** 67.0th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.5%
- **30-Day Avg:** 24.0%
- **90-Day Avg:** 23.8%
- **Data Points:** 744 (2023-08-11 to 2026-06-25)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 41.9% | 174/415 | 33.3% | Up | +0.0164 | Overbought |
| 2 | Industrials | 35.8% | 139/388 | 34.8% | Up | +0.0055 | Normal |
| 3 | Financial | 30.8% | 188/610 | 29.9% | Up | +0.0022 | Normal |
| 4 | Real Estate | 28.8% | 42/146 | 25.4% | Down | -0.0022 | Normal |
| 5 | Consumer Cyclical | 27.8% | 77/277 | 28.2% | Down | +0.0000 | Normal |
| 6 | Technology | 23.8% | 97/407 | 30.1% | Down | -0.0082 | Normal |
| 7 | Consumer Defensive | 22.9% | 27/118 | 19.1% | Up | +0.0012 | Normal |
| 8 | Communication Services | 19.8% | 22/111 | 18.4% | Down | -0.0036 | Normal |
| 9 | Basic Materials | 18.8% | 28/149 | 22.7% | Up | +0.0018 | Normal |
| 10 | Energy | 11.9% | 19/159 | 9.4% | Down | -0.0041 | Normal |
| 11 | Utilities | 11.1% | 9/81 | 7.4% | Up | +0.0062 | Normal |

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
