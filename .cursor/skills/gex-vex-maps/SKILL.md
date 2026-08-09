---
name: gex-vex-maps
description: >-
  Ingest Skylit Heatseeker GEX/VEX exposure map screenshots into dated artifacts.
  Use when the user pastes GEX, VEX, gamma/volatility heatmaps, Skylit Heatseeker,
  or says gex-vex-maps.
---

# GEX / VEX Maps

Follow [commands/gex-vex-maps.md](../../../commands/gex-vex-maps.md).

## Load during extract

| File | When |
|------|------|
| [references/input_contract.md](references/input_contract.md) | Always |
| [references/skylit_heatseeker.md](references/skylit_heatseeker.md) | Always |

## Output

| Mode | Files |
|------|-------|
| GEX | `{TICKER}_gex_{YYYY-MM-DD}.{md,json}` |
| VEX | `{TICKER}_vex_{YYYY-MM-DD}.{md,json}` |

Artifact key: `gex_vex_maps`.

## Guardrails

- Screenshots only — no Skylit API/MCP
- Abs value > color; context levels only — not trade signals
- Co-pilot only — no MCP orders
