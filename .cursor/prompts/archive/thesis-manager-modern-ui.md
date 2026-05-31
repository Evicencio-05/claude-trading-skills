# Thesis Manager — Modern UI Refresh (Mockup-Driven)

## Goal
Refactor `tools/thesis-manager/` Streamlit UI to match the **clean, modern dark dashboard** in the reference mockup, with **button-based navigation** and a **collapsible sidebar** — no radio controls for page selection.

## Visual reference
- **Mockup image:** `assets/image-d51a07e0-b4c3-48e0-8e61-2a52e111b51c.png` (workspace) — use as layout/palette guide, not pixel-perfect spec
- **Keep:** Dark theme, wide layout, metric cards row, colored table rows, bordered detail panels, section labels (`A — …`), IRA/status pills, minimal chrome
- **Change from mockup:**
  - Sidebar nav = **full-width text buttons**, not radio circles
  - Sidebar = **collapsible** (expanded shows labels; collapsed shows icons or initials only)

## Inputs
- **Scope:** `tools/thesis-manager/app.py`, `.streamlit/config.toml`, optional new `tools/thesis-manager/ui_theme.py` or `assets/custom.css` injected via `st.markdown(unsafe_allow_html=True)`
- **Optional:** User preference for collapsed default (`expanded` | `collapsed`) — default **expanded**

## Pre-flight
- [ ] Read `app.py` (all four pages: Dashboard, Research, Add Thesis, Review)
- [ ] Read mockup image and [thesis-manager-dashboard-mockup-image.md](thesis-manager-dashboard-mockup-image.md)
- [ ] Run baseline: `uv run streamlit run tools/thesis-manager/app.py`
- [ ] Note current nav: `st.sidebar.radio` in `main()` (~lines 1053–1060) — **replace entirely**

## Design requirements

### 1 — Collapsible sidebar
- Toggle control at top of sidebar (e.g. `◀` / `▶` or hamburger) sets `st.session_state["sidebar_collapsed"]`
- **Expanded:** width ~220–260px; show app title "Thesis Manager" + chart icon; nav buttons with full labels; footer caption `trader-memory-core UI`
- **Collapsed:** narrow rail (~56–72px); hide title text and caption; nav shows icon-only or single-letter (D / R / + / ✓) with `help=` tooltip for full name
- Persist collapse state in `st.session_state` across reruns (same session)
- Use custom CSS only where Streamlit layout cannot achieve collapse; prefer minimal CSS targeting `[data-testid="stSidebar"]`

### 2 — Navigation buttons (no radio)
- Replace `st.sidebar.radio("Page", PAGES, …)` with one `st.sidebar.button` per page:
  - Dashboard, Research, Add Thesis, Review
- **Active page:** visual distinct state — `type="primary"` or custom CSS class (pill background like mockup gray highlight, not Streamlit default alone if insufficient)
- **Inactive:** `type="secondary"` or ghost style
- Clicking a button sets `st.session_state["sidebar_page"]` and `st.rerun()`
- Preserve existing cross-page jumps (e.g. Dashboard `Go to Research` → set `nav_page` / `sidebar_page` to Research)

### 3 — Global polish (all pages)
- **Metrics row:** consistent card spacing; keep warning deltas on Pending / Expiring / Stale counts
- **Tables:** retain row background semantics (pending gold `#3d3500`, expiry red `#3d0000`, stale red, fresh green tint on Research)
- **Detail panels:** `st.container(border=True)` with clearer header hierarchy (`st.subheader` + muted captions)
- **Buttons:** primary actions filled (Submit, Mark for Review); secondary outlined (Refresh, Close Position, Go to Research)
- **Typography:** slightly increased section spacing; dividers between major blocks
- **Do not** add charts, images, or marketing hero blocks

### 4 — Page-specific (no feature changes)
- **Dashboard:** unchanged data/logic; layout only
- **Research:** metrics + table + watchlist + queue — same fields, cleaner section headers
- **Add Thesis:** pending cards + manual expander — same forms
- **Review:** urgent / post-trade / closed week — same actions

## Implementation approach

1. Extract `render_sidebar() -> str` returning current page name; centralize collapse + nav buttons there
2. Extract shared CSS to `inject_theme_css(collapsed: bool)` — dark refinements optional (border-radius on cards, sidebar transition)
3. Keep all business logic in `utils.py` / `research_utils.py` — **UI-only diff** in `app.py` unless a tiny helper is needed for active-nav detection
4. Update `tools/thesis-manager/README.md` with sidebar collapse behavior

## Testing

| Layer | What to verify |
|-------|----------------|
| Manual QA | Toggle collapse; all four pages load; active button highlights; `Go to Research` still works |
| Manual QA | Forms still submit (Add Thesis, Close, Review lesson) |
| Optional unit | `test_thesis_manager_nav.py` — pure helper for `page_from_button_label` / collapse state if extracted |

Run: `ruff check tools/thesis-manager/`

## Outputs
- Code: `tools/thesis-manager/` (+ README)
- Optional: `reports/thesis_manager_ui_refresh_YYYY-MM-DD.md` — before/after screenshots checklist (English)

## Rules
- **No** changes to `thesis_store` writes, research staleness logic, or sync scripts
- **No** new Python dependencies unless user approves (CSS-in-markdown is fine)
- **No** commits unless user asks

## Stop conditions
- Ask user if custom CSS breaks their Streamlit version — offer fallback: buttons without collapse animation
- Ask before renaming pages or adding a fifth nav item

## Do not
- Reintroduce `st.sidebar.radio` for navigation
- Build a non-Streamlit frontend
- Change mockup content (tickers, counts) in production data — sample data only in docs/screenshots

## Reference — target sidebar behavior (ASCII)

```
EXPANDED                    COLLAPSED
┌──────────────────┐        ┌────┐
│ 📊 Thesis Manager │ [◀]   │ 📊 │ [▶]
│ [ Dashboard    ] │        │ D  │
│ [ Research     ] │        │ R  │
│ [ Add Thesis   ] │        │ +  │
│ [ Review       ] │        │ ✓  │
│ trader-memory…   │        └────┘
└──────────────────┘
     ↑ primary/ghost buttons, not radio dots
```

## After run
Paste [prompt-complete.md](prompt-complete.md) with `thesis-manager-modern-ui.md`.
