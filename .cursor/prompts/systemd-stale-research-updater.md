# Systemd — Stale Deep-Research Updater (Positions + Watchlist)

## Goal
Build a **zero-LLM systemd job** that finds stale deep-research reports for tickers you still care about (open positions or explicit watchlist), refreshes **scriptable** data, queues synthesis work, and writes a dated status report — following the `pre_market.py` + `launchd/` timer pattern on Arch Linux.

**Adjacent work:** Web UI for viewing/updating research → [.cursor/prompts/thesis-manager-research-ui.md](thesis-manager-research-ui.md)

## Inputs
- **Staleness threshold:** 14 calendar days (match `commands/review-portfolio.md` and Phase 1B)
- **Schedule:** weekly, default **Sunday 6 PM local** (or user override)
- **Eligible tickers:**
  - **In position:** thesis status `ACTIVE` or `ENTRY_READY` in `state/theses/`
  - **Watching:** tickers in `config/research_watchlist.yaml` with `watching: true`
  - **Also watching:** thesis status `IDEA` **only if** ticker is in watchlist YAML (avoid stale screener noise)
- **Mode:** `scan-only` for first PR; optional `--prefetch` for scriptable data fetches

## Pre-flight
- [ ] Read `commands/update-research.md`, `commands/review-portfolio.md`, `scripts/pre_market.py`
- [ ] Read `launchd/README.md`, `launchd/pre-market.service`, `launchd/pre-market.timer`
- [ ] Read `tools/thesis-manager/utils.py` — reuse repo-root resolution pattern
- [ ] Read `project-docs/reference/cost-discipline.md` — **no LLM in systemd path**

## Architecture (required split)

| Layer | Runs when | Cost | Output |
|-------|-----------|------|--------|
| **Scan** | systemd timer | $0 | `state/research_update_queue.json` |
| **Prefetch** | same job, `--prefetch` | FMP calls only if key set | `reports/logs/research_prefetch/{TICKER}_{date}.json` |
| **Synthesize** | Cursor / webapp / manual | LLM | `reports/research/{TICKER}_{date}.md` via `update-research` workflow |

Systemd **must not** call Claude or Cursor. It prepares the queue; humans/agents run `update-research`.

## Phase 1 — Shared library (TDD)

Create `scripts/research_watchlist.py` (test first in `scripts/tests/test_research_watchlist.py`):

```python
# Functions to implement:
def load_watchlist_config(path: Path) -> dict[str, dict]  # ticker → {watching, notes}
def tickers_from_theses(state_dir: Path, statuses: tuple) -> set[str]
def eligible_tickers(state_dir, watchlist_path) -> list[str]  # union, sorted
def latest_report_date(research_dir: Path, ticker: str) -> date | None
def days_stale(latest: date | None, as_of: date) -> int | None  # None if no report
def build_staleness_rows(...) -> list[dict]  # ticker, last_report, days_stale, reason, needs_update
```

Create `config/research_watchlist.yaml.example` (commit example; real file gitignored or committed without secrets):

```yaml
# Tickers to track even without a position
MRAM:
  watching: true
  notes: "swing candidate"
FPS:
  watching: true
```

**Filename parsing:** `reports/research/{TICKER}_{YYYY-MM-DD}.md` — ticker = segment before `_YYYY-MM-DD` suffix (same as review-portfolio).

## Phase 2 — CLI orchestrator

Create `scripts/update_stale_research.py`:

```bash
uv run python3 scripts/update_stale_research.py --dry-run          # print table, no writes
uv run python3 scripts/update_stale_research.py                      # write queue + summary
uv run python3 scripts/update_stale_research.py --prefetch           # + scriptable data per stale ticker
uv run python3 scripts/update_stale_research.py --threshold 14
uv run python3 scripts/update_stale_research.py --ticker MRAM        # single ticker
```

**Default behavior (non-dry-run):**
1. Compute eligible + stale tickers
2. Write `state/research_update_queue.json`:

```json
{
  "generated_at": "ISO8601",
  "threshold_days": 14,
  "tickers": [
    {
      "ticker": "FPS",
      "last_report": "2026-05-13",
      "days_stale": 15,
      "eligibility": ["watchlist"],
      "status": "needs_update",
      "prefetch_path": null
    }
  ]
}
```

3. Write `reports/logs/research_staleness_YYYY-MM-DD.md` — human-readable table + copy-paste Cursor lines:
   - `Follow commands/update-research.md for FPS`
4. If `--prefetch` and `FMP_API_KEY` set: for each stale ticker, run **scriptable** fetches only (reuse patterns from update-research Step 2a–c where scripts exist: breadth via saved pre_market JSON if today exists, `fred_calendar.py`, optional FMP quote endpoint). Save JSON per ticker; set `prefetch_path` in queue.
5. If no report exists for eligible ticker → `status: needs_deep_research` (suggest `deep-research`, not update)

**Exit codes:** 0 = success; 1 = error; 2 = stale tickers found (optional, for systemd `SuccessExitStatus=`)

## Phase 3 — systemd units

Add to `launchd/` (repo templates; user copies to `~/.config/systemd/user/`):

- `research-staleness.service` — oneshot, mirrors `pre-market.service`
- `research-staleness.timer` — weekly schedule

**Service requirements:**
- `Type=oneshot`
- `WorkingDirectory=` repo root (use relative path in docs; **no username** in committed ExecStart — document `sed` or `%h` pattern in launchd/README)
- `ExecStart=/usr/bin/uv run python3 scripts/update_stale_research.py --prefetch`
- Logs: `/tmp/research_staleness.log` (document in README)
- `Environment=PATH=...` — load `.env` via script (`load_dotenv` like pre_market)

**Timer:** weekly; document timezone adjustment like `pre-market.timer`

Update `launchd/README.md` with install/test/disable instructions.

## Phase 4 — Docs & queue consumers

| File | Update |
|------|--------|
| `PENDING_WORK.md` | Weekly staleness job; link to timer |
| `project-docs/phase-1b-robinhood-research.md` | Replace manual review-portfolio staleness note with script + timer |
| `LOAD_GUIDE.md` | On-demand: `scripts/update_stale_research.py` |
| `tools/thesis-manager/` | **Do not implement UI here** — see adjacent webapp prompt |

## Phase 5 — Tests & validation

```bash
uv run python3 -m pytest scripts/tests/test_research_watchlist.py -v
uv run python3 scripts/update_stale_research.py --dry-run
systemctl --user daemon-reload  # after user installs units
systemctl --user start research-staleness.service
```

Fixtures: tmp `reports/research/`, tmp theses, tmp watchlist YAML.

## Rules
- TDD: tests before implementation
- **Zero LLM** in systemd job
- Never write `state/theses/` YAML directly
- Reuse `commands/review-portfolio.md` staleness semantics (14 days)
- Prefetch is best-effort — log failures, continue queue
- No absolute paths with usernames in committed files

## Do not
- Invoke Cursor, Claude API, or `update-research` prose generation from systemd
- Update tickers with `CLOSED`/`INVALIDATED` theses unless still in watchlist YAML with `watching: true`
- Delete old `reports/research/` files
- Commit `.env` or secrets
- Duplicate watchlist logic in webapp — import/share `research_watchlist.py`

## Deliverables checklist
- [ ] `scripts/research_watchlist.py` + tests
- [ ] `scripts/update_stale_research.py`
- [ ] `config/research_watchlist.yaml.example`
- [ ] `launchd/research-staleness.service` + `.timer`
- [ ] `launchd/README.md` section
- [ ] Sample `reports/logs/research_staleness_YYYY-MM-DD.md` from dry-run
