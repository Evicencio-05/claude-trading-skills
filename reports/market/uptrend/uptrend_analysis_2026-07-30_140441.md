# Uptrend Analyzer Report

**Generated:** 2026-07-30 14:04:41
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **30.6/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Upper |
| **Zone Proximity** | **Near boundary: -9.4 points from 40 (below)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -7 (raw: 37.6/100) |
| **Active Warnings** | 2: LATE CYCLE WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Participation (47/100) |
| **Weakest Component** | Market Breadth (Overall) (27/100) |
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
| Uptrend Ratio | 21.5% |
| 10-Day MA | 23.4% |
| Trend | down |
| Slope | -0.0025 |
| Distance from 37% (Overbought) | -15.5pp |
| Distance from 9.7% (Oversold) | +11.8pp |
| Date | 2026-07-29 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 27 | 8.1 | VERY WEAK: 21.5% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ██░░ 47 | 11.8 | MODERATE: 4/11 sectors uptrending, spread 36.2% |
| 3 | **Sector Rotation** | 15% | █░░░ 38 | 5.7 | DEFENSIVE TILT: Defensive leads by 1.7pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | ██░░ 40 | 8.0 | NEUTRAL MOMENTUM: slope=-0.0022, decelerating |
| 5 | **Historical Context** | 10% | ██░░ 41 | 4.1 | NEAR MEDIAN: 21.5% at 41.2th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 21.5%
- **10-Day MA:** 23.4%
- **Trend:** down
- **Slope:** -0.0025
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 4/11
- **Count Score:** 40/100
- **Spread:** 36.2% (score: 56/100)
- **Overbought (>37%):** 1 sectors (Energy)
- **Oversold (<9.7%):** 1 sectors (Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 19.0%
- **Defensive Avg:** 20.8%
- **Commodity Avg:** 31.5%
- **Cyclical-Defensive Gap:** -1.7pp
- **Late Cycle Warning:** YES (commodity penalty: -10)
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0624, spread=0.1538
    - Trend dissenter: Consumer Cyclical (up vs majority down)
  - **Defensive Divergence:** std=0.0843, spread=0.2281
    - Outlier: Utilities (deviation: -0.1337)
    - Trend dissenter: Consumer Defensive (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 10.3% | Down | -0.0049 |
| Consumer Cyclical | 24.5% | Up | +0.0061 |
| Communication Services | 21.8% | Down | -0.0021 |
| Financial | 25.7% | Down | -0.0063 |
| Industrials | 12.9% | Down | -0.0028 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 7.4% | Down | -0.0086 |
| Consumer Defensive | 20.7% | Up | +0.0088 |
| Healthcare | 24.8% | Down | -0.0155 |
| Real Estate | 30.2% | Down | -0.0001 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 43.6% | Up | +0.0208 |
| Basic Materials | 19.4% | Up | +0.0085 |


### 4. Momentum

- **Raw Slope:** -0.0025
- **Smoothed Slope (EMA(3)):** -0.0022 (score: 50/100)
- **Acceleration (10v10):** -0.001728 (decelerating, score: 25/100)
- **Sector Slope Breadth:** 4/11 positive (score: 36/100)

### 5. Historical Context

- **Current Ratio:** 21.5%
- **Percentile Rank:** 41.2th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.7%
- **30-Day Avg:** 26.3%
- **90-Day Avg:** 24.4%
- **Data Points:** 768 (2023-08-11 to 2026-07-29)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 43.6% | 68/156 | 47.8% | Up | +0.0208 | Overbought |
| 2 | Real Estate | 30.2% | 42/139 | 35.5% | Down | -0.0001 | Normal |
| 3 | Financial | 25.7% | 157/611 | 27.6% | Down | -0.0063 | Normal |
| 4 | Healthcare | 24.8% | 102/411 | 29.0% | Down | -0.0155 | Normal |
| 5 | Consumer Cyclical | 24.5% | 68/278 | 20.5% | Up | +0.0061 | Normal |
| 6 | Communication Services | 21.8% | 24/110 | 18.5% | Down | -0.0021 | Normal |
| 7 | Consumer Defensive | 20.7% | 25/121 | 16.5% | Up | +0.0088 | Normal |
| 8 | Basic Materials | 19.4% | 28/144 | 16.4% | Up | +0.0085 | Normal |
| 9 | Industrials | 12.9% | 50/387 | 19.2% | Down | -0.0028 | Normal |
| 10 | Technology | 10.3% | 42/407 | 11.6% | Down | -0.0049 | Normal |
| 11 | Utilities | 7.4% | 6/81 | 12.3% | Down | -0.0086 | Oversold |

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
