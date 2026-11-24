# MARKETPLACE IV — the missing lenses

Four floors absent from the zoo, in the black-swan world. Each reveals what
the others assume — not by being better, but by disagreeing differently.

## The agents

- **BAYESIAN**: 3 Beta particles (regime-switching filter). Maintains
  *distributions*, not points. Knows its uncertainty as a quantified object.
  On swans, posterior entropy spikes → declares swan, predicts 0.5.
- **EVOLUTIONARY**: 24 biases. No learning, no memory, no model. Every 50
  steps: keep fittest 12, reproduce with mutation. The *population* adapts;
  no individual knows anything. Selection is learning without a learner.
- **SOCIAL** (theory of mind): 3 experts (momentum, mean, contrarian). Models
  each expert's *hidden state* (calm/confused) via mini-Bayes on their errors.
  Trusts the calm. Second-order: models knowers, not the world.
- **REACTIVE** (embodied-minimal): predicts last bit. No model, no memory
  beyond 1 step, no concept of swans. Pure coupling. The world is its own
  best model.
- **JEPA**: robust baseline from Marketplace II (strategic ignorance).

## What happened

**REACTIVE wins (wealth 3530) by spending zero.** It doesn't understand swans,
can't conceive of them, has the worst calibration (Brier 0.432) — and profits
most. The embodied lesson, mechanized: *representation is overhead*. Coupling
beats modeling when the world has persistence.

**SOCIAL is second (2371) with the best swan detection (0.90).** Modeling
others' *confusion* detects novelty well. But it doesn't beat its best expert
(0.569 vs 0.664) — knowing *why* others are wrong doesn't make *you* right.

**EVOLUTIONARY survives (1690) with the best swan accuracy (0.754).**
Diversity works: some members happen to fit the unprecedented. But overall
accuracy is 0.480 — it *persists* without *learning*. No memory, no reuse.

**BAYESIAN is well-calibrated (Brier 0.245) but not the best** — JEPA's
*strategic* 0.5 (0.236) beats Bayes' *principled* uncertainty. Refusing to
predict can be better calibrated than predicting with uncertainty. Quantified
not-knowing costs more than strategic not-knowing.

**JEPA remains the best traditional agent** (acc 0.627). Strategic ignorance
is hard to beat.

## Pre-registered (2/4 PASS)

- P1 FAILED: evo (0.754), not reactive (0.739), best in swans. Diversity beats
  coupling for accuracy; coupling wins on cost.
- P2 FAILED: jepa (0.236), not bayes (0.245), best Brier. Surprise — strategic
  refusal calibrates better than principled uncertainty here.
- P3 PASSED: evo survives (wealth 1690). Selection without a learner works.
- P4 FAILED: social (0.569) < best expert (0.664). Theory of mind detects
  novelty but doesn't exploit it better.

## The triangulation

Each lens reveals the others' assumptions:
- Reactive reveals: *prediction doesn't need a model* (everyone else assumes it does).
- Bayes reveals: *everyone else is overconfident* (they don't represent uncertainty).
- Evo reveals: *learning doesn't need a learner* (everyone else assumes an agent).
- Social reveals: *the world contains other minds* (everyone else models only bits).

The swan, triangulated: reactive couples to it, evo's diversity absorbs it,
social detects it via others' confusion, bayes quantifies not-knowing it,
jepa refuses to pay for it. Five disagreements, one invariant: *unprecedented*.

## Run it

```sh
python3 marketplace4.py   # ~2s, writes marketplace4.png
```

## Files

- `marketplace4.py` — four new lenses + JEPA baseline, swan world
- `marketplace4.png` — wealth + calibration
- `README.md` — this file

## Honest limits

Toy costs throughout (Bayes LN2*3, Social LN2*2 — the *ratio* matters more than
the absolute). Reactive's win depends on world persistence (momentum fails in
anti-persistent worlds). Evo's 24 biases are arbitrary. Social's ToM is
minimal (3 experts, binary hidden state). The P-failures are the findings.
