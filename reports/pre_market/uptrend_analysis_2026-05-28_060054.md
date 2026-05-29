# Uptrend Analyzer Report

**Generated:** 2026-05-28 06:00:54
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **54.7/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: -5.3 points from 60 (below)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 57.7/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (69/100) |
| **Weakest Component** | Market Breadth (Overall) (43/100) |
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
| Uptrend Ratio | 24.4% |
| 10-Day MA | 22.2% |
| Trend | up |
| Slope | +0.0004 |
| Distance from 37% (Overbought) | -12.6pp |
| Distance from 9.7% (Oversold) | +14.7pp |
| Date | 2026-05-27 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 43 | 12.9 | WEAK: 24.4% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ███░ 67 | 16.8 | HEALTHY: 7/11 sectors uptrending, spread 26.2% |
| 3 | **Sector Rotation** | 15% | ███░ 69 | 10.3 | BALANCED: Cyclical-Defensive gap 7.1pp |
| 4 | **Momentum** | 20% | ███░ 62 | 12.4 | POSITIVE MOMENTUM: slope=-0.0000, accelerating |
| 5 | **Historical Context** | 10% | ██░░ 53 | 5.3 | NEAR MEDIAN: 24.4% at 52.8th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 24.4%
- **10-Day MA:** 22.2%
- **Trend:** up
- **Slope:** +0.0004
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 7/11
- **Count Score:** 60/100
- **Spread:** 26.2% (score: 78/100)
- **Overbought (>37%):** 1 sectors (Technology)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 26.5%
- **Defensive Avg:** 19.5%
- **Commodity Avg:** 19.2%
- **Cyclical-Defensive Gap:** 7.1pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0777, spread=0.2148
    - Outlier: Technology (deviation: +0.1303)
  - **Defensive Divergence:** std=0.0466, spread=0.109
    - Trend dissenter: Consumer Defensive (down vs majority up)
    - Trend dissenter: Healthcare (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 39.6% | Up | +0.0033 |
| Consumer Cyclical | 20.6% | Up | +0.0089 |
| Communication Services | 23.6% | Up | +0.0047 |
| Financial | 18.1% | Up | +0.0072 |
| Industrials | 30.7% | Up | +0.0039 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 13.6% | Up | +0.0011 |
| Consumer Defensive | 16.2% | Down | -0.0020 |
| Healthcare | 23.5% | Down | -0.0031 |
| Real Estate | 24.5% | Up | +0.0077 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 13.3% | Down | -0.0376 |
| Basic Materials | 25.2% | Down | -0.0176 |


### 4. Momentum

- **Raw Slope:** +0.0004
- **Smoothed Slope (EMA(3)):** -0.0000 (score: 54/100)
- **Acceleration (10v10):** 0.001025 (accelerating, score: 75/100)
- **Sector Slope Breadth:** 7/11 positive (score: 64/100)

### 5. Historical Context

- **Current Ratio:** 24.4%
- **Percentile Rank:** 52.8th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 27.0%
- **90-Day Avg:** 25.7%
- **Data Points:** 723 (2023-08-11 to 2026-05-27)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Technology | 39.6% | 165/417 | 33.6% | Up | +0.0033 | Overbought |
| 2 | Industrials | 30.7% | 119/387 | 25.0% | Up | +0.0039 | Normal |
| 3 | Basic Materials | 25.2% | 39/155 | 18.0% | Down | -0.0176 | Normal |
| 4 | Real Estate | 24.5% | 35/143 | 19.9% | Up | +0.0077 | Normal |
| 5 | Communication Services | 23.6% | 26/110 | 21.4% | Up | +0.0047 | Normal |
| 6 | Healthcare | 23.5% | 97/412 | 21.0% | Down | -0.0031 | Normal |
| 7 | Consumer Cyclical | 20.6% | 58/281 | 12.8% | Up | +0.0089 | Normal |
| 8 | Financial | 18.1% | 108/597 | 15.6% | Up | +0.0072 | Normal |
| 9 | Consumer Defensive | 16.2% | 19/117 | 14.8% | Down | -0.0020 | Normal |
| 10 | Utilities | 13.6% | 11/81 | 10.3% | Up | +0.0011 | Normal |
| 11 | Energy | 13.3% | 22/165 | 48.5% | Down | -0.0376 | Normal |

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
