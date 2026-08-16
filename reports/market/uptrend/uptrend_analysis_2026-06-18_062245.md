# Uptrend Analyzer Report

**Generated:** 2026-06-18 06:22:45
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **56.0/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: -4.0 points from 60 (below)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 59.0/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (72/100) |
| **Weakest Component** | Market Breadth (Overall) (44/100) |
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
| Uptrend Ratio | 24.9% |
| 10-Day MA | 24.2% |
| Trend | up |
| Slope | +0.0038 |
| Distance from 37% (Overbought) | -12.1pp |
| Distance from 9.7% (Oversold) | +15.2pp |
| Date | 2026-06-17 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 44 | 13.2 | WEAK: 24.9% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ███░ 65 | 16.2 | HEALTHY: 7/11 sectors uptrending, spread 29.3% |
| 3 | **Sector Rotation** | 15% | ███░ 72 | 10.8 | RISK-ON: Cyclical leads by 8.9pp |
| 4 | **Momentum** | 20% | ███░ 67 | 13.4 | POSITIVE MOMENTUM: slope=0.0043, accelerating |
| 5 | **Historical Context** | 10% | ██░░ 54 | 5.4 | NEAR MEDIAN: 24.9% at 54.4th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 24.9%
- **10-Day MA:** 24.2%
- **Trend:** up
- **Slope:** +0.0038
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 7/11
- **Count Score:** 60/100
- **Spread:** 29.3% (score: 71/100)
- **Overbought (>37%):** 0 sectors ()
- **Oversold (<9.7%):** 2 sectors (Energy, Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 25.8%
- **Defensive Avg:** 16.9%
- **Commodity Avg:** 16.6%
- **Cyclical-Defensive Gap:** 8.9pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0534, spread=0.1632
    - Outlier: Communication Services (deviation: -0.0914)
    - Trend dissenter: Technology (down vs majority up)
    - Trend dissenter: Communication Services (down vs majority up)
  - **Defensive Divergence:** std=0.097, spread=0.273
    - Trend dissenter: Utilities (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 28.4% | Down | -0.0131 |
| Consumer Cyclical | 25.3% | Up | +0.0039 |
| Communication Services | 16.7% | Down | -0.0002 |
| Financial | 25.7% | Up | +0.0156 |
| Industrials | 33.0% | Up | +0.0036 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 3.7% | Down | -0.0088 |
| Consumer Defensive | 15.3% | Up | +0.0023 |
| Healthcare | 31.0% | Up | +0.0154 |
| Real Estate | 17.5% | Up | +0.0024 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 6.1% | Down | -0.0121 |
| Basic Materials | 27.1% | Up | +0.0023 |


### 4. Momentum

- **Raw Slope:** +0.0038
- **Smoothed Slope (EMA(3)):** +0.0043 (score: 63/100)
- **Acceleration (10v10):** 0.001296 (accelerating, score: 75/100)
- **Sector Slope Breadth:** 7/11 positive (score: 64/100)

### 5. Historical Context

- **Current Ratio:** 24.9%
- **Percentile Rank:** 54.4th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 23.4%
- **90-Day Avg:** 24.1%
- **Data Points:** 738 (2023-08-11 to 2026-06-17)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Industrials | 33.0% | 128/388 | 28.5% | Up | +0.0036 | Normal |
| 2 | Healthcare | 31.0% | 124/400 | 24.3% | Up | +0.0154 | Normal |
| 3 | Technology | 28.4% | 116/408 | 28.8% | Down | -0.0131 | Normal |
| 4 | Basic Materials | 27.1% | 42/155 | 19.4% | Up | +0.0023 | Normal |
| 5 | Financial | 25.7% | 154/600 | 25.2% | Up | +0.0156 | Normal |
| 6 | Consumer Cyclical | 25.3% | 70/277 | 25.1% | Up | +0.0039 | Normal |
| 7 | Real Estate | 17.5% | 25/143 | 25.6% | Up | +0.0024 | Normal |
| 8 | Communication Services | 16.7% | 18/108 | 19.7% | Down | -0.0002 | Normal |
| 9 | Consumer Defensive | 15.3% | 18/118 | 17.4% | Up | +0.0023 | Normal |
| 10 | Energy | 6.1% | 10/164 | 16.0% | Down | -0.0121 | Oversold |
| 11 | Utilities | 3.7% | 3/81 | 7.7% | Down | -0.0088 | Oversold |

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
