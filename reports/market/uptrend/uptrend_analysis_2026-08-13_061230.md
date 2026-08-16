# Uptrend Analyzer Report

**Generated:** 2026-08-13 06:12:30
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **55.2/100** |
| **Zone** | 🟡 Neutral |
| **Zone Detail** | Neutral |
| **Zone Proximity** | **Near boundary: -4.8 points from 60 (below)** |
| **Exposure Guidance** | Reduced Exposure (60-80%) |
| **Warning Penalty** | -10 (raw: 65.2/100) |
| **Active Warnings** | 3: LATE CYCLE WARNING, HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (76/100) |
| **Weakest Component** | Market Breadth (Overall) (57/100) |
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
| Uptrend Ratio | 30.1% |
| 10-Day MA | 25.7% |
| Trend | up |
| Slope | +0.0064 |
| Distance from 37% (Overbought) | -6.9pp |
| Distance from 9.7% (Oversold) | +20.4pp |
| Date | 2026-08-12 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ██░░ 57 | 17.1 | NEUTRAL: 30.1% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ██░░ 59 | 14.8 | MODERATE: 8/11 sectors uptrending, spread 45.7% |
| 3 | **Sector Rotation** | 15% | ███░ 76 | 11.4 | RISK-ON: Cyclical leads by 13.4pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | ███░ 74 | 14.8 | POSITIVE MOMENTUM: slope=0.0057, strong accelerating |
| 5 | **Historical Context** | 10% | ███░ 72 | 7.2 | SLIGHTLY ABOVE: 30.1% at 72.3th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 30.1%
- **10-Day MA:** 25.7%
- **Trend:** up
- **Slope:** +0.0064
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 8/11
- **Count Score:** 80/100
- **Spread:** 45.7% (score: 28/100)
- **Overbought (>37%):** 2 sectors (Energy, Healthcare)
- **Oversold (<9.7%):** 1 sectors (Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 29.6%
- **Defensive Avg:** 16.2%
- **Commodity Avg:** 38.7%
- **Cyclical-Defensive Gap:** 13.4pp
- **Late Cycle Warning:** YES (commodity penalty: -5)
- **Divergence Warning:** YES (penalty: -5)
  - **Defensive Divergence:** std=0.132, spread=0.3532
    - Outlier: Healthcare (deviation: +0.2157)
    - Trend dissenter: Healthcare (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 31.4% | Up | +0.0199 |
| Consumer Cyclical | 27.4% | Up | +0.0025 |
| Communication Services | 26.2% | Up | +0.0034 |
| Financial | 32.5% | Up | +0.0034 |
| Industrials | 30.5% | Up | +0.0114 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 2.5% | Down | -0.0062 |
| Consumer Defensive | 14.8% | Down | -0.0074 |
| Healthcare | 37.8% | Up | +0.0101 |
| Real Estate | 9.9% | Down | -0.0216 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 48.2% | Up | +0.0080 |
| Basic Materials | 29.2% | Up | +0.0085 |


### 4. Momentum

- **Raw Slope:** +0.0064 
- **Smoothed Slope (EMA(3)):** +0.0057 (score: 66/100)
- **Acceleration (10v10):** 0.00511 (strong_accelerating, score: 90/100)
- **Sector Slope Breadth:** 8/11 positive (score: 73/100)

### 5. Historical Context

- **Current Ratio:** 30.1%
- **Percentile Rank:** 72.3th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.8%
- **30-Day Avg:** 25.4%
- **90-Day Avg:** 25.8%
- **Data Points:** 777 (2023-08-11 to 2026-08-12)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 48.2% | 79/164 | 41.5% | Up | +0.0080 | Overbought |
| 2 | Healthcare | 37.8% | 161/426 | 28.9% | Up | +0.0101 | Overbought |
| 3 | Financial | 32.5% | 194/597 | 29.2% | Up | +0.0034 | Normal |
| 4 | Technology | 31.4% | 133/424 | 22.1% | Up | +0.0199 | Normal |
| 5 | Industrials | 30.5% | 120/394 | 25.1% | Up | +0.0114 | Normal |
| 6 | Basic Materials | 29.2% | 45/154 | 26.0% | Up | +0.0085 | Normal |
| 7 | Consumer Cyclical | 27.4% | 78/285 | 27.3% | Up | +0.0025 | Normal |
| 8 | Communication Services | 26.2% | 28/107 | 23.0% | Up | +0.0034 | Normal |
| 9 | Consumer Defensive | 14.8% | 18/122 | 15.7% | Down | -0.0074 | Normal |
| 10 | Real Estate | 9.9% | 14/142 | 15.2% | Down | -0.0216 | Normal |
| 11 | Utilities | 2.5% | 2/81 | 3.3% | Down | -0.0062 | Oversold |

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
