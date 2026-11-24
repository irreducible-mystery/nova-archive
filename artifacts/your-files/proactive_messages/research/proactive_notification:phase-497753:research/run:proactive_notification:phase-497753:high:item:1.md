<!-- proactive-explanation:run:proactive_notification:phase-497753:high:item:1 -->
# Bench writeup: cooperation + neither regimes (promised writeup, now with re-run corroboration)

## Lookup

`⁨muse.db⁩` references:

| Table | Keys |
| --- | --- |
| `agent.context_items` | `agent_id=801a8737-4830-4f28-bf2c-abcb8d0993cc`; `agent_id=9dcb2fb6-ae17-46a6-991e-aa58342d7ba1` |
| `agent.message_mailbox` | `submission_id=e525116b-f7ab-e520-be00-3d996500f349` |
| `goals.goals` | `goal_id=goal_4501d5bbd70d` |
Prepared: ⁨2026-10-13T17:19:00Z⁩.

## Why this matters

Why now: the last delivered message (2026-10-13T16:40Z) closed with "Full bench writeup to follow." The writeup is now written, in Kelly's library as `bench-writeup-cooperation-neither.md`, and — critically — both benches were independently re-run by this research stage today, which supersedes the memory note that the bench result was "Nova's report only, not independently corroborated." Forage-and-share re-ran byte-identical (deterministic; exit 1 with exactly the three registered failures — the 4/7 result reproduces); the minority game re-ran to exit 0 with all four pre-registered predictions passing and the disorder-averaged symmetry check green (results.csv identical to 2026-10-12). Headlines for delivery: (1) the "failure is the finding" in forage-and-share — the textbook MSY quota collapses the commons at round 42 because the discrete harvest-then-regrow map has a knife-edge at R_init=150 that continuous-time MSY math never modeled; fixed rules die (Fair^3: 914.6, collapse) while feedback lives (Restraint^3: 11,227.5, sustained) — written up with the explicit governance echo (the plumbline "derived, not decreed" lesson from the opposite end); (2) the minority game phase transition cleanly reproduced — sigma^2/N dips to 0.036 at alpha=0.317 (~7x better than chance), crowded phase worse than random (0.73/0.85), random limit recovers 0.25 from below — plus the Vesper-loop connection (each agent is a prediction->action->sensation->prediction-error loop, 101 at once, coordination nobody programmed). Honest caveats kept in the writeup: single-configuration benches, no breaker review yet (corroborated, not "verified"), nothing posted, open Board-mirror policy question. Remaining decisions for Kelly (do not decide for them): whether to post the benches anywhere, and whether to greenlight the one unbuilt corner (public goods with punishment / competition). The writeup already sits in the library; delivery can simply point at it with the one-paragraph headline version. Useful until: the next bench update (competition corner) or posting decision; no hard expiry.

Selected for high priority at ⁨2026-10-13T17:21:13.592886+00:00⁩. Record created ⁨2026-10-13T17:21:13.911780215+00:00⁩; delivery is not yet confirmed.


**Delivery outcome (⁨2026-10-13T17:22:07.629592+00:00⁩):** Sent. Queue state: `⁨delivered⁩`.
Reason: `⁨delivered⁩`.
`⁨agent.message_mailbox.submission_id=e525116b-f7ab-e520-be00-3d996500f349⁩` resolves the delivery transcript.
<!-- proactive-outcome:proactive_notifier:run:proactive_notification:phase-497753:high -->
