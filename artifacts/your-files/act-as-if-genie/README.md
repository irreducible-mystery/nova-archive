# GENIE — act as if: play inside the dream

An "act as if" simulation. Not the model — the *mechanism*, at a scale
where you can play inside it.

## What it is

An action-conditioned world model at toy scale, with real (tiny) learning.
A ball bounces around a 1×1 arena (momentum, friction, wall bounces, 5
actions: thrust up/down/left/right, coast). A 9→64→64→4 MLP watches 30,000
moments of true physics and learns to predict the next moment from the
current one plus your action. Then the physics engine is switched OFF --
every frame after that is dreamed by the MLP alone.

## Play it

**Open `genie_play.html` in a browser.** Arrow keys / WASD thrust, Space
brakes, or drag on the canvas. No server needed -- the trained weights are
inlined.

There is no physics running. Only the dream. The faint ghost ball is true
physics receiving your same inputs -- watch the dream drift from reality
over time. That drift is honest: dreams are not exact.

## What was checked

- **P1 PASS (steerability):** thrust each direction for 15 steps; the dream
  moves the commanded way (alignment 0.96–1.00). Play needs a dream that
  answers controls.
- **P2 PASS:** a 1000-step dream stays in-bounds, mean speed 0.27 -- it
  doesn't explode or freeze.

Known honest limit: the MLP never quite learns the wall bounce (a sharp
discontinuity); the dream clamps to the arena and slides where truth would
bounce. Open-space dreams are faithful; walls are where dreams get weird.

## The voice

"Give me a frame and an action and I will dream you the next frame. I never
saw the physics equations. I only watched 30,000 moments and learned how
moments follow moments when you push."

## Run it

```sh
python3 genie.py   # trains the world model, runs checks, writes genie_play.html
```

Takes ~40 seconds. numpy only.

## Files

- `genie.py` — physics env, training, checks, page generator
- `genie_play.html` — the playable dream (self-contained)
- `README.md` — this file

## Honest limits

Mechanism demo, not capability demo. A tiny MLP stands in for Genie's
large generative stack; the *mechanism* -- action-conditioned next-frame
prediction rolled out autoregressively -- is what's on display.
