# Cursor Prompts — Learning Loop

Task prompts are **ephemeral by default** (Tier 1). Durable knowledge lives in [state/prompt_learnings.yaml](../../state/prompt_learnings.yaml), not a growing file library.

## Invoke chain

| Step | Prompt | When |
|------|--------|------|
| 1 — Author | [prompt-engine.md](prompt-engine.md) | Draft a new task prompt (chat only by default) |
| 2 — Execute | Paste prompt from step 1 | Run the work |
| 3 — Verify | [prompt-complete.md](prompt-complete.md) | After the run — retro report feeds the learning loop |
| 4 — Distill | [prompt-distill.md](prompt-distill.md) or weekly systemd timer | Process retros → YAML → digest |

Meta prompts (Tier 0) maintain the loop; they are not trading workflows.

## Tier policy

| Tier | What | Where |
|------|------|-------|
| 0 Meta | Engine, complete, distill | This directory — always kept |
| 1 Ephemeral | One-off tasks | **Chat only** — snapshot in retro |
| 2 Durable | Repeatable invocations | `.cursor/prompts/<name>.md` — see table below |
| 3 Workflow | Multi-step | `commands/` — not saved here |

Full policy: [prompt-engine.md](prompt-engine.md) § Tier policy.

## Tier 2 — durable prompts

| Prompt | Purpose |
|--------|---------|
| [sync-phase-docs.md](sync-phase-docs.md) | Reconcile PENDING_WORK + STATUS + phase docs to disk evidence |
| [codebase-cleanup.md](codebase-cleanup.md) | Audit overlap, dead code, doc duplication |
| [systemd-stale-research-updater.md](systemd-stale-research-updater.md) | Weekly systemd job: stale research queue |

## Tier 0 — meta prompts

| Prompt | Purpose |
|--------|---------|
| [prompt-engine.md](prompt-engine.md) | Generate task prompts; reads `state/prompt_learnings.yaml` |
| [prompt-complete.md](prompt-complete.md) | Post-run verification + retro report |
| [prompt-distill.md](prompt-distill.md) | Run distiller script; review weekly digest |

## Automation

Weekly (after stale-research scan):

```bash
uv run python3 scripts/distill_prompt_learnings.py
```

Systemd: [launchd/prompt-learning.timer](../../launchd/prompt-learning.timer) — Sunday 6:30 PM local.

Output: `reports/prompts/prompt_learning_digest_YYYY-MM-DD.md` (≤15-line header; optional detail).

## Archive

One-shot prompts moved to [archive/](archive/) — knowledge extracted to `state/prompt_learnings.yaml` `task_families`. Regenerate via `prompt-engine`, do not reuse archived files.

## When to use what

| Artifact | Use when |
|----------|----------|
| `prompt-engine` + chat prompt | Almost all tasks |
| Tier 2 `.cursor/prompts/*.md` | Monthly/weekly repeatable invocations |
| `commands/*.md` | Multi-step workflows (Claude Code + Cursor) |
| `.cursor/skills/*/SKILL.md` | Cursor skill discovery |
| `state/prompt_learnings.yaml` | Machine-learned patterns (distiller-maintained) |
| `PENDING_WORK.md` | Cross-session queue |

Single source of truth: workflow *logic* in `commands/` and `skills/`; prompts **point at** those files.
