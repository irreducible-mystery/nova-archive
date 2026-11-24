# Quantum Marketplace

*2026-10-15. Experiment: does interference beat selection?*
*Script: `~/workspace/act-as-if/quantum_marketplace.py` (seeded, deterministic).
Registered run: `python3 quantum_marketplace.py` → exit 1.*

## Question

The [sketch](../quantum-marketplace-sketch.md) proposed the quantum analogue of
the act-as-if zoo: Quantum Hydra holds hypothesis *superpositions* instead of
selecting among hypotheses. Interference replaces selection; decoherence
replaces erasure. Two claims were to be tested:

1. **Regime changes are free** — wrong amplitudes destructively interfere
   automatically; no rebuild needed.
2. **Interference beats selection during swans** — re-weighting by phase is
   faster than classical head-switching.

## Design

Same M4/M5 black-swan world (seed 99): 1000 bits, ~120-step regimes, 3 swans
(25 steps, biases 0.92/0.08/0.92) at t = 336, 550, 820. Scoring +6 (1-step),
+15 (10-step), +25/−10 (swan call). Bankruptcy at wealth < 0.

**Quantum Hydra** (K ≤ 8 heads, starts from 3 warmup biases):
- amplify: `α ← α·exp(i·θ·correct_k)`, correct_k = ±1 on last bit, θ = 0.3
- decohere: `α ← (1−γ)·α + γ·√p·e^{i·rand}`, γ ∈ {0.0, 0.1, 0.3, 0.5, 1.0}
- cost: `K·(0.15·(1−γ) + 0.05)`/step → 0.20·K at γ=0 (matches classical Hydra's
  0.2·K), 0.05·K at γ=1 (cheap but phase-scrambled)
- predict: **coherent** `argmax_k e_k·Re[α_k]` (e_k = 1−|windowmean−bias_k|);
  **measured** samples k∼|α_k|² and pays +0.5/step
- grow: same novelty trigger as classical Hydra (streak ≥ 6, +5.0)

Phase is the *only* learning channel (amplification preserves |α_k|), which
isolates interference as the mechanism. Baselines: classical Hydra (M3 port),
reactive, JEPA.

Two deliberate deviations from the sketch's letter, both documented:
- **Cost is γ-dependent** (0.20K→0.05K), not flat 0.15K. The sketch's P3
  ("isolation cost exceeds the interference benefit") requires a cost gradient
  in γ; flat cost would make P3 untestable. γ=0 matches classical cost exactly.
- **New-head trigger** is the classical novelty streak, not `max|α_k|² < 0.3`.
  As written that threshold fires immediately at K=8 (uniform → 0.125 < 0.3);
  the streak is the workable reading of "(like Hydra grows)".

## Pre-registered predictions — all four FAILED (exit 1)

| # | Prediction | Result |
|---|-----------|--------|
| P1 | best-γ coherent swan-acc > Hydra swan-acc | **FAIL** 0.551 vs 0.870 (best quantum swan-acc at any γ: 0.783 < 0.870) |
| P2 | Hydra calm acc-per-cost > quantum | **FAIL** 0.70 vs 2.20 (metric pathology — see below) |
| P3 | wealth(γ) peaks at interior γ ∈ {0.1,0.3,0.5} | **FAIL** best γ = 1.0 (boundary) |
| P4 | coherent beats measured in swans AND measured beats coherent in calm | **FAIL** (0.551>0.377 ✓, but 0.497>0.529 ✗) |

## Results

```
agent      | wealth | acc   | swan  | calm  | spent  | adds | alive
hydra      | 3238.0 | 0.667 | 0.870 | 0.649 |  777.0 |  2   | yes
reactive   | 3647.0 | 0.568 | 0.739 | 0.553 |    0.0 |  0   | yes
jepa       | 2087.9 | 0.627 | 0.522 | 0.637 | 1844.1 |  0   | yes
q0.0_coh   | 3139.0 | 0.632 | 0.783 | 0.619 |  777.0 |  2   | yes
q0.1_coh   | 2688.5 | 0.539 | 0.449 | 0.547 |  719.5 |  2   | yes
q0.3_coh   | 2405.6 | 0.494 | 0.406 | 0.502 |  604.4 |  2   | yes
q0.5_coh   | 2580.6 | 0.530 | 0.710 | 0.514 |  489.4 |  2   | yes
q1.0_coh   | 3269.2 | 0.531 | 0.551 | 0.529 |  201.8 |  2   | yes
q*_meas    | 2042–2671 | 0.487–0.552 | 0.348–0.594 | 0.497–0.549 | 622–1197 | 2 | yes
```

Wealth ranking: **reactive 3647 > q1.0_coh 3269 > hydra 3238 > q0.0_coh 3139 >
… > jepa 2088**. (q1.0_coh beats hydra on wealth while being much dumber —
0.531 vs 0.667 accuracy — because it pays 0.05K/step. Wealth rewards
cheapness; note for metric design.)

## The sharp finding (diagnostics, unregistered but decisive)

**θ=0 control**: Quantum Hydra with amplification turned off (θ=0, γ=0) recovers
classical Hydra *exactly*: swan-acc 0.870 = 0.870, calm-acc 0.649 = 0.649.
Turning interference on (θ=0.3) strictly hurts: swan-acc drops to 0.783.

**Seed robustness** (master seeds 20261015/7/77/777): γ=0.0 coherent swan-acc is
0.783 on *every* seed (deterministic — no randomness at γ=0). γ>0 bounces with
seed noise, best-γ alternates between 0.0 and 1.0 (never interior → P3 fails on
all seeds), and no γ on any seed beats Hydra's 0.870 (P1 fails on all seeds).

**Why interference fails here** — the phase-wrap argument, confirmed empirically:
a head correct with probability q drifts in phase at θ·(2q−1)/step and wraps
with period 2π/(θ·|2q−1|). At θ=0.3 a 75%-accurate head wraps every ~42 steps,
so inside a ~120-step regime no persistent constructive/destructive alignment
builds up — long-run ⟨Re[α_k]⟩ → 0 for every head. The coherent score becomes
*evidence × zero-mean phase noise*: classical selection plus noise. And the
binary prediction game is decided by evidence (window mean vs bias), which
classical log-likelihood selection already uses optimally. There is nothing
for phase to add.

**"Regime changes are free" is refuted**: every agent — classical and all ten
quantum variants — added exactly 2 new hypotheses. Interference substituted for
nothing; the rebuilds happened anyway.

**Measured mode is strictly dominated**: every measured variant loses to its
coherent twin on wealth, swan-acc, and calm-acc. Collapse destroys what little
the phases carry, and costs +0.5/step for the privilege.

P2's failure is a metric pathology worth recording: at γ=1.0 the agent pays
0.05K/step, so accuracy-per-cost explodes (2.20 vs 0.70) while accuracy itself
is worse (0.529 vs 0.649). Accuracy-per-cost without a cost floor rewards
cheapness, not efficiency. (The wealth ranking shows the same Goodhart.)

## What this means for the M5/M6 governance finding

It does **not** overturn "subsidize contradiction-holders" — it refines the
mechanism. This experiment tested whether *superposition itself* (cheap joint
holding of incompatible hypotheses) outperforms selection. It doesn't, at
least not with rotate-by-correctness dynamics. The M5/M6 argument was never
that superposition is smarter — it was that contradiction-holders must
**survive** selection markets so their hypotheses exist when regimes flip.
The scarce resource is *persistence across the flip*, not joint holding before
it. Notably, a quantum dynamics that *would* give phases persistent memory —
rotate-toward-fixed-point (correct→0, wrong→π) instead of constant rotation —
is exactly the analogue of what the subsidy buys economically: persistence,
not just cheap holding. That variant is the honest next experiment.

## Open follow-ups

1. Rotate-toward-fixed-point amplification (phase as memory, no wrap) — does
   interference beat selection then? **(done 2026-10-16 — see Follow-ups below;
   answer: no on swans, small calm edge)**
2. θ sweep: the wrap analysis predicts an optimal θ with wrap period ≈ regime
   length (θ ≈ 0.1 here). **(done 2026-10-16 — see Follow-ups below;
   interior local optimum confirmed at exactly 0.10, but global peak is θ=0)**
3. Fix P2's metric: accuracy-per-cost with a cost floor, or accuracy at fixed
   cost budget.
4. Shared-seed γ comparison to remove the seed confound at γ>0.

## Follow-ups (2026-10-16): θ sweep + persistent memory — 1/4 PASS (exit 1)

Script: `quantum_marketplace_followups.py` (this directory; canonical copy in
`~/workspace/act-as-if/`). Registered run: `python3
quantum_marketplace_followups.py` → exit 1. Seeds [20261015, 7, 77];
seed-invariance CONFIRMED (deterministic at γ=0 — verified, not assumed).
Base config for everything: γ=0.0, coherent prediction.

### Follow-up 1 — θ sweep, constant rotation (P1, P2)

θ ∈ {0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5}. Swan-acc: **0.870, 0.493, 0.870,
0.754, 0.652, 0.783, 0.768** — strongly non-monotonic.

- **P1 FAIL**: peak θ = 0.0 (the classical limit), not interior. But the
  interior *local* optimum among θ>0 sits at exactly **θ=0.10** — the
  wrap-theory prediction (wrap period 2π/(0.1·0.5) ≈ 126 steps ≈ regime
  length). The theory located the sweet spot correctly; its value merely
  *ties* selection instead of beating it.
- Reading, labeled as interpretation: **stale signal is worse than noise**.
  Ordering 0.05 (0.493) < 0.3/0.5 (0.78) < 0.1 ≈ 0.0 (0.870): slow phase
  drift (θ=0.05, drift ≈ π per regime for good heads) is a *systematic*,
  regime-scale distortion of the selection weights — stale trust in
  previously-good heads, which in a regime-switching world is actively
  misleading. Fast drift (θ≥0.3) is mere noise; tuned drift (θ=0.1) oscillates
  ~once per regime and averages out to classical. Interference needs its
  timescale matched to the world's timescale just to not hurt — and even
  then it cannot help.
- **P2 FAIL as stated, mechanism fully understood**: θ=0 recovers Hydra's
  *predictions* exactly — 0 direction disagreements in 840 steps, swan-acc
  0.870 = 0.870, calm-acc 0.649 = 0.649 — but wealth differs (3448 vs 3238).
  Decomposition: the entire 210-coin gap is **swan-call timing** (flags differ
  on 445/840 steps; 1-step wins, 10-step wins, and costs identical). The
  coherent predictor's classical limit uses argmax-e (window-mean distance)
  where Hydra uses argmax-ll (full-window likelihood): same directions, but
  different head *identities*, hence different novel-source flags, hence
  different ±25/−10 calls. Lesson, load-bearing for every zoo wealth ranking:
  **the swan-call component dominates wealth gaps between prediction-identical
  agents — decompose wealth before believing it.**

### Follow-up 2 — persistent memory, rotate-toward-fixed-point (P3, P4)

Pull variant: each head's phase is pulled toward 0 (correct last bit) or π
(wrong), with strength κ ∈ {0, 0.1, 0.3, 0.5, 1.0}. The pull *replaces*
constant rotation (no θ in this variant; documented in the script). κ=0
control recovers Hydra exactly (diagnostic: yes). Swan-acc: 0.870 (κ=0),
**0.870 (κ=0.1)**, 0.841 (0.3), 0.739 (0.5), 0.739 (1.0).

- **P3 FAIL**: best pull (κ=0.1, 0.870) *ties* best constant-rotation
  (θ=0.10, 0.870) — does not strictly beat it. (It beats the registered
  θ=0.3's 0.783 comfortably, but the sweep-best is the honest baseline.)
- **P4 PASS**: 0.870 ≥ 0.870 − 0.01 — matches classical Hydra on swans.
- Where the pull *does* win is **calm, not swans**: pull0.1 calm-acc 0.655 >
  Hydra 0.649 and > θ=0-baseline 0.649; wealth 3498 > 3448 > 3238. Against the
  shared e-selection baseline (θ=0), persistent memory adds +50 wealth via the
  calm edge. Phase-as-memory buys **steadiness, not flip-survival**.
- **The "survival of contradiction-holders" claim is NOT recovered**:
  n_adds = 2 for every variant in both follow-ups — regime-change rebuilds
  still happen everywhere. Nothing avoids the rebuild; the phase-space
  analogue of the subsidy does not buy what the economic subsidy bought.

### Bottom line

- Interference never beats selection. At best it ties (finely tuned
  θ=0.10), usually it hurts, sometimes it is catastrophic (θ=0.05).
- Persistent memory (pull) is the only quantum variant that adds anything,
  and it is a calm-weather value: +0.006 calm-acc, +50 wealth over the
  shared baseline. On swans it matches classical, never exceeds it.
- The quantum governance story in its strong form — superposition /
  interference as the mechanism for surviving regime flips — **does not
  survive**. What survives is weaker: phase-as-memory ≈ economic subsidy as
  *steadiness*, a calm-side effect, not a flip-side one.
- Metric lesson: the ±25/−10 swan-call component can dominate wealth gaps
  between agents with identical predictions. All zoo wealth comparisons
  should be decomposed before they are believed.

### Files (follow-ups)

- `quantum_marketplace_followups.py` — the experiment (registered run exits 1;
  seeds [20261015, 7, 77] via argv; diagnostics in /tmp, not retained)
- `followups_results.json` — predictions + per-agent metrics (primary seed)
- `followups_theta.png` — P1: swan-acc and wealth vs θ
- `followups_kappa.png` — P3/P4: pull variant vs baselines
- `followups_wealth.png` — wealth through swans: best of each family

## Files

- `quantum_marketplace.py` — the experiment (registered run: `python3
  quantum_marketplace.py`, exit 1; diagnostics: seed/prefix/θ overrides via argv)
- `quantum_results.json` — predictions + per-agent metrics
- `quantum_wealth.png`, `quantum_gamma.png`, `quantum_adds.png` — figures
- Diagnostic JSONs (`diag7/diag77/diag777/theta0_results.json`) retained in
  `~/workspace/act-as-if/` as evidence.
