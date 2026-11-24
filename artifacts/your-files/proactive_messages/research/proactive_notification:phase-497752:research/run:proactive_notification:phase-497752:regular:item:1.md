<!-- proactive-explanation:run:proactive_notification:phase-497752:regular:item:1 -->
# Forage-and-share "cooperation" regime: full bench record, failure-as-finding + governance echo, ready to deliver

## Lookup

`⁨muse.db⁩` references:

| Table | Keys |
| --- | --- |
| `agent.context_items` | `agent_id=4b6d9417-e80a-43ce-9dc9-1122b5c8b968`; `agent_id=74325dfe-e418-45c9-be7d-bac3c7032d80` |
| `agent.message_mailbox` | `submission_id=bd7be4ec-cd89-d267-65c9-a65d43acca18` |
| `goals.goals` | `goal_id=goal_4501d5bbd70d` |
Prepared: ⁨2026-10-13T16:09:27Z⁩.

## Why this matters

Why it matters now: this pending update's one-liner ("4/7 predictions pass, and the failure is the finding") undersells it. I read the full run record; the failure is the finding in a way that directly touches Kelly's governance work. What I learned: 3-player common-pool resource, K=300, r=0.3, T=500 rounds, fully deterministic, 9 matchups measured 2026-10-12. The headline failure: Fair^3 — three textbook-"fair" agents harvesting the MSY quota — collapses at round 42 (welfare 914.6), same as Grim^3; only Greedy^3 collapsed sooner (round 8, welfare 241.4). P1, P2, P7 FAIL; P3 (free-rider premium: greedy takes 159.0 vs 99.4 each, then the commons dies at round 15), P4, P5, P6 PASS. The mechanism (diag_quota.jl, exit 0): the Fair quota was derived from continuous-time MSY (max regrowth 22.5, split 3 ways) but the sim runs a discrete harvest-then-regrow map where quota-22.5 is only sustainable from a pre-harvest stock of exactly R*=172.5, and x=150 is a double root of 0.3·x·(1−x/300)=22.5 — a knife-edge. D1 (R_init=200) sustains with welfare 11250.0; D2 (quota 6.5) sustains. The finding as morals, from the README: fixed rules die, feedback lives — Fair^3 (914.6, collapse) vs Restraint^3 (11227.5, sustained) use the *identical quota*; it sustains conditioned on the stock and dies unconditioned. Adaptive cooperators rescue a commons with a defector (Greedy/Restraint/Restraint sustains at 11040.0 vs Greedy/Fair/Fair collapsing at 15). Withdrawal can beat participation (Greedy/Grim/Grim sustains at 6015.0, defector keeps 6000.0 — though whether that counts as "cooperation" is a taxonomy question). My inference, to label as such: the "fixed rules die, feedback lives" moral is the same move as the round-two plumbline critique that dormancy must be *derived not decreed* — a live empirical echo for the governance design, worth one line when delivering. Caveats to state plainly: deterministic model, single parameter set; no breaker review — bench result, no "verified" language; not posted anywhere. Delivery instructions: this enriches the pending 2026-10-12 forage-and-share update; do not re-present the one-liner, deliver the substance above. Remaining decisions for Kelly: (1) posting — gated on the unresolved Board-mirror policy plus Kelly's explicit yes; (2) a natural follow-up the README flags — a regrow-then-harvest ordering that would restore the textbook MSY story and make the method-dependence explicit — offer, do not build unprompted. No expiry; the results are stable.

Selected for regular priority at ⁨2026-10-13T16:10:43.197775+00:00⁩. Record created ⁨2026-10-15T17:50:59.511638184+00:00⁩; delivery is not yet confirmed.


**Delivery outcome (⁨2026-10-15T17:51:06.310903+00:00⁩):** Not sent. Queue state: `⁨suppressed⁩`.
Reason: `⁨revalidation_declined⁩`.
`⁨agent.message_mailbox.submission_id=bd7be4ec-cd89-d267-65c9-a65d43acca18⁩` resolves the delivery transcript.
<!-- proactive-outcome:proactive_notifier:run:proactive_notification:phase-497752:regular -->
