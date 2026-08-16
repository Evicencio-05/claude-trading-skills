# Uptrend Analyzer Report

**Generated:** 2026-08-03 06:03:09
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **21.5/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Lower |
| **Zone Proximity** | **Near boundary: +1.5 points from 20 (above)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -10 (raw: 31.5/100) |
| **Active Warnings** | 3: LATE CYCLE WARNING, HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (52/100) |
| **Weakest Component** | Sector Participation (13/100) |
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
| Uptrend Ratio | 21.0% |
| 10-Day MA | 22.4% |
| Trend | down |
| Slope | -0.0054 |
| Distance from 37% (Overbought) | -16.0pp |
| Distance from 9.7% (Oversold) | +11.3pp |
| Date | 2026-07-31 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 26 | 7.8 | VERY WEAK: 21.0% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ░░░░ 13 | 3.2 | VERY NARROW: 3/11 sectors uptrending, spread 53.8% |
| 3 | **Sector Rotation** | 15% | ██░░ 52 | 7.8 | BALANCED: Cyclical-Defensive gap 4.0pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | ██░░ 43 | 8.6 | NEUTRAL MOMENTUM: slope=-0.0043, steady |
| 5 | **Historical Context** | 10% | ██░░ 40 | 4.0 | NEAR MEDIAN: 21.0% at 40.2th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 21.0%
- **10-Day MA:** 22.4%
- **Trend:** down
- **Slope:** -0.0054
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 3/11
- **Count Score:** 20/100
- **Spread:** 53.8% (score: 4/100)
- **Overbought (>37%):** 1 sectors (Energy)
- **Oversold (<9.7%):** 1 sectors (Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 18.5%
- **Defensive Avg:** 14.5%
- **Commodity Avg:** 38.3%
- **Cyclical-Defensive Gap:** 4.0pp
- **Late Cycle Warning:** YES (commodity penalty: -10)
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0434, spread=0.1169
    - Trend dissenter: Consumer Cyclical (up vs majority down)
  - **Defensive Divergence:** std=0.0758, spread=0.2078
    - Outlier: Utilities (deviation: -0.1203)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 12.1% | Down | -0.0024 |
| Consumer Cyclical | 22.9% | Up | +0.0007 |
| Communication Services | 17.4% | Down | -0.0049 |
| Financial | 23.8% | Down | -0.0101 |
| Industrials | 16.4% | Down | -0.0022 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 2.5% | Down | -0.0113 |
| Consumer Defensive | 14.9% | Down | -0.0021 |
| Healthcare | 23.2% | Down | -0.0149 |
| Real Estate | 17.4% | Down | -0.0232 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 56.2% | Up | +0.0138 |
| Basic Materials | 20.3% | Up | +0.0092 |


### 4. Momentum

- **Raw Slope:** -0.0054
- **Smoothed Slope (EMA(3)):** -0.0043 (score: 46/100)
- **Acceleration (10v10):** -0.000632 (steady, score: 50/100)
- **Sector Slope Breadth:** 3/11 positive (score: 27/100)

### 5. Historical Context

- **Current Ratio:** 21.0%
- **Percentile Rank:** 40.2th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.7%
- **30-Day Avg:** 25.9%
- **90-Day Avg:** 24.7%
- **Data Points:** 770 (2023-08-11 to 2026-07-31)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 56.2% | 90/160 | 50.4% | Up | +0.0138 | Overbought |
| 2 | Financial | 23.8% | 144/606 | 25.7% | Down | -0.0101 | Normal |
| 3 | Healthcare | 23.2% | 96/413 | 26.9% | Down | -0.0149 | Normal |
| 4 | Consumer Cyclical | 22.9% | 64/279 | 20.3% | Up | +0.0007 | Normal |
| 5 | Basic Materials | 20.3% | 29/143 | 18.8% | Up | +0.0092 | Normal |
| 6 | Communication Services | 17.4% | 19/109 | 17.8% | Down | -0.0049 | Normal |
| 7 | Real Estate | 17.4% | 24/138 | 31.4% | Down | -0.0232 | Normal |
| 8 | Industrials | 16.4% | 64/391 | 18.3% | Down | -0.0022 | Normal |
| 9 | Consumer Defensive | 14.9% | 18/121 | 16.3% | Down | -0.0021 | Normal |
| 10 | Technology | 12.1% | 50/414 | 11.1% | Down | -0.0024 | Normal |
| 11 | Utilities | 2.5% | 2/81 | 10.4% | Down | -0.0113 | Oversold |

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
