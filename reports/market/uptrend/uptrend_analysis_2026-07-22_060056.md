# Uptrend Analyzer Report

**Generated:** 2026-07-22 06:00:56
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **27.4/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Lower |
| **Zone Proximity** | **Near boundary: +7.4 points from 20 (above)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -10 (raw: 37.4/100) |
| **Active Warnings** | 3: LATE CYCLE WARNING, HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (54/100) |
| **Weakest Component** | Momentum (34/100) |
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
| Uptrend Ratio | 25.2% |
| 10-Day MA | 25.1% |
| Trend | down |
| Slope | -0.0019 |
| Distance from 37% (Overbought) | -11.8pp |
| Distance from 9.7% (Oversold) | +15.5pp |
| Date | 2026-07-21 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 35 | 10.5 | WEAK: 25.2% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | █░░░ 38 | 9.5 | NARROW: 4/11 sectors uptrending, spread 43.1% |
| 3 | **Sector Rotation** | 15% | █░░░ 35 | 5.2 | DEFENSIVE TILT: Defensive leads by 4.9pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | █░░░ 34 | 6.8 | WEAK MOMENTUM: slope=-0.0034, strong decelerating |
| 5 | **Historical Context** | 10% | ██░░ 54 | 5.4 | NEAR MEDIAN: 25.2% at 53.9th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 25.2%
- **10-Day MA:** 25.1%
- **Trend:** down
- **Slope:** -0.0019
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 4/11
- **Count Score:** 40/100
- **Spread:** 43.1% (score: 36/100)
- **Overbought (>37%):** 2 sectors (Energy, Real Estate)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 20.2%
- **Defensive Avg:** 25.0%
- **Commodity Avg:** 33.1%
- **Cyclical-Defensive Gap:** -4.9pp
- **Late Cycle Warning:** YES (commodity penalty: -5)
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0548, spread=0.1702
    - Outlier: Financial (deviation: +0.0962)
    - Trend dissenter: Technology (up vs majority down)
  - **Defensive Divergence:** std=0.1228, spread=0.2873
    - Trend dissenter: Real Estate (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 12.8% | Up | +0.0006 |
| Consumer Cyclical | 19.1% | Down | -0.0026 |
| Communication Services | 18.9% | Down | -0.0054 |
| Financial | 29.8% | Down | -0.0053 |
| Industrials | 20.3% | Down | -0.0002 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 10.0% | Down | -0.0048 |
| Consumer Defensive | 16.0% | Down | -0.0065 |
| Healthcare | 35.4% | Down | -0.0148 |
| Real Estate | 38.7% | Up | +0.0063 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 53.1% | Up | +0.0362 |
| Basic Materials | 13.0% | Up | +0.0008 |


### 4. Momentum

- **Raw Slope:** -0.0019
- **Smoothed Slope (EMA(3)):** -0.0034 (score: 48/100)
- **Acceleration (10v10):** -0.007046 (strong_decelerating, score: 10/100)
- **Sector Slope Breadth:** 4/11 positive (score: 36/100)

### 5. Historical Context

- **Current Ratio:** 25.2%
- **Percentile Rank:** 53.9th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.8%
- **30-Day Avg:** 27.1%
- **90-Day Avg:** 23.8%
- **Data Points:** 762 (2023-08-11 to 2026-07-21)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 53.1% | 85/160 | 33.6% | Up | +0.0362 | Overbought |
| 2 | Real Estate | 38.7% | 55/142 | 31.3% | Up | +0.0063 | Overbought |
| 3 | Healthcare | 35.4% | 149/421 | 40.6% | Down | -0.0148 | Normal |
| 4 | Financial | 29.8% | 182/611 | 31.3% | Down | -0.0053 | Normal |
| 5 | Industrials | 20.3% | 80/394 | 17.9% | Down | -0.0002 | Normal |
| 6 | Consumer Cyclical | 19.1% | 53/278 | 18.0% | Down | -0.0026 | Normal |
| 7 | Communication Services | 18.9% | 21/111 | 23.0% | Down | -0.0054 | Normal |
| 8 | Consumer Defensive | 16.0% | 19/119 | 18.5% | Down | -0.0065 | Normal |
| 9 | Basic Materials | 13.0% | 19/146 | 10.6% | Up | +0.0008 | Normal |
| 10 | Technology | 12.8% | 53/415 | 16.2% | Up | +0.0006 | Normal |
| 11 | Utilities | 10.0% | 8/80 | 13.8% | Down | -0.0048 | Normal |

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
