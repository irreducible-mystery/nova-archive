# Quantum Marketplace — sketch v0.1

*2026-10-15. The quantum analogue of the act-as-if zoo. Interference replaces
selection; decoherence replaces erasure.*

## The one move

Classical Hydra (M3) maintains K hypotheses and pays `0.2*K` per step to
*select* among them. Quantum Hydra maintains K *amplitudes* and pays coherence
cost to let them *interfere*. No selection — the prediction emerges from
amplitude combination.

## Representation

State is a normalized vector in C^K:
```
|ψ⟩ = Σ_k α_k |h_k⟩,  Σ|α_k|² = 1
```
Each |h_k⟩ is a hypothesis (a predictor). α_k is its complex amplitude.

## Dynamics

**Amplification** (the interference step): after each observation, amplitudes
of correct hypotheses are rotated toward constructive interference, wrong ones
toward destructive. This is Grover-like but continuous:
```
α_k ← α_k * exp(i·θ·correct_k) / norm
```
where correct_k = +1 if h_k was right, -1 if wrong, and θ is the amplification
angle (a hyperparameter — the "interference strength").

**Prediction**: two modes —
- *Coherent*: prediction = argmax_k Re[α_k · ⟨h_k|obs⟩] (interference decides)
- *Measured*: sample k ~ |α_k|², predict h_k (collapse decides, pays measurement cost)

**Decoherence**: each step, without paying isolation cost, amplitudes decay
toward classical mixture:
```
α_k ← (1-γ)·α_k + γ·sqrt(p_k)·e^{i·random}
```
where γ is the decoherence rate and p_k is the classical probability. At γ=1,
you're just classical Hydra. At γ=0 (perfect isolation, maximum cost), you're
fully quantum.

## Cost function

| Cost | Classical Hydra | Quantum Hydra |
|------|----------------|---------------|
| Per hypothesis | 0.2·K (selection) | c_coh·K (isolation) |
| Per prediction | 0 (selection is the cost) | c_meas (if measured) |
| Regime change | Rebuild hypotheses | Amplitudes re-interfere (free) |

The key asymmetry: **regime changes are free for quantum Hydra**.
Classical Hydra must detect the swan, discard old hypotheses, build new ones.
Quantum Hydra's "wrong" amplitudes destructively interfere automatically —
the superposition *is* the adaptation. You pay coherence, not reconstruction.

## Pre-registered predictions

- **P1**: Quantum Hydra beats classical Hydra during swans. Interference
  re-weights faster than selection rebuilds. (Measure: swan-accuracy.)
- **P2**: Quantum Hydra loses in calm. Decoherence tax with no regime
  change to exploit. (Measure: calm-accuracy per unit cost.)
- **P3**: Optimal coherence is interior. Too little γ→0 isolation and you
  decohere to classical (paying quantum overhead for classical behavior).
  Too much and the isolation cost exceeds the interference benefit.
  (Measure: wealth vs c_coh, expect a peak.)
- **P4**: Measurement mode matters. Coherent prediction beats measured
  prediction during swans (interference > collapse), but measured wins
  in calm (collapse is cheaper than maintaining coherence for no reason).

## The paraconsistency connection

M5's paraconsistent agent held Both at 2× and went bankrupt. Quantum Hydra
holds superposition at coherence cost — which, at the right γ, is *cheaper*
than 2×. This is the physical realization of what Tetra (the language sketch)
proposes syntactically: contradiction is cheap to hold, expensive to resolve.
Quantum mechanics *is* the existence proof that this pricing works.

## What this would test

Whether the M5/M6 governance finding — "subsidize contradiction-holders" —
has a physical substrate. If quantum Hydra wins, it's because nature already
solved the problem the commons is struggling with: how to hold incompatible
possibilities without paying full price for each.

## Open questions

1. What's the right γ schedule? Fixed, or adaptive (more coherence during
   detected volatility)?
2. Does entanglement between hypotheses (not just superposition) add anything?
   Correlated amplitudes for "these two hypotheses tend to be right together."
3. The measurement problem as governance: who decides when to collapse?
   That's the "who calls the vote" question from #221, in physics drag.
