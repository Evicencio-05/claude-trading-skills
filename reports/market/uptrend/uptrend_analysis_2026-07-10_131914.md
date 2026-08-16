# Uptrend Analyzer Report

**Generated:** 2026-07-10 13:19:14
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **37.0/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Upper |
| **Zone Proximity** | **Near boundary: -3.0 points from 40 (below)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -5 (raw: 42.0/100) |
| **Active Warnings** | 2: HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (57/100) |
| **Weakest Component** | Market Breadth (Overall) (38/100) |
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
| Uptrend Ratio | 26.3% |
| 10-Day MA | 28.8% |
| Trend | down |
| Slope | -0.0024 |
| Distance from 37% (Overbought) | -10.7pp |
| Distance from 9.7% (Oversold) | +16.6pp |
| Date | 2026-07-09 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 38 | 11.4 | WEAK: 26.3% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ██░░ 41 | 10.2 | MODERATE: 4/11 sectors uptrending, spread 40.7% |
| 3 | **Sector Rotation** | 15% | ██░░ 44 | 6.6 | DEFENSIVE TILT: Defensive leads by 3.2pp |
| 4 | **Momentum** | 20% | ██░░ 40 | 8.0 | NEUTRAL MOMENTUM: slope=-0.0020, decelerating |
| 5 | **Historical Context** | 10% | ██░░ 57 | 5.7 | NEAR MEDIAN: 26.3% at 57.0th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 26.3%
- **10-Day MA:** 28.8%
- **Trend:** down
- **Slope:** -0.0024
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 4/11
- **Count Score:** 40/100
- **Spread:** 40.7% (score: 43/100)
- **Overbought (>37%):** 1 sectors (Healthcare)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 22.3%
- **Defensive Avg:** 25.5%
- **Commodity Avg:** 17.3%
- **Cyclical-Defensive Gap:** -3.2pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0539, spread=0.1606
    - Outlier: Financial (deviation: +0.0917)
    - Trend dissenter: Communication Services (up vs majority down)
    - Trend dissenter: Financial (up vs majority down)
  - **Defensive Divergence:** std=0.1534, spread=0.4071
    - Outlier: Healthcare (deviation: +0.2510)
    - Trend dissenter: Healthcare (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 21.3% | Down | -0.0026 |
| Consumer Cyclical | 15.4% | Down | -0.0124 |
| Communication Services | 24.1% | Up | +0.0043 |
| Financial | 31.5% | Up | +0.0006 |
| Industrials | 19.2% | Down | -0.0166 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 9.9% | Down | -0.0012 |
| Consumer Defensive | 17.4% | Down | -0.0055 |
| Healthcare | 50.6% | Up | +0.0087 |
| Real Estate | 24.1% | Down | -0.0046 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 23.7% | Up | +0.0118 |
| Basic Materials | 10.9% | Down | -0.0079 |


### 4. Momentum

- **Raw Slope:** -0.0024
- **Smoothed Slope (EMA(3)):** -0.0020 (score: 50/100)
- **Acceleration (10v10):** -0.003301 (decelerating, score: 25/100)
- **Sector Slope Breadth:** 4/11 positive (score: 36/100)

### 5. Historical Context

- **Current Ratio:** 26.3%
- **Percentile Rank:** 57.0th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.7%
- **30-Day Avg:** 26.2%
- **90-Day Avg:** 23.4%
- **Data Points:** 754 (2023-08-11 to 2026-07-09)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 50.6% | 216/427 | 49.4% | Up | +0.0087 | Overbought |
| 2 | Financial | 31.5% | 197/626 | 33.4% | Up | +0.0006 | Normal |
| 3 | Real Estate | 24.1% | 35/145 | 31.0% | Down | -0.0046 | Normal |
| 4 | Communication Services | 24.1% | 27/112 | 25.3% | Up | +0.0043 | Normal |
| 5 | Energy | 23.7% | 37/156 | 17.1% | Up | +0.0118 | Normal |
| 6 | Technology | 21.3% | 90/423 | 19.6% | Down | -0.0026 | Normal |
| 7 | Industrials | 19.2% | 76/395 | 27.5% | Down | -0.0166 | Normal |
| 8 | Consumer Defensive | 17.4% | 21/121 | 23.8% | Down | -0.0055 | Normal |
| 9 | Consumer Cyclical | 15.4% | 43/279 | 23.3% | Down | -0.0124 | Normal |
| 10 | Basic Materials | 10.9% | 16/147 | 14.8% | Down | -0.0079 | Normal |
| 11 | Utilities | 9.9% | 8/81 | 14.1% | Down | -0.0012 | Normal |

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
