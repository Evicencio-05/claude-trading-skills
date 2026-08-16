# Uptrend Analyzer Report

**Generated:** 2026-07-31 06:00:20
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **24.8/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Lower |
| **Zone Proximity** | **Near boundary: +4.8 points from 20 (above)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -10 (raw: 34.8/100) |
| **Active Warnings** | 3: LATE CYCLE WARNING, HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (45/100) |
| **Weakest Component** | Sector Participation (28/100) |
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
| Uptrend Ratio | 22.5% |
| 10-Day MA | 23.0% |
| Trend | down |
| Slope | -0.0042 |
| Distance from 37% (Overbought) | -14.5pp |
| Distance from 9.7% (Oversold) | +12.8pp |
| Date | 2026-07-30 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 29 | 8.7 | VERY WEAK: 22.5% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | █░░░ 28 | 7.0 | NARROW: 3/11 sectors uptrending, spread 41.9% |
| 3 | **Sector Rotation** | 15% | █░░░ 39 | 5.8 | DEFENSIVE TILT: Defensive leads by 1.2pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | ██░░ 44 | 8.8 | NEUTRAL MOMENTUM: slope=-0.0032, steady |
| 5 | **Historical Context** | 10% | ██░░ 45 | 4.5 | NEAR MEDIAN: 22.5% at 44.7th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 22.5%
- **10-Day MA:** 23.0%
- **Trend:** down
- **Slope:** -0.0042
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 3/11
- **Count Score:** 20/100
- **Spread:** 41.9% (score: 39/100)
- **Overbought (>37%):** 1 sectors (Energy)
- **Oversold (<9.7%):** 1 sectors (Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 18.7%
- **Defensive Avg:** 19.8%
- **Commodity Avg:** 37.5%
- **Cyclical-Defensive Gap:** -1.2pp
- **Late Cycle Warning:** YES (commodity penalty: -10)
- **Divergence Warning:** YES (penalty: -5)
  - **Defensive Divergence:** std=0.0832, spread=0.2185
    - Outlier: Utilities (deviation: -0.1366)
    - Trend dissenter: Consumer Defensive (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 11.7% | Down | -0.0023 |
| Consumer Cyclical | 21.1% | Down | -0.0032 |
| Communication Services | 20.0% | Down | -0.0030 |
| Financial | 27.5% | Down | -0.0090 |
| Industrials | 13.0% | Down | -0.0074 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 6.2% | Down | -0.0076 |
| Consumer Defensive | 20.5% | Up | +0.0008 |
| Healthcare | 28.0% | Down | -0.0059 |
| Real Estate | 24.6% | Down | -0.0184 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 48.1% | Up | +0.0116 |
| Basic Materials | 26.9% | Up | +0.0152 |


### 4. Momentum

- **Raw Slope:** -0.0042
- **Smoothed Slope (EMA(3)):** -0.0032 (score: 48/100)
- **Acceleration (10v10):** -0.000979 (steady, score: 50/100)
- **Sector Slope Breadth:** 3/11 positive (score: 27/100)

### 5. Historical Context

- **Current Ratio:** 22.5%
- **Percentile Rank:** 44.7th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.7%
- **30-Day Avg:** 26.1%
- **90-Day Avg:** 24.5%
- **Data Points:** 769 (2023-08-11 to 2026-07-30)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 48.1% | 76/158 | 49.0% | Up | +0.0116 | Overbought |
| 2 | Healthcare | 28.0% | 116/414 | 28.4% | Down | -0.0059 | Normal |
| 3 | Financial | 27.5% | 168/611 | 26.7% | Down | -0.0090 | Normal |
| 4 | Basic Materials | 26.9% | 39/145 | 17.9% | Up | +0.0152 | Normal |
| 5 | Real Estate | 24.6% | 34/138 | 33.7% | Down | -0.0184 | Normal |
| 6 | Consumer Cyclical | 21.1% | 59/279 | 20.2% | Down | -0.0032 | Normal |
| 7 | Consumer Defensive | 20.5% | 25/122 | 16.5% | Up | +0.0008 | Normal |
| 8 | Communication Services | 20.0% | 22/110 | 18.2% | Down | -0.0030 | Normal |
| 9 | Industrials | 13.0% | 50/386 | 18.5% | Down | -0.0074 | Normal |
| 10 | Technology | 11.7% | 48/411 | 11.3% | Down | -0.0023 | Normal |
| 11 | Utilities | 6.2% | 5/81 | 11.5% | Down | -0.0076 | Oversold |

---

## Recommended Actions

**Zone:** Cautious (Cautious-Lower)
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
