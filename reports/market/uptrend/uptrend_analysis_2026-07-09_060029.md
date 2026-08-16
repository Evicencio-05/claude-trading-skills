# Uptrend Analyzer Report

**Generated:** 2026-07-09 06:00:29
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **31.8/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Upper |
| **Zone Proximity** | **Near boundary: -8.2 points from 40 (below)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -5 (raw: 36.8/100) |
| **Active Warnings** | 2: HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (48/100) |
| **Weakest Component** | Market Breadth (Overall) (31/100) |
| **Data Quality** | Complete (5/5 components) |
| **Confidence** | High (moderate, Both regime coverage) |

> **Guidance:** Weak breadth environment. Prioritize capital preservation over gains.

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
| Uptrend Ratio | 23.2% |
| 10-Day MA | 29.0% |
| Trend | down |
| Slope | -0.0041 |
| Distance from 37% (Overbought) | -13.8pp |
| Distance from 9.7% (Oversold) | +13.5pp |
| Date | 2026-07-08 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 31 | 9.3 | WEAK: 23.2% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | █░░░ 39 | 9.8 | NARROW: 4/11 sectors uptrending, spread 42.4% |
| 3 | **Sector Rotation** | 15% | █░░░ 33 | 5.0 | DEFENSIVE TILT: Defensive leads by 7.4pp |
| 4 | **Momentum** | 20% | ██░░ 40 | 8.0 | NEUTRAL MOMENTUM: slope=-0.0015, decelerating |
| 5 | **Historical Context** | 10% | ██░░ 48 | 4.8 | NEAR MEDIAN: 23.2% at 48.4th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 23.2%
- **10-Day MA:** 29.0%
- **Trend:** down
- **Slope:** -0.0041
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 4/11
- **Count Score:** 40/100
- **Spread:** 42.4% (score: 38/100)
- **Overbought (>37%):** 1 sectors (Healthcare)
- **Oversold (<9.7%):** 1 sectors (Basic Materials)

### 3. Sector Rotation

- **Cyclical Avg:** 18.7%
- **Defensive Avg:** 26.1%
- **Commodity Avg:** 17.7%
- **Cyclical-Defensive Gap:** -7.4pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.045, spread=0.1111
    - Trend dissenter: Communication Services (up vs majority down)
  - **Defensive Divergence:** std=0.1441, spread=0.3877
    - Outlier: Healthcare (deviation: +0.2378)
    - Trend dissenter: Utilities (down vs majority up)
    - Trend dissenter: Real Estate (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 14.8% | Down | -0.0083 |
| Consumer Cyclical | 13.7% | Down | -0.0156 |
| Communication Services | 24.8% | Up | +0.0069 |
| Financial | 23.3% | Down | -0.0070 |
| Industrials | 17.1% | Down | -0.0161 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 11.1% | Down | +0.0000 |
| Consumer Defensive | 20.7% | Up | +0.0012 |
| Healthcare | 49.9% | Up | +0.0096 |
| Real Estate | 22.8% | Down | -0.0060 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 27.9% | Up | +0.0229 |
| Basic Materials | 7.5% | Down | -0.0100 |


### 4. Momentum

- **Raw Slope:** -0.0041
- **Smoothed Slope (EMA(3)):** -0.0015 (score: 51/100)
- **Acceleration (10v10):** -0.00222 (decelerating, score: 25/100)
- **Sector Slope Breadth:** 4/11 positive (score: 36/100)

### 5. Historical Context

- **Current Ratio:** 23.2%
- **Percentile Rank:** 48.4th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.6%
- **30-Day Avg:** 26.1%
- **90-Day Avg:** 23.4%
- **Data Points:** 753 (2023-08-11 to 2026-07-08)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 49.9% | 213/427 | 48.5% | Up | +0.0096 | Overbought |
| 2 | Energy | 27.9% | 43/154 | 15.9% | Up | +0.0229 | Normal |
| 3 | Communication Services | 24.8% | 28/113 | 24.9% | Up | +0.0069 | Normal |
| 4 | Financial | 23.3% | 146/627 | 33.3% | Down | -0.0070 | Normal |
| 5 | Real Estate | 22.8% | 33/145 | 31.4% | Down | -0.0060 | Normal |
| 6 | Consumer Defensive | 20.7% | 25/121 | 24.4% | Up | +0.0012 | Normal |
| 7 | Industrials | 17.1% | 67/391 | 29.1% | Down | -0.0161 | Normal |
| 8 | Technology | 14.8% | 62/420 | 19.8% | Down | -0.0083 | Normal |
| 9 | Consumer Cyclical | 13.7% | 38/278 | 24.5% | Down | -0.0156 | Normal |
| 10 | Utilities | 11.1% | 9/81 | 14.2% | Down | +0.0000 | Normal |
| 11 | Basic Materials | 7.5% | 11/147 | 15.6% | Down | -0.0100 | Oversold |

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
