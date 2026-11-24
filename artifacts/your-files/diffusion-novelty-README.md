# The novelty dial — a checkable toy for diffusion's novelty claim

Companion to the 2026-10-13 diffusion-models brief ("novelty and noise" thread).
The brief claimed: in diffusion, novelty lives in the seed/prompt/model triad,
and the novelty dial is *how much noise you let in*. This toy makes that
checkable on a 2D mixture where everything is known.

## Setup

- Data: 4-component 2D Gaussian mixture, means at (±3, ±3), σ = 0.7.
  60 fixed "training" points — deliberately sparse, so "in the basin" and
  "on a training point" stay distinguishable.
- Score: **oracle**, closed form for the true mixture. Any copying the reverse
  process does is the process's fault, not the estimator's.
- Reverse: deterministic DDIM (η = 0). Same seed + same params = bit-identical
  output; stochasticity enters only through the starting noise.
- The dial: take a training point x_orig, forward-diffuse it to `t_start`,
  then run the deterministic reverse to t = 0. `t_start` = how much noise you
  let in. (SDEdit / img2img-strength semantics.)

## Metrics

- **d_orig**: distance from a generated point to the *specific* training point
  its noise started from. Small = the model reconstructed the image it was
  given (extraction); large = the origin was erased, output is a fresh sample.
- **d_min**: distance to the *nearest* training point (secondary: checks
  outputs stay in the learned basin at every dial setting).
- **nn_med**: median in-sample nearest-neighbor distance of the training set
  (0.348 here) — the scale training points sit next to each other.

## Predictions (pre-registered) and results — 4/4 PASS, exit 0

| # | Prediction | Result |
|---|-----------|--------|
| P1 | mean d_orig monotone increasing in t_start | PASS: 0.22 → 0.49 → 0.86 → 1.95 → 3.64 → 4.74 |
| P2 | t_start=40: median d_orig < nn_med (extraction regime) | PASS: 0.209 < 0.348 |
| P3 | t_start=500: median d_orig > 3·nn_med (novelty regime) | PASS: 5.59 > 1.04 |
| P4 | bit-identical under same seed; different under new seed | PASS (`np.array_equal`) |

## The honest nuance

`mean d_min` stays ≈ 0.3 at *every* dial setting — outputs never leave the
learned basin. The dial doesn't move you out of distribution; it moves you
from **"that training image"** to **"a new sample from the basin"**. Novelty,
here, is *which basin point*, not *whether basin*. And at t_start=40 the model
hands back the specific image it was shown — extraction, the Carlini regime,
with an oracle score and zero estimation error. Memorization is in the
process, not (only) in the learning.

## What didn't work (kept, because it's the finding)

First attempt used 500 training points and measured d_min only: the dial was
invisible — everything landed within 0.15 of *some* training point at every
setting. Dense coverage saturates the metric. That's the Carlini duplication
driver in miniature: duplication = dense covering = extraction becomes
unavoidable. The fix was measuring distance to the *originating* point, not
the nearest point.

## Run

```
python3 novelty_dial.py
```

Stdlib + numpy + matplotlib only. Writes `novelty_dial.png` (origin→output
segments at three dial settings) and `dial_curve.png` (the dial curve).
Seed fixed at 7; all randomness seeded.

## Limits

2D toy; oracle score (real models learn approximate scores from data, and
learned-score error can push copying either way); Euclidean distance in data
space, not perceptual distance; one mixture geometry. The shape of the dial
curve — monotone, with extraction at the low end — is the claim that should
survive; the exact thresholds won't.
