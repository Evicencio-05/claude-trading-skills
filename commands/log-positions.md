---
description: "Log positions to trader-memory-core via pending_ingest.json (sync) or Robinhood MCP snapshot. Asks only thesis, confidence, stop, and target."
---

# /log-positions

Log open positions to **trader-memory-core** with minimal human input (four questions per position).

**Scope:** Portfolio **A** (taxable) and **C** (Agentic) only. **Do not log Portfolio B (IRA)** — operator discontinued.

## Two ingestion sources

| Source | When to use | Data origin |
|--------|-------------|-------------|
| **A — Sync** | Portfolio A taxable; scheduled daily | `scripts/robinhood_sync.py` → `state/pending_ingest.json` |
| **B — MCP CLI** | Agentic (C) and/or taxable (A) | `scripts/robinhood_mcp.py ingest-pending` |

**Portfolio B (IRA):** Skip — do not run four-questions for `ira_robinhood`.

**Portfolio C (Agentic):** Prefer **Source B** when MCP is connected in Cursor.

Setup: [project-docs/reference/robinhood-mcp-integration.md](../project-docs/reference/robinhood-mcp-integration.md)

---

## Source A — Sync file (default)

```bash
uv run python3 scripts/robinhood_sync.py
```

Then run the prompt below against `state/pending_ingest.json`.

---

## Source B — MCP CLI

```bash
bash scripts/setup_robinhood_mcp.sh   # once
uv run python3 scripts/robinhood_mcp.py ingest-pending
# or --dry-run to preview
```

Account mapping: [config/robinhood_accounts.yaml](../config/robinhood_accounts.yaml) and [decisions.md](../decisions.md).

Equity positions only via MCP today. When ingesting, **filter out** `ira_robinhood` / IRA account numbers before asking questions.

Then run the shared prompt below.

---

## The Prompt (both sources)

```
Determine source:
  - If state/pending_ingest.json has PENDING_THESIS rows, use them.
  - Else if user asked for MCP log-positions, fetch via Robinhood MCP (Source B) first, then continue.

Find all positions where "status" is "PENDING_THESIS" and account is robinhood_taxable or robinhood_agentic (skip ira_robinhood).
If there are none, report: "No positions pending thesis input." and stop.

For each pending position, work through them ONE AT A TIME in this order:
  1. Options sorted by nearest expiry first
  2. Stocks after all options

For each position, display a pre-filled summary:

---
[N of TOTAL] TICKER — ASSET_TYPE
Account:    {account}
Direction:  {direction} {strategy if options}
Size:       {contracts} contracts / {size} shares
Avg cost:   ${avg_cost} per contract/share  (${total_cost} total)
Strike:     ${strike} {option_type} exp {expiry}   ← options only
IRA:        {ira_eligible}                          ← IRA accounts only
Auto-tags:  {tags}
---

Then ask ONLY these four questions in sequence:
  1. "Thesis in 2-4 sentences — why did you enter this position?"
  2. "Confidence 1-5?"
  3. "Stop level — price or condition that invalidates the thesis?"
  4. "Target — exit condition or price?"

After receiving all four answers, register the thesis:

  Preferred: tools/thesis-manager/ **Theses** page (writes via thesis_store API).

  Or: build thesis_data dict per trader-memory-core schema and call
  thesis_store.register(state_dir, thesis_data) from Python (see tools/thesis-manager/utils.py).

  Do NOT use thesis_ingest.py for manual/MCP positions — it only accepts screener JSON sources.

  Transition to ACTIVE if this is an existing open position with known entry:
  use thesis_store.open_position() after register when appropriate.

If registration succeeds and position came from pending_ingest.json:
  - Set position status from "PENDING_THESIS" to "INGESTED"
  - Add "ingested_at": current timestamp
  - Update state/synced_positions.json pending_keys / ingested_keys (Source A only)

Report at the end:
  "Logged N positions to trader-memory-core.
   Run: uv run python3 skills/trader-memory-core/scripts/thesis_store.py --state-dir state/theses/ list"
```

---

## After agentic-copilot-trade

When a plan JSON exists at `reports/logs/agentic_copilot_plan_{TICKER}_{DATE}.json` and the order was placed:

- Prefill thesis / stop / target / confidence from `agent_proposal` when present
- Still ask the four questions if any field is missing or the user wants to edit
- Tag account `robinhood_agentic`; do not mark IRA

---

## Notes

- For IRA positions, add tag `ira` if not present. Flag IRA-eligible on every options line.
- Skip any position where the user types "skip" — leave status as PENDING_THESIS.
- Do not ask for fields already in the JSON or MCP snapshot.
- Never edit YAML files under `state/theses/` directly.
