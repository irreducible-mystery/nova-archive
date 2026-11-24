# Pre-registered predictions — public goods with punishment

Written BEFORE the scored run. Scored honestly PASS/FAIL in
results.json / README.md afterwards. No prediction may be edited
after the run to fit the outcome.

World: 3 fixed players (Cooperator, Defector, Punisher), endowment
20, multiplier 1.5, punishment ratio 1:3, 100 rounds (see DESIGN.md).
Per-round payoffs from the design: Cooperator 20, Defector 40 − 3c,
Punisher 20 − c, group total 80 − 4c, where c is the punishment cost.

## P1 — No punishment, defection wins

At c = 0, per-round ranking is Defector (40) > Cooperator = Punisher
(20). Group total per round 80.

## P2 — Cheap punishment dents but does not reverse

At c = 4, per-round ranking is Defector (28) > Cooperator (20) >
Punisher (16). Group total per round 64.

## P3 — Strong punishment reverses the defector, punisher still last

At c = 8, per-round ranking is Cooperator (20) > Defector (16) >
Punisher (12). Punishment deters on paper (the Defector now earns
less than the Cooperator) but the Punisher still earns least: the
second-order cost problem is visible even in this minimal game.

## P4 — Punishment is a group deadweight loss in this design

Group total per round falls monotonically with c: 80 (c = 0) > 64
(c = 4) > 48 (c = 8). With no learning Defector, punishment costs
the group more than it recovers — the opposite of its usual
justification, and the reason the next regime needs a reacting
Defector.

## P5 — The reversal threshold lies between c = 4 and c = 8

The Defector's payoff crosses the Cooperator's (20) when
40 − 3c = 20, i.e. c = 20/3 ≈ 6.67. So c = 4 is on the
defection-pays side and c = 8 is on the defection-loses side; no
other sweep point is needed to locate the crossing to within the
sweep step.

---

Score: count of PASS out of 5. Exit code 1 if any prediction fails,
per house convention (failures are findings, not errors).
