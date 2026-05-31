---
name: log-trade-screenshot
description: >-
  Extract Robinhood trade confirmation data from pasted screenshots and write
  to trader-memory-core. Autofills prices, dates, contract details, and
  open/close status; user supplies thesis and post-trade lessons only. Use when
  the user pastes trade confirmation screenshots, says log-trade-screenshot,
  backfill closed trade from image, or paste trade confirmation.
---

# Log Trade Screenshot

Follow [commands/log-trade-screenshot.md](../../../commands/log-trade-screenshot.md).

## Quick start

User pastes screenshot(s) → extract fields → show summary → user says **go** → write via `tools/thesis-manager/utils.py`.

## User vs agent

| Agent autofills | User provides |
|-----------------|---------------|
| Ticker, strike, expiry, qty, fill price, date, account, open/close | Thesis, confidence, stop, target (opens) |
| Match to existing ACTIVE thesis | Exit reason if ambiguous (closes) |
| Register / close / outcome update | What happened + lesson (optional, closes) |

## IRA

Flag eligibility with `utils.ira_options_eligible`. Block register if IRA + ineligible strategy.
