# TA Confluence Rubric

Score each ticker 0–100 after sources are assembled. Verdict: **PLAY** / **WATCH** / **NO_TRADE**.

**TW color source of truth:** Patreon **lists** (`list_tw_*`) via `scripts/tw_list_resolve.py`. Chart-inferred color must not override list color.

## Factor weights

| Factor | Weight | Score guide |
|--------|--------|-------------|
| TW trigger color aligns with bias | 30 | Full: period **list** color BLUE/BLUE_GREEN (long) or PINK/PINK_RED (short). Half: GREEN (long) / RED (short) continuation only. Zero: wrong-side trigger or missing period list color. |
| HTF not fighting | 20 | Use `tw_stack` + `htf_fight`: **full** if `score_guide=full` (including HTF absent = weekly **and** monthly lists missing). **partial** if mixed. **zero** if clear/fierce fight. |
| GEX/VEX support direction | 25 | Full: king/gatekeepers/floors-ceilings agree with bias (see below). Half: one mode agrees, other neutral. Zero: maps fight bias or missing both modes. |
| GEX∩VEX overlap near thesis | 15 | Full: shared king/gatekeeper zone near intended level. Half: overlap far from spot. Zero: no overlap or single mode only. |
| Operator chart structure | 10 | Full: SMA + nearest fib/S/R/VP levels defined with asymmetric edge. Half: levels present but mid-chop / unclear edge. Zero: no operator chart. |

### Map direction heuristics (bias-aware)

**Long bias — supportive maps**

- Upside magnets / king above spot with path not blocked by hostile gatekeeper
- Floor building / rolling floors (downside magnets rising)
- Positive nodes near spot acting as support; avoid large negative air pocket immediately below if chasing

**Short bias — supportive maps**

- Ceiling / king below path of least resistance downward, or large nodes above as rejection
- Rolling ceilings (upside magnets shrinking / moving down)
- Negative nodes that amplify downside once broken (wicky) — note trap risk on overshoot

Absolute value outranks color. King can be yellow or purple.

## Hard stops (override score)

| Condition | Max verdict |
|-----------|-------------|
| Operator chart missing | **WATCH** (never PLAY) |
| Period **list** color missing (chart-only TW) | **WATCH** (never PLAY) |
| Hard TW vs map conflict (e.g. long + BLUE but maps clearly ceiling/bearish posture) | **NO_TRADE** unless operator chat-overrides |
| Fierce HTF fight (`htf.fierce` — e.g. daily BLUE under weekly/monthly RED/PINK_RED stack for long) | **NO_TRADE** default |
| Fierce HTF fight short (daily PINK under weekly/monthly GREEN/BLUE_GREEN stack) | **NO_TRADE** default |
| Operator mid-range with ~1:1 R:R and no map edge | **WATCH** or **NO_TRADE** |

Chat override: operator may force PLAY after hard stop — record `override: true` + reason in JSON; process grade must flag it.

## Verdict thresholds

| Score | Default verdict | Notes |
|-------|-----------------|-------|
| ≥ 75 | **PLAY** | Only if no hard stop |
| 50–74 | **WATCH** | Need confirmation / another TF / clearer chart edge |
| < 50 | **NO_TRADE** | Pass is success |

Missing operator chart always caps at WATCH even if raw score ≥ 75.
Missing period list color always caps at WATCH even if raw score ≥ 75.

## Candle-first shortlist filters

| Bias | Include from TW **list** |
|------|--------------------------|
| `long` | BLUE, BLUE_GREEN (primary); GREEN = context only, not auto-shortlist |
| `short` | PINK, PINK_RED (primary); RED = context; TRIM_OPTION = optional trim watch, not new short entry |
| `either` | BLUE, BLUE_GREEN, PINK, PINK_RED |

Period = list period (`daily` / `weekly` / `monthly`). Prefer matching GEX/VEX + operator timeframe to that period’s intent (daily list → daily chart; weekly list → weekly chart when available).

Use `tw_list_resolve.py shortlist` for the period list; score HTF from `stack` across daily/weekly/monthly list files for the same `as_of`.

## Map-first shortlist filters

1. Keep tickers with material |king| or top nodes (not all-zero maps).
2. Drop maps with no readable structure.
3. Rank by |king_node.value_k| then confluence_with overlap quality.
4. Then require period **list** color (via stack resolver) before PLAY.
