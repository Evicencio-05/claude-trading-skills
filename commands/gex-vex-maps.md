---
description: "Ingest Skylit Heatseeker GEX/VEX heatmap screenshots into dated markdown+JSON artifacts."
argument-hint: "<TICKER|SPX> [gex|vex|both]"
---

# /gex-vex-maps {TICKER}

Ingest **user-supplied** Skylit **GEX** and/or **VEX** maps. Screenshots only — no Skylit API. Co-pilot only.

**Paths:** `reports/charts/gex_vex/{TICKER}_gex_{as_of}` · `{TICKER}_vex_{as_of}`.

## PHASE 0 — INTAKE

Detect mode badge. Load [input_contract.md](../.cursor/skills/gex-vex-maps/references/input_contract.md) + [skylit_heatseeker.md](../.cursor/skills/gex-vex-maps/references/skylit_heatseeker.md).

## PHASE 1 — EXTRACT

Rank by |value_k|; set confluence when both modes provided.

## PHASE 2 — PERSIST

Write `.json` + `.md` per mode. No trade plan.
