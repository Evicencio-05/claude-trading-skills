"""Thesis Manager — fast UI for trader-memory-core thesis entry and review."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
import market_utils  # noqa: E402
import research_utils  # noqa: E402
import utils  # noqa: E402

PAGES = ["Dashboard", "Market", "Research", "Reports", "Theses", "Review"]

# ── constants ─────────────────────────────────────────────────────────────────

# Must match thesis.schema.json enum exactly — flow_play/lottery are not valid
THESIS_TYPES = utils.THESIS_TYPES
CONFIDENCE_LABELS: dict[int, str] = {
    1: "1 — Lottery",
    2: "2 — Speculative",
    3: "3 — Moderate",
    4: "4 — Conviction",
    5: "5 — High Conviction",
}
EXIT_REASONS = utils.EXIT_REASONS
EXIT_REASON_LABELS: dict[str, str] = {
    "stop_hit": "Stop hit",
    "target_hit": "Target hit",
    "time_stop": "Expired / time stop",
    "invalidated": "Thesis invalidated",
    "manual": "Manual exit",
}


# ── shared helpers ─────────────────────────────────────────────────────────────


def _fmt_account(raw: str) -> str:
    return utils.fmt_account(raw)


def _ira_badge(account: str, strategy: str) -> str | None:
    return utils.ira_badge_html(account, strategy)


def _days_to_expiry(expiry_str: str | None) -> int | None:
    return utils.days_to_expiry(expiry_str)


def _parse_price(text: str) -> float | None:
    return utils.parse_price(text)


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
    return utils.build_thesis_data(
        ticker=ticker,
        thesis_type=thesis_type,
        thesis_text=thesis_text,
        confidence=confidence,
        stop_text=stop_text,
        target_text=target_text,
        avg_cost=avg_cost,
        strategy=strategy,
    )


# ── cached data loaders ────────────────────────────────────────────────────────


@st.cache_data(ttl=60)
def _theses(statuses_key: str) -> list[dict]:
    if not statuses_key:
        return utils.load_theses(None)
    return utils.load_theses(statuses_key.split(","))


@st.cache_data(ttl=60)
def _pending() -> list[dict]:
    return utils.load_pending_ingest()


@st.cache_data(ttl=60)
def _research_rows() -> list[dict]:
    return research_utils.get_research_dashboard_rows()


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

    research_rows = _research_rows()
    stale_n = sum(1 for r in research_rows if r["ui_status"] in ("stale", "missing"))
    rc1, rc2 = st.columns([3, 1])
    with rc1:
        st.caption(f"Research stale: **{stale_n}** — open Research page for update prompts")
    with rc2:
        if st.button("Go to Research", key="dash_go_research"):
            st.session_state["nav_page"] = "Research"
            st.rerun()

    market_ctx = market_utils.load_market_context()
    mc1, mc2 = st.columns([3, 1])
    with mc1:
        if market_ctx:
            syn = market_ctx.get("synthesis") or {}
            st.caption(
                f"Market: **{syn.get('posture', 'UNKNOWN')}** "
                f"({syn.get('ceiling', 'N/A')}) — {market_ctx.get('as_of', '')}"
            )
        else:
            st.caption("Market: no pre-market report — run `scripts/pre_market.py`")
    with mc2:
        if st.button("Go to Market", key="dash_go_market"):
            st.session_state["nav_page"] = "Market"
            st.rerun()

    st.divider()

    dupes = utils.pending_duplicate_tickers(open_theses, pending_all)
    if dupes:
        st.warning(
            f"Duplicate tickers already logged as open theses: {', '.join(sorted(dupes))}. "
            "Close or skip pending rows to avoid double-counting."
        )

    # --- position table ---
    if not open_theses and not pending_thesis:
        st.info("No positions logged yet. Sync from Dashboard or add a thesis on **Theses**.")
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
                "Confidence": str(int(cs * 5)) if cs else "—",
                "Days Left": str(dte) if dte is not None else "—",
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
                "Days Left": str(dte) if dte is not None else "—",
                "Status": "PENDING_THESIS",
            }
        )

    df_display = pd.DataFrame(rows)

    def _style_row(row):
        status = row.get("Status", "")
        try:
            dte = int(row.get("Days Left", ""))
        except (ValueError, TypeError):
            dte = None
        bg = ""
        if status == "PENDING_THESIS":
            bg = "background-color: #3d3500"
        elif dte is not None and dte <= 7:
            bg = "background-color: #3d0000"
        elif dte is not None and dte <= 14:
            bg = "background-color: #3d2000"
        return [bg] * len(row)

    display_cols = ["Ticker", "Type", "Account", "Expiry", "Confidence", "Days Left", "Status"]
    display_df = utils.arrow_safe_df(df_display, display_cols)
    styled = display_df.style.apply(_style_row, axis=1)

    event = st.dataframe(
        styled,
        width="stretch",
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

                if st.button("Manage in Theses", key=f"manage_{row_id}"):
                    st.session_state["nav_page"] = "Theses"
                    st.rerun()
            elif ppos:
                st.subheader(f"{row['Ticker']} — PENDING_THESIS")
                st.caption(
                    "Robinhood sync found this position — add your thesis on the Theses page."
                )
                if st.button("Go to Theses", key=f"pending_{row_id}"):
                    st.session_state["nav_page"] = "Theses"
                    st.rerun()

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


# ── pending sync ingest (Theses page) ─────────────────────────────────────────


def _show_pending_positions_section() -> None:
    """Robinhood sync rows awaiting thesis text — promoted to ACTIVE on submit."""
    pending = utils.load_pending_ingest()
    pending_thesis = sorted(
        [p for p in pending if p.get("status") == "PENDING_THESIS"],
        key=lambda p: p.get("expiry") or "9999",
    )

    if not pending_thesis:
        return

    st.subheader("Pending from sync")
    st.caption("Positions from Robinhood sync that need a thesis before they appear as ACTIVE.")

    open_theses = utils.load_theses(["ACTIVE", "ENTRY_READY"])
    dupes = utils.pending_duplicate_tickers(open_theses, pending)
    if dupes:
        st.warning(f"These pending tickers already have open theses: {', '.join(sorted(dupes))}")

    for i, pos in enumerate(pending_thesis):
        ticker = pos.get("ticker", "?")
        key_prefix = f"pend_{i}_{ticker}"
        if st.session_state.get(f"collapsed_{key_prefix}"):
            continue
        with st.container(border=True):
            _pending_position_form(pos, key_prefix)


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
        dismiss_exclude = st.checkbox(
            "Add to exclude list",
            value=True,
            key=f"dismiss_excl_{key_prefix}",
        )
        if st.button("Dismiss", key=f"dismiss_{key_prefix}"):
            pos_key = pos.get("key", "")
            all_positions = utils.load_pending_ingest()
            utils.save_pending_ingest(utils.mark_pending_skipped(all_positions, pos_key))
            if pos_key:
                utils.block_sync_key(pos_key)
            if dismiss_exclude and ticker:
                try:
                    research_utils.add_exclude_ticker(ticker, "dismissed pending position")
                except (ValueError, OSError) as exc:
                    st.warning(f"Exclude list not updated: {exc}")
            st.success(f"Dismissed {ticker} — will not re-sync.")
            st.session_state[f"collapsed_{key_prefix}"] = True
            st.cache_data.clear()
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

    if st.button("Submit", key=f"sub_{key_prefix}"):
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
        val_errors = utils.validate_thesis_submit(
            td, account=account, strategy=strategy, confidence=confidence
        )
        if val_errors:
            st.error("\n".join(val_errors))
            return
        thesis_id, err = _run_safe(utils.register_pending_position, td, pos)
        if err:
            st.error(f"Register failed (register_pending_position for {ticker}):\n{err}")
            return
        all_positions = utils.load_pending_ingest()
        utils.save_pending_ingest(
            utils.mark_pending_ingested(all_positions, pos.get("key", ""), thesis_id)
        )
        st.success(f"Registered {ticker} → {thesis_id} (ACTIVE)")
        st.session_state[f"collapsed_{key_prefix}"] = True
        st.cache_data.clear()
        st.rerun()


# ── page: theses (CRUD) ───────────────────────────────────────────────────────


def _thesis_summary_row(t: dict) -> dict:
    pos = t.get("position") or {}
    cs = t.get("confidence_score") or 0
    created = str(t.get("created_at") or "")[:10] or "—"
    return {
        "_id": t.get("thesis_id", ""),
        "Ticker": t.get("ticker", ""),
        "Type": t.get("thesis_type", ""),
        "Status": t.get("status", ""),
        "Account": _fmt_account(pos.get("account_type") or ""),
        "Confidence": str(int(cs * 5)) if cs else "—",
        "Created": created,
    }


def _render_thesis_edit_form(thesis: dict) -> None:
    """Editable fields + lifecycle actions for one thesis."""
    tid = thesis.get("thesis_id", "")
    ticker = thesis.get("ticker", "")
    status = thesis.get("status", "")
    cs = thesis.get("confidence_score") or 0
    mon = thesis.get("monitoring") or {}
    outcome = thesis.get("outcome") or {}
    exit_d = thesis.get("exit") or {}
    entry_d = thesis.get("entry") or {}
    pos = thesis.get("position") or {}

    st.caption(f"ID: `{tid}` · Status: **{status}** · Ticker/type are fixed after creation")

    meta1, meta2, meta3 = st.columns(3)
    meta1.write("**Type:**", thesis.get("thesis_type") or "—")
    meta2.write("**Account:**", _fmt_account(pos.get("account_type") or ""))
    meta3.write(
        "**Entry:**",
        entry_d.get("actual_price") or entry_d.get("target_price") or "—",
    )

    with st.form(key=f"edit_form_{tid}"):
        thesis_text = st.text_area(
            "Thesis *",
            value=thesis.get("thesis_statement") or "",
            height=100,
        )
        catalyst = st.text_input(
            "Catalyst",
            value=str(thesis.get("catalyst") or ""),
        )
        setup_type = st.text_input(
            "Setup type",
            value=str(thesis.get("setup_type") or ""),
        )
        fc1, fc2, fc3, fc4 = st.columns(4)
        with fc1:
            confidence = st.select_slider(
                "Confidence",
                options=[1, 2, 3, 4, 5],
                value=utils.confidence_level_from_score(cs),
                format_func=lambda x: CONFIDENCE_LABELS[x],
            )
        with fc2:
            stop_val = st.text_input("Stop", value=utils.stop_display(thesis))
        with fc3:
            target_val = st.text_input("Target", value=utils.target_display(thesis))
        with fc4:
            review_days = st.number_input(
                "Review every (days)",
                min_value=1,
                value=int(mon.get("review_interval_days") or 7),
            )

        if status in ("CLOSED", "INVALIDATED"):
            st.markdown("**Post-trade review**")
            what = st.text_area(
                "What happened?",
                value=str(outcome.get("what_happened") or ""),
                height=60,
            )
            lesson = st.text_input(
                "Lessons learned",
                value=str(outcome.get("lessons_learned") or ""),
            )
        else:
            what = None
            lesson = None

        submitted = st.form_submit_button("Save changes")

    if submitted:
        if not thesis_text.strip():
            st.warning("Thesis text is required.")
            return
        fields = utils.build_update_fields(
            thesis_text=thesis_text,
            confidence=confidence,
            stop_text=stop_val,
            target_text=target_val,
            catalyst=catalyst,
            setup_type=setup_type,
            review_interval_days=int(review_days),
            lessons_learned=lesson,
            what_happened=what,
        )
        val_errors = utils.validate_thesis_update(fields, confidence=confidence)
        if val_errors:
            st.error("\n".join(val_errors))
            return
        _, err = _run_safe(utils.update_thesis, tid, fields)
        if err:
            st.error(f"Update failed:\n{err}")
        else:
            st.success(f"Saved {ticker}.")
            st.cache_data.clear()
            st.rerun()

    st.divider()
    st.subheader("Actions")

    a1, a2, a3, a4 = st.columns(4)
    with a1:
        if status in ("ACTIVE", "ENTRY_READY") and st.button(
            "Mark reviewed", key=f"crud_rev_{tid}"
        ):
            _, err = _run_safe(utils.mark_reviewed, tid)
            if err:
                st.error(err)
            else:
                st.success("Marked reviewed.")
                st.cache_data.clear()
                st.rerun()
    with a2:
        if status == "IDEA" and st.button("Promote to ENTRY_READY", key=f"crud_promote_{tid}"):
            _, err = _run_safe(
                utils.transition_thesis,
                tid,
                "ENTRY_READY",
                "promoted via Theses page",
            )
            if err:
                st.error(err)
            else:
                st.success("Promoted to ENTRY_READY.")
                st.cache_data.clear()
                st.rerun()
    with a3:
        if status in ("ACTIVE", "ENTRY_READY", "IDEA") and st.button(
            "Stop tracking", key=f"crud_stop_{tid}"
        ):
            _, err = _run_safe(utils.stop_tracking_thesis, tid, "stopped via Theses page")
            if err:
                st.error(err)
            else:
                try:
                    research_utils.add_exclude_ticker(ticker, "stopped tracking")
                except (ValueError, OSError) as exc:
                    st.warning(f"Exclude list not updated: {exc}")
                st.success(f"Stopped tracking {ticker}.")
                st.cache_data.clear()
                st.rerun()
    with a4:
        if status in ("ACTIVE", "ENTRY_READY", "IDEA") and st.button(
            "Close position", key=f"crud_close_{tid}"
        ):
            st.session_state[f"crud_closing_{tid}"] = True

    if st.session_state.get(f"crud_closing_{tid}"):
        with st.form(key=f"crud_close_form_{tid}"):
            ep = st.number_input("Exit price", min_value=0.0, format="%.4f")
            ed = st.date_input("Exit date", value=date.today())
            reason = st.selectbox(
                "Exit reason",
                EXIT_REASONS,
                format_func=lambda x: EXIT_REASON_LABELS.get(x, x),
            )
            if st.form_submit_button("Confirm close"):
                _, err = _run_safe(utils.finalize_thesis, tid, reason, ep, ed)
                if err:
                    st.error(f"Close failed:\n{err}")
                else:
                    st.success(f"Closed {ticker}.")
                    st.session_state.pop(f"crud_closing_{tid}", None)
                    st.cache_data.clear()
                    st.rerun()

    with st.expander("Delete permanently", expanded=False):
        st.caption("Removes the thesis YAML file. Terminal theses only unless Force is checked.")
        confirm_del = st.checkbox("I understand this cannot be undone", key=f"crud_confirm_{tid}")
        force_del = st.checkbox("Force delete (non-terminal)", key=f"crud_force_{tid}")
        if st.button("Delete thesis", key=f"crud_del_{tid}"):
            if not confirm_del:
                st.warning("Check the confirmation box first.")
            else:
                _, err = _run_safe(utils.delete_thesis, tid, force=force_del)
                if err:
                    st.error(f"Delete failed:\n{err}")
                else:
                    try:
                        research_utils.add_exclude_ticker(ticker, "deleted thesis")
                    except (ValueError, OSError) as exc:
                        st.warning(f"Exclude list not updated: {exc}")
                    st.success(f"Deleted {ticker}.")
                    st.cache_data.clear()
                    st.rerun()

    if status in ("CLOSED", "INVALIDATED"):
        st.caption(
            f"Exit: {exit_d.get('actual_price') or '—'} · "
            f"Reason: {exit_d.get('exit_reason') or '—'}"
        )


def show_theses() -> None:
    st.header("Theses")
    st.caption("Create, browse, edit, and delete theses via thesis_store (no raw YAML edits).")

    _show_pending_positions_section()

    pending_count = sum(
        1 for p in utils.load_pending_ingest() if p.get("status") == "PENDING_THESIS"
    )
    if pending_count == 0:
        st.caption(
            "No pending sync rows — run **Refresh Positions** on Dashboard after Robinhood sync."
        )

    if pending_count:
        st.divider()

    with st.expander("Create new thesis (IDEA)", expanded=False):
        cc1, cc2 = st.columns(2)
        with cc1:
            c_ticker = (
                st.text_input("Ticker *", placeholder="AAPL", key="crud_new_ticker").strip().upper()
            )
            c_type = st.selectbox("Thesis type *", THESIS_TYPES, key="crud_new_type")
        with cc2:
            c_conf = st.select_slider(
                "Confidence",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: CONFIDENCE_LABELS[x],
                key="crud_new_conf",
            )
        c_text = st.text_area("Thesis *", height=80, key="crud_new_text")
        cc3, cc4 = st.columns(2)
        with cc3:
            c_stop = st.text_input("Stop", key="crud_new_stop")
        with cc4:
            c_target = st.text_input("Target", key="crud_new_target")
        if st.button("Register thesis", key="crud_register"):
            if not c_ticker:
                st.warning("Ticker is required.")
            elif not c_text.strip():
                st.warning("Thesis text is required.")
            else:
                td = _build_thesis_data(
                    ticker=c_ticker,
                    thesis_type=c_type,
                    thesis_text=c_text,
                    confidence=c_conf,
                    stop_text=c_stop,
                    target_text=c_target,
                    avg_cost=0.0,
                )
                val_errors = utils.validate_thesis_submit(td, confidence=c_conf)
                if val_errors:
                    st.error("\n".join(val_errors))
                else:
                    thesis_id, err = _run_safe(utils.register_thesis, td)
                    if err:
                        st.error(f"Register failed:\n{err}")
                    else:
                        st.success(f"Created {c_ticker} → {thesis_id} (IDEA)")
                        st.cache_data.clear()
                        st.rerun()

    st.divider()

    filter_cols = st.columns([2, 2, 1])
    with filter_cols[0]:
        status_filter = st.multiselect(
            "Status filter",
            utils.THESIS_STATUSES,
            default=utils.THESIS_STATUSES,
            key="crud_status_filter",
        )
    with filter_cols[1]:
        ticker_filter = (
            st.text_input(
                "Ticker search",
                placeholder="Filter by ticker",
                key="crud_ticker_filter",
            )
            .strip()
            .upper()
        )
    with filter_cols[2]:
        if st.button("Refresh", key="crud_refresh"):
            st.cache_data.clear()
            st.rerun()

    if not status_filter:
        st.info("Select at least one status to list theses.")
        return

    all_theses = utils.sort_theses_for_display(utils.load_theses(status_filter))
    if ticker_filter:
        all_theses = [t for t in all_theses if ticker_filter in str(t.get("ticker", "")).upper()]

    if not all_theses:
        st.info("No theses match the current filters.")
        return

    rows = [_thesis_summary_row(t) for t in all_theses]
    display_cols = ["Ticker", "Type", "Status", "Account", "Confidence", "Created"]
    display_df = utils.arrow_safe_df(pd.DataFrame(rows), display_cols)

    event = st.dataframe(
        display_df,
        width="stretch",
        on_select="rerun",
        selection_mode="single-row",
        key="crud_table",
        hide_index=True,
    )

    sel = (event.selection.rows if hasattr(event, "selection") else []) or []
    if sel:
        thesis = all_theses[sel[0]]
        with st.container(border=True):
            st.subheader(f"{thesis.get('ticker')} — edit")
            _render_thesis_edit_form(thesis)


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
                st.caption(f"Thesis: {summary}", width="content")
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
                    reason = st.selectbox(
                        "Exit reason",
                        EXIT_REASONS,
                        format_func=lambda x: EXIT_REASON_LABELS.get(x, x),
                        key=f"uc_r_{tid}",
                    )
                    if st.form_submit_button("Confirm Close"):
                        _, err = _run_safe(utils.finalize_thesis, tid, reason, ep, ed)
                        if err:
                            st.error(
                                f"Close failed (finalize_thesis {tid!r} {reason!r} {ep} {ed.isoformat()!r}):\n{err}"
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
                            utils.finalize_thesis, tid, "manual", 0.0, date.today()
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
    excluded_closed = sum(
        1 for t in closed_theses if utils.is_ticker_excluded(str(t.get("ticker", "")))
    )
    if excluded_closed:
        st.caption(f"{excluded_closed} excluded closed position(s) hidden below.")
    thirty_ago = (date.today() - timedelta(days=30)).isoformat()
    needs_review = [
        t
        for t in closed_theses
        if not utils.is_ticker_excluded(str(t.get("ticker", "")))
        and ((t.get("exit") or {}).get("actual_date") or "") >= thirty_ago
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
        t
        for t in closed_theses
        if not utils.is_ticker_excluded(str(t.get("ticker", "")))
        and ((t.get("exit") or {}).get("actual_date") or "") >= seven_ago
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
                    "Entry": str(ep) if ep is not None else "—",
                    "Exit": str(xp) if xp is not None else "—",
                    "P&L": pnl,
                    "Confidence": f"{int(cs * 5)}/5" if cs else "—",
                    "Outcome": exit_d.get("exit_reason") or "—",
                }
            )
        closed_cols = ["Ticker", "Account", "Entry", "Exit", "P&L", "Confidence", "Outcome"]
        st.dataframe(
            utils.arrow_safe_df(pd.DataFrame(rows), closed_cols),
            width="stretch",
            hide_index=True,
        )


# ── page 4: research ───────────────────────────────────────────────────────────


def _research_row_style(row: pd.Series, meta: dict) -> list[str]:
    ticker = row.get("Ticker", "")
    info = meta.get(ticker, {})
    ui_status = info.get("ui_status", "")
    badge = info.get("badge", "")
    thesis_status = info.get("thesis_status", "")
    bg = ""
    if ui_status == "stale" or (
        ui_status == "missing" and thesis_status in ("ACTIVE", "ENTRY_READY")
    ):
        bg = "background-color: #3d0000"
    elif badge == "WARN":
        bg = "background-color: #3d2000"
    elif badge == "OK":
        bg = "background-color: #0a2e1a"
    return [bg] * len(row)


def _run_stale_research_scan(dry_run: bool) -> tuple[str, int]:
    script = utils.get_repo_root() / "scripts" / "update_stale_research.py"
    cmd = [sys.executable, str(script)]
    if dry_run:
        cmd.append("--dry-run")
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=utils.get_repo_root(),
        timeout=120,
    )
    output = (result.stdout or "") + (result.stderr or "")
    return output.strip(), result.returncode


def show_research() -> None:
    st.header("Research")

    rows = _research_rows()
    if not rows:
        st.info("No eligible tickers — add positions or edit research_watchlist.yaml")
        _show_research_refresh()
        return

    stale_count = sum(1 for r in rows if r["ui_status"] == "stale" or r["badge"] == "STALE")
    missing_count = sum(1 for r in rows if r["ui_status"] in ("missing", "needs_deep_research"))
    queued_count = research_utils.queue_recent_count()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tracked tickers", len(rows))
    m2.metric(
        "Stale (>14d)",
        stale_count,
        delta=f"⚠ {stale_count}" if stale_count else None,
        delta_color="inverse" if stale_count else "off",
    )
    m3.metric(
        "Missing report",
        missing_count,
        delta=f"⚠ {missing_count}" if missing_count else None,
        delta_color="inverse" if missing_count else "off",
    )
    m4.metric("Queued updates", queued_count)

    st.divider()

    meta = {r["ticker"]: r for r in rows}
    table_rows = []
    for r in rows:
        table_rows.append(
            {
                "_ticker": r["ticker"],
                "Ticker": r["ticker"],
                "Last Report": r["last_report_date"] or "—",
                "Days": str(r["days_stale"]) if r["days_stale"] is not None else "—",
                "Thesis": r["thesis_status"],
                "Watching": "yes" if r["watching"] else "—",
                "Status": r["ui_status"],
                "Badge": r["badge"],
            }
        )

    df = pd.DataFrame(table_rows)
    display_cols = ["Ticker", "Last Report", "Days", "Thesis", "Watching", "Status", "Badge"]
    display_df = utils.arrow_safe_df(df, display_cols)
    styled = display_df.style.apply(
        lambda row: _research_row_style(row, meta),
        axis=1,
    )

    event = st.dataframe(
        styled,
        width="stretch",
        on_select="rerun",
        selection_mode="single-row",
        key="research_table",
        hide_index=True,
    )

    sel = (event.selection.rows if hasattr(event, "selection") else []) or []
    if sel:
        selected = table_rows[sel[0]]
        ticker = selected["_ticker"]
        info = meta[ticker]

        with st.container(border=True):
            st.subheader(f"{ticker} — {info['ui_status']}")
            if info.get("notes"):
                st.caption(info["notes"])
            st.caption(f"Eligibility: {', '.join(info['eligibility']) or '—'}")

            if info.get("prefetch_available") and info.get("prefetch_path"):
                with st.expander("Open prefetch", expanded=False):
                    try:
                        prefetch_data = json.loads(Path(info["prefetch_path"]).read_text())
                        st.json(prefetch_data)
                    except (json.JSONDecodeError, OSError) as exc:
                        st.error(f"Could not read prefetch: {exc}")

            if info["ui_status"] != "missing":
                st.text_area(
                    "Copy update prompt",
                    value=research_utils.build_update_prompt(ticker),
                    height=120,
                    key=f"upd_prompt_{ticker}",
                )
            if info["ui_status"] == "missing":
                st.text_area(
                    "Copy deep-research prompt",
                    value=research_utils.build_deep_research_prompt(ticker),
                    height=80,
                    key=f"deep_prompt_{ticker}",
                )

            if st.button("Exclude from research", key=f"excl_{ticker}"):
                try:
                    research_utils.add_exclude_ticker(ticker, "excluded via research page")
                    st.success(f"{ticker} added to exclude list.")
                    st.cache_data.clear()
                    st.rerun()
                except (ValueError, OSError) as exc:
                    st.error(str(exc))

    st.divider()

    with st.container(border=True):
        st.subheader("Excluded tickers")
        st.caption(
            f"File: {research_utils.resolve_exclude_path().relative_to(utils.get_repo_root())}"
        )
        exclude = research_utils.load_exclude_for_editor()
        excl_rows = [
            {"Ticker": t, "Reason": cfg.get("reason", "")} for t, cfg in sorted(exclude.items())
        ]
        if not excl_rows:
            excl_rows = [{"Ticker": "", "Reason": ""}]
        excl_edited = st.data_editor(
            pd.DataFrame(excl_rows),
            num_rows="dynamic",
            column_config={
                "Ticker": st.column_config.TextColumn("Ticker", required=True),
                "Reason": st.column_config.TextColumn("Reason"),
            },
            hide_index=True,
            key="exclude_editor",
        )
        if st.button("Save exclude list", key="save_exclude"):
            entries: dict[str, dict] = {}
            for _, row in excl_edited.iterrows():
                t = str(row.get("Ticker", "")).strip().upper()
                if not t:
                    continue
                entries[t] = {"reason": str(row.get("Reason", "") or "")}
            try:
                research_utils.save_exclude(entries)
                st.success("Exclude list saved.")
                st.cache_data.clear()
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
            except OSError as exc:
                st.error(f"Save failed: {exc}")

    st.divider()

    with st.container(border=True):
        st.subheader("Watchlist")
        st.caption(
            f"File: {research_utils.resolve_watchlist_path().relative_to(utils.get_repo_root())}"
        )
        watchlist = research_utils.load_watchlist_for_editor()
        editor_rows = [
            {
                "Ticker": t,
                "Watching": cfg.get("watching", False),
                "Notes": cfg.get("notes", ""),
            }
            for t, cfg in sorted(watchlist.items())
        ]
        if not editor_rows:
            editor_rows = [{"Ticker": "", "Watching": True, "Notes": ""}]

        edited = st.data_editor(
            pd.DataFrame(editor_rows),
            num_rows="dynamic",
            column_config={
                "Ticker": st.column_config.TextColumn("Ticker", required=True),
                "Watching": st.column_config.CheckboxColumn("Watching"),
                "Notes": st.column_config.TextColumn("Notes"),
            },
            hide_index=True,
            key="watchlist_editor",
        )

        if st.button("Save watchlist", key="save_watchlist"):
            entries: dict[str, dict] = {}
            for _, row in edited.iterrows():
                t = str(row.get("Ticker", "")).strip().upper()
                if not t:
                    continue
                entries[t] = {
                    "watching": bool(row.get("Watching", False)),
                    "notes": str(row.get("Notes", "") or ""),
                }
            try:
                research_utils.save_watchlist(entries)
                st.success("Watchlist saved.")
                st.cache_data.clear()
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
            except OSError as exc:
                st.error(f"Save failed: {exc}")

    st.divider()

    queue = research_utils.load_update_queue()
    with st.container(border=True):
        st.subheader("Update queue")
        if queue:
            st.caption(
                f"Generated: {queue.get('generated_at', '—')} | "
                f"Threshold: {queue.get('threshold_days', research_utils.STALE_THRESHOLD_DAYS)}d"
            )
            q_rows = []
            for entry in queue.get("tickers") or []:
                if not isinstance(entry, dict):
                    continue
                q_rows.append(
                    {
                        "Ticker": entry.get("ticker", ""),
                        "Status": entry.get("status", ""),
                        "Days stale": (
                            str(entry["days_stale"]) if entry.get("days_stale") is not None else "—"
                        ),
                        "Last report": entry.get("last_report") or "—",
                    }
                )
            if q_rows:
                queue_cols = ["Ticker", "Status", "Days stale", "Last report"]
                st.dataframe(
                    utils.arrow_safe_df(pd.DataFrame(q_rows), queue_cols),
                    width="stretch",
                    hide_index=True,
                )
        else:
            st.info("No queue file yet. Regenerate to create state/research_update_queue.json.")

        b1, b2 = st.columns(2)
        with b1:
            if st.button("Refresh queue now", key="research_dry_run"):
                with st.spinner("Running dry-run scan..."):
                    output, code = _run_stale_research_scan(dry_run=True)
                st.code(output or "(no output)")
                st.caption(f"Exit code: {code}")
        with b2:
            if st.button("Regenerate queue", key="research_regen_queue"):
                with st.spinner("Regenerating queue..."):
                    output, code = _run_stale_research_scan(dry_run=False)
                if code in (0, 2):
                    st.success("Queue regenerated.")
                    if output:
                        st.code(output[:2000])
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Scan failed (exit {code}):\n{output[:2000]}")

    st.divider()
    _show_research_refresh()


# ── page: market ───────────────────────────────────────────────────────────────


def show_market() -> None:
    st.header("Market")

    dates = market_utils.list_market_context_dates()
    if not dates:
        st.info(
            "No pre-market reports in reports/logs/. "
            "Run `uv run python3 scripts/pre_market.py` on a trading day."
        )
        return

    date_options = [d.isoformat() for d in dates]
    if st.session_state.get("market_date") not in date_options:
        st.session_state.pop("market_date", None)
    selected = st.selectbox("Report date", date_options, key="market_date")
    as_of = date.fromisoformat(selected)
    ctx = market_utils.load_market_context(as_of)
    if not ctx:
        st.warning(f"No market context found for {selected}.")
        return

    syn = ctx.get("synthesis") or {}
    b = ctx.get("breadth") or {}
    u = ctx.get("uptrend") or {}
    s = ctx.get("sector") or {}
    flags = ctx.get("position_flags") or {}

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Posture", syn.get("posture", "UNKNOWN"))
    c2.metric("Ceiling", syn.get("ceiling", "N/A"))
    c3.metric("Breadth", f"{b.get('score', '—')}/100", help=str(b.get("zone") or ""))
    c4.metric("Uptrend", f"{u.get('score', '—')}/100", help=str(u.get("zone") or ""))
    c5.metric("Leading Sector", s.get("leading_sector") or "—")

    st.subheader("Synthesis")
    if syn.get("headline"):
        st.write(syn["headline"])

    risk_flags = syn.get("risk_flags") or []
    if risk_flags:
        st.markdown("**Risk flags**")
        for rf in risk_flags:
            st.markdown(f"- {rf}")

    actions = syn.get("actions") or []
    if actions:
        st.markdown("**Actions**")
        for action in actions:
            st.markdown(f"- {action}")

    warnings = (u.get("active_warnings") or []) + (b.get("active_warnings") or [])
    if warnings:
        st.subheader("Warnings")
        for w in warnings:
            if isinstance(w, dict):
                label = w.get("label") or w.get("flag") or "Warning"
                desc = w.get("description") or ""
                st.warning(f"**{label}** — {desc}")

    st.subheader("Sector")
    st.caption(
        f"Cycle: **{s.get('cycle_phase') or 'N/A'}** · Regime: **{s.get('risk_regime') or 'N/A'}**"
    )
    top = s.get("top_sectors") or []
    if top:
        st.table(
            pd.DataFrame(
                [
                    {
                        "Rank": row.get("rank"),
                        "Sector": row.get("sector"),
                        "Ratio": row.get("ratio"),
                    }
                    for row in top
                ]
            )
        )
    overbought = s.get("overbought") or []
    if overbought:
        st.markdown("**Overbought:** " + ", ".join(overbought))

    urgent = flags.get("urgent") or []
    watch = flags.get("watch") or []
    if urgent or watch:
        st.subheader("Position Flags")
        for flag in urgent:
            st.error(flag)
        for flag in watch:
            st.warning(flag)

    sources = ctx.get("sources") or {}
    st.divider()
    st.subheader("Detail Reports")
    for label, key in (
        ("Breadth", "breadth"),
        ("Uptrend", "uptrend"),
        ("Sector", "sector"),
    ):
        rel = sources.get(key)
        content, display_path, is_json_summary = market_utils.load_artifact_display(rel, key)
        with st.expander(f"{label} — {display_path or rel or 'not found'}"):
            if content:
                if is_json_summary:
                    st.caption("Summary generated from JSON (full markdown report not found).")
                st.markdown(research_utils.escape_dollar_signs_for_streamlit(content))
            else:
                st.caption("Report not available.")

    ctx_path = ctx.get("_path")
    if ctx_path:
        st.caption(f"Context file: `{ctx_path}`")


# ── page: reports ──────────────────────────────────────────────────────────────


def show_reports() -> None:
    st.header("Reports")

    tickers = research_utils.list_report_tickers()
    if not tickers:
        st.info(
            "No research reports in reports/research/. "
            "Run deep-research or update-research, then return here."
        )
        if st.button("Go to Research", key="reports_empty_go_research"):
            st.session_state["nav_page"] = "Research"
            st.rerun()
        return

    ticker = st.selectbox("Ticker", tickers, key="reports_ticker")
    if st.session_state.get("_reports_ticker_prev") != ticker:
        st.session_state.pop("reports_date", None)
    st.session_state["_reports_ticker_prev"] = ticker

    entries = research_utils.list_reports_for_ticker(ticker)
    if not entries:
        st.warning(f"No report files found for {ticker}.")
        return

    if len(entries) > 1:
        date_options = [e["date"].isoformat() for e in entries]
        if st.session_state.get("reports_date") not in date_options:
            st.session_state.pop("reports_date", None)
        selected_date = st.selectbox("Report date", date_options, key="reports_date")
        selected = next(e for e in entries if e["date"].isoformat() == selected_date)
    else:
        selected = entries[0]

    report_path: Path = selected["path"]
    report_date: date = selected["date"]
    days_old = (date.today() - report_date).days
    try:
        rel_path = report_path.relative_to(utils.get_repo_root())
    except ValueError:
        rel_path = report_path
    st.caption(f"{rel_path} · {days_old} days old")

    content = research_utils.load_report_markdown(report_path)
    if content:
        with st.container(height=3000):
            st.markdown(research_utils.escape_dollar_signs_for_streamlit(content))
    else:
        st.warning("Could not read report file.")

    if days_old > research_utils.STALE_THRESHOLD_DAYS:
        st.caption(f"Report is stale (>{research_utils.STALE_THRESHOLD_DAYS} days).")

    st.divider()
    archive_exclude = st.checkbox(
        "Also add ticker to exclude list",
        value=True,
        key="reports_archive_exclude",
    )
    if st.button("Archive this report", key="reports_archive_btn"):
        try:
            research_utils.archive_report(report_path)
            if archive_exclude:
                research_utils.add_exclude_ticker(ticker, "archived report")
            st.success(f"Archived {report_path.name}.")
            st.cache_data.clear()
            st.rerun()
        except (FileNotFoundError, FileExistsError, OSError) as exc:
            st.error(str(exc))

    if st.button("Go to Research", key="reports_go_research"):
        st.session_state["nav_page"] = "Research"
        st.rerun()


def _show_research_refresh() -> None:
    if st.button("Refresh data", key="research_refresh_data"):
        st.cache_data.clear()
        st.rerun()


# ── entry point ────────────────────────────────────────────────────────────────


def main() -> None:
    st.set_page_config(page_title="Thesis Manager", page_icon="📊", layout="wide")

    if "nav_page" in st.session_state:
        st.session_state["sidebar_page"] = st.session_state.pop("nav_page")

    page = st.sidebar.radio(
        "Page",
        PAGES,
        label_visibility="collapsed",
        key="sidebar_page",
    )
    st.sidebar.caption("trader-memory-core UI")

    if page == "Dashboard":
        show_dashboard()
    elif page == "Market":
        show_market()
    elif page == "Research":
        show_research()
    elif page == "Reports":
        show_reports()
    elif page == "Theses":
        show_theses()
    else:
        show_review()


if __name__ == "__main__":
    main()
