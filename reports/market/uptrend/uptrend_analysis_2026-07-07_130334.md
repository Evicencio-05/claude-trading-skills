# Uptrend Analyzer Report

**Generated:** 2026-07-07 13:03:34
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **50.7/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: -9.3 points from 60 (below)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -5 (raw: 55.7/100) |
| **Active Warnings** | 2: HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (70/100) |
| **Weakest Component** | Sector Rotation (45/100) |
| **Data Quality** | Complete (5/5 components) |
| **Confidence** | High (moderate, Both regime coverage) |

> **Guidance:** Mixed signals. Participate selectively with tighter risk controls.

---

## Active Warnings

### HIGH SELECTIVITY WARNING
> Wide spread between strongest and weakest sectors indicates highly selective market. Breadth may be masking narrowing leadership.

- Concentrate on sectors with ratio above 10MA
- Avoid lagging sectors even if trend is nominally 'up'
- Reduce position count to highest-conviction ideas

### SECTOR DIVERGENCE WARNING
> Significant divergence detected within sector groups. Some sectors within the same group are moving in opposite directions, suggesting hidden risk beneath the averages.

- Verify individual sector trends before entering positions
- Avoid sectors diverging from their group majority
- Monitor for group convergence or further deterioration

---

## Current Market Snapshot

| Metric | Value |
|--------|-------|
| Uptrend Ratio | 29.8% |
| 10-Day MA | 29.4% |
| Trend | up |
| Slope | +0.0015 |
| Distance from 37% (Overbought) | -7.2pp |
| Distance from 9.7% (Oversold) | +20.1pp |
| Date | 2026-07-06 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 57 | 17.1 | NEUTRAL: 29.8% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ██░░ 54 | 13.5 | MODERATE: 7/11 sectors uptrending, spread 40.0% |
| 3 | **Sector Rotation** | 15% | ██░░ 45 | 6.8 | BALANCED: Cyclical-Defensive gap -3.0pp |
| 4 | **Momentum** | 20% | ██░░ 57 | 11.4 | NEUTRAL MOMENTUM: slope=0.0016, steady |
| 5 | **Historical Context** | 10% | ███░ 70 | 7.0 | SLIGHTLY ABOVE: 29.8% at 69.7th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 29.8%
- **10-Day MA:** 29.4%
- **Trend:** up
- **Slope:** +0.0015
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 7/11
- **Count Score:** 60/100
- **Spread:** 40.0% (score: 45/100)
- **Overbought (>37%):** 2 sectors (Healthcare, Financial)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 26.7%
- **Defensive Avg:** 29.7%
- **Commodity Avg:** 14.8%
- **Cyclical-Defensive Gap:** -3.0pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0667, spread=0.1969
    - Outlier: Financial (deviation: +0.1100)
    - Trend dissenter: Communication Services (up vs majority down)
    - Trend dissenter: Financial (up vs majority down)
  - **Defensive Divergence:** std=0.1453, spread=0.4005

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 18.0% | Down | -0.0157 |
| Consumer Cyclical | 22.2% | Down | -0.0046 |
| Communication Services | 26.3% | Up | +0.0107 |
| Financial | 37.7% | Up | +0.0069 |
| Industrials | 29.2% | Down | -0.0085 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 11.1% | Up | +0.0049 |
| Consumer Defensive | 24.2% | Up | +0.0071 |
| Healthcare | 51.2% | Up | +0.0162 |
| Real Estate | 32.4% | Up | +0.0100 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 14.1% | Up | +0.0067 |
| Basic Materials | 15.4% | Down | -0.0073 |


### 4. Momentum

- **Raw Slope:** +0.0015
- **Smoothed Slope (EMA(3)):** +0.0016 (score: 58/100)
- **Acceleration (10v10):** 0.000928 (steady, score: 50/100)
- **Sector Slope Breadth:** 7/11 positive (score: 64/100)

### 5. Historical Context

- **Current Ratio:** 29.8%
- **Percentile Rank:** 69.7th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.6%
- **30-Day Avg:** 26.1%
- **90-Day Avg:** 23.6%
- **Data Points:** 751 (2023-08-11 to 2026-07-06)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 51.2% | 221/432 | 46.1% | Up | +0.0162 | Overbought |
| 2 | Financial | 37.7% | 235/624 | 33.7% | Up | +0.0069 | Overbought |
| 3 | Real Estate | 32.4% | 47/145 | 31.6% | Up | +0.0100 | Normal |
| 4 | Industrials | 29.2% | 114/391 | 31.9% | Down | -0.0085 | Normal |
| 5 | Communication Services | 26.3% | 30/114 | 23.3% | Up | +0.0107 | Normal |
| 6 | Consumer Defensive | 24.2% | 29/120 | 23.8% | Up | +0.0071 | Normal |
| 7 | Consumer Cyclical | 22.2% | 62/279 | 26.5% | Down | -0.0046 | Normal |
| 8 | Technology | 18.0% | 76/423 | 21.9% | Down | -0.0157 | Normal |
| 9 | Basic Materials | 15.4% | 23/149 | 16.7% | Down | -0.0073 | Normal |
| 10 | Energy | 14.1% | 22/156 | 12.7% | Up | +0.0067 | Normal |
| 11 | Utilities | 11.1% | 9/81 | 13.2% | Up | +0.0049 | Normal |

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
