# JEPA — act as if: predict the idea, not the pixels

An "act as if" simulation. Not the model — the *mechanism*, at a scale
where you can watch it think.

## What it is

A Joint Embedding Predictive Architecture at toy scale, with real (tiny)
learning. Scenes are 16×16 canvases: one shape (circle/square) at a random
position and size, plus pixel noise. A random 8×8 patch is masked.

- **JEPA branch:** a small MLP predicts the 4-dim LATENT `[type, x, y, size]`
  from the masked image. It predicts the *idea* of what's missing.
- **Pixel baseline:** a small MLP predicts the masked PIXELS directly.

The "encoder" is an oracle (we generated the scenes, so we know the true
latent) — standing in for a learned encoder. The *objective* (predict
representations, not pixels) is what's being demonstrated.

## What you'll see

- **P1 PASS:** JEPA's latent error (0.126) beats the pixel model's implied
  latent error (0.137). Predicting the idea beats reconstructing the image.
- **P2 PASS:** crank the noise from σ=0.05 to σ=0.40. JEPA's error stays
  ~flat (spread 0.027) — its target contains no noise. The pixel objective
  carries an irreducible σ² tax (0.0025 → 0.1600) no model can dodge.
- **The voice:** JEPA narrates from its actual prediction — "there's a
  square, left-middle, large. That's the part that was predictable, so
  that's the part I predicted. The rest is weather."
- **The plot:** original → masked → JEPA's clean render of its latent →
  the pixel model's blurry attempt.

## The point

JEPA doesn't fail at unpredictable detail — it *refuses* it, by design.
That refusal is the efficiency claim (~10× cheaper than pixel
reconstruction in the real systems): don't spend capacity on weather.

## Run it

```sh
python3 jepa.py   # trains 4 tiny MLPs, prints checks + narration, writes jepa.png
```

Takes ~3 minutes (the baseline's implied-latent grid search is the slow part).

## Files

- `jepa.py` — the simulation (numpy + matplotlib only)
- `jepa.png` — side-by-side: what JEPA sees vs what the pixel model paints
- `README.md` — this file

## Honest limits

Mechanism demo, not capability demo. Oracle encoder stands in for learned
representation; toy scenes, toy MLPs. What's on display is the *character*
of latent prediction — the refusal — not what V-JEPA 2 can do.
