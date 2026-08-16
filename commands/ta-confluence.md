---
description: "Fuse TradeWhisperer candle lists (HTF stacks), Skylit GEX/VEX maps, and operator charts into a PLAY/WATCH/NO_TRADE brief with judgment coaching. Modes: candle_first | map_first."
argument-hint: "[candle_first|map_first] [daily|weekly|monthly] [bias: long|short|either] [TICKER]"
---

# /ta-confluence

Combine the three TA intake sources into a **setup brief**. Co-pilot only — no MCP orders, no news/FMP, no scraping.

**Artifact paths:** key `ta_confluence` → `reports/charts/confluence/`.

**TW color SoT:** Patreon **lists** (`list_tw_*`). Charts optional for structure. Resolve stacks with `uv run python3 scripts/tw_list_resolve.py`.

---

## Invoke

```
/ta-confluence candle_first daily bias: long
/ta-confluence map_first weekly bias: either
/ta-confluence map_first UMAC
```

Paste TW **lists** (prefer text), plus GEX/VEX and operator charts as needed. TW chart screenshots are optional.

---

## PHASE 0 — MODE AND PERIOD

Parse overrides (defaults in parentheses):

| Override | Default | Effect |
|----------|---------|--------|
| `candle_first` / `map_first` | Infer from inputs; else ask once | Entry path |
| `daily` / `weekly` / `monthly` | From TW list title if present; else `daily` | Period for TW color / shortlist |
| `bias: long` / `short` / `either` | `long` for candle_first; `either` for map_first | Shortlist filter |
| `override play` | off | Allow PLAY despite hard stop — must record reason |

Load:

- [confluence_rubric.md](../.cursor/skills/ta-confluence/references/confluence_rubric.md)
- [judgment_prompts.md](../.cursor/skills/ta-confluence/references/judgment_prompts.md)

---

## PHASE 1 — SOURCE ASSEMBLE

Reuse intake skills; write/read artifacts under `reports/charts/`. Do not re-implement extraction.

### candle_first

1. Ingest TW **lists** via `tradewhisperer-charts` (period list required for the session period). Also ingest weekly/monthly lists when pasted or already on disk for the same `as_of`.
2. Run `uv run python3 scripts/tw_list_resolve.py shortlist --period {period} --as-of {as_of} --bias {bias}` (or equivalent library call) for the shortlist.
3. For each shortlist / operator-chosen ticker, run `… stack TICKER --as-of {as_of} --bias {bias} --period {period}` → `tw_stack` + HTF fight.
4. Optional: ingest TW **charts** for finalists (structure only). List color wins on conflict → note under `gaps`.
5. Ask operator which shortlist tickers to map (or accept “all primary”).
6. Ingest **GEX + VEX** per ticker via `gex-vex-maps` (prefer both).
7. For finalists, require **operator-charts** paste — stop and ask if missing.

### map_first

1. Ingest pasted **GEX/VEX** via `gex-vex-maps`; drop empty/weak maps.
2. Rank by |king| and structure.
3. Resolve TW color via list stack: same-day `list_tw_{period}_*` + `tw_list_resolve.py stack`. Chart-only color is insufficient for PLAY — ingest list if missing.
4. Require **operator-charts** for any ticker considered for PLAY.

If a source is missing, note `gaps` and continue with capped verdicts.

---

## PHASE 2 — CONFLUENCE SCORE

For each ticker with enough data, score 0–100 per [confluence_rubric.md](../.cursor/skills/ta-confluence/references/confluence_rubric.md).

Use `tw_stack` for the HTF factor / hard stops (`htf_fight` from resolver). Apply hard stops (missing operator chart → max WATCH; hard TW↔map / fierce HTF fight → NO_TRADE unless override; missing period **list** color → cannot PLAY).

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
  "shortlist": [{"ticker": "UMAC", "tw_color": "BLUE", "tw_stack": {"daily": "BLUE", "weekly": "GREEN", "monthly": null}, "score": 72, "verdict": "WATCH"}],
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
  "tw_color": "BLUE",
  "tw_stack": {"daily": "BLUE", "weekly": "GREEN", "monthly": null},
  "htf": {"fight": false, "fierce": false, "htf_absent": false, "score_guide": "full"},
  "artifacts": {
    "tw_lists": {
      "daily": "reports/charts/tradewhisperer/list_tw_daily_YYYY-MM-DD.json",
      "weekly": "reports/charts/tradewhisperer/list_tw_weekly_YYYY-MM-DD.json",
      "monthly": null
    },
    "tw_chart": null,
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

## PHASE 5 — PREDICTION LOG (v1.5)

After persist, append rows per [prediction_log_v15.md](../.cursor/skills/ta-confluence/references/prediction_log_v15.md)
to `reports/charts/confluence/prediction_log_{as_of}.md` (optional `.json`).

Skip if the session was a dry fixture with no operator judgment. Fill `outcome_*`
on later days for taken PLAY/WATCH that became trades (Portfolio C or A only).

---

## Non-goals

- Auto thesis_store / Agentic orders
- Scraping Patreon or Skylit
- Deep-research / news
- PLAY without operator chart
- PLAY from chart-inferred TW color without a period list
- IRA thesis logging
