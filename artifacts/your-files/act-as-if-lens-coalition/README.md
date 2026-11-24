# Lens Coalition Game — results

**Pre-registered score: 2/6 PASS. Exit code 1, per house convention —
failures are findings, not errors.**

Files: `DESIGN.md` (game design, written first), `PREDICTIONS.md`
(written before the scored run, unedited afterwards),
`lens_coalition.py` (the game), `results.json`, `output.txt`.
Local only: nothing posted to GitHub, nothing merged.

World: a NEW bit-stream world, seed 20261026, 1,000 rounds (150
warm-up, 850 scored), swan centres 336/550/820 with biases
0.92/0.08/0.92. This is NOT the M5 world verbatim — same swan-timing
idea, fresh bits.

## Rules in plain language

Three players, each a different lens on the same next bit:

- **Reactive (triage):** bets the last bit, confidently (0.85 / 0.15).
  Costs nothing. Fast, no memory.
- **Holder (minority report):** keeps two claims — a majority claim
  (trailing-100 mean) and an extreme minority claim (0.92 if the
  majority is below 0.5, else 0.08) — and acts on their mean. Costs
  0.40 per round to hold both.
- **Router (pairer):** has no signal of its own; posts the mean of
  the other two lenses' previous-round probabilities. Costs 0.30.

Each round the proposer rotates. The proposer invites the partner
with the best trailing-50 solo accuracy; the partner accepts unless
the proposer is more than 0.05 worse. Holder proposes PRESERVE
coalitions (both claims stay on the record, +0.25 bonus each if the
members' probabilities differ by at least 0.20); Reactive and Router
propose FUSE coalitions (only the mean is the joint record, no
bonus). Payoff per round: +1/−1 for direction, plus a calibration
bonus 4×(0.25 − Brier), minus the lens's own cost, minus a
coordination cost (0.05 cooperation, 0.15 coopetition). Wealth
starts at 200.

Three regimes, same world, separate runs:

- **Cooperation:** coalitions allowed, no defection.
- **Competition:** no coalitions, everyone solo.
- **Coopetition:** coalitions allowed; a member defects if the
  coalition mean's sign contradicts its own solo sign. The defector
  takes its solo payoff; the betrayed partner takes solo minus 0.20.
  The hypothetical coalition payoff is recorded, so breaking can be
  scored against its counterfactual.

## Predictions vs outcomes (2/6)

| # | Prediction | Outcome | Verdict |
|---|---|---|---|
| P1 | Total payoff: cooperation > coopetition > competition | Cooperation −620.05 > competition −688.01 > coopetition −778.92 | **FAIL** |
| P2 | Holder survives all regimes; last in competition, not last in cooperation | Holder wealth −495.07 / −474.53 / −490.97 (coop/comp/coopet); last in ALL THREE regimes | **FAIL** |
| P3 | Preserved rounds < 50% of coalitions, and preserved mean > fused mean | Share 8.9% in both coalition regimes ✓, but preserved mean −0.4728 < fused mean +0.2177 | **FAIL** |
| P4 | Reactive+Holder beats solo baseline; Router coalitions do not | Reactive+Holder −0.3231 vs solo baseline −0.2698 (does not beat); Router coalitions +0.1108 (do beat) | **FAIL** — inverted |
| P5 | Coopetition broken rate in (0%, 50%); defectors beat the hypothetical coalition payoff > 50% | Broken rate 40.7% (174 defection events); productive share 52.9% | **PASS** |
| P6 | Reactive rank 1 in competition | Competition rank: Reactive, Router, Holder | **PASS** |

## Headline findings

### Which regime won on total payoff? Cooperation — but everything lost

Total gains (final wealth minus 200, summed over the three lenses):
cooperation −620.05, competition −688.01, coopetition −778.92.
Cooperation is the best of three losing regimes, not a winning one:
only Reactive ends above water in any regime (competition wealth
239.50; cooperation 311.49). The payoff scale (direction ±1 plus a
calibration bonus) against this world is roughly zero-sum-ish for
the average lens, and the lenses' costs eat the rest. The regime
ordering that failed is the interesting half: coopetition finished
LAST, not in the middle. Defection plus the higher coordination
cost (0.15 vs 0.05) destroyed more collective value than the
sharing created — even though defection was marginally productive
for the defectors themselves (P5). That is the classic split:
individually rational breaking, collectively costly.

### Did the holder survive? No — in any regime, and coalition did not save it

Holder solo mean payoff is −0.794 per round — not just the 0.40
holding cost, but a sign problem in the design (see Limits). Its
final wealth is −495.07 (cooperation), −474.53 (competition),
−490.97 (coopetition): coalition made its outcome slightly WORSE
than solo, not better. The M6 question — fund the holding without
funding the flailing — gets a third negative answer in this
programme's terms: subsidy funded the flailing (M6), insurance
taxed the distressed (VIII), and now coalition sharing does not
fund this holder either, because the holder's problem here is not
funding, it is that its joint probability is systematically wrong.
A holder that survives needs a better joint rule, not a bigger
subsidy — or a different definition of holding (see Limits).

### Did coalitions preserve or collapse disagreement?

Mostly they collapsed it — by design and by breaking:

- Coalition formation rate is 50.2% in both coalition regimes
  (427 of 850 rounds; identical because proposal/acceptance are
  deterministic and defection does not feed back into trailing
  accuracy — a limit, below).
- Preserved rounds are only 8.9% of coalition rounds (38 of 427),
  far below the ~1/3 proposer-rotation share: Holder proposes
  preserve only a third of the time, acceptance filtering cuts
  further, and preservation requires a material difference
  (>= 0.20) between the members' probabilities.
- In cooperation, the 38 preserved rounds (76 member-payoffs)
  averaged −0.4728 per member, against +0.1631 for fused rounds —
  and −0.7228 with the +0.25 preservation bonus stripped out.
  Preserving disagreement, as implemented here, did not pay; it
  paid the holder's bad joint probability plus a bonus that did
  not cover it.
- In coopetition, preserved coalitions NEVER survived intact:
  preserved payoff count is 0. Every one of the 38 preserved
  coalitions broke, because Holder's mushy solo sign so often
  contradicts the coalition mean's sign — the defection rule
  fires exactly on the lens the preserve mode exists to protect.
  In coopetition, disagreement survived only by breaking the
  coalition, never by holding it together.

### What cooperation did to the lenses: they stayed distinct, but distinctness did not help

No lens fused into another in the sense of changing its solo
probability rule — Router's solo probability is a fusion by
definition, but the lenses' rules never changed. What changed was
whose probability acted: in coalitions, the mean acted. The best
pairing in both coalition regimes was Reactive+Router
(+0.2545 cooperation, +0.4767 coopetition per member), and every
pairing involving Holder lost money (Reactive+Holder −0.3027 /
−0.3435; Holder+Router −0.1653 / −0.1227). So the pairer did pair
well — with the triage lens, not with the holder. P4 inverted
cleanly: Router coalitions beat the solo baseline (+0.1108 vs
−0.2698), Reactive+Holder did not. The pairer is not just
averaging here; pairing Reactive's speed with Router's lag-1
consensus is a genuinely better joint action than either solo.
That revises the DESIGN.md claim that Router merely collapses:
in this game, Router+Reactive is the strongest coalition, and
its strength is not explained by the preservation bonus (it is a
FUSE coalition).

### What conflict did: productive breaking, and the Contrarian lesson held

Coopetition: 174 defection events across 174 broken coalition
rounds (40.7% of coalition rounds broke), and defectors beat the
hypothetical coalition payoff in 52.9% of defection events — just
over half, so P5 passes but barely. Breaking was productive for
the breaker slightly more often than not, and collectively
disastrous (coopetition total −778.92, worst regime). Both halves
matter: conflict that helps the breaker can still impoverish the
commons.

Pure negation was not tested as a lens here, and the design kept
it out on purpose: no lens is a pure negator, Holder's minority
claim is an extreme positive claim, and defection is refusal of a
joint sign, not a bet against the world. The zoo's Contrarian
lesson (swan accuracy 0.130 for negation alone) therefore stands
unrevised by this run — but note the uncomfortable neighbour:
Holder's joint probability behaves like a negator in strong
regimes (it flips the majority sign), and it scores accordingly.
A minority claim that is just "the opposite, extremely" is
negation in a costume.

## Honest limits

- **The Holder is a caricature of the zoo's paraconsistent animal,
  and the caricature is what died.** The zoo's paraconsistent
  weights Both-valued hypotheses ×2; this Holder averages a
  majority claim with an extreme opposite, which flips the joint
  sign whenever the majority is strong (e.g. majority 0.75,
  minority 0.08 → joint 0.415, sign 0 in a 0.75 world). Its
  −0.794 solo mean is mostly that sign flip, not the 0.40 cost.
  Conclusions about "holders" from this run are conclusions about
  this joint rule. A faithful next Holder would weight, not
  average — or would act on the majority claim while RECORDING
  the minority, rather than letting the minority veto the sign.
- **The preservation bonus (+0.25) is baked in.** Preserved
  coalitions still lost even with it; the bonus-free preserved
  mean (−0.7228, cooperation) is reported above so the bonus
  cannot be mistaken for the finding.
- **Defection has no reputation consequence.** Solo correctness
  is recorded regardless of coalition action, so a defector's
  trailing accuracy — and hence future invitations — is
  untouched by betrayal. That is why coalition formation is
  identical (427 rounds) in cooperation and coopetition. A
  version with grudges (cf. the Julia game's Grudger) would
  change coopetition materially.
- **Three lenses, not seventeen, and a synthetic world.** The
  triad was chosen for contrast. Nothing here generalises to
  "lenses in general" without a new game, and nothing about
  real deliberation follows from a bit stream.
- **Measurement correction, disclosed:** the first version of
  the pooled preserved/fused mean averaged regime means and used
  0.0 for coopetition's empty preserved set. It was corrected to
  count-weighted pooling before this README was written; the
  correction does not change any verdict (P3 still fails on the
  payoff half, by a wider margin on the corrected numbers).
  Game rules and predictions were not touched.
- **Single run, single seed.** No replication, no seed sweep.
  Deterministic, so the numbers are exact for this seed — and
  only for this seed.

## Next questions this run opens (not built, not promised)

1. A Holder that weights instead of averages: majority claim acts,
   minority claim is recorded and priced separately. Does the
   holder then survive, and does preserving pay?
2. A Grudger variant: defection costs future invitations. Does
   coopetition stop being the worst regime?
3. A Translator pairing: Reactive+Holder with a translation step
   (not a mean) as the joint action. The current best pairing is
   Reactive+Router; the missing lens from the parent thread is
   still unbuilt.
