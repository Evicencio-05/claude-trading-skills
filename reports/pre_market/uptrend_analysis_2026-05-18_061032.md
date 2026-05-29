# Uptrend Analyzer Report

**Generated:** 2026-05-18 06:10:32
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **15.9/100** |
| **Zone** | 🔴 Bear |
| **Zone Detail** | Bear |
| **Zone Proximity** | **Near boundary: -4.1 points from 20 (below)** |
| **Exposure Guidance** | Capital Preservation (0-30%) |
| **Warning Penalty** | -10 (raw: 25.9/100) |
| **Active Warnings** | 3: LATE CYCLE WARNING, HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (59/100) |
| **Weakest Component** | Sector Participation (1/100) |
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
| Uptrend Ratio | 20.8% |
| 10-Day MA | 25.2% |
| Trend | down |
| Slope | -0.0082 |
| Distance from 37% (Overbought) | -16.2pp |
| Distance from 9.7% (Oversold) | +11.1pp |
| Date | 2026-05-15 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 26 | 7.8 | VERY WEAK: 20.8% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ░░░░ 1 | 0.2 | VERY NARROW: 0/11 sectors uptrending, spread 54.1% |
| 3 | **Sector Rotation** | 15% | ██░░ 59 | 8.8 | BALANCED: Cyclical-Defensive gap 6.9pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | █░░░ 24 | 4.8 | WEAK MOMENTUM: slope=-0.0061, strong decelerating |
| 5 | **Historical Context** | 10% | ██░░ 42 | 4.2 | NEAR MEDIAN: 20.8% at 41.9th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 20.8%
- **10-Day MA:** 25.2%
- **Trend:** down
- **Slope:** -0.0082
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 0/11
- **Count Score:** 0/100
- **Spread:** 54.1% (score: 3/100)
- **Overbought (>37%):** 1 sectors (Energy)
- **Oversold (<9.7%):** 1 sectors (Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 20.0%
- **Defensive Avg:** 13.0%
- **Commodity Avg:** 39.9%
- **Cyclical-Defensive Gap:** 6.9pp
- **Late Cycle Warning:** YES (commodity penalty: -10)
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0858, spread=0.2205

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 32.4% | Down | -0.0049 |
| Consumer Cyclical | 10.5% | Down | -0.0099 |
| Communication Services | 21.1% | Down | -0.0014 |
| Financial | 10.4% | Down | -0.0112 |
| Industrials | 25.5% | Down | -0.0123 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 6.2% | Down | -0.0131 |
| Consumer Defensive | 14.9% | Down | -0.0056 |
| Healthcare | 19.8% | Down | -0.0030 |
| Real Estate | 11.3% | Down | -0.0123 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 60.2% | Down | -0.0020 |
| Basic Materials | 19.5% | Down | -0.0130 |


### 4. Momentum

- **Raw Slope:** -0.0082
- **Smoothed Slope (EMA(3)):** -0.0061 (score: 42/100)
- **Acceleration (10v10):** -0.016834 (strong_decelerating, score: 10/100)
- **Sector Slope Breadth:** 0/11 positive (score: 0/100)

### 5. Historical Context

- **Current Ratio:** 20.8%
- **Percentile Rank:** 41.9th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 26.5%
- **90-Day Avg:** 26.5%
- **Data Points:** 715 (2023-08-11 to 2026-05-15)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 60.2% | 100/166 | 47.5% | Down | -0.0020 | Overbought |
| 2 | Technology | 32.4% | 130/401 | 36.2% | Down | -0.0049 | Normal |
| 3 | Industrials | 25.5% | 97/381 | 31.4% | Down | -0.0123 | Normal |
| 4 | Communication Services | 21.1% | 23/109 | 21.3% | Down | -0.0014 | Normal |
| 5 | Healthcare | 19.8% | 81/409 | 26.3% | Down | -0.0030 | Normal |
| 6 | Basic Materials | 19.5% | 30/154 | 34.1% | Down | -0.0130 | Normal |
| 7 | Consumer Defensive | 14.9% | 17/114 | 15.7% | Down | -0.0056 | Normal |
| 8 | Real Estate | 11.3% | 16/142 | 19.9% | Down | -0.0123 | Normal |
| 9 | Consumer Cyclical | 10.5% | 29/276 | 13.6% | Down | -0.0099 | Normal |
| 10 | Financial | 10.4% | 62/598 | 15.6% | Down | -0.0112 | Normal |
| 11 | Utilities | 6.2% | 5/81 | 11.0% | Down | -0.0131 | Oversold |

> **Note on Status vs Trend:**
> Status (Overbought/Normal/Oversold) reflects the ratio *level* relative to thresholds.
> Trend (Up/Down) reflects the *direction* of the 10-day MA slope.
> These can diverge:
> - **Overbought + Down** = high level but momentum rolling over (warning)
> - **Oversold + Up** = low level but momentum improving (potential recovery)
> - **Energy**: Overbought (60.2%) / Trend Down

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
