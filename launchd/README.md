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
Files: robinhood-sync.service + robinhood-sync.timer (install to ~/.config/systemd/user/)

**Prerequisite:** Complete manual 2FA once; fill ACCOUNT_MAP in `scripts/robinhood_sync.py`.

Setup:
  cp launchd/robinhood-sync.service launchd/robinhood-sync.timer ~/.config/systemd/user/
  systemctl --user daemon-reload
  systemctl --user enable robinhood-sync.timer
  systemctl --user start robinhood-sync.timer

Test: uv run scripts/robinhood_sync.py --dry-run
Logs: tail /tmp/robinhood_sync.log

## Stale Research Scan (systemd — Linux/Arch)
Runs scripts/update_stale_research.py weekly (default Sunday 6 PM local).
Zero LLM — writes state/research_update_queue.json and a summary log.
Files: research-staleness.service + research-staleness.timer (install to ~/.config/systemd/user/)

**Prerequisite:** Copy watchlist config:
  cp config/research_watchlist.yaml.example config/research_watchlist.yaml

Install (replace repo path if not ~/repos/claude-trading-skills):
  sed 's|%h/repos/claude-trading-skills|'"$HOME"'/repos/claude-trading-skills|' \
    launchd/research-staleness.service > ~/.config/systemd/user/research-staleness.service
  cp launchd/research-staleness.timer ~/.config/systemd/user/
  systemctl --user daemon-reload
  systemctl --user enable research-staleness.timer
  systemctl --user start research-staleness.timer

Test:
  uv run python3 scripts/update_stale_research.py --dry-run
  systemctl --user start research-staleness.service

Logs: tail /tmp/research_staleness.log

Disable:
  systemctl --user disable research-staleness.timer

## Prompt Learning Distill (systemd — Linux/Arch)
Runs scripts/distill_prompt_learnings.py weekly (default Sunday 6:30 PM local, after stale-research scan).
Zero LLM — processes prompt_run_retro reports into state/prompt_learnings.yaml and writes a digest.
Files: prompt-learning.service + prompt-learning.timer (install to ~/.config/systemd/user/)

**Prerequisite:** Run [prompt-complete.md](../.cursor/prompts/prompt-complete.md) at least once so retro reports exist.

Install (replace repo path if not ~/repos/claude-trading-skills):
  sed 's|%h/repos/claude-trading-skills|'"$HOME"'/repos/claude-trading-skills|' \
    launchd/prompt-learning.service > ~/.config/systemd/user/prompt-learning.service
  cp launchd/prompt-learning.timer ~/.config/systemd/user/
  systemctl --user daemon-reload
  systemctl --user enable prompt-learning.timer
  systemctl --user start prompt-learning.timer

Test:
  uv run python3 scripts/distill_prompt_learnings.py --dry-run
  systemctl --user start prompt-learning.service

Logs: tail /tmp/prompt_learning.log
Digest: reports/prompt_learning_digest_YYYY-MM-DD.md

Disable:
  systemctl --user disable prompt-learning.timer

## Note on .plist files
The .plist files in this directory are macOS launchd format.
This system runs Arch Linux — use systemd instead.
.plist files are kept for reference only.

## Disable until Phase 3
skill-generation and skill-improvement jobs are disabled.
Do not enable before Phase 3. See phase-3-learning-loop.md.
