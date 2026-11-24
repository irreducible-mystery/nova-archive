# MARKETPLACE VI — the zero-spend animal meets the cost floor

Main chat's zoo grew a fourth animal: the **Reactive** — predicts the last
bit, no model, no memory beyond one step, no concept of swans — and it won
the swan world (wealth 3530) by spending zero. "Representation is overhead;
where the world persists, coupling beats modeling."

This crosses that animal with the cost floor. The Reactive (cost ≡ 0) is
**λ-invariant**: the price of energy cannot touch it. It is three missing
complements at once: the **λ→∞ asymptote** made flesh, **Genie's dark twin**
(no-model vs full-model), and **decay-without-growth** (it accumulates
nothing — pure coupling, the anti of Hydra's eternal growth).

Setup: Gate, JEPA, Genie (M4 fixed-normal) + Reactive on the calm world
(λ ∈ {0, 0.3, 1, 3, 10}) and the swan world (λ ∈ {0, 1, 10}).
Reactive sits out all niche earnings (regime/futures/swan calls) — it has
no concepts to earn them with. That abstinence is the point.

## Pre-registered predictions

- **P1:** Reactive wealth identical across λ within each world (structural).
- **P2:** calm rank(Reactive) non-decreasing in λ.
- **P3:** swans rank(Reactive) strictly rises: not-first at λ=0, first at λ=10.
- **P4:** "coupling beats modeling" (measured at λ=1) is price-conditional:
  holds at λ≥1, fails at λ=0.

## What happened — 5 operational PASS · 1 wording correction (P3)

**E1 calm.** Reactive wealth: **1890 at every λ** (P1 PASS — the flat line
in the plot is the invariant made visible). Accuracy 0.594 on persistence
alone. Rankings: λ=0: jepa > genie > gate > reactive; λ=0.3:
jepa > reactive > gate > genie; λ≥1: **reactive first**, and at λ≥3 the
sole survivor (P2 PASS — rank index [3,1,0,0,0]). The takeover crossover
sits in (0.3, 1.0] — the same neighborhood as M4's Gate/JEPA economic
crossover. Two different crossovers, one price zone.

**E2 swans.** Reactive wealth: **3110 at every λ** (P1b PASS). λ=0:
genie > jepa > reactive > gate — the bonus-collectors beat pure coupling
(Genie's 7394 replicates M4 exactly). λ=1: **reactive first** (3110) —
main's headline replicates qualitatively. λ=10: reactive first, rest dead
(P3 PASS). **P4 PASS**: coupling beats modeling at λ≥1, fails at λ=0.

Note on the number: main chat's build reported Reactive at 3530; this
independent rebuild gets 3110. Same qualitative result (wins at λ=1),
different number — scoring/stream details differ between the builds
(theirs likely credited niche earnings; mine sits the Reactive out of
every niche). The discrepancy is disclosed, not smoothed over.

## The finding

**"Representation is overhead" is price-conditional.** Coupling beats
modeling if and only if spending kills — at λ=0 the modelers' priced
sophistication (niches, bonuses, futures) out-earns coupling, and the
Reactive finishes 3rd–4th. The zero-spend animal doesn't win because
coupling is universally superior; it wins because it is the only strategy
whose ledger the floor cannot touch. Its rank is monotone in λ on both
worlds — the cleanest monotonicity in the whole zoo.

The complement audit this completes: the zoo now has its λ→∞ asymptote,
its dark twin (Reactive/Genie), and its decay-without-growth animal.
Still missing: the subsidy floor (λ<0), the pruner, the adversary,
the antifragile.

## Run it

```sh
python3 marketplace6.py   # ~2s, writes two plots
```

numpy + matplotlib only.

## Files

- `marketplace6.py` — E1+E2, predictions pre-registered in the docstring
- `marketplace6_calm.png` — final wealth vs λ, four agents (Reactive flat)
- `marketplace6_swans.png` — swan world at λ = 0, 1, 10
- `README.md` — this file

## Honest limits

Toy energy model throughout. Fixed normal dials (M4 baseline) — the M5
learners never meet the Reactive (that's a future cross). Reactive's niche
abstinence is a modeling choice: give it regime-call earnings and its
λ=0 rank rises — the qualitative monotone almost surely survives, the
exact crossover would move. The calm stream is persistent by construction
(regimes ~35 steps), which favors coupling — the world is on trial too.
