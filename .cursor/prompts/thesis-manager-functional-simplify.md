# Thesis Manager — Functional Simplicity + Reports Page

## Goal
Simplify Thesis Manager UI to stock Streamlit (readable, no custom chrome) and add a Reports page to read deep-research markdown in-app.

## Inputs
- Scope: `tools/thesis-manager/app.py`, `research_utils.py`, optional removal/slimming of `ui_theme.py`
- Report source: `reports/research/{TICKER}_{YYYY-MM-DD}.md` (via existing `open_report_path`)
- User choice: dedicated **Reports** nav page (list tickers → read full report)

## Pre-flight
- [ ] Read `tools/thesis-manager/app.py`, `research_utils.py`, `ui_theme.py`
- [ ] Confirm sample reports exist: `reports/research/*.md`

## Steps
1. **Strip UI chrome** — remove collapsible sidebar, `inject_theme_css`, section-caption HTML, and button-type polish; restore `st.sidebar.radio` nav (5 pages)
2. **Add `research_utils` helpers** (TDD):
   - `list_report_tickers() -> list[str]` — tickers with at least one report in `reports/research/`
   - `list_reports_for_ticker(ticker) -> list[dict]` — `{date, path}` newest first
   - `load_report_markdown(path: Path) -> str | None` — read file safely
3. **Add `show_reports()` page** in `app.py`:
   - Ticker `st.selectbox` (sorted)
   - If multiple reports for ticker, secondary selectbox or caption with date
   - Show report path + staleness caption (days since report date)
   - Render full markdown inline in scrollable container (`st.container(height=500)` or minimal max-height CSS)
   - Empty state when no reports: link to Research page for update prompts
4. **Research page** — remove collapsed "View report" expander (Reports page is canonical reader); keep staleness table, prompts, watchlist, queue unchanged
5. **Optional Dashboard** — one-line caption under detail panel: "Report: {date}" with `st.session_state nav_page` jump to Reports (only if trivial; skip if scope creep)
6. Update `tools/thesis-manager/README.md` — document Reports page; remove collapse-nav docs
7. Tests: `scripts/tests/test_thesis_manager_reports.py` for new helpers; update/remove nav tests tied to `ui_theme`
8. Run: `uv run python3 -m pytest scripts/tests/test_thesis_manager_*.py -v` and `uv run ruff check tools/thesis-manager/`

## Outputs
- Code changes in `tools/thesis-manager/`
- Optional: `.cursor/prompts/thesis-manager-functional-simplify.md` (this prompt, committed if user wants)

## Rules
- UI-only + thin read helpers — no changes to `thesis_store` writes, staleness scan logic, or sync scripts
- No new Python dependencies
- No commits unless user asks
- Keep semantic table row colors (pending/expiry/stale) — functional signal, not decoration

## Do not
- Rebuild mockup-driven sidebar or custom CSS theme
- Add charts, hero blocks, or non-Streamlit frontend
- Call LLMs from Streamlit to generate reports
