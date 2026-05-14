#!/usr/bin/env python3
"""
pre_market.py — Automated pre-market routine (zero API cost)

Runs the three free daily skills, checks the FRED calendar,
flags position risks, and writes a structured posture report.

No Claude involvement — pure Python. Scheduled via launchd.

Usage:
    python3 scripts/pre_market.py              # normal run
    python3 scripts/pre_market.py --dry-run    # print output, no writes
    python3 scripts/pre_market.py --force      # run even on weekends

Output:
    reports/logs/market_context_YYYY-MM-DD.md  — full daily report
    reports/logs/posture_history.log           — one-line running history
"""

import argparse
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ── Paths ─────────────────────────────────────────────────────────────────────
REPO = Path(__file__).parent.parent
SKILLS = REPO / "skills"
SCRIPTS = REPO / "scripts"
STATE = REPO / "state" / "theses"
REPORTS = REPO / "reports" / "pre_market"
LOGS = REPO / "reports" / "logs"
TODAY = date.today().isoformat()
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H%M%S")

# ── Helpers ───────────────────────────────────────────────────────────────────


def run_skill_script(skill: str, script: str, args: list[str] | None = None) -> tuple[str, int]:
    """Run a skill's Python script and return (stdout, returncode)."""
    if args is None:
        args = []
    path = SKILLS / skill / "scripts" / script
    if not path.exists():
        return f"ERROR: {path} not found", 1
    result = subprocess.run(
        [sys.executable, str(path)] + args, capture_output=True, text=True, cwd=REPO
    )
    return result.stdout + result.stderr, result.returncode


def run_fred_calendar() -> str:
    """Run fred_calendar.py --days 3 and return HIGH impact events only."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "fred_calendar.py"), "--days", "3"],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    output = result.stdout
    # Filter to HIGH impact lines only
    lines = [
        ln
        for ln in output.splitlines()
        if "HIGH" in ln.upper()
        or "FOMC" in ln.upper()
        or "CPI" in ln.upper()
        or "NFP" in ln.upper()
        or "NONFARM" in ln.upper()
    ]
    return "\n".join(lines) if lines else "none"


def check_position_flags() -> tuple[list[str], list[str]]:
    """
    Read state/theses/ YAML files for open positions.
    Returns (urgent_flags, watch_flags).
    Urgent: expiry <= 7 days or stop breached.
    Watch:  expiry <= 14 days or earnings within 5 days on held ticker.
    """
    urgent, watch = [], []
    if not STATE.exists():
        return urgent, watch

    try:
        import yaml
    except ImportError:
        return ["WARNING: pyyaml not installed — position flags skipped"], []

    today = date.today()
    for f in STATE.glob("*.yaml"):
        try:
            data = yaml.safe_load(f.read_text()) or {}
        except Exception:
            continue

        status = data.get("status", "")
        if status not in ("ACTIVE", "ENTRY_READY"):
            continue

        ticker = data.get("ticker", f.stem).upper()
        asset_type = data.get("asset_type", "")
        stop = data.get("stop_loss") or data.get("stop", "")
        target = data.get("target", "")
        expiry_str = data.get("expiry") or data.get("expiration_date", "")

        ref = f"stop={stop} target={target}"

        # Options expiry check
        if asset_type == "options" and expiry_str:
            try:
                expiry = date.fromisoformat(str(expiry_str)[:10])
                days_to_expiry = (expiry - today).days
                if days_to_expiry <= 7:
                    urgent.append(
                        f"[URGENT] {ticker} | expires in {days_to_expiry}d ({expiry_str}) | {ref}"
                    )
                elif days_to_expiry <= 14:
                    watch.append(
                        f"[WATCH]  {ticker} | expires in {days_to_expiry}d ({expiry_str}) | {ref}"
                    )
            except (ValueError, TypeError):
                pass

    return urgent, watch


def parse_breadth_score(output: str) -> tuple[str, str]:
    """Extract composite score and zone from market-breadth-analyzer output."""
    score, zone = "N/A", "N/A"
    for line in output.splitlines():
        ln = line.lower()
        if "composite" in ln and ("score" in ln or "/100" in ln):
            parts = line.split()
            for i, p in enumerate(parts):
                if "/" in p and "100" in p:
                    score = p.split("/")[0].strip()
                elif p.replace(".", "").isdigit():
                    score = p.strip()
        if any(
            z in ln for z in ["bull", "bear", "neutral", "caution", "healthy", "weak", "strong"]
        ):
            for word in line.split():
                if word.lower() in [
                    "bullish",
                    "bearish",
                    "neutral",
                    "caution",
                    "healthy",
                    "weak",
                    "strong",
                    "critical",
                ]:
                    zone = word.capitalize()
    return score, zone


def parse_uptrend_score(output: str) -> tuple[str, str]:
    """Extract composite score and warnings from uptrend-analyzer output."""
    score, warnings = "N/A", ""
    for line in output.splitlines():
        ln = line.lower()
        # Match "Composite Score: 33.5/100"
        if "composite score:" in ln:
            try:
                part = line.split(":")[-1].strip()
                score = part.split("/")[0].strip()
            except (IndexError, ValueError):
                pass
        if any(w in ln for w in ["warning", "late cycle", "divergence", "high spread", "penalty"]):
            warnings = line.strip()
    return score, warnings if warnings else "none"


def parse_sector(output: str) -> tuple[str, str]:
    """Extract #1 ranked sector and cycle phase from sector-analyst output."""
    sector, phase = "N/A", "N/A"
    in_ranking = False
    for line in output.splitlines():
        ln = line.lower()
        # Detect sector ranking table and grab rank 1
        if "rank" in ln and "sector" in ln and "ratio" in ln:
            in_ranking = True
            continue
        if in_ranking and line.startswith("| 1 "):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                sector = parts[2]  # sector name column
            in_ranking = False
        # Cycle phase — look for "Late" / "Mid" / "Early" / "Recession"
        if "cycle phase" in ln or ("late" in ln and "confidence" in ln):
            for word in ["Late", "Mid", "Early", "Recession"]:
                if word.lower() in ln:
                    phase = word
                    break
    return sector[:40], phase[:40]


def determine_posture(breadth_score: str, macro_events: str, urgent_flags: list) -> tuple[str, str]:
    """Simple rule-based posture from playbook.md."""
    try:
        b = float(breadth_score)
    except (ValueError, TypeError):
        return "UNKNOWN", "N/A"

    has_macro_today = macro_events != "none" and TODAY in macro_events
    has_urgent = len(urgent_flags) > 0

    if has_urgent or b < 40:
        return "REDUCE_ONLY", "30%"
    elif b < 60 or has_macro_today:
        return "CAUTIOUS", "50%"
    else:
        return "NEW_ENTRY_ALLOWED", "70%"


# ── Main ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Run even on weekends")
    args = parser.parse_args()

    # Weekend check
    if not args.force and date.today().weekday() >= 5:
        print(f"{TIMESTAMP} — Skipping: weekend")
        return

    REPORTS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    report_path = LOGS / f"market_context_{TODAY}.md"
    history_path = LOGS / "posture_history.log"

    print(f"Running pre-market routine for {TODAY}...")

    # ── Step 1: Run the three free skills ─────────────────────────────────────
    print("  [1/4] Market breadth...")
    breadth_out, _ = run_skill_script(
        "market-breadth-analyzer", "market_breadth_analyzer.py", ["--output-dir", str(REPORTS)]
    )
    breadth_score, breadth_zone = parse_breadth_score(breadth_out)

    print("  [2/4] Uptrend analysis...")
    uptrend_out, _ = run_skill_script(
        "uptrend-analyzer", "uptrend_analyzer.py", ["--output-dir", str(REPORTS)]
    )
    uptrend_score, uptrend_warnings = parse_uptrend_score(uptrend_out)

    print("  [3/4] Sector rotation...")
    sector_out, _ = run_skill_script(
        "sector-analyst", "analyze_sector_rotation.py", ["--output-dir", str(REPORTS), "--save"]
    )
    leading_sector, cycle_phase = parse_sector(sector_out)

    # ── Step 2: FRED calendar ─────────────────────────────────────────────────
    print("  [4/4] Macro calendar + position flags...")
    macro_events = run_fred_calendar()

    # ── Step 3: Position flags ────────────────────────────────────────────────
    urgent_flags, watch_flags = check_position_flags()
    all_flags = urgent_flags + watch_flags
    flags_str = "\n".join(all_flags) if all_flags else "none"

    # ── Step 4: Posture ───────────────────────────────────────────────────────
    posture, ceiling = determine_posture(breadth_score, macro_events, urgent_flags)

    # ── Build report ──────────────────────────────────────────────────────────
    report = f"""# Pre-Market Report — {TODAY}
*Generated: {datetime.now().strftime("%H:%M:%S")}*

## Market Posture

```
Date:            {TODAY}
Breadth:         {breadth_score}/100 ({breadth_zone})
Uptrend:         {uptrend_score}/100
Uptrend warning: {uptrend_warnings}
Leading sector:  {leading_sector}
Cycle phase:     {cycle_phase}
Macro events:    {macro_events if macro_events != "none" else "none"}
Flags:           {flags_str if flags_str != "none" else "none"}
Posture:         {posture}
Ceiling:         {ceiling}
```

## Position Flags

{flags_str if flags_str != "none" else "No urgent or watch flags."}

## Breadth Detail

```
{breadth_out.strip()}
```

## Uptrend Detail

```
{uptrend_out.strip()}
```

## Sector Detail

```
{sector_out.strip()}
```
"""

    # ── One-line history entry ────────────────────────────────────────────────
    history_line = (
        f"{TODAY} | breadth={breadth_score} | uptrend={uptrend_score} | "
        f"sector={leading_sector[:20]} | {posture} | {ceiling} | "
        f"flags={'yes' if all_flags else 'none'}\n"
    )

    # ── Write or print ────────────────────────────────────────────────────────
    if args.dry_run:
        print("\n" + "=" * 60)
        print(report)
        print("=" * 60)
        print(f"\nHistory line: {history_line.strip()}")
        print("\n[DRY RUN — nothing written]")
        return

    report_path.write_text(report)
    with open(history_path, "a") as f:
        f.write(history_line)

    print(f"\n✓ Report saved: {report_path}")
    print(f"✓ History updated: {history_path}")
    print(f"\n  Breadth:  {breadth_score}/100 ({breadth_zone})")
    print(f"  Uptrend:  {uptrend_score}/100")
    print(f"  Sector:   {leading_sector}")
    print(f"  Posture:  {posture} ({ceiling})")
    if all_flags:
        print(f"\n  ⚠️  {len(urgent_flags)} urgent, {len(watch_flags)} watch flags")
        for f in urgent_flags:
            print(f"  {f}")


if __name__ == "__main__":
    main()
