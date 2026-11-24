# MARKETPLACE III — is antifragility possible?

The question: can a model GAIN from volatility, not just survive it?
Taleb's bar: fragile = harmed by disorder, robust = unaffected,
antifragile = IMPROVED by disorder (convex payoff in the stressor).

## The agent: HYDRA

Starts with warmup hypotheses. On persistent surprise (no hypothesis
explains the recent window), spawns a new hypothesis fitted to the novel
regime — and KEEPS it forever. The hypothesis set only grows. Each shock
makes it strictly more capable. (The record is eternal; selection among
hypotheses is the temporal surface — cf. FLOOR.md, PR #214.)

The price: selecting among K hypotheses costs 0.2*K per step. Optionality
is priced. Every head makes every future decision slightly more expensive.

## Two worlds

- **A:** 4 swans, each a fresh unprecedented bias (i.i.d., no meta-structure).
- **B:** 4 swans drawn from 2 recurring types (meta-structure exists).

## Pre-registered predictions

- **P1:** World B — Hydra's per-swan wealth delta improves 1→4 (learning
  curve = antifragile signature). World A — no improvement.
- **P2:** World A — Hydra ≈ JEPA (no meta-structure → robustness is ceiling).
- **P3:** World B — Hydra > JEPA (converts recurring swans to profit).

## What happened

**P1: FAILED as stated.** Per-swan deltas (World B): +174, +73, +199, +165.
Not monotonic. Swan 2 was the costly one — growing a second head.

**P2: FAILED.** Hydra (4374) >> JEPA (1661) in World A. Hydra is just a
better agent overall, not specifically antifragile.

**P3: PASSED.** Hydra (5170) > JEPA (1903) in World B.

Hydra grew heads (7 in A, 6 in B) and reused them. But the clean convex
learning curve did not emerge in 4 swans — noise dominates.

## The honest finding

Hydra is not antifragile. It is **robust and opportunistic**: it profits
from volatility (+150/swan) by engaging (growing heads, calling swans)
rather than hiding (JEPA's strategic ignorance). Better than robustness,
but not improvement-from-shocks.

True antifragility requires three things, and the experiment clarifies
each:

1. **Meta-structure in volatility.** If shocks are truly i.i.d., nothing
   can gain — robustness is the ceiling. (You cannot extract information
   from zero-information events.) Hydra did better in B than A (5170 vs
   4374), the weak signature that recurrence is exploitable.
2. **A growing hypothesis space, not just adaptive parameters.** The Gate
   adapts parameters (zero-sum: learn new = forget old). Hydra grows
   hypotheses (positive-sum: each shock adds permanent structure).
3. **Long horizons.** The learning curve needs many shocks to rise above
   noise. Four swans show the mechanism (growth, reuse) but not the
   convexity. The growth *cost* (swan 2's +73) is visible; the compounding
   benefit needs more repetitions.

The mechanism is sound; the signal needs time. Antifragility is possible
in principle, but it is a long-horizon property, and our 4-swan world was
too short to see it cleanly.

## Run it

```sh
python3 marketplace3.py   # ~2s, writes marketplace3.png
```

## Files

- `marketplace3.py` — Hydra vs Gate vs JEPA, two worlds (i.i.d./recurring)
- `marketplace3.png` — wealth in both worlds (red = swans)
- `README.md` — this file

## Honest limits

Toy energy model throughout. Hydra's novelty threshold (0.15 error, 6-step
streak) and head cap (8) are hand-tuned. The "robust and opportunistic"
vs "antifragile" distinction is conceptual; a longer run (12+ swans) could
separate them empirically. Not run here.
