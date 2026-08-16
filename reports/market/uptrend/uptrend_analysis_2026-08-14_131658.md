# Uptrend Analyzer Report

**Generated:** 2026-08-14 13:16:58
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **57.6/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: -2.4 points from 60 (below)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -10 (raw: 67.6/100) |
| **Active Warnings** | 3: LATE CYCLE WARNING, HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (77/100) |
| **Weakest Component** | Market Breadth (Overall) (60/100) |
| **Data Quality** | Complete (5/5 components) |
| **Confidence** | High (moderate, Both regime coverage) |

> **Guidance:** Mixed signals. Participate selectively with tighter risk controls.

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
| Uptrend Ratio | 31.1% |
| 10-Day MA | 26.6% |
| Trend | up |
| Slope | +0.0096 |
| Distance from 37% (Overbought) | -5.9pp |
| Distance from 9.7% (Oversold) | +21.4pp |
| Date | 2026-08-13 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ███░ 60 | 18.0 | NEUTRAL: 31.1% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ███░ 61 | 15.2 | HEALTHY: 8/11 sectors uptrending, spread 43.9% |
| 3 | **Sector Rotation** | 15% | ███░ 77 | 11.5 | RISK-ON: Cyclical leads by 14.2pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | ███░ 76 | 15.2 | POSITIVE MOMENTUM: slope=0.0076, strong accelerating |
| 5 | **Historical Context** | 10% | ███░ 76 | 7.6 | SLIGHTLY ABOVE: 31.1% at 75.5th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 31.1%
- **10-Day MA:** 26.6%
- **Trend:** up
- **Slope:** +0.0096
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 8/11
- **Count Score:** 80/100
- **Spread:** 43.9% (score: 33/100)
- **Overbought (>37%):** 2 sectors (Energy, Healthcare)
- **Oversold (<9.7%):** 1 sectors (Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 31.5%
- **Defensive Avg:** 17.3%
- **Commodity Avg:** 37.2%
- **Cyclical-Defensive Gap:** 14.2pp
- **Late Cycle Warning:** YES (commodity penalty: -5)
- **Divergence Warning:** YES (penalty: -5)
  - **Defensive Divergence:** std=0.1251, spread=0.3345
    - Outlier: Healthcare (deviation: +0.1981)
    - Trend dissenter: Healthcare (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 36.2% | Up | +0.0258 |
| Consumer Cyclical | 26.3% | Up | +0.0019 |
| Communication Services | 30.3% | Up | +0.0085 |
| Financial | 32.7% | Up | +0.0070 |
| Industrials | 32.3% | Up | +0.0194 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 3.7% | Down | -0.0037 |
| Consumer Defensive | 18.0% | Down | -0.0026 |
| Healthcare | 37.1% | Up | +0.0123 |
| Real Estate | 10.5% | Down | -0.0197 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 47.6% | Up | +0.0040 |
| Basic Materials | 26.8% | Up | +0.0073 |


### 4. Momentum

- **Raw Slope:** +0.0096 
- **Smoothed Slope (EMA(3)):** +0.0076 (score: 69/100)
- **Acceleration (10v10):** 0.005673 (strong_accelerating, score: 90/100)
- **Sector Slope Breadth:** 8/11 positive (score: 73/100)

### 5. Historical Context

- **Current Ratio:** 31.1%
- **Percentile Rank:** 75.5th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.8%
- **30-Day Avg:** 25.5%
- **90-Day Avg:** 26.0%
- **Data Points:** 778 (2023-08-11 to 2026-08-13)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 47.6% | 78/164 | 41.9% | Up | +0.0040 | Overbought |
| 2 | Healthcare | 37.1% | 159/428 | 30.1% | Up | +0.0123 | Overbought |
| 3 | Technology | 36.2% | 154/426 | 24.7% | Up | +0.0258 | Normal |
| 4 | Financial | 32.7% | 196/600 | 29.9% | Up | +0.0070 | Normal |
| 5 | Industrials | 32.3% | 128/396 | 27.1% | Up | +0.0194 | Normal |
| 6 | Communication Services | 30.3% | 33/109 | 23.8% | Up | +0.0085 | Normal |
| 7 | Basic Materials | 26.8% | 42/157 | 26.7% | Up | +0.0073 | Normal |
| 8 | Consumer Cyclical | 26.3% | 75/285 | 27.5% | Up | +0.0019 | Normal |
| 9 | Consumer Defensive | 18.0% | 22/122 | 15.5% | Down | -0.0026 | Normal |
| 10 | Real Estate | 10.5% | 15/143 | 13.3% | Down | -0.0197 | Normal |
| 11 | Utilities | 3.7% | 3/81 | 3.0% | Down | -0.0037 | Oversold |

---

## Recommended Actions

**Zone:** Neutral (Neutral)
**Exposure Guidance:** Reduced Exposure (60-80%)

- Reduce position sizes by 20-30%
- Focus on strongest sectors only
- Tighten stop-losses
- Avoid low-quality setups
- Increase cash allocation gradually

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
