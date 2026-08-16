# Uptrend Analyzer Report

**Generated:** 2026-07-13 06:00:56
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **35.9/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Upper |
| **Zone Proximity** | **Near boundary: -4.1 points from 40 (below)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -3 (raw: 38.9/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (60/100) |
| **Weakest Component** | Sector Participation (33/100) |
| **Data Quality** | Complete (5/5 components) |
| **Confidence** | High (moderate, Both regime coverage) |

> **Guidance:** Weak breadth environment. Prioritize capital preservation over gains.

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
| Uptrend Ratio | 26.9% |
| 10-Day MA | 28.4% |
| Trend | down |
| Slope | -0.0036 |
| Distance from 37% (Overbought) | -10.2pp |
| Distance from 9.7% (Oversold) | +17.2pp |
| Date | 2026-07-10 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 39 | 11.7 | WEAK: 26.9% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | █░░░ 33 | 8.2 | NARROW: 2/11 sectors uptrending, spread 37.3% |
| 3 | **Sector Rotation** | 15% | █░░░ 38 | 5.7 | DEFENSIVE TILT: Defensive leads by 5.6pp |
| 4 | **Momentum** | 20% | █░░░ 36 | 7.2 | WEAK MOMENTUM: slope=-0.0028, decelerating |
| 5 | **Historical Context** | 10% | ███░ 60 | 6.0 | SLIGHTLY ABOVE: 26.9% at 59.5th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 26.9%
- **10-Day MA:** 28.4%
- **Trend:** down
- **Slope:** -0.0036
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 2/11
- **Count Score:** 20/100
- **Spread:** 37.3% (score: 53/100)
- **Overbought (>37%):** 1 sectors (Healthcare)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 22.6%
- **Defensive Avg:** 28.2%
- **Commodity Avg:** 18.9%
- **Cyclical-Defensive Gap:** -5.6pp
- **Divergence Warning:** YES (penalty: -5)
  - **Defensive Divergence:** std=0.1169, spread=0.3148
    - Outlier: Healthcare (deviation: +0.1929)
    - Trend dissenter: Healthcare (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 20.3% | Down | -0.0001 |
| Consumer Cyclical | 18.6% | Down | -0.0112 |
| Communication Services | 23.2% | Down | -0.0013 |
| Financial | 33.4% | Down | -0.0003 |
| Industrials | 17.7% | Down | -0.0153 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 16.0% | Down | -0.0037 |
| Consumer Defensive | 24.4% | Down | -0.0011 |
| Healthcare | 47.5% | Up | +0.0017 |
| Real Estate | 25.0% | Down | -0.0113 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 27.6% | Up | +0.0130 |
| Basic Materials | 10.2% | Down | -0.0102 |


### 4. Momentum

- **Raw Slope:** -0.0036
- **Smoothed Slope (EMA(3)):** -0.0028 (score: 49/100)
- **Acceleration (10v10):** -0.003935 (decelerating, score: 25/100)
- **Sector Slope Breadth:** 2/11 positive (score: 18/100)

### 5. Historical Context

- **Current Ratio:** 26.9%
- **Percentile Rank:** 59.5th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.7%
- **30-Day Avg:** 26.3%
- **90-Day Avg:** 23.4%
- **Data Points:** 755 (2023-08-11 to 2026-07-10)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 47.5% | 202/425 | 49.6% | Up | +0.0017 | Overbought |
| 2 | Financial | 33.4% | 210/629 | 33.3% | Down | -0.0003 | Normal |
| 3 | Energy | 27.6% | 43/156 | 18.4% | Up | +0.0130 | Normal |
| 4 | Real Estate | 25.0% | 36/144 | 29.9% | Down | -0.0113 | Normal |
| 5 | Consumer Defensive | 24.4% | 29/119 | 23.7% | Down | -0.0011 | Normal |
| 6 | Communication Services | 23.2% | 26/112 | 25.2% | Down | -0.0013 | Normal |
| 7 | Technology | 20.3% | 86/424 | 19.5% | Down | -0.0001 | Normal |
| 8 | Consumer Cyclical | 18.6% | 52/279 | 22.2% | Down | -0.0112 | Normal |
| 9 | Industrials | 17.7% | 70/396 | 25.9% | Down | -0.0153 | Normal |
| 10 | Utilities | 16.0% | 13/81 | 13.7% | Down | -0.0037 | Normal |
| 11 | Basic Materials | 10.2% | 15/147 | 13.8% | Down | -0.0102 | Normal |

---

## Recommended Actions

**Zone:** Cautious (Cautious-Upper)
**Exposure Guidance:** Defensive (30-60%)

- Significant cash allocation (40-70%)
- Only hold strongest leaders in uptrending sectors
- Tight stops on all positions
- Consider defensive sector allocation
- No new aggressive entries

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
