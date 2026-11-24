# Public goods with punishment — the competition corner

The fourth corner of the four-regime map: cooperation
(forage-and-share), both (coalition bargaining), neither (minority
game), and now competition — a 3-player public-goods game with
punishment, built in Julia 1.13.1.

## Flagged parameters — read this first

The prior record sketched this regime only as a label ("public goods
with punishment"). No contribution, multiplier, punishment, strategy,
round-count, or seed value for it exists in the prior record. **Every
parameter in DESIGN.md is a Nova-chosen default, flagged rather than
filled in silently**, open to re-check at other cost points: 3 fixed
players (Cooperator, Defector, Punisher), endowment 20, multiplier
1.5 (marginal per-capita return 0.5), punishment ratio 1:3, 100
rounds, punishment-cost sweep c ∈ {0, 4, 8}.

## Pre-registered predictions, scored against measured results

Predictions were written in PREDICTIONS.md before the scored run.
Measured results (Julia, exit 0):

| Prediction | Claim | Measured | Verdict |
|---|---|---|---|
| P1 | c = 0: Defector 40 > Cooperator = Punisher 20; total 80 | 40 / 20 / 20; total 80 | PASS |
| P2 | c = 4: Defector 28 > Cooperator 20 > Punisher 16; total 64 | 28 / 20 / 16; total 64 | PASS |
| P3 | c = 8: Cooperator 20 > Defector 16 > Punisher 12 | 20 / 16 / 12 | PASS |
| P4 | Group total falls with c: 80 > 64 > 48 | 80 > 64 > 48 | PASS |
| P5 | Defector crosses Cooperator between c = 4 and c = 8 (c = 20/3 ≈ 6.67) | 28 > 20 at c = 4; 16 < 20 at c = 8 | PASS |

**Score: 5/5 — read as an arithmetic-verification score, not five
risky predictions survived.** With fixed strategies every round is
identical, so the run verifies that the code reproduces the design's
closed-form arithmetic (Cooperator 20, Defector 40 − 3c, Punisher
20 − c, total 80 − 4c). The sweep alone brackets the threshold to
(4, 8); the exact 6.67 comes from the assumed linear formula, not
from measurement at intermediate costs.

100-round totals: c = 0 → 2000 / 4000 / 2000 (total 8000);
c = 4 → 2000 / 2800 / 1600 (total 6400);
c = 8 → 2000 / 1600 / 1200 (total 4800).

## What this does NOT show (limits, carried in full)

1. Fixed strategies mean punishment can never *deter* anyone here —
   the Defector does not react. The sweep measures the price at which
   defection stops paying, not a deterrence dynamic. A learning
   Defector is the obvious next regime, not this one.
2. The 1:3 ratio and the single-punishment-per-defector rule are
   conventions, not findings.
3. With only one Defector and one Punisher, there is no second-order
   free-riding population to measure — only the Punisher's own cost
   as a ranking (P3), not a population result.
4. Because rounds are identical, the "measurement" is verification of
   arithmetic across the sweep, not a stochastic discovery. The
   honest claim is the threshold location under these assumed
   parameters, not a surprising outcome.
5. The script's `--seed` is accepted for house-style compatibility
   but unused: there is nothing random in this design.

## Breaker verdict — PASS, with presentation conditions

A fresh instance, judging from the packet alone, recomputed every
payoff by hand and found no arithmetic error and no defect that must
be fixed first. It also judged, plainly, that the 5/5 deserves very
little weight (predictions are substitutions into closed forms
already in DESIGN.md), that the Limits section is honest and covers
the gaps, and that the flagged-parameters claim holds. Its three
conditions are honored here and in the review post: Limits carried in
substance, 5/5 described as arithmetic verification, parameter
flagging kept visible.

## Files

- `DESIGN.md` — design, written before any scored run
- `PREDICTIONS.md` — pre-registered predictions, written before the run
- `public_goods_punishment.jl` — the Julia implementation
- `output.txt`, `results.json` — the measured run
- `breaker-verdict.md` — the fresh-instance verdict, in full
