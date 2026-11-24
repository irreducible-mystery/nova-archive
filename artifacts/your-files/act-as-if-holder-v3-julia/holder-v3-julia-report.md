# Holder v3 in Julia — scored report

Date: 2026-10-27. Local only, nothing posted to any repo or
external surface. No next version built from this result; the
result is returned for Kelly's decision on the next design step.
The Python v3 run is not modified.

## What this is

A Julia port of the Python Holder v3, run on the same world as
Holder v2/v3. Holder v3's one change from v2: the 0.03 trailing-50
Brier-gap collapse rule is deleted; collapse happens only after
the flip flag (trailing-20 bias flips sign vs trailing-100 bias)
has been false for N = 25 consecutive scored rounds in holding
state. On collapse, collapse to the better trailing-50 Brier
claim for 25 rounds, then return to holding. Portfolio stakes
0.5/0.5, carrying cost 0.05/round, stipend variants 0.10/round
while holding. Reactive (triage) and Router (pairer, trailing-50
accuracy) unchanged. 1,000 rounds, 150 warm-up, 850 scored,
swan centres 336/550/820, biases 0.92/0.08/0.92.

## Method note — how "same world" was achieved honestly

Julia's random-number generator is not NumPy's, so regenerating
the world in Julia would not have produced the same bit stream.
Instead, the Python world generator (seed 20261026) was run once
to export the 1,000 bits to `bits.txt` in this folder, and the
Julia port reads those bits. The game logic, payoff formula,
proposer rotation, invitation, defection, and collapse rules
are ported from `holder_v3.py` in the same order. That is the
same world, carried over, not a new world that happens to
share a seed number.

## Predictions (written before any Julia run)

Copied from the Julia predictions file, which adopts the Python
v3 predictions unchanged:

- P-A: V3S holding share > 20% in both cooperation and
  coopetition, AND postflip holding share ≥ calm share + 10
  points in both regimes.
- P-B: V3S stipend total > 10.00 in both regimes, AND
  |(V3S wealth − V3N wealth) − stipend| ≤ 1.00 in both regimes.
- P-C: Brier-gap collapses = 0, every collapse trigger
  flip_stale.
- P-D: Router consultation postflip < calm, both variants,
  both coalition regimes.
- P-E: V3S wealth < 354.86 (cooperation) and < 325.01
  (coopetition) — the v2 V2S wealths.

## Scored outcomes — 4/5 (exit 1, house convention)

- **P-A FAIL — on the concentration clause only.** Holding
  share 525/850 = 61.8% in both regimes (share clause passes
  easily, vs v2's 3/850 = 0.4%), but holding is uniform, not
  concentrated post-flip: calm 62.2%, swan 56.0%, postflip
  63.3%. Postflip exceeds calm by 1.1 points, not ≥ 10.
  Holding by kind: calm 426/685, swan 42/75, postflip 57/90.
- **P-B PASS.** Stipend total 52.50 in both regimes (vs v2's
  0.30); V3S−V3N wealth gap exactly 52.50 in both regimes
  (176.84 − 124.34 = 52.50 cooperation; 123.67 − 71.17 =
  52.50 coopetition). The stipend test is informative here.
- **P-C PASS.** Brier-gap collapses = 0. Collapses: 13 per
  variant per regime (78 total across 2 variants × 3
  regimes), all flip_stale, all winner M, 0 expiry. The
  Brier-gap branch does not exist in the Julia code either.
- **P-D PASS.** Router consultation postflip 33.3% vs calm
  59.8% (swan 41.7%), for both variants in both coalition
  regimes, attempts postflip 30 (10 invites), calm 229
  (137 invites). Routing is unchanged, and it still routes
  away exactly when disagreement is most informative.
- **P-E PASS.** V3S wealth 176.84 (cooperation), 123.67
  (coopetition), 36.01 (competition) — all below v2's
  354.86 / 325.01. V3N: 124.34 / 71.17 / −16.49
  (competition negative). Persistence and profitability
  stay separate verdicts: holding a lot, finishing below v2.

## Holding duration and collapse events

- Holding rounds: 525 of 850 scored rounds in every
  variant/regime run (the collapse clock is regime-independent
  in this design — collapse timing depends only on the flip
  flag and the holding state, which the regime does not
  change; wealth differs by regime, holding does not).
- Collapsed rounds: 325 of 850.
- Collapse events: 13 per variant per regime, each a
  25-round collapse to the majority claim M (trailing-50
  Brier winner in every case), then return to holding.
  No collapse fired on a Brier gap, none on expiry.
- Flip rounds: 146 of 850 scored rounds. Minority claim
  mean payoff on flip rounds −0.1549, off-flip −1.5431
  (the v2 finding, reproduced exactly — the minority still
  loses even on its own flip rounds, just less badly).
- Control (v1, re-run in Julia on the same bits): Holder
  wealth −495.07 (cooperation), −490.97 (coopetition),
  −474.53 (competition); first negative at round 397
  (cooperation/competition) and 393 (coopetition); mean
  payoff excl. stipend −0.8177 / −0.8129 / −0.7936;
  Brier M 0.2286, m 0.5203 — the v2 baseline's control
  numbers, reproduced.

## Flip-round results

The flip-round question is what v3 was built to test, and
the Julia port answers it the same way Python v3 did:
holding survives through flips (holding is not
concentrated post-flip, it is uniform — the flip-stale
rule fires only in long stable stretches, and flips
reset the false streak, so holding persists across
transition windows without being confined to them),
but the minority claim it holds is still a losing claim
on flip rounds (−0.1549). That is why P-A's
concentration clause fails and P-E passes together:
v3 solved persistence, not profitability. The next
variables, recorded in Python v3 and not built here,
remain: a minority claim calibrated to flip rounds,
and a Router that consults on disagreement rather
than trailing accuracy.

## Python v3 vs Julia v3 — direct comparison

| Measure | Python v3 | Julia v3 | Match? |
|---|---|---|---|
| Holding rounds / share | 525 / 61.8% | 525 / 61.8% | Exact |
| Holding by kind (calm/swan/postflip) | 62.2% / 56.0% / 63.3% | 62.2% / 56.0% / 63.3% | Exact |
| Collapses per variant per regime | 13, all flip-stale | 13, all flip-stale | Exact |
| V3S wealth coop/coopet/comp | 176.84 / 123.67 / 36.01 | 176.84 / 123.67 / 36.01 | To 2 decimals |
| V3N wealth competition | −16.49 | −16.49 | Exact |
| Stipend total | 52.50 | 52.50 | Exact |
| Router consultation postflip/calm | 33.3% / 59.8% | 33.3% / 59.8% | Exact |
| Score | 4/5 (P-A FAIL, concentration only) | 4/5 (P-A FAIL, concentration only) | Exact |

Floating-point wealth values agree to the second decimal
shown; the Julia run's unrounded V3S wealths are
176.8377 (cooperation) and 123.6748 (coopetition), matching
Python's 176.8377 / 123.6748. Integer counts (holding
rounds, collapses, flip rounds, attempts, invites) agree
exactly — any divergence there would have been a port
bug, and there is none.

## Files in this folder

- `holder_v3.jl` — the Julia port (run from this folder)
- `bits.txt` — the 1,000-bit world, exported from the
  Python generator (seed 20261026)
- `output.txt` — the full Julia run output (all 9 runs:
  v3_stipend, v3_nostipend, v1 × cooperation, coopetition,
  competition), re-run twice with identical output
- This report

## Limits

- The port proves the Python v3 result is not a
  Python artefact; it does not independently confirm it
  in the independence-map sense — same world, same
  author, same design, same predictions. Count it as a
  cross-language reproduction, not a second experiment.
- The v2 wealth constants in P-E (354.86 / 325.01) are
  taken from the Python v2 record, not re-derived here.
- N = 50 was not run, per the Python v3 choice (N = 25
  only, no sweep).
