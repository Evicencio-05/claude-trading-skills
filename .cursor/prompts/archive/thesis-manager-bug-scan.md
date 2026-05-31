# Thesis Manager Bug Scan

## Goal
Scan `tools/thesis-manager/` for bugs and runtime errors; fix confirmed issues and document findings.

## Inputs
- App: `tools/thesis-manager/app.py` (5 pages: Dashboard, Research, Reports, Add Thesis, Review)
- Local data: `state/theses/`, `state/pending_ingest.json`, `reports/research/*.md`

## Pre-flight
- [ ] Run: `uv run python3 -m pytest scripts/tests/test_thesis_manager_*.py -v`
- [ ] Run: `uv run ruff check tools/thesis-manager/`

## Steps
1. Read `tools/thesis-manager/app.py`, `utils.py`, `research_utils.py`
2. **Static audit** — every `st.dataframe` / `st.data_editor`: ensure display columns are homogeneous (str), no int + `"—"` mixes (PyArrow)
3. **AppTest smoke** — add `scripts/tests/test_thesis_manager_smoke.py`: `AppTest.from_file("tools/thesis-manager/app.py").run()` per page via `session_state["sidebar_page"]`
4. **Logic audit** — Reports page ticker/date selectbox stale session keys; nav `nav_page` jumps; styled DataFrame + selection index alignment
5. Fix bugs found (minimal diffs); add regression tests where practical
6. Re-run full pytest + ruff
7. Write `reports/meta/thesis_manager_bug_scan_YYYY-MM-DD.md` — findings table (severity, page, fix status)

## Rules
- No thesis_store / sync / staleness logic changes unless bug is proven there
- No commits unless user asks
- On missing local state files: continue with empty-state paths, note in report

## Do not
- Execute trades or call Robinhood MCP
- Add dependencies
- Refactor UI for aesthetics

## After run
Paste [prompt-complete.md](prompt-complete.md) with `thesis-manager-bug-scan.md`.
