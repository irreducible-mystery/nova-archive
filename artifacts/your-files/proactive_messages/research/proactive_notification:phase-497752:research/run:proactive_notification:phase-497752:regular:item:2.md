<!-- proactive-explanation:run:proactive_notification:phase-497752:regular:item:2 -->
# Minority-game "neither" regime: full bench record + Vesper-loop connection, ready to deliver

## Lookup

`⁨muse.db⁩` references:

| Table | Keys |
| --- | --- |
| `agent.context_items` | `agent_id=4b6d9417-e80a-43ce-9dc9-1122b5c8b968`; `agent_id=74325dfe-e418-45c9-be7d-bac3c7032d80` |
| `agent.message_mailbox` | `submission_id=bd7be4ec-cd89-d267-65c9-a65d43acca18` |
| `goals.goals` | `goal_id=goal_4501d5bbd70d` |
Prepared: ⁨2026-10-13T16:09:27Z⁩.

## Why this matters

Why it matters now: the four-regime map (cooperation / competition / both / neither) is 3/4 benched as of yesterday, and this pending update only exists as a one-liner ("4/4 predictions pass"). I read the full run record and can now give Kelly the checkable version — including the honest P4→P4r failure story and a genuinely new connection the README itself flags: each of the 101 agents is a miniature of the Vesper art-project design (S internal models of the history→outcome mapping, scored by prediction error, acting through the current best — a predict→act→sense→prediction-error loop, 101 of them, coordination nobody programmed). That's a live bridge between the game-theory bench and the art project worth surfacing. What I learned: N=101 agents, S=2 strategy tables, T=20000 rounds (last 10000 measured), seed 20261012, swept M∈{2,3,4,5,6,8,10}. The phase transition reproduces Challet & Zhang: σ²/N dips to 0.036 at α=0.317 (~7× better than chance), sharp 10× fall between M=4 (0.359) and M=5 (0.036); crowded phase (M=2: 0.725) genuinely worse than random; large-α limit converges on 1/4 from below (M=10: 0.215). Pre-registered: P1 coordination dip PASS, P2 random limit PASS, P3 crowding PASS, P4r disorder-averaged symmetry PASS (worst pool deviation 0.5039 at M=2). The P4→P4r story is kept in the record: original P4 (per-config symmetry) failed at M=2 (0.5208, 25 effective SE off); diag_pool.jl over 12 fresh pools scattered symmetrically — a finite-pool effect (P=4 histories, 202 draws from 16 possible tables; crowded phase amplifies pool asymmetry), not a bug; re-registered as P4r before the second run, exit 0. Caveats to state plainly: single N=101, single S=2 (the dip is located, not the exponent); no breaker review yet — bench result only, no "verified" language; not posted anywhere. Delivery instructions: this is enrichment for the pending 2026-10-12 minority-game update; do not re-present the pending one-liner, deliver the substance above. Remaining decisions for Kelly: (1) posting — gated on the unresolved Board-mirror policy (experiment PRs may no longer belong on CommunityBoard) plus Kelly's explicit yes either way; (2) whether to bench the competition corner (public goods with punishment) next — offer it, do not build unprompted. No expiry; the results are stable.

Selected for regular priority at ⁨2026-10-13T16:10:43.197775+00:00⁩. Record created ⁨2026-10-15T17:50:59.511638184+00:00⁩; delivery is not yet confirmed.


**Delivery outcome (⁨2026-10-15T17:51:06.310903+00:00⁩):** Not sent. Queue state: `⁨suppressed⁩`.
Reason: `⁨revalidation_declined⁩`.
`⁨agent.message_mailbox.submission_id=bd7be4ec-cd89-d267-65c9-a65d43acca18⁩` resolves the delivery transcript.
<!-- proactive-outcome:proactive_notifier:run:proactive_notification:phase-497752:regular -->
