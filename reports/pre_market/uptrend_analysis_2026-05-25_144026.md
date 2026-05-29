# Uptrend Analyzer Report

**Generated:** 2026-05-25 14:40:26
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **37.5/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Upper |
| **Zone Proximity** | **Near boundary: -2.5 points from 40 (below)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -7 (raw: 44.5/100) |
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
| 10-Day MA | 22.0% |
| Trend | down |
| Slope | -0.0020 |
| Distance from 37% (Overbought) | -13.9pp |
| Distance from 9.7% (Oversold) | +13.4pp |
| Date | 2026-05-25 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 30 | 9.0 | WEAK: 23.1% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ██░░ 48 | 12.0 | MODERATE: 5/11 sectors uptrending, spread 35.4% |
| 3 | **Sector Rotation** | 15% | ██░░ 59 | 8.8 | BALANCED: Cyclical-Defensive gap 4.8pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | ██░░ 48 | 9.6 | NEUTRAL MOMENTUM: slope=-0.0030, steady |
| 5 | **Historical Context** | 10% | ██░░ 50 | 5.0 | NEAR MEDIAN: 23.1% at 49.6th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 23.1%
- **10-Day MA:** 22.0%
- **Trend:** down
- **Slope:** -0.0020
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 5/11
- **Count Score:** 40/100
- **Spread:** 35.4% (score: 59/100)
- **Overbought (>37%):** 1 sectors (Energy)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 22.4%
- **Defensive Avg:** 17.5%
- **Commodity Avg:** 31.5%
- **Cyclical-Defensive Gap:** 4.8pp
- **Late Cycle Warning:** YES (commodity penalty: -5)
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0779, spread=0.2203
    - Outlier: Technology (deviation: +0.1379)
    - Trend dissenter: Consumer Cyclical (up vs majority down)
    - Trend dissenter: Financial (up vs majority down)
  - **Defensive Divergence:** std=0.0512, spread=0.1183
    - Trend dissenter: Consumer Defensive (down vs majority up)
    - Trend dissenter: Healthcare (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 36.2% | Down | -0.0020 |
| Consumer Cyclical | 14.1% | Up | +0.0014 |
| Communication Services | 19.3% | Down | -0.0016 |
| Financial | 17.1% | Up | +0.0041 |
| Industrials | 25.2% | Down | -0.0068 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 11.2% | Up | +0.0038 |
| Consumer Defensive | 13.8% | Down | -0.0010 |
| Healthcare | 22.1% | Down | -0.0047 |
| Real Estate | 23.1% | Up | +0.0014 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 46.7% | Up | +0.0003 |
| Basic Materials | 16.2% | Down | -0.0244 |


### 4. Momentum

- **Raw Slope:** -0.0020
- **Smoothed Slope (EMA(3)):** -0.0030 (score: 48/100)
- **Acceleration (10v10):** -0.000949 (steady, score: 50/100)
- **Sector Slope Breadth:** 5/11 positive (score: 45/100)

### 5. Historical Context

- **Current Ratio:** 23.1%
- **Percentile Rank:** 49.6th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 27.4%
- **90-Day Avg:** 25.9%
- **Data Points:** 721 (2023-08-11 to 2026-05-25)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 46.7% | 77/165 | 54.5% | Up | +0.0003 | Overbought |
| 2 | Technology | 36.2% | 149/412 | 32.8% | Down | -0.0020 | Normal |
| 3 | Industrials | 25.2% | 96/381 | 24.3% | Down | -0.0068 | Normal |
| 4 | Real Estate | 23.1% | 33/143 | 18.9% | Up | +0.0014 | Normal |
| 5 | Healthcare | 22.1% | 90/408 | 21.4% | Down | -0.0047 | Normal |
| 6 | Communication Services | 19.3% | 21/109 | 20.2% | Down | -0.0016 | Normal |
| 7 | Financial | 17.1% | 102/596 | 13.7% | Up | +0.0041 | Normal |
| 8 | Basic Materials | 16.2% | 25/154 | 21.2% | Down | -0.0244 | Normal |
| 9 | Consumer Cyclical | 14.1% | 39/276 | 11.1% | Up | +0.0014 | Normal |
| 10 | Consumer Defensive | 13.8% | 16/116 | 15.4% | Down | -0.0010 | Normal |
| 11 | Utilities | 11.2% | 9/80 | 9.9% | Up | +0.0038 | Normal |

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
