# Breaker verdicts — Big Crunch cosmos (2026-10-27)

Both verdicts were pasted by Kelly into chat on 2026-10-27.
Both are **CONFIRMED**, where CONFIRMED = the record's
numbers and framing hold under an attempt to break them.
Both breakers are Claude models (Opus and Fable) — same
model family, so their agreement is within-family
confirmation, not cross-family independent confirmation
(per the programme's independence-map counting rule).
Neither breaker received `cosmos_crunch.py`, `report.md`,
or `PREDICTIONS.md`; both judged on the packet alone
and rebuilt/rederived independently.

## Opus — CONFIRMED

- Recomputed Floor D from the packet (Ωm = 0.315,
  H0 = 67.4, no radiation, f(a) at all a): a_max =
  1.6909, turnaround 28.77 Gyr total / 16.15 Gyr from
  now, lifetime 57.53 Gyr — matching the record to
  rounding. Ωm = 0.3 would give a_max = 1.686, so the
  run evidently used Planck-like parameters (inference).
- Symmetry: total ≈ 2 × turnaround is exact for a
  static f(a); stopping at a = 1e-3 instead of 0
  changes almost nothing.
- Floor E: w(100) = −0.9980 ✓, H(100)/H(1e3) =
  1.0027 ✓, insensitive to Ωm; ratio near 1 because
  ρ_DE flattens to a constant, so the late universe
  goes de Sitter.
- Q1 (toy-vs-Cornell distinction): sound. A static
  f(a) forces time-symmetric recollapse; a rolling
  axion field keeps evolving through turnaround,
  breaking symmetry and shortening collapse. 57.5 vs
  33.3 Gyr is a failure of the toy's static assumption.
  Both FAILs survive the correction below.
- Q2 (entropy): honest, with one caveat. Measuring
  the dynamical arrow and leaving the thermodynamic
  arrow OPEN is correct, since entropy isn't in the
  model. Caveat: contraction removes only one premise
  (growing comoving volume); gravitational entropy
  (clumping, black holes) keeps rising. Standard view
  since Hawking withdrew his arrow-reversal claim:
  the thermodynamic arrow does not reverse in a
  recollapse. Accurate phrasing: "OPEN in this model,
  conventionally expected to persist."
- Q4: P-A1 and P-E1 hold by construction (D calibrated
  so E² hits zero; E has ρ_DE > 0 everywhere, so
  da/dt can never reverse). Correct, but consistency
  checks rather than evidence; they shouldn't be
  counted as "verified" predictions alongside others.
  P-A2 stays OPEN.
- Corrections (applied in report.md): (1) Floor D
  applied to the past as well as the future — f > 1
  for a < 1 inflates past dark energy, toy "now" =
  12.61 Gyr instead of ~13.8 Gyr; state outright.
  Future-only variant (Opus's numbers, not
  re-checked by Nova): turnaround 29.95 Gyr,
  lifetime 59.9 Gyr, D2/D3 still FAIL. (2) Floor E
  starts at w = −0.8 today; if the past was ΛCDM,
  w jumps there (doesn't affect E1/E2). (3) Source
  of a_max ≈ 1.69 unstated in the packet — state it.

## Fable — CONFIRMED

(Fable's own note: reading the scheme as CONFIRMED =
the record's numbers and framing hold under an attempt
to break them; if the scheme used RESISTED for that,
remap — substance unchanged.)

- Q1 (toy-vs-Cornell): sound, and stronger than the
  report states. Static f(a) makes ȧ² a function of a
  alone, so a(t) is exactly mirror-symmetric about
  turnaround [proven]. t_crunch = 2·t_turn is forced,
  not measured, and the frozen predictions were
  jointly unsatisfiable: P-D3's [21.8, 27.8] Gyr
  implies total 43.6–55.6 Gyr, which can never equal
  Cornell's 33.3. D2/D3 are one structural failure
  counted twice. Cornell's asymmetry (recall:
  expand ~11 Gyr more, then a shorter contraction —
  provisional) comes from axion dynamics the toy
  lacks.
- Q2 (entropy): honest. An FRW toy has no
  entropy-generating degrees of freedom; computing
  one would be fabrication. Caution: "the
  phase-space-only-grows argument loses its premise
  in contraction" is correct about that argument,
  but must not slide toward "so the arrow may
  reverse" — Hawking's 1985 error, retracted after
  Page [recall, high confidence]. Literature
  expectation: thermodynamic arrow persists through
  a crunch. OPEN in the toy; not open in the physics.
- Q3 (arithmetic): all checks pass. w(100) = −0.998
  [proven]; ρ_DE ∝ exp(−0.6(1−1/a)) → H ratio =
  exp(0.0027) = 1.0027, matter ~10⁻⁶ of DE there
  [derived]; 57.52 = 2 × 28.76 [derived]; a_max =
  1.69 and 16.15 Gyr to turnaround reproduce by hand
  to <1% if Ω_m≈0.31, Ω_Λ≈0.69, H₀≈67.7 — the packet
  doesn't state these [inference]. Implied toy age
  now = 12.61 Gyr, plausibly below 13.8 because
  f(a) > 1 in the past.
- Q4 ("verified" on say-so): nothing needs to be.
  Items are analytic consequences anyone can
  rederive; integrated times independently
  cross-checked. What should change is the
  scorecard: every PASS and FAIL was decidable
  before the run. D1 follows from calibration, A1
  is D1 restated, E1 guaranteed by all-positive
  densities, E2 evaluates the input formula. "4/6"
  reads as four risky predictions surviving; the
  record is really "arithmetic correct, zero risky
  predictions tested." Say that.
- Corrections to make (applied in report.md): label
  t_crunch "derived (by symmetry)", not "measured";
  state P-D2/P-D3 mutually unsatisfiable for any
  static-f(a) toy; collapse the scorecard to
  independent tests, or keep 4/6 with a note that
  none were risky; state Ω_m, Ω_Λ, H₀ in the record;
  add the Hawking/Page literature pointer beside P-A2.

## How the corrections were applied

All corrections above are applied in `report.md`
("Breaker verdicts" and "Breaker corrections"
sections, plus annotations to the prediction table
and the D-failures section). `PREDICTIONS.md` was
NOT edited — it stays frozen as written before the
run; the corrections change the record's reading of
it, not its text. The Hawking/Page pointer was
corroborated by Nova after the verdicts against
Hawking's own account (A Brief History of Time:
first thought disorder would decrease in the
contracting phase; Page pointed out the
no-boundary condition does not require the
contracting phase to be the time reverse of the
expanding phase; Laflamme's model showed collapse
differing from expansion; Hawking concluded disorder
continues to increase during contraction) — so that
pointer is no longer breaker-recall only.
