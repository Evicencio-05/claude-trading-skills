"""Thesis Manager — fast UI for trader-memory-core thesis entry and review."""

from __future__ import annotations

import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
import utils  # noqa: E402

# ── constants ─────────────────────────────────────────────────────────────────

# Must match thesis.schema.json enum exactly — flow_play/lottery are not valid
THESIS_TYPES = [
    "growth_momentum",
    "pivot_breakout",
    "earnings_drift",
    "mean_reversion",
    "dividend_income",
]
CONFIDENCE_LABELS: dict[int, str] = {
    1: "1 — Lottery",
    2: "2 — Speculative",
    3: "3 — Moderate",
    4: "4 — Conviction",
    5: "5 — High Conviction",
}
EXIT_REASONS = ["stop_hit", "target_hit", "time_stop", "invalidated", "manual"]
ACCOUNTS = ["robinhood_taxable", "ira_robinhood", "robinhood_agentic", "lucid_eval"]


# ── shared helpers ─────────────────────────────────────────────────────────────


def _fmt_account(raw: str) -> str:
    """Convert a raw Robinhood account URL to a short display string."""
    if not raw:
        return "—"
    if raw.startswith("http"):
        parts = [p for p in raw.rstrip("/").split("/") if p]
        return f"rh:{parts[-1]}" if parts else raw
    return raw


def _ira_badge(account: str, strategy: str) -> str | None:
    """Return badge HTML if account is IRA, else None."""
    if "ira" not in account.lower():
        return None
    if strategy in ("long_call", "long_put", ""):
        return (
            '<span style="background:#2d6a4f;color:#fff;'
            'padding:2px 8px;border-radius:4px;font-size:0.85em">'
            "IRA Eligible</span>"
        )
    return (
        '<span style="background:#b5192b;color:#fff;'
        'padding:2px 8px;border-radius:4px;font-size:0.85em">'
        "NOT IRA Eligible — check before submitting</span>"
    )


def _days_to_expiry(expiry_str: str | None) -> int | None:
    if not expiry_str:
        return None
    try:
        return (date.fromisoformat(str(expiry_str)) - date.today()).days
    except (ValueError, TypeError):
        return None


def _parse_price(text: str) -> float | None:
    """Try to parse a price string as float. Returns None if not numeric."""
    try:
        return float(text.strip().lstrip("$"))
    except ValueError:
        return None


def _run_safe(fn, *args, **kwargs):
    """Call fn(*args, **kwargs). Returns (result, None) or (None, error_str)."""
    try:
        return fn(*args, **kwargs), None
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)


def _build_thesis_data(
    ticker: str,
    thesis_type: str,
    thesis_text: str,
    confidence: int,
    stop_text: str,
    target_text: str,
    avg_cost: float,
    strategy: str = "",
) -> dict:
    """Assemble a thesis_data dict that thesis_store.register() accepts."""
    stop_price = _parse_price(stop_text)
    target_price = _parse_price(target_text)
    kill = []
    if stop_text.strip() and stop_price is None:
        kill = [stop_text.strip()]
    return {
        "ticker": ticker.upper(),
        "thesis_type": thesis_type,
        "thesis_statement": thesis_text.strip(),
        "setup_type": strategy or "manual",
        "catalyst": "",
        "mechanism_tag": "manual",
        "evidence": [],
        "kill_criteria": kill,
        "confidence": None,
        "confidence_score": round(confidence * 0.2, 1),
        "entry": {
            "target_price": avg_cost if avg_cost else None,
            "conditions": [],
        },
        "exit": {
            "stop_loss": stop_price,
            "stop_loss_pct": None,
            "take_profit": target_price,
            "take_profit_rr": None,
            "time_stop_days": None,
        },
        "origin": {
            "skill": "manual",
            "output_file": "",
            "screening_grade": None,
            "screening_score": None,
            "raw_provenance": {},
        },
        "monitoring": {"review_interval_days": 7},
    }


# ── cached data loaders ────────────────────────────────────────────────────────


@st.cache_data(ttl=60)
def _theses(statuses_key: str) -> list[dict]:
    if not statuses_key:
        return utils.load_theses(None)
    return utils.load_theses(statuses_key.split(","))


@st.cache_data(ttl=60)
def _pending() -> list[dict]:
    return utils.load_pending_ingest()


# ── page 1: dashboard ─────────────────────────────────────────────────────────


def show_dashboard() -> None:
    st.header("Dashboard")

    open_theses = _theses("ACTIVE,ENTRY_READY")
    pending_all = _pending()
    pending_thesis = [p for p in pending_all if p.get("status") == "PENDING_THESIS"]
    # --- metric cards ---
    expiring_count = sum(
        1
        for t in open_theses
        if _days_to_expiry(((t.get("position") or {}).get("raw_source") or {}).get("expiry"))
        is not None
        and _days_to_expiry(((t.get("position") or {}).get("raw_source") or {}).get("expiry")) <= 7
    ) + sum(
        1
        for p in pending_thesis
        if _days_to_expiry(p.get("expiry")) is not None and _days_to_expiry(p.get("expiry")) <= 7
    )

    days_since = utils.days_since_last_entry()
    if days_since is None:
        days_label = "—"
        days_note = "No entries yet"
    else:
        indicator = " 🔴" if days_since > 7 else (" 🟡" if days_since > 3 else "")
        days_label = f"{days_since}{indicator}"
        days_note = ""

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Open Positions", len(open_theses))
    c2.metric(
        "Pending Thesis",
        len(pending_thesis),
        delta=f"⚠ {len(pending_thesis)}" if pending_thesis else None,
        delta_color="inverse" if pending_thesis else "off",
    )
    c3.metric(
        "Expiring ≤ 7 days",
        expiring_count,
        delta=f"⚠ {expiring_count}" if expiring_count else None,
        delta_color="inverse" if expiring_count else "off",
    )
    with c4:
        st.metric("Days Since Last Entry", days_label)
        if days_note:
            st.caption(days_note)

    st.divider()

    # --- position table ---
    if not open_theses and not pending_thesis:
        st.info("No positions logged yet. Use **Add Thesis** to get started.")
        _show_refresh_button()
        return

    rows = []
    for t in open_theses:
        pos = t.get("position") or {}
        raw = pos.get("raw_source") or {}
        expiry = raw.get("expiry")
        dte = _days_to_expiry(expiry)
        cs = t.get("confidence_score") or 0
        rows.append(
            {
                "_id": t.get("thesis_id", ""),
                "Ticker": t.get("ticker", ""),
                "Type": t.get("thesis_type", ""),
                "Account": _fmt_account(pos.get("account_type") or ""),
                "Expiry": expiry or "—",
                "Confidence": int(cs * 5) if cs else "—",
                "Days Left": dte if dte is not None else "—",
                "Status": t.get("status", ""),
            }
        )
    for p in pending_thesis:
        expiry = p.get("expiry")
        dte = _days_to_expiry(expiry)
        rows.append(
            {
                "_id": p.get("key", ""),
                "Ticker": p.get("ticker", ""),
                "Type": p.get("asset_type", ""),
                "Account": _fmt_account(p.get("account", "")),
                "Expiry": expiry or "—",
                "Confidence": "—",
                "Days Left": dte if dte is not None else "—",
                "Status": "PENDING_THESIS",
            }
        )

    df_display = pd.DataFrame(rows)

    def _style_row(row):
        status = row.get("Status", "")
        dte = row.get("Days Left")
        bg = ""
        if status == "PENDING_THESIS":
            bg = "background-color: #3d3500"
        elif isinstance(dte, int) and dte <= 7:
            bg = "background-color: #3d0000"
        elif isinstance(dte, int) and dte <= 14:
            bg = "background-color: #3d2000"
        return [bg] * len(row)

    display_cols = ["Ticker", "Type", "Account", "Expiry", "Confidence", "Days Left", "Status"]
    styled = df_display[display_cols].style.apply(_style_row, axis=1)

    event = st.dataframe(
        styled,
        use_container_width=True,
        on_select="rerun",
        selection_mode="single-row",
        key="dash_table",
    )

    sel = (event.selection.rows if hasattr(event, "selection") else []) or []
    if sel:
        idx = sel[0]
        row = rows[idx]
        row_id = row["_id"]
        thesis = next((t for t in open_theses if t.get("thesis_id") == row_id), None)
        ppos = next((p for p in pending_thesis if p.get("key") == row_id), None)

        with st.container(border=True):
            if thesis:
                st.subheader(f"{row['Ticker']} — {row['Status']}")
                lc, rc = st.columns(2)
                with lc:
                    st.write("**Thesis:**", thesis.get("thesis_statement") or "—")
                    exit_d = thesis.get("exit") or {}
                    st.write("**Stop:**", exit_d.get("stop_loss") or "—")
                    st.write("**Target:**", exit_d.get("take_profit") or "—")
                    st.write(
                        "**Kill criteria:**", "; ".join(thesis.get("kill_criteria") or []) or "—"
                    )
                with rc:
                    mon = thesis.get("monitoring") or {}
                    st.write("**Last reviewed:**", mon.get("last_review_date") or "never")
                    cs = thesis.get("confidence_score") or 0
                    st.write("**Confidence:**", f"{int(cs * 5)}/5" if cs else "—")

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("Mark for Review", key=f"rev_{row_id}"):
                        _, err = _run_safe(utils.mark_reviewed, row_id)
                        if err:
                            st.error(f"Failed: {err}")
                        else:
                            st.success("Marked reviewed.")
                            st.cache_data.clear()
                            st.rerun()
                with b2:
                    if st.button("Close Position", key=f"close_{row_id}"):
                        st.session_state[f"closing_{row_id}"] = True

                if st.session_state.get(f"closing_{row_id}"):
                    with st.form(key=f"close_form_{row_id}"):
                        ep = st.number_input("Exit price", min_value=0.0, format="%.4f")
                        ed = st.date_input("Exit date", value=date.today())
                        reason = st.selectbox("Exit reason", EXIT_REASONS)
                        if st.form_submit_button("Confirm Close"):
                            _, err = _run_safe(
                                utils.close_thesis, row_id, reason, ep, ed.isoformat()
                            )
                            if err:
                                st.error(
                                    f"Close failed (command: close_thesis {row_id!r} {reason!r} {ep} {ed.isoformat()!r}):\n{err}"
                                )
                            else:
                                st.success(f"Closed {row['Ticker']}.")
                                st.session_state.pop(f"closing_{row_id}", None)
                                st.cache_data.clear()
                                st.rerun()
            elif ppos:
                st.subheader(f"{row['Ticker']} — PENDING_THESIS")
                st.write("Go to **Add Thesis** to fill in the thesis for this position.")

    st.divider()
    _show_refresh_button()


def _show_refresh_button() -> None:
    if st.button("Refresh Positions"):
        sync_script = utils.get_repo_root() / "scripts" / "robinhood_sync.py"
        try:
            result = subprocess.run(
                [sys.executable, str(sync_script)],
                capture_output=True,
                text=True,
                timeout=90,
            )
            if result.returncode == 0:
                st.success(f"Synced via robinhood_sync.py\n{result.stdout[:300]}")
            else:
                st.error(f"Sync failed (python3 scripts/robinhood_sync.py):\n{result.stderr[:500]}")
        except FileNotFoundError:
            st.warning("scripts/robinhood_sync.py not found.")
        except subprocess.TimeoutExpired:
            st.error("Sync timed out after 90s.")
        st.caption(f"Last attempted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.cache_data.clear()
        st.rerun()


# ── page 2: add thesis ─────────────────────────────────────────────────────────


def _pending_position_form(pos: dict, key_prefix: str) -> None:
    """Render the fill-in form for one pending position."""
    ticker = pos.get("ticker", "?")
    account = pos.get("account", "")
    asset_type = pos.get("asset_type", "")
    strategy = pos.get("strategy", "")
    expiry = pos.get("expiry", "")
    strike = pos.get("strike", "")
    contracts = pos.get("contracts", "")
    avg_cost = pos.get("avg_cost", 0.0)

    hdr_cols = st.columns([4, 1])
    with hdr_cols[0]:
        st.markdown(f"### {ticker}")
        badge = _ira_badge(account, strategy)
        if badge:
            st.markdown(badge, unsafe_allow_html=True)
    with hdr_cols[1]:
        if st.button("Skip", key=f"skip_{key_prefix}"):
            st.session_state[f"collapsed_{key_prefix}"] = True
            st.rerun()

    meta = st.columns(4)
    meta[0].caption(f"Account: {_fmt_account(account)}")
    meta[0].caption(f"Type: {asset_type}")
    if strike:
        meta[1].caption(f"Strike: {strike}")
    if expiry:
        meta[1].caption(f"Expiry: {expiry}")
    if contracts:
        meta[2].caption(f"Contracts: {contracts}")
    meta[2].caption(f"Avg cost: {avg_cost}")
    dte = _days_to_expiry(expiry)
    if dte is not None:
        color = "red" if dte <= 7 else ("orange" if dte <= 14 else "green")
        meta[3].markdown(
            f"<span style='color:{color};font-weight:bold'>{dte}d left</span>",
            unsafe_allow_html=True,
        )

    thesis_type = st.selectbox(
        "Thesis type",
        THESIS_TYPES,
        index=0,
        key=f"tt_{key_prefix}",
    )
    thesis_text = st.text_area(
        "Thesis *",
        placeholder="Why did you enter? What's the catalyst? What would make this wrong?",
        height=100,
        key=f"th_{key_prefix}",
    )
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        confidence = st.select_slider(
            "Confidence",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: CONFIDENCE_LABELS[x],
            key=f"conf_{key_prefix}",
        )
    with fc2:
        stop_val = st.text_input(
            "Stop",
            placeholder="Price or condition that invalidates the thesis",
            key=f"stop_{key_prefix}",
        )
    with fc3:
        target_val = st.text_input(
            "Target",
            placeholder="Exit condition or price target",
            key=f"tgt_{key_prefix}",
        )

    if st.button("Submit", key=f"sub_{key_prefix}", type="primary"):
        if not thesis_text.strip():
            st.warning("Thesis text is required.")
            return
        td = _build_thesis_data(
            ticker=ticker,
            thesis_type=thesis_type,
            thesis_text=thesis_text,
            confidence=confidence,
            stop_text=stop_val,
            target_text=target_val,
            avg_cost=float(avg_cost) if avg_cost else 0.0,
            strategy=strategy,
        )
        thesis_id, err = _run_safe(utils.register_thesis, td)
        if err:
            st.error(f"Register failed (register_thesis for {ticker}):\n{err}")
            return
        all_positions = utils.load_pending_ingest()
        for p2 in all_positions:
            if p2.get("key") == pos.get("key"):
                p2["status"] = "INGESTED"
                p2["thesis_id"] = thesis_id
                break
        utils.save_pending_ingest(all_positions)
        st.success(f"Registered {ticker} → {thesis_id}")
        st.session_state[f"collapsed_{key_prefix}"] = True
        st.cache_data.clear()
        st.rerun()


def show_add_thesis() -> None:
    st.header("Add Thesis")

    # ── Section A: pending positions ──────────────────────────────────────────
    st.subheader("A — Pending Positions")
    pending = utils.load_pending_ingest()
    pending_thesis = sorted(
        [p for p in pending if p.get("status") == "PENDING_THESIS"],
        key=lambda p: p.get("expiry") or "9999",
    )

    if not pending_thesis:
        st.info("No pending sync data. Run **Robinhood sync** from the Dashboard.")
    else:
        for i, pos in enumerate(pending_thesis):
            ticker = pos.get("ticker", "?")
            key_prefix = f"pend_{i}_{ticker}"
            if st.session_state.get(f"collapsed_{key_prefix}"):
                continue
            with st.container(border=True):
                _pending_position_form(pos, key_prefix)

    st.divider()

    # ── Section B: manual entry ───────────────────────────────────────────────
    with st.expander("Add position manually", expanded=False):
        mc1, mc2 = st.columns(2)
        with mc1:
            m_ticker = (
                st.text_input("Ticker *", placeholder="AAPL", key="man_ticker").strip().upper()
            )
            m_asset = st.selectbox("Asset type", ["stock", "options", "futures"], key="man_asset")
            m_dir = st.selectbox("Direction", ["long", "short"], key="man_dir")
            m_account = st.selectbox("Account", ACCOUNTS, key="man_account")
        with mc2:
            st.number_input("Size (shares/contracts)", min_value=0.0, key="man_size")
            m_cost = st.number_input("Avg cost", min_value=0.0, format="%.4f", key="man_cost")
            st.date_input("Entry date", value=date.today(), key="man_entry_date")

        m_strategy = ""
        if m_asset == "options":
            oc1, oc2, oc3 = st.columns(3)
            with oc1:
                st.number_input("Strike", min_value=0.0, format="%.2f", key="man_strike")
            with oc2:
                st.date_input("Expiry", key="man_expiry")
            with oc3:
                m_opt_type = st.selectbox("Option type", ["call", "put"], key="man_opt_type")
            m_strategy = f"{m_dir}_{m_opt_type}"
            st.text_input("Strategy (auto)", value=m_strategy, disabled=True, key="man_strat_disp")
            badge = _ira_badge(m_account, m_strategy)
            if badge:
                st.markdown(badge, unsafe_allow_html=True)
        elif "ira" in m_account.lower():
            st.markdown(
                _ira_badge(m_account, "long_call") or "",
                unsafe_allow_html=True,
            )

        m_thesis_type = st.selectbox("Thesis type *", THESIS_TYPES, key="man_tt")
        m_thesis = st.text_area(
            "Thesis *",
            placeholder="Why did you enter? What's the catalyst? What would make this wrong?",
            height=100,
            key="man_thesis",
        )
        bf1, bf2, bf3 = st.columns(3)
        with bf1:
            m_conf = st.select_slider(
                "Confidence",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: CONFIDENCE_LABELS[x],
                key="man_conf",
            )
        with bf2:
            m_stop = st.text_input(
                "Stop",
                placeholder="Price or condition that invalidates the thesis",
                key="man_stop",
            )
        with bf3:
            m_target = st.text_input(
                "Target",
                placeholder="Exit condition or price target",
                key="man_target",
            )

        if st.button("Submit", key="man_submit", type="primary"):
            if not m_ticker:
                st.warning("Ticker is required.")
            elif not m_thesis.strip():
                st.warning("Thesis text is required.")
            else:
                td = _build_thesis_data(
                    ticker=m_ticker,
                    thesis_type=m_thesis_type,
                    thesis_text=m_thesis,
                    confidence=m_conf,
                    stop_text=m_stop,
                    target_text=m_target,
                    avg_cost=float(m_cost),
                    strategy=m_strategy,
                )
                thesis_id, err = _run_safe(utils.register_thesis, td)
                if err:
                    st.error(f"Register failed (register_thesis for {m_ticker}):\n{err}")
                else:
                    st.success(f"Registered {m_ticker} → {thesis_id}")
                    st.cache_data.clear()


# ── page 3: review ─────────────────────────────────────────────────────────────


def show_review() -> None:
    st.header("Review")

    # ── Section A: urgent flags ───────────────────────────────────────────────
    st.subheader("A — Urgent Flags")

    open_theses = utils.load_theses(["ACTIVE", "ENTRY_READY"])
    flagged: list[tuple[dict, list[str]]] = []
    for t in open_theses:
        reasons: list[str] = []
        raw = (t.get("position") or {}).get("raw_source") or {}
        dte = _days_to_expiry(raw.get("expiry"))
        if dte is not None and dte <= 7:
            reasons.append(f"Options expiring in {dte} days")
        mon = t.get("monitoring") or {}
        last_rev = mon.get("last_review_date")
        if last_rev:
            try:
                stale = (date.today() - date.fromisoformat(str(last_rev))).days
                if stale > 14:
                    reasons.append(f"Not reviewed in {stale} days")
            except (ValueError, TypeError):
                pass
        else:
            reasons.append("Never reviewed")
        cs = t.get("confidence_score") or 0
        if 0 < cs <= 0.4:
            reasons.append(f"Low confidence ({int(cs * 5)}/5)")
        if reasons:
            flagged.append((t, reasons))

    if not flagged:
        st.success("No urgent flags. All positions look current.")
    else:
        for t, reasons in flagged:
            tid = t.get("thesis_id", "")
            ticker = t.get("ticker", "")
            summary = (t.get("thesis_statement") or "—")[:100]
            exit_d = t.get("exit") or {}

            with st.container(border=True):
                st.markdown(f"**{ticker}** — {', '.join(reasons)}")
                st.caption(f"Thesis: {summary}")
                st.caption(
                    f"Stop: {exit_d.get('stop_loss') or '—'} | "
                    f"Target: {exit_d.get('take_profit') or '—'}"
                )

                b1, b2, b3 = st.columns(3)
                with b1:
                    if st.button("Still Valid", key=f"valid_{tid}"):
                        _, err = _run_safe(utils.mark_reviewed, tid)
                        if err:
                            st.error(f"Failed: {err}")
                        else:
                            st.success("Marked reviewed.")
                            st.cache_data.clear()
                            st.rerun()
                with b2:
                    if st.button("Close Position", key=f"urg_close_{tid}"):
                        st.session_state[f"urg_closing_{tid}"] = True
                with b3:
                    if st.button("Roll", key=f"roll_{tid}"):
                        st.session_state[f"rolling_{tid}"] = True

            if st.session_state.get(f"urg_closing_{tid}"):
                with st.form(key=f"urg_close_form_{tid}"):
                    ep = st.number_input(
                        "Exit price", min_value=0.0, format="%.4f", key=f"uc_ep_{tid}"
                    )
                    ed = st.date_input("Exit date", value=date.today(), key=f"uc_ed_{tid}")
                    reason = st.selectbox("Exit reason", EXIT_REASONS, key=f"uc_r_{tid}")
                    if st.form_submit_button("Confirm Close"):
                        _, err = _run_safe(utils.close_thesis, tid, reason, ep, ed.isoformat())
                        if err:
                            st.error(
                                f"Close failed (close_thesis {tid!r} {reason!r} {ep} {ed.isoformat()!r}):\n{err}"
                            )
                        else:
                            st.success(f"Closed {ticker}.")
                            st.session_state.pop(f"urg_closing_{tid}", None)
                            st.cache_data.clear()
                            st.rerun()

            if st.session_state.get(f"rolling_{tid}"):
                with st.form(key=f"roll_form_{tid}"):
                    r_strike = st.number_input(
                        "New strike", min_value=0.0, format="%.2f", key=f"rr_s_{tid}"
                    )
                    r_expiry = st.date_input("New expiry", key=f"rr_e_{tid}")
                    r_cost = st.number_input(
                        "New avg cost", min_value=0.0, format="%.4f", key=f"rr_c_{tid}"
                    )
                    r_note = st.text_input("Roll rationale", key=f"rr_n_{tid}")
                    if st.form_submit_button("Confirm Roll"):
                        _, close_err = _run_safe(
                            utils.close_thesis, tid, "manual", 0.0, date.today().isoformat()
                        )
                        if close_err:
                            st.error(f"Close original failed:\n{close_err}")
                        else:
                            cs = t.get("confidence_score") or 0.6
                            roll_text = (
                                f"Roll from {tid} → {r_strike} strike exp {r_expiry}. {r_note}"
                            ).strip()
                            new_td = _build_thesis_data(
                                ticker=ticker,
                                thesis_type=t.get("thesis_type") or "growth_momentum",
                                thesis_text=roll_text,
                                confidence=max(1, round(cs * 5)),
                                stop_text="",
                                target_text="",
                                avg_cost=float(r_cost),
                            )
                            new_id, reg_err = _run_safe(utils.register_thesis, new_td)
                            if reg_err:
                                st.error(f"New thesis failed:\n{reg_err}")
                            else:
                                st.success(f"Rolled {ticker} → {new_id}")
                                st.session_state.pop(f"rolling_{tid}", None)
                                st.cache_data.clear()
                                st.rerun()

    st.divider()

    # ── Section B: needs post-trade review ────────────────────────────────────
    st.subheader("B — Needs Post-Trade Review")

    closed_theses = utils.load_theses(["CLOSED"])
    thirty_ago = (date.today() - timedelta(days=30)).isoformat()
    needs_review = [
        t
        for t in closed_theses
        if ((t.get("exit") or {}).get("actual_date") or "") >= thirty_ago
        and not ((t.get("outcome") or {}).get("lessons_learned"))
    ]

    if not needs_review:
        st.success("All recently closed positions have been reviewed.")
    else:
        for t in needs_review:
            tid = t.get("thesis_id", "")
            ticker = t.get("ticker", "")
            entry_p = (t.get("entry") or {}).get("actual_price")
            exit_p = (t.get("exit") or {}).get("actual_price")
            pnl = "—"
            if isinstance(entry_p, (int, float)) and isinstance(exit_p, (int, float)) and entry_p:
                pnl = f"{(exit_p - entry_p) / entry_p * 100:+.1f}%"
            cs = t.get("confidence_score") or 0
            pos = t.get("position") or {}

            with st.container(border=True):
                rc1, rc2, rc3, rc4, rc5 = st.columns([3, 1, 1, 1, 1])
                rc1.write(f"**{ticker}**")
                rc2.caption(f"Entry: {entry_p or '—'}")
                rc3.caption(f"Exit: {exit_p or '—'}")
                rc4.caption(f"P&L: {pnl}")
                rc5.caption(f"Conf: {int(cs * 5)}/5" if cs else "—")
                st.caption(f"Account: {_fmt_account(pos.get('account_type') or '')}")

                with st.form(key=f"review_form_{tid}"):
                    what = st.text_area(
                        "What happened? (2-3 sentences)", height=80, key=f"rv_w_{tid}"
                    )
                    lesson = st.text_input("Key lesson? (one sentence)", key=f"rv_l_{tid}")
                    if st.form_submit_button("Submit Review"):
                        existing_outcome = dict(t.get("outcome") or {})
                        existing_outcome["lessons_learned"] = lesson.strip()
                        existing_outcome["what_happened"] = what.strip()
                        _, err = _run_safe(utils.update_thesis, tid, {"outcome": existing_outcome})
                        if err:
                            st.error(f"Update failed (update_thesis {tid!r} outcome):\n{err}")
                        else:
                            st.success("Review saved.")
                            st.cache_data.clear()
                            st.rerun()

    st.divider()

    # ── Section C: closed this week ───────────────────────────────────────────
    st.subheader("C — Closed This Week")

    seven_ago = (date.today() - timedelta(days=7)).isoformat()
    week_closed = [
        t for t in closed_theses if ((t.get("exit") or {}).get("actual_date") or "") >= seven_ago
    ]

    if not week_closed:
        st.info("No positions closed in the last 7 days.")
    else:
        rows = []
        for t in week_closed:
            exit_d = t.get("exit") or {}
            entry_d = t.get("entry") or {}
            pos = t.get("position") or {}
            ep = entry_d.get("actual_price")
            xp = exit_d.get("actual_price")
            pnl = "—"
            if isinstance(ep, (int, float)) and isinstance(xp, (int, float)) and ep:
                pnl = f"{(xp - ep) / ep * 100:+.1f}%"
            cs = t.get("confidence_score") or 0
            rows.append(
                {
                    "Ticker": t.get("ticker", ""),
                    "Account": _fmt_account(pos.get("account_type") or ""),
                    "Entry": ep or "—",
                    "Exit": xp or "—",
                    "P&L": pnl,
                    "Confidence": f"{int(cs * 5)}/5" if cs else "—",
                    "Outcome": exit_d.get("exit_reason") or "—",
                }
            )
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ── entry point ────────────────────────────────────────────────────────────────


def main() -> None:
    st.set_page_config(page_title="Thesis Manager", page_icon="📊", layout="wide")
    page = st.sidebar.radio(
        "Page",
        ["Dashboard", "Add Thesis", "Review"],
        label_visibility="collapsed",
    )
    st.sidebar.divider()
    st.sidebar.caption("trader-memory-core UI")

    if page == "Dashboard":
        show_dashboard()
    elif page == "Add Thesis":
        show_add_thesis()
    else:
        show_review()


if __name__ == "__main__":
    main()
