# Lens-preserving scoreboard — Marketplace VIII, re-read without a winner

Local only. Nothing here is posted to any repo, nothing is merged, and
no single winner is declared. The point of this scoreboard is the one
Kelly asked for: the same 17 animals, on the same M5 black-swan world
(seed 99, swans at 336/550/820, 840 scored rounds t=150..989), read as
different lenses on the same game, with their disagreements and their
marginal contributions kept visible instead of collapsed into a rank.

## What was done, and what was not

- `PREDICTIONS.md` was written BEFORE any new number was computed.
- The VIII market was then re-run once through an instrumented copy,
  `marketplace8_instrumented.py` (logic unchanged, recording only:
  per-round p for every animal, Router's scores and top-3 per round).
  No VIII original file was changed.
- The analysis, `lens_scoreboard.py`, computes only lens-preserving
  quantities from those trajectories. Its full output is
  `lens_scoreboard_output.txt`; its machine-readable numbers are
  `lens_scoreboard_results.json`. Every number in this README comes
  from that output.
- This is a RE-ANALYSIS of the VIII run, not a new run — except for
  the two leave-one-out replays, which are post-hoc recomputations
  with trajectories held fixed (see Limits). No new world, no new
  animals, no new market rules.

## Reproduction check (must pass before anything else is believed)

The instrumented rerun reproduces VIII's saved results exactly, to the
tenth of a coin / fourth decimal of Brier, for all 17 animals
(wealth, priced wealth, lived-rounds Brier recomputed from the recorded
p trajectories). Overlap numbers verified against the VIII README table:

- Reactive: sign wealth 3488.0 (VIII #2), priced wealth −5920.0
  (VIII last), lived Brier 0.4321. ✓
- Diffusion: swan accuracy 0.870, priced wealth −504.9 (VIII priced
  rank 13). ✓
- Short: priced wealth 857.2 (VIII priced #1); escrow net +150.0,
  38 shorts on 70 calls, 34–4. ✓
- Underwriter: sign wealth 4928.1 (VIII #1); insurance net +4117.5
  (premiums 5042.5, payouts 925.0). ✓
- JEPA: lived Brier 0.2195 — over 64 lived rounds, all calm, dead at
  t≈213 before any swan. ✓ (This is the number the rest of the
  scoreboard interrogates.)

Deaths, for reference: paraconsistent 37 lived rounds (dead t≈186),
JEPA 64 (t≈213), dialectical 161 (t≈310), contrarian 312 (t≈461),
selfbuild 532 (t≈681), stigmergic 570 (t≈719), gate 571 (t≈720).
Ten animals survive the full 840 rounds. The alive pool thins from 15
signal animals at t=200 to 9 at t=850 — every "over time" number below
is read against that thinning.

## Pre-registered score: 2 of 4 required claims PASS (plus secondary E: FAIL)

### Claim A — Disagreement spikes around swans: FAIL

- Calm mean spread (std of p across alive signal animals): 0.2011
  (771 rounds).
- Swan mean spread: 0.1890 (69 rounds) — 6.0% LOWER than calm, not
  20% higher as predicted.
- Swan-onset mean spread (first 5 rounds of each swan): 0.1863 —
  7.4% lower than calm.
- By segment: first swan 0.2106 (only +4.8% over calm), second 0.1851,
  third 0.1712.
- The claim fails as written, and the failure is informative (see
  below). It is not reworded.

### Claim B — Marginal contribution: FAIL (B1 passes, B2 fails; both were required)

- B1, Router leave-one-out (replay Router's (score−0.45)² top-3 rule
  with one animal removed from the pool, other trajectories fixed,
  re-score Router's priced wealth with the VIII lane formula;
  recomputed base 667.2 = VIII original 667.2 exactly):
  - Biggest POSITIVE contributions to Router (priced wealth falls
    without them): Diffusion −66.8, Stigmergic −19.9, Underwriter
    −16.8, Calibrator −13.0.
  - Biggest NEGATIVE contributions (priced wealth RISES without
    them): Paraconsistent +90.9, JEPA +65.9, Dialectical +45.0.
  - Near-zero: Federated +0.02 despite being Router's most frequent
    partner (427 of 840 rounds in the top 3) — frequency is not
    priced contribution. Contrarian, Gate, Reactive: exactly 0.0,
    because they were never in Router's top 3; Satisficer appears
    once in the top-3 counts with no measurable priced effect.
  - B1 threshold (≥20 coins for at least one removal) is met several
    times over. B1: PASS.
- B2, ensemble-mean leave-one-out (mean p of alive signal animals;
  base ensemble Brier 0.2320):
  - Largest moves: removing Reactive improves ensemble Brier by
    −0.0050 (precisely −0.00499), removing Satisficer by −0.0041,
    removing Diffusion worsens it by +0.0025, Calibrator +0.0022.
  - B2 threshold was ≥0.005 for at least one removal. The largest
    move is 0.00499 — it misses by 0.00001. B2: FAIL, by a hair, and
    that hair is itself a finding: the ensemble is robust to any
    single lens in a way Router is not.
- Claim B overall: FAIL.

### Claim C — Lifespan-matched Brier changes the ranking: PASS

- All-17 common rounds: only 37 rounds (t=150..186, all calm, before
  the first death). On those rounds JEPA's Brier is 0.2178 — slightly
  better than its lived 0.2195 — but its rank falls to 4th, behind
  Federated (0.2031), Diffusion (0.2114) and Stigmergic (0.2176, ahead
  of JEPA by 0.0003). C1 (JEPA not top 3 in common rounds): PASS,
  by three ten-thousandths, on a 37-round window. The narrowness is
  part of the result, not a footnote to hide.
- Swan-weighted Brier (swan rounds ×3, calm ×1; animals with no swan
  rounds — paraconsistent, dialectical, JEPA — reported as "no swan
  rounds", not 0): top 5 becomes Stigmergic, Self-build, Federated,
  Calibrator, Short, vs lived top 5 JEPA, Stigmergic, Self-build,
  Federated, Calibrator. Multiple swaps inside the top 5. C2: PASS.
- Caveat that travels with the pass: the all-17 common window is
  calm-only, so it cannot rank swan performance at all — it ranks
  early-calm performance. Lifespan-matching and swan-weighting answer
  different questions, and neither alone is "the" calibration ranking.

### Claim D — Per-regime breakdown inverts a standing: PASS

- Full-run Brier rank 11 Diffusion (0.236) has the BEST swan Brier in
  the zoo (0.130, swan accuracy 0.870). Full-run rank 3 Self-build
  (0.224) has swan Brier 0.148, second-best. Full-run rank 2
  Stigmergic (0.223) has swan Brier 0.153.
- Conversely, full-run #1 JEPA, #9 Dialectical and #13 Paraconsistent
  have no swan rounds at all — their full-run standings say nothing
  about swans.
- At least one bottom-half animal rising to the top half on swans:
  Diffusion, and Retriever (full rank 10 → swan Brier 0.166, 8th of
  14 swan-tested animals). D: PASS.

### Claim E (secondary) — The ensemble is not a winner either: FAIL

- Ensemble Brier 0.2320 vs median animal's lived Brier 0.2317
  (Dialectical): the ensemble is slightly WORSE than the median
  animal, not better as predicted. It is also worse than the best
  survivor's Brier (Federated 0.2264), which is the half of E that
  held. E: FAIL on its first half. The ensemble is a summary, not a
  winner — but not even a better-than-median summary here, because
  the 0/1 animals (Reactive, Satisficer, Gate) drag the mean.

## Headline findings (all from the script output)

1. **Disagreement does not spike ON swans — it spikes AFTER them.**
   Exploratory (not pre-registered) split, same trajectories: mean
   spread in the 30 rounds after each swan (0.2420, 0.2141, 0.2273)
   exceeds both the swan windows themselves (0.2106, 0.1851, 0.1712)
   and the 30 rounds before them (0.2205, 0.1907, 0.2012). The
   reading that fits: swan regimes are extreme (0.92/0.08), so the
   surviving lenses converge on the extreme p while the swan lasts;
   calm regimes (0.25/0.50/0.75) and regime switches keep lenses
   apart, and readjustment after a swan re-opens the disagreement.
   Disagreement here is a lag / readjustment signal, not a
   contemporaneous swan detector. Claim A's failure is what revealed
   this — averaging the disagreement away would have hidden it twice.
2. **The biggest Router contributors are negative.** Router's priced
   wealth improves most by REMOVING its early partners
   (Paraconsistent +90.9, JEPA +65.9, Dialectical +45.0) — animals
   that were in its top 3 early (388, 244, 413 rounds) and then died.
   Its biggest positive contributor is Diffusion (−66.8). A lens can
   be frequently selected, early-selected, and still be a priced
   liability. Selection frequency, priced contribution, and functional
   value are three different columns; the cards keep them separate.
3. **Lifespan-matching dethrones JEPA, but only just — and only on
   calm.** VIII's Finding 6 (the lane rewards dying young in easy
   weather) survives in direction but not in drama: JEPA falls from
   #1 to #4 on common rounds, by 0.0003, on a 37-round calm-only
   window. The stronger lifespan correction is the swan-weighted
   ranking, which drops the three no-swan animals out of the ranking
   entirely instead of pretending their calm numbers compare.
4. **Per-regime, the zoo inverts.** Diffusion is a bad probabilist
   overall (Brier 0.236, priced rank 13) and the best swan probabilist
   (swan Brier 0.130). Reactive is the mirror: sign #2, priced last,
   calm Brier 0.447, swan Brier 0.261. A single full-run number cannot
   hold both halves of either animal. This is the scoreboard's
   central result: the lenses differ by regime, and regime is where
   their differences live.
5. **The ensemble is fragile to 0/1 bets, robust to single lenses.**
   No single removal moves ensemble Brier by 0.005 (max 0.00499), yet
   the ensemble as a whole is worse than the median animal because
   three 0/1-ish animals drag every round's mean. Robustness to
   removal and goodness of the mean are different properties.

## Lens cards

`LENS_CARDS.md` — one card per animal (all 17): claim, tell, cost,
breaking regime, and what the zoo loses if it is removed. No card
declares a winner; several cards record priced contribution and
functional value pointing opposite ways, on purpose.

## Honest limits

- Re-analysis, not a new run: the world, the animals, and the market
  rules are VIII's. Nothing here tests whether these findings survive
  a different seed, a different swan schedule, or a different venue.
- Leave-one-out is post-hoc with trajectories held fixed. Removing an
  animal from the whole VIII market would change the ecology (Router's
  p feeds Contrarian's consensus, Calibrator's raw, Mimetic's leader
  choice, Stigmergic's trace field), so a full-ecology LOO would
  measure a different, larger effect. The numbers here are the
  Router-only and ensemble-only effects, labelled as such.
- The all-17 common-rounds window is 37 rounds, all calm. It is
  reported because the pre-registration required it, not because it
  is a good ranking window — a 37-round calm ranking should not be
  quoted without that sentence attached.
- Swan-weighted Brier uses weight 3×, chosen in the pre-registration
  before seeing the numbers. A different weight would move the
  ranking; the weight is a floor choice, and it is stated here so it
  can be contested.
- Short's Brier is its consensus placeholder's Brier. Its real
  performance is escrow (34–4, +150), which lives in the sign ledger,
  not in any Brier column. Scoring Short on Brier alone would be a
  category error the scoreboard refuses.
- Animals that died before a swan have no swan Brier. They are shown
  as "—", never as 0.000 (the empty-set default in VIII's raw output
  was a trap this scoreboard explicitly avoids).
- Determinism: the instrumented rerun reproduced VIII to the tenth of
  a coin on every animal, so the trajectories are the VIII
  trajectories, not a near miss. Re-running `lens_scoreboard.py`
  reproduces this README's numbers.
