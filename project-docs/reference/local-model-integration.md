# Local Model Integration (Ollama)

> **Read this when:** setting up Ollama, routing bulk tasks off Cursor tokens, or wiring `--llm-ideas-cmd` / `--enable-llm` flags.

This fork uses **Ollama + qwen2.5:7b** as the free tier for bulk, low-stakes text work per [cost-discipline.md](cost-discipline.md). Cursor agents delegate to repo scripts instead of generating long prose in subscription context.

---

## Quick start

```bash
# Install Ollama: https://ollama.com
ollama pull qwen2.5:7b

# Verify from repo root
uv run python3 scripts/local_llm_cli.py health
# OK: qwen2.5:7b @ http://127.0.0.1:11434
```

Optional env in repo-root `.env` (gitignored):

```bash
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:7b
```

Optional overrides: copy [config/local_llm.yaml.example](../../config/local_llm.yaml.example) to `config/local_llm.yaml` (gitignored if you add secrets — host/model only is fine committed in example).

---

## Core components

| Path | Role |
|------|------|
| [scripts/local_llm.py](../../scripts/local_llm.py) | Ollama HTTP client: `is_available()`, `chat()`, `distill_suggest()` |
| [scripts/local_llm_cli.py](../../scripts/local_llm_cli.py) | Task CLI for Cursor delegation and pipeline hooks |
| [.cursor/rules/local-model-routing.mdc](../../.cursor/rules/local-model-routing.mdc) | When Cursor agents must shell out vs stay in agent |
| [reports/logs/local_llm_usage.jsonl](../../reports/logs/local_llm_usage.jsonl) | Append-only usage log (`estimated_cost_usd: 0`) |

---

## Routing matrix

| Task | Command / integration | Writes repo state? | Human review? |
|------|----------------------|-------------------|---------------|
| Health check | `local_llm_cli.py health` | No | No |
| Ad-hoc prompt | `local_llm_cli.py complete --prompt FILE` | No | Optional |
| Edge hints | `build_hints.py --llm-ideas-cmd "uv run python3 scripts/local_llm_cli.py edge-hints"` | Output YAML only | Spot-check hints |
| Prompt retro draft | `local_llm_cli.py retro-draft --evidence FILE --task-family SLUG` | No (stdout) | **Yes** before saving retro |
| Commit message draft | `local_llm_cli.py commit-message` | No | **Yes** — user runs `git commit` |
| Distill LLM suggestions | `distill_prompt_learnings.py --enable-llm` | Digest section only | **Yes** before editing YAML |
| Skill idea abstraction | `mine_session_logs.py --llm-provider local` | Backlog JSON | Spot-check 10% |
| Deep/update research | Cursor / Claude API | Yes | N/A — **never local** |
| Robinhood MCP / theses | Cursor agent | Yes | N/A — **never local** |
| Skill improvement PRs | Claude CLI | Yes | N/A — **never local** |

---

## Cursor agent usage

Rule: [.cursor/rules/local-model-routing.mdc](../../.cursor/rules/local-model-routing.mdc) (always on).

**Delegate to local CLI when:**

1. **Prompt retro** — gather evidence to a file, then:

```bash
uv run python3 scripts/local_llm_cli.py retro-draft \
  --evidence /tmp/retro_evidence.txt \
  --task-family thesis_manager_dev
```

Review output, then save `reports/prompts/prompt_run_retro_YYYY-MM-DD.md` per [prompt-complete.md](../../.cursor/prompts/prompt-complete.md).

2. **Commit message only** (user commits):

```bash
uv run python3 scripts/local_llm_cli.py commit-message
```

3. **Weekly distill with LLM review**:

```bash
uv run python3 scripts/distill_prompt_learnings.py --enable-llm
```

Read **LLM suggestions (review before merge)** in the digest — do not auto-edit `state/prompt_learnings.yaml`.

**Stay on Cursor subscription model when:** multi-file refactors, MCP, pytest loops, research synthesis, trading decisions.

---

## Workflow recipes

### Edge hint extractor

```bash
uv run python3 skills/edge-hint-extractor/scripts/build_hints.py \
  --market-summary path/to/market_summary.json \
  --anomalies path/to/anomalies.json \
  --llm-ideas-cmd "uv run python3 scripts/local_llm_cli.py edge-hints" \
  --output-dir reports/
```

Contract: JSON on stdin, YAML hints on stdout — see [hints_schema.md](../../skills/edge-hint-extractor/references/hints_schema.md).

### Prompt learning distiller (optional LLM)

```bash
uv run python3 scripts/distill_prompt_learnings.py --dry-run
uv run python3 scripts/distill_prompt_learnings.py --enable-llm
```

Deterministic distill always runs first. LLM adds review-only suggestions to the digest.

### Skill idea miner (local abstraction)

```bash
uv run python3 skills/skill-idea-miner/scripts/mine_session_logs.py \
  --llm-provider local \
  --dry-run
```

Scoring still uses Claude CLI when available (`score_ideas.py` unchanged).

---

## What never uses local models

- Autonomous **git commit / push / PR**
- **Trade execution**, Robinhood MCP workflows, thesis lifecycle writes
- **Deep research** and **update research** synthesis
- **Skill improvement / generation** pipelines (quality gate)
- Formatting, lint, typecheck, data fetch (use `ruff`, scripts, APIs — see cost-discipline)

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Exit code 2, model not found | `ollama pull qwen2.5:7b` |
| Connection refused | Start Ollama service; check `OLLAMA_HOST` |
| Garbage YAML/JSON | Risk M1 — spot-check; fall back to Cursor/Claude for that task |
| Timeout | Increase `timeout_seconds` in `config/local_llm.yaml` |

---

## Cost logging

Each call appends one JSON line to `reports/logs/local_llm_usage.jsonl`:

```json
{"ts": "2026-05-31T12:00:00+00:00", "task": "edge_hints", "model": "qwen2.5:7b", "prompt_chars": 1200, "response_chars": 400, "estimated_cost_usd": 0.0}
```

---

## Related docs

- [cost-discipline.md](cost-discipline.md) — model tier table
- [AGENTS.md](../../AGENTS.md) — hybrid routing
- [cursor-integration.md](cursor-integration.md) — Cursor setup checklist
- [risk-register.md](risk-register.md) — M1 local model quality risk
