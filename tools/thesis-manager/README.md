# Thesis Manager

Run:     streamlit run tools/thesis-manager/app.py
Purpose: Thesis input and position review for trader-memory-core
Data:    Reads state/theses/ and state/pending_ingest.json
Writes:  Calls thesis_store API (never directly edits YAML files)

## Navigation

Five pages via sidebar radio: **Dashboard**, **Research**, **Reports**, **Add Thesis**, **Review**.

Cross-page links (e.g. Dashboard **Go to Research**) set `nav_page` and jump on the next rerun.

## Reports page

Read deep-research markdown in-app from `reports/research/{TICKER}_{YYYY-MM-DD}.md`.

- Select ticker (all tickers with at least one report file)
- If multiple dated reports exist, pick the report date (newest first)
- Full report renders in a scrollable panel
- **Go to Research** for staleness prompts and update queue

## Pending ingest flow

When you submit from **Add Thesis → Pending Positions**, the app:

1. Validates thesis text, type, confidence, and IRA options eligibility
2. Registers via `thesis_store.register()`
3. Promotes to **ACTIVE** with entry price/date from sync data
4. Attaches `position` metadata (account, expiry, strike) for dashboard display
5. Marks the pending row **INGESTED** in `state/pending_ingest.json`

Manual entry (expander) registers as **IDEA** only — use when logging a plan before fill.

## Research page

Tracks deep-research freshness for open positions + watchlist.
Pairs with weekly `research-staleness.timer` systemd job.
Run scan: `uv run python3 scripts/update_stale_research.py`

The Research page reads `state/research_update_queue.json`, shows staleness
for eligible tickers, and provides copy-paste Cursor prompts for
`update-research` / `deep-research` workflows (no LLM calls from Streamlit).

Watchlist config: `config/research_watchlist.yaml` (editable in-app).

Exclude config: `config/research_exclude.yaml` (copy from `config/research_exclude.yaml.example`).
Excluded tickers are hidden from Research staleness, Reports ticker list, and
`update_stale_research.py` scans. Edit in-app under **Research → Excluded tickers**.

## Removing tickers

| Goal | UI action |
|------|-----------|
| Drop from research tracking (e.g. INO) | Research → **Exclude from research** or Excluded tickers editor; Reports → **Archive this report** |
| Stop tracking a position (e.g. XSP) | Dashboard → **Stop tracking** (invalidates thesis + adds exclude) |
| Never ingest from sync again | Add Thesis → **Dismiss** on pending row (SKIPPED + sync block) |
| Remove thesis file entirely | Dashboard → Advanced → **Delete thesis permanently** (confirm; terminal only unless Force) |

## Tests

```bash
uv run python3 -m pytest scripts/tests/test_thesis_manager_*.py -v
```
