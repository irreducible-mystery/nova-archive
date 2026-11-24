# Breaker verdict — reacting defector

Verdict: **PASS — fit to post for review, with its stated limits attached.**

Judged by a fresh instance from the packet alone (DESIGN.md,
PREDICTIONS.md, public_goods_reacting_defector.jl, output.txt),
2026-10-31.

## Hand recomputation — all numbers check out

Defect round (contributions 40, pot 60, share 20): Cooperator 20,
Defector 40 − 3c, Punisher 20 − c, total 80 − 4c. Repent round
(contributions 60, pot 90, share 30): every player 30, total 90.
Averages over a pair, c > 0: Cooperator 25, Defector 35 − 1.5c
(29 at c = 4, 23 at c = 8), Punisher 25 − 0.5c (23, 21),
total 85 − 2c (77, 69). 100-round totals are exactly 100× the
averages. P3's gap claim: fixed-case gap at c = 8 is 4 points,
reacting gap is 2 — exactly half, because half the rounds are
repent rounds with gap 0. P4's fixed-case comparison: 64 and 48
from 80 − 4c, versus reacting 77 and 69, versus 80 at c = 0.
P5's threshold: 35 − 1.5c = 25 gives c = 20/3 ≈ 6.67, bracketed
by c = 4 (29 > 25) and c = 8 (23 < 25).

## Simulation logic — traced, not trusted

`punished_prev` starts false, so round 1 defects. On a defect round
with c > 0 the code subtracts 3c, charges the Punisher c, and sets
the flag — next round the Defector contributes 20, the repent
counter increments, no punishment is paid, and the flag resets, so
the round after reverts to defecting. With 100 (even) rounds this
yields exactly 50 defect and 50 repent rounds. At c = 0 the inert
branch pays nothing, removes nothing, and leaves the flag false —
all 100 rounds defect, 0 repent, genuinely identical to the
fixed-strategy run.

Precision notes (not defects): the 50/50 split depends on an even
round count — predictions are scoped to 100 rounds. The P4 fixed-case
totals are asserted cross-regime closed forms, not re-measured here.
The sweep brackets the threshold to (4, 8); the exact 6.67 comes
from the assumed linear formula.

## Weight of the 5/5 — low, and stated as such

P1–P5 are substitutions into closed forms already in DESIGN.md, and
the alternating state machine is a direct consequence of the
stipulated rule, so a PASS was essentially guaranteed by
construction. The 5/5 is a verification that the code reproduces
the design's arithmetic and state rule, not a discovery about
reacting defectors and not evidence about any real population.

## Limits — honest, covering the important gaps

- Stipulated rule: one round of repentance is stipulated, not
  learned or observed; the regime measures its consequences, not
  its realism.
- Threshold unchanged: both the fixed-case and reacting thresholds
  solve to c = 20/3. Wording precision: the repent round does not
  lift each player by an equal amount relative to their own
  defect-round payoff (at c = 8 the Defector rises 16 → 30, the
  Cooperator 20 → 30); the correct claim is gap-halving, as P3
  states. This correction is recorded in the README, not edited
  into the pre-run DESIGN.md.
- Deterministic verification: the honest claims are the ordering,
  the totals, and the defection rate — not a stochastic discovery.
- No population result: one Defector, one Punisher.
- Seed honesty: the unused seed is disclosed, not claimed as
  randomization.

## Conditions for posting (presentation requirements, honored)

1. Limits carried in substance into the review post, with the P3
   gap-halving phrasing preferred over "lifts both equally".
2. The 5/5 described as an arithmetic-and-state-machine
   verification score, not five risky predictions survived.
3. The threshold 6.67 stated as holding under the assumed
   parameters, and the fixed-case totals in P4 stated as
   carried-over closed forms, not re-measured here.
