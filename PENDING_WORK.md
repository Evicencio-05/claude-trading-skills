# PENDING_WORK.md

> Persistent task queue across Cursor, Claude Code, and terminal sessions.
> **Last updated:** 2026-05-29
> **Active phase:** Phase 1 — Audit & Activate
> **Session load order:** [PROJECT.md](PROJECT.md) → [LOAD_GUIDE.md](LOAD_GUIDE.md) → [project-docs/STATUS.md](project-docs/STATUS.md)

**Legend:** Auto-execute = agent can do without approval. Needs approval = money/architecture. Needs data = human-only input.

**Fork policy:** Do not modify upstream `skills/<name>/SKILL.md` or `skills/<name>/scripts/` except fixes listed in [decisions.md](decisions.md). Never write `state/theses/` directly — use `thesis_store.py` / thesis-manager.

---

## Done (do not redo)

- [x] Cursor harness: `.cursor/rules/`, `.cursor/skills/` symlinks, [AGENTS.md](AGENTS.md)
- [x] Robinhood MCP integration docs: [robinhood-mcp-integration.md](project-docs/reference/robinhood-mcp-integration.md), `.cursor/mcp.json.example`, `robinhood-mcp.mdc`, `robinhood-portfolio-review` skill
- [x] MCP hybrid: `robinhood_mcp.py` CLI, `config/robinhood_accounts.yaml`, setup script, direct URL for Cursor
- [x] MCP structuredContent proxy (CLI-only): `scripts/mcp_stdio_structured_content_proxy.py`
- [x] log-positions Source B (MCP snapshot path) in command + skill
- [x] `/deep-research` Phase 1 exit (3+ tickers) — no new runs in current batch
- [x] P2, pre_market, robinhood-sync systemd, thesis-manager (see prior session)

---

## Auto-execute

- [ ] **Robinhood MCP — connect in Cursor (you)**
      1. `bash scripts/setup_robinhood_mcp.sh` (from repo root)
      2. Restart Cursor; confirm `robinhood-trading` green
      3. Run discovery prompts in [robinhood-mcp-integration.md](project-docs/reference/robinhood-mcp-integration.md)
      4. Fill account table in [decisions.md](decisions.md)

- [ ] **First MCP portfolio review**
      Invoke skill `robinhood-portfolio-review` after MCP connected

- [ ] **ACCOUNT_MAP refresh** — `uv run python3 scripts/robinhood_sync.py --dry-run`

- [ ] **scenario-analyzer Japanese output** — DEFERRED

- [x] **MCP ingest bridge** — `robinhood_mcp.py ingest-pending` (replaces separate script)

---

## Needs approval

- [ ] **Upgrade FMP Starter ($29/mo)** — approved verbally, not activated

---

## Needs data (human input only)

- [ ] **Log open IRA positions** — MCP Source B + `log-positions` or thesis-manager
- [ ] **Log expired as CLOSED** — POWL, TSLA, PENG $55C x3
- [ ] **Verify HOOD/ICHR June expiries** before logging

---

## Phase 2 (locked)

See [project-docs/phase-2-futures-skills.md](project-docs/phase-2-futures-skills.md).
