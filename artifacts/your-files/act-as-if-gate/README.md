# The Gate — act as if: Mamba-style selective memory

An "act as if" simulation. Not the model — the *mechanism*, at a scale
where you can watch it think.

## What it is

A faithful implementation of Mamba's selective scan (`h_t = Abar_t h_{t-1}
+ Bbar_t x_t`, input-dependent delta), run on a 95-token passage: a 40-token
story followed by 55 tokens of filler. The gate decides per token how wide
to open, driven by surprisal as a stand-in for learned salience (labeled
honestly in the code — the math is real, the salience oracle stands in for
weights).

## What you'll see

- **The gate is selective:** "lighthouse" opens it to 1.94; "the" barely
  cracks it at 0.00. Novelty writes deep; filler washes through.
- **The gate speaks:** data-driven narration of its keep/forget decisions.
- **The tension, measured:** both checks pass, but P1 (story-direction
  survival) passes *barely* — 0.230 vs 0.203. Sharp gates protect against
  noise AND impose recency bias within the story itself. The gate that
  forgets the filler also forgets the beginning.

## The brain connection

Your memory does this. You don't store everything — you selectively encode
by salience and novelty, and the rest decays. Finite state, input-dependent
forgetting, the tradeoff between holding on and letting go. The demo just
mathematizes what you already do.

## Run it

```sh
python3 mamba_gate.py   # prints checks + gate narration, writes gate.png
```

## Files

- `mamba_gate.py` — the simulation (numpy + matplotlib, no other deps)
- `gate.png` — gate openings per token + state evolution heatmap
- `README.md` — this file

## Honest limits

Mechanism demo, not capability demo. No learned weights; surprisal stands
in for training. Toy scale (6 state dims). The *character* of selective
memory is what's on display — not what a trained Mamba can do.
