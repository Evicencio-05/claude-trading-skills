# Tech Stack Decisions

> **Read this when:** adding new dependencies, choosing tools for a new component, or evaluating whether to swap existing infrastructure.

---

## Locked-In Choices (do not change without explicit decision)

| Concern | Choice | Why |
|---|---|---|
| Language | Python 3.11+ | Already required by upstream repo; rich ecosystem for trading/data/ML |
| Package manager | `uv` | Already used by upstream repo; fast and reproducible |
| Code formatting | `ruff` | Already configured in pre-commit; deterministic; replaces black/isort/flake8 |
| Type checking | `mypy` | Already in pre-commit; required by repo conventions |
| Testing | `pytest` | Already used; conventions documented in upstream `CLAUDE.md` |
| Pre-commit | `pre-commit` framework | Already configured |
| Schema validation | Pydantic | Already used by upstream repo |
| Logging | `structlog` | Required by upstream repo conventions |
| Async I/O | `asyncio` + `httpx` | Required by upstream conventions |

These are not up for debate. Keep them.

---

## Defaults That You'll Add for This Project

| Concern | Choice | Notes |
|---|---|---|
| Database (structured) | SQLite | Already used by `trader-memory-core`; no infra overhead |
| Database (vector) | Chroma local | Standard for the existing learning loop |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) | Free, local, fast; no API needed |
| Local LLM (optional) | Ollama + qwen2.5:7b | Only when bulk classification needed |
| Dashboard | Streamlit | Local, free, fast to build |
| Backtesting | `vectorbt` (preferred) or `backtrader` | Both mature; pick one and stick with it |
| Scheduling | `cron` (Linux) or `launchd` (macOS) | Already used by skill-improvement loop |
| Configuration | YAML for non-secret config, `.env` for secrets | Standard pattern from upstream |

---

## Data Source Decisions

| Data type | Primary | Fallback | Cost |
|---|---|---|---|
| Stock prices (delayed) | `yfinance` | FMP | Free |
| Stock prices (real-time) | Alpaca free tier | FMP | Free |
| Options chains | Yahoo Finance | Tradier sandbox | Free |
| News | NewsAPI free + RSS | WebSearch via Claude | Free |
| SEC filings | SEC EDGAR direct | FMP | Free |
| Economic calendar | FMP | Trading Economics RSS | Free (with FMP key) |
| Reddit sentiment | PRAW (Reddit API) | Manual scraping | Free |
| Market breadth | TraderMonty's GitHub CSV | — | Free |
| Futures real-time | Tradovate (via Lucid) | — | Free with Lucid account |
| Futures historical | Firstrate Data | CME data shop | $25/symbol one-time |

### Deferred (don't add until proven need)

- Polygon.io ($30+/mo)
- Skylit ($99/mo)
- FINVIZ Elite ($40/mo)
- Unusual Whales ($50+/mo)

See `cost-discipline.md` for the decision framework.

---

## Repository Structure

The forked repo's structure is already established. Your additions follow these conventions:

```
trading-agent/                       # Your fork
├── PROJECT.md                       # Main router (always read first)
├── CLAUDE.md                        # Upstream-provided
├── README.md                        # Upstream-provided
├── project-docs/                    # NEW — your phase docs
│   ├── phase-1-audit.md
│   ├── phase-2-futures-skills.md
│   ├── phase-3-learning-loop.md
│   ├── phase-4-backtesting.md
│   ├── phase-5-live-execution.md
│   └── reference/
│       ├── lucid-rules.md
│       ├── cost-discipline.md
│       ├── tech-stack.md
│       ├── risk-register.md
│       └── existing-skills-map.md
│
├── decisions.md                     # NEW — log every meaningful decision
├── skills_audit.md                  # NEW — Phase 1 audit ratings
│
├── skills/                          # Existing + your new skills
│   ├── ... (existing 40+)
│   ├── lucid-rules-engine/          # NEW (Phase 2)
│   ├── futures-position-sizer/      # NEW (Phase 2)
│   ├── tradovate-integration/       # NEW (Phase 2)
│   ├── futures-pre-market-scan/     # NEW (Phase 2)
│   ├── futures-session-monitor/     # NEW (Phase 2)
│   ├── behavioral-pattern-detector/ # NEW (Phase 3)
│   └── futures-executor/            # NEW (Phase 5 only)
│
├── playbook/                        # NEW — your living rulebook
│   ├── playbook.md
│   └── changelog.md
│
├── state/                           # NEW — runtime state
│   ├── theses/                      # trader-memory-core data
│   ├── lucid_accounts/              # account state for rules engine
│   └── prompt_performance.json
│
├── data/
│   ├── raw/                         # Parquet, CSV
│   └── processed/
│
├── prompts/                         # Versioned system prompts
│   ├── current/
│   └── archive/
│
├── reports/                         # Generated reports (existing convention)
│
├── scripts/
│   ├── ... (existing)
│   ├── dashboard.py                 # NEW — Streamlit dashboard (Phase 3)
│   └── cost_report.py               # NEW — daily Anthropic spend report
│
├── tests/                           # Repo-wide test conventions
│
└── ~/trading-research/              # Generated by commands (not in repo)
    ├── reports/
    ├── archives/
    ├── intraday/
    ├── options/
    └── logs/
```

---

## Key Patterns to Follow

### From the upstream repo

- **SKILL.md format:** YAML frontmatter with `name` and `description`, body in imperative form
- **Reference docs:** Knowledge bases in `references/` loaded conditionally
- **Scripts:** I/O and execution in `scripts/`, never auto-loaded into context
- **Tests:** Live in `skills/<name>/tests/` or `skills/<name>/scripts/tests/`
- **Output:** Reports saved to `reports/` with `<skill>_<analysis>_<date>.md` naming

### Conventions you're adding

- **Phase docs:** Read on demand based on `PROJECT.md` "Active Phase"
- **Decisions log:** Every meaningful choice goes in `decisions.md` with date, context, alternatives considered
- **Cost ledger:** Every Claude API call logged with token count and estimated cost
- **State files:** SQLite for structured, JSON for simple key-value
- **No magic numbers:** All thresholds in `config.yaml`, never hardcoded

---

## Patterns to Avoid

- **Multi-agent frameworks (CrewAI, AutoGen, LangChain):** Overkill for current scope. The existing repo uses simple subprocess orchestration in `edge-pipeline-orchestrator`. Mirror that pattern.
- **Cloud infrastructure:** Everything runs locally. No AWS, no GCP, no managed databases.
- **Microservices:** Single-process Python is fine for this scale.
- **Custom MCP servers:** Use `tool_search` to find existing MCP integrations. Don't build custom ones unless absolutely necessary.

---

## Hardware Assumptions

- Single laptop or desktop
- macOS or Linux (Windows untested for the launchd jobs)
- 16GB RAM recommended (Ollama needs 8GB free for qwen2.5:7b)
- ~50GB disk space (most goes to historical futures data in Phase 4)
- Always-on internet during market hours (Phase 5+)

---

## Backup Strategy

- **Code:** Git remote (private GitHub fork)
- **Trade journal (`state/theses/`):** Daily backup to encrypted cloud storage
- **Lucid account credentials:** Password manager only, never in `.env`
- **Historical data:** Backup once after acquisition, treat as immutable
