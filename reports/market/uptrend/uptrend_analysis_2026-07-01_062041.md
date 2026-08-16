# Uptrend Analyzer Report

**Generated:** 2026-07-01 06:20:41
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **64.4/100** |
| **Zone** | 🟢 Bull |
| **Zone Detail** | Bull-Lower |
| **Zone Proximity** | **Near boundary: +4.4 points from 60 (above)** |
| **Exposure Guidance** | Normal Exposure, Lower End (80-90%) |
| **Warning Penalty** | -3 (raw: 67.4/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (78/100) |
| **Weakest Component** | Sector Rotation (59/100) |
| **Data Quality** | Complete (5/5 components) |
| **Confidence** | High (moderate, Both regime coverage) |

> **Guidance:** Healthy market breadth supporting equity allocation. Standard position management. However, active warnings suggest operating at the conservative end of the range.
>
> Note: Score is in the Bull zone, but 1 warning(s) are active.
> Exposure guidance has been tightened. See Active Warnings below.

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
| Uptrend Ratio | 32.3% |
| 10-Day MA | 28.5% |
| Trend | up |
| Slope | +0.0037 |
| Distance from 37% (Overbought) | -4.8pp |
| Distance from 9.7% (Oversold) | +22.6pp |
| Date | 2026-06-30 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ███░ 63 | 18.9 | NEUTRAL: 32.3% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ███░ 73 | 18.2 | HEALTHY: 8/11 sectors uptrending, spread 33.9% |
| 3 | **Sector Rotation** | 15% | ██░░ 59 | 8.8 | BALANCED: Cyclical-Defensive gap 3.1pp |
| 4 | **Momentum** | 20% | ███░ 68 | 13.6 | POSITIVE MOMENTUM: slope=0.0035, accelerating |
| 5 | **Historical Context** | 10% | ███░ 78 | 7.8 | SLIGHTLY ABOVE: 32.3% at 78.4th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 32.3%
- **10-Day MA:** 28.5%
- **Trend:** up
- **Slope:** +0.0037
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 8/11
- **Count Score:** 80/100
- **Spread:** 33.9% (score: 62/100)
- **Overbought (>37%):** 2 sectors (Healthcare, Industrials)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 31.6%
- **Defensive Avg:** 28.6%
- **Commodity Avg:** 16.7%
- **Cyclical-Defensive Gap:** 3.1pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.042, spread=0.1191
    - Outlier: Industrials (deviation: +0.0660)
    - Trend dissenter: Consumer Cyclical (down vs majority up)
  - **Defensive Divergence:** std=0.1233, spread=0.3395
    - Outlier: Healthcare (deviation: +0.1898)
    - Trend dissenter: Real Estate (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 32.2% | Up | +0.0010 |
| Consumer Cyclical | 28.0% | Down | -0.0028 |
| Communication Services | 26.3% | Up | +0.0034 |
| Financial | 33.4% | Up | +0.0027 |
| Industrials | 38.2% | Up | +0.0018 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 13.6% | Up | +0.0037 |
| Consumer Defensive | 23.7% | Up | +0.0052 |
| Healthcare | 47.5% | Up | +0.0190 |
| Real Estate | 29.4% | Down | +0.0000 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 16.0% | Up | +0.0081 |
| Basic Materials | 17.4% | Down | -0.0150 |


### 4. Momentum

- **Raw Slope:** +0.0037
- **Smoothed Slope (EMA(3)):** +0.0035 (score: 62/100)
- **Acceleration (10v10):** 0.004361 (accelerating, score: 75/100)
- **Sector Slope Breadth:** 8/11 positive (score: 73/100)

### 5. Historical Context

- **Current Ratio:** 32.3%
- **Percentile Rank:** 78.4th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.5%
- **30-Day Avg:** 25.2%
- **90-Day Avg:** 23.7%
- **Data Points:** 747 (2023-08-11 to 2026-06-30)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 47.5% | 202/425 | 39.0% | Up | +0.0190 | Overbought |
| 2 | Industrials | 38.2% | 151/395 | 35.2% | Up | +0.0018 | Overbought |
| 3 | Financial | 33.4% | 208/623 | 30.7% | Up | +0.0027 | Normal |
| 4 | Technology | 32.2% | 134/416 | 28.2% | Up | +0.0010 | Normal |
| 5 | Real Estate | 29.4% | 42/143 | 26.8% | Down | +0.0000 | Normal |
| 6 | Consumer Cyclical | 28.0% | 79/282 | 27.9% | Down | -0.0028 | Normal |
| 7 | Communication Services | 26.3% | 30/114 | 19.3% | Up | +0.0034 | Normal |
| 8 | Consumer Defensive | 23.7% | 28/118 | 20.6% | Up | +0.0052 | Normal |
| 9 | Basic Materials | 17.4% | 26/149 | 19.7% | Down | -0.0150 | Normal |
| 10 | Energy | 16.0% | 25/156 | 10.1% | Up | +0.0081 | Normal |
| 11 | Utilities | 13.6% | 11/81 | 9.8% | Up | +0.0037 | Normal |

---

## Recommended Actions

**Zone:** Bull (Bull-Lower)
**Exposure Guidance:** Normal Exposure, Lower End (80-90%)

- Normal position sizing
- New entries on quality setups
- Standard stop-loss levels
- Monitor sector rotation for early warnings

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
