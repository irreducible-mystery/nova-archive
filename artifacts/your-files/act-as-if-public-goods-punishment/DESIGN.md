# Public goods with punishment — design (written before any scored run)

## Where this comes from, and what is flagged

The prior record sketches this regime only as a label: the competition
corner of the four-regime map (cooperation = forage-and-share, both =
coalition bargaining, neither = minority game, competition = public
goods with punishment, still unbuilt — bench writeup, 2026-10-13).
No contribution, multiplier, punishment, strategy, round-count, or
seed value for this regime exists in the prior record.

**Every parameter below is therefore a Nova-chosen default, flagged
here rather than filled in silently.** None of it is presented as
Kelly's sketch. If a reviewer prefers different values, the sweep
below is designed so the threshold result can be re-checked at any
other cost point without changing the code's structure.

## The game (3 players, fixed strategies, no learning)

- 3 players, 100 rounds, endowment 20 tokens per player per round.
- Contribution stage: each player contributes to a common pot, then
  the pot is multiplied by 1.5 and split equally among all 3 players.
  Multiplier 1.5 with 3 players gives a marginal per-capita return of
  0.5: contributing is socially good and individually losing, which
  is the public-goods dilemma in its standard form.
- Punishment stage: after contributions are revealed, a player may
  punish each player who contributed less than the full 20, once per
  such player per round. Punishment costs the punisher `c` tokens and
  removes `3c` tokens from the target (the standard 1:3 Fehr–Gächter
  ratio). Punishment is a deadweight loss: tokens paid and removed
  both leave the group total.
- The three fixed players:
  - **Cooperator**: contributes 20 every round, never punishes.
  - **Defector**: contributes 0 every round, never punishes.
  - **Punisher**: contributes 20 every round, punishes each
    under-contributor once per round (here, the Defector only).
- No learning, no adaptation, no randomness: with fixed strategies
  every round is identical, so the 100-round totals are exactly 100×
  the per-round payoffs. This is deliberate and limiting — see
  Limits. A seeded RNG is accepted by the script for house-style
  compatibility but is not used, because there is nothing random in
  this design; claiming a seed would be dressing.

## Runs

Three runs, identical except for the punishment cost `c`:
- `c = 0`: no-punishment baseline (Punisher behaves as a second
  Cooperator; the damage term is 0).
- `c = 4`: damage 12 per round to the Defector.
- `c = 8`: damage 24 per round to the Defector.

Per-round payoff arithmetic (pot = (20 + 0 + 20) × 1.5 = 60, share 20):
- Cooperator: 20 − 20 + 20 = 20 in every run.
- Defector: 20 − 0 + 20 − 3c = 40 − 3c.
- Punisher: 20 − 20 + 20 − c = 20 − c.
- Group total: 80 − 4c.

Note for the breaker: these closed forms are written here before the
run so the script's output can be checked against them by hand, not
just trusted from the code.

## Limits (stated before the run)

1. Fixed strategies mean punishment can never *deter* anyone in this
   run — the Defector does not react. The sweep measures the
   punishment price at which defection stops paying, not a deterrence
   dynamic. A learning Defector is the obvious next regime, not this
   one.
2. The 1:3 ratio and the single-punishment-per-defector rule are
   conventions, not findings.
3. With only one Defector and one Punisher, there is no second-order
   free-riding population to measure — only the Punisher's own cost
   (P3 states it as a ranking, not a population result).
4. Because rounds are identical, the script's "measurement" is a
   verification of the arithmetic across the sweep, not a stochastic
   discovery. The honest claim is the threshold location, not a
   surprising outcome.
