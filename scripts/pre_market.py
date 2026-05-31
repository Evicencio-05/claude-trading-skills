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
    reports/logs/market_context_YYYY-MM-DD.json — structured summary
    reports/logs/market_context_YYYY-MM-DD.md   — executive summary
    reports/logs/posture_history.log            — one-line running history
"""

import argparse
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

from dotenv import load_dotenv
from market_context_extract import build_market_context_summary, write_market_context
from report_paths import default_output_dir

load_dotenv()

# ── Paths ─────────────────────────────────────────────────────────────────────
REPO = Path(__file__).parent.parent
SKILLS = REPO / "skills"
SCRIPTS = REPO / "scripts"
STATE = REPO / "state" / "theses"
BREADTH_DIR = default_output_dir(REPO, "market_breadth")
UPTREND_DIR = default_output_dir(REPO, "uptrend_analysis")
SECTOR_DIR = default_output_dir(REPO, "sector_rotation")
LOGS = REPO / "reports" / "logs"
TODAY = date.today()
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


def history_line(summary: dict) -> str:
    b = summary.get("breadth") or {}
    u = summary.get("uptrend") or {}
    s = summary.get("sector") or {}
    syn = summary.get("synthesis") or {}
    flags = summary.get("position_flags") or {}
    all_flags = (flags.get("urgent") or []) + (flags.get("watch") or [])
    sector = (s.get("leading_sector") or "N/A")[:20]
    return (
        f"{summary.get('as_of')} | breadth={b.get('score', 'N/A')} | "
        f"uptrend={u.get('score', 'N/A')} | sector={sector} | "
        f"{syn.get('posture', 'UNKNOWN')} | {syn.get('ceiling', 'N/A')} | "
        f"flags={'yes' if all_flags else 'none'}\n"
    )


# ── Main ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Run even on weekends")
    args = parser.parse_args()

    if not args.force and TODAY.weekday() >= 5:
        print(f"{TIMESTAMP} — Skipping: weekend")
        return

    BREADTH_DIR.mkdir(parents=True, exist_ok=True)
    UPTREND_DIR.mkdir(parents=True, exist_ok=True)
    SECTOR_DIR.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    print(f"Running pre-market routine for {TODAY.isoformat()}...")

    print("  [1/4] Market breadth...")
    breadth_out, _ = run_skill_script(
        "market-breadth-analyzer",
        "market_breadth_analyzer.py",
        ["--output-dir", str(BREADTH_DIR)],
    )

    print("  [2/4] Uptrend analysis...")
    uptrend_out, _ = run_skill_script(
        "uptrend-analyzer",
        "uptrend_analyzer.py",
        ["--output-dir", str(UPTREND_DIR)],
    )

    print("  [3/4] Sector rotation...")
    sector_out, _ = run_skill_script(
        "sector-analyst",
        "analyze_sector_rotation.py",
        ["--output-dir", str(SECTOR_DIR), "--save"],
    )

    print("  [4/4] Macro calendar + position flags...")
    macro_events = run_fred_calendar()
    urgent_flags, watch_flags = check_position_flags()

    summary = build_market_context_summary(
        REPO,
        as_of=TODAY,
        macro_events=macro_events,
        urgent_flags=urgent_flags,
        watch_flags=watch_flags,
        breadth_stdout=breadth_out,
        uptrend_stdout=uptrend_out,
        sector_stdout=sector_out,
    )

    line = history_line(summary)
    syn = summary.get("synthesis") or {}
    b = summary.get("breadth") or {}
    u = summary.get("uptrend") or {}
    s = summary.get("sector") or {}

    if args.dry_run:
        print("\n" + "=" * 60)
        print(json.dumps(summary, indent=2, default=str))
        print("=" * 60)
        print(f"\nHistory line: {line.strip()}")
        print("\n[DRY RUN — nothing written]")
        return

    json_path, md_path = write_market_context(REPO, summary, as_of=TODAY)
    history_path = LOGS / "posture_history.log"
    with open(history_path, "a") as f:
        f.write(line)

    print(f"\n✓ JSON saved: {json_path}")
    print(f"✓ Report saved: {md_path}")
    print(f"✓ History updated: {history_path}")
    print(f"\n  Breadth:  {b.get('score', 'N/A')}/100 ({b.get('zone', 'N/A')})")
    print(f"  Uptrend:  {u.get('score', 'N/A')}/100")
    print(f"  Sector:   {s.get('leading_sector', 'N/A')}")
    print(f"  Posture:  {syn.get('posture', 'UNKNOWN')} ({syn.get('ceiling', 'N/A')})")
    if urgent_flags or watch_flags:
        print(f"\n  ⚠️  {len(urgent_flags)} urgent, {len(watch_flags)} watch flags")
        for flag in urgent_flags:
            print(f"  {flag}")


if __name__ == "__main__":
    main()
