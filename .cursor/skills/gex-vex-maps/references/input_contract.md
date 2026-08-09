# GEX / VEX — Input Contract

> **Status:** Active. Vendor: **Skylit Heatseeker™** screenshots. Guide: [skylit_heatseeker.md](skylit_heatseeker.md).

| Mode | Artifact stem |
|------|---------------|
| GEX | `{TICKER}_gex_{as_of}` |
| VEX | `{TICKER}_vex_{as_of}` |

Output: `reports/charts/gex_vex/`.

## Extract

`category` (gex|vex), `vendor: skylit`, `spot`, `change`/`change_pct`, `atm_strike`, `expirations`, `king_node`, `top_nodes` (by |value_k|), `nodes_near_spot`, `gatekeeper_candidates`, `air_pockets`, `range_edges`, `map_timestamp`, `confluence_with` (when sibling mode same session).

`value_k`: `$573K` → `573`, `-$83K` → `-83`.

## Rules

Abs value ranks King; ★ is hint. When both modes present, note overlapping strike/expiry zones. Levels only — no trade plan. No Skylit API.
