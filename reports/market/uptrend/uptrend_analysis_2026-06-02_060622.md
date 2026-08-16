# Uptrend Analyzer Report

**Generated:** 2026-06-02 06:06:22
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **56.4/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: -3.6 points from 60 (below)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 59.4/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Participation (78/100) |
| **Weakest Component** | Market Breadth (Overall) (36/100) |
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
| Uptrend Ratio | 21.0% |
| 10-Day MA | 22.6% |
| Trend | up |
| Slope | +0.0015 |
| Distance from 37% (Overbought) | -16.0pp |
| Distance from 9.7% (Oversold) | +11.3pp |
| Date | 2026-06-01 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 36 | 10.8 | WEAK: 21.0% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ███░ 78 | 19.5 | HEALTHY: 9/11 sectors uptrending, spread 26.9% |
| 3 | **Sector Rotation** | 15% | ███░ 75 | 11.2 | RISK-ON: Cyclical leads by 10.4pp |
| 4 | **Momentum** | 20% | ███░ 68 | 13.6 | POSITIVE MOMENTUM: slope=0.0013, accelerating |
| 5 | **Historical Context** | 10% | ██░░ 42 | 4.2 | NEAR MEDIAN: 21.0% at 41.8th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 21.0%
- **10-Day MA:** 22.6%
- **Trend:** up
- **Slope:** +0.0015
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 9/11
- **Count Score:** 80/100
- **Spread:** 26.9% (score: 76/100)
- **Overbought (>37%):** 0 sectors ()
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 24.5%
- **Defensive Avg:** 14.1%
- **Commodity Avg:** 19.7%
- **Cyclical-Defensive Gap:** 10.4pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.081, spread=0.2341
    - Outlier: Technology (deviation: +0.1231)
  - **Defensive Divergence:** std=0.0317, spread=0.0855
    - Trend dissenter: Consumer Defensive (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 36.8% | Up | +0.0090 |
| Consumer Cyclical | 18.3% | Up | +0.0096 |
| Communication Services | 28.1% | Up | +0.0061 |
| Financial | 13.4% | Up | +0.0025 |
| Industrials | 25.8% | Up | +0.0043 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 9.9% | Up | +0.0024 |
| Consumer Defensive | 12.7% | Down | -0.0028 |
| Healthcare | 18.4% | Up | +0.0033 |
| Real Estate | 15.4% | Up | +0.0006 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 12.7% | Down | -0.0567 |
| Basic Materials | 26.8% | Up | +0.0125 |


### 4. Momentum

- **Raw Slope:** +0.0015
- **Smoothed Slope (EMA(3)):** +0.0013 (score: 57/100)
- **Acceleration (10v10):** 0.002819 (accelerating, score: 75/100)
- **Sector Slope Breadth:** 9/11 positive (score: 82/100)

### 5. Historical Context

- **Current Ratio:** 21.0%
- **Percentile Rank:** 41.8th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 25.7%
- **90-Day Avg:** 25.3%
- **Data Points:** 726 (2023-08-11 to 2026-06-01)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Technology | 36.8% | 157/427 | 35.2% | Up | +0.0090 | Normal |
| 2 | Communication Services | 28.1% | 32/114 | 22.1% | Up | +0.0061 | Normal |
| 3 | Basic Materials | 26.8% | 42/157 | 19.8% | Up | +0.0125 | Normal |
| 4 | Industrials | 25.8% | 100/387 | 25.5% | Up | +0.0043 | Normal |
| 5 | Healthcare | 18.4% | 75/407 | 21.6% | Up | +0.0033 | Normal |
| 6 | Consumer Cyclical | 18.3% | 51/279 | 15.9% | Up | +0.0096 | Normal |
| 7 | Real Estate | 15.4% | 22/143 | 21.1% | Up | +0.0006 | Normal |
| 8 | Financial | 13.4% | 80/599 | 17.0% | Up | +0.0025 | Normal |
| 9 | Energy | 12.7% | 21/165 | 33.6% | Down | -0.0567 | Normal |
| 10 | Consumer Defensive | 12.7% | 15/118 | 13.9% | Down | -0.0028 | Normal |
| 11 | Utilities | 9.9% | 8/81 | 11.3% | Up | +0.0024 | Normal |

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
