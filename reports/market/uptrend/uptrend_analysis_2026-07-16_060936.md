# Uptrend Analyzer Report

**Generated:** 2026-07-16 06:09:36
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **34.0/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Upper |
| **Zone Proximity** | **Near boundary: -6.0 points from 40 (below)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -3 (raw: 37.0/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (51/100) |
| **Weakest Component** | Momentum (29/100) |
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
| Uptrend Ratio | 24.0% |
| 10-Day MA | 26.3% |
| Trend | down |
| Slope | -0.0063 |
| Distance from 37% (Overbought) | -13.0pp |
| Distance from 9.7% (Oversold) | +14.3pp |
| Date | 2026-07-15 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 32 | 9.6 | WEAK: 24.0% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ██░░ 40 | 10.0 | MODERATE: 3/11 sectors uptrending, spread 29.4% |
| 3 | **Sector Rotation** | 15% | ██░░ 43 | 6.5 | DEFENSIVE TILT: Defensive leads by 3.6pp |
| 4 | **Momentum** | 20% | █░░░ 29 | 5.8 | WEAK MOMENTUM: slope=-0.0063, strong decelerating |
| 5 | **Historical Context** | 10% | ██░░ 51 | 5.1 | NEAR MEDIAN: 24.0% at 50.7th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 24.0%
- **10-Day MA:** 26.3%
- **Trend:** down
- **Slope:** -0.0063
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 3/11
- **Count Score:** 20/100
- **Spread:** 29.4% (score: 71/100)
- **Overbought (>37%):** 1 sectors (Healthcare)
- **Oversold (<9.7%):** 0 sectors ()

### 3. Sector Rotation

- **Cyclical Avg:** 21.0%
- **Defensive Avg:** 24.6%
- **Commodity Avg:** 16.9%
- **Cyclical-Defensive Gap:** -3.6pp
- **Divergence Warning:** YES (penalty: -5)
  - **Defensive Divergence:** std=0.1135, spread=0.2847
    - Trend dissenter: Consumer Defensive (down vs majority up)
    - Trend dissenter: Healthcare (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 15.2% | Down | -0.0089 |
| Consumer Cyclical | 18.3% | Down | -0.0062 |
| Communication Services | 23.9% | Down | -0.0022 |
| Financial | 32.0% | Down | -0.0042 |
| Industrials | 15.7% | Down | -0.0161 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 16.0% | Up | +0.0049 |
| Consumer Defensive | 11.9% | Down | -0.0138 |
| Healthcare | 40.3% | Down | -0.0068 |
| Real Estate | 30.3% | Up | +0.0034 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 22.8% | Up | +0.0067 |
| Basic Materials | 11.0% | Down | -0.0066 |


### 4. Momentum

- **Raw Slope:** -0.0063
- **Smoothed Slope (EMA(3)):** -0.0063 (score: 42/100)
- **Acceleration (10v10):** -0.006505 (strong_decelerating, score: 10/100)
- **Sector Slope Breadth:** 3/11 positive (score: 27/100)

### 5. Historical Context

- **Current Ratio:** 24.0%
- **Percentile Rank:** 50.7th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.8%
- **30-Day Avg:** 26.5%
- **90-Day Avg:** 23.4%
- **Data Points:** 758 (2023-08-11 to 2026-07-15)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Healthcare | 40.3% | 169/419 | 47.6% | Down | -0.0068 | Overbought |
| 2 | Financial | 32.0% | 199/621 | 32.6% | Down | -0.0042 | Normal |
| 3 | Real Estate | 30.3% | 43/142 | 28.7% | Up | +0.0034 | Normal |
| 4 | Communication Services | 23.9% | 27/113 | 24.4% | Down | -0.0022 | Normal |
| 5 | Energy | 22.8% | 36/158 | 21.4% | Up | +0.0067 | Normal |
| 6 | Consumer Cyclical | 18.3% | 51/278 | 18.8% | Down | -0.0062 | Normal |
| 7 | Utilities | 16.0% | 13/81 | 14.4% | Up | +0.0049 | Normal |
| 8 | Industrials | 15.7% | 62/394 | 20.3% | Down | -0.0161 | Normal |
| 9 | Technology | 15.2% | 64/421 | 16.3% | Down | -0.0089 | Normal |
| 10 | Consumer Defensive | 11.9% | 14/118 | 21.7% | Down | -0.0138 | Normal |
| 11 | Basic Materials | 11.0% | 16/146 | 12.0% | Down | -0.0066 | Normal |

> **Note on Status vs Trend:**
> Status (Overbought/Normal/Oversold) reflects the ratio *level* relative to thresholds.
> Trend (Up/Down) reflects the *direction* of the 10-day MA slope.
> These can diverge:
> - **Overbought + Down** = high level but momentum rolling over (warning)
> - **Oversold + Up** = low level but momentum improving (potential recovery)
> - **Healthcare**: Overbought (40.3%) / Trend Down

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
