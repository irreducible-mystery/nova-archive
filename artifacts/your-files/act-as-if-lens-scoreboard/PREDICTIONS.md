# Lens-preserving scoreboard — pre-registered predictions

Written BEFORE any new numbers were computed for this scoreboard.
Source world: Marketplace VIII, M5 black-swan world verbatim (seed 99),
17 animals, run in `~/workspace/act-as-if/marketplace8_new_roles.py`.
No VIII original file is changed; per-round trajectories are recomputed
by an instrumented copy of that script (see README for the reproduction
check). This file was written before the instrumented run was executed,
so the predictions below are not fitted to the new numbers.

Known VIII summary numbers used as background (from the VIII README,
not from this scoreboard): Reactive sign #2 / priced last, Brier 0.432;
Diffusion swan accuracy 0.870 / priced rank 13; Short priced #1;
Underwriter sign #1; JEPA lived-rounds Brier 0.2195 over only 64 lived
rounds, all pre-swan; paraconsistent dead ~t=186, before the first swan.

## Claim A — Disagreement spikes around swans

Prediction: PASS if BOTH hold:
- (A1) Mean cross-animal spread of p (standard deviation across alive
  animals, per round) on swan rounds is at least 20% higher, relative,
  than the same mean on calm rounds.
- (A2) Mean spread in swan-onset windows (first 5 rounds of each swan
  window) is higher than the calm mean.
Why: lenses differ most when the regime breaks; in calm they mostly
track the same recent mean. If disagreement does NOT spike, then the
"lenses diverge at breaks" reading of the zoo is wrong, and disagreement
is just background noise.

## Claim B — Marginal contribution, not head-to-head rank

Prediction: PASS if BOTH hold:
- (B1) Leave-one-out on the Router pool (recompute Router's p from the
  recorded trajectories with one animal removed from its top-3 pool,
  holding all other animals' trajectories fixed, and re-score Router's
  priced wealth with the VIII calibration-lane formula) changes
  Router's priced wealth by at least 20 coins for at least one removed
  animal.
- (B2) Leave-one-out on a simple ensemble mean (mean p of alive animals
  per round, same rounds, holding trajectories fixed) changes ensemble
  Brier by at least 0.005 for at least one removed animal.
Why: if no single removal moves either quantity, then "contribution"
is a story, not a measurement, and the scoreboard should say so.
Note the holding-fixed caveat: this is a Router/ensemble-only ablation,
not a full market rerun — removing an animal from the whole market
would change the ecology (Router's p feeds Contrarian, Calibrator,
Mimetic, Stigmergic), so a full-ecology LOO would measure something
else. That distinction is recorded, not hidden.

## Claim C — Lifespan-matched Brier changes the calibration ranking

Prediction: PASS if BOTH hold:
- (C1) In the all-17 common-rounds Brier (rounds where every animal is
  still alive), JEPA is NOT in the top 3 — i.e. its lived-rounds #1
  standing (0.2195 over 64 pre-swan rounds) does not survive matching.
- (C2) The swan-weighted Brier ranking (swan rounds weighted 3x, calm
  1x, over each animal's lived rounds; animals with no swan rounds
  reported as "no swan rounds", not scored as 0) differs from the
  lived-rounds Brier ranking by at least one rank swap inside the top 5.
Why: VIII's own Finding 6 says the lived-rounds lane rewards dying
young in easy weather. If matching does not move the ranking, that
finding was overstated.

## Claim D — Per-regime breakdown inverts at least one standing

Prediction: PASS if at least one animal that is in the top half on
full-run Brier falls to the bottom half on swan-rounds Brier (lived
swan rounds only), OR at least one animal in the bottom half on
full-run Brier rises to the top half on swan-rounds Brier.
Animals with no lived swan rounds are reported as "—" and cannot count
toward either half of this claim (absence is not a score).
Why: a lens that is a good calm animal and a bad swan animal (or the
reverse) is exactly what a single full-run number hides.

## Claim E (secondary, not required for the scoreboard to be useful) — The ensemble is not a winner either

Prediction: the simple ensemble mean's Brier is better (lower) than
the median animal's lived-rounds Brier, but worse than the best
survivor's Brier. I.e. averaging helps over the typical lens and does
not beat the best lens — so the ensemble is a summary, not a new
winner to crown.
Why: if the ensemble beat every animal, the scoreboard would have
smuggled a winner back in through the back door.

## Scoring rule

Each claim A–D is scored PASS/FAIL exactly as written above, after the
analysis script runs. E is scored PASS/FAIL the same way but labelled
secondary. No claim is reworded after seeing the numbers; failures
stay failures in the README, with the numbers that failed them.
