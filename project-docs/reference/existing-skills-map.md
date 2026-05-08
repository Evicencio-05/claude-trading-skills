# Existing Skills Map

> **Read this when:** considering whether to build something new (check if it exists first), or in Phase 1 when auditing the upstream skills.

This is a quick-reference inventory of skills in the upstream `claude-trading-skills` repo. Use this to avoid duplicating existing functionality.

---

## Always Use These (validated foundations)

These skills are well-built and solve problems you definitely have:

- **`trader-memory-core`** — Persistent thesis store. THE foundation of the learning loop. Use from Day 1 of Phase 1.
- **`exposure-coach`** — Daily market posture synthesis. Should be your first morning command.
- **`technical-analyst`** — Generic chart analysis. Works on stocks, indices, futures, FX, crypto.
- **`market-news-analyst`** — Past-10-days market news with impact scoring. Useful for catalyst awareness.
- **`economic-calendar-fetcher`** — Critical for futures (FOMC, NFP, CPI move ES/NQ hard).
- **`position-sizer`** — Risk-based sizing. Will need extension for futures (Phase 2).

---

## Pre-Built Commands (use as-is)

These are full workflows already wired up:

| Command | What it does | Useful for |
|---|---|---|
| `/deep-research <TICKER>` | 8-phase comprehensive stock research | Equity research |
| `/update-research <TICKER>` | Diff-based update of a previous report | Watchlist maintenance |
| `/intraday-options <TICKER> <CAPITAL>` | Intraday options swing analysis | Same-day options trades |
| `/options-strategy-planner <TICKER>` | Comprehensive options strategy plan | Multi-week options positions |
| `/review-portfolio` | Batch update across watchlist | Weekly portfolio review |
| `/scenario-analyzer <headline>` | News headline → 18-month scenario projection | Macro / event analysis |

**Implication for Phase 2:** mirror the `/intraday-options` pattern when building `/futures-setup`. Same structure, different asset class.

---

## Market Context Skills (use heavily)

| Skill | What it does | Cost |
|---|---|---|
| `market-breadth-analyzer` | 6-component breadth score | Free (CSV) |
| `uptrend-analyzer` | 5-component uptrend ratio | Free (CSV) |
| `macro-regime-detector` | Cross-asset regime detection | FMP |
| `market-top-detector` | 6-component distribution detection | Free |
| `ftd-detector` | Follow-Through Day detector | FMP |
| `sector-analyst` | Sector rotation patterns | Free (CSV) |
| `theme-detector` | Trending themes (3D scoring) | Free / FMP optional |
| `institutional-flow-tracker` | 13F filings analysis | FMP |

**For futures focus:** `market-breadth-analyzer` and `market-top-detector` are the most relevant. The others are equity-rotation-focused.

---

## Stock Screening (lower priority for futures focus)

| Skill | What it does |
|---|---|
| `vcp-screener` | Minervini VCP pattern |
| `canslim-screener` | O'Neil CANSLIM (Phase 3.1, 7 components) |
| `value-dividend-screener` | High-yield dividend stocks |
| `dividend-growth-pullback-screener` | Dividend growth at oversold levels |
| `pead-screener` | Post-earnings drift |
| `earnings-trade-analyzer` | 5-factor earnings reaction scoring |
| `kanchi-dividend-sop` | 5-step dividend SOP |
| `pair-trade-screener` | Statistical arbitrage |
| `finviz-screener` | Natural language → FinViz filters |

**Futures focus implication:** Most of these are not directly applicable. Audit them in Phase 1 with low expectations. Keep the patterns for reference (the SKILL.md structure, the report templates, the API integration patterns).

---

## Trade Planning Skills

| Skill | What it does | Notes |
|---|---|---|
| `position-sizer` | Risk-based position sizing | Extend in Phase 2 for futures |
| `options-strategy-advisor` | Black-Scholes + 17 strategies | Not relevant for futures (no options on futures in scope) |
| `parabolic-short-trade-planner` | 3-phase Qullamaggie short setup | **Study this as a template** — most production-mature skill |
| `breakout-trade-planner` | Breakout setup planner | Generic, may be adaptable to futures |
| `portfolio-manager` | Alpaca MCP integration | **Study this as a template** for `tradovate-integration` |

---

## Learning Loop Infrastructure (use throughout)

| Skill | What it does | Phase |
|---|---|---|
| `trader-memory-core` | Thesis lifecycle (IDEA → ENTRY_READY → ACTIVE → CLOSED) | 1+ |
| `signal-postmortem` | Post-trade outcome classification | 3+ |
| `edge-pipeline-orchestrator` | End-to-end edge research pipeline | 3+ |
| `edge-strategy-reviewer` | Deterministic strategy quality gate | 3+ |
| `edge-signal-aggregator` | Aggregates signals from multiple skills | 3+ |
| `edge-candidate-agent` | Converts research tickets → strategy specs | 3+ |
| `trade-hypothesis-ideator` | Generates falsifiable hypotheses | Optional |
| `strategy-pivot-designer` | Detects backtest stagnation, proposes pivots | 4+ |

---

## Quality / Self-Improvement Infrastructure

| Skill | What it does | Phase |
|---|---|---|
| `dual-axis-skill-reviewer` | Scores skills (deterministic + optional LLM) | 3+ |
| `skill-idea-miner` | Mines session logs for new skill ideas | 3+ (optional) |
| `skill-designer` | Generates Claude CLI prompts for new skills | 3+ (optional) |
| `data-quality-checker` | Validates markdown reports | All |
| `skill-improvement-loop` | Daily auto-review + improvement PRs | 3+ |
| `skill-generation-pipeline` | Weekly mining + daily skill design + PRs | 4+ (optional) |

**Important:** The auto-PR pipelines (skill-improvement-loop, skill-generation-pipeline) require careful PR review. Don't enable them until Phase 3.

---

## Skills That Don't Exist Yet (you'll build these)

| Phase | Skill | Why it's needed |
|---|---|---|
| 2 | `lucid-rules-engine` | No prop firm rules engine exists |
| 2 | `futures-position-sizer` | `position-sizer` doesn't know futures contract math |
| 2 | `tradovate-integration` | Existing repo uses Alpaca for stocks, not Tradovate for futures |
| 2 | `futures-pre-market-scan` | No CME futures pre-market scanner exists |
| 2 | `futures-session-monitor` | No real-time intraday monitor for futures session structure |
| 3 | `behavioral-pattern-detector` | No personal behavioral pattern detection |
| 5 | `futures-executor` | No autonomous executor (and shouldn't exist before Phase 5) |

---

## Pattern Templates (study these before building)

When building new skills, study the closest existing analog:

- **Offline calculation skill** → study `position-sizer`
- **API integration skill** → study `portfolio-manager` (Alpaca)
- **Multi-phase production skill with FSM** → study `parabolic-short-trade-planner`
- **Orchestration skill** → study `edge-pipeline-orchestrator`
- **Learning/memory skill** → study `trader-memory-core`
- **Daily monitoring skill** → study `ibd-distribution-day-monitor`
- **Wrapper around other skills** → study `exposure-coach`

---

## Skills to Probably Skip

These exist but are likely not relevant for your futures-focused workflow:

- `stanley-druckenmiller-investment` — Macro philosophy guide; may have value but not core
- `us-market-bubble-detector` — Useful occasionally but low frequency
- `downtrend-duration-analyzer` — Visualization tool, low-frequency utility
- All the dividend-specific skills — Equity income focus, not futures
- `pair-trade-screener` — Statistical arbitrage on equities

Your Phase 1 audit will confirm which of these are genuinely useless to you. Don't delete them — just mark "not relevant" in `skills_audit.md`.

---

## Authoritative Source

This map is a quick reference. The authoritative inventory is:
- `README.md` (upstream) — full skill descriptions
- `CLAUDE.md` (upstream) — operational details, API requirements
- `docs/en/skill-catalog.md` (upstream) — categorized catalog

Keep this map updated when:
- You build a new skill
- You retire a skill
- You significantly change a skill's purpose
- An upstream pull adds new skills (if you ever pull from upstream)
