# Uptrend Analyzer Report

**Generated:** 2026-06-10 06:02:50
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **41.9/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: +1.9 points from 40 (above)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 44.9/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (61/100) |
| **Weakest Component** | Market Breadth (Overall) (28/100) |
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
| Uptrend Ratio | 21.9% |
| 10-Day MA | 22.2% |
| Trend | down |
| Slope | -0.0045 |
| Distance from 37% (Overbought) | -15.1pp |
| Distance from 9.7% (Oversold) | +12.2pp |
| Date | 2026-06-09 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 28 | 8.4 | VERY WEAK: 21.9% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ██░░ 47 | 11.8 | MODERATE: 3/11 sectors uptrending, spread 21.5% |
| 3 | **Sector Rotation** | 15% | ███░ 61 | 9.2 | BALANCED: Cyclical-Defensive gap 3.8pp |
| 4 | **Momentum** | 20% | ██░░ 56 | 11.2 | NEUTRAL MOMENTUM: slope=-0.0034, strong accelerating |
| 5 | **Historical Context** | 10% | ██░░ 44 | 4.4 | NEAR MEDIAN: 21.9% at 43.9th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 21.9%
- **10-Day MA:** 22.2%
- **Trend:** down
- **Slope:** -0.0045
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 3/11
- **Count Score:** 20/100
- **Spread:** 21.5% (score: 87/100)
- **Overbought (>37%):** 0 sectors ()
- **Oversold (<9.7%):** 1 sectors (Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 22.6%
- **Defensive Avg:** 18.8%
- **Commodity Avg:** 12.7%
- **Cyclical-Defensive Gap:** 3.8pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0352, spread=0.1063
    - Outlier: Communication Services (deviation: -0.0625)
    - Trend dissenter: Consumer Cyclical (up vs majority down)
  - **Defensive Divergence:** std=0.0822, spread=0.2147
    - Trend dissenter: Utilities (down vs majority up)
    - Trend dissenter: Healthcare (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 22.0% | Down | -0.0179 |
| Consumer Cyclical | 24.3% | Up | +0.0051 |
| Communication Services | 16.4% | Down | -0.0071 |
| Financial | 23.5% | Down | -0.0003 |
| Industrials | 27.0% | Down | -0.0032 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 7.5% | Down | -0.0073 |
| Consumer Defensive | 15.0% | Up | +0.0028 |
| Healthcare | 23.8% | Down | -0.0005 |
| Real Estate | 29.0% | Up | +0.0038 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 13.0% | Down | -0.0142 |
| Basic Materials | 12.3% | Down | -0.0148 |


### 4. Momentum

- **Raw Slope:** -0.0045
- **Smoothed Slope (EMA(3)):** -0.0034 (score: 48/100)
- **Acceleration (10v10):** 0.005067 (strong_accelerating, score: 90/100)
- **Sector Slope Breadth:** 3/11 positive (score: 27/100)

### 5. Historical Context

- **Current Ratio:** 21.9%
- **Percentile Rank:** 43.9th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 23.6%
- **90-Day Avg:** 24.4%
- **Data Points:** 732 (2023-08-11 to 2026-06-09)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Real Estate | 29.0% | 42/145 | 20.6% | Up | +0.0038 | Normal |
| 2 | Industrials | 27.0% | 105/389 | 27.3% | Down | -0.0032 | Normal |
| 3 | Consumer Cyclical | 24.3% | 67/276 | 20.8% | Up | +0.0051 | Normal |
| 4 | Healthcare | 23.8% | 95/399 | 20.1% | Down | -0.0005 | Normal |
| 5 | Financial | 23.5% | 140/597 | 17.5% | Down | -0.0003 | Normal |
| 6 | Technology | 22.0% | 89/405 | 34.9% | Down | -0.0179 | Normal |
| 7 | Communication Services | 16.4% | 18/110 | 20.4% | Down | -0.0071 | Normal |
| 8 | Consumer Defensive | 15.0% | 18/120 | 13.5% | Up | +0.0028 | Normal |
| 9 | Energy | 13.0% | 21/161 | 15.8% | Down | -0.0142 | Normal |
| 10 | Basic Materials | 12.3% | 19/154 | 22.2% | Down | -0.0148 | Normal |
| 11 | Utilities | 7.5% | 6/80 | 11.2% | Down | -0.0073 | Oversold |

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
