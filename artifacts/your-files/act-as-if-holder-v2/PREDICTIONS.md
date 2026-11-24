# Holder v2 — pre-registered predictions

Written before any scored run. Thresholds are numeric so PASS/FAIL
is not a judgement call. Regimes: cooperation and coopetition are
the scored regimes; competition is a solo baseline. "v1" means the
v1 control re-run in this script (same world, same accounting).
v1's previous-run reference: Holder wealth about -475 to -495 in
cooperation/coopetition (gains about -675 to -695 from a 200 start),
last in all regimes.

- **P-A — v2-with-stipend survives and beats v1.** In BOTH
  cooperation and coopetition: V2S final wealth > 0 AND V2S final
  wealth > v1 final wealth in the same regime. Both halves
  required, both regimes required.
- **P-B — v2-without-stipend survives longer than v1 but does not
  beat it on wealth.** In BOTH regimes: V2N first round with
  wealth <= 0 is strictly later than v1's (or V2N never goes <= 0
  while v1 does), AND V2N final wealth <= v1 final wealth in the
  same regime. Both halves required, both regimes required.
- **P-C — post-flip value of v2 exceeds its calm value, and
  exceeds the fused baseline's post-flip value.** In BOTH regimes,
  for V2S and V2N separately: mean payoff per scored round in
  post-flip windows (centre+13 to centre+42) > mean payoff in calm
  rounds, AND > v1 control's post-flip mean payoff in the same
  regime. All four comparisons required (2 variants x 2 regimes
  for the calm half, and the same for the v1 half).
- **P-D — collapse fires on evidence more often than on expiry.**
  Across both regimes for V2S and V2N combined: number of
  evidence-triggered collapses > number of expiry-triggered
  collapses.
- **P-E — Router consultation of v2 rises in post-flip windows
  vs calm.** For V2S and V2N, in cooperation and coopetition
  separately: share of Router-as-proposer rounds in which Router
  invites Holder v2, in post-flip windows, is strictly greater
  than the same share in calm windows. All four comparisons
  required.

Score: number of predictions P-A..P-E passed, out of 5. Exit code
0 iff 5/5, else 1 (house convention).
