# Uptrend Analyzer Report

**Generated:** 2026-06-11 10:57:56
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **43.5/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: +3.5 points from 40 (above)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -3 (raw: 46.5/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Participation (59/100) |
| **Weakest Component** | Market Breadth (Overall) (26/100) |
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
| 10-Day MA | 21.8% |
| Trend | down |
| Slope | -0.0034 |
| Distance from 37% (Overbought) | -16.0pp |
| Distance from 9.7% (Oversold) | +11.3pp |
| Date | 2026-06-10 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 26 | 7.8 | VERY WEAK: 21.0% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ██░░ 59 | 14.8 | MODERATE: 5/11 sectors uptrending, spread 21.0% |
| 3 | **Sector Rotation** | 15% | ██░░ 58 | 8.7 | BALANCED: Cyclical-Defensive gap 2.4pp |
| 4 | **Momentum** | 20% | ██░░ 55 | 11.0 | NEUTRAL MOMENTUM: slope=-0.0034, accelerating |
| 5 | **Historical Context** | 10% | ██░░ 42 | 4.2 | NEAR MEDIAN: 21.0% at 42.1th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 21.0%
- **10-Day MA:** 21.8%
- **Trend:** down
- **Slope:** -0.0034
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 5/11
- **Count Score:** 40/100
- **Spread:** 21.0% (score: 88/100)
- **Overbought (>37%):** 0 sectors ()
- **Oversold (<9.7%):** 1 sectors (Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 21.1%
- **Defensive Avg:** 18.7%
- **Commodity Avg:** 19.7%
- **Cyclical-Defensive Gap:** 2.4pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0302, spread=0.078
    - Trend dissenter: Consumer Cyclical (up vs majority down)
    - Trend dissenter: Financial (up vs majority down)
  - **Defensive Divergence:** std=0.0769, spread=0.2102
    - Outlier: Utilities (deviation: -0.1244)
    - Trend dissenter: Utilities (down vs majority up)
    - Trend dissenter: Healthcare (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 17.0% | Down | -0.0226 |
| Consumer Cyclical | 24.3% | Up | +0.0036 |
| Communication Services | 20.7% | Down | -0.0029 |
| Financial | 24.8% | Up | +0.0067 |
| Industrials | 18.9% | Down | -0.0119 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 6.2% | Down | -0.0073 |
| Consumer Defensive | 20.0% | Up | +0.0038 |
| Healthcare | 21.2% | Down | -0.0023 |
| Real Estate | 27.3% | Up | +0.0028 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 26.7% | Up | +0.0134 |
| Basic Materials | 12.7% | Down | -0.0125 |


### 4. Momentum

- **Raw Slope:** -0.0034
- **Smoothed Slope (EMA(3)):** -0.0034 (score: 48/100)
- **Acceleration (10v10):** 0.004458 (accelerating, score: 75/100)
- **Sector Slope Breadth:** 5/11 positive (score: 45/100)

### 5. Historical Context

- **Current Ratio:** 21.0%
- **Percentile Rank:** 42.1th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 23.5%
- **90-Day Avg:** 24.3%
- **Data Points:** 733 (2023-08-11 to 2026-06-10)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Real Estate | 27.3% | 39/143 | 20.8% | Up | +0.0028 | Normal |
| 2 | Energy | 26.7% | 43/161 | 17.2% | Up | +0.0134 | Normal |
| 3 | Financial | 24.8% | 148/597 | 18.2% | Up | +0.0067 | Normal |
| 4 | Consumer Cyclical | 24.3% | 67/276 | 21.2% | Up | +0.0036 | Normal |
| 5 | Healthcare | 21.2% | 85/400 | 19.9% | Down | -0.0023 | Normal |
| 6 | Communication Services | 20.7% | 23/111 | 20.1% | Down | -0.0029 | Normal |
| 7 | Consumer Defensive | 20.0% | 24/120 | 13.9% | Up | +0.0038 | Normal |
| 8 | Industrials | 18.9% | 73/387 | 26.1% | Down | -0.0119 | Normal |
| 9 | Technology | 17.0% | 69/406 | 32.6% | Down | -0.0226 | Normal |
| 10 | Basic Materials | 12.7% | 19/150 | 20.9% | Down | -0.0125 | Normal |
| 11 | Utilities | 6.2% | 5/80 | 10.5% | Down | -0.0073 | Oversold |

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
