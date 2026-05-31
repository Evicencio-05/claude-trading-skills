# Thesis Manager Bug Scan — 2026-05-29

**Scope:** `tools/thesis-manager/` (5 pages)
**Baseline tests:** 48 passed
**Final tests:** 53 passed (48 unit + 1 arrow_safe + 6 report + 5 AppTest smoke)

## Summary

Automated scan found three fixable issues (PyArrow dtype mixing, queue int/str column, Reports date desync). All fixed with minimal diffs. No exceptions on AppTest smoke runs across all pages.

## Findings

| ID | Severity | Page | Issue | Status |
|----|----------|------|-------|--------|
| B1 | High | Dashboard | `Confidence` column mixed `int` and `"—"` → PyArrow serialization errors | Fixed + `arrow_safe_df` hardening |
| B2 | Medium | All tables | Other `st.dataframe` calls could hit same PyArrow mixed-type class | Fixed |
| B3 | Medium | Research | Update queue `Days stale` could be raw int from JSON | Fixed |
| B4 | Low | Reports | Stale `reports_date` when switching ticker | Fixed |
| B5 | Info | Smoke tests | `at.exception is None` wrong for AppTest empty `ElementList` | Fixed |

## Commands run

```bash
uv run python3 -m pytest scripts/tests/test_thesis_manager_*.py -v  # 53 passed
uv run ruff check tools/thesis-manager/ scripts/tests/test_thesis_manager_*.py
```
