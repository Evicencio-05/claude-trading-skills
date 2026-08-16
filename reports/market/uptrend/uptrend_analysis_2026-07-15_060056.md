# Uptrend Analyzer Report

**Generated:** 2026-07-15 06:00:56
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **34.1/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Upper |
| **Zone Proximity** | **Near boundary: -5.9 points from 40 (below)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -3 (raw: 37.1/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (52/100) |
| **Weakest Component** | Momentum (28/100) |
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
| Uptrend Ratio | 24.3% |
| 10-Day MA | 27.0% |
| Trend | down |
| Slope | -0.0079 |
| Distance from 37% (Overbought) | -12.7pp |
| Distance from 9.7% (Oversold) | +14.6pp |
| Date | 2026-07-14 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 33 | 9.9 | WEAK: 24.3% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ██░░ 42 | 10.5 | MODERATE: 2/11 sectors uptrending, spread 27.7% |
| 3 | **Sector Rotation** | 15% | █░░░ 39 | 5.8 | DEFENSIVE TILT: Defensive leads by 5.1pp |
| 4 | **Momentum** | 20% | █░░░ 28 | 5.6 | WEAK MOMENTUM: slope=-0.0063, strong decelerating |
| 5 | **Historical Context** | 10% | ██░░ 52 | 5.2 | NEAR MEDIAN: 24.3% at 51.7th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 24.3%
- **10-Day MA:** 27.0%
- **Trend:** down
- **Slope:** -0.0079
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 2/11
- **Count Score:** 20/100
- **Spread:** 27.7% (score: 75/100)
- **Overbought (>37%):** 1 sectors (Healthcare)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 20.9%
- **Defensive Avg:** 26.0%
- **Commodity Avg:** 20.9%
- **Cyclical-Defensive Gap:** -5.1pp
- **Divergence Warning:** YES (penalty: -5)
  - **Defensive Divergence:** std=0.087, spread=0.2252
    - Trend dissenter: Utilities (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 17.4% | Down | -0.0148 |
| Consumer Cyclical | 14.3% | Down | -0.0137 |
| Communication Services | 25.5% | Down | -0.0009 |
| Financial | 30.6% | Down | -0.0028 |
| Industrials | 16.8% | Down | -0.0214 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 16.0% | Up | +0.0025 |
| Consumer Defensive | 20.2% | Down | -0.0036 |
| Healthcare | 38.6% | Down | -0.0090 |
| Real Estate | 29.4% | Down | +0.0000 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 31.0% | Up | +0.0150 |
| Basic Materials | 10.9% | Down | -0.0066 |


### 4. Momentum

- **Raw Slope:** -0.0079
- **Smoothed Slope (EMA(3)):** -0.0063 (score: 42/100)
- **Acceleration (10v10):** -0.005416 (strong_decelerating, score: 10/100)
- **Sector Slope Breadth:** 2/11 positive (score: 18/100)

### 5. Historical Context

- **Current Ratio:** 24.3%
- **Percentile Rank:** 51.7th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.8%
- **30-Day Avg:** 26.4%
- **90-Day Avg:** 23.3%
- **Data Points:** 757 (2023-08-11 to 2026-07-14)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 38.6% | 162/420 | 48.3% | Down | -0.0090 | Overbought |
| 2 | Energy | 31.0% | 49/158 | 20.7% | Up | +0.0150 | Normal |
| 3 | Financial | 30.6% | 190/621 | 33.0% | Down | -0.0028 | Normal |
| 4 | Real Estate | 29.4% | 42/143 | 28.4% | Down | +0.0000 | Normal |
| 5 | Communication Services | 25.5% | 28/110 | 24.6% | Down | -0.0009 | Normal |
| 6 | Consumer Defensive | 20.2% | 24/119 | 23.1% | Down | -0.0036 | Normal |
| 7 | Technology | 17.4% | 73/420 | 17.2% | Down | -0.0148 | Normal |
| 8 | Industrials | 16.8% | 66/392 | 21.9% | Down | -0.0214 | Normal |
| 9 | Utilities | 16.0% | 13/81 | 14.0% | Up | +0.0025 | Normal |
| 10 | Consumer Cyclical | 14.3% | 40/279 | 19.5% | Down | -0.0137 | Normal |
| 11 | Basic Materials | 10.9% | 16/147 | 12.7% | Down | -0.0066 | Normal |

> **Note on Status vs Trend:**
> Status (Overbought/Normal/Oversold) reflects the ratio *level* relative to thresholds.
> Trend (Up/Down) reflects the *direction* of the 10-day MA slope.
> These can diverge:
> - **Overbought + Down** = high level but momentum rolling over (warning)
> - **Oversold + Up** = low level but momentum improving (potential recovery)
> - **Healthcare**: Overbought (38.6%) / Trend Down

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
