# Public goods with a reacting defector — design (written before any scored run)

## What changes from the fixed-strategy version

The previous regime (julia3claude PR #18, 5/5 arithmetic-verification)
had fixed strategies: the Defector never reacted, so punishment could
never deter anyone and the sweep measured only the price at which
defection stops paying. This regime adds exactly one reaction, and
nothing else. All other parameters are carried over unchanged:
3 players, endowment 20, multiplier 1.5, punishment ratio 1:3,
100 rounds, punishment-cost sweep c ∈ {0, 4, 8}.

## The one reaction (flagged, Nova-chosen)

- **Defector**: contributes 0, unless it was punished in the previous
  round, in which case it contributes the full 20 for exactly one
  round (one round of repentance), then reverts to defecting.
  Repentance is triggered only when punishment actually bites, i.e.
  when c > 0 (damage 3c > 0). At c = 0 the "punishment" costs nothing
  and removes nothing, so it triggers nothing — the c = 0 run is
  therefore identical to the fixed-strategy run, which is the point:
  it is the inert-punishment control.
- **Cooperator**: contributes 20 every round, never punishes.
- **Punisher**: contributes 20 every round, punishes each
  under-contributor once per round (here, the Defector, only on
  rounds when it defects).
- Round 1: the Defector has not been punished yet, so it defects.
  With 100 rounds, the c > 0 runs therefore alternate defect,
  repent, defect, repent, … — exactly 50 defect rounds and 50
  repent rounds. This is a consequence of the one-round rule, not a
  fitted parameter.
- No learning beyond the one-round rule, no randomness, no other
  strategy changes. A seeded RNG is accepted by the script for
  house-style compatibility but is not used.

## Per-round arithmetic (written before the run, for hand-checking)

- Defect round (contributions 20 + 0 + 20 = 40, pot 60, share 20):
  Cooperator 20, Defector 40 − 3c, Punisher 20 − c, total 80 − 4c.
- Repent round (contributions 60, pot 90, share 30): every player
  20 − 20 + 30 = 30, total 90. No punishment is spent, because
  nobody under-contributes.
- Averages over a defect + repent pair, c > 0:
  Cooperator (20 + 30) / 2 = 25.
  Defector ((40 − 3c) + 30) / 2 = 35 − 1.5c.
  Punisher ((20 − c) + 30) / 2 = 25 − 0.5c.
  Total (80 − 4c + 90) / 2 = 85 − 2c.

So: c = 4 → 25 / 29 / 23, total 77. c = 8 → 25 / 23 / 21, total 69.
At c = 0 (no repentance): 20 / 40 / 20, total 80, as before.

## Limits (stated before the run)

1. One round of repentance is a stipulated rule, not a learned or
   observed behavior. A real reacting defector might repent longer,
   shorter, or not at all — this regime measures the consequences of
   this rule, not the rule's realism.
2. The reversal threshold is unchanged from the fixed case in
   algebra (Defector average 35 − 1.5c crosses Cooperator 25 at
   c = 20/3 ≈ 6.67), because the repent round lifts both players
   equally. What changes is the gap size and the group total, not
   the threshold location.
3. As before, the run is deterministic: with the alternating pattern
   fixed by the rule, the "measurement" is a verification that the
   simulation reproduces the closed forms above, not a stochastic
   discovery. The honest claims are the ordering, the totals, and
   the defection rate — not a surprising outcome.
4. One Defector, one Punisher: still no population result.
