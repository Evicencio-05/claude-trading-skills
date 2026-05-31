# Uptrend Analyzer Report

**Generated:** 2026-05-19 06:19:48
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **18.0/100** |
| **Zone** | 🔴 Bear |
| **Zone Detail** | Bear |
| **Zone Proximity** | **Near boundary: -2.0 points from 20 (below)** |
| **Exposure Guidance** | Capital Preservation (0-30%) |
| **Warning Penalty** | -10 (raw: 28.0/100) |
| **Active Warnings** | 3: LATE CYCLE WARNING, HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (54/100) |
| **Weakest Component** | Sector Participation (12/100) |
| **Data Quality** | Complete (5/5 components) |
| **Confidence** | High (moderate, Both regime coverage) |

> **Guidance:** Severe breadth deterioration. Maximum defensive posture.

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
| Uptrend Ratio | 19.5% |
| 10-Day MA | 24.7% |
| Trend | down |
| Slope | -0.0045 |
| Distance from 37% (Overbought) | -17.5pp |
| Distance from 9.7% (Oversold) | +9.8pp |
| Date | 2026-05-18 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 24 | 7.2 | VERY WEAK: 19.5% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ░░░░ 12 | 3.0 | VERY NARROW: 3/11 sectors uptrending, spread 62.0% |
| 3 | **Sector Rotation** | 15% | ██░░ 54 | 8.1 | BALANCED: Cyclical-Defensive gap 4.9pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | █░░░ 30 | 6.0 | WEAK MOMENTUM: slope=-0.0053, strong decelerating |
| 5 | **Historical Context** | 10% | █░░░ 37 | 3.7 | BELOW AVERAGE: 19.5% at 37.2th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 19.5%
- **10-Day MA:** 24.7%
- **Trend:** down
- **Slope:** -0.0045
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 3/11
- **Count Score:** 20/100
- **Spread:** 62.0% (score: 0/100)
- **Overbought (>37%):** 1 sectors (Energy)
- **Oversold (<9.7%):** 2 sectors (Consumer Cyclical, Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 18.2%
- **Defensive Avg:** 13.2%
- **Commodity Avg:** 41.9%
- **Cyclical-Defensive Gap:** 4.9pp
- **Late Cycle Warning:** YES (commodity penalty: -10)
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0723, spread=0.191
    - Trend dissenter: Communication Services (up vs majority down)
  - **Defensive Divergence:** std=0.0332, spread=0.0802
    - Outlier: Utilities (deviation: -0.0574)
    - Trend dissenter: Consumer Defensive (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 27.8% | Down | -0.0073 |
| Consumer Cyclical | 8.7% | Down | -0.0005 |
| Communication Services | 22.0% | Up | +0.0033 |
| Financial | 10.9% | Down | -0.0034 |
| Industrials | 21.5% | Down | -0.0067 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 7.5% | Down | -0.0071 |
| Consumer Defensive | 15.5% | Up | +0.0036 |
| Healthcare | 15.1% | Down | -0.0103 |
| Real Estate | 14.8% | Down | -0.0040 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 69.5% | Up | +0.0093 |
| Basic Materials | 14.3% | Down | -0.0139 |


### 4. Momentum

- **Raw Slope:** -0.0045
- **Smoothed Slope (EMA(3)):** -0.0053 (score: 44/100)
- **Acceleration (10v10):** -0.013157 (strong_decelerating, score: 10/100)
- **Sector Slope Breadth:** 3/11 positive (score: 27/100)

### 5. Historical Context

- **Current Ratio:** 19.5%
- **Percentile Rank:** 37.2th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 26.8%
- **90-Day Avg:** 26.4%
- **Data Points:** 716 (2023-08-11 to 2026-05-18)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 69.5% | 116/167 | 48.5% | Up | +0.0093 | Overbought |
| 2 | Technology | 27.8% | 112/403 | 35.4% | Down | -0.0073 | Normal |
| 3 | Communication Services | 22.0% | 24/109 | 21.7% | Up | +0.0033 | Normal |
| 4 | Industrials | 21.5% | 82/381 | 30.7% | Down | -0.0067 | Normal |
| 5 | Consumer Defensive | 15.5% | 18/116 | 16.1% | Up | +0.0036 | Normal |
| 6 | Healthcare | 15.1% | 61/403 | 25.2% | Down | -0.0103 | Normal |
| 7 | Real Estate | 14.8% | 21/142 | 19.5% | Down | -0.0040 | Normal |
| 8 | Basic Materials | 14.3% | 22/154 | 32.7% | Down | -0.0139 | Normal |
| 9 | Financial | 10.9% | 65/598 | 15.3% | Down | -0.0034 | Normal |
| 10 | Consumer Cyclical | 8.7% | 24/276 | 13.5% | Down | -0.0005 | Oversold |
| 11 | Utilities | 7.5% | 6/80 | 10.3% | Down | -0.0071 | Oversold |

---

## Recommended Actions

**Zone:** Bear (Bear)
**Exposure Guidance:** Capital Preservation (0-30%)

- Maximum cash (70-100%)
- Exit most equity positions
- Only ultra-high-conviction holdings
- Consider hedges (inverse ETFs, puts)
- Wait for breadth recovery before re-entry

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
