# Uptrend Analyzer Report

**Generated:** 2026-06-17 06:00:39
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **60.2/100** |
| **Zone** | 🟢 Bull |
| **Zone Detail** | Bull-Lower |
| **Zone Proximity** | **Near boundary: +0.2 points from 60 (above)** |
| **Exposure Guidance** | Normal Exposure, Lower End (80-90%) |
| **Warning Penalty** | -3 (raw: 63.2/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (72/100) |
| **Weakest Component** | Market Breadth (Overall) (54/100) |
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
| Uptrend Ratio | 28.6% |
| 10-Day MA | 23.8% |
| Trend | up |
| Slope | +0.0051 |
| Distance from 37% (Overbought) | -8.4pp |
| Distance from 9.7% (Oversold) | +18.9pp |
| Date | 2026-06-16 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 54 | 16.2 | NEUTRAL: 28.6% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ███░ 65 | 16.2 | HEALTHY: 7/11 sectors uptrending, spread 28.5% |
| 3 | **Sector Rotation** | 15% | ███░ 72 | 10.8 | RISK-ON: Cyclical leads by 8.9pp |
| 4 | **Momentum** | 20% | ███░ 67 | 13.4 | POSITIVE MOMENTUM: slope=0.0049, accelerating |
| 5 | **Historical Context** | 10% | ███░ 66 | 6.6 | SLIGHTLY ABOVE: 28.6% at 66.1th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 28.6%
- **10-Day MA:** 23.8%
- **Trend:** up
- **Slope:** +0.0051
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 7/11
- **Count Score:** 60/100
- **Spread:** 28.5% (score: 73/100)
- **Overbought (>37%):** 0 sectors ()
- **Oversold (<9.7%):** 1 sectors (Energy)

### 3. Sector Rotation

- **Cyclical Avg:** 30.4%
- **Defensive Avg:** 21.6%
- **Commodity Avg:** 20.2%
- **Cyclical-Defensive Gap:** 8.9pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0431, spread=0.135
    - Outlier: Communication Services (deviation: -0.0749)
    - Trend dissenter: Technology (down vs majority up)
    - Trend dissenter: Communication Services (down vs majority up)
  - **Defensive Divergence:** std=0.0799, spread=0.1949
    - Trend dissenter: Utilities (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 31.2% | Down | -0.0110 |
| Consumer Cyclical | 30.8% | Up | +0.0102 |
| Communication Services | 22.9% | Down | -0.0001 |
| Financial | 30.7% | Up | +0.0125 |
| Industrials | 36.4% | Up | +0.0069 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 9.9% | Down | -0.0049 |
| Consumer Defensive | 18.5% | Up | +0.0063 |
| Healthcare | 28.5% | Up | +0.0153 |
| Real Estate | 29.4% | Up | +0.0116 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 8.0% | Down | -0.0138 |
| Basic Materials | 32.5% | Up | +0.0027 |


### 4. Momentum

- **Raw Slope:** +0.0051
- **Smoothed Slope (EMA(3)):** +0.0049 (score: 64/100)
- **Acceleration (10v10):** 0.002074 (accelerating, score: 75/100)
- **Sector Slope Breadth:** 7/11 positive (score: 64/100)

### 5. Historical Context

- **Current Ratio:** 28.6%
- **Percentile Rank:** 66.1th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 23.6%
- **90-Day Avg:** 24.2%
- **Data Points:** 737 (2023-08-11 to 2026-06-16)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Industrials | 36.4% | 141/387 | 28.1% | Up | +0.0069 | Normal |
| 2 | Basic Materials | 32.5% | 50/154 | 19.2% | Up | +0.0027 | Normal |
| 3 | Technology | 31.2% | 128/410 | 30.1% | Down | -0.0110 | Normal |
| 4 | Consumer Cyclical | 30.8% | 85/276 | 24.7% | Up | +0.0102 | Normal |
| 5 | Financial | 30.7% | 184/599 | 23.7% | Up | +0.0125 | Normal |
| 6 | Real Estate | 29.4% | 42/143 | 25.3% | Up | +0.0116 | Normal |
| 7 | Healthcare | 28.5% | 114/400 | 22.8% | Up | +0.0153 | Normal |
| 8 | Communication Services | 22.9% | 25/109 | 19.8% | Down | -0.0001 | Normal |
| 9 | Consumer Defensive | 18.5% | 22/119 | 17.2% | Up | +0.0063 | Normal |
| 10 | Utilities | 9.9% | 8/81 | 8.6% | Down | -0.0049 | Normal |
| 11 | Energy | 8.0% | 13/163 | 17.2% | Down | -0.0138 | Oversold |

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
