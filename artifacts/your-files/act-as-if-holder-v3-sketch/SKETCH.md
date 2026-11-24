# Holder v3 — SKETCH ONLY, NOT RUN, NOT BUILT

Drafted 2026-10-27 (Tuesday) as the sketch for the open fork left by
Holder v2: a flip-keyed collapse rule, or sit with the v2 result.
Nothing here has been run, no code has been written, nothing has
been posted to any repo. If Kelly picks this, the predictions below
are locked first, then — and only then — a run is built.

## Why v3 exists

Holder v2 (2026-10-27, local only) answered "what would a lens have
to be like for holding disagreement to actually pay?" with an
uncomfortable sharpening: it survived (+354.86 cooperation with
stipend, +325.01 coopetition, vs v1's -495.07 / -490.97) by almost
never holding — 847 of 850 scored rounds collapsed, 3 rounds in
holding state. The 0.03 trailing-50 Brier-gap collapse rule fired
instantly (minority Brier 0.5203 vs majority 0.2286; 136 evidence
collapses, 0 expiry collapses), so the stipend test was
uninformative (0.30 total paid — the entire with-vs-without
difference) and Router consulted Holder less after flips (33.3%)
than in calm (59.8%).

V3 changes exactly one thing — the collapse rule — so that the
question v2 failed to test can actually be tested: does holding
persist, and does the stipend then matter?

## What stays identical to v2 (comparability is the point)

- Same world: seed 20261026, 1,000 rounds, 150 warm-up, 850 scored,
  swan centres 336 / 550 / 820. NOT the M5 world.
- Same players: Reactive (triage, cost 0), Router (pairer, cost
  0.30, unchanged routing on trailing-50 accuracy), Holder.
- Same Holder portfolio: Majority M = trailing-100 mean clipped to
  [0.05, 0.95]; Minority m = extreme opposite (0.92 if M < 0.5,
  else 0.08); separate sub-accounts, never an averaged p.
- Same translation: m wins when the trailing-20 bias flips sign
  against the trailing-100 bias (flip rounds were 146 of 850 in v2).
- Same costs and stipend variants: carrying cost 0.05/round;
  V3S with a 0.10/round state stipend while holding, V3N without.
- Same return mechanic: after a collapse, return to holding.

## The one change: flip-keyed collapse

- DELETE the Brier-gap collapse rule entirely. Brier-evidence
  collapses are 0 by design in v3.
- Collapse only when the flip flag has been FALSE for N consecutive
  scored rounds — i.e. holding is for transition windows, and it
  ends when the world has been stable long enough that the minority
  condition has had no recent purchase.
- Primary N proposed: 25 rounds (matches v2's 25-round collapse
  clock, keeps the two runs comparable). Alternative Kelly may
  pick instead: N = 50. Do not run both unless she says so — the
  point is one clean test, not a sweep.
- On collapse, collapse to the better trailing-50 Brier claim for
  25 rounds, then return to holding (as in v2).

## Draft pre-registration (to be locked before any run)

- P-A (persistence): holding share far above v2's 0.4%, and
  concentrated in post-swan / post-flip windows rather than spread
  evenly. This is the test v2 could not run.
- P-B (stipend informativeness): total stipend paid far above
  v2's 0.30, and the V3S-minus-V3N wealth gap approximately equals
  the stipend total. If holding still does not persist, P-A fails
  and the stipend test is again uninformative — say so, don't
  rescue it.
- P-C (no Brier collapse): evidence collapses = 0, by construction.
- P-D (routing, unchanged): Router consultation of Holder still
  lower post-flip than in calm, because routing is still
  trailing-50 accuracy. V3 does NOT fix routing; bundling a Router
  fix would confound the collapse-rule test. That fix stays a
  separate next step.
- P-E (wealth, honest direction): v3 finishes BELOW v2 on wealth
  (+354.86 / +325.01), because it actually holds the minority
  longer — and the minority still lost in v2 even on its own flip
  rounds (-0.155 on flip rounds vs -1.543 off them). Persistence
  and profitability are separate verdicts: a v3 that holds a lot
  and finishes below v2 is a successful persistence test and a
  failed profitability test, not a contradiction.

## Deliberately NOT bundled

- A minority claim calibrated to flip rounds (rather than the
  extreme 0.92/0.08). That is a different variable; bundling it
  would leave it unclear whether any change came from the collapse
  rule or from a better minority.
- A Router that consults on disagreement or post-flip value.
  Separate step, for the same reason.
- The still-unbuilt Translator pairing.

## Kelly's decisions (any, all, or none — sitting is a valid answer)

1. Build v3 as sketched (N = 25), or with N = 50 instead?
2. Or sit with the v2 result for now — the sketch stays here,
   unrun, until she picks it up.
3. Nothing is run, coded, or posted until she picks 1.
