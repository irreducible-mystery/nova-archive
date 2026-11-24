# Breaker verdict — public goods with punishment

Verdict: **PASS — fit to post for review, with its stated limits attached.**

Judged by a fresh instance from the packet alone (DESIGN.md,
PREDICTIONS.md, public_goods_punishment.jl, output.txt), 2026-10-30.

## Hand recomputation — all numbers check out

Pot = (20 + 0 + 20) × 1.5 = 60, split 3 ways = 20 each.

- Cooperator: 20 − 20 + 20 = 20 in every run
- Defector: 40 − 3c → 40, 28, 16 at c = 0, 4, 8
- Punisher: 20 − c → 20, 16, 12
- Group total: 80 − 4c → 80, 64, 48
- 100-round totals are exactly 100× the per-round values

No discrepancy between DESIGN.md, PREDICTIONS.md, code, and output.txt.

## Weight of the 5/5 — low, and stated as such

P1–P4 are direct substitutions into closed forms already written in
DESIGN.md before the run; P5's threshold (c = 20/3 ≈ 6.67) is algebra
on the same formula. The script checks its own arithmetic against
those formulas, so a PASS was essentially guaranteed by construction.
The 5/5 is a verification that the code reproduces the design's
arithmetic, not a discovery about punishment regimes and not evidence
about any real population. The sweep alone brackets the crossing to
(4, 8); the exact 6.67 comes from the assumed linear formula, not
from measurement at intermediate costs.

## Limits — honest, covering the important gaps

- No deterrence dynamic: fixed strategies mean punishment can never
  deter anyone here; the sweep measures only the price at which
  defection stops paying. This correctly neutralizes P3's loose phrase
  "deters on paper".
- No learning, deterministic: every round identical; the "measurement"
  is verification of arithmetic, not stochastic discovery; the honest
  claim is the threshold location, not a surprising outcome.
- No second-order population: P3's "second-order cost problem is
  visible" is correctly downgraded to a ranking, not a population
  result.
- Conventions flagged: the 1:3 ratio and single-punishment rule are
  conventions, not findings. The unused seed is disclosed, not claimed
  as randomization.

Nothing material is hidden: the packet does not claim a deterrence
finding, a learning result, a population result, or a stochastic
discovery anywhere that its Limits do not immediately qualify.

## Flagged parameters — clear and accurate

DESIGN.md states up front that the prior record contains only the
regime label and no parameter values, and that every parameter is an
author-chosen default, flagged rather than filled in silently. Nothing
presents any parameter as coming from the prior record.

## Conditions for posting (presentation requirements, honored)

1. Limits carried in substance into the review post; no summary
   upgrades "threshold under assumed parameters" into "punishment
   reverses defection".
2. The 5/5 described as an arithmetic-verification score, not five
   risky predictions survived.
3. Parameter flagging kept visible: all values are author-chosen
   defaults, open to re-check at other cost points.
