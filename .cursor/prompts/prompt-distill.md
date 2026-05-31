# Prompt Learning Distill — weekly maintenance

## Goal
Run the deterministic prompt learning distiller, summarize the digest, and optionally review auto-promoted patterns — without auditing every prompt file manually.

## Inputs
- **Mode:** `distill-only` (default) | `distill-and-review` (summarize top promoted patterns in chat)
- **Dry run:** yes | no (default no)

## Pre-flight
- [ ] Read [state/prompt_learnings.yaml](../../state/prompt_learnings.yaml)
- [ ] Check for unprocessed retros: `ls -1 reports/prompts/prompt_run_retro_*.md 2>/dev/null | tail -5`

## Steps

1. Run distiller:

```bash
uv run python3 scripts/distill_prompt_learnings.py --dry-run   # preview
uv run python3 scripts/distill_prompt_learnings.py             # apply
uv run python3 scripts/distill_prompt_learnings.py --enable-llm  # + Ollama suggestions (review only)
```

2. Read today's digest: `reports/prompts/prompt_learning_digest_YYYY-MM-DD.md`

   If `--enable-llm` was used, review **LLM suggestions (review before merge)** — do not auto-edit YAML.

3. If **distill-and-review**, summarize in chat (≤10 bullets):
   - Retros processed
   - Newly promoted patterns (id + fix one-liner)
   - Archived prompts moved to `.cursor/prompts/archive/`
   - Task family run count changes
   - **Action required:** none | optional review

4. Do **not** bulk-edit `prompt-engine.md` — learnings YAML is the machine source of truth; `prompt-engine` reads it at author time.

## Outputs
- Updated [state/prompt_learnings.yaml](../../state/prompt_learnings.yaml)
- [reports/prompts/prompt_learning_digest_YYYY-MM-DD.md](../../reports/prompts/prompt_learning_digest_YYYY-MM-DD.md)
- Archived one-shots in `.cursor/prompts/archive/` (if any eligible)

## Rules
- Deterministic distill always runs first; `--enable-llm` adds review-only Ollama suggestions to digest
- Idempotent — safe to re-run; retros processed once
- Weekly timer: `prompt-learning.timer` (Sunday 6:30 PM local, after research-staleness)

## Do not
- Rewrite all task prompts
- Commit unless user asks
- Edit archived prompts — regenerate from `task_families` via `prompt-engine`

## After run
Paste [prompt-complete.md](prompt-complete.md) with Task prompt: inline, Task family: prompt_maintenance
