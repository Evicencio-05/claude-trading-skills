# PENDING_WORK.md

> Persistent task queue across Cursor, Claude Code, and terminal sessions.
> **Last updated:** 2026-05-28
> **Active phase:** Phase 1 — Audit & Activate
> **Session load order:** [PROJECT.md](PROJECT.md) → [LOAD_GUIDE.md](LOAD_GUIDE.md) → [project-docs/STATUS.md](project-docs/STATUS.md)

**Legend:** Auto-execute = agent can do without approval. Needs approval = money/architecture. Needs data = human-only input.

**Fork policy:** Do not modify upstream `skills/<name>/SKILL.md` or `skills/<name>/scripts/` except fixes listed in [decisions.md](decisions.md). Never write `state/theses/` directly — use `thesis_store.py` / thesis-manager.

---

## Done (do not redo)

- [x] Cursor harness: `.cursor/rules/`, `.cursor/skills/` symlinks, [AGENTS.md](AGENTS.md)
- [x] `/deep-research` Phase 1 exit (3+ tickers) — no new runs in current batch
- [x] **P2 verified 2026-05-28:** breadth=42, uptrend=54 from nested JSON; LOW confidence expected without regime/top_risk
- [x] **pre_market:** 13+ days in `posture_history.log`; timer units in `~/.config/systemd/user/`; dry-run OK
- [x] **robinhood-sync systemd:** `launchd/robinhood-sync.*` created; timer enabled in user systemd
- [x] **thesis-manager:** `py_compile` + Streamlit headless start OK; 16 theses load from store
- [x] **MCP docs:** decisions.md + playbook + log-positions updated (human account discovery still needed)

---

## Auto-execute

- [ ] **Robinhood MCP account discovery** (human in Claude Code)
      List accounts via Agentic MCP → append to [decisions.md](decisions.md)
      Confirm whether Portfolio B IRA is visible

- [ ] **ACCOUNT_MAP refresh** after login change
      `uv run python3 scripts/robinhood_sync.py --dry-run`

- [ ] **scenario-analyzer Japanese output** — DEFERRED (upstream SKILL.md policy)

---

## Needs approval

- [ ] **Upgrade FMP Starter ($29/mo)** — approved verbally, not activated

---

## Needs data (human input only)

- [ ] **Log open IRA positions** — thesis-manager Add Thesis
- [ ] **Log expired as CLOSED** — POWL, TSLA, PENG $55C x3
- [ ] **Verify HOOD/ICHR June expiries** before logging

---

## Phase 2 (locked)

See [project-docs/phase-2-futures-skills.md](project-docs/phase-2-futures-skills.md).
