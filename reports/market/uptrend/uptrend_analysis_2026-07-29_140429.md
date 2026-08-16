# Uptrend Analyzer Report

**Generated:** 2026-07-29 14:04:29
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **38.8/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Upper |
| **Zone Proximity** | **Near boundary: -1.2 points from 40 (below)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -7 (raw: 45.8/100) |
| **Active Warnings** | 2: LATE CYCLE WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Participation (63/100) |
| **Weakest Component** | Market Breadth (Overall) (32/100) |
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
| Uptrend Ratio | 23.7% |
| 10-Day MA | 23.6% |
| Trend | down |
| Slope | -0.0006 |
| Distance from 37% (Overbought) | -13.3pp |
| Distance from 9.7% (Oversold) | +14.0pp |
| Date | 2026-07-28 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 32 | 9.6 | WEAK: 23.7% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ███░ 63 | 15.8 | HEALTHY: 6/11 sectors uptrending, spread 31.5% |
| 3 | **Sector Rotation** | 15% | ██░░ 44 | 6.6 | DEFENSIVE TILT: Defensive leads by 1.1pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | ██░░ 44 | 8.8 | NEUTRAL MOMENTUM: slope=-0.0018, decelerating |
| 5 | **Historical Context** | 10% | ██░░ 50 | 5.0 | NEAR MEDIAN: 23.7% at 50.0th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 23.7%
- **10-Day MA:** 23.6%
- **Trend:** down
- **Slope:** -0.0006
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 6/11
- **Count Score:** 60/100
- **Spread:** 31.5% (score: 67/100)
- **Overbought (>37%):** 1 sectors (Energy)
- **Oversold (<9.7%):** 1 sectors (Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 21.4%
- **Defensive Avg:** 22.5%
- **Commodity Avg:** 30.4%
- **Cyclical-Defensive Gap:** -1.1pp
- **Late Cycle Warning:** YES (commodity penalty: -5)
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0595, spread=0.1763
    - Outlier: Technology (deviation: -0.0998)
    - Trend dissenter: Consumer Cyclical (up vs majority down)
    - Trend dissenter: Industrials (up vs majority down)
  - **Defensive Divergence:** std=0.0864, spread=0.2279
    - Outlier: Utilities (deviation: -0.1383)
    - Trend dissenter: Utilities (down vs majority up)
    - Trend dissenter: Healthcare (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 11.4% | Down | -0.0059 |
| Consumer Cyclical | 24.8% | Up | +0.0105 |
| Communication Services | 22.7% | Down | -0.0027 |
| Financial | 29.1% | Down | -0.0015 |
| Industrials | 19.0% | Up | +0.0022 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 8.6% | Down | -0.0074 |
| Consumer Defensive | 22.1% | Up | +0.0020 |
| Healthcare | 27.7% | Down | -0.0109 |
| Real Estate | 31.4% | Up | +0.0021 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 40.1% | Up | +0.0091 |
| Basic Materials | 20.7% | Up | +0.0098 |


### 4. Momentum

- **Raw Slope:** -0.0006
- **Smoothed Slope (EMA(3)):** -0.0018 (score: 51/100)
- **Acceleration (10v10):** -0.003222 (decelerating, score: 25/100)
- **Sector Slope Breadth:** 6/11 positive (score: 55/100)

### 5. Historical Context

- **Current Ratio:** 23.7%
- **Percentile Rank:** 50.0th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.7%
- **30-Day Avg:** 26.4%
- **90-Day Avg:** 24.3%
- **Data Points:** 767 (2023-08-11 to 2026-07-28)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 40.1% | 63/157 | 45.8% | Up | +0.0091 | Overbought |
| 2 | Real Estate | 31.4% | 44/140 | 35.5% | Up | +0.0021 | Normal |
| 3 | Financial | 29.1% | 177/609 | 28.2% | Down | -0.0015 | Normal |
| 4 | Healthcare | 27.7% | 114/412 | 30.6% | Down | -0.0109 | Normal |
| 5 | Consumer Cyclical | 24.8% | 69/278 | 19.9% | Up | +0.0105 | Normal |
| 6 | Communication Services | 22.7% | 25/110 | 18.8% | Down | -0.0027 | Normal |
| 7 | Consumer Defensive | 22.1% | 27/122 | 15.6% | Up | +0.0020 | Normal |
| 8 | Basic Materials | 20.7% | 30/145 | 15.5% | Up | +0.0098 | Normal |
| 9 | Industrials | 19.0% | 74/389 | 19.5% | Up | +0.0022 | Normal |
| 10 | Technology | 11.4% | 47/411 | 12.0% | Down | -0.0059 | Normal |
| 11 | Utilities | 8.6% | 7/81 | 13.2% | Down | -0.0074 | Oversold |

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
