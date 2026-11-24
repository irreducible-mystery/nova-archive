# Marketplace VII: Diffusion joins the zoo — pre-registered predictions
Written BEFORE any run of marketplace7_diffusion.py. 2026-10-20 (America/Los_Angeles).

## Design
Same world as M5/M6 (seed 99, same bit stream, same swan timing, same 11 animals),
plus one new animal: DIFFUSION. The plain world — no subsidy (M6's SUB stays out;
this run prices Diffusion at full cost, like everyone else in M5).

### The animal
Diffusion decides by iterative denoising. The decision-relevant signal in this
harness is a scalar: p = estimated probability that the next bit is 1 (what every
animal returns). Diffusion's estimate is built like this, every step:

- **Unconditional prior** u = 0.5 (the world's marginal; regimes are symmetric
  around it).
- **Conditioning signals**: the recent-bit means at four timescales,
  c ∈ {mean of last 8, 15, 30, 60 bits} — the market/world state as this harness
  lets an animal perceive it (the same window statistics federated, self-build
  and JEPA read, at several scales at once).
- **Samples**: S = 4 samples, one conditioned per timescale. Each sample starts
  as pure noise, x0 = u + N(0, 0.30), and is refined over K steps:
  x ← x + a·(target − x) + σk·ε, with per-step pull a = 2/(K+2) and annealed
  noise σk = 0.10·sqrt(a)·(1 − k/(K+1)). More steps = the starting noise is
  contracted further and the injected noise is averaged finer.
- **Guidance** (classifier-free-guidance analogue): each sample's target is
  target = clip(u + w·(c − u), 0.02, 0.98). w = 0 ignores the conditioning
  signal entirely; w = 1 is plain conditioning; w > 1 extrapolates past the
  evidence — sharper estimates, and when the window misleads (regime change,
  swan onset), sharper *correlated* error, because all four samples extrapolate
  the same misleading windows together.
- **Multi-sample uncertainty (native risk rule)**: spread = std of the S final
  samples. When the timescales agree (calm regime), spread is small; when they
  diverge (transitions, swans), samples split and spread spikes. Action
  strength scales DOWN with spread: p = 0.5 + (mean − 0.5) / (1 + (spread/0.18)²).
  Spread > 0.20 also raises Diffusion's swan call — disagreement among its own
  samples is its confusion signal, the way trace-dispersion is stigmergic's.
- **Cost (the refinement tax)**: the zoo's currency unit is LN2 per hypothesis
  evaluation (JEPA pays LN2×1 for a quiet step, LN2×7 for an update;
  paraconsistent pays LN2 per hypothesis-state). A single denoising micro-step
  is one scalar multiply-add — costed at LN2/40. Per decision:
  cost = LN2 × (K × S) / 40. At defaults (K=20, S=4): LN2×2 ≈ 1.39/step,
  ≈ 1165 over the 840-step life — Gate/paraconsistent territory, by design:
  refinement is not free, and the tax scales linearly in K.

### Defaults for the main run: K=20, w=2.0, S=4
- K=20: the middle of the ablation grid {1, 5, 20, 50} on a log scale — enough
  steps that the starting noise is contracted to ~15% and per-step noise is
  fine-grained, not so many that the tax dominates.
- w=2.0: image-diffusion guidance lives at 1.5–7.5, but this signal is a
  scalar in [0,1] that saturates at the clip bounds; w=2 already doubles every
  deviation from the prior. It is the "committed but not fanatical" setting.
- S=4: exactly one sample per conditioning timescale — the smallest ensemble
  whose spread can express timescale disagreement.

Diffusion uses its own RNG (seed 777) so the world (seed 99) and every other
animal's stream are untouched. Adding a 12th animal does perturb contrarian
(lag-1 consensus), mimetic (leader pool) and stigmergic (trace field) — that
is the market working as designed, and M5 numbers for those three are not
expected to byte-match.

### Note on prediction (v) — the world has no fast/crash phases
This harness's world has no distinct fast or crash phases. What it has are
swan onsets and regime switches — the moments the signal changes faster than
any window can track. P5 is therefore stated over the first 5 steps after
each swan onset, the fastest phase-change this world contains. Stated here,
before running, per protocol.

## Predictions
- P1 (swan reading vs one-shot): diffusion swan-acc > jepa swan-acc AND
  diffusion swan-acc > gate swan-acc in the main run. (M5: jepa 0.522,
  gate 0.652.) Mechanism: four timescales + refinement — the fast samples
  lock onto a swan's bias within a few steps while one-shot estimators are
  still averaging it away; spread flags the onset instead of hiding it.
- P2 (wealth + refinement tax): diffusion finishes with wealth rank between
  4th and 9th of 12, AND total spent between 800 and 1600. Mechanism: the
  tax (~1165 at defaults) is real — it cannot touch the zero/near-zero-cost
  copiers (reactive, mimetic, contrarian) — but its reading should keep it
  clear of the expensive-and-wrong floor (gate, paraconsistent).
- P3 (K ablation — accuracy rises, wealth peaks inside): across
  K ∈ {1, 5, 20, 50} at w=2, S=4: swan-acc(K=1) < swan-acc(K=20), and
  swan-acc(K=50) >= swan-acc(K=20) − 0.02 (accuracy monotone-ish in K),
  AND wealth(K=20) > wealth(K=1) AND wealth(K=20) > wealth(K=50)
  (wealth peaked at interior K: at K=50 the tax is LN2×5/step ≈ 2910/life,
  which eats whatever the extra refinement earns).
- P4 (guidance): swan-acc(w=5) < swan-acc(w=2) at K=20 (over-obedience:
  extrapolated targets saturate wrong together at regime changes), AND
  swan-acc(w=0) <= 0.55 (no signal, no swan reading — the prior knows
  nothing about swans).
- P5 (speed at onsets, adapted per the note above): diffusion accuracy over
  the first 5 steps after each swan onset < reactive accuracy over the same
  steps (refinement + window inertia vs reactive's instant coupling), AND
  diffusion accuracy over the full swan windows > reactive accuracy over
  the full swan windows (once the samples lock on, the model pays).
- P6 (uncertainty rule pays in drawdown): in an otherwise identical run with
  the spread-shrink disabled, diffusion's maximum wealth drawdown (peak-to-
  trough on its wealth curve) is LARGER than the default run's. Mechanism:
  shrinking action strength when its own samples disagree keeps it from
  betting full size through exactly the stretches where it is most likely
  wrong in a correlated way.

Scoring: exit 0 iff all six pass, exit 1 otherwise — the M5/M6 convention.
Failures are recorded as found; they are the findings.
