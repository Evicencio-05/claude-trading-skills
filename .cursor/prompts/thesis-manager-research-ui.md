# Thesis Manager — Research Dashboard & Update Workflow

## Goal
Extend `tools/thesis-manager/` (Streamlit) with a **Research** page that shows deep-research health per ticker (position or watchlist), surfaces staleness, links to reports, and makes triggering updates frictionless — consuming the same queue as the systemd staleness job.

**Adjacent work:** Background scan + prefetch → [.cursor/prompts/systemd-stale-research-updater.md](systemd-stale-research-updater.md)

## Inputs
- **Staleness threshold:** 14 days (configurable constant, match review-portfolio)
- **Data sources:**
  - `reports/research/{TICKER}_{date}.md`
  - `state/theses/` via `utils.load_theses()`
  - `config/research_watchlist.yaml` (via `scripts/research_watchlist.py` — **implement systemd prompt first** or stub the import)
  - `state/research_update_queue.json` (written by `update_stale_research.py`)
  - Optional: `reports/logs/research_prefetch/{TICKER}_*.json`

## Pre-flight
- [ ] Read `tools/thesis-manager/app.py`, `utils.py`, `README.md`
- [ ] Read `commands/update-research.md`, `commands/deep-research.md`
- [ ] Confirm `scripts/research_watchlist.py` exists (from adjacent prompt); if not, implement minimal shared module first
- [ ] Run app: `uv run streamlit run tools/thesis-manager/app.py`

## Phase 1 — Shared research helpers

Add `tools/thesis-manager/research_utils.py` (thin wrapper — **no duplicate staleness logic**):

```python
# Import from scripts.research_watchlist OR sys.path insert repo/scripts
def get_research_dashboard_rows(as_of: date | None = None) -> list[dict]
def load_update_queue() -> dict | None
def open_report_path(ticker: str) -> Path | None  # latest reports/research file
def staleness_badge(days: int | None) -> str  # OK / WARN / STALE / MISSING
```

Each row dict:

| Field | Source |
|-------|--------|
| `ticker` | eligible set |
| `last_report_date` | latest filename |
| `days_stale` | computed |
| `report_path` | Path for open/download |
| `thesis_status` | ACTIVE / ENTRY_READY / IDEA / — |
| `watching` | YAML flag |
| `eligibility` | `position`, `watchlist`, or both |
| `queue_status` | from `research_update_queue.json` |
| `prefetch_available` | bool |

Add `scripts/tests/` only if testing pure functions via import; otherwise manual QA checklist in PR.

## Phase 2 — New Streamlit page: **Research**

Update sidebar in `app.py`:

```python
["Dashboard", "Research", "Add Thesis", "Review"]
```

### 2A — Summary metrics (top row)

- **Tracked tickers** — count eligible
- **Stale (>14d)** — count red
- **Missing report** — eligible but no file
- **Queued updates** — from `research_update_queue.json` if generated today/week

### 2B — Main table

Sortable dataframe / `st.dataframe` with columns:

| Ticker | Last Report | Days | Thesis | Watching | Status | Actions |

**Row styling** (match Dashboard patterns):
- Red: stale or missing report for ACTIVE/ENTRY_READY
- Yellow: 7–14 days
- Green: fresh (≤7d)

**Status values:** `fresh`, `stale`, `missing`, `queued`, `needs_deep_research`

### 2C — Row actions

Per selected ticker (use `st.dataframe` selection or expander per row):

1. **View report** — `st.markdown` read file contents in expander, or `st.link_button` if serving file path is awkward (prefer in-app preview of latest MD)
2. **Open prefetch** — show JSON from `reports/logs/research_prefetch/` if present
3. **Copy update prompt** — text area with ready-to-paste Cursor instruction:

   ```text
   Follow commands/update-research.md for {TICKER}.
   Prefetch data: reports/logs/research_prefetch/{TICKER}_{date}.json (if exists)
   Save to reports/research/{TICKER}_{today}.md
   ```

4. **Copy deep-research prompt** — if `missing`, point to `commands/deep-research.md`

**Do not** call LLM from Streamlit. Copy-paste prompts only (cost discipline).

### 2D — Watchlist editor (lightweight)

Section below table: edit `config/research_watchlist.yaml`

- Add ticker + notes + watching toggle
- Save via safe write (validate YAML structure)
- Or: read-only with note "edit file manually" for v1 — **prefer editable** if simple

### 2E — Queue panel

If `state/research_update_queue.json` exists:
- Show `generated_at`, list tickers needing update
- Button: **Refresh queue now** → runs subprocess:

  ```python
  subprocess.run([sys.executable, "scripts/update_stale_research.py", "--dry-run"], ...)
  ```

- Button: **Regenerate queue** → `update_stale_research.py` (no dry-run) with spinner + success toast

## Phase 3 — Dashboard integration (minimal)

On existing **Dashboard**, add one metric or caption:

- "Research stale: N" — link to Research page via `st.session_state` page switch or sidebar hint

Optional: show staleness icon next to Ticker in position table (requires join with research rows).

## Phase 4 — UX polish

- Cache research rows `@st.cache_data(ttl=60)` like `_theses()`
- `_show_refresh_button()` pattern — clear cache on refresh
- Empty state: "No eligible tickers — add positions or edit research_watchlist.yaml"
- Document in `tools/thesis-manager/README.md`:

```markdown
## Research page
Tracks deep-research freshness for open positions + watchlist.
Pairs with weekly `research-staleness.timer` systemd job.
```

## Phase 5 — Validation

Manual test checklist:
- [ ] Ticker with fresh report shows green
- [ ] FPS (or known stale) shows stale + copy-update prompt
- [ ] ACTIVE thesis without report shows missing + deep-research prompt
- [ ] Queue file from systemd script displays in Queue panel
- [ ] Watchlist add/remove persists to YAML
- [ ] App still runs: Dashboard, Add Thesis, Review unchanged

```bash
uv run streamlit run tools/thesis-manager/app.py
ruff check tools/thesis-manager/
```

## Rules
- Import staleness logic from `scripts/research_watchlist.py` — single source of truth
- Never write `state/theses/` YAML directly — keep using `utils` wrappers
- Never invoke Claude/API from Streamlit
- Match existing app style: wide layout, border containers, IRA badges where relevant
- English UI; report content is English

## Do not
- Build a second webapp — extend thesis-manager only
- Fork `update-research.md` workflow text into the UI
- Auto-run LLM updates in background
- Remove existing pages or break pending ingest flow
- Commit secrets in watchlist YAML

## Deliverables checklist
- [ ] `tools/thesis-manager/research_utils.py`
- [ ] `show_research()` page in `app.py`
- [ ] Sidebar + optional dashboard staleness hint
- [ ] README update
- [ ] Screenshot optional in `reports/` (not required)

## Suggested build order (with adjacent prompt)

1. Implement `scripts/research_watchlist.py` + `update_stale_research.py` (systemd prompt)
2. Implement Research page consuming shared module (this prompt)
3. Install systemd timer
4. Use webapp Queue panel + copy-paste prompts to run weekly updates in Cursor
