# Archived Scripts

One-shot and migration utilities kept for history. **Do not re-run** without reading each script's header — they may duplicate theses or move files unexpectedly.

| Script | Purpose | Archived |
|--------|---------|----------|
| `log_manual_positions.py` | One-shot IRA/Lucid backfill into trader-memory-core (2026-05-09/10) | 2026-05-28 |
| `normalize_research_filenames.py` | Migrate deep-research reports to `reports/research/{TICKER}_{date}.md` | 2026-05-28 |
| `migrate_reports_layout.py` | One-time `reports/` category-dir layout migration | 2026-08-10 |

Active equivalents: `/log-positions` + `robinhood_sync.py` / `robinhood_mcp.py ingest-pending` for position logging. Category layout is live under `reports/{market,screeners,portfolio,...}/` via `scripts/report_paths.py`.
