# Uptrend Analyzer Report

**Generated:** 2026-07-08 06:08:42
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **48.3/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: +8.3 points from 40 (above)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 51.3/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (60/100) |
| **Weakest Component** | Sector Rotation (34/100) |
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
| Uptrend Ratio | 27.0% |
| 10-Day MA | 29.4% |
| Trend | up |
| Slope | +0.0006 |
| Distance from 37% (Overbought) | -10.0pp |
| Distance from 9.7% (Oversold) | +17.3pp |
| Date | 2026-07-07 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 50 | 15.0 | NEUTRAL: 27.0% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ██░░ 56 | 14.0 | MODERATE: 7/11 sectors uptrending, spread 38.1% |
| 3 | **Sector Rotation** | 15% | █░░░ 34 | 5.1 | DEFENSIVE TILT: Defensive leads by 7.2pp |
| 4 | **Momentum** | 20% | ██░░ 56 | 11.2 | NEUTRAL MOMENTUM: slope=0.0011, steady |
| 5 | **Historical Context** | 10% | ███░ 60 | 6.0 | SLIGHTLY ABOVE: 27.0% at 60.4th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 27.0%
- **10-Day MA:** 29.4%
- **Trend:** up
- **Slope:** +0.0006
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 7/11
- **Count Score:** 60/100
- **Spread:** 38.1% (score: 51/100)
- **Overbought (>37%):** 1 sectors (Healthcare)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 22.7%
- **Defensive Avg:** 30.0%
- **Commodity Avg:** 14.6%
- **Cyclical-Defensive Gap:** -7.2pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.074, spread=0.2295
    - Outlier: Financial (deviation: +0.1235)
    - Trend dissenter: Communication Services (up vs majority down)
    - Trend dissenter: Financial (up vs majority down)
  - **Defensive Divergence:** std=0.1325, spread=0.3542
    - Outlier: Healthcare (deviation: +0.2024)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 12.1% | Down | -0.0127 |
| Consumer Cyclical | 21.7% | Down | -0.0044 |
| Communication Services | 24.3% | Up | +0.0090 |
| Financial | 35.1% | Up | +0.0031 |
| Industrials | 20.5% | Down | -0.0121 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 14.8% | Up | +0.0099 |
| Consumer Defensive | 22.5% | Up | +0.0049 |
| Healthcare | 50.2% | Up | +0.0149 |
| Real Estate | 32.4% | Up | +0.0046 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 16.9% | Up | +0.0088 |
| Basic Materials | 12.2% | Down | -0.0011 |


### 4. Momentum

- **Raw Slope:** +0.0006
- **Smoothed Slope (EMA(3)):** +0.0011 (score: 57/100)
- **Acceleration (10v10):** -0.000499 (steady, score: 50/100)
- **Sector Slope Breadth:** 7/11 positive (score: 64/100)

### 5. Historical Context

- **Current Ratio:** 27.0%
- **Percentile Rank:** 60.4th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.7%
- **30-Day Avg:** 26.1%
- **90-Day Avg:** 23.5%
- **Data Points:** 752 (2023-08-11 to 2026-07-07)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 50.2% | 217/432 | 47.6% | Up | +0.0149 | Overbought |
| 2 | Financial | 35.1% | 219/624 | 34.0% | Up | +0.0031 | Normal |
| 3 | Real Estate | 32.4% | 47/145 | 32.0% | Up | +0.0046 | Normal |
| 4 | Communication Services | 24.3% | 27/111 | 24.2% | Up | +0.0090 | Normal |
| 5 | Consumer Defensive | 22.5% | 27/120 | 24.3% | Up | +0.0049 | Normal |
| 6 | Consumer Cyclical | 21.7% | 60/277 | 26.1% | Down | -0.0044 | Normal |
| 7 | Industrials | 20.5% | 80/390 | 30.7% | Down | -0.0121 | Normal |
| 8 | Energy | 16.9% | 26/154 | 13.6% | Up | +0.0088 | Normal |
| 9 | Utilities | 14.8% | 12/81 | 14.2% | Up | +0.0099 | Normal |
| 10 | Basic Materials | 12.2% | 18/147 | 16.6% | Down | -0.0011 | Normal |
| 11 | Technology | 12.1% | 51/420 | 20.6% | Down | -0.0127 | Normal |

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
