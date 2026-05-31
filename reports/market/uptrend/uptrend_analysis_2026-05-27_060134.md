# Uptrend Analyzer Report

**Generated:** 2026-05-27 06:01:34
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **55.1/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: -4.9 points from 60 (below)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 58.1/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (71/100) |
| **Weakest Component** | Market Breadth (Overall) (48/100) |
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
| Uptrend Ratio | 26.3% |
| 10-Day MA | 22.2% |
| Trend | up |
| Slope | +0.0022 |
| Distance from 37% (Overbought) | -10.7pp |
| Distance from 9.7% (Oversold) | +16.6pp |
| Date | 2026-05-26 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 48 | 14.4 | NEUTRAL: 26.3% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ███░ 66 | 16.5 | HEALTHY: 7/11 sectors uptrending, spread 27.7% |
| 3 | **Sector Rotation** | 15% | ███░ 71 | 10.7 | RISK-ON: Cyclical leads by 8.2pp |
| 4 | **Momentum** | 20% | ██░░ 54 | 10.8 | NEUTRAL MOMENTUM: slope=-0.0004, steady |
| 5 | **Historical Context** | 10% | ██░░ 58 | 5.8 | NEAR MEDIAN: 26.3% at 57.7th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 26.3%
- **10-Day MA:** 22.2%
- **Trend:** up
- **Slope:** +0.0022
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 7/11
- **Count Score:** 60/100
- **Spread:** 27.7% (score: 75/100)
- **Overbought (>37%):** 1 sectors (Technology)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 27.3%
- **Defensive Avg:** 19.1%
- **Commodity Avg:** 27.2%
- **Cyclical-Defensive Gap:** 8.2pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0724, spread=0.2077
    - Outlier: Technology (deviation: +0.1263)
  - **Defensive Divergence:** std=0.0571, spread=0.13
    - Trend dissenter: Consumer Defensive (down vs majority up)
    - Trend dissenter: Healthcare (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 39.9% | Up | +0.0043 |
| Consumer Cyclical | 19.1% | Up | +0.0082 |
| Communication Services | 23.4% | Up | +0.0077 |
| Financial | 23.7% | Up | +0.0113 |
| Industrials | 30.2% | Up | +0.0023 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 14.8% | Up | +0.0036 |
| Consumer Defensive | 12.2% | Down | -0.0043 |
| Healthcare | 24.3% | Down | -0.0015 |
| Real Estate | 25.2% | Up | +0.0028 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 27.3% | Down | -0.0227 |
| Basic Materials | 27.1% | Down | -0.0143 |


### 4. Momentum

- **Raw Slope:** +0.0022
- **Smoothed Slope (EMA(3)):** -0.0004 (score: 53/100)
- **Acceleration (10v10):** 0.000649 (steady, score: 50/100)
- **Sector Slope Breadth:** 7/11 positive (score: 64/100)

### 5. Historical Context

- **Current Ratio:** 26.3%
- **Percentile Rank:** 57.7th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 27.3%
- **90-Day Avg:** 25.8%
- **Data Points:** 722 (2023-08-11 to 2026-05-26)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Technology | 39.9% | 166/416 | 33.2% | Up | +0.0043 | Overbought |
| 2 | Industrials | 30.2% | 116/384 | 24.6% | Up | +0.0023 | Normal |
| 3 | Energy | 27.3% | 45/165 | 52.2% | Down | -0.0227 | Normal |
| 4 | Basic Materials | 27.1% | 42/155 | 19.8% | Down | -0.0143 | Normal |
| 5 | Real Estate | 25.2% | 36/143 | 19.1% | Up | +0.0028 | Normal |
| 6 | Healthcare | 24.3% | 99/407 | 21.3% | Down | -0.0015 | Normal |
| 7 | Financial | 23.7% | 142/599 | 14.9% | Up | +0.0113 | Normal |
| 8 | Communication Services | 23.4% | 26/111 | 20.9% | Up | +0.0077 | Normal |
| 9 | Consumer Cyclical | 19.1% | 53/277 | 11.9% | Up | +0.0082 | Normal |
| 10 | Utilities | 14.8% | 12/81 | 10.2% | Up | +0.0036 | Normal |
| 11 | Consumer Defensive | 12.2% | 14/115 | 15.0% | Down | -0.0043 | Normal |

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
