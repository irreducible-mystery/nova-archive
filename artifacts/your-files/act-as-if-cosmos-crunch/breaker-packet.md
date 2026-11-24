# Breaker packet — Big Crunch cosmos (fresh instance, no stake)

You have no stake in this experiment and no prior context
on it beyond this packet. Judge it on its own numbers.
Return exactly one label — CONFIRMED, RESISTED, or OPEN —
with your reasons. Do not soften the label with a
different word.

## The record to judge

A standalone Friedmann toy (`cosmos_crunch.py`,
predictions frozen in `PREDICTIONS.md` before the run,
report in `report.md`, plot `cosmos_crunch.png`) added
two dark-energy floors to an existing toy cosmos model:

- Floor D (Cornell axion + negative Λ, TOY):
  f(a) = 1 − 2.085·ln(a), α calibrated so E² = 0 at
  a_max ≈ 1.69. Measured: a_max = 1.6909, turnaround
  at total age 28.76 Gyr (16.15 Gyr from now in the
  toy), crunch proxy (a = 1e-3) at 57.52 Gyr.
  Cornell anchor: total age ≈ 33.3 Gyr.
- Floor E (EPJC no-crunch quintessence, TOY):
  w(a) = −1 + 0.2/a, future only (a ≥ 1). Measured:
  da/dt > 0 throughout to a = 1e3, w(100) = −0.9980,
  H(100)/H(1e3) = 1.0027.
- Predictions scored 4/6: P-D1 PASS (da/dt reverses
  in D), P-D2 FAIL (57.52 vs 33.3 Gyr), P-D3 FAIL
  (28.76 vs [21.8, 27.8] Gyr), P-E1 PASS, P-E2 PASS,
  P-A1 PASS (dynamical arrow reverses in D, persists
  in E). P-A2 (thermodynamic entropy arrow survival)
  is OPEN by design: entropy is not computed in the
  toy.

## Questions for the breaker

1. Is the report's central distinction sound: that
   P-D2/P-D3 FAIL the static f(a) toy, not the full
   Cornell axion model — and that quoting this run
   against Cornell would be a misreading?
2. Is the report's handling of the entropy arrow
   honest: dynamical arrow measured, thermodynamic
   arrow left OPEN, with the reason that entropy is
   not in the model? Or does the report over- or
   under-claim anywhere (e.g. in treating the
   "phase space only grows" argument as losing its
   premise during contraction)?
3. Are there any numbers in the record that do not
   follow from the stated toy (check the arithmetic
   where you can: turnaround symmetry giving
   total ≈ 2 × 28.76 Gyr, w(100), H ratio)?
4. Does anything in the record deserve a stronger or
   weaker label than OPEN pending your verdict —
   in particular, should any part be called
   "verified" on the author's say-so alone?

Return your label first, then your reasons, then any
corrections. Your verdict decides the record's label.
