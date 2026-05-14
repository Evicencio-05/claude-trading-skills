# Scheduled Jobs

## Pre-Market Routine (systemd — Linux/Arch)
Runs scripts/pre_market.py at 8 AM ET weekdays.
Files: pre-market.service + pre-market.timer (install to ~/.config/systemd/user/)

Setup:
  systemctl --user daemon-reload
  systemctl --user enable pre-market.timer
  systemctl --user start pre-market.timer

Test: uv run scripts/pre_market.py --dry-run
Logs: tail /tmp/pre_market.log

## Robinhood Sync (systemd — Linux/Arch)
Runs scripts/robinhood_sync.py at 4:30 PM ET weekdays.
File: robinhood-sync.service + robinhood-sync.timer
(Not yet created — follows same pattern as pre-market)

## Note on .plist files
The .plist files in this directory are macOS launchd format.
This system runs Arch Linux — use systemd instead.
.plist files are kept for reference only.

## Disable until Phase 3
skill-generation and skill-improvement jobs are disabled.
Do not enable before Phase 3. See phase-3-learning-loop.md.
