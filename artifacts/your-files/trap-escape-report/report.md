# Trap escape — two escapes from the jaded room's chaos trap

Pre-registered head-to-head, 2026-10-27. Simulation only; no art-project
files or hardware plans changed.

## Setup (identical in all conditions)

Jaded room only: same audience (fast habituation, narrow tolerance), same
seed, same start (r = 2.9), 5 days of 288 ticks. Three conditions:

- Baseline: no escape — the original jaded run, for replication.
- Nudge: tiny timed nudges to r, at most 0.005 in size, applied only when
  the system is within 0.05 of its current period-1 fixed point — the
  small-steering approach.
- Reset: nightly dreaming reset at each day boundary — r set to 3.50,
  wildness reset to 0.20, nothing else changed.

## Predictions (written before any run)

- P1: Baseline pins at the trap: fraction of time above r = 3.9 at least
  0.60, mean r at least 3.80.
- P2: Nudge cuts the trapped fraction by at least 0.20 versus baseline,
  but final-day mean r stays at or above 3.70 (steered, not escaped).
- P3: Reset gives final-day mean r at or below 3.70 and trapped fraction
  at or below 0.30, with a sawtooth (climb within each day, drop at reset).
- P4: Reset mean r is below nudge mean r (reset wins on escape).
- P5: Nudge uses fewer than 200 nudges, mean size below 0.005.

## Measured outcomes

| Condition | Mean r | Final-day mean r | Fraction above 3.9 | Day means |
|---|---|---|---|---|
| Baseline | 3.833 | 4.000 | 0.696 | 3.269, 3.896, 4.000, 4.000, 4.000 |
| Nudge | 3.833 | 4.000 | 0.699 | 3.273, 3.895, 3.997, 4.000, 4.000 |
| Reset | 3.686 | 3.819 | 0.183 | 3.269, 3.746, 3.778, 3.819, 3.819 |

Nudge details: 109 nudges, mean size 0.0049 — tiny, as promised, and
essentially no effect. Reset details: resets at ticks 288, 576, 864, 1152.

## Predictions scored honestly

- P1: PASS. Baseline replicates the original trap (mean 3.833, trapped
  fraction 0.696).
- P2: FAIL, both halves. Nudge trapped fraction 0.699 is not 0.20 below
  baseline — it is the same — and final-day mean is 4.000.
- P3: FAIL overall. Reset trapped fraction 0.183 passes, but final-day
  mean 3.819 does not pass 3.70. Day means climb within each day after
  each reset, so the trap re-forms inside a single day.
- P4: PASS. Reset mean 3.686 is below nudge mean 3.833.
- P5: PASS. 109 nudges, mean size 0.0049.

Score: 3 of 5.

## Verdict: neither escape, as built, escapes — but they fail differently

The trap is not steerable from inside by these tiny timed nudges: 109
nudges at the maximum allowed size move the outcome by less than 0.001
in mean r. The nudges are swamped by the drive that pins r at 4.0.

The nightly reset is not a full escape either, at nightly frequency:
it cuts the trapped fraction from 0.696 to 0.183, but r climbs back
toward 4.0 within each day, so the final day still averages 3.819.
Reset mitigates; it does not hold.

So the honest verdict is mixed, not one-way: the trap needs something
stronger than either escape as built — a more frequent reset, a lower
reset target, a ceiling on r, or a change to the audience itself.
That is the next test, not a conclusion that the trap is unbreakable.
