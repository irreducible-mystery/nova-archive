# Big Crunch cosmos — experiment record

**Status: CONFIRMED — by two breaker verdicts, 2026-10-27
(see "Breaker verdicts" below).** CONFIRMED here means the
record's numbers and framing hold under an attempt to
break them — not that the Cornell or EPJC models are
themselves verified, and not that the toy tested anything
risky (see "Scorecard, corrected"). Both breakers are
Claude models (Opus and Fable), so this is confirmation
within one model family, not cross-family confirmation.
Original COSMOS (`~/workspace/your_files/act-as-if-cosmos/`)
is untouched; this is a standalone extension.

**Parameters, stated outright (they were in the code
and in this report's parameter paragraph, but not in
the breaker packet — both breakers had to infer them):
H₀ = 67.4 km/s/Mpc, Ω_m = 0.315, Ω_de = 0.685,
Ω_r = 9.2e-5 (Planck 2018, as in the original COSMOS).**

## Breaker verdicts (2026-10-27, Kelly-pasted)

Two verdicts, both **CONFIRMED**, both judged on the
packet alone (neither breaker received `cosmos_crunch.py`,
`report.md`, or `PREDICTIONS.md`; both rebuilt/rederived
independently, so nothing below rests on the author's word).
Full summaries: `breaker-verdicts.md` in this folder.

- **Opus:** recomputed Floor D from the packet
  (a_max = 1.6909, turnaround 28.77 Gyr total / 16.15 Gyr
  from now, lifetime 57.53 Gyr — matching the record to
  rounding) and Floor E (w(100) = −0.9980, H ratio
  1.0027, both ✓). Q1 sound, Q2 honest with one caveat
  (below), Q4: P-A1/P-E1 hold by construction and are
  consistency checks, not evidence.
- **Fable:** proved the symmetry structurally (ȧ² a
  function of a alone ⇒ a(t) exactly mirror-symmetric
  about turnaround), showed P-D2/P-D3 were jointly
  unsatisfiable (below), and collapsed the scorecard:
  "arithmetic correct, zero risky predictions tested."

**Differences between them, since they were asked about:**
Opus is the numeric recomputation (including a
future-only Floor D variant: turnaround 29.95 Gyr,
lifetime 59.9 Gyr, D2/D3 still FAIL — Opus's numbers,
not re-checked by Nova) plus the gravitational-entropy
caveat. Fable is the structural proof (symmetry as a
theorem, not a measurement) plus the scorecard
critique and the parameter-omission catch. Same
verdict, different angles — and same model family,
so the agreement is not independent confirmation in
the independence-map sense.

## Breaker corrections (applied 2026-10-27; the frozen
## predictions file is NOT edited — these correct the
## record's reading of it)

1. **Floor D was applied to the past as well as the
   future.** Unlike Floor E, it was not restricted to
   a ≥ 1. Because f(a) > 1 for a < 1, past dark energy
   is inflated and the toy's "now" is 12.61 Gyr
   (28.76 − 16.15), not ~13.8 Gyr. Stated outright
   here, as Opus required. (Opus's future-only
   variant — turnaround 29.95 Gyr, lifetime 59.9 Gyr —
   still FAILs D2/D3.)
2. **t_crunch is derived (by symmetry), not measured.**
   With E² depending only on a, contraction mirrors
   expansion exactly, so total = 2 × turnaround is
   forced, not an empirical outcome. The run output's
   "measured" language for t_crunch is superseded by
   this. Stopping at a = 1e-3 instead of 0 changes
   almost nothing (<1 Myr, per Fable).
3. **P-D2 and P-D3 were mutually unsatisfiable.**
   P-D3's band [21.8, 27.8] Gyr for turnaround implies
   a total age of 43.6–55.6 Gyr for any static-f(a)
   toy, which can never equal Cornell's 33.3 Gyr.
   D2/D3 are therefore **one structural failure
   counted twice**, not two independent failures.
4. **Scorecard, corrected.** Raw score stays 4/6, but
   with Fable's note attached: none of the passes
   were risky. D1 follows from the calibration
   (E² set to hit zero), A1 restates D1, E1 is
   guaranteed by all-positive densities, E2 evaluates
   the input formula. Collapsed to independent tests:
   (a) arithmetic/symmetry — correct; (b) Floor E
   de Sitter endpoint — by construction;
   (c) toy-vs-Cornell distinction — sound;
   (d) entropy handling — honest, OPEN in the toy.
   "4/6" must not be read as four risky predictions
   surviving.
5. **Floor E starts at w = −0.8 today.** If the past
   was ΛCDM, w jumps there at a = 1. Noted; it does
   not affect E1 or E2.
6. **Source of a_max ≈ 1.69, stated explicitly.**
   It comes from secondary coverage of Luu, Qiu,
   Tye — the August 2026 benchmark summary, which
   states the model's scale factor "grows to about
   1.69 times its present value" before reversing.
   The primary paper was still not re-read line by
   line; the calibration target is secondary-sourced,
   and the 7-vs-11 Gyr turnaround difference in
   coverage remains unresolved (see "Open / not done").
7. **P-A2, revised phrasing.** "OPEN in this model,
   conventionally expected to persist." The
   conventional expectation is Hawking's retracted
   arrow-reversal: he first thought disorder would
   decrease in a contracting phase, then — after
   Don Page pointed out that the no-boundary
   condition does not require the contracting phase
   to be the time reverse of the expanding phase,
   and Raymond Laflamme found a model where collapse
   differs from expansion — concluded disorder
   continues to increase during contraction
   (A Brief History of Time, ch. 9/10). Contraction
   removes only the growing-volume premise, not the
   gravitational-entropy premise (clumping, black
   holes keep rising, per Opus). The toy still does
   not compute entropy, so P-A2 stays OPEN *in the
   toy* — but the report must not slide from that
   toward "so the arrow may reverse."

## Question

Does the entropy arrow survive contraction (da/dt < 0)?

Short answer from this run: the *dynamical* arrow (sign of
da/dt) reverses in the crunch floor and persists in the
no-crunch floor — but the *thermodynamic* arrow (entropy)
is not computed by any Friedmann toy here, so its survival
through contraction is **OPEN, not decided by this run**.
That distinction is the finding, not a footnote.

## The two floors, honestly represented

### Floor D — Cornell axion + negative Λ (toy representation)

- Anchor: Luu, Qiu, Tye, "The Lifespan of Our Universe"
  (2025), fitted to DES/DESI data as reported in secondary
  coverage (phys.org July 2025; SpaceDaily August 2026).
  Ultralight axion + negative cosmological constant;
  best-fit scale factor grows to a_max ≈ 1.69, then
  reverses; total age ≈ 33.3 Gyr (crunch ~20 Gyr from
  now). Turnaround time differs between reports
  (~7 Gyr from now in July 2025 coverage, ~11 Gyr in
  the August 2026 benchmark summary) — a version/fit
  difference, recorded, not smoothed. The full paper
  was not re-read line by line for this toy.
- Toy: flat Friedmann, dark-energy factor
  f(a) = 1 − 2.085·ln(a), with α chosen so E²(a) = 0
  at a ≈ 1.69. **This is a calibration, not a result.**
  It is NOT the axion field equations: no field rolling,
  no oscillation, no time-dependent equation of state
  beyond the static f(a).

### Floor E — EPJC no-crunch quintessence (toy representation)

- Anchor: Myrzakulov, Hussain, Shahalam (2026),
  "Nonminimally coupled quintessence with double
  exponential potential: observational evidence against
  big crunch singularity", Eur. Phys. J. C 86(9), 1055,
  DOI 10.1140/epjc/s10052-026-16306-7. Data-preferred
  couplings steer away from collapse: the field freezes
  at an attractor, Hubble derivative vanishes, Ω_de → 1,
  effective w → −1 (de Sitter endpoint); the model
  remains phantom-free; variants are strongly disfavored
  vs ΛCDM at background level.
- Toy: flat Friedmann with w(a) = −1 + 0.2/a, so
  w = −0.8 today and w → −1 as a → ∞, giving
  ρ_de(a) = exp(−0.6·(1 − 1/a)). **Future only**
  (a ≥ 1): this w(a) diverges at a → 0, so it is not
  a past model at all, and is not used as one.
  It is NOT the full nonminimally coupled field
  equations (no coupling ξ, no double-exponential
  potential).

Both floors use Planck 2018 parameters from the
original COSMOS (H₀ = 67.4, Ω_m = 0.315, Ω_r = 9.2e-5,
Ω_de = 0.685). Same caveat as the original: toy fixes
H₀/Ω across floors instead of refitting per floor.

## Predictions (frozen before the run) beside outcomes

From `PREDICTIONS.md`, written 2026-10-27 before any run.

| Prediction | Frozen claim | Measured | Verdict |
|---|---|---|---|
| P-D1 | D reaches sustained da/dt < 0 after turnaround, to crunch proxy a = 1e-3 | Expansion sign +, contraction sign −, crunch at 57.52 Gyr > turnaround 28.76 Gyr (crunch time derived by symmetry, not measured — see corrections) | PASS |
| P-D2 | D total age within ±3 Gyr of Cornell's 33.3 Gyr | 57.52 Gyr, +24.22 Gyr off | FAIL |
| P-D3 | D turnaround within [21.8, 27.8] Gyr total age (13.8 + 11 ± 3) | 28.76 Gyr (16.15 Gyr from now in the toy) | FAIL (just outside; 0.96 Gyr past the band) |
| P-E1 | E never reaches da/dt < 0, to a = 1e3 | da/dt > 0 throughout, min 6.895e-02 | PASS |
| P-E2 | E de Sitter endpoint: w(100) within 0.01 of −1, H(100) within 5% of H(1e3) | w(100) = −0.9980, H ratio = 1.0027 | PASS |
| P-A1 | Dynamical arrow reverses in D, persists in E | D sign flips, E sign stays + | PASS |
| P-A2 | Thermodynamic entropy arrow survival | Entropy not computed in any Friedmann toy here | OPEN by design |

**Score: 4/6** (excluding OPEN P-A2). The run's exit
code is 1 under the house convention (not all pass) —
that is a score, not an error. **Read with the
breaker corrections above: none of the passes were
risky predictions; the independent-test summary in
correction 4 supersedes the raw 4/6 as the honest
reading.**

## What the D failures mean — and what they do not mean

The static f(a) toy is symmetric in a way the real
axion model is not: with H² depending only on a,
contraction from a_max back down retraces the
expansion time exactly (28.76 Gyr out,
28.76 Gyr back, total 57.52 Gyr) — proven by Fable,
not merely observed in the run. The Cornell model's
33.3 Gyr total requires contraction to be *faster*
than expansion — the axion field keeps rolling and
the negative constant is exposed differently on the
way down. That dynamics is exactly what the toy
leaves out.

So: **P-D2/P-D3 FAIL the toy, not Cornell.** The toy
proves a declining-density Friedmann model cannot
match both a_max = 1.69 and total age 33.3 Gyr at
once; it does not test, confirm, or refute the full
axion model. Anyone quoting this run as "the Big
Crunch model is wrong" is misreading it. Likewise,
P-D1 passes for the toy's dynamics, not for Cornell's.

Floor E's passes are narrower than they look: they
show the w(a) toy has a de Sitter endpoint, which
it was built to have. The EPJC result itself — that
data-preferred couplings select potentials that
never go negative — is a property of the full
field model, not something this toy re-derives.

## The arrow, stated carefully

- Dynamical arrow = sign(da/dt). It reverses in D,
  persists in E. Measured, not argued.
- Thermodynamic arrow = entropy increase (second
  law). Not in the model. The original COSMOS README
  already warned the entropy argument is thermodynamic
  reasoning *about* the model, not derived *from* it.
  During contraction, volume shrinks, so the
  "phase space only grows" argument that supported
  the arrow in expanding floors no longer applies —
  but that is an argument *losing its premise*, not
  a measurement of entropy reversing. Whether entropy
  keeps increasing through a crunch (e.g. via
  gravitational entropy, horizon entropy, or a
  low-entropy bounce condition) is a question for a
  model that actually computes entropy. This run
  does not answer it, and must not be cited as
  answering it either way.

## Files in this folder

- `PREDICTIONS.md` — frozen predictions, before the run.
- `cosmos_crunch.py` — the extension (original cosmos.py
  untouched). Run: `python3 cosmos_crunch.py`.
- `cosmos_crunch.png` — scale-factor evolution, both
  floors, plotted against time since now; D turns at
  a_max = 1.69 (+16.2 Gyr from now in the toy) and
  reaches the crunch proxy at +44.9 Gyr; E rises
  monotonically.
- `output.txt` — measured numbers, one line each.
- `breaker-packet.md` — the packet as sent (note: it
  did not state the parameters; both breakers inferred
  them — see corrections 5 in the breaker section and
  the parameters line at the top of this report).
- `breaker-verdicts.md` — summaries of the Opus and
  Fable verdicts, 2026-10-27, both CONFIRMED.

## Open / not done

- Breaker verdict: DONE (two CONFIRMED verdicts, same
  model family — see top of this report).
- Reading the Luu/Qiu/Tye paper itself, rather than
  secondary coverage, to resolve the 7-vs-11 Gyr
  turnaround difference and to check whether the
  toy's a_max calibration matches the paper's
  best-fit parameters or a later refit.
- A contraction model that actually computes entropy
  (or states which entropy) — the piece that would
  be needed to move P-A2 out of OPEN.
- Nothing from this record is posted to any repo.
