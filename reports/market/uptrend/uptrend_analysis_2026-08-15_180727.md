# Uptrend Analyzer Report

**Generated:** 2026-08-15 18:07:27
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
| **Strongest Component** | Historical Context (82/100) |
| **Weakest Component** | Sector Participation (51/100) |
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
| Uptrend Ratio | 32.9% |
| 10-Day MA | 27.7% |
| Trend | up |
| Slope | +0.0104 |
| Distance from 37% (Overbought) | -4.1pp |
| Distance from 9.7% (Oversold) | +23.2pp |
| Date | 2026-08-14 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | ███░ 64 | 19.2 | NEUTRAL: 32.9% uptrend ratio, trend up |
| 2 | **Sector Participation** | 25% | ██░░ 51 | 12.8 | MODERATE: 8/11 sectors uptrending, spread 52.7% |
| 3 | **Sector Rotation** | 15% | ███░ 79 | 11.8 | RISK-ON: Cyclical leads by 14.8pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | ███░ 78 | 15.6 | POSITIVE MOMENTUM: slope=0.0090, strong accelerating |
| 5 | **Historical Context** | 10% | ████ 82 | 8.2 | ABOVE AVERAGE: 32.9% at 81.6th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 32.9%
- **10-Day MA:** 27.7%
- **Trend:** up
- **Slope:** +0.0104
- **Trend Adjustment:** +5

### 2. Sector Participation

- **Uptrending Sectors:** 8/11
- **Count Score:** 80/100
- **Spread:** 52.7% (score: 7/100)
- **Overbought (>37%):** 3 sectors (Energy, Technology, Healthcare)
- **Oversold (<9.7%):** 2 sectors (Real Estate, Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 32.4%
- **Defensive Avg:** 17.6%
- **Commodity Avg:** 42.0%
- **Cyclical-Defensive Gap:** 14.8pp
- **Late Cycle Warning:** YES (commodity penalty: -5)
- **Divergence Warning:** YES (penalty: -5)
  - **Defensive Divergence:** std=0.1496, spread=0.3949
    - Outlier: Healthcare (deviation: +0.2431)
    - Trend dissenter: Healthcare (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 42.3% | Up | +0.0306 |
| Consumer Cyclical | 24.7% | Up | +0.0036 |
| Communication Services | 29.4% | Up | +0.0094 |
| Financial | 31.4% | Up | +0.0039 |
| Industrials | 34.3% | Up | +0.0213 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 2.5% | Down | -0.0037 |
| Consumer Defensive | 17.1% | Down | -0.0034 |
| Healthcare | 42.0% | Up | +0.0139 |
| Real Estate | 9.1% | Down | -0.0155 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 55.2% | Up | +0.0071 |
| Basic Materials | 28.9% | Up | +0.0020 |


### 4. Momentum

- **Raw Slope:** +0.0104 
- **Smoothed Slope (EMA(3)):** +0.0090 (score: 72/100)
- **Acceleration (10v10):** 0.006814 (strong_accelerating, score: 90/100)
- **Sector Slope Breadth:** 8/11 positive (score: 73/100)

### 5. Historical Context

- **Current Ratio:** 32.9%
- **Percentile Rank:** 81.6th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.8%
- **30-Day Avg:** 25.6%
- **90-Day Avg:** 26.2%
- **Data Points:** 779 (2023-08-11 to 2026-08-14)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 55.2% | 91/165 | 42.6% | Up | +0.0071 | Overbought |
| 2 | Technology | 42.3% | 179/423 | 27.7% | Up | +0.0306 | Overbought |
| 3 | Healthcare | 42.0% | 180/429 | 31.5% | Up | +0.0139 | Overbought |
| 4 | Industrials | 34.3% | 135/394 | 29.2% | Up | +0.0213 | Normal |
| 5 | Financial | 31.4% | 188/598 | 30.3% | Up | +0.0039 | Normal |
| 6 | Communication Services | 29.4% | 32/109 | 24.7% | Up | +0.0094 | Normal |
| 7 | Basic Materials | 28.9% | 46/159 | 26.9% | Up | +0.0020 | Normal |
| 8 | Consumer Cyclical | 24.7% | 71/287 | 27.8% | Up | +0.0036 | Normal |
| 9 | Consumer Defensive | 17.1% | 21/123 | 15.1% | Down | -0.0034 | Normal |
| 10 | Real Estate | 9.1% | 13/143 | 11.7% | Down | -0.0155 | Oversold |
| 11 | Utilities | 2.5% | 2/81 | 2.6% | Down | -0.0037 | Oversold |

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
