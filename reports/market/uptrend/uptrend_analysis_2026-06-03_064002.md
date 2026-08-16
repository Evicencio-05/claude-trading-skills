# Uptrend Analyzer Report

**Generated:** 2026-06-03 06:40:02
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **58.9/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: -1.1 points from 60 (below)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 61.9/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (79/100) |
| **Weakest Component** | Market Breadth (Overall) (41/100) |
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
| Uptrend Ratio | 23.5% |
| 10-Day MA | 23.2% |
| Trend | up |
| Slope | +0.0066 |
| Distance from 37% (Overbought) | -13.5pp |
| Distance from 9.7% (Oversold) | +13.8pp |
| Date | 2026-06-02 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 41 | 12.3 | WEAK: 23.5% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ███░ 76 | 19.0 | HEALTHY: 8/11 sectors uptrending, spread 30.1% |
| 3 | **Sector Rotation** | 15% | ███░ 79 | 11.8 | RISK-ON: Cyclical leads by 12.2pp |
| 4 | **Momentum** | 20% | ███░ 68 | 13.6 | POSITIVE MOMENTUM: slope=0.0040, accelerating |
| 5 | **Historical Context** | 10% | ██░░ 51 | 5.1 | NEAR MEDIAN: 23.5% at 50.6th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 23.5%
- **10-Day MA:** 23.2%
- **Trend:** up
- **Slope:** +0.0066
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 8/11
- **Count Score:** 80/100
- **Spread:** 30.1% (score: 70/100)
- **Overbought (>37%):** 1 sectors (Technology)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 26.7%
- **Defensive Avg:** 14.5%
- **Commodity Avg:** 25.8%
- **Cyclical-Defensive Gap:** 12.2pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0863, spread=0.2401
    - Outlier: Technology (deviation: +0.1552)
  - **Defensive Divergence:** std=0.0213, spread=0.0563
    - Outlier: Real Estate (deviation: +0.0331)
    - Trend dissenter: Consumer Defensive (down vs majority up)
    - Trend dissenter: Healthcare (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 42.3% | Up | +0.0174 |
| Consumer Cyclical | 20.6% | Up | +0.0130 |
| Communication Services | 23.0% | Up | +0.0036 |
| Financial | 18.2% | Up | +0.0095 |
| Industrials | 29.6% | Up | +0.0135 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 14.8% | Up | +0.0086 |
| Consumer Defensive | 12.2% | Down | -0.0033 |
| Healthcare | 13.2% | Down | -0.0013 |
| Real Estate | 17.8% | Up | +0.0037 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 21.8% | Down | -0.0446 |
| Basic Materials | 29.7% | Up | +0.0239 |


### 4. Momentum

- **Raw Slope:** +0.0066
- **Smoothed Slope (EMA(3)):** +0.0040 (score: 63/100)
- **Acceleration (10v10):** 0.003977 (accelerating, score: 75/100)
- **Sector Slope Breadth:** 8/11 positive (score: 73/100)

### 5. Historical Context

- **Current Ratio:** 23.5%
- **Percentile Rank:** 50.6th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 25.4%
- **90-Day Avg:** 25.2%
- **Data Points:** 727 (2023-08-11 to 2026-06-02)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Technology | 42.3% | 180/426 | 36.9% | Up | +0.0174 | Overbought |
| 2 | Basic Materials | 29.7% | 47/158 | 22.2% | Up | +0.0239 | Normal |
| 3 | Industrials | 29.6% | 115/389 | 26.8% | Up | +0.0135 | Normal |
| 4 | Communication Services | 23.0% | 26/113 | 22.4% | Up | +0.0036 | Normal |
| 5 | Energy | 21.8% | 36/165 | 29.2% | Down | -0.0446 | Normal |
| 6 | Consumer Cyclical | 20.6% | 57/277 | 17.2% | Up | +0.0130 | Normal |
| 7 | Financial | 18.2% | 110/603 | 17.9% | Up | +0.0095 | Normal |
| 8 | Real Estate | 17.8% | 26/146 | 21.5% | Up | +0.0037 | Normal |
| 9 | Utilities | 14.8% | 12/81 | 12.2% | Up | +0.0086 | Normal |
| 10 | Healthcare | 13.2% | 53/402 | 21.5% | Down | -0.0013 | Normal |
| 11 | Consumer Defensive | 12.2% | 14/115 | 13.6% | Down | -0.0033 | Normal |

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
