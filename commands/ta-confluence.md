---
description: "Fuse TradeWhisperer candles, Skylit GEX/VEX, and operator charts into a PLAY/WATCH/NO_TRADE brief with judgment coaching. Modes: candle_first | map_first."
argument-hint: "[candle_first|map_first] [daily|weekly|monthly] [bias: long|short|either] [TICKER]"
---

# /ta-confluence

Combine the three TA intake sources into a **setup brief**. Co-pilot only — no MCP orders, no news/FMP, no scraping.

**Artifact paths:** key `ta_confluence` → `reports/charts/confluence/`.

---

## Invoke

```
/ta-confluence candle_first daily bias: long
/ta-confluence map_first weekly bias: either
/ta-confluence map_first UMAC
```

Paste the relevant screenshots/lists in the same thread (TW list/charts, GEX/VEX, operator charts).

---

## PHASE 0 — MODE AND PERIOD

Parse overrides (defaults in parentheses):

| Override | Default | Effect |
|----------|---------|--------|
| `candle_first` / `map_first` | Infer from inputs; else ask once | Entry path |
| `daily` / `weekly` / `monthly` | From TW list title if present; else `daily` | Period for TW color |
| `bias: long` / `short` / `either` | `long` for candle_first; `either` for map_first | Shortlist filter |
| `override play` | off | Allow PLAY despite hard stop — must record reason |

Load:

- [confluence_rubric.md](../.cursor/skills/ta-confluence/references/confluence_rubric.md)
- [judgment_prompts.md](../.cursor/skills/ta-confluence/references/judgment_prompts.md)

---

## PHASE 1 — SOURCE ASSEMBLE

Reuse intake skills; write/read artifacts under `reports/charts/`. Do not re-implement extraction.

### candle_first

1. Ingest TW **list** (and optional charts) via `tradewhisperer-charts`.
2. Shortlist per rubric (BLUE/BLUE_GREEN for long; PINK/PINK_RED for short).
3. Ask operator which shortlist tickers to map (or accept “all primary”).
4. Ingest **GEX + VEX** per ticker via `gex-vex-maps` (prefer both).
5. For finalists, require **operator-charts** paste — stop and ask if missing.

### map_first

1. Ingest pasted **GEX/VEX** via `gex-vex-maps`; drop empty/weak maps.
2. Rank by |king| and structure.
3. Resolve TW color for period: use same-day `list_tw_{period}_*` if present, else ingest TW list/chart via `tradewhisperer-charts`.
4. Require **operator-charts** for any ticker considered for PLAY.

If a source is missing, note `gaps` and continue with capped verdicts.

---

## PHASE 2 — CONFLUENCE SCORE

For each ticker with enough data, score 0–100 per [confluence_rubric.md](../.cursor/skills/ta-confluence/references/confluence_rubric.md).

Apply hard stops (missing operator chart → max WATCH; hard TW↔map / HTF fight → NO_TRADE unless override).

Produce factor breakdown in JSON.

---

## PHASE 3 — JUDGMENT

For each ticker reaching WATCH or PLAY (and for interesting NO_TRADE if useful), fill [judgment_prompts.md](../.cursor/skills/ta-confluence/references/judgment_prompts.md):

- Devil’s advocate (2–3)
- Invalidation (TW / maps / operator)
- Not allowed to ignore
- R:R sketch from levels only
- Process grade
- One thing to verify

Verdict must be explicit: **PLAY** | **WATCH** | **NO_TRADE**.

---

## PHASE 4 — PERSIST

Create `reports/charts/confluence/` if needed.

| Scope | Files |
|-------|-------|
| Session | `session_confluence_{period}_{as_of}.json` + `.md` |
| Charted ticker | `{TICKER}_confluence_{as_of}.json` + `.md` |

### Session JSON shape

```json
{
  "source": "ta_confluence",
  "mode": "candle_first|map_first",
  "period": "daily|weekly|monthly",
  "bias": "long|short|either",
  "as_of": "YYYY-MM-DD",
  "shortlist": [{"ticker": "UMAC", "tw_color": "BLUE", "score": 72, "verdict": "WATCH"}],
  "gaps": [],
  "override": null
}
```

### Ticker JSON shape

```json
{
  "source": "ta_confluence",
  "ticker": "UMAC",
  "as_of": "YYYY-MM-DD",
  "mode": "map_first",
  "period": "daily",
  "bias": "long",
  "artifacts": {
    "tw": "reports/charts/tradewhisperer/...",
    "gex": "reports/charts/gex_vex/...",
    "vex": "reports/charts/gex_vex/...",
    "operator": "reports/charts/operator/..."
  },
  "score": 78,
  "factors": {},
  "verdict": "PLAY|WATCH|NO_TRADE",
  "judgment": {
    "devils_advocate": [],
    "invalidation": {},
    "not_allowed_to_ignore": [],
    "rr_sketch": {},
    "process_grade": {},
    "one_thing_to_verify": ""
  },
  "override": null,
  "gaps": []
}
```

Markdown: ranked table + per-ticker brief. Confirm paths in chat. **No trade plan sizing / MCP.**

---

## Non-goals

- Auto thesis_store / Agentic orders
- Scraping Patreon or Skylit
- Deep-research / news
- PLAY without operator chart
