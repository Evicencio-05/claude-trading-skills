# Uptrend Analyzer Report

**Generated:** 2026-06-24 06:24:44
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **56.2/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: -3.8 points from 60 (below)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 59.2/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Momentum (68/100) |
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
| Uptrend Ratio | 26.4% |
| 10-Day MA | 26.8% |
| Trend | up |
| Slope | +0.0045 |
| Distance from 37% (Overbought) | -10.6pp |
| Distance from 9.7% (Oversold) | +16.7pp |
| Date | 2026-06-23 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 48 | 14.4 | NEUTRAL: 26.4% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ███░ 64 | 16.0 | HEALTHY: 7/11 sectors uptrending, spread 30.4% |
| 3 | **Sector Rotation** | 15% | ███░ 63 | 9.4 | BALANCED: Cyclical-Defensive gap 4.7pp |
| 4 | **Momentum** | 20% | ███░ 68 | 13.6 | POSITIVE MOMENTUM: slope=0.0060, accelerating |
| 5 | **Historical Context** | 10% | ██░░ 58 | 5.8 | NEAR MEDIAN: 26.4% at 58.2th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 26.4%
- **10-Day MA:** 26.8%
- **Trend:** up
- **Slope:** +0.0045
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 7/11
- **Count Score:** 60/100
- **Spread:** 30.4% (score: 69/100)
- **Overbought (>37%):** 0 sectors ()
- **Oversold (<9.7%):** 2 sectors (Energy, Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 26.1%
- **Defensive Avg:** 21.4%
- **Commodity Avg:** 10.7%
- **Cyclical-Defensive Gap:** 4.7pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0623, spread=0.1725
    - Outlier: Communication Services (deviation: -0.1083)
    - Trend dissenter: Communication Services (down vs majority up)
  - **Defensive Divergence:** std=0.1141, spread=0.3043
    - Trend dissenter: Utilities (down vs majority up)
    - Trend dissenter: Real Estate (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 24.8% | Up | +0.0028 |
| Consumer Cyclical | 26.1% | Up | +0.0018 |
| Communication Services | 15.3% | Down | -0.0010 |
| Financial | 32.0% | Up | +0.0085 |
| Industrials | 32.6% | Up | +0.0056 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 4.9% | Down | -0.0026 |
| Consumer Defensive | 17.6% | Up | +0.0026 |
| Healthcare | 35.4% | Up | +0.0116 |
| Real Estate | 27.8% | Down | -0.0012 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 8.1% | Down | -0.0050 |
| Basic Materials | 13.3% | Up | +0.0010 |


### 4. Momentum

- **Raw Slope:** +0.0045
- **Smoothed Slope (EMA(3)):** +0.0060 (score: 66/100)
- **Acceleration (10v10):** 0.003406 (accelerating, score: 75/100)
- **Sector Slope Breadth:** 7/11 positive (score: 64/100)

### 5. Historical Context

- **Current Ratio:** 26.4%
- **Percentile Rank:** 58.2th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.5%
- **30-Day Avg:** 23.7%
- **90-Day Avg:** 23.9%
- **Data Points:** 742 (2023-08-11 to 2026-06-23)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 35.4% | 145/410 | 29.7% | Up | +0.0116 | Normal |
| 2 | Industrials | 32.6% | 127/390 | 32.8% | Up | +0.0056 | Normal |
| 3 | Financial | 32.0% | 194/607 | 29.1% | Up | +0.0085 | Normal |
| 4 | Real Estate | 27.8% | 40/144 | 25.5% | Down | -0.0012 | Normal |
| 5 | Consumer Cyclical | 26.1% | 72/276 | 27.7% | Up | +0.0018 | Normal |
| 6 | Technology | 24.8% | 102/411 | 30.3% | Up | +0.0028 | Normal |
| 7 | Consumer Defensive | 17.6% | 21/119 | 19.0% | Up | +0.0026 | Normal |
| 8 | Communication Services | 15.3% | 17/111 | 19.1% | Down | -0.0010 | Normal |
| 9 | Basic Materials | 13.3% | 20/150 | 22.1% | Up | +0.0010 | Normal |
| 10 | Energy | 8.1% | 13/161 | 11.9% | Down | -0.0050 | Oversold |
| 11 | Utilities | 4.9% | 4/81 | 6.3% | Down | -0.0026 | Oversold |

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
