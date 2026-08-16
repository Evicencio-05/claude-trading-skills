# Uptrend Analyzer Report

**Generated:** 2026-06-25 06:08:04
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **58.9/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: -1.1 points from 60 (below)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 61.9/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Participation (72/100) |
| **Weakest Component** | Market Breadth (Overall) (51/100) |
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
| Uptrend Ratio | 27.4% |
| 10-Day MA | 27.4% |
| Trend | up |
| Slope | +0.0063 |
| Distance from 37% (Overbought) | -9.6pp |
| Distance from 9.7% (Oversold) | +17.7pp |
| Date | 2026-06-24 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 51 | 15.3 | NEUTRAL: 27.4% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ███░ 72 | 18.0 | HEALTHY: 8/11 sectors uptrending, spread 35.3% |
| 3 | **Sector Rotation** | 15% | ██░░ 56 | 8.4 | BALANCED: Cyclical-Defensive gap 1.8pp |
| 4 | **Momentum** | 20% | ███░ 70 | 14.0 | POSITIVE MOMENTUM: slope=0.0062, accelerating |
| 5 | **Historical Context** | 10% | ███░ 62 | 6.2 | SLIGHTLY ABOVE: 27.4% at 62.2th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 27.4%
- **10-Day MA:** 27.4%
- **Trend:** up
- **Slope:** +0.0063
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 8/11
- **Count Score:** 80/100
- **Spread:** 35.3% (score: 59/100)
- **Overbought (>37%):** 1 sectors (Healthcare)
- **Oversold (<9.7%):** 1 sectors (Energy)

### 3. Sector Rotation

- **Cyclical Avg:** 26.7%
- **Defensive Avg:** 24.9%
- **Commodity Avg:** 11.2%
- **Cyclical-Defensive Gap:** 1.8pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0555, spread=0.1539
    - Outlier: Communication Services (deviation: -0.0888)
    - Trend dissenter: Communication Services (down vs majority up)
  - **Defensive Divergence:** std=0.1085, spread=0.2918
    - Trend dissenter: Consumer Defensive (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 23.0% | Up | +0.0060 |
| Consumer Cyclical | 29.2% | Up | +0.0050 |
| Communication Services | 17.9% | Down | -0.0029 |
| Financial | 30.3% | Up | +0.0055 |
| Industrials | 33.2% | Up | +0.0144 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 11.1% | Up | +0.0049 |
| Consumer Defensive | 19.5% | Down | -0.0005 |
| Healthcare | 40.3% | Up | +0.0190 |
| Real Estate | 28.8% | Up | +0.0015 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 5.0% | Down | -0.0217 |
| Basic Materials | 17.4% | Up | +0.0048 |


### 4. Momentum

- **Raw Slope:** +0.0063
- **Smoothed Slope (EMA(3)):** +0.0062 (score: 67/100)
- **Acceleration (10v10):** 0.004697 (accelerating, score: 75/100)
- **Sector Slope Breadth:** 8/11 positive (score: 73/100)

### 5. Historical Context

- **Current Ratio:** 27.4%
- **Percentile Rank:** 62.2th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.5%
- **30-Day Avg:** 23.8%
- **90-Day Avg:** 23.8%
- **Data Points:** 743 (2023-08-11 to 2026-06-24)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 40.3% | 166/412 | 31.7% | Up | +0.0190 | Overbought |
| 2 | Industrials | 33.2% | 129/388 | 34.2% | Up | +0.0144 | Normal |
| 3 | Financial | 30.3% | 183/604 | 29.7% | Up | +0.0055 | Normal |
| 4 | Consumer Cyclical | 29.2% | 81/277 | 28.2% | Up | +0.0050 | Normal |
| 5 | Real Estate | 28.8% | 42/146 | 25.6% | Up | +0.0015 | Normal |
| 6 | Technology | 23.0% | 94/408 | 30.9% | Up | +0.0060 | Normal |
| 7 | Consumer Defensive | 19.5% | 23/118 | 19.0% | Down | -0.0005 | Normal |
| 8 | Communication Services | 17.9% | 20/112 | 18.8% | Down | -0.0029 | Normal |
| 9 | Basic Materials | 17.4% | 26/149 | 22.6% | Up | +0.0048 | Normal |
| 10 | Utilities | 11.1% | 9/81 | 6.8% | Up | +0.0049 | Normal |
| 11 | Energy | 5.0% | 8/160 | 9.8% | Down | -0.0217 | Oversold |

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
