#!/bin/bash
# scripts/run_pre_market.sh
#
# Wrapper for the automated pre-market routine.
# Called by launchd — handles logging, market day check,
# and passes the correct prompt to Claude Code CLI.
#
# Usage (manual): bash scripts/run_pre_market.sh
# Usage (auto):   via launchd com.trading.pre-market.plist

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$REPO_DIR/reports/logs"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
LOG_FILE="$LOG_DIR/pre_market_runner.log"

mkdir -p "$LOG_DIR"

# ── Market day check ─────────────────────────────────────────────────────────
# Skip weekends. US market holidays are not checked here — Claude will note
# if markets are closed in the output.
DAY_OF_WEEK=$(date +%u)  # 1=Mon ... 7=Sun
if [ "$DAY_OF_WEEK" -ge 6 ]; then
    echo "$TIMESTAMP — Skipping: weekend" >> "$LOG_FILE"
    exit 0
fi

# ── Check claude CLI is available ────────────────────────────────────────────
if ! command -v claude &> /dev/null; then
    echo "$TIMESTAMP — ERROR: claude CLI not found. Is Claude Code installed?" >> "$LOG_FILE"
    exit 1
fi

# ── Run pre-market routine ────────────────────────────────────────────────────
echo "$TIMESTAMP — Starting pre-market routine..." >> "$LOG_FILE"

cd "$REPO_DIR"

claude --print \
    "Read commands/pre-market.md and run it exactly as written.
     The skills market-breadth-analyzer, uptrend-analyzer, and sector-analyst
     already exist in skills/ — read their SKILL.md files and execute their
     scripts. Do not create anything new. Save output to
     reports/logs/market_context_${DATE}.md as instructed in the command." \
    --allowedTools "Bash,Read,Write" \
    >> "$LOG_DIR/market_context_${DATE}.md" 2>> "$LOG_FILE"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "$TIMESTAMP — Completed successfully. Output: reports/logs/market_context_${DATE}.md" >> "$LOG_FILE"
else
    echo "$TIMESTAMP — ERROR: claude exited with code $EXIT_CODE" >> "$LOG_FILE"
fi

exit $EXIT_CODE
