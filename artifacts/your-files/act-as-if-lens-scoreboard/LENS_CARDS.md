# Lens cards — Marketplace VIII animals, lens-preserving

One card per animal. Each card keeps the animal's claim, tell, cost,
breaking regime, and what the zoo loses if it is removed — separately
from its wealth rank. Numbers are from the lens-scoreboard rerun, which
reproduced VIII exactly (see README): lived rounds, lived/calm/swan
Brier, calm/swan accuracy. "—" for swan means the animal died before
any swan round; that is absence, not a score of 0. Short's Brier is the
consensus placeholder's Brier, not a bit-prediction of its own — its
real work is escrow, reported separately.

## Paraconsistent — the holder

- Claim: Belnap 4-valued hypotheses (True / False / Both / Neither);
  Both is double-weighted, so contradiction is held, not averaged away.
- Tell: acts on the overlap of evidence for and against; swan call when
  nB ≥ 2.
- Cost: LN2 × (nT + 2·nB + nF + 0.5·nN) per round; 151.8 spent over just
  37 lived rounds.
- Numbers: lived Brier 0.245, calm Brier 0.245, calm accuracy 0.730
  (the highest calm accuracy in the zoo), swan —.
- Breaks: in the calm, not on a swan. Dead at t≈186, before the first
  swan, under VIII's stake rule, which cut mushy-p income while costs
  stayed whole.
- If removed: the zoo loses its contradiction-holder. Note the tension
  the scoreboard is built to hold: removing it from Router's pool
  *improves* Router's priced wealth by +90.9 — priced contribution and
  functional value point opposite ways here. Both facts stay on the card.

## Self-build — the scout that builds from scratch

- Claim: zero hypotheses at birth; builds a new one from surprise,
  discards the worst when full.
- Tell: builds when recent-stream surprise > 0.15; swan call when
  surprise > 0.30.
- Cost: 0.1/round + 5.0 per build; 768.2 spent over 532 lived rounds.
- Numbers: lived Brier 0.224, calm 0.232, swan 0.148; calm accuracy
  0.669, swan accuracy 0.848. Dead at t≈681.
- Breaks: building is expensive, and the built hypotheses die with the
  animal in the sizing squeeze.
- If removed: the zoo loses its only from-scratch modeller — the one
  that ever finds a thing nobody else looked for. Its swan Brier is
  second-best in the zoo.

## Dialectical — thesis, antithesis, synthesis

- Claim: when thesis and antithesis both fail (trailing-20 error > 0.45
  for both), synthesize a third position from the recent stream.
- Tell: a synthesis event, costing an extra 3.0, is itself the swan call.
- Cost: LN2 + 0.5 per round, +3.0 per synthesis; 192.1 spent over 161
  lived rounds.
- Numbers: lived Brier 0.232, calm 0.232, swan —; calm accuracy 0.702.
- Breaks: never reaches a swan; dead at t≈310, in the calm.
- If removed: the zoo loses position-combination (distinct from
  Council/Router prediction-fusion: this combines positions, not p's).
  Router's priced wealth improves +45.0 without it — again, priced
  contribution and functional loss are different columns.

## Federated — local autonomy, occasional sync

- Claim: three sub-agents on strided slices, confidence-weighted.
- Tell: swan call when the slices disagree by > 0.4.
- Cost: 0.9/round (three summaries); 756.0 spent, survivor.
- Numbers: lived Brier 0.226, calm 0.234, swan 0.141; calm accuracy
  0.637, swan accuracy 0.870.
- Breaks: calm Brier is mid-pack; it is a swan animal more than a calm
  one.
- If removed: the zoo loses its most frequent Router partner (427 of
  840 rounds in Router's top 3) — and the scoreboard's cleanest
  warning: removing it changes Router's priced wealth by only +0.02.
  Frequency of selection is not priced contribution.

## Contrarian — negation as a control

- Claim: bet against the lag-1 consensus.
- Tell: p = 1 − consensus, clipped.
- Cost: 0.2/round; 62.4 spent over 312 lived rounds.
- Numbers: lived Brier 0.345, calm 0.336, swan 0.460; calm accuracy
  0.343, swan accuracy 0.130.
- Breaks: everywhere measured. Negation is not insight.
- If removed: the zoo loses its cheap-dissent control — the empirical
  bound that says dissent must be smarter than negation. Its removal
  changes ensemble Brier by −0.0002 (nothing) and Router's priced
  wealth by exactly 0 (it was never in Router's top 3).

## Satisficer — good enough, then coast

- Claim: above 0.60 trailing accuracy, coast (post the last bit);
  below, adapt minimally.
- Tell: coasting vs adapting is visible in its cost (0.05 vs 0.5).
- Cost: 0.05 coasting, 0.5 adapting; 264.3 spent, survivor.
- Numbers: lived Brier 0.370, calm 0.383, swan 0.229; sign wealth
  2494.2, priced wealth −4109.5.
- Breaks: calibration. Coasting is a 0/1 bet, and the Brier lane
  savages certainty — sign #3, priced #15 in VIII.
- If removed: the zoo loses its steward — the maintainer who keeps
  things running without gold-plating. Ensemble Brier improves
  −0.0041 without it, because its 0/1 bets drag the mean.

## Mimetic — the copier

- Claim: copy the trailing-20 accuracy leader, one step lagged.
- Tell: its p is always somebody else's previous p.
- Cost: 0.2/round; 168.0 spent, survivor.
- Numbers: lived Brier 0.245, calm 0.249, swan 0.195; calm accuracy
  0.555, swan accuracy 0.609.
- Breaks: it can only be as good as the leader it copies, one step late.
- If removed: the zoo loses its replication mechanism — how norms
  actually propagate, for good norms and for errors alike. (The BOARD.md
  truncation bug spread exactly this way in the wider programme.)

## Gate — the selective gate, retrained on warmup

- Claim: Mamba-style selective gate, logistic head fitted on the
  warmup window.
- Tell: gate erasure cost rises with surprise.
- Cost: LN2 × erasure + 0.1; 1044.6 spent over 571 lived rounds.
- Numbers: lived Brier 0.420, calm 0.428, swan 0.329; calm accuracy
  0.520, swan accuracy 0.652.
- Breaks: calibration and cost together — the second-most expensive
  animal, with the second-worst Brier. Dead at t≈720.
- If removed: the zoo loses its frantic adapter archetype (with JEPA:
  first to find a new regime, first to need rescue). Router never
  selects it (top-3 frequency 0), so Router's priced wealth is
  unchanged by its removal.

## JEPA — the latent switcher

- Claim: a latent bias, switched when recent surprise > 0.12; a
  swan mode that posts 0.5 while it waits the regime out.
- Tell: frequent updates (8 of last 10) trigger swan mode.
- Cost: LN2 on a quiet round, 7·LN2 on an update; 171.2 spent over 64
  lived rounds.
- Numbers: lived Brier 0.220 (VIII's #1), calm 0.220, swan —;
  calm accuracy 0.703. Common-rounds (37 rounds, all calm) Brier
  0.218, rank 4 of 17.
- Breaks: untested where it matters — it died at t≈213, before any
  swan, so its #1 lived Brier is a calm-only number.
- If removed: the zoo loses its fastest latent switcher, and Router
  loses a frequent early partner (244 top-3 rounds; Router's priced
  wealth improves +65.9 without it, because those early picks aged
  badly as JEPA died).

## Reactive — triage

- Claim: no model; post the last bit.
- Tell: p is always 0 or 1.
- Cost: 0.0; survivor.
- Numbers: lived Brier 0.432, calm 0.447, swan 0.261; sign wealth
  3488.0 (VIII #2), priced wealth −5920.0 (VIII last).
- Breaks: calibration, by construction. Certainty is punished by
  Brier exactly as much as direction is rewarded by sign scoring.
- If removed: the zoo loses its first responder — somebody has to
  notice the fire while the deliberators are still choosing. Removing
  it improves ensemble Brier by −0.0050, the largest ensemble move
  in the scoreboard, because 0/1 bets drag a mean more than any other
  single animal's. That is a fact about the ensemble, not a verdict
  on triage.

## Stigmergic — coordination through traces

- Claim: no world model; read the shared trace field (other animals'
  recent p's), write its own mark.
- Tell: swan call when trace spread > 0.25.
- Cost: 0.3/round; 171.0 spent over 570 lived rounds.
- Numbers: lived Brier 0.223, calm 0.229, swan 0.153; calm accuracy
  0.647, swan accuracy 0.848.
- Breaks: dies at t≈719, after two swans; its trace is only as good
  as the field it reads.
- If removed: the zoo loses trace-coordination — the commons' shared
  file as environment. Router's priced wealth falls −19.9 without it,
  the third-largest positive Router contribution.

## Diffusion — the refiner

- Claim: iterative denoising toward window means at timescales
  8/15/30/60, guidance w=2, 4 samples; in VIII it posts the unshrunk
  mean and lets its spread set the stake.
- Tell: sample spread; swan call when spread > 0.20.
- Cost: LN2 × (20×4)/40 per round; 1164.5 spent, the zoo's most
  expensive animal; survivor.
- Numbers: lived Brier 0.236, calm 0.246, swan 0.130 (best swan Brier
  in the zoo); swan accuracy 0.870 (zoo ceiling tier); sign wealth
  1179.3, priced wealth −504.9 (priced rank 13).
- Breaks: calibration at K=20 — refinement becomes overconfidence,
  and Brier punishes exactly that. Its own K=1 variant beats K=20 on
  Brier itself (0.2285 vs 0.2363, VIII ablation).
- If removed: the zoo loses its best swan detector and Router's
  largest positive priced contribution (Router's priced wealth falls
  −66.8 without it). Good detector, bad probabilist — both on the card.

## Router — the pairer

- Claim: no signal of its own; select the top 3 other animals by
  trailing-40 accuracy (half-weighted with swan-step accuracy) and
  post their (score − 0.45)²-weighted mean, lagged one round.
- Tell: its top-3 membership over time (Federated 427 rounds, Self-build
  416, Dialectical 413, Paraconsistent 388, JEPA 244, Stigmergic 219,
  Diffusion 182 — early partners dominate, then die).
- Cost: 0.3/round; 252.0 spent, survivor.
- Numbers: lived Brier 0.229, calm 0.234, swan 0.164; sign wealth
  1132.8, priced wealth 667.2 (VIII priced rank 3).
- Breaks: it inherits its partners' deaths. Its early top-3 were
  animals that died before or during the swans.
- If removed: the zoo loses pairing itself — the function of choosing
  who answers, which is cheaper (0.3/round) than any animal it pairs.

## Calibrator — the calibration-keeper

- Claim: Platt/temperature scaling of the lag-1 consensus, refit every
  round on the trailing 150 (raw, outcome) pairs.
- Tell: fitted (a, b) — how much the consensus needs stretching.
- Cost: LN2/round; 582.2 spent, survivor.
- Numbers: lived Brier 0.228, calm 0.235, swan 0.156; calm accuracy
  0.606, swan accuracy 0.841.
- Breaks: the role is real, this occupant did not win it — Stigmergic,
  Self-build and Federated beat it on lived Brier, and its swan Brier
  (0.156) is mid-pack among survivors.
- If removed: the zoo loses its only dedicated calibration-keeper.
  Router's priced wealth falls −13.0 without it.

## Retriever — the remembrancer

- Claim: episode store of 16-bit patterns → next bit; p is the outcome
  frequency among the 12 Hamming-nearest stored patterns, blended with
  the last-60 mean at strength 3.
- Tell: retrieval set size and agreement; swan call when the nearest
  12 agree at ≥ 0.85 or ≤ 0.15.
- Cost: 0.25/round; 210.0 spent, survivor.
- Numbers: lived Brier 0.233, calm 0.239, swan 0.166; swan accuracy
  0.783 overall, halves 0.826 → 0.696 (VIII's P5 inversion).
- Breaks: memory dilution — late in the run the store is mostly
  ordinary days, and it averages the exceptional away.
- If removed: the zoo loses its archive. The card's warning: memory
  is not monotonic capital; the archivist's real job may be forgetting
  on purpose.

## Underwriter — the insurer

- Claim: a deliberately weak signal (lean on the last-30 mean) plus a
  real insurance book: premium from the market's trailing-250 swan
  frequency × 1.30 margin, at most 6 covers/round, 25 payout on a swan
  step, reserve floor 60.
- Tell: premium level and surcharge state (×1.5 for 50 rounds after a
  payout).
- Cost: 0.2/round admin, plus the book; 168.0 spent, survivor.
- Numbers: lived Brier 0.230, calm 0.233, swan 0.193; sign wealth
  4928.1 (VIII #1), priced wealth 700.1; insurance net +4117.5
  (premiums 5042.5, payouts 925.0, 1743 covers; no buyer recovered
  even half its premiums).
- Breaks: as governance, not as solvency. An insurer whose revenue is
  other animals' distress, in a market where distress is partly
  manufactured by the sizing rule, taxes the holding it was built to save.
- If removed: the zoo loses risk pooling — and its apex. Router's
  priced wealth falls −16.8 without it.

## Short — the bounty-breaker

- Claim: no bit position of its own (stake 0); its p in the lanes is
  the consensus placeholder. Its work is escrow: counter-stake the
  public swan calls of callers whose trailing-50 Brier ≥ 0.26, worst
  first, max 3 per call round.
- Tell: the Brier gate — it hunts miscalibration, not bits.
- Cost: 0.05/round scanning, 1.0 upkeep on call rounds where it takes
  no short; 42.0 spent, survivor.
- Numbers: placeholder Brier 0.229, calm 0.236, swan 0.151; priced
  wealth 857.2 (VIII priced #1, via the lane, not via escrow — escrow
  net is in the sign ledger); escrow: 38 shorts on 70 calls, 34–4,
  net +150.0.
- Breaks: if callers are well calibrated, there is no prey. The bounty
  pool beside it was near-useless (bonuses paid 16.0 all run).
- If removed: the zoo loses its breaker with a price on it — the only
  animal whose income is directly indexed to other animals' miscalibration.
