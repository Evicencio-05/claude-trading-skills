# Uptrend Analyzer Report

**Generated:** 2026-06-09 06:53:03
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **41.9/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: +1.9 points from 40 (above)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 44.9/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (69/100) |
| **Weakest Component** | Market Breadth (Overall) (25/100) |
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
| Uptrend Ratio | 20.2% |
| 10-Day MA | 22.6% |
| Trend | down |
| Slope | -0.0029 |
| Distance from 37% (Overbought) | -16.8pp |
| Distance from 9.7% (Oversold) | +10.5pp |
| Date | 2026-06-08 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 25 | 7.5 | VERY WEAK: 20.2% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ██░░ 47 | 11.8 | MODERATE: 3/11 sectors uptrending, spread 21.7% |
| 3 | **Sector Rotation** | 15% | ███░ 69 | 10.3 | BALANCED: Cyclical-Defensive gap 7.0pp |
| 4 | **Momentum** | 20% | ██░░ 57 | 11.4 | NEUTRAL MOMENTUM: slope=-0.0023, strong accelerating |
| 5 | **Historical Context** | 10% | █░░░ 39 | 3.9 | BELOW AVERAGE: 20.2% at 38.8th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 20.2%
- **10-Day MA:** 22.6%
- **Trend:** down
- **Slope:** -0.0029
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 3/11
- **Count Score:** 20/100
- **Spread:** 21.7% (score: 87/100)
- **Overbought (>37%):** 0 sectors ()
- **Oversold (<9.7%):** 1 sectors (Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 21.9%
- **Defensive Avg:** 14.9%
- **Commodity Avg:** 15.6%
- **Cyclical-Defensive Gap:** 7.0pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.036, spread=0.1071
    - Outlier: Technology (deviation: +0.0608)
    - Trend dissenter: Consumer Cyclical (up vs majority down)
    - Trend dissenter: Financial (up vs majority down)
  - **Defensive Divergence:** std=0.0514, spread=0.1333
    - Outlier: Utilities (deviation: -0.0863)
    - Trend dissenter: Consumer Defensive (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 28.0% | Down | -0.0082 |
| Consumer Cyclical | 21.0% | Up | +0.0069 |
| Communication Services | 17.3% | Down | -0.0020 |
| Financial | 20.0% | Up | +0.0029 |
| Industrials | 23.3% | Down | -0.0019 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 6.2% | Down | -0.0050 |
| Consumer Defensive | 16.0% | Up | +0.0022 |
| Healthcare | 17.7% | Down | -0.0044 |
| Real Estate | 19.6% | Down | -0.0035 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 20.2% | Down | -0.0264 |
| Basic Materials | 10.9% | Down | -0.0053 |


### 4. Momentum

- **Raw Slope:** -0.0029
- **Smoothed Slope (EMA(3)):** -0.0023 (score: 50/100)
- **Acceleration (10v10):** 0.005846 (strong_accelerating, score: 90/100)
- **Sector Slope Breadth:** 3/11 positive (score: 27/100)

### 5. Historical Context

- **Current Ratio:** 20.2%
- **Percentile Rank:** 38.8th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 23.9%
- **90-Day Avg:** 24.6%
- **Data Points:** 731 (2023-08-11 to 2026-06-08)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Technology | 28.0% | 115/411 | 36.7% | Down | -0.0082 | Normal |
| 2 | Industrials | 23.3% | 90/387 | 27.6% | Down | -0.0019 | Normal |
| 3 | Consumer Cyclical | 21.0% | 58/276 | 20.3% | Up | +0.0069 | Normal |
| 4 | Energy | 20.2% | 33/163 | 17.2% | Down | -0.0264 | Normal |
| 5 | Financial | 20.0% | 119/596 | 17.6% | Up | +0.0029 | Normal |
| 6 | Real Estate | 19.6% | 28/143 | 20.2% | Down | -0.0035 | Normal |
| 7 | Healthcare | 17.7% | 71/401 | 20.2% | Down | -0.0044 | Normal |
| 8 | Communication Services | 17.3% | 19/110 | 21.1% | Down | -0.0020 | Normal |
| 9 | Consumer Defensive | 16.0% | 19/119 | 13.3% | Up | +0.0022 | Normal |
| 10 | Basic Materials | 10.9% | 17/156 | 23.6% | Down | -0.0053 | Normal |
| 11 | Utilities | 6.2% | 5/80 | 11.9% | Down | -0.0050 | Oversold |

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
