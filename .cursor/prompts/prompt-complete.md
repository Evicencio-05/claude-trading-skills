# Prompt Run — Completion & Verification

## Goal
Verify that a **finished** Cursor Agent run met the task prompt's Goal and Outputs; document gaps, prompt defects, and durable follow-ups — without redoing the whole task unless the user asks.

## Inputs
- **Task prompt (required):** one of:
  - **Ephemeral (default):** `inline` — read the prompt from the user context block below or from chat history
  - **Durable (Tier 2):** e.g. `sync-phase-docs.md` — read `.cursor/prompts/<name>.md` in full
- **Task family (required for learning loop):** slug from [state/prompt_learnings.yaml](../../state/prompt_learnings.yaml) (e.g. `thesis_manager_dev`, `doc_sync`, `infra_systemd`) or `custom` if none fits
- **User notes (optional):** what felt wrong, manual fixes you already made
- **Mode:** `verify-only` (default) | `verify-and-fix-prompt` (Tier 2 durable files only — minimal path/phase fixes)

## Pre-flight
- [ ] Read the task prompt: Goal, Inputs, Pre-flight, Steps, Outputs, Do not, linked `commands/` / `skills/`
- [ ] Read [state/prompt_learnings.yaml](../../state/prompt_learnings.yaml) — note patterns that would have prevented defects
- [ ] Read [PENDING_WORK.md](../../PENDING_WORK.md) if follow-ups may be added (dedupe open items)
- [ ] Read [project-docs/STATUS.md](../../project-docs/STATUS.md) for active phase name (flag stale phase refs)

## Phase 1 — Evidence harvest

From the **conversation and repo**, collect evidence only — do not assume success.

**Optional (save tokens):** write evidence to a temp file, then draft the retro skeleton locally:

```bash
uv run python3 scripts/local_llm_cli.py retro-draft \
  --evidence /tmp/retro_evidence.txt \
  --task-family <task_family_slug>
```

Review and edit CLI output before Phase 2 — do not trust unverified local model prose.

```bash
ls -la reports/ 2>/dev/null | tail -20
```

For each path or pattern listed under **## Outputs** in the task prompt:

| Check | Pass criteria |
|-------|----------------|
| File exists | `test -f` or `ls` match |
| Naming | Date/suffix matches repo convention stated in prompt |
| Language | English for reports |
| Content vs Goal | File or chat deliverable actually addresses the one-sentence Goal |

For **## Pre-flight** checkboxes, record each: **done** | **skipped** | **failed** — and whether skipping mattered for the Goal.

For **Steps** that reference `commands/` or `skills/`, confirm the agent **linked or followed** them (not reimplemented inline long workflow text).

## Phase 2 — Verification matrix

Fill this table in chat (and in the retro report):

| Area | Status | Evidence |
|------|--------|----------|
| Goal | met / partial / failed | quote path, command output, or chat excerpt |
| Outputs | all / some / none | per-file paths |
| Pre-flight | N/M done | list which |
| Integration | ok / gaps | commands/skills used; IRA / Phase 5 / thesis_store / TDD if applicable |
| Do not | clean / violations | trades, commits, secrets, direct `state/theses/` writes |

**Repo gates (when task touched trading/portfolio/theses):**

- No autonomous trade execution (co-pilot only)
- Robinhood: read all accounts; trade Agentic only; IRA options flagged
- Thesis writes via `thesis_store.py` / thesis-manager — not raw YAML edits
- No secrets or username absolute paths in committed artifacts

## Phase 3 — Defect log

Use normalized **root cause** slugs when possible (matches [state/prompt_learnings.yaml](../../state/prompt_learnings.yaml)):

| # | What went wrong | Root cause | Suggested fix (one line) |
|---|-----------------|------------|--------------------------|
| 1 | | e.g. direct_state_theses_edit, stale_phase_name, wrong_output_path | |

If **verify-and-fix-prompt** and task was **Tier 2 durable**, apply **minimal** edits to `.cursor/prompts/<task>.md` only. **Do not edit ephemeral prompts on disk** — fixes flow to learnings via retro + weekly distiller.

If defects match existing patterns in learnings YAML, note which pattern id — distiller increments `seen` automatically.

## Phase 4 — Write retro report

Save `reports/prompts/prompt_run_retro_YYYY-MM-DD.md` (required — feeds weekly distiller):

```markdown
# Prompt Run Retro — YYYY-MM-DD

**Task prompt:** inline | `.cursor/prompts/<name>.md`
**Task family:** thesis_manager_dev
**Goal verdict:** met | partial | failed

## Prompt snapshot
<details>
<summary>Full prompt text (for ephemeral runs)</summary>

[paste entire task prompt here]

</details>

## Verification matrix
[paste table]

## Defect log
[paste table]

## Prompt fixes applied
- [none | Tier 2 file: change]

## Meta notes
- [bullets or none — distiller may promote patterns when seen >= 3]

## Follow-ups
- PENDING_WORK: [added | none | user to approve]
```

## Phase 5 — PENDING_WORK (optional)

Only if user said **track follow-ups** or defects imply durable work:

- Search [PENDING_WORK.md](../../PENDING_WORK.md) for duplicates
- Append under the correct section with legend tags
- Update **Last updated** in header
- Do **not** mark existing items `[x]` here — use [sync-phase-docs.md](sync-phase-docs.md)

## Rules
- **Evidence only** — failed Goal without a missing file or clear gap is still **failed**
- **Do not redo** the full task unless user explicitly asks
- **Always write retro** — even when Goal met (confirms patterns for distiller)
- Prefer this file over per-task completion sections (single unbiased rule set)

## Do not
- Run new deep-research, trades, or billing changes
- Commit unless user explicitly asks
- Mark PENDING_WORK items complete without evidence
- Invent outputs that were never promised in the task prompt
- Save Tier 1 prompts to `.cursor/prompts/` — learning lives in retro + YAML

## User context (paste when invoking)

```
Task prompt: inline | <name>.md
Task family: <slug from prompt_learnings.yaml>
Prompt text (required if inline):
---
[paste full prompt here]
---
What I fixed manually (optional): ...
Track in PENDING_WORK: yes | no
Mode: verify-only | verify-and-fix-prompt
```
