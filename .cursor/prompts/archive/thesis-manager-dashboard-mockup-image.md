# Thesis Manager — AI Image Mockup Prompts

> **Use:** Paste into Midjourney, Ideogram, DALL·E, Flux, or similar. Generate **reference mockups** for UX direction — not pixel-perfect Streamlit clones.
> **App source of truth:** `tools/thesis-manager/app.py` (dark theme in `.streamlit/config.toml`)

---

## Recommended generation settings

| Setting | Value |
|---------|--------|
| Aspect ratio | 16:9 (desktop) or 3:2 |
| Style | Clean SaaS dashboard, flat UI, subtle shadows, no 3D |
| Theme | **Dark mode** — charcoal background `#0e1117`, cards `#262730`, accent green for OK, amber warn, red alert |
| Avoid | Stock photos, charts with fake tickers as ads, glassmorphism overload, mobile phone frames unless asked |

---

## Master prompt (single composite — all pages visible)

Copy everything between the lines:

```
Professional UI mockup of a desktop web app called "Thesis Manager" for a solo stock trader. Dark theme, clean minimal SaaS layout, wide screen 16:9.

LEFT SIDEBAR (narrow, fixed):
- App title "Thesis Manager" with small chart icon
- Vertical navigation as full-width pill buttons (not radio dots): Dashboard (selected), Research, Add Thesis, Review; sidebar collapsible with toggle
- Footer caption: "trader-memory-core UI"

MAIN CONTENT — DASHBOARD PAGE (primary focus, 70% of canvas):

Top row — four equal metric cards in a row:
1) "Open Positions" value 6
2) "Pending Thesis" value 2 with small warning delta
3) "Expiring ≤ 7 days" value 1 with warning
4) "Days Since Last Entry" value 4

Below metrics — subtle caption line: "Research stale: 3" and a small secondary button "Go to Research"

Divider, then a data table with columns: Ticker | Type | Account | Expiry | Confidence | Days Left | Status
Sample rows with color-coded row backgrounds: one row amber "PENDING_THESIS", one row red tint for expiry ≤7 days, normal rows for ACTIVE
Tickers example: MRAM, HOOD, MU — mix stock and options types, accounts like rh:taxable and ira_robinhood

One table row selected — detail panel below table in a bordered card:
- Header "MRAM — ACTIVE"
- Two columns: left shows Thesis text, Stop, Target, Kill criteria; right shows Last reviewed, Confidence 4/5
- Buttons: "Mark for Review", "Close Position"

Bottom: primary outline button "Refresh Positions"

SMALL INSET PREVIEWS (right edge or bottom strip, thumbnail tabs) showing other pages without full detail:

RESEARCH page inset: four metrics (Tracked tickers, Stale >14d, Missing report, Queued updates), table columns Ticker | Last Report | Days | Thesis | Watching | Status | Badge, green/yellow/red row tints, section labels "Watchlist" and "Update queue"

ADD THESIS page inset: section "A — Pending Positions" with bordered card for ticker HOOD, IRA Eligible green pill badge, form fields Thesis type dropdown, Thesis textarea, Confidence slider 1-5, Stop, Target, Submit button; collapsed section "Add position manually"

REVIEW page inset: "A — Urgent Flags" card with ticker and reasons, buttons Still Valid / Close Position / Roll; "B — Needs Post-Trade Review" with lesson form; "C — Closed This Week" small table

Typography: system sans-serif (Inter or similar), high contrast white text on dark gray, plenty of whitespace, no clutter, no marketing hero banners. Looks like Streamlit or Retool admin UI. Figma-quality wireframe polish.
```

**Negative prompt (append if the tool supports it):**

```
blurry text, illegible labels, light mode, white background, neon cyberpunk, cartoon, isometric 3D, cluttered charts, bitcoin logos, trading floor photo, people, hands, watermark, logo soup, 10+ competing fonts, skeuomorphic leather
```

---

## Per-page prompts (generate separately for higher fidelity)

### 1 — Dashboard (hero image)

```
Dark-mode desktop UI mockup, "Thesis Manager" app, Dashboard page. Minimal clean trader dashboard.

Sidebar: Dashboard selected, Research, Add Thesis, Review, caption trader-memory-core UI.

Main: header "Dashboard". Four metric cards in a row — Open Positions 6, Pending Thesis 2 (warning), Expiring ≤ 7 days 1 (warning), Days Since Last Entry 4.

Caption "Research stale: 3" + button Go to Research. Warning banner about duplicate tickers optional.

Sortable data table: columns Ticker, Type, Account, Expiry, Confidence, Days Left, Status. Rows with subtle dark red/orange/olive row highlights for expiry and pending states. One row selected.

Detail card below: MRAM ACTIVE, thesis statement snippet, stop, target, kill criteria, last reviewed, confidence 4/5, buttons Mark for Review and Close Position.

Button Refresh Positions at bottom. Charcoal UI, Inter font, spacious padding, no charts, no photos.
```

### 2 — Research

```
Dark-mode desktop UI mockup, Thesis Manager Research page. Clean data-heavy but simple layout.

Sidebar navigation with Research selected.

Header "Research". Four metrics: Tracked tickers 12, Stale (>14d) 3 warning, Missing report 1 warning, Queued updates 2.

Main table: Ticker, Last Report, Days, Thesis, Watching, Status, Badge. Row colors: green fresh, yellow aging, red stale/missing. Example tickers FPS INO VECO MRAM.

Selected row detail: subheader FPS stale, eligibility caption, collapsed expanders View report and Open prefetch, read-only text area labeled Copy update prompt.

Lower sections in bordered cards: Watchlist editable table (Ticker, Watching checkbox, Notes) with Save watchlist button; Update queue table with Generated date and buttons Refresh queue now, Regenerate queue.

Dark Streamlit-style admin UI, minimal decoration.
```

### 3 — Add Thesis

```
Dark-mode desktop UI mockup, Thesis Manager Add Thesis page. Form-focused, clean.

Sidebar with Add Thesis selected. Header "Add Thesis".

Section A — Pending Positions: bordered card for HOOD options position, green pill "IRA Eligible", metadata captions Account Type Strike Expiry Contracts Avg cost, bold "12d left" in green/orange/red, dropdown Thesis type, large Thesis textarea, three columns Confidence slider 1-5, Stop field, Target field, primary Submit button, small Skip button top right.

Divider. Collapsed accordion "Add position manually" hint below.

Dark minimal UI, generous form spacing, no clutter.
```

### 4 — Review

```
Dark-mode desktop UI mockup, Thesis Manager Review page. Three stacked sections, card-based.

Sidebar Review selected. Header "Review".

Section A — Urgent Flags: bordered cards, each shows ticker bold, comma-separated reasons (options expiring, not reviewed, low confidence), caption thesis stop target, three buttons Still Valid, Close Position, Roll.

Section B — Needs Post-Trade Review: card per closed trade with Entry Exit P&L Conf captions, form What happened textarea, Key lesson input, Submit Review.

Section C — Closed This Week: compact dataframe Ticker Account Entry Exit P&L Confidence Outcome.

Dark theme, success green empty state optional "No urgent flags". Clean typography.
```

---

## 4-up composite prompt (Figma handoff style)

```
Single image, 2x2 grid of four dark-mode UI screens, same app "Thesis Manager", consistent sidebar and dark theme.

Top-left: Dashboard with metrics and positions table.
Top-right: Research with staleness metrics and colored table.
Bottom-left: Add Thesis with pending position form card.
Bottom-right: Review with urgent flag cards.

Uniform spacing, labeled page titles in each quadrant, presentation slide quality, white thin gutters between panels, no device bezel.
```

---

## Content checklist (verify mockup includes)

| Area | Must show |
|------|-----------|
| Nav | Dashboard, Research, Add Thesis, Review |
| Dashboard metrics | Open Positions, Pending Thesis, Expiring ≤7d, Days Since Last Entry |
| Dashboard table | 7 columns + row status colors + row selection detail |
| Dashboard actions | Go to Research, Mark for Review, Close Position, Refresh Positions |
| Research metrics | Tracked, Stale, Missing, Queued |
| Research table | 7 columns + status/badge coloring |
| Research panels | Watchlist editor, Update queue + regen buttons |
| Add Thesis | Pending card + IRA badge + thesis form + manual expander |
| Review | Urgent flags, Post-trade review forms, Closed this week table |
| Theme | Dark base, restrained red/amber/green semantic colors only |

---

## Iteration tips

1. Generate **Dashboard** first; refine palette and sidebar width.
2. Use `--cref` / style reference image from pass 1 for other pages (tool-dependent).
3. If text is garbled, regenerate with fewer words on buttons (labels only: "Submit", "Refresh", "Research").
4. For stakeholder decks, use the **4-up composite**; for design tickets, use **per-page** prompts.

## Do not

- Treat generated images as implementation specs (Streamlit widgets differ).
- Show live brokerage logos or real account numbers.
- Depict trade execution buttons (app is co-pilot / journal only).

## After run
Paste [prompt-complete.md](prompt-complete.md) with `thesis-manager-dashboard-mockup-image.md`.
