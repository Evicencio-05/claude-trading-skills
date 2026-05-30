# Thesis Manager — Improvement Discovery & TDD Delivery

## Goal
Audit `tools/thesis-manager/`, propose prioritized UX/UI, service-layer, and position-handling improvements, then implement the highest-value items using **test-first development** with explicit edge-case coverage.

## Inputs
- **Scope:** `tools/thesis-manager/` (Streamlit app) and its direct dependencies (`utils.py`, `research_utils.py`, `scripts/research_watchlist.py`, `skills/trader-memory-core/scripts/thesis_store.py`)
- **Optional focus areas** from user (e.g. "Research table UX", "pending ingest flow", "IRA options badges") — if none, cover all three: UX/UI, data/service layer, positions/theses
- **Out of scope unless user expands:** upstream skill edits, autonomous trading, new webapp

## Pre-flight
- [ ] Read `PROJECT.md`, `project-docs/STATUS.md`, `PENDING_WORK.md` — align with Phase 1B (co-pilot only)
- [ ] Read `tools/thesis-manager/README.md`, `app.py`, `utils.py`, `research_utils.py`
- [ ] Read `decisions.md` (portfolio accounts, IRA rules, thesis write policy)
- [ ] Read `skills/trader-memory-core/scripts/tests/test_thesis_store.py` — match store API contracts
- [ ] Run app once: `uv run streamlit run tools/thesis-manager/app.py`
- [ ] Baseline tests: `uv run python3 -m pytest skills/trader-memory-core/scripts/tests/ -q`

## Phase 1 — Discovery & improvement backlog

Produce a short proposal (chat or `reports/thesis_manager_improvements_YYYY-MM-DD.md`) with:

| Category | Examples to evaluate |
|----------|---------------------|
| **UX/UI** | Navigation, table density, empty states, error surfacing, mobile-ish layout, copy-paste flows, consistent badges (IRA, staleness, expiry) |
| **Service layer** | Duplication vs `scripts/research_watchlist.py`, repo-root resolution, queue/watchlist reads, `_run_safe` error UX |
| **Positions / theses** | Pending ingest → thesis promotion, multi-leg/options display, account mapping, status transitions, schema validation before write |

For each candidate improvement, note: **user pain**, **risk**, **testability** (pure fn vs Streamlit-only), **effort** (S/M/L). Rank top 3–5 for implementation this session.

**Reuse audit — do not reinvent:**
- Staleness logic → `scripts/research_watchlist.py` / `research_utils.py`
- Thesis writes → `utils.py` wrappers → `thesis_store` only
- Research queue → `state/research_update_queue.json` + [.cursor/prompts/systemd-stale-research-updater.md](systemd-stale-research-updater.md)
- Research UI spec → [.cursor/prompts/thesis-manager-research-ui.md](thesis-manager-research-ui.md) (gap-fill only, don't duplicate)

## Phase 2 — Test-first implementation

For each approved improvement (user picks from backlog or "top 3 by value"):

1. **Extract testable logic** from `app.py` into `utils.py` or `research_utils.py` when Streamlit-coupled — keep UI thin.
2. **Write failing tests first** under `scripts/tests/test_thesis_manager_*.py` (import via repo root / `sys.path` pattern used elsewhere). Cover:
   - Happy path
   - Empty / missing files (`state/theses/`, `pending_ingest.json`, queue, watchlist YAML)
   - Malformed JSON / partial thesis records
   - IRA account + strategy combinations (`long_call`, spreads, empty strategy)
   - Options expiry edge cases (past, today, invalid date string)
   - Unknown account keys, Robinhood URL vs short account id formatting
   - Write failures surfaced to UI (mock `thesis_store` where needed)
3. **Minimal implementation** until green.
4. **Streamlit QA checklist** (manual) for anything not unit-testable: page navigation, widgets, session state, file download buttons.

Run before finishing each item:
```bash
uv run python3 -m pytest scripts/tests/test_thesis_manager_*.py -v
ruff check tools/thesis-manager/
```

## Phase 3 — Deliverables

| Output | Path / format |
|--------|----------------|
| Improvement backlog + what shipped | `reports/thesis_manager_improvements_YYYY-MM-DD.md` (English) |
| New/updated tests | `scripts/tests/test_thesis_manager_*.py` |
| Code | `tools/thesis-manager/` only (+ shared `scripts/` if logic belongs there) |
| README | Update `tools/thesis-manager/README.md` for behavior changes |

## Rules
- **Never** write `state/theses/*.yaml` directly — `thesis_store` API via `utils.py` only
- **Never** autonomous trade execution (Phase 5 gate); UI may copy prompts only
- Flag **IRA-ineligible** options strategies before any actionable submit
- Prefer extending existing modules over new parallel services
- On ambiguous product choice: implement the smallest safe variant, document alternatives in the report
- **Stop and ask** before: new dependencies, breaking thesis schema, or changes to `skills/trader-memory-core/scripts/` (wrapper-only fork policy)

## Edge cases checklist (must address in tests or QA)

- [ ] No theses / empty store directory
- [ ] Thesis index entry without loadable full record
- [ ] `pending_ingest.json` missing, empty, or corrupt
- [ ] Duplicate tickers across ACTIVE + pending
- [ ] Research report filename variants / no report for eligible ticker
- [ ] Queue file from different week or empty `tickers` list
- [ ] Watchlist YAML missing → example fallback
- [ ] `get_repo_root()` failure (document behavior)
- [ ] Submit with invalid price, confidence, or thesis_type enum
- [ ] Close thesis: each `EXIT_REASONS` value persists correctly

## Do not
- Modify upstream `skills/*/SKILL.md` or skill scripts (except tests you add under `scripts/tests/`)
- Commit or push unless the user explicitly asks
- Commit secrets, API keys, or absolute paths with usernames
- Build a second webapp or replace Streamlit without user approval
- Run paid APIs or LLM calls from the Streamlit process
