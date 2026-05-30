# Cursor Prompts

Reusable, copy-paste prompts for Cursor Agent in this repo. Unlike `commands/` (full workflow specs) or `.cursor/rules/` (always-on context), these are **task invocation prompts** — short, explicit instructions you paste into chat.

| Prompt | Purpose |
|--------|---------|
| [prompt-engine.md](prompt-engine.md) | Meta-prompt: generate new task prompts for this repo |
| [codebase-cleanup.md](codebase-cleanup.md) | Audit overlap, dead code, and doc duplication; safe cleanup plan |
| [phase-1b-robinhood-focus.md](phase-1b-robinhood-focus.md) | Defer futures Phase 2; improve research pipeline; start Robinhood MCP co-pilot trading |
| [remove-futures-equity-focus.md](remove-futures-equity-focus.md) | Remove futures permanently; 3-phase equity-only roadmap (Research → Learning Loop → Agentic) |
| [sync-phase-docs.md](sync-phase-docs.md) | Reconcile PENDING_WORK + STATUS + phase docs to completed work on disk |
| [systemd-stale-research-updater.md](systemd-stale-research-updater.md) | Weekly systemd job: scan stale research for positions + watchlist; queue updates |
| [thesis-manager-research-ui.md](thesis-manager-research-ui.md) | Streamlit Research page: staleness dashboard, report preview, update prompts |
| [thesis-manager-improvements.md](thesis-manager-improvements.md) | Audit + TDD improvements: UX/UI, services, position handling, edge cases |
| [thesis-manager-dashboard-mockup-image.md](thesis-manager-dashboard-mockup-image.md) | AI image prompts: dark-theme mockups for all four app pages |
| [thesis-manager-modern-ui.md](thesis-manager-modern-ui.md) | Implement mockup-style UI: collapsible sidebar, button nav (no radio) |

## When to use what

| Artifact | Use when |
|----------|----------|
| `.cursor/prompts/*.md` | One-shot or repeatable chat invocations |
| `commands/*.md` | Multi-step workflows shared by Claude Code + Cursor |
| `.cursor/skills/*/SKILL.md` | Cursor skill discovery + thin wrappers over commands |
| `.cursor/rules/*.mdc` | Persistent agent behavior (router, MCP guardrails) |

Single source of truth: workflow *logic* lives in `commands/` and `skills/`; prompts here should **point at** those files, not duplicate them.
