# Marketplace VII: Diffusion joins the zoo

**Question:** what happens when an animal that decides by *iterative
denoising* — start from noise, refine in K steps toward a conditioned
signal, sample several times and read its own disagreement as uncertainty —
is priced by the same market that priced the copiers, the holders, and the
one-shot modelers?

**Design:** the M5 black-swan world verbatim (seed 99, same bit stream,
same swans at 336/550/820, same 11 animals), plus Diffusion as the 12th.
No subsidy. Pre-registered predictions in `marketplace7_PREDICTIONS.md`,
written before any run: **2/6 passed.** Exit code 1, per house convention —
the failures are the findings, and this time they mostly indict the
market's scoring, not the animal.

## The animal

| Diffusion concept | Marketplace implementation | Mechanism or analogy? |
|---|---|---|
| Latent signal | The scalar p = P(next bit = 1) — the only decision signal this harness has | Mechanism (it is what every animal outputs) |
| Pure-noise start | Each sample starts x₀ = 0.5 + N(0, 0.30) around the unconditional prior | Mechanism |
| Denoising steps | K iterations of x ← x + a·(target − x) + σₖε, a = 2/(K+2), noise annealed σₖ = 0.10√a·(1 − k/(K+1)) | Mechanism — the *dynamics* are real; there is no learned denoiser network, the pull is analytic |
| Conditioning | Recent-bit means at timescales {8, 15, 30, 60} — the window statistics this world's animals can actually perceive | Analogy at the edges: real conditioning signals, but hand-built, not learned |
| Classifier-free guidance | target = clip(u + w·(c − u)); w=0 ignores the signal, w>1 extrapolates past it | The arithmetic is mechanism; "classifier-free" is analogy — the unconditional branch is the constant prior, not a second model |
| Multi-sample uncertainty | S=4 samples, one per timescale; spread = their std. Timescales agree in calm, split at transitions | Mechanism |
| Uncertainty → position size | p = 0.5 + (mean − 0.5)/(1 + (spread/0.18)²): strength shrinks as spread grows; spread > 0.20 is its swan call | Implemented faithfully — and **unpriced by this market** (see Finding 3) |
| Compute cost | LN2 × (K·S)/40 per step — a denoising micro-step costed at 1/40 of the zoo's LN2 hypothesis-evaluation unit | Declared mapping, same currency as JEPA/paraconsistent |

Defaults: K=20, w=2, S=4 → cost LN2×2 ≈ 1.39/step, 1164 over the run.
Diffusion's RNG is its own (seed 777); the world and the other animals'
streams are untouched. (Stigmergic 3362→3366 and contrarian 2597→2591
moved slightly — a 12th animal changes the consensus and the trace field,
which is the market working as designed.)

## Results — main run

Wealth ranking: mimetic(3872) > reactive(3530) > stigmergic(3366) >
federated(3274) > satisficer(3196) > dialectical(2966) > selfbuild(2941) >
**diffusion(2894)** > contrarian(2591) > jepa(1947) > gate(1451) >
paraconsistent(−2, DEAD).

Diffusion: wealth **2894 (8th of 12)**, acc 0.662, calm 0.643,
**swan-acc 0.870** — the zoo's ceiling tier, tied with paraconsistent,
selfbuild, dialectical and federated — swan-call accuracy 0.83, spent 1164.

## Predictions vs outcomes (2/6)

| # | Prediction | Verdict |
|---|---|---|
| P1 | Swan-acc beats both one-shot agents (JEPA, Gate) | **PASS** — 0.870 vs JEPA 0.522, Gate 0.652 |
| P2 | Wealth rank 4–9 of 12, spent 800–1600 (the refinement tax is real) | **PASS** — rank 8, spent 1164 |
| P3 | Accuracy rises with K; wealth peaks at interior K=20 | **FAIL** — see Finding 1 |
| P4 | w=5 swan-acc < w=2 (over-obedience hurts); w=0 ≤ 0.55 | **FAIL** — half right: w=0 = 0.420 ✓, but w=5 = w=2 = 0.870 |
| P5 | Slower than reactive at swan onsets, better over full swans | **FAIL** — inverted: onset-5 accuracy 0.933 vs reactive 0.867; it was *faster* at onsets. Second clause held (0.870 > 0.739) |
| P6 | Uncertainty shrink reduces max drawdown vs no-uncertainty variant | **FAIL** — drawdowns identical to the decimal (20.6 = 20.6), wealth identical too. See Finding 3 |

## Ablations

**K (w=2, S=4):** swan-acc is **0.870 at every K** — flat. Wealth falls
monotonically as K rises: K=1 → 3951, K=5 → 3802, K=20 → 2894, K=50 → 1177.
At K=1, Diffusion would have won the entire market (3951 > mimetic 3872) —
as barely a diffusion model at all: one guided step from noise.

**Guidance (K=20):** w=0 → swan-acc 0.420, wealth 2000 (the signal is the
animal; no signal, no reading). w ∈ {1, 2, 5} → swan-acc 0.870 at all
three; wealth 2924 / 2894 / 2792 — a gentle decline, no cliff.

## Findings

1. **This market cannot see refinement.** The payoff reads only the *sign*
   of (p − 0.5), every 10th step also at a 10-step horizon. Refinement
   improves the *estimate* — its distance from the truth, its calibration —
   and the scoring is blind to all of that. Once one denoising step gets
   the direction right (and one step toward a window mean usually does),
   steps 2–50 buy nothing the market pays for, at LN2/10 per sample-step.
   The refinement tax is real; the refined product is unpriced. P3's
   failure is a measurement of the market's resolution, not of denoising.

2. **Guidance saturation is the same blindness.** w extrapolates the
   estimate's *magnitude*. Magnitude is exactly what sign-scoring throws
   away, so the predicted over-obedience harm at w=5 has nowhere to land:
   extrapolated targets saturate at the clip bounds, direction rarely
   flips, errors don't become visible as *more wrong*, only as wrong.
   To test guidance honestly this zoo would need a scoring rule that
   prices confidence (Brier-style, as M4 reported alongside wealth) —
   pre-registering that is a Marketplace VIII question, not a patch here.

3. **The uncertainty rule is inexpressible in this market — exactly.**
   The no-uncertainty variant produced a *bit-identical wealth trajectory*
   (2894, drawdown 20.6). Shrinking p toward 0.5 never crosses 0.5, and a
   market that pays on sign alone cannot distinguish a full-size bet from
   a tenth-size one. Diffusion's native risk rule — its most distinctive
   organ — is a position-sizing rule in a market with no position sizes.
   P6 didn't fail because the rule doesn't work; it failed because the
   world has no variable for the rule to act on. Recorded as found.

4. **It is fast where it was predicted slow.** P5 assumed windows +
   refinement = inertia at onsets. Instead the 8-bit timescale sample
   locks onto a swan within a step or two and drags the mean with it,
   while reactive is right only when the swan's bias happens to repeat
   the last pre-swan bit. Multi-timescale sampling is an onset *asset*:
   the fastest sample is a scout the one-shot agents don't have.

## Proposed commons role: the Refiner — assessed

The candidacy: Diffusion as the commons' refiner — take rough, noisy
first-pass estimates and return denoised ones; publish its spread as a
public confusion gauge. The evidence from this run is mixed and mostly
about the venue:

- **For:** best-tier swan reading (0.870) and a strong swan-call (0.83);
  its spread is a genuine, self-generated uncertainty signal, the thing
  M4's zoo mostly lacked; fast at onsets (Finding 4).
- **Against / unproven:** nothing in this run had Diffusion refine
  *anyone else's* estimate — as a competitor it is a mid-pack animal
  whose signature organs (refinement depth, guidance, position sizing)
  the market literally cannot price (Findings 1–3). A refiner's value
  only exists in a commons that consumes refined estimates and pays for
  calibration. This market does neither.
- **Verdict:** role plausible, **not established by this run** — and the
  run tells us why: before the zoo can employ a refiner, the market
  needs a price for estimate quality (a Brier-priced lane, or consumers
  who bet using others' p's with size). Until then Diffusion's honest
  zoo niche is what the numbers show: a cheap-at-K=1, best-tier
  swan-reader whose expensive depths are a subsidy case waiting for a
  denominated reason — the M6 pattern, one animal later.

## Honest limits

- No learned denoiser: the score/pull is analytic (toward window means).
  What was tested is diffusion *dynamics* — noise start, annealed
  refinement, guidance extrapolation, sample spread — not a trained
  diffusion model.
- Swan-acc saturates: five animals tie at 0.870, so P1's margin over
  JEPA/Gate is real but the metric has a low ceiling in this world.
- Single world, single seed set (99/1001/777), as with all M-series runs.
- Ablation runs re-run the full market each time; other animals' numbers
  inside ablation runs were not separately audited beyond diffusion's row.

## Reproduce
`python3 marketplace7_diffusion.py` — runs the main market plus the K,
guidance, and no-uncertainty ablations (~8s), writes
`marketplace7_results.json` and `marketplace7_diffusion.png`, exits 1
(2/6 predictions passed; the failures are the findings above).

## Files
- `marketplace7_diffusion.py` — M5 harness verbatim + Diffusion
- `marketplace7_PREDICTIONS.md` — pre-registered predictions (written first)
- `marketplace7_results.json` — main table, ranking, ablations, scoring
- `marketplace7_output.txt` — full run output
- `marketplace7_diffusion.png` — wealth curves + wealth-vs-K bars
