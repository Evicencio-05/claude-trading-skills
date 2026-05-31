# Sync Phase Docs & PENDING_WORK to Completed Work

## Goal
Reconcile **PENDING_WORK.md**, **STATUS.md**, and active phase docs with **evidence on disk** — marking completed work done, refreshing watchlists (e.g. deep-research tickers and dates), and leaving only genuine open items in the queue.

## Inputs
- **As-of date:** today (ET) unless user specifies
- **User additions:** optional free-text list of work completed since last doc update (paste at end of prompt)
- **Mode:** `sync-only` (default) — update docs; do not run new research or trades

## Pre-flight
- [ ] Read `PENDING_WORK.md`, `project-docs/STATUS.md`, `project-docs/phase-1-research-copilot.md` (active; replaces archived `phase-1b-robinhood-research.md`), `project-docs/archive/phase-1-audit.md`
- [ ] Read latest `reports/meta/phase_1b_kickoff_*.md` if present
- [ ] Read `decisions.md` — do not contradict binding decisions

## Phase 1 — Evidence harvest (read-only)

Run these commands and capture output in your working notes:

```bash
# Deep research / updates — canonical watchlist source
ls -1 reports/research/*.md 2>/dev/null | sort

# Per ticker: keep NEWEST date only; note duplicates and staleness (>14 calendar days)
# Example pattern: TICKER_YYYY-MM-DD.md

# Daily market context
ls -1 reports/logs/market_context_*.md 2>/dev/null | wc -l
wc -l reports/logs/posture_history.log 2>/dev/null

# Portfolio reviews & batch summaries
ls -1 reports/portfolio/portfolio_review_*.md 2>/dev/null
ls -1 reports/logs/portfolio_summary_*.md 2>/dev/null

# Phase kickoff / prior sync reports
ls -1 reports/meta/phase_1b_kickoff_*.md reports/meta/docs_sync_*.md 2>/dev/null

# Thesis store (do not edit theses in this task)
uv run python3 skills/trader-memory-core/scripts/thesis_store.py \
  --state-dir state/theses/ list

# Pending broker ingest
test -f state/pending_ingest.json && cat state/pending_ingest.json | head -50

# MCP / infra smoke (optional — only if docs claim "verified")
uv run python3 scripts/robinhood_mcp.py accounts 2>&1 | head -5

# Recent git activity (what changed since last doc date in PENDING_WORK header)
git log --oneline -15
git log -1 --format='%ci' -- PENDING_WORK.md project-docs/STATUS.md
```

Build an **evidence table** before editing any doc:

| Category | Artifact | Finding | Implies |
|----------|----------|---------|---------|
| Deep research | `reports/research/TICKER_DATE.md` | latest date, stale? | mark done / keep open |
| Update research | changelog in `reports/logs/*_changelog.md` | | |
| pre_market | market_context + posture_history rows | count toward 14-day exit | |
| Portfolio review | `reports/portfolio/portfolio_review_*.md` | count toward 2+ exit | |
| review-portfolio | `portfolio_summary_*.md` | weekly cadence done? | |
| MCP | kickoff / portfolio review | accounts verified | |
| ingest | pending_ingest.json | TE logged? | |
| Theses | thesis_store list | IRA/taxable coverage | |
| vcp / screeners | PENDING_WORK notes or reports/ | smoke vs full run | |
| Infra | systemd timers mentioned in docs | confirm still accurate | |

**Staleness rule (research):** report date &gt;14 days before as-of → flag stale in docs; do **not** mark "deep research complete" for that ticker unless a newer `reports/research/TICKER_*.md` exists.

**Dedupe rule:** For each ticker, one row in watchlist tables — **latest report date only**. Drop superseded dates from active queue (older files may remain on disk).

## Phase 2 — Diff against docs

Compare evidence to these files. Flag every mismatch:

| Doc | What to reconcile |
|-----|-------------------|
| `PENDING_WORK.md` | Unchecked items already done; Done section missing new work; duplicate todos; wrong "Last updated" |
| `project-docs/STATUS.md` | This week's focus, Phase 1 exit table, Phase 1 carryover, Recent Changes |
| `project-docs/phase-1-research-copilot.md` | Watchlist table, exit criteria checkboxes, workstream status (active phase doc) |
| `project-docs/archive/phase-1-audit.md` | Exit criteria checkboxes (only if evidence clearly satisfies) |

Common fixes this repo needs (check all):

- **Deep-research tickers:** Docs may list MRAM, MU, P, FPS, INO, VECO — refresh dates from `reports/research/` (e.g. MRAM/MU/P @ 2026-05-27; FPS @ 2026-05-13 stale)
- **"Deep research FPS"** in queue vs **"FPS done"** in Done — resolve: Phase 1 minimum met, but FPS **update** may still be open if stale
- **5+ deep/update exit criterion:** count distinct tickers with reports in last 30 days vs total ever
- **14-day pre_market:** posture_history line count vs checkbox
- **portfolio_review count:** file count vs "2+ reports" exit
- **Phase 1B kickoff actions** (ingest-pending, log-positions TE) — verify against pending_ingest + theses, not kickoff checkboxes alone

## Phase 3 — Apply doc updates

Edit in this order (single consistent snapshot):

### 1. `PENDING_WORK.md`
- Update header **Last updated** to today
- Move completed items → **Done (do not redo)** with date note
- Uncheck → `[x]` only with evidence citation (path or command output)
- Remove completed items from active sections (don't leave done work in P0/P1)
- Refresh **Research pipeline** watchlist line: tickers + latest report date + stale flags
- Keep genuinely open: FMP Starter, IRA logging, Agentic confirm trade, expired thesis closes

### 2. `project-docs/STATUS.md`
- Update **Last updated**
- Rewrite **This week's focus** — max 5 bullets, **open work only**
- Refresh **Phase 1 Exit Criteria Progress** table from evidence
- Update **Phase 1 Exit (carryover)** checkboxes
- Add **Recent Changes** bullet: "Docs synced to evidence YYYY-MM-DD"

### 3. `project-docs/phase-1-research-copilot.md`
- Sync watchlist table with `reports/research/` (ticker, latest date, stale Y/N)
- Update exit criteria checkboxes where evidence is unambiguous
- Do not mark futures defer items as started

### 4. `project-docs/archive/phase-1-audit.md` (optional)
- Only update exit criteria if evidence clearly satisfies (e.g. 3+ deep-research tickers already `[x]` — don't uncheck)

### 5. Write sync report

Save `reports/meta/docs_sync_YYYY-MM-DD.md`:

```markdown
# Docs Sync — YYYY-MM-DD

## Evidence summary
- Research reports: [table ticker → latest date → stale?]
- pre_market days: N (posture_history)
- portfolio reviews: N
- theses: N active / N IDEA / pending ingest: Y/N

## Changes made
| File | Change |

## Still open (unchanged)
- [bullets]

## User-provided completions applied
- [from input or "none"]
```

## Rules
- **Evidence only** — never mark `[x]` without a file path, thesis id, or command output
- **Conservative on trades** — don't mark "10+ trades logged" unless thesis_store count supports it (include types)
- **Don't edit** `state/theses/` YAML in this task — read via CLI only
- **Don't contradict** `decisions.md` or DEFERRED futures banner
- **Minimal prose** — tables and checklists over paragraphs
- If evidence is ambiguous, leave checkbox open and note in sync report

## Do not
- Run new deep-research, trades, or FMP billing
- Delete research reports or theses
- Commit unless user explicitly asks
- Invent tickers not in `reports/research/` unless user provided them in **User additions**
- Duplicate long workflow text — link to `commands/` and phase docs

## User additions (paste below when invoking)

```
[Optional: list work you know is done but may not be on disk yet, e.g.
 "Completed deep research on XYZ 2026-05-29", "Logged TE thesis", etc.]
```

## After run
Paste [prompt-complete.md](prompt-complete.md) with `sync-phase-docs.md`.
