# Uptrend Analyzer Report

**Generated:** 2026-05-15 06:00:48
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **26.7/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Lower |
| **Zone Proximity** | **Near boundary: +6.7 points from 20 (above)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -10 (raw: 36.7/100) |
| **Active Warnings** | 3: LATE CYCLE WARNING, HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Rotation (55/100) |
| **Weakest Component** | Sector Participation (29/100) |
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
| Uptrend Ratio | 24.6% |
| 10-Day MA | 26.0% |
| Trend | down |
| Slope | -0.0055 |
| Distance from 37% (Overbought) | -12.4pp |
| Distance from 9.7% (Oversold) | +14.9pp |
| Date | 2026-05-14 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 33 | 9.9 | WEAK: 24.6% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | █░░░ 29 | 7.2 | NARROW: 2/11 sectors uptrending, spread 40.9% |
| 3 | **Sector Rotation** | 15% | ██░░ 55 | 8.2 | BALANCED: Cyclical-Defensive gap 5.1pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | █░░░ 30 | 6.0 | WEAK MOMENTUM: slope=-0.0041, strong decelerating |
| 5 | **Historical Context** | 10% | ██░░ 53 | 5.3 | NEAR MEDIAN: 24.6% at 52.9th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 24.6%
- **10-Day MA:** 26.0%
- **Trend:** down
- **Slope:** -0.0055
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 2/11
- **Count Score:** 20/100
- **Spread:** 40.9% (score: 42/100)
- **Overbought (>37%):** 1 sectors (Energy)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 23.0%
- **Defensive Avg:** 17.9%
- **Commodity Avg:** 43.9%
- **Cyclical-Defensive Gap:** 5.1pp
- **Late Cycle Warning:** YES (commodity penalty: -10)
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0995, spread=0.2535
  - **Defensive Divergence:** std=0.0505, spread=0.1332
    - Outlier: Healthcare (deviation: +0.0775)
    - Trend dissenter: Healthcare (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 36.8% | Down | -0.0010 |
| Consumer Cyclical | 11.5% | Down | -0.0097 |
| Communication Services | 23.4% | Down | -0.0009 |
| Financial | 12.5% | Down | -0.0099 |
| Industrials | 30.8% | Down | -0.0109 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 12.3% | Down | -0.0081 |
| Consumer Defensive | 14.8% | Down | -0.0085 |
| Healthcare | 25.7% | Up | +0.0017 |
| Real Estate | 18.9% | Down | -0.0061 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 52.4% | Down | -0.0063 |
| Basic Materials | 35.4% | Up | +0.0030 |


### 4. Momentum

- **Raw Slope:** -0.0055
- **Smoothed Slope (EMA(3)):** -0.0041 (score: 46/100)
- **Acceleration (10v10):** -0.018954 (strong_decelerating, score: 10/100)
- **Sector Slope Breadth:** 2/11 positive (score: 18/100)

### 5. Historical Context

- **Current Ratio:** 24.6%
- **Percentile Rank:** 52.9th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.5%
- **30-Day Avg:** 26.1%
- **90-Day Avg:** 26.4%
- **Data Points:** 714 (2023-08-11 to 2026-05-14)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 52.4% | 87/166 | 47.8% | Down | -0.0063 | Overbought |
| 2 | Technology | 36.8% | 148/402 | 36.6% | Down | -0.0010 | Normal |
| 3 | Basic Materials | 35.4% | 56/158 | 35.4% | Up | +0.0030 | Normal |
| 4 | Industrials | 30.8% | 118/383 | 32.6% | Down | -0.0109 | Normal |
| 5 | Healthcare | 25.7% | 106/413 | 26.5% | Up | +0.0017 | Normal |
| 6 | Communication Services | 23.4% | 26/111 | 21.5% | Down | -0.0009 | Normal |
| 7 | Real Estate | 18.9% | 27/143 | 21.1% | Down | -0.0061 | Normal |
| 8 | Consumer Defensive | 14.8% | 17/115 | 16.3% | Down | -0.0085 | Normal |
| 9 | Financial | 12.5% | 75/600 | 16.7% | Down | -0.0099 | Normal |
| 10 | Utilities | 12.3% | 10/81 | 12.3% | Down | -0.0081 | Normal |
| 11 | Consumer Cyclical | 11.5% | 32/279 | 14.6% | Down | -0.0097 | Normal |

> **Note on Status vs Trend:**
> Status (Overbought/Normal/Oversold) reflects the ratio *level* relative to thresholds.
> Trend (Up/Down) reflects the *direction* of the 10-day MA slope.
> These can diverge:
> - **Overbought + Down** = high level but momentum rolling over (warning)
> - **Oversold + Up** = low level but momentum improving (potential recovery)
> - **Energy**: Overbought (52.4%) / Trend Down

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
