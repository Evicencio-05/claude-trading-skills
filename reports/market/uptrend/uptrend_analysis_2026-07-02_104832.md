# Uptrend Analyzer Report

**Generated:** 2026-07-02 10:48:32
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **57.9/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: -2.1 points from 60 (below)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 60.9/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (72/100) |
| **Weakest Component** | Sector Rotation (54/100) |
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
| Uptrend Ratio | 30.4% |
| 10-Day MA | 29.1% |
| Trend | up |
| Slope | +0.0054 |
| Distance from 37% (Overbought) | -6.7pp |
| Distance from 9.7% (Oversold) | +20.6pp |
| Date | 2026-07-01 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 58 | 17.4 | NEUTRAL: 30.4% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ██░░ 59 | 14.8 | MODERATE: 7/11 sectors uptrending, spread 36.1% |
| 3 | **Sector Rotation** | 15% | ██░░ 54 | 8.1 | BALANCED: Cyclical-Defensive gap 0.9pp |
| 4 | **Momentum** | 20% | ███░ 67 | 13.4 | POSITIVE MOMENTUM: slope=0.0045, accelerating |
| 5 | **Historical Context** | 10% | ███░ 72 | 7.2 | SLIGHTLY ABOVE: 30.4% at 71.9th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 30.4%
- **10-Day MA:** 29.1%
- **Trend:** up
- **Slope:** +0.0054
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 7/11
- **Count Score:** 60/100
- **Spread:** 36.1% (score: 57/100)
- **Overbought (>37%):** 1 sectors (Healthcare)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 28.6%
- **Defensive Avg:** 27.7%
- **Commodity Avg:** 16.8%
- **Cyclical-Defensive Gap:** 0.9pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0472, spread=0.1213
    - Outlier: Financial (deviation: +0.0767)
    - Trend dissenter: Communication Services (up vs majority down)
    - Trend dissenter: Financial (up vs majority down)
  - **Defensive Divergence:** std=0.1284, spread=0.3607
    - Outlier: Healthcare (deviation: +0.1948)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 24.1% | Down | -0.0043 |
| Consumer Cyclical | 24.6% | Down | -0.0007 |
| Communication Services | 26.1% | Up | +0.0094 |
| Financial | 36.2% | Up | +0.0106 |
| Industrials | 31.8% | Down | -0.0012 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 11.1% | Up | +0.0074 |
| Consumer Defensive | 25.6% | Up | +0.0104 |
| Healthcare | 47.2% | Up | +0.0162 |
| Real Estate | 26.9% | Up | +0.0094 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 16.1% | Up | +0.0100 |
| Basic Materials | 17.6% | Down | -0.0095 |


### 4. Momentum

- **Raw Slope:** +0.0054
- **Smoothed Slope (EMA(3)):** +0.0044 (score: 63/100)
- **Acceleration (10v10):** 0.004116 (accelerating, score: 75/100)
- **Sector Slope Breadth:** 7/11 positive (score: 64/100)

### 5. Historical Context

- **Current Ratio:** 30.4%
- **Percentile Rank:** 71.9th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.6%
- **30-Day Avg:** 25.5%
- **90-Day Avg:** 23.7%
- **Data Points:** 748 (2023-08-11 to 2026-07-01)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 47.2% | 201/426 | 40.6% | Up | +0.0162 | Overbought |
| 2 | Financial | 36.2% | 229/632 | 31.8% | Up | +0.0106 | Normal |
| 3 | Industrials | 31.8% | 126/396 | 35.0% | Down | -0.0012 | Normal |
| 4 | Real Estate | 26.9% | 39/145 | 27.7% | Up | +0.0094 | Normal |
| 5 | Communication Services | 26.1% | 30/115 | 20.3% | Up | +0.0094 | Normal |
| 6 | Consumer Defensive | 25.6% | 31/121 | 21.7% | Up | +0.0104 | Normal |
| 7 | Consumer Cyclical | 24.6% | 69/281 | 27.8% | Down | -0.0007 | Normal |
| 8 | Technology | 24.1% | 101/419 | 27.8% | Down | -0.0043 | Normal |
| 9 | Basic Materials | 17.6% | 26/148 | 18.8% | Down | -0.0095 | Normal |
| 10 | Energy | 16.1% | 25/155 | 11.1% | Up | +0.0100 | Normal |
| 11 | Utilities | 11.1% | 9/81 | 10.5% | Up | +0.0074 | Normal |

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
