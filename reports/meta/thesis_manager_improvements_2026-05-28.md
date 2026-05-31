# Thesis Manager Improvements — 2026-05-28

Audit and TDD delivery for `tools/thesis-manager/` (Phase 1B co-pilot scope).

## Backlog (ranked)

| # | Improvement | Pain | Risk | Testability | Effort | Shipped |
|---|-------------|------|------|-------------|--------|---------|
| 1 | Pending ingest → ACTIVE promotion (`register_pending_position`) | Positions logged as IDEA only; dashboard missing expiry/account | Med — wrong lifecycle | High (pure + store) | M | **Yes** |
| 2 | IRA submit gate + shared eligibility helpers | IRA spreads could be logged without block | High — rule violation | High | S | **Yes** |
| 3 | Extract pure helpers to `utils.py` + 42 unit tests | Untestable Streamlit logic | Low | High | M | **Yes** |
| 4 | Pre-submit validation (thesis_type, statement, confidence) | Opaque thesis_store errors in UI | Low | High | S | **Yes** |
| 5 | Duplicate ticker warning (ACTIVE + pending) | Double-counting positions | Low | High | S | **Yes** |
| 6 | Manual entry → ACTIVE with position block | Manual log leaves IDEA | Med | High | M | No — manual stays IDEA (user opens separately) |
| 7 | Research table mobile layout | Cramped on small screens | Low | Streamlit-only | M | Deferred |
| 8 | `_run_safe` structured error codes | Generic error strings | Low | Med | S | Deferred |

## What shipped

### Service layer (`utils.py`)

- `fmt_account`, `ira_options_eligible`, `ira_badge_html`, `days_to_expiry`, `parse_price`
- `build_thesis_data`, `validate_thesis_submit`
- `position_from_pending`, `mark_pending_ingested`, `pending_duplicate_tickers`
- `register_pending_position` — register → ENTRY_READY → ACTIVE + position metadata from pending row
- Shared constants: `THESIS_TYPES`, `EXIT_REASONS`, `IRA_ELIGIBLE_STRATEGIES`

### UI (`app.py`)

- Pending submit uses `register_pending_position` (ACTIVE + position block)
- IRA-ineligible options blocked before submit (pending + manual)
- Validation errors surfaced before thesis_store calls
- Dashboard + Add Thesis warn on duplicate tickers (open thesis + pending)

### Tests

- `scripts/tests/test_thesis_manager_utils.py` — 34 tests
- `scripts/tests/test_thesis_manager_pending.py` — 8 tests (incl. all `EXIT_REASONS`)

Run:

```bash
uv run python3 -m pytest scripts/tests/test_thesis_manager_*.py -v
uv run ruff check tools/thesis-manager/
```

## Edge-case coverage

| Case | Covered |
|------|---------|
| Empty/missing pending_ingest | Test |
| Corrupt pending JSON | Test |
| Invalid expiry string | Test |
| IRA + ineligible strategy | Test + UI block |
| Duplicate ACTIVE + pending | Test + UI warning |
| All EXIT_REASONS on ACTIVE close | Test |
| ENTRY_READY terminate via finalize | Test |
| Missing thesis store dir | Existing `load_theses` returns [] |
| Watchlist YAML missing | Existing `resolve_watchlist_path` fallback |

## Manual Streamlit QA

- [ ] Dashboard: duplicate warning when pending overlaps ACTIVE
- [ ] Add Thesis pending: submit promotes to ACTIVE; row collapses; pending marked INGESTED
- [ ] Add Thesis IRA options: ineligible strategy shows badge + blocks submit
- [ ] Close position: each exit reason persists (spot-check one ticker)
- [ ] Research page unchanged (regression)

## Alternatives not chosen

- **Manual entry auto-ACTIVE:** Left as IDEA-only; user may log planned trades before fill. Could add optional “Open as ACTIVE” checkbox later.
- **Structured error taxonomy:** Kept string errors from `_run_safe`; sufficient for co-pilot UI.
