# Thesis Manager — Ticker Removal UI

## Goal
Wire watchlist, research, reports, and position removal into Thesis Manager so tickers like XSP and INO can be dismissed without manual YAML edits.

## Inputs
- Scope: `tools/thesis-manager/`, `scripts/research_watchlist.py`, `scripts/update_stale_research.py`, `config/`
- Examples: XSP (contract — stop tracking + exclude stats/UI), INO (drop from research — exclude + archive report)
- User choice: soft exclude list + confirm-gated permanent thesis delete

## Pre-flight
- [ ] Read `tools/thesis-manager/app.py`, `utils.py`, `research_utils.py`, `tools/thesis-manager/README.md`
- [ ] Read `scripts/research_watchlist.py`, `scripts/tests/test_research_watchlist.py`
- [ ] Read `skills/trader-memory-core/scripts/thesis_store.py` (terminate, close, rebuild_index)
- [ ] Baseline: `uv run python3 -m pytest scripts/tests/test_thesis_manager_*.py scripts/tests/test_research_watchlist.py -q`

## Steps
1. **Exclude config (TDD)** — add `config/research_exclude.yaml.example`; load/save helpers in `research_utils.py` mirroring watchlist (`resolve_exclude_path`, `load_exclude_for_editor`, `save_exclude`). Format:
   ```yaml
   INO:
     reason: "not interested"
   XSP:
     reason: "hedge — exclude from research stats"
   ```
2. **Filter eligibility (TDD)** — in `scripts/research_watchlist.py`:
   - `load_exclude_config(path) -> dict[str, dict]`
   - `apply_exclude(tickers, exclude_path) -> list[str]`
   - Update `eligible_tickers()` to subtract excluded tickers
   - Extend `scripts/tests/test_research_watchlist.py`
3. **Wire staleness script** — `scripts/update_stale_research.py` resolves exclude path (same pattern as watchlist) so queue JSON omits excluded tickers
4. **Report archive helper (TDD)** — `research_utils.archive_report(path) -> Path` moves file to `reports/archive/research/` (mkdir parents); `list_report_tickers()` skips tickers on exclude list
5. **Thesis removal API (TDD)** — add `thesis_store.delete(state_dir, thesis_id)`:
   - Allowed only for `CLOSED` / `INVALIDATED` unless `force=True` (ACTIVE/IDEA/ENTRY_READY raise)
   - Deletes `th_*.yaml`, updates index via existing index helpers, returns deleted id
   - Tests in `skills/trader-memory-core/scripts/tests/test_thesis_store.py`
   - Thin wrapper `utils.delete_thesis(thesis_id, force=False)` for UI
6. **Pending + sync helpers (TDD)** — in `utils.py`:
   - `mark_pending_skipped(positions, key) -> list` (status `SKIPPED`)
   - `block_sync_key(key)` — append to `state/synced_positions.json` `ingested_keys` so `robinhood_sync.py` won't re-add
   - `stop_tracking_thesis(thesis_id)` — terminate ACTIVE/ENTRY_READY/IDEA to `INVALIDATED` without exit prices (no P&L); no-op if already terminal
7. **Streamlit UI** — `app.py`:
   - **Research → Excluded tickers** — `st.data_editor` + Save (parallel to Watchlist section)
   - **Research table** — per-row action: "Exclude" (add ticker + reason, clear cache, rerun)
   - **Reports** — filter ticker selectbox; button "Archive report" (moves file, optional auto-add to exclude)
   - **Dashboard detail** — "Stop tracking" (invalidate if open + add exclude); expander "Advanced" → "Delete thesis permanently" with `st.checkbox` confirm + `delete_thesis`
   - **Add Thesis pending** — replace session-only Skip with "Dismiss" (SKIPPED + sync block + optional exclude)
   - **Review** — filter out excluded tickers from sections B/C tables (optional caption: "N excluded hidden")
8. **Docs + example** — update `tools/thesis-manager/README.md`; add `config/research_exclude.yaml.example`
9. **Tests** — `scripts/tests/test_thesis_manager_exclusions.py` (exclude load/save, archive, delete wrapper mocks, pending skip)
10. **Finish** — `uv run python3 -m pytest scripts/tests/test_thesis_manager_*.py scripts/tests/test_research_watchlist.py skills/trader-memory-core/scripts/tests/test_thesis_store.py -q` and `ruff check` on touched paths

## Outputs
- New prompt file (this doc)
- Code + tests as above
- Optional: `reports/thesis_manager_ticker_removal_YYYY-MM-DD.md` — what shipped + manual QA checklist

## Rules
- Thesis writes/deletes via `thesis_store` / `utils` only — never hand-edit `state/theses/*.yaml`
- No LLM calls from Streamlit; no trades
- Permanent delete requires explicit confirm checkbox in UI
- `watching: false` alone is insufficient — exclude list is the canonical "hide everywhere"

## Do not
- Commit unless user asks
- Change Robinhood sync ingestion logic beyond `ingested_keys` block helper
- Add new Python dependencies
