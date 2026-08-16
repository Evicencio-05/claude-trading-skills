# Uptrend Analyzer Report

**Generated:** 2026-06-29 06:21:43
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **57.6/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: -2.4 points from 60 (below)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 60.6/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (72/100) |
| **Weakest Component** | Sector Rotation (44/100) |
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
| 10-Day MA | 27.8% |
| Trend | up |
| Slope | +0.0018 |
| Distance from 37% (Overbought) | -6.6pp |
| Distance from 9.7% (Oversold) | +20.7pp |
| Date | 2026-06-26 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 58 | 17.4 | NEUTRAL: 30.4% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ███░ 63 | 15.8 | HEALTHY: 6/11 sectors uptrending, spread 31.3% |
| 3 | **Sector Rotation** | 15% | ██░░ 44 | 6.6 | DEFENSIVE TILT: Defensive leads by 3.5pp |
| 4 | **Momentum** | 20% | ███░ 68 | 13.6 | POSITIVE MOMENTUM: slope=0.0030, strong accelerating |
| 5 | **Historical Context** | 10% | ███░ 72 | 7.2 | SLIGHTLY ABOVE: 30.4% at 72.1th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 30.4%
- **10-Day MA:** 27.8%
- **Trend:** up
- **Slope:** +0.0018
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 6/11
- **Count Score:** 60/100
- **Spread:** 31.3% (score: 67/100)
- **Overbought (>37%):** 1 sectors (Healthcare)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 28.3%
- **Defensive Avg:** 31.8%
- **Commodity Avg:** 17.5%
- **Cyclical-Defensive Gap:** -3.5pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0511, spread=0.1333
    - Outlier: Technology (deviation: -0.0791)
    - Trend dissenter: Financial (up vs majority down)
    - Trend dissenter: Industrials (up vs majority down)
  - **Defensive Divergence:** std=0.1005, spread=0.2611

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 20.4% | Down | -0.0114 |
| Consumer Cyclical | 29.9% | Down | +0.0000 |
| Communication Services | 24.6% | Down | -0.0009 |
| Financial | 33.7% | Up | +0.0022 |
| Industrials | 33.0% | Up | +0.0004 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 19.8% | Up | +0.0111 |
| Consumer Defensive | 25.4% | Up | +0.0038 |
| Healthcare | 45.9% | Up | +0.0186 |
| Real Estate | 36.3% | Up | +0.0048 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 14.6% | Down | -0.0081 |
| Basic Materials | 20.4% | Down | -0.0026 |


### 4. Momentum

- **Raw Slope:** +0.0018
- **Smoothed Slope (EMA(3)):** +0.0030 (score: 61/100)
- **Acceleration (10v10):** 0.005085 (strong_accelerating, score: 90/100)
- **Sector Slope Breadth:** 6/11 positive (score: 55/100)

### 5. Historical Context

- **Current Ratio:** 30.4%
- **Percentile Rank:** 72.1th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.5%
- **30-Day Avg:** 24.3%
- **90-Day Avg:** 23.7%
- **Data Points:** 745 (2023-08-11 to 2026-06-26)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 45.9% | 194/423 | 35.2% | Up | +0.0186 | Overbought |
| 2 | Real Estate | 36.3% | 53/146 | 25.9% | Up | +0.0048 | Normal |
| 3 | Financial | 33.7% | 206/611 | 30.1% | Up | +0.0022 | Normal |
| 4 | Industrials | 33.0% | 129/391 | 34.8% | Up | +0.0004 | Normal |
| 5 | Consumer Cyclical | 29.9% | 83/278 | 28.2% | Down | +0.0000 | Normal |
| 6 | Consumer Defensive | 25.4% | 30/118 | 19.5% | Up | +0.0038 | Normal |
| 7 | Communication Services | 24.6% | 28/114 | 18.3% | Down | -0.0009 | Normal |
| 8 | Basic Materials | 20.4% | 30/147 | 22.5% | Down | -0.0026 | Normal |
| 9 | Technology | 20.4% | 84/412 | 29.0% | Down | -0.0114 | Normal |
| 10 | Utilities | 19.8% | 16/81 | 8.5% | Up | +0.0111 | Normal |
| 11 | Energy | 14.6% | 23/158 | 8.5% | Down | -0.0081 | Normal |

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
