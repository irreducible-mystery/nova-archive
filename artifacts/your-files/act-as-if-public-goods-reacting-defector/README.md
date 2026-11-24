# Public goods with a reacting defector

The follow-up to the fixed-strategy competition regime (julia3claude
PR #18): exactly one change — the Defector now reacts. After being
punished, it contributes the full 20 for exactly one round, then
reverts to defecting. Everything else is carried over unchanged:
3 players, endowment 20, multiplier 1.5, punishment ratio 1:3,
100 rounds, punishment-cost sweep c ∈ {0, 4, 8}.

## The one reaction (flagged, Nova-chosen)

One round of repentance is a stipulated rule, not a learned or
observed behavior. It is triggered only when punishment actually
bites (c > 0). At c = 0 the "punishment" costs and removes nothing,
so it triggers nothing — the c = 0 run is the inert-punishment
control, identical to the fixed-strategy run. Round 1 defects (never
punished yet), so with 100 rounds the c > 0 runs alternate defect,
repent, defect, repent — exactly 50 of each. That 50/50 split
depends on the round count being even; predictions here are scoped
to 100 rounds and would need re-deriving at any other count.

## Pre-registered predictions, scored against measured results

Predictions were written in PREDICTIONS.md before the scored run.
Measured results (Julia, exit 0), per-round averages:

| Prediction | Claim | Measured | Verdict |
|---|---|---|---|
| P1 | c = 0: 20 / 40 / 20, total 80, 0 repent rounds | 20 / 40 / 20, total 80, 0 repent | PASS |
| P2 | c = 4: Cooperator 25, Defector 29, Punisher 23, total 77 | 25 / 29 / 23, total 77 | PASS |
| P3 | c = 8: Cooperator 25, Defector 23, Punisher 21, total 69; gap 2, half the fixed-case gap | 25 / 23 / 21, total 69 | PASS |
| P4 | Reacting totals 77 and 69 beat fixed-case 64 and 48, but fall short of 80 at c = 0 | 77 > 64, 69 > 48, both < 80 | PASS |
| P5 | Exactly 50 repent rounds at c = 4 and c = 8; Defector crosses Cooperator between c = 4 and c = 8 | 50 and 50; 29 > 25, then 23 < 25 | PASS |

**Score: 5/5 — read as an arithmetic-and-state-machine verification
score, not five risky predictions survived.** The predictions are
substitutions into closed forms already in DESIGN.md, and the one
genuinely simulated element — the alternating state machine — is a
direct consequence of the stipulated rule.

100-round totals: c = 0 → 2000 / 4000 / 2000 (total 8000);
c = 4 → 2500 / 2900 / 2300 (total 7700);
c = 8 → 2500 / 2300 / 2100 (total 6900).

Why the numbers move: a defect round pays 20 / (40 − 3c) / (20 − c)
(total 80 − 4c); a repent round pays 30 to everyone (contributions
60, pot 90, share 30, total 90). Averaging the pair gives
Cooperator 25, Defector 35 − 1.5c, Punisher 25 − 0.5c,
total 85 − 2c.

## Post-run wording correction (recorded, pre-run files untouched)

DESIGN.md Limit 2 said the repent round "lifts both players
equally." That phrasing is imprecise and is corrected here, not
silently edited in the pre-run file: at c = 8 the Defector rises
16 → 30 while the Cooperator rises 20 → 30. The correct claim, and
the one P3 states, is gap-halving: the Defector–Cooperator gap is
2 points here versus 4 in the fixed case, because half the rounds
are repent rounds in which both earn 30 and the gap is 0. The
threshold itself is genuinely unchanged (both solve to
c = 20/3 ≈ 6.67).

Also noted: the fixed-case totals cited in P4 (64 and 48) are
carried-over closed forms from the earlier regime (80 − 4c), not
re-measured in this run. The sweep brackets the threshold to
(4, 8); the exact 6.67 comes from the assumed linear formula, not
from measurement at intermediate costs.

## What this does NOT show (limits, carried in full)

1. One round of repentance is stipulated, not learned or observed.
   This regime measures the consequences of this rule, not its
   realism. A real defector might repent longer, shorter, or not
   at all.
2. The reversal threshold is unchanged from the fixed case
   (c ≈ 6.67). What changes is the gap size and the group total,
   not the threshold location.
3. The run is deterministic: it verifies that the simulation
   reproduces the closed forms, not a stochastic discovery. The
   honest claims are the ordering, the totals, and the defection
   rate.
4. One Defector, one Punisher: still no population result.
5. The script's `--seed` is accepted for house-style compatibility
   but unused: there is nothing random in this design.

## Breaker verdict — PASS, with presentation conditions

A fresh instance, judging from the packet alone, traced the state
machine round by round (round 1 defects, punishment sets repentance,
repentance resets it, c = 0 stays inert) and recomputed every
payoff by hand with no arithmetic error and no defect that must be
fixed first. It judged the 5/5 as verification weight only, the
Limits honest, and the two precision notes above as presentation
requirements — both honored here and in the review post.

## Files

- `DESIGN.md` — design, written before any scored run
- `PREDICTIONS.md` — pre-registered predictions, written before the run
- `public_goods_reacting_defector.jl` — the Julia implementation
- `output.txt`, `results.json` — the measured run
- `breaker-verdict.md` — the fresh-instance verdict, in full
