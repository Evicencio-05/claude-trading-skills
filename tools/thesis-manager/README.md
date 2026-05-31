# Thesis Manager

Run:     streamlit run tools/thesis-manager/app.py
Purpose: Thesis input and position review for trader-memory-core
Data:    Reads state/theses/ and state/pending_ingest.json
Writes:  Calls thesis_store API (never directly edits YAML files)

## Navigation

Five pages via sidebar radio: **Dashboard**, **Research**, **Reports**, **Theses**, **Review**.

Cross-page links (e.g. Dashboard **Go to Research**, **Manage in Theses**) set `nav_page` and jump on the next rerun.

## Theses page (CRUD)

Single home for thesis lifecycle — create, sync ingest, edit, and delete.

| Operation | UI |
|-----------|-----|
| **Create** | **Create new thesis (IDEA)** expander — manual plan before fill |
| **Sync ingest** | **Pending from sync** cards — Robinhood positions awaiting thesis text |
| **Read** | Filter by status/ticker; select a row to view details |
| **Update** | Edit thesis text, catalyst, setup, confidence, stop/target, review interval; post-trade fields on CLOSED/INVALIDATED |
| **Delete** | **Delete permanently** expander (terminal only; Force for non-terminal) |

Lifecycle actions on the edit panel: Mark reviewed, Promote IDEA → ENTRY_READY, Stop tracking (+ exclude list), Close position.

Protected fields (read-only after creation): `ticker`, `thesis_type`, `status` (use action buttons instead).

## Dashboard

Read-only position overview with metrics. Select a row for a summary, then **Manage in Theses** for edits and lifecycle actions. **Refresh Positions** runs `scripts/robinhood_sync.py`.

Pending sync rows link to **Theses** for thesis entry.

## Pending ingest flow

When you submit from **Theses → Pending from sync**, the app:

1. Validates thesis text, type, confidence, and IRA options eligibility
2. Registers via `thesis_store.register()`
3. Promotes to **ACTIVE** with entry price/date from sync data
4. Attaches `position` metadata (account, expiry, strike) for dashboard display
5. Marks the pending row **INGESTED** in `state/pending_ingest.json`

## Reports page

Read deep-research markdown in-app from `reports/research/{TICKER}_{YYYY-MM-DD}.md`.

- Select ticker (all tickers with at least one report file)
- If multiple dated reports exist, pick the report date (newest first)
- Full report renders in a scrollable panel
- **Go to Research** for staleness prompts and update queue

## Research page

Tracks deep-research freshness for open positions + watchlist.
Pairs with weekly `research-staleness.timer` systemd job.
Run scan: `uv run python3 scripts/update_stale_research.py`

The Research page reads `state/research_update_queue.json`, shows staleness
for eligible tickers, and provides copy-paste Cursor prompts for
`update-research` / `deep-research` workflows (no LLM calls from Streamlit).
Copy prompts include PASS 0 preflight (`scripts/research_preflight.py`) and manifest path.

Watchlist config: `config/research_watchlist.yaml` (editable in-app).

Exclude config: `config/research_exclude.yaml` (copy from `config/research_exclude.yaml.example`).
Excluded tickers are hidden from Research staleness, Reports ticker list, and
`update_stale_research.py` scans. Edit in-app under **Research → Excluded tickers**.

## Removing tickers

| Goal | UI action |
|------|-----------|
| Drop from research tracking (e.g. INO) | Research → **Exclude from research** or Excluded tickers editor; Reports → **Archive this report** |
| Stop tracking a position (e.g. XSP) | **Theses → Stop tracking** (invalidates thesis + adds exclude) |
| Never ingest from sync again | **Theses → Pending from sync → Dismiss** (SKIPPED + sync block) |
| Remove thesis file entirely | **Theses → Delete permanently** (confirm; terminal only unless Force) |

## Tests

```bash
uv run python3 -m pytest scripts/tests/test_thesis_manager_*.py -v
```
