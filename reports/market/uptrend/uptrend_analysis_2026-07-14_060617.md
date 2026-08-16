# Uptrend Analyzer Report

**Generated:** 2026-07-14 06:06:17
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **34.2/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Upper |
| **Zone Proximity** | **Near boundary: -5.8 points from 40 (below)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -3 (raw: 37.2/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (53/100) |
| **Weakest Component** | Market Breadth (Overall) (34/100) |
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
| Uptrend Ratio | 24.9% |
| 10-Day MA | 27.8% |
| Trend | down |
| Slope | -0.0066 |
| Distance from 37% (Overbought) | -12.1pp |
| Distance from 9.7% (Oversold) | +15.2pp |
| Date | 2026-07-13 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 34 | 10.2 | WEAK: 24.9% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | █░░░ 37 | 9.2 | NARROW: 2/11 sectors uptrending, spread 33.7% |
| 3 | **Sector Rotation** | 15% | █░░░ 38 | 5.7 | DEFENSIVE TILT: Defensive leads by 5.3pp |
| 4 | **Momentum** | 20% | █░░░ 34 | 6.8 | WEAK MOMENTUM: slope=-0.0047, decelerating |
| 5 | **Historical Context** | 10% | ██░░ 53 | 5.3 | NEAR MEDIAN: 24.9% at 53.2th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 24.9%
- **10-Day MA:** 27.8%
- **Trend:** down
- **Slope:** -0.0066
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 2/11
- **Count Score:** 20/100
- **Spread:** 33.7% (score: 63/100)
- **Overbought (>37%):** 1 sectors (Healthcare)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 21.0%
- **Defensive Avg:** 26.4%
- **Commodity Avg:** 17.9%
- **Cyclical-Defensive Gap:** -5.3pp
- **Divergence Warning:** YES (penalty: -5)
  - **Defensive Divergence:** std=0.1035, spread=0.2666
    - Outlier: Healthcare (deviation: +0.1759)
    - Trend dissenter: Utilities (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 17.8% | Down | -0.0086 |
| Consumer Cyclical | 15.4% | Down | -0.0135 |
| Communication Services | 23.4% | Down | -0.0044 |
| Financial | 32.3% | Down | -0.0007 |
| Industrials | 16.1% | Down | -0.0190 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 17.3% | Up | +0.0000 |
| Consumer Defensive | 22.5% | Down | -0.0029 |
| Healthcare | 43.9% | Down | -0.0036 |
| Real Estate | 21.7% | Down | -0.0149 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 25.6% | Up | +0.0086 |
| Basic Materials | 10.2% | Down | -0.0046 |


### 4. Momentum

- **Raw Slope:** -0.0066
- **Smoothed Slope (EMA(3)):** -0.0047 (score: 45/100)
- **Acceleration (10v10):** -0.004582 (decelerating, score: 25/100)
- **Sector Slope Breadth:** 2/11 positive (score: 18/100)

### 5. Historical Context

- **Current Ratio:** 24.9%
- **Percentile Rank:** 53.2th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.8%
- **30-Day Avg:** 26.4%
- **90-Day Avg:** 23.3%
- **Data Points:** 756 (2023-08-11 to 2026-07-13)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 43.9% | 185/421 | 49.2% | Down | -0.0036 | Overbought |
| 2 | Financial | 32.3% | 200/619 | 33.3% | Down | -0.0007 | Normal |
| 3 | Energy | 25.6% | 40/156 | 19.2% | Up | +0.0086 | Normal |
| 4 | Communication Services | 23.4% | 26/111 | 24.7% | Down | -0.0044 | Normal |
| 5 | Consumer Defensive | 22.5% | 27/120 | 23.4% | Down | -0.0029 | Normal |
| 6 | Real Estate | 21.7% | 31/143 | 28.4% | Down | -0.0149 | Normal |
| 7 | Technology | 17.8% | 75/421 | 18.7% | Down | -0.0086 | Normal |
| 8 | Utilities | 17.3% | 14/81 | 13.7% | Up | +0.0000 | Normal |
| 9 | Industrials | 16.1% | 63/392 | 24.0% | Down | -0.0190 | Normal |
| 10 | Consumer Cyclical | 15.4% | 43/279 | 20.8% | Down | -0.0135 | Normal |
| 11 | Basic Materials | 10.2% | 15/147 | 13.3% | Down | -0.0046 | Normal |

> **Note on Status vs Trend:**
> Status (Overbought/Normal/Oversold) reflects the ratio *level* relative to thresholds.
> Trend (Up/Down) reflects the *direction* of the 10-day MA slope.
> These can diverge:
> - **Overbought + Down** = high level but momentum rolling over (warning)
> - **Oversold + Up** = low level but momentum improving (potential recovery)
> - **Healthcare**: Overbought (43.9%) / Trend Down

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
