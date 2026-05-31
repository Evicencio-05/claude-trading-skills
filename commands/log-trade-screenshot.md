---
description: "Extract Robinhood trade-confirmation fields from pasted screenshots and write to trader-memory-core. User supplies thesis and lessons only."
---

# /log-trade-screenshot

Paste one or more Robinhood trade confirmation screenshots. The agent reads the images, autofills mechanical fields, and writes to `state/theses/` via `tools/thesis-manager/utils.py` (never edit YAML by hand).

**User provides:** thesis, confidence, stop, target (opens / backfills only); optional exit reason if ambiguous; optional post-trade review text (closes).

**Agent autofills:** ticker, account, asset type, direction, strategy, strike, expiry, option type, quantity, fill price, fill date/time, open vs close, fees when visible.

---

## Invoke

```
/log-trade-screenshot
```

Or: "log trade from screenshot", "paste trade confirmation", "backfill closed trade from image".

Paste screenshots in the same message (one trade per image, or open + close for the same contract).

---

## Agent workflow

### 1 — Extract (vision)

For each screenshot, read Robinhood confirmation fields:

| Field | Notes |
|-------|--------|
| Action header | e.g. `Sell FPS $60 Call 6/18` → ticker, strike, type, expiry |
| Position effect | **Open** = entry fill; **Close** = exit fill |
| Side | Buy vs Sell (with open/close determines long open vs close) |
| Quantity | Contracts or shares |
| Fill price | Per contract/share |
| Filled time | Date + timezone → use trade date for `actual_date` |
| Account label | Map below |
| Order type / TIF | Informational only |

**Account mapping** (→ `position.account_type`):

| Robinhood label | thesis_store value |
|-----------------|-------------------|
| Roth IRA / IRA | `ira_robinhood` |
| Individual / taxable | `robinhood_taxable` |
| Agentic | `robinhood_agentic` |

**Strategy** (options, IRA check):

| Pattern | strategy |
|---------|----------|
| Buy + Open + call | `long_call` |
| Buy + Open + put | `long_put` |
| Sell + Open + call (covered) | `covered_call` |
| Other / unclear | `""` and flag IRA eligibility |

Show a numbered summary per image before writing. Wait for user **"go"** or corrections (unless they said "write now").

### 2 — Match existing thesis

```bash
uv run python3 skills/trader-memory-core/scripts/thesis_store.py --state-dir state/theses/ list
```

Match **ACTIVE** (or **ENTRY_READY**) theses on: ticker, strike, expiry, account, option type.

| Match result | Path |
|--------------|------|
| **Close** screenshot + ACTIVE match | → Close only (§4) |
| **Open** screenshot + no match | → Register + ACTIVE (§3) |
| **Close** + no match | Need entry data: second (open) screenshot, or ask entry price/date once |
| **Open** + ACTIVE already exists | Warn duplicate; offer close old + re-open or skip |

### 3 — Open / backfill entry (register → ACTIVE)

Ask **only** these four questions (same as [log-positions.md](log-positions.md)):

1. Thesis (2–4 sentences)
2. Confidence 1–5
3. Stop (price or condition)
4. Target (price or condition)

Then run Python (repo root):

```python
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, "tools/thesis-manager")
import utils

pending = {
    "ticker": "FPS",
    "account": "ira_robinhood",
    "asset_type": "options",
    "direction": "long",
    "strategy": "long_call",
    "strike": 60.0,
    "expiry": "2026-06-18",
    "option_type": "call",
    "contracts": 3,
    "avg_cost": 1.25,  # entry fill from screenshot
    "synced_at": "2026-05-10T18:16:00-07:00",  # filled time from open screenshot
}
thesis_data = utils.build_thesis_data(
    ticker=pending["ticker"],
    thesis_type="growth_momentum",  # pick from utils.THESIS_TYPES; ask if unclear
    thesis_text="...",
    confidence=3,
    stop_text="...",
    target_text="...",
    avg_cost=pending["avg_cost"],
    strategy=pending["strategy"],
)
thesis_data["origin"] = {"skill": "trade_screenshot", "output_file": "manual/screenshot"}
thesis_data["_source_date"] = "2026-05-10"  # entry date YYYY-MM-DD for backfill

tid = utils.register_pending_position(thesis_data, pending)
# Backfill entry timestamp if needed:
# store.open_position(..., event_date="2026-05-10T18:16:00+00:00")
print(tid)
```

Block submit if IRA account + non-eligible strategy (`utils.ira_options_eligible`).

### 4 — Close (ACTIVE → CLOSED)

Infer `exit_reason` when obvious; otherwise ask once:

| Signal | exit_reason |
|--------|-------------|
| Expired / $0 close | `time_stop` |
| Hit stated target | `target_hit` |
| Stop / invalidation | `stop_hit` / `invalidated` |
| Discretionary / unclear | `manual` |

```python
import sys
from datetime import date

sys.path.insert(0, "tools/thesis-manager")
import utils

utils.finalize_thesis(
    thesis_id,
    "manual",           # utils.EXIT_REASONS
    0.90,               # exit fill price
    date(2026, 5, 27),  # exit trade date
)
```

Optional post-trade review (user text only):

```python
utils.update_thesis(tid, {
    "outcome": {
        "what_happened": "...",
        "lessons_learned": "...",
    }
})
```

### 5 — Report

After each trade:

```
Logged: FPS long_call 3x $60 call 2026-06-18
  thesis_id: th_fps_...
  status: ACTIVE | CLOSED
  entry: $1.25 @ 2026-05-10
  exit:  $0.90 @ 2026-05-27  (if closed)
  P&L: see thesis YAML outcome block
Verify: streamlit run tools/thesis-manager/app.py → Dashboard / Review
```

Process multiple screenshots **one trade at a time** (options by nearest expiry first).

---

## Rules

- Do **not** use `thesis_ingest.py` (screener JSON only).
- Do **not** edit files under `state/theses/*.yaml` directly.
- Prefer `utils.register_pending_position`, `utils.finalize_thesis`, `utils.update_thesis`.
- If extraction is ambiguous (year on expiry, partial screenshot), ask one clarifying question — do not guess strike/expiry/account.
- Phase 1 co-pilot: read/write thesis store only — no MCP orders.
