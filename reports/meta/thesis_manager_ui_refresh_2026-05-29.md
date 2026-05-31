# Thesis Manager UI Refresh — QA Checklist

**Date:** 2026-05-29
**Scope:** Collapsible sidebar, button navigation, dark-theme polish (UI-only)

## Before / after

| Area | Before | After |
|------|--------|-------|
| Nav | `st.sidebar.radio` | Full-width sidebar buttons + active pill highlight |
| Sidebar width | Fixed Streamlit default | ~248px expanded / ~68px collapsed |
| Collapse | N/A | `◀` / `▶` toggle, session-persisted |
| Metrics | Plain Streamlit metrics | Card-style borders + spacing |
| Actions | Default button types | Primary (Submit, Mark for Review) / secondary (Refresh, Close, Go to Research) |

## Manual QA

- [ ] Toggle sidebar collapse; labels switch full ↔ short (D/R/+/✓)
- [ ] All four pages load from sidebar buttons
- [ ] Active page button shows distinct highlight
- [ ] Dashboard **Go to Research** jumps to Research page
- [ ] Add Thesis **Submit** still registers pending positions
- [ ] Review **Submit Review** and **Close Position** forms work
- [ ] Row colors unchanged on Dashboard and Research tables

## Automated

```bash
uv run python3 -m pytest scripts/tests/test_thesis_manager_nav.py -v
ruff check tools/thesis-manager/
```

## Screenshots

Capture after manual run:

1. Dashboard — expanded sidebar, metrics row, table + detail panel
2. Dashboard — collapsed sidebar rail
3. Research — staleness metrics + colored table
4. Add Thesis — pending card with IRA badge
5. Review — urgent flags section

Run: `uv run streamlit run tools/thesis-manager/app.py`
