# Uptrend Analyzer Report

**Generated:** 2026-07-23 06:27:38
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **26.6/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Lower |
| **Zone Proximity** | **Near boundary: +6.6 points from 20 (above)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -10 (raw: 36.6/100) |
| **Active Warnings** | 3: LATE CYCLE WARNING, HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Participation (48/100) |
| **Weakest Component** | Market Breadth (Overall) (28/100) |
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
| Uptrend Ratio | 21.6% |
| 10-Day MA | 24.9% |
| Trend | down |
| Slope | -0.0017 |
| Distance from 37% (Overbought) | -15.4pp |
| Distance from 9.7% (Oversold) | +11.9pp |
| Date | 2026-07-22 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 28 | 8.4 | VERY WEAK: 21.6% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ██░░ 48 | 12.0 | MODERATE: 6/11 sectors uptrending, spread 44.6% |
| 3 | **Sector Rotation** | 15% | █░░░ 28 | 4.2 | DEFENSIVE TILT: Defensive leads by 5.5pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | █░░░ 39 | 7.8 | WEAK MOMENTUM: slope=-0.0025, strong decelerating |
| 5 | **Historical Context** | 10% | ██░░ 42 | 4.2 | NEAR MEDIAN: 21.6% at 41.9th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 21.6%
- **10-Day MA:** 24.9%
- **Trend:** down
- **Slope:** -0.0017
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 6/11
- **Count Score:** 60/100
- **Spread:** 44.6% (score: 31/100)
- **Overbought (>37%):** 1 sectors (Energy)
- **Oversold (<9.7%):** 1 sectors (Technology)

### 3. Sector Rotation

- **Cyclical Avg:** 16.9%
- **Defensive Avg:** 22.4%
- **Commodity Avg:** 37.3%
- **Cyclical-Defensive Gap:** -5.5pp
- **Late Cycle Warning:** YES (commodity penalty: -10)
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0429, spread=0.1176
    - Outlier: Technology (deviation: -0.0751)
    - Trend dissenter: Consumer Cyclical (up vs majority down)
    - Trend dissenter: Industrials (up vs majority down)
  - **Defensive Divergence:** std=0.0719, spread=0.1727
    - Trend dissenter: Consumer Defensive (down vs majority up)
    - Trend dissenter: Healthcare (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 9.4% | Down | -0.0053 |
| Consumer Cyclical | 18.1% | Up | +0.0044 |
| Communication Services | 15.3% | Down | -0.0095 |
| Financial | 21.2% | Down | -0.0021 |
| Industrials | 20.6% | Up | +0.0035 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 16.0% | Up | +0.0049 |
| Consumer Defensive | 15.1% | Down | -0.0055 |
| Healthcare | 26.1% | Down | -0.0238 |
| Real Estate | 32.4% | Up | +0.0096 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 54.0% | Up | +0.0261 |
| Basic Materials | 20.5% | Up | +0.0131 |


### 4. Momentum

- **Raw Slope:** -0.0017
- **Smoothed Slope (EMA(3)):** -0.0025 (score: 49/100)
- **Acceleration (10v10):** -0.00638 (strong_decelerating, score: 10/100)
- **Sector Slope Breadth:** 6/11 positive (score: 55/100)

### 5. Historical Context

- **Current Ratio:** 21.6%
- **Percentile Rank:** 41.9th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.8%
- **30-Day Avg:** 27.1%
- **90-Day Avg:** 23.9%
- **Data Points:** 763 (2023-08-11 to 2026-07-22)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 54.0% | 87/161 | 36.2% | Up | +0.0261 | Overbought |
| 2 | Real Estate | 32.4% | 46/142 | 32.3% | Up | +0.0096 | Normal |
| 3 | Healthcare | 26.1% | 110/422 | 38.2% | Down | -0.0238 | Normal |
| 4 | Financial | 21.2% | 129/609 | 31.0% | Down | -0.0021 | Normal |
| 5 | Industrials | 20.6% | 81/393 | 18.2% | Up | +0.0035 | Normal |
| 6 | Basic Materials | 20.5% | 30/146 | 11.9% | Up | +0.0131 | Normal |
| 7 | Consumer Cyclical | 18.1% | 50/276 | 18.5% | Up | +0.0044 | Normal |
| 8 | Utilities | 16.0% | 13/81 | 14.3% | Up | +0.0049 | Normal |
| 9 | Communication Services | 15.3% | 17/111 | 22.1% | Down | -0.0095 | Normal |
| 10 | Consumer Defensive | 15.1% | 18/119 | 17.9% | Down | -0.0055 | Normal |
| 11 | Technology | 9.4% | 39/414 | 15.7% | Down | -0.0053 | Oversold |

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
