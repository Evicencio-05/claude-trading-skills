# Binding Decisions Log

> This file records decisions that affect the project's direction,
> cost, or architecture. Log here so future sessions don't
> relitigate settled questions.
> Format: Date | Decision | Rationale | Revisit condition

## API & Services

**[2026-05-09] FMP free tier confirmed insufficient for swing trading pipeline.**
vcp-screener and breakout-trade-planner blocked on free tier.
Batch quote endpoint restricted. economic-calendar-fetcher returns [] silently.
All ETFs except SPY blocked.
Decision: Upgrade to FMP Starter ($29/mo) before next live session.
Revisit: Never — free tier confirmed broken for core workflow.

**[2026-05-09] FRED API as economic-calendar-fetcher replacement.**
economic-calendar-fetcher permanently blocked on free FMP tier.
Decision: Use scripts/fred_calendar.py (built 2026-05-09) as permanent
replacement for macro event calendar.
Revisit: If FMP Starter restores this — test and consider reverting.

**[2026-05-09] Skylit ($99/mo) deferred.**
Decision: No Skylit until Phase 3+ AND strategy specifically needs GEX/dark pool
data AND can afford 3 months ($297) AND strategy could pay for it within 2 months
at current portfolio size.
Revisit: Phase 3 exit criteria review.

**[Deferred] Tradovate API/MCP deferred to Phase 2.**
Prop firm demo account API credentials not straightforwardly available.
No blocking need during Phase 1 audit.
Decision: Defer Tradovate API integration to Phase 2 week 6-7.
Revisit: Phase 2 start.

**[Deferred] GitHub MCP deferred.**
Correct URL and OAuth setup unclear. No Phase 1 need.
Decision: Defer to Phase 3 when skill-improvement PRs need review.
Revisit: Phase 3 start.

## Architecture

**[2026-05-11] Built Robinhood sync instead of using Trayd MCP.**
trayd-mcp passes credentials through third-party AWS servers.
For Portfolio B (IRA), keeping credentials local is preferred.
Decision: Build scripts/robinhood_sync.py using robin_stocks.
This pattern becomes the template for Tradovate sync in Phase 2.
Revisit: Never for Portfolio B. Could revisit Trayd for Portfolio A
if robin_stocks auth becomes a persistent friction point.

**[2026-05-09] launchd jobs disabled until Phase 3.**
Skill-improvement loop and skill-generation pipeline disabled.
Decision: Do not enable until Phase 3 exit criteria are met and enough session
data exists to evaluate improvement suggestions.
Revisit: phase-3-learning-loop.md section 3.6.

**[2026-05-09] Alpaca paper account identified as quick win.**
portfolio-manager skill requires Alpaca MCP. Free paper account activates it
without cost.
Decision: Set up Alpaca paper account before Phase 2.
Revisit: Phase 2 start.

**[2026-05-09] scenario-analyzer rewrite deferred.**
Japanese output is hardcoded (~30-min SKILL.md edit to fix).
Underlying methodology is sound. Not urgent.
Decision: Rewrite during a quiet session when current priorities clear.
Revisit: Phase 2 or whenever workflow needs macro scenario analysis.

## Portfolio

**[2026-05-09] Two-portfolio system established.**
Portfolio A: ~$500 Robinhood taxable — deployment capital.
Portfolio B: ~$10K Robinhood IRA — full buy/sell access, IRA options restrictions
apply (long calls/puts, covered calls, cash-secured puts only — no naked selling,
no undefined risk).
Learning-first mandate. Capital cannot easily be replenished.
Decision: All commands must flag IRA eligibility for Portfolio B.
Revisit: When account structure changes.

**[2026-05-28] Three Robinhood portfolios + hybrid sync paths.**
Portfolio A: ~$250 taxable (Robinhood individual) — `robinhood_sync.py` + ACCOUNT_MAP.
Portfolio B: ~$10K Roth IRA — **not** reachable via unofficial `robin_stocks` API;
log via thesis-manager or `/log-positions` after manual verification.
Portfolio C: ~$50 Robinhood Agentic — official Robinhood Agentic MCP in Claude Code;
equities first, options later. Account key in thesis-manager: `robinhood_agentic`.
Decision: Do not replace IRA manual logging until MCP account list confirms IRA access.
Agent documents MCP scope in decisions.md when user runs account discovery in Claude Code.
Revisit: After MCP lists all linked accounts.

## MCP & Brokerage

**[2026-05-28] Robinhood Agentic MCP vs local sync.**
Official Robinhood Agentic MCP URL: `https://agent.robinhood.com/mcp/trading`
Cursor: copy [.cursor/mcp.json.example](.cursor/mcp.json.example) → `.cursor/mcp.json` (gitignored).
Use MCP for portfolio read + log-positions Source B; use `robinhood_sync.py` for scheduled Portfolio A.
IRA (Portfolio B): MCP read expected per Robinhood; no MCP trades on IRA.
Revisit: When account discovery table below is filled.

**[2026-05-29] Robinhood hybrid: Cursor URL + CLI data plane.**
Cursor `.cursor/mcp.json` uses direct `url` only (avoids -32001 spawn timeout). Agent workflows use [`scripts/robinhood_mcp.py`](scripts/robinhood_mcp.py) (local mcp-remote + structuredContent proxy in subprocess). Account map: [`config/robinhood_accounts.yaml`](config/robinhood_accounts.yaml).
Revisit: In-chat MCP tool calls when Robinhood returns valid `structuredContent` upstream.

### Robinhood MCP account discovery (fill after Cursor OAuth)

Run prompts in [project-docs/reference/robinhood-mcp-integration.md](project-docs/reference/robinhood-mcp-integration.md) Phase 1.

| Robinhood account (name / number) | Maps to | Read MCP | Trade MCP | Notes |
|-----------------------------------|---------|----------|-----------|-------|
| ••••7016 (Agentic) | `robinhood_agentic` | Yes | Yes | individual, agentic_allowed |
| ••••9309 (default) | `robinhood_taxable` | Yes | No | individual cash |
| ••••3854 | `ira_robinhood` | Yes | No | ira_roth |

**Discovery completed:** [x] Date: 2026-05-29 — see [config/robinhood_accounts.yaml](config/robinhood_accounts.yaml)

## Scheduler

**[2026-05-14] Scheduler is systemd, not launchd.**
System runs Arch Linux. launchd is macOS-only.
Decision: All scheduled jobs use systemd user services.
.plist files kept in launchd/ for reference only.
Revisit: Never unless OS changes.
