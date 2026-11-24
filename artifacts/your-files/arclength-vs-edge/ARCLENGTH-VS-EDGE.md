# Arclength indicator vs the Langton edge — head-to-head report

**Run:** 2026-10-14, Julia 1.13.1. Seed 20261008, 50 rules × 3 ICs per λ bin (1,200 runs).
**Result:** 3/4 pre-registered predictions passed (exit 1 — P3 failed as strictly written; see the nuance below).
**Nothing posted anywhere.** Results are local unless Kelly says otherwise.

## What was tested

The time-averaged arclength chaos indicator from [arXiv:2602.07660](https://arxiv.org/abs/2602.07660)
("Trajectory arclength reveals chaos", Jiménez-López & García-Garrido, Feb 2026):
for a trajectory, accumulate the distance traveled per step and average over time.
The paper defines it for Hamiltonian flows via the Lagrangian descriptor and
distinguishes regimes spectrally; the adaptation used here is the discrete-time
analog for the binary CA — cumulative Hamming distance between consecutive
lattice states, time-averaged, normalized per cell:

> A = (1/(L·T)) · Σ_t Hamming(state_t, state_{t+1}), T = 400 steps after 200-step burn-in.

Only the scalar indicator was implemented, not the paper's spectral (PSD) analysis.
The run used the **identical rule/IC draws** as the earlier Langton sweep (same seed,
same draw order), so arclength sits on exactly the same (rule, IC) pairs as the
damage numbers. Excess entropy E is the existing measurement (different sample:
40 rules × 2 ICs, seed 20261009) — bin-level comparison only.

## Pre-registered predictions (recorded 2026-10-14 05:57 UTC, before measurement)

- **P1** — contrast: A(m=1) < 0.05, A(m=15) > 0.30. **PASS** (0.00479, 0.41232)
- **P2** — edge location: steepest bin-to-bin rise in A across the m=11→13 gap ±1 bin
  (the gap where damage rose steepest). **PASS** (steepest rise exactly at m=11→13)
- **P3** — shape: A monotone non-decreasing, no interior peak-and-dip like E showed.
  **FAIL** as written (A crested at m=13: 0.43990, then 0.41232 at m=15)
- **P4** — Spearman rank correlation between per-bin A and damage ≥ 0.9. **PASS** (0.976)

## Numbers

| m | λ | arclength A (±SE) | excess entropy E | damage |
|---|---|---|---|---|
| 1 | 0.0312 | 0.00479 ± 0.00139 | 0.01240 | 0.00042 |
| 3 | 0.0938 | 0.05891 ± 0.00670 | 0.15253 | 0.00341 |
| 5 | 0.1562 | 0.11998 ± 0.01124 | 0.23683 | 0.00977 |
| 7 | 0.2188 | 0.18747 ± 0.01342 | 0.41384 | 0.04978 |
| 9 | 0.2812 | 0.22409 ± 0.01652 | 0.66535 | 0.08922 |
| 11 | 0.3438 | 0.32463 ± 0.01969 | 0.69780 | 0.12766 |
| 13 | 0.4062 | 0.43990 ± 0.01687 | 0.94481 | 0.22752 |
| 15 | 0.4688 | 0.41232 ± 0.02016 | 0.87094 | 0.27454 |

![Arclength vs excess entropy vs damage across the Langton sweep](arclength_vs_edge.png)

## Verdict

**Both indicators locate the same edge.** The steepest rise in arclength falls across
the m=11→13 gap (λ 0.3438→0.4062) — exactly the gap where damage rose steepest —
and excess entropy peaks at m=13. Three different quantities (geometric arclength,
information-theoretic E, perturbative damage) all put the transition in the same
place. That is the head-to-head answered: same edge.

**The surprise is the shape.** I predicted arclength would rise monotonically (it is,
after all, essentially mean activity) while E alone showed the interior peak. Instead
A crested at m=13 just like E. But — honesty requires the nuance — the dip from m=13
to m=15 is 0.0276 against a standard error of the difference of ~0.026, i.e. about
one standard error. It is **not a significant dip**; the data are equally consistent
with a plateau. So P3's strict failure is a small, non-significant violation: A rises
and then plateaus, while E's peak-and-dip stands as measured (its own standard errors
were not recorded, so I cannot say whether E's dip is significant either).

## Confounds and limits, stated plainly

1. The paper's indicator is built for Hamiltonian flows; the Hamming-arclength
   adaptation is mine. In a binary CA it coincides with mean activity — a known
   quantity — so this test asks whether a *geometric* indicator's edge matches the
   information-theoretic edge, not whether activity is a new discovery.
2. E was measured on a different rule/IC sample than A and damage; only the
   bin-level comparison is licensed.
3. Measurement is post-burn-in (attractor regime). Transient arclength was not measured.
4. The paper's spectral classification (delta vs 1/ω) was not implemented; the
   comparison is scalar-curve to scalar-curve.
5. No per-bin uncertainties exist for the E column, so E's m=13→15 dip cannot be
   significance-tested from the recorded data.

## Files

- `arclength.jl` — the measurement script (same CA core and draw order as the
  original Langton sweep; predictions evaluated in-script, exit 1 on 3/4).
- `PREDICTIONS.md` — the pre-registered predictions, timestamped before measurement.
- `arclength.csv` — per-bin mean arclength values.
- `arclength_vs_edge.png` — the three-curve comparison plot.
