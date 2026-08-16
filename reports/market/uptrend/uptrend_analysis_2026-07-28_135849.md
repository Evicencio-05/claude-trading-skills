# Uptrend Analyzer Report

**Generated:** 2026-07-28 13:58:49
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **32.4/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Upper |
| **Zone Proximity** | **Near boundary: -7.6 points from 40 (below)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -7 (raw: 39.4/100) |
| **Active Warnings** | 2: LATE CYCLE WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (48/100) |
| **Weakest Component** | Market Breadth (Overall) (31/100) |
| **Data Quality** | Complete (5/5 components) |
| **Confidence** | High (moderate, Both regime coverage) |

> **Guidance:** Weak breadth environment. Prioritize capital preservation over gains.

---

## Active Warnings

### LATE CYCLE WARNING
> Commodity sectors leading both cyclical and defensive groups. Historically associated with late-cycle inflation or sector rotation preceding broader market weakness.

- Favor lower end of exposure range (e.g. 80% if guidance is 80-100%)
- New entries limited to A-grade setups only
- Tighten stops on commodity/cyclical positions
- Monitor for commodity rollover as potential broad market lead indicator

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
| 10-Day MA | 23.7% |
| Trend | down |
| Slope | -0.0017 |
| Distance from 37% (Overbought) | -13.8pp |
| Distance from 9.7% (Oversold) | +13.5pp |
| Date | 2026-07-27 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 31 | 9.3 | WEAK: 23.2% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ██░░ 45 | 11.2 | MODERATE: 5/11 sectors uptrending, spread 37.2% |
| 3 | **Sector Rotation** | 15% | █░░░ 39 | 5.8 | DEFENSIVE TILT: Defensive leads by 3.5pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | ██░░ 41 | 8.2 | NEUTRAL MOMENTUM: slope=-0.0031, decelerating |
| 5 | **Historical Context** | 10% | ██░░ 48 | 4.8 | NEAR MEDIAN: 23.2% at 48.1th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 23.2%
- **10-Day MA:** 23.7%
- **Trend:** down
- **Slope:** -0.0017
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 5/11
- **Count Score:** 40/100
- **Spread:** 37.2% (score: 53/100)
- **Overbought (>37%):** 2 sectors (Energy, Real Estate)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 20.1%
- **Defensive Avg:** 23.5%
- **Commodity Avg:** 33.0%
- **Cyclical-Defensive Gap:** -3.5pp
- **Late Cycle Warning:** YES (commodity penalty: -5)
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0507, spread=0.1521
    - Outlier: Technology (deviation: -0.0888)
    - Trend dissenter: Consumer Cyclical (up vs majority down)
    - Trend dissenter: Industrials (up vs majority down)
  - **Defensive Divergence:** std=0.0935, spread=0.248
    - Trend dissenter: Real Estate (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 11.2% | Down | -0.0066 |
| Consumer Cyclical | 22.8% | Up | +0.0074 |
| Communication Services | 20.9% | Down | -0.0025 |
| Financial | 26.4% | Down | -0.0059 |
| Industrials | 19.0% | Up | +0.0030 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 12.3% | Down | -0.0049 |
| Consumer Defensive | 18.0% | Down | -0.0045 |
| Healthcare | 26.6% | Down | -0.0174 |
| Real Estate | 37.1% | Up | +0.0155 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 48.4% | Up | +0.0228 |
| Basic Materials | 17.7% | Up | +0.0075 |


### 4. Momentum

- **Raw Slope:** -0.0017
- **Smoothed Slope (EMA(3)):** -0.0031 (score: 48/100)
- **Acceleration (10v10):** -0.004647 (decelerating, score: 25/100)
- **Sector Slope Breadth:** 5/11 positive (score: 45/100)

### 5. Historical Context

- **Current Ratio:** 23.2%
- **Percentile Rank:** 48.1th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.8%
- **30-Day Avg:** 26.5%
- **90-Day Avg:** 24.2%
- **Data Points:** 766 (2023-08-11 to 2026-07-27)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 48.4% | 76/157 | 44.9% | Up | +0.0228 | Overbought |
| 2 | Real Estate | 37.1% | 52/140 | 35.3% | Up | +0.0155 | Overbought |
| 3 | Healthcare | 26.6% | 110/414 | 31.7% | Down | -0.0174 | Normal |
| 4 | Financial | 26.4% | 160/606 | 28.3% | Down | -0.0059 | Normal |
| 5 | Consumer Cyclical | 22.8% | 63/276 | 18.9% | Up | +0.0074 | Normal |
| 6 | Communication Services | 20.9% | 23/110 | 19.0% | Down | -0.0025 | Normal |
| 7 | Industrials | 19.0% | 74/389 | 19.3% | Up | +0.0030 | Normal |
| 8 | Consumer Defensive | 18.0% | 22/122 | 15.4% | Down | -0.0045 | Normal |
| 9 | Basic Materials | 17.7% | 26/147 | 14.5% | Up | +0.0075 | Normal |
| 10 | Utilities | 12.3% | 10/81 | 13.9% | Down | -0.0049 | Normal |
| 11 | Technology | 11.2% | 46/411 | 12.6% | Down | -0.0066 | Normal |

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
