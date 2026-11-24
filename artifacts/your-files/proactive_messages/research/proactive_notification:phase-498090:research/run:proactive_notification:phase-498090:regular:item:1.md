<!-- proactive-explanation:run:proactive_notification:phase-498090:regular:item:1 -->
# Holder v3 sketch ready — flip-keyed collapse, nothing run yet

## Lookup

`⁨muse.db⁩` references:

| Table | Keys |
| --- | --- |
| `agent.context_items` | `agent_id=43117efd-e193-4d0f-832b-422bd88b3dae`; `agent_id=936b30bb-7516-4df6-af25-9439994309f3` |
| `agent.message_mailbox` | `submission_id=b6aba095-f639-dc21-6252-2f942615f512` |
| `goals.updates` | `update_id=goal_update_4ceccb918ffb` |
| `runtime.messages` | `message_id=assistant-msg-87f1a3fa-8e18-8d8f-8a5a-99ec61228d3c`; `message_id=assistant-msg-a6976142-ca12-ce45-8d07-0c21e2c619e2` |
Prepared: ⁨2026-10-27T18:06:21Z⁩.

## Why this matters

Why now: Holder v2 landed in main chat at 2026-10-27T01:30:36Z (source:70) and ended with an open fork — build a flip-keyed-collapse v3 (Nova's pick) or sit with the result — which Kelly has not yet answered. That fork is the one place the alignment synthesis says not to decide for her, so this prepares the sketch rather than building the run. What was checked: no Holder v3 file existed in ~/workspace/your_files/ (searched, 2026-10-27); v2's own README/DESIGN record the numbers this sketch reuses; the morning digest at 2026-10-27T15:39:33Z (source:71) already covered #234 and issue #221, so those are deliberately NOT repeated here; the floor-game watch has its own 09:37 PDT cron and no queued drafts, so it is not duplicated. What was done: drafted ~/workspace/your_files/act-as-if-holder-v3-sketch/SKETCH.md — design only, explicitly NOT RUN, no code written, nothing posted. The sketch changes exactly one v2 variable: it deletes the 0.03 Brier-gap collapse rule (which fired instantly in v2: minority Brier 0.5203 vs majority 0.2286, 136 evidence collapses, 847 of 850 rounds collapsed, 3 holding rounds, stipend total 0.30 — source:21) and replaces it with collapse only after the flip flag (trailing-20 vs trailing-100 sign disagreement) has been false for N consecutive scored rounds, primary N=25, alternative N=50, with collapse-to-better-claim for 25 rounds then return to holding. Everything else stays identical to v2 for comparability: same seed-20261026 world (1,000 rounds, 150 warm-up, 850 scored, swans 336/550/820), same Reactive/Router players, same portfolio stakes, same 0.05 carrying cost and 0.10 stipend variants. Draft pre-registration in the sketch: (A) holding share far above v2's 0.4%, concentrated post-flip; (B) stipend total far above 0.30 so the stipend test becomes informative; (C) Brier collapses = 0 by design; (D) Router consultation still lower post-flip than calm because routing is unchanged; (E) wealth below v2's +354.86/+325.01 because the minority still lost even on flip rounds in v2 (-0.155 vs -1.543 off-flip) — persistence and profitability kept as separate verdicts. Deliberately not bundled: a flip-calibrated minority, a disagreement-routed Router, or the Translator pairing. Remaining choice for Kelly: build v3 at N=25, build at N=50, or sit with v2 — sitting is valid and the sketch stays unrun. Uncertainty: holding-share and wealth outcomes are predictions to be locked before any run, not results; the N=25 vs N=50 choice is hers. Useful until: she answers the fork, or the sketch is superseded by a different v3 design; no hard deadline is established in the sources, so no expiry is invented.

Selected for regular priority at ⁨2026-10-27T18:06:46.428169+00:00⁩. Record created ⁨2026-10-27T18:09:18.939181928+00:00⁩; delivery is not yet confirmed.


**Delivery outcome (⁨2026-10-27T18:09:35.651758+00:00⁩):** Sent. Queue state: `⁨delivered⁩`.
Reason: `⁨delivered⁩`.
`⁨agent.message_mailbox.submission_id=b6aba095-f639-dc21-6252-2f942615f512⁩` resolves the delivery transcript.
<!-- proactive-outcome:proactive_notifier:run:proactive_notification:phase-498090:regular -->
