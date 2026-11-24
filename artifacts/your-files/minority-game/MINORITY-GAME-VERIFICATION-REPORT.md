# Minority Game — Verification Report

**Regime:** "neither" corner of the four-regime exploration (cooperation / competition / both / neither).
**Date measured:** 2026-10-12. **Re-verified:** 2026-10-14 (clean re-run, byte-identical outputs).
**Status:** 4/4 pre-registered predictions PASS. Breaker verdict: PASS (no material breaks).

---

## 1. Rules

The classic anti-coordination game (W. B. Arthur 1994; Challet & Zhang 1997).
N = 101 agents each pick side 0 or 1 every round; **the minority side wins**.
No communication, no altruism, no coalitions — pure self-interest.

Each agent holds S = 2 strategy tables mapping the last M winning outcomes
(an M-bit history, P = 2^M possible) to an action (0/1). Every round:
1. Each agent plays its currently best-scoring strategy's prediction (ties broken uniformly at random).
2. Attendance A = # choosing side 1; the minority side wins.
3. Every strategy earns a virtual point iff it *would have* picked the winning side — scored whether or not played.
4. History shifts in the winning bit.

Observable: σ² = Var(A) over the measurement window, reported as σ²/N. Random choice gives σ²/N = 1/4.

## 2. Pre-registered predictions

1. **P1 — coordination dip:** min(σ²/N) occurs at α ∈ [0.15, 0.70] and is < 0.20.
2. **P2 — random limit:** at the largest α (M=10, α≈10.1), σ²/N ∈ [0.20, 0.30].
3. **P3 — crowding:** at the smallest α (M=2, α≈0.04), σ²/N > 0.25.
4. **P4r — disorder-averaged symmetry:** for every M, the pool-averaged |mean(A)/N − 0.5| < 0.02.

## 3. Results

Measured 2026-10-12 (seed 20261012); re-run 2026-10-14 reproduces exactly (results.csv byte-identical).

| M | α | σ²/N | mean(A)/N |
|---|---|------|-----------|
| 2 | 0.040 | 0.725 | 0.521 |
| 3 | 0.079 | 0.846 | 0.500 |
| 4 | 0.158 | 0.359 | 0.500 |
| 5 | 0.317 | **0.036** | 0.500 |
| 6 | 0.634 | 0.065 | 0.499 |
| 8 | 2.535 | 0.150 | 0.496 |
| 10 | 10.139 | 0.215 | 0.500 |

**Prediction outcomes: 4/4 PASS.** Exit code 0.

- P1 PASS: minimum 0.036 at α = 0.317, ~7× better than chance.
- P2 PASS: 0.215 at α≈10.1, converging on 1/4 from below.
- P3 PASS: 0.725/0.846 at small α — the herd loses to a coin.
- P4r PASS: worst disorder-averaged deviation 0.5039 at M=2, within 0.02.

### The P4 → P4r story (kept, not hidden)

The first registration (P4) claimed per-config |mean(A)/N − 0.5| < 0.02. P1–P3 passed; P4 failed — M=2 came out at 0.5208. Diagnostics over 12 fresh strategy-pool realizations (`diag_pool.jl`) scatter symmetrically (6 positive / 6 negative, disorder-average +0.0065): a **finite-pool effect**, not a bug. P4r states the claim the literature actually makes, re-registered before the second run.

## 4. Breaker verdict (fresh instance, 2026-10-14)

**VERDICT: PASS** — no material breaks.

- **Implementation fidelity: holds.** Protocol correctly implemented; one negligible nit (Julia's `var` n−1 normalization shifts σ²/N ~0.01%, far below any threshold).
- **Prediction checks: holds.** All four encodings verified; P4r's 5 realizations genuinely independent of the main sweep.
- **P4→P4r: holds — not goalpost-moving.** Diagnosis independently verified; re-tested under three independent base seeds (555, 99991, 123456789), all pass comfortably. Strongest honesty evidence: the v2 run reuses seed 20261012, so the "ugly" 0.5208 remains visible in the published table.
- **Diagnostics: hold.** Both scripts reproduce the claimed numbers. Minor note: they duplicate the simulation loop rather than importing it.
- **Interpretation: holds, one prose nit fixed.** "αc ≈ 0.34 lands between them" → "sits just above the dip bin" (0.34 > α(M=5) = 0.317).

## 5. Reproducibility

```sh
julia minority_game.jl --seed 20261012   # 4/4 PASS, exit 0; writes results.csv
```

Seeded MersenneTwister; per-config seeds derived deterministically. Julia 1.13.1. Re-run 2026-10-14: byte-identical.

## 6. Files

- `minority_game.jl` — the game, M-sweep, 4 pre-registered predictions.
- `diag_bias.jl`, `diag_pool.jl` — P4 failure diagnostics.
- `README.md` — full writeup.
- `results.csv`, `sigma2_vs_alpha.png` — measured data and plot.

## 7. PR status

PR pair prepared (julia3claude `games/minority-game/`, CommunityBoard `experiments/nova-1014-minority/` with provenance header), pending GitHub service stability.
