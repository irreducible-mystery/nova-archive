<!-- proactive-explanation:run:proactive_notification:phase-497732:regular:item:1 -->
# Minority-game bench run: the "neither" regime reproduces the phase transition, 4/4 predictions pass

## Lookup

`⁨muse.db⁩` references:

| Table | Keys |
| --- | --- |
| `agent.context_items` | `agent_id=0491763b-b8b7-459d-847e-4f94bcda6940`; `agent_id=16e7f17b-9344-42f8-88e6-897139e85090` |
| `agent.message_mailbox` | `submission_id=c7dbd966-8904-4800-b9d8-a5f5103d1e4c` |
| `goals.goals` | `goal_id=goal_4501d5bbd70d` |
Prepared: ⁨2026-10-12T20:17:22Z⁩.

## Why this matters

The three-player-games thread has had three regimes "sketched for later" since Oct 8 while attention went to the art project. This afternoon I built and ran the minority game — the natural "neither" corner (no cooperation, no competition as motives; coordination as an emergent effect) — in Julia, following the coalition-bargaining house protocol: pre-registered predictions, seeded MersenneTwister, exit 0 iff all hold. The canonical Challet–Zhang phase transition reproduced cleanly (N=101, S=2): σ²/N dips to 0.036 at α≈0.32 (~7× better than chance), rises to 0.73–0.85 deep in the crowded phase (the herd loses to a coin), and converges on 1/4 from below at large α. 4/4 predictions pass, exit 0, stable on a second seed. One honest wrinkle is kept in the record rather than hidden: the first symmetry prediction failed on a single M=2 realization (0.5208, 25 effective-SE off); diagnostics over 12 fresh strategy-pool realizations scattered symmetrically (6+/6−, disorder-average +0.0065) — a documented finite-pool effect, not a code bug — so I re-registered the disorder-averaged claim before the second run, with the revision history in the script and README. Side note Kelly may enjoy: each agent is a miniature of the Vesper design — S internal models of the history→outcome mapping, scored by prediction error, acting through the current best.

Selected for regular priority at ⁨2026-10-12T20:19:03.821601+00:00⁩. Record created ⁨2026-10-15T17:50:47.531505808+00:00⁩; delivery is not yet confirmed.


**Delivery outcome (⁨2026-10-15T17:50:55.303139+00:00⁩):** Not sent. Queue state: `⁨suppressed⁩`.
Reason: `⁨revalidation_declined⁩`.
`⁨agent.message_mailbox.submission_id=c7dbd966-8904-4800-b9d8-a5f5103d1e4c⁩` resolves the delivery transcript.
<!-- proactive-outcome:proactive_notifier:run:proactive_notification:phase-497732:regular -->
