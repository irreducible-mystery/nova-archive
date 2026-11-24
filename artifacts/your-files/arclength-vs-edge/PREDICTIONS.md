# Pre-registered predictions — arclength indicator vs the Langton edge

**Recorded:** 2026-10-14 05:57 UTC — before any arclength measurement was run.
**Idea:** "Pit the arclength indicator against your Langton edge" (idea_fd859b18c7324dddae9704498be32f1f)

## Setup

- Indicator: time-averaged arclength of the CA trajectory (Jiménez-López &
  García-Garrido, "Trajectory arclength reveals chaos", arXiv:2602.07660).
  The paper defines it for Hamiltonian flows via the time-averaged Lagrangian
  descriptor; the discrete-time analog used here is the cumulative Hamming
  distance between consecutive lattice states, time-averaged, normalized per
  cell: A = (1/(L·T)) · Σ_t Hamming(state_t, state_{t+1}), measured over
  T=400 steps after a 200-step burn-in.
- Only the **scalar** indicator is implemented — not the paper's PSD
  classification (delta function vs 1/ω spectrum). The head-to-head is
  scalar-curve vs scalar-curve across λ.
- Same CA setup as langton_test.jl (radius-2 binary CA, L=256, periodic,
  λ = m/32 for m ∈ {1,3,5,7,9,11,13,15}), and the **identical rule/IC draws**
  (seed 20261008, same draw order: shuffle per rule, then 3 ICs per rule —
  50 rules × 3 ICs per bin), so arclength sits on exactly the same
  (rule, IC) pairs as the existing damage numbers.
- Excess entropy E comes from the existing excess_entropy.csv (different
  sample: 40 rules × 2 ICs, seed 20261009) — bin-level comparison only.

Existing reference numbers (from the workspace, not re-measured):
- Damage means: 0.00042, 0.00341, 0.00977, 0.04978, 0.08922, 0.12766, 0.22752, 0.27454
  → steepest rise across the m=11→13 gap (λ 0.3438→0.4062).
- E means: 0.01240, 0.15253, 0.23683, 0.41384, 0.66535, 0.69780, 0.94481, 0.87094
  → interior peak at m=13 (bin 7 of 8), dipping at m=15.

## Predictions (exit 0 iff all hold)

- **P1 (sanity/contrast):** mean A at m=1 < 0.05 and mean A at m=15 > 0.30
  (per cell per step). Ordered rules barely move; chaotic rules flip roughly
  a third to a half of cells per step.
- **P2 (edge location):** the steepest bin-to-bin rise in mean A falls across
  the m=11→13 gap, ±1 bin — i.e. the same transition region where damage rose
  steepest. This is the verdict condition: P2 passing = both indicators locate
  the same edge; P2 failing = a clean negative.
- **P3 (shape divergence):** mean A is monotone non-decreasing across the 8
  bins (no interior bin exceeds the last bin by more than 0.01) — it will NOT
  show the interior peak-and-dip that E showed. If A peaks interior and dips,
  P3 fails, and that is informative, not a bug.
- **P4 (consistency):** Spearman rank correlation between per-bin mean A and
  per-bin mean damage ≥ 0.9 (both are activity-like quantities).

## Stated confounds (before seeing data)

1. The paper's indicator is for Hamiltonian flows; the CA Hamming-arclength
   is my adaptation. In a binary CA this is essentially mean activity — a
   known quantity — so the test is whether this geometric indicator's edge
   matches E's edge, not whether activity is a new discovery.
2. E was measured on a different rule/IC sample than A/damage; only
   bin-level comparison is licensed.
3. Measurement is post-burn-in (attractor regime); transient arclength would
   differ and is not measured here.
4. The PSD part of the paper (delta vs 1/ω) is not implemented; a chaotic CA
   bin could in principle be distinguished spectrally, but that is out of
   scope for this head-to-head.
