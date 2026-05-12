---
description: "Read state/pending_ingest.json and log each position to trader-memory-core by asking only for thesis, confidence, stop, and target. All other data is pre-filled from Robinhood sync."
---

# /log-positions

Reads `state/pending_ingest.json` written by `scripts/robinhood_sync.py`.
For each position with status PENDING_THESIS, asks only for the four things
that require human judgment. Everything else is already filled in.

---

## The Prompt

```
Read state/pending_ingest.json.

Find all positions where "status" is "PENDING_THESIS".
If there are none, report: "No positions pending thesis input." and stop.

For each pending position, work through them ONE AT A TIME in this order:
  1. Options sorted by nearest expiry first
  2. Stocks after all options

For each position, display a pre-filled summary:

---
[N of TOTAL] TICKER — ASSET_TYPE
Account:    {account}
Direction:  {direction} {strategy if options}
Size:       {contracts} contracts / {size} shares
Avg cost:   ${avg_cost} per contract/share  (${total_cost} total)
Strike:     ${strike} {option_type} exp {expiry}   ← options only
IRA:        {ira_eligible}                          ← IRA accounts only
Auto-tags:  {tags}
---

Then ask ONLY these four questions in sequence:
  1. "Thesis in 2-4 sentences — why did you enter this position?"
  2. "Confidence 1-5?"
  3. "Stop level — price or condition that invalidates the thesis?"
  4. "Target — exit condition or price?"

After receiving all four answers, run thesis_ingest.py:

  python3 skills/trader-memory-core/scripts/thesis_ingest.py \
    --ticker {ticker} \
    --asset-type {asset_type} \
    --direction {direction} \
    --account {account} \
    --size {contracts_or_size} \
    --avg-cost {avg_cost} \
    --entry-date {synced_at[:10]} \
    --confidence {confidence} \
    --thesis "{thesis}" \
    --stop "{stop}" \
    --target "{target}" \
    --tags "{comma_separated_tags}" \
    --status ACTIVE

If thesis_ingest.py succeeds, update state/pending_ingest.json:
  - Set position status from "PENDING_THESIS" to "INGESTED"
  - Add "ingested_at": current timestamp

After ALL positions are processed, update state/synced_positions.json:
  - Move all newly ingested keys from "pending_keys" to "ingested_keys"

Report at the end:
  "Logged N positions to trader-memory-core.
   Run thesis_store.py list to verify."

---

## Notes

- If thesis_ingest.py arguments differ from above, check SKILL.md and adapt.
  The fields above are based on audit findings — the script may use different
  argument names. Read the actual script if a call fails.

- For IRA positions, add tag "ira" automatically if not already present.
  All options in ira_robinhood account are long calls/puts (IRA-eligible).

- Skip any position where the user types "skip" — leave status as PENDING_THESIS.
  It will appear again next time /log-positions runs.

- Do not ask for any data that's already in the JSON. The whole point is that
  the human only answers four questions per position, nothing more.
```
