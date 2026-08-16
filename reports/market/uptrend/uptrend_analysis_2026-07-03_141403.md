# Uptrend Analyzer Report

**Generated:** 2026-07-03 14:14:03
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **50.8/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: -9.2 points from 60 (below)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 53.8/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (66/100) |
| **Weakest Component** | Sector Rotation (32/100) |
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
| Uptrend Ratio | 28.5% |
| 10-Day MA | 29.1% |
| Trend | up |
| Slope | +0.0008 |
| Distance from 37% (Overbought) | -8.5pp |
| Distance from 9.7% (Oversold) | +18.8pp |
| Date | 2026-07-02 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 53 | 15.9 | NEUTRAL: 28.5% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ██░░ 54 | 13.5 | MODERATE: 7/11 sectors uptrending, spread 39.9% |
| 3 | **Sector Rotation** | 15% | █░░░ 32 | 4.8 | DEFENSIVE TILT: Defensive leads by 7.9pp |
| 4 | **Momentum** | 20% | ███░ 65 | 13.0 | POSITIVE MOMENTUM: slope=0.0026, accelerating |
| 5 | **Historical Context** | 10% | ███░ 66 | 6.6 | SLIGHTLY ABOVE: 28.5% at 65.8th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 28.5%
- **10-Day MA:** 29.1%
- **Trend:** up
- **Slope:** +0.0008
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 7/11
- **Count Score:** 60/100
- **Spread:** 39.9% (score: 45/100)
- **Overbought (>37%):** 1 sectors (Healthcare)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 24.4%
- **Defensive Avg:** 32.3%
- **Commodity Avg:** 14.1%
- **Cyclical-Defensive Gap:** -7.9pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0686, spread=0.2166
    - Outlier: Technology (deviation: -0.1122)
    - Outlier: Financial (deviation: +0.1044)
    - Trend dissenter: Communication Services (up vs majority down)
    - Trend dissenter: Financial (up vs majority down)
  - **Defensive Divergence:** std=0.1311, spread=0.3593
    - Outlier: Healthcare (deviation: +0.1969)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 13.2% | Down | -0.0214 |
| Consumer Cyclical | 24.4% | Down | -0.0040 |
| Communication Services | 24.3% | Up | +0.0097 |
| Financial | 34.8% | Up | +0.0060 |
| Industrials | 25.2% | Down | -0.0112 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 16.0% | Up | +0.0110 |
| Consumer Defensive | 26.7% | Up | +0.0070 |
| Healthcare | 52.0% | Up | +0.0192 |
| Real Estate | 34.5% | Up | +0.0143 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 12.1% | Up | +0.0048 |
| Basic Materials | 16.0% | Down | -0.0067 |


### 4. Momentum

- **Raw Slope:** +0.0008
- **Smoothed Slope (EMA(3)):** +0.0026 (score: 60/100)
- **Acceleration (10v10):** 0.003838 (accelerating, score: 75/100)
- **Sector Slope Breadth:** 7/11 positive (score: 64/100)

### 5. Historical Context

- **Current Ratio:** 28.5%
- **Percentile Rank:** 65.8th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.6%
- **30-Day Avg:** 25.7%
- **90-Day Avg:** 23.6%
- **Data Points:** 749 (2023-08-11 to 2026-07-02)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 52.0% | 223/429 | 42.5% | Up | +0.0192 | Overbought |
| 2 | Financial | 34.8% | 219/629 | 32.4% | Up | +0.0060 | Normal |
| 3 | Real Estate | 34.5% | 50/145 | 29.1% | Up | +0.0143 | Normal |
| 4 | Consumer Defensive | 26.7% | 32/120 | 22.4% | Up | +0.0070 | Normal |
| 5 | Industrials | 25.2% | 99/393 | 33.9% | Down | -0.0112 | Normal |
| 6 | Consumer Cyclical | 24.4% | 68/279 | 27.4% | Down | -0.0040 | Normal |
| 7 | Communication Services | 24.3% | 28/115 | 21.2% | Up | +0.0097 | Normal |
| 8 | Utilities | 16.0% | 13/81 | 11.6% | Up | +0.0110 | Normal |
| 9 | Basic Materials | 16.0% | 24/150 | 18.1% | Down | -0.0067 | Normal |
| 10 | Technology | 13.2% | 55/418 | 25.6% | Down | -0.0214 | Normal |
| 11 | Energy | 12.1% | 19/157 | 11.6% | Up | +0.0048 | Normal |

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
