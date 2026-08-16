# Uptrend Analyzer Report

**Generated:** 2026-06-30 06:15:10
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **62.5/100** |
| **Zone** | 🟢 Bull |
| **Zone Detail** | Bull-Lower |
| **Zone Proximity** | **Near boundary: +2.5 points from 60 (above)** |
| **Exposure Guidance** | Normal Exposure, Lower End (80-90%) |
| **Warning Penalty** | -3 (raw: 65.5/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (77/100) |
| **Weakest Component** | Sector Rotation (49/100) |
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
| Uptrend Ratio | 31.5% |
| 10-Day MA | 28.2% |
| Trend | up |
| Slope | +0.0035 |
| Distance from 37% (Overbought) | -5.5pp |
| Distance from 9.7% (Oversold) | +21.8pp |
| Date | 2026-06-29 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ███░ 61 | 18.3 | NEUTRAL: 31.5% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ███░ 74 | 18.5 | HEALTHY: 8/11 sectors uptrending, spread 32.8% |
| 3 | **Sector Rotation** | 15% | ██░░ 49 | 7.3 | BALANCED: Cyclical-Defensive gap -1.4pp |
| 4 | **Momentum** | 20% | ███░ 68 | 13.6 | POSITIVE MOMENTUM: slope=0.0032, accelerating |
| 5 | **Historical Context** | 10% | ███░ 77 | 7.7 | SLIGHTLY ABOVE: 31.5% at 76.6th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 31.5%
- **10-Day MA:** 28.2%
- **Trend:** up
- **Slope:** +0.0035
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 8/11
- **Count Score:** 80/100
- **Spread:** 32.8% (score: 64/100)
- **Overbought (>37%):** 1 sectors (Healthcare)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 30.3%
- **Defensive Avg:** 31.7%
- **Commodity Avg:** 15.9%
- **Cyclical-Defensive Gap:** -1.4pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0328, spread=0.0872
    - Trend dissenter: Technology (down vs majority up)
    - Trend dissenter: Consumer Cyclical (down vs majority up)
  - **Defensive Divergence:** std=0.1141, spread=0.3023

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 26.4% | Down | -0.0089 |
| Consumer Cyclical | 28.9% | Down | -0.0005 |
| Communication Services | 27.8% | Up | +0.0067 |
| Financial | 33.0% | Up | +0.0033 |
| Industrials | 35.1% | Up | +0.0018 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 17.3% | Up | +0.0086 |
| Consumer Defensive | 25.4% | Up | +0.0061 |
| Healthcare | 47.5% | Up | +0.0194 |
| Real Estate | 36.6% | Up | +0.0086 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 17.1% | Up | +0.0074 |
| Basic Materials | 14.8% | Down | -0.0123 |


### 4. Momentum

- **Raw Slope:** +0.0035
- **Smoothed Slope (EMA(3)):** +0.0032 (score: 61/100)
- **Acceleration (10v10):** 0.004597 (accelerating, score: 75/100)
- **Sector Slope Breadth:** 8/11 positive (score: 73/100)

### 5. Historical Context

- **Current Ratio:** 31.5%
- **Percentile Rank:** 76.6th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.5%
- **30-Day Avg:** 24.7%
- **90-Day Avg:** 23.7%
- **Data Points:** 746 (2023-08-11 to 2026-06-29)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 47.5% | 201/423 | 37.1% | Up | +0.0194 | Overbought |
| 2 | Real Estate | 36.6% | 53/145 | 26.8% | Up | +0.0086 | Normal |
| 3 | Industrials | 35.1% | 138/393 | 35.0% | Up | +0.0018 | Normal |
| 4 | Financial | 33.0% | 206/624 | 30.5% | Up | +0.0033 | Normal |
| 5 | Consumer Cyclical | 28.9% | 81/280 | 28.2% | Down | -0.0005 | Normal |
| 6 | Communication Services | 27.8% | 32/115 | 19.0% | Up | +0.0067 | Normal |
| 7 | Technology | 26.4% | 109/413 | 28.1% | Down | -0.0089 | Normal |
| 8 | Consumer Defensive | 25.4% | 30/118 | 20.1% | Up | +0.0061 | Normal |
| 9 | Utilities | 17.3% | 14/81 | 9.4% | Up | +0.0086 | Normal |
| 10 | Energy | 17.1% | 27/158 | 9.3% | Up | +0.0074 | Normal |
| 11 | Basic Materials | 14.8% | 22/149 | 21.2% | Down | -0.0123 | Normal |

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
