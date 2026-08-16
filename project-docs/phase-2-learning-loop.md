# Phase 2 — TA Learning Loop

**Duration:** ~8 weeks after Phase 1 exit
**Goal:** Turn confluence sessions and trade outcomes into a personal playbook. Observe TW + GEX/VEX patterns, coach operator charting, refine theses, and close the loop with postmortems — not fundamentals-quality tracking or screener-first R&D.

---

## Prerequisites

Phase 1 exit criteria met. You should have:

- Reliable TW list / GEX-VEX / operator chart → `ta-confluence` cadence
- 10+ trades logged across ≥2 types in `trader-memory-core`
- 3+ co-pilot Agentic trades with thesis logging
- Playbook seed started in [playbook.md](playbook.md) (TA setup skeleton OK)

---

## What you're building

### 2.1 — Session pattern journal (Weeks 1–2)

After each confluence session, write a short dated note (markdown under `reports/charts/confluence/` or `reports/logs/ta_patterns_YYYY-MM-DD.md`):

- Recurring TW list / HTF stack patterns (colors that worked, fights that failed)
- Recurring GEX/VEX structures (king placement, air pockets, traps)
- Operator chart habits worth keeping or fixing
- Verdict quality: PLAY / WATCH / NO_TRADE vs what happened next (when known)

**Rules:** Cite artifacts, not generic TA. Propose only — operator approves playbook merges.

### 2.2 — Charting coach loop (Weeks 2–4)

Active coaching on operator markups:

- What to mark vs ignore on the next chart
- Level hygiene (S/R, fib, VP shelf, SMA stack conflicts)
- Bias mistakes (forcing PLAY without period list color, ignoring HTF fight)
- One concrete “try this next session” item per review

Output lives in playbook **Charting Coach** section + session notes. No silent edits to risk config.

### 2.3 — Personal TA playbook (Weeks 2–5)

Expand [playbook.md](playbook.md) with setups derived from the three sources:

```markdown
### Setup: [Name]
- TW conditions (period list color, HTF stack / fight rules)
- Map conditions (GEX/VEX magnets, kings, traps)
- Operator chart conditions (S/R, fib, VP, SMA)
- Entry trigger
- Invalidation (TW + maps + operator — one kill each when data exists)
- Target methodology
- When NOT to take it
- Linked confluence / thesis IDs
```

**Process:**

- Document 2–3 live setups even if rough
- Weekly distill: session notes → candidate playbook deltas for human approve/reject
- Prefer extending `ta-confluence` judgment refs over building new skills

### 2.4 — Thesis + postmortem loop (Weeks 4–6)

- Confluence PLAY / strong WATCH → thesis draft (trader-memory-core)
- Optional deep-research only for PLAY or verge-of-confluence (user OK)
- On close: postmortem tied to which source domains were right/wrong
- Track invalidation discipline (did TW/map/chart kills fire? Did you act?)

Defer old “research quality tracking for every deep-research report” — only track research that was actually requested under the TA gate.

### 2.5 — Lightweight behavior checks (Week 5–6)

Use trader-memory history for **TA-relevant** process flags only (no separate Streamlit-first build):

- Entry without confluence artifact / operator chart
- PLAY override without documented reason
- Ignored invalidation after entry
- Thesis drift past stated kill levels
- Overtrading relative to playbook max/day (when defined)

Optional later: automate as a thin script. Do not block Phase 2 on a full behavioral-pattern-detector product.

### 2.6 — Playbook validation (Weeks 6–7)

Validate setups against logged outcomes (small-n honest):

- Forward journal: next N similar setups → hit rate / R multiple
- Use `backtest-expert` only if a setup is rule-crisp enough; do not force Sharpe gates on n≪100
- Retire or revise rules that fail out-of-sample notes

Quality bar for graduating a setup to default co-pilot use:

- Written invalidation in all three domains (or explicit gap)
- ≥5 logged instances with postmortem notes (or documented exception)
- Operator sign-off in playbook

### 2.7 — Skill improvement (optional, Weeks 7–8)

Enable skill-improvement loop only with branch protection and human PR review. Leave skill-generation disabled until Phase 3. Prefer patches to TA skills / judgment refs over new fundamentals skills.

### 2.8 — Skylit paid subscription decision (end of Phase 2)

Pastes/screenshots already in use. Subscribe to Skylit **API / $99/mo** only if YES to ALL:

- Specific playbook setup needs data you cannot get from pasted maps
- Free / paste workflow exhausted
- Can afford 3 months ($297)
- Strategy could pay for subscription within 2 months at account size

Document YES/NO in [decisions.md](../decisions.md).

---

## Exit criteria

- [ ] Recurring TA pattern journal active (session notes for ≥4 weeks)
- [ ] Charting coach section in playbook with ≥5 actionable items applied or rejected
- [ ] Personal playbook has 3+ TA setups (TW + maps + operator conditions)
- [ ] 30+ total trades logged with thesis discipline
- [ ] ≥5 closed trades with postmortems linking confluence domains
- [ ] At least 2 playbook rules explicitly approved from weekly distill
- [ ] Deep-research usage stays gated (PLAY / verge / explicit ask) — spot-check session logs
- [ ] Explicit YES/NO on Skylit paid subscription in decisions.md
- [ ] Monthly Anthropic spend &lt; $30

---

## Common pitfalls

1. Sliding back into fundamentals-first deep-research as daily default
2. Writing playbook rules without citing TW/map/chart artifacts
3. Auto-merging skill-improvement or playbook LLM suggestions
4. Buying Skylit API “just to see” — $99/mo is the project budget
5. Forcing backtest Sharpe gates on tiny trade samples

---

## What's NOT in Phase 2

- Autonomous MCP execution (Phase 3)
- Rebuilding a fundamentals research-quality program as the phase goal
- New upstream skill creation beyond thin wrappers / TA judgment extensions
- Streamlit dashboard as a Phase 2 blocker (nice-to-have only)

---

## When ready to advance

Update `PROJECT.md` Active Phase to Phase 3. Read [phase-3-agentic-execution.md](phase-3-agentic-execution.md).
