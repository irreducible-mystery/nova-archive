# Pre-registered predictions — reacting defector

Written BEFORE the scored run. Scored honestly PASS/FAIL in
results.json / README.md afterwards. No prediction may be edited
after the run to fit the outcome.

World: 3 players, endowment 20, multiplier 1.5, punishment ratio
1:3, 100 rounds, Defector repents for exactly one round after being
punished (only when c > 0); see DESIGN.md. Per-round averages for
c > 0: Cooperator 25, Defector 35 − 1.5c, Punisher 25 − 0.5c,
total 85 − 2c. At c = 0: 20 / 40 / 20, total 80.

## P1 — Inert punishment changes nothing

At c = 0, per-round payoffs are Cooperator 20, Defector 40,
Punisher 20, total 80 — identical to the fixed-strategy run — and
the Defector defects in all 100 rounds (0 repent rounds).

## P2 — Cheap punishment dents but does not reverse

At c = 4, per-round averages are Cooperator 25, Defector 29,
Punisher 23, total 77. Ordering: Defector > Cooperator > Punisher.

## P3 — Strong punishment reverses, punisher still last, gaps compressed

At c = 8, per-round averages are Cooperator 25, Defector 23,
Punisher 21, total 69. Ordering: Cooperator > Defector > Punisher.
The Defector–Cooperator gap is 2 points, half the fixed-case gap
(4 points: 20 vs 16), because half the rounds are repentance rounds
in which both earn 30.

## P4 — Reaction recovers group welfare versus fixed strategies, but not versus no punishment

Group totals per round: reacting 77 (c = 4) and 69 (c = 8), versus
fixed-case 64 and 48 at the same costs, versus 80 at c = 0.
So reaction beats the fixed case at both c > 0, but still falls
short of the no-punishment total in both cases.

## P5 — Defection halves when punishment bites

At c = 4 and c = 8, exactly 50 of 100 rounds are repent rounds
(defection rate 50%, down from 100% at c = 0), and the Defector's
average crosses the Cooperator's between c = 4 and c = 8
(35 − 1.5c = 25 at c = 20/3 ≈ 6.67).

---

Score: count of PASS out of 5. Exit code 1 if any prediction fails,
per house convention (failures are findings, not errors).
