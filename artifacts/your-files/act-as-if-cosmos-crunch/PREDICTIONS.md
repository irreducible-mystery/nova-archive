# Big Crunch cosmos — predictions, written 2026-10-27 BEFORE any run

Two new dark-energy floors added to the COSMOS toy (original
cosmos.py untouched; this is a standalone extension in this
folder). Original floors A/B/C are not re-run here except as
the baseline that da/dt > 0 always held for them.

## Floor D — Cornell axion + negative Λ, toy representation

Primary anchor (secondary reports of Luu, Qiu, Tye, "The
Lifespan of Our Universe", 2025, via DES/DESI fits):
ultralight axion + negative cosmological constant; best-fit
scale factor grows to a_max ≈ 1.69, then reverses;
total age ≈ 33.3 Gyr (crunch ~20 Gyr from now). Turnaround
time is reported as ~11 Gyr from now in the August 2026
benchmark summary and ~7 Gyr from now in July 2025
reporting — a version/fit difference, recorded here, not
smoothed. Total age 33.3 Gyr is the anchor used below.

Toy representation (NOT the full axion field equations):
flat Friedmann with dark-energy density factor
f(a) = 1 − α·ln(a), α = 2.085, chosen so that E²(a) = 0
at a ≈ 1.69 (the turnaround condition). This is a
calibration, not a prediction: a_max is fixed by α.
What is NOT fixed by α, and is therefore tested, is
the total age that results from integrating this
Friedmann model through contraction.

- P-D1 (arrow reversal, dynamical): Floor D reaches
  da/dt < 0 for a sustained interval after turnaround,
  and da/dt changes sign exactly once (expansion →
  contraction), ending at a → 0 (crunch proxy a = 1e-3).
- P-D2 (Cornell total age): Floor D's total age
  (expansion to turnaround + contraction to a = 1e-3)
  is within ±3 Gyr of 33.3 Gyr.
- P-D3 (turnaround time): turnaround occurs within
  ±3 Gyr of 24.8 Gyr total age (13.8 + 11, the benchmark
  summary) — i.e. t_turn in [21.8, 27.8] Gyr.

## Floor E — EPJC no-crunch quintessence, toy representation

Primary anchor: Myrzakulov, Hussain, Shahalam (2026),
"Nonminimally coupled quintessence with double
exponential potential: observational evidence against
big crunch singularity", Eur. Phys. J. C 86(9), 1055,
DOI 10.1140/epjc/s10052-026-16306-7. Data-preferred
couplings steer away from collapse: the field freezes
at an attractor, Hubble derivative vanishes, Ω_de → 1,
effective equation of state → −1, a de Sitter endpoint;
variants strongly disfavored vs ΛCDM, and the model
remains phantom-free.

Toy representation (NOT the full nonminimally coupled
field equations with coupling ξ and double-exponential
potential): flat Friedmann with effective equation of
state w(a) = −1 + 0.2/a, so w = −0.8 today (a = 1) and
w → −1 as a → ∞, giving ρ_de(a) = exp(−0.6·(1 − 1/a))
in units of today's density, and H → constant at late
times (de Sitter endpoint).

- P-E1 (no reversal): Floor E never reaches da/dt < 0;
  da/dt > 0 for all t in the run, to a = 1e3.
- P-E2 (de Sitter endpoint): Floor E's effective w → −1
  (within 0.01 by a = 100) and H approaches a constant
  (within 5% of its a = 1e3 value by a = 100).

## The entropy arrow — what this experiment can and cannot say

Operational arrow in this experiment = sign(da/dt),
the dynamical arrow. The thermodynamic arrow (entropy,
second law) is NOT computed by any Friedmann toy here
— the original COSMOS README says so explicitly, and
this extension does not change that.

- P-A1: The dynamical arrow reverses in Floor D
  (da/dt changes sign) and persists in Floor E
  (da/dt > 0 always). This is falsifiable from the
  scale-factor evolution alone.
- P-A2: Whether the thermodynamic entropy arrow
  survives contraction is OPEN after this run, not
  PASS or FAIL. A da/dt reversal does not, by itself,
  prove entropy reverses (entropy is not in the
  model), and a da/dt persistence does not prove
  entropy increases (entropy is not in the model
  either). Any claim that this run settles the
  thermodynamic arrow is unsupported — say so in
  the record, do not rescue it.

Scoring: P-D1, P-D2, P-D3, P-E1, P-E2, P-A1 are scored
PASS/FAIL from measured numbers. P-A2 is recorded as
OPEN by design. Overall label for the record is decided
by a fresh-instance breaker (not run here) and is
OPEN until that verdict returns — this record must not
be called CONFIRMED, RESISTED, or verified on the
author's say-so alone.
