# Thesis Manager Ticker Removal — 2026-05-30

## Shipped

| Area | Change |
|------|--------|
| Config | `config/research_exclude.yaml.example`; user file `config/research_exclude.yaml` |
| Scripts | `load_exclude_config`, `apply_exclude`, filter in `eligible_tickers` / `update_stale_research.py` |
| Store | `thesis_store.delete()` (terminal only; `force=True` for open theses) |
| UI | Research excluded editor; Reports archive; Dashboard stop tracking + delete; Add Thesis dismiss |
| Prompt | `.cursor/prompts/thesis-manager-ticker-removal.md` |

## Tests

152 passed (`test_thesis_manager_*`, `test_research_watchlist`, `test_thesis_store`).

## Manual QA

- [ ] Research: exclude INO → absent from staleness table
- [ ] Reports: archive INO report → gone from ticker list
- [ ] Dashboard: XSP **Stop tracking** → off open table + in exclude list
- [ ] Dashboard: Advanced **Delete permanently** on terminal thesis (with confirm)
- [ ] Add Thesis: **Dismiss** pending row → SKIPPED; re-sync does not re-add
- [ ] Review: excluded closed positions hidden with caption

## Usage (INO / XSP)

1. Copy `config/research_exclude.yaml.example` → `config/research_exclude.yaml` if missing.
2. **INO:** Reports → Archive report (check exclude); or Research → Exclude / editor.
3. **XSP:** Dashboard → Stop tracking; or Dismiss on pending before ingest; permanent delete only after terminal/confirm.
