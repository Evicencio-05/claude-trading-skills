# Uptrend Analyzer Report

**Generated:** 2026-05-22 20:04:37
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **32.1/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Upper |
| **Zone Proximity** | **Near boundary: -7.9 points from 40 (below)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -7 (raw: 39.1/100) |
| **Active Warnings** | 2: LATE CYCLE WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (59/100) |
| **Weakest Component** | Market Breadth (Overall) (30/100) |
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
| Uptrend Ratio | 23.1% |
| 10-Day MA | 22.2% |
| Trend | down |
| Slope | -0.0022 |
| Distance from 37% (Overbought) | -13.9pp |
| Distance from 9.7% (Oversold) | +13.4pp |
| Date | 2026-05-22 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 30 | 9.0 | WEAK: 23.1% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | █░░░ 36 | 9.0 | NARROW: 3/11 sectors uptrending, spread 35.1% |
| 3 | **Sector Rotation** | 15% | ██░░ 59 | 8.8 | BALANCED: Cyclical-Defensive gap 4.8pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | █░░░ 36 | 7.2 | WEAK MOMENTUM: slope=-0.0040, decelerating |
| 5 | **Historical Context** | 10% | ██░░ 50 | 5.0 | NEAR MEDIAN: 23.1% at 49.5th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 23.1%
- **10-Day MA:** 22.2%
- **Trend:** down
- **Slope:** -0.0022
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 3/11
- **Count Score:** 20/100
- **Spread:** 35.1% (score: 60/100)
- **Overbought (>37%):** 1 sectors (Energy)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 22.4%
- **Defensive Avg:** 17.5%
- **Commodity Avg:** 31.3%
- **Cyclical-Defensive Gap:** 4.8pp
- **Late Cycle Warning:** YES (commodity penalty: -5)
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0786, spread=0.2224
    - Outlier: Technology (deviation: +0.1394)
  - **Defensive Divergence:** std=0.051, spread=0.1183
    - Trend dissenter: Consumer Defensive (down vs majority up)
    - Trend dissenter: Healthcare (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 36.3% | Down | -0.0008 |
| Consumer Cyclical | 14.1% | Down | -0.0035 |
| Communication Services | 19.3% | Down | -0.0051 |
| Financial | 17.1% | Down | -0.0007 |
| Industrials | 25.1% | Down | -0.0075 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 11.2% | Up | +0.0013 |
| Consumer Defensive | 13.8% | Down | -0.0009 |
| Healthcare | 22.0% | Down | -0.0035 |
| Real Estate | 23.1% | Up | +0.0002 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 46.4% | Up | +0.0151 |
| Basic Materials | 16.2% | Down | -0.0156 |


### 4. Momentum

- **Raw Slope:** -0.0022
- **Smoothed Slope (EMA(3)):** -0.0040 (score: 46/100)
- **Acceleration (10v10):** -0.002992 (decelerating, score: 25/100)
- **Sector Slope Breadth:** 3/11 positive (score: 27/100)

### 5. Historical Context

- **Current Ratio:** 23.1%
- **Percentile Rank:** 49.5th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 27.4%
- **90-Day Avg:** 26.0%
- **Data Points:** 720 (2023-08-11 to 2026-05-22)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 46.4% | 77/166 | 54.5% | Up | +0.0151 | Overbought |
| 2 | Technology | 36.3% | 150/413 | 33.0% | Down | -0.0008 | Normal |
| 3 | Industrials | 25.1% | 96/382 | 25.0% | Down | -0.0075 | Normal |
| 4 | Real Estate | 23.1% | 33/143 | 18.7% | Up | +0.0002 | Normal |
| 5 | Healthcare | 22.0% | 90/409 | 21.9% | Down | -0.0035 | Normal |
| 6 | Communication Services | 19.3% | 21/109 | 20.3% | Down | -0.0051 | Normal |
| 7 | Financial | 17.1% | 103/603 | 13.3% | Down | -0.0007 | Normal |
| 8 | Basic Materials | 16.2% | 25/154 | 23.6% | Down | -0.0156 | Normal |
| 9 | Consumer Cyclical | 14.1% | 39/277 | 10.9% | Down | -0.0035 | Normal |
| 10 | Consumer Defensive | 13.8% | 16/116 | 15.5% | Down | -0.0009 | Normal |
| 11 | Utilities | 11.2% | 9/80 | 9.5% | Up | +0.0013 | Normal |

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
