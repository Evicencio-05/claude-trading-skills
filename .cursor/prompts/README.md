# Cursor Prompts

Reusable, copy-paste prompts for Cursor Agent in this repo. Unlike `commands/` (full workflow specs) or `.cursor/rules/` (always-on context), these are **task invocation prompts** — short, explicit instructions you paste into chat.

| Prompt | Purpose |
|--------|---------|
| [prompt-engine.md](prompt-engine.md) | Meta-prompt: generate new task prompts for this repo |
| [codebase-cleanup.md](codebase-cleanup.md) | Audit overlap, dead code, and doc duplication; safe cleanup plan |
| [phase-1b-robinhood-focus.md](phase-1b-robinhood-focus.md) | Defer futures Phase 2; improve research pipeline; start Robinhood MCP co-pilot trading |
| [sync-phase-docs.md](sync-phase-docs.md) | Reconcile PENDING_WORK + STATUS + phase docs to completed work on disk |
| [systemd-stale-research-updater.md](systemd-stale-research-updater.md) | Weekly systemd job: scan stale research for positions + watchlist; queue updates |
| [thesis-manager-research-ui.md](thesis-manager-research-ui.md) | Streamlit Research page: staleness dashboard, report preview, update prompts |

## When to use what

| Artifact | Use when |
|----------|----------|
| `.cursor/prompts/*.md` | One-shot or repeatable chat invocations |
| `commands/*.md` | Multi-step workflows shared by Claude Code + Cursor |
| `.cursor/skills/*/SKILL.md` | Cursor skill discovery + thin wrappers over commands |
| `.cursor/rules/*.mdc` | Persistent agent behavior (router, MCP guardrails) |

Single source of truth: workflow *logic* lives in `commands/` and `skills/`; prompts here should **point at** those files, not duplicate them.
