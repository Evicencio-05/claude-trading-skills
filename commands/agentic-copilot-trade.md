---
description: "Agentic co-pilot: draft trade plan from research, size for Portfolio C, MCP order review — user confirms before place."
argument-hint: "[TICKER]"
---

# Agentic Co-Pilot Trade — {TICKER}

> **Co-pilot only:** User must confirm plan and order. No autonomous `place_equity_order` before Phase 3B ([PROJECT.md](../PROJECT.md)).
>
> **Account:** Portfolio C — `robinhood_agentic` only (`agentic_allowed: true` in [config/robinhood_accounts.yaml](../config/robinhood_accounts.yaml)). Never MCP trade IRA or taxable.
>
> **Config:** [config/agentic_copilot.yaml](../config/agentic_copilot.yaml) (copy from [agentic_copilot.yaml.example](../config/agentic_copilot.yaml.example)). Chat overrides win on conflict.
>
> **Artifact paths:** [scripts/report_paths.py](../scripts/report_paths.py) — plan JSON under `reports/logs/`.

Replace `{TICKER}` with the user symbol when provided; omit for assisted selection (PASS 0).

---

## PASS 0 — CONFIG AND TICKER

### 0a. Load effective config

1. If `config/agentic_copilot.yaml` exists, read it.
2. Else read `config/agentic_copilot.yaml.example` and state clearly: **using example defaults — copy to `config/agentic_copilot.yaml` for persistent overrides.**
3. Parse **chat overrides** from the user message (chat wins over YAML):

| Override (chat) | Maps to config key |
|-----------------|-------------------|
| `max_risk_dollars: N` | `sizing.max_risk_dollars` |
| `max_position_dollars: N` | `sizing.max_position_dollars` |
| `max_position_pct: N` | `sizing.max_position_pct` |
| `risk_pct: N` or `risk_pct: null` | `sizing.risk_pct` |
| `min_shares: N` | `sizing.min_shares` |
| `fixed_account_size: N` | `sizing.fixed_account_size` + `account_size_source: fixed` |
| `ignore posture` / `skip_posture` | `gates.require_new_entry_allowed: false` |
| `allow watch` / `skip actionable research` | `gates.require_actionable_research: false` |
| `stale_research_days: N` | `gates.stale_research_days` |
| `no plan artifact` | `learning.write_plan_artifact: false` |
| `add to position` | Set intent flag `add_to_existing: true` |

Merge into `effective_config` (document merged values in the plan artifact).

### 0b. Resolve {TICKER}

**If user provided a ticker** → uppercase, use it.

**Else (assisted selection):**

1. If latest `reports/logs/entry_watchlist_YYYY-MM-DD.json` exists (today ET preferred, else ≤1 trading day old), prefer rows with actionable research and highest tier/score. Present **≤5 options** if ambiguous.
2. Else ask the user for a ticker (do not invent conviction tiers). Optional TA handoff: latest PLAY from `reports/charts/confluence/`.
3. **STOP** until one ticker is resolved. Do not proceed to PASS 1 without it.

---

## PASS 1 — CONTEXT (read-only; no place order)

1. **Market context** — If today's `reports/logs/market_context_YYYY-MM-DD.json` (or `.md`) is missing:
   ```bash
   uv run python3 scripts/pre_market.py
   ```
   Read posture: `new_entry_allowed` (or equivalent). If `gates.require_new_entry_allowed` and posture blocks → **STOP** unless user overrode posture in chat.

2. **Broker snapshot** — Follow skill **robinhood-portfolio-review** (CLI primary):
   ```bash
   uv run python3 scripts/robinhood_mcp.py accounts
   uv run python3 scripts/robinhood_mcp.py positions --all
   ```
   Resolve Agentic `account_number` from [config/robinhood_accounts.yaml](../config/robinhood_accounts.yaml) (`thesis_store: robinhood_agentic`). Record buying power / equity for sizing.

3. **Research** — Read latest `reports/research/{TICKER}_*.md` (newest date suffix). If missing or stale per config → **STOP** (suggest `/update-research` or `/deep-research`) unless user disabled `require_actionable_research`.

4. **Optional TA confluence** — If `reports/charts/confluence/{TICKER}_confluence_*.json` exists for today/recent session, summarize verdict (PLAY/WATCH/NO_TRADE) in the gates block. Do not auto-override research gates.

5. **Gates summary** — One chat block: posture, Agentic buying power, research date, verdict, confluence if any.

---

## PASS 2 — DRAFT PLAN (wait for confirm)

1. Pull entry / stop / target / thesis from research Phase 11 (or equivalent trade plan section). If "No trade plan" and `require_actionable_research` → **STOP**.
2. Size with **position-sizer** using Agentic buying power and `effective_config.sizing` caps (`max_risk_dollars`, `max_position_dollars`, fractional when configured).
3. Present a clear plan block: ticker, account, shares/dollar_amount, entry, stop, target, max loss, thesis one-liner, confidence 1–5.
4. **STOP** — wait for exactly one of:
   - `confirm` — proceed to PASS 3 (review only)
   - `confirm plan and order` — PASS 3 then PASS 4 without a second STOP (still run review first)
   - `edit: …` — revise draft and re-present
   - `pass` — abort

---

## PASS 3 — MCP REVIEW

Call Robinhood Agentic MCP `review_equity_order` for Portfolio C only with the drafted order fields. Show review summary (quote, estimated shares, checks).

If user said only `confirm` (not `confirm plan and order`): **STOP** — wait for `confirm order` before PASS 4.

---

## PASS 4 — PLACE (gated)

Only after confirm:

1. Fresh `ref_id` for the place call.
2. MCP `place_equity_order` on **Agentic account only**.
3. Record `order_id`, `order_state`, `ref_id` in chat.

On failure: do not retry blindly; report MCP error and stop.

---

## PASS 5 — ARTIFACT + THESIS

1. If `learning.write_plan_artifact`, write:
   `reports/logs/agentic_copilot_plan_{TICKER}_{YYYY-MM-DD}.json`
   including `effective_config`, `agent_proposal`, `user_decision`, `user_overrides`, `review_summary`, order fields, `research_path`.
2. Register/update thesis via `thesis_store.py` (not raw YAML). Prefer `/log-positions` prefill for residual PENDING.
3. Never invent fills — log `order_state` as returned by MCP.

---

## Guardrails

- No place without explicit user confirm language above
- Never trade IRA / taxable via MCP
- Risk caps from user-editable config only — do not raise caps without user ask
- Prefer `/ta-confluence` PLAY as context, not as a bypass for research/posture gates
