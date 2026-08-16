# Options Flow Tail Rubric

Reference for Phase 3 scoring in [options-flow-tail.md](../../../commands/options-flow-tail.md).

**Philosophy:** Tail the **thesis**, not the contract. Institutional whales often use size, leverage, and hedges unavailable to retail. The goal is directional conviction with defined risk.

---

## Hard disqualifiers

Mark row `DISQUALIFIED` (score 0). Still include in pass list with reason.

| Rule | Condition | Reason label |
|------|-----------|--------------|
| Wrong-side aggression | Tail long bias + bearish print (bid-side call buy or ask-side put for bullish tail) | `wrong_side` |
| Likely closing | Volume ≪ OI AND ΔOI flat or negative AND ΔOI% near 0 | `likely_closing` |
| Earnings trap | Earnings within DTE AND user did not request event play | `earnings_inside_dte` |
| ETF/index (single-name mode) | Ticker is ETF/index (USO, SPY, QQQ, IWM, XLE, etc.) when `single-name only` | `etf_flow` |
| Extreme chase | Option `day_pct` or `chg_pct` > 100% (already ripped) | `chasing` |
| Below premium floor | Premium < `min_premium` override | `below_floor` |
| Wrong bias | `bias: long` but row is bearish put tail candidate (or inverse) | `bias_mismatch` |

When evidence is ambiguous (e.g. OI data missing), do not disqualify — penalize in opening-evidence component instead.

---

## Weighted score (0–100)

Apply to survivors only. Each component is 0–100 internally, then weighted.

| Component | Weight | Scoring guide |
|-----------|--------|---------------|
| **Premium size** | 25% | $3M+ → 100; $1M–3M → 80; $500K–1M → 60; $250K–500K → 40 |
| **Ask-side aggression** | 20% | ASK ≥ 90% → 100; 75–89% → 75; 60–74% → 50; < 60% → 25 |
| **Opening evidence** | 20% | Vol ≥ OI → 100; Vol > 0.5× OI + positive ΔOI% → 75; Vol > 0.25× OI → 50; else 25 |
| **Sentiment confluence** | 15% | Contract bull ≥ 95% + chain bull aligned → 100; contract bull ≥ 90% + chain MID → 60; contract bull ≥ 80% + chain bear → 20 |
| **Tradeability** | 10% | DTE 14–45 + OTM 2–8% → 100; DTE 7–13 or OTM 8–15% → 60; DTE 0–6 or OTM > 15% → 30 |
| **Event / chase penalty** | 10% | Start at 100; −30 if earnings ≤ DTE; −20 if day_pct > 50%; −15 if IV unknown but OTM > 10% on ≤7 DTE |

**Formula:** `tail_score = round(Σ component × weight)`

---

## Enrichment adjustments (Phase 4)

Applied after base score; cap final `adjusted_score` at 100.

| Signal | Adjustment |
|--------|------------|
| Entry watchlist Tier A | +10 |
| Entry watchlist Tier B | +5 |
| Entry watchlist Tier D | −5 |
| Actionable research report (<14d) | +5 |
| Stale research (>14d) | −3 |
| Sector top-3 rotation + aligned bias | +5 |
| Sector lagging / defensive mismatch | −5 |
| Earnings inside DTE (confirmed) | −15 on primary only |

---

## Chain sentiment parsing

| Screener value | Treat as |
|----------------|----------|
| `BULL NN%` | Bullish chain |
| `BEAR NN%` | Bearish chain |
| `MID` | Neutral / mixed |

**Confluence bonus:** Contract BULL ≥ 95% AND chain BULL ≥ 55% → strong tail candidate.

**Confluence penalty:** Contract BULL ≥ 90% BUT chain MID or opposite → reduce sentiment component; note in pass reasoning if severe.

---

## IRA account penalties

When `account: ira`:

- Naked short options, undefined-risk spreads → mark structure **ineligible** in Phase 5.
- Do not disqualify flow row solely for IRA — adjust lite structure recommendation instead.

---

## Verdict thresholds

| Adjusted score | Interpretation |
|----------------|----------------|
| ≥ 75 | Strong tail candidate |
| 60–74 | Acceptable with Medium confidence |
| < 60 | Pass unless user explicitly wants lottery tail |

Primary pick requires adjusted score ≥ 60 AND passes market gate (Phase 1), unless user overrides.

---

## Sector clustering

When multiple rows share a theme (e.g. ALAB, LRCX, STM all semis):

- Note **theme cluster** in primary thesis.
- Prefer highest-scored name with best liquidity / research support.
- Do not tail entire cluster unless user asks — one primary + one runner-up max.

---

## Common pass reasons (quick reference)

| Ticker pattern | Typical reason |
|----------------|----------------|
| USO, GLD, SLV | Commodity ETF — macro, not single-name |
| MSTR | High beta proxy — chain often MID despite size |
| ≤6 DTE OTM calls | Lottery structure — tail direction via spread/stock |
| Duplicate ticker two strikes | Pick higher ΔOI / ASK%; pass the other |
