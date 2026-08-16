# Uptrend Analyzer Report

**Generated:** 2026-07-17 17:13:38
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **36.4/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Upper |
| **Zone Proximity** | **Near boundary: -3.6 points from 40 (below)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -3 (raw: 39.4/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (58/100) |
| **Weakest Component** | Momentum (33/100) |
| **Data Quality** | Complete (5/5 components) |
| **Confidence** | High (moderate, Both regime coverage) |

> **Guidance:** Weak breadth environment. Prioritize capital preservation over gains.

---

## Active Warnings

### SECTOR DIVERGENCE WARNING
> Significant divergence detected within sector groups. Some sectors within the same group are moving in opposite directions, suggesting hidden risk beneath the averages.

- Verify individual sector trends before entering positions
- Avoid sectors diverging from their group majority
- Monitor for group convergence or further deterioration

---

## Current Market Snapshot

| Metric | Value |
|--------|-------|
| Uptrend Ratio | 26.4% |
| 10-Day MA | 26.0% |
| Trend | down |
| Slope | -0.0020 |
| Distance from 37% (Overbought) | -10.6pp |
| Distance from 9.7% (Oversold) | +16.7pp |
| Date | 2026-07-17 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 38 | 11.4 | WEAK: 26.4% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | █░░░ 39 | 9.8 | NARROW: 3/11 sectors uptrending, spread 31.4% |
| 3 | **Sector Rotation** | 15% | █░░░ 39 | 5.8 | DEFENSIVE TILT: Defensive leads by 5.1pp |
| 4 | **Momentum** | 20% | █░░░ 33 | 6.6 | WEAK MOMENTUM: slope=-0.0030, strong decelerating |
| 5 | **Historical Context** | 10% | ██░░ 58 | 5.8 | NEAR MEDIAN: 26.4% at 57.7th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 26.4%
- **10-Day MA:** 26.0%
- **Trend:** down
- **Slope:** -0.0020
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 3/11
- **Count Score:** 20/100
- **Spread:** 31.4% (score: 67/100)
- **Overbought (>37%):** 3 sectors (Energy, Real Estate, Healthcare)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 22.3%
- **Defensive Avg:** 27.4%
- **Commodity Avg:** 26.7%
- **Cyclical-Defensive Gap:** -5.1pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0644, spread=0.1933
    - Outlier: Financial (deviation: +0.1153)
    - Trend dissenter: Technology (up vs majority down)
  - **Defensive Divergence:** std=0.1209, spread=0.2681
    - Trend dissenter: Real Estate (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 14.5% | Up | +0.0013 |
| Consumer Cyclical | 22.2% | Down | -0.0022 |
| Communication Services | 22.3% | Down | -0.0020 |
| Financial | 33.8% | Down | -0.0011 |
| Industrials | 18.6% | Down | -0.0066 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 13.8% | Down | -0.0023 |
| Consumer Defensive | 16.9% | Down | -0.0097 |
| Healthcare | 38.2% | Down | -0.0138 |
| Real Estate | 40.6% | Up | +0.0061 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 42.4% | Up | +0.0303 |
| Basic Materials | 11.0% | Down | -0.0050 |


### 4. Momentum

- **Raw Slope:** -0.0020
- **Smoothed Slope (EMA(3)):** -0.0030 (score: 48/100)
- **Acceleration (10v10):** -0.00703 (strong_decelerating, score: 10/100)
- **Sector Slope Breadth:** 3/11 positive (score: 27/100)

### 5. Historical Context

- **Current Ratio:** 26.4%
- **Percentile Rank:** 57.7th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.8%
- **30-Day Avg:** 26.9%
- **90-Day Avg:** 23.6%
- **Data Points:** 760 (2023-08-11 to 2026-07-17)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 42.4% | 67/158 | 26.9% | Up | +0.0303 | Overbought |
| 2 | Real Estate | 40.6% | 58/143 | 30.2% | Up | +0.0061 | Overbought |
| 3 | Healthcare | 38.2% | 161/422 | 44.4% | Down | -0.0138 | Overbought |
| 4 | Financial | 33.8% | 209/618 | 32.6% | Down | -0.0011 | Normal |
| 5 | Communication Services | 22.3% | 25/112 | 24.1% | Down | -0.0020 | Normal |
| 6 | Consumer Cyclical | 22.2% | 62/279 | 18.6% | Down | -0.0022 | Normal |
| 7 | Industrials | 18.6% | 73/393 | 19.1% | Down | -0.0066 | Normal |
| 8 | Consumer Defensive | 16.9% | 20/118 | 20.0% | Down | -0.0097 | Normal |
| 9 | Technology | 14.5% | 60/414 | 16.5% | Up | +0.0013 | Normal |
| 10 | Utilities | 13.8% | 11/80 | 14.0% | Down | -0.0023 | Normal |
| 11 | Basic Materials | 11.0% | 16/145 | 11.1% | Down | -0.0050 | Normal |

> **Note on Status vs Trend:**
> Status (Overbought/Normal/Oversold) reflects the ratio *level* relative to thresholds.
> Trend (Up/Down) reflects the *direction* of the 10-day MA slope.
> These can diverge:
> - **Overbought + Down** = high level but momentum rolling over (warning)
> - **Oversold + Up** = low level but momentum improving (potential recovery)
> - **Healthcare**: Overbought (38.2%) / Trend Down

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
