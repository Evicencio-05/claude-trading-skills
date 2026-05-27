# Uptrend Analyzer Report

**Generated:** 2026-05-14 00:46:40
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **33.5/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Upper |
| **Zone Proximity** | **Near boundary: -6.5 points from 40 (below)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -10 (raw: 43.5/100) |
| **Active Warnings** | 3: LATE CYCLE WARNING, HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Sector Participation (54/100) |
| **Weakest Component** | Market Breadth (Overall) (32/100) |
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
| Uptrend Ratio | 24.0% |
| 10-Day MA | 26.5% |
| Trend | down |
| Slope | -0.0002 |
| Distance from 37% (Overbought) | -13.0pp |
| Distance from 9.7% (Oversold) | +14.3pp |
| Date | 2026-05-13 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 32 | 9.6 | WEAK: 24.0% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ██░░ 54 | 13.5 | MODERATE: 7/11 sectors uptrending, spread 40.1% |
| 3 | **Sector Rotation** | 15% | ██░░ 48 | 7.2 | BALANCED: Cyclical-Defensive gap 2.4pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | ██░░ 40 | 8.0 | NEUTRAL MOMENTUM: slope=-0.0027, strong decelerating |
| 5 | **Historical Context** | 10% | ██░░ 52 | 5.2 | NEAR MEDIAN: 24.0% at 51.7th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 24.0%
- **10-Day MA:** 26.5%
- **Trend:** down
- **Slope:** -0.0002
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 7/11
- **Count Score:** 60/100
- **Spread:** 40.1% (score: 45/100)
- **Overbought (>37%):** 2 sectors (Energy, Basic Materials)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 20.9%
- **Defensive Avg:** 18.5%
- **Commodity Avg:** 46.8%
- **Cyclical-Defensive Gap:** 2.4pp
- **Late Cycle Warning:** YES (commodity penalty: -10)
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0959, spread=0.2538
    - Outlier: Technology (deviation: +0.1530)
    - Trend dissenter: Technology (up vs majority down)
    - Trend dissenter: Communication Services (up vs majority down)
  - **Defensive Divergence:** std=0.0513, spread=0.1413
    - Outlier: Healthcare (deviation: +0.0809)
    - Trend dissenter: Real Estate (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 36.2% | Up | +0.0028 |
| Consumer Cyclical | 11.7% | Down | -0.0024 |
| Communication Services | 18.9% | Up | +0.0016 |
| Financial | 10.9% | Down | -0.0080 |
| Industrials | 26.9% | Down | -0.0064 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 12.5% | Up | +0.0005 |
| Consumer Defensive | 18.3% | Up | +0.0027 |
| Healthcare | 26.6% | Up | +0.0071 |
| Real Estate | 16.8% | Down | -0.0075 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 50.9% | Up | +0.0030 |
| Basic Materials | 42.8% | Up | +0.0196 |


### 4. Momentum

- **Raw Slope:** -0.0002
- **Smoothed Slope (EMA(3)):** -0.0027 (score: 49/100)
- **Acceleration (10v10):** -0.020941 (strong_decelerating, score: 10/100)
- **Sector Slope Breadth:** 7/11 positive (score: 64/100)

### 5. Historical Context

- **Current Ratio:** 24.0%
- **Percentile Rank:** 51.7th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 25.7%
- **90-Day Avg:** 26.4%
- **Data Points:** 713 (2023-08-11 to 2026-05-13)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 50.9% | 84/165 | 48.4% | Up | +0.0030 | Overbought |
| 2 | Basic Materials | 42.8% | 68/159 | 35.1% | Up | +0.0196 | Overbought |
| 3 | Technology | 36.2% | 146/403 | 36.8% | Up | +0.0028 | Normal |
| 4 | Industrials | 26.9% | 103/383 | 33.7% | Down | -0.0064 | Normal |
| 5 | Healthcare | 26.6% | 110/413 | 26.4% | Up | +0.0071 | Normal |
| 6 | Communication Services | 18.9% | 21/111 | 21.6% | Up | +0.0016 | Normal |
| 7 | Consumer Defensive | 18.3% | 21/115 | 17.1% | Up | +0.0027 | Normal |
| 8 | Real Estate | 16.8% | 24/143 | 21.8% | Down | -0.0075 | Normal |
| 9 | Utilities | 12.5% | 10/80 | 13.1% | Up | +0.0005 | Normal |
| 10 | Consumer Cyclical | 11.7% | 33/281 | 15.5% | Down | -0.0024 | Normal |
| 11 | Financial | 10.9% | 65/599 | 17.7% | Down | -0.0080 | Normal |

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
