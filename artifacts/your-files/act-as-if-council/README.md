# THE COUNCIL — act as if: JEPA × Genie

An "act as if" simulation. Not the models — the *coordination*, at a scale
where you can watch it argue.

## What it is

Kelly's hypothesis made runnable: JEPA and Genie communicating should be
more than either alone. So they get a table.

- **The Dreamer** (Genie): an ensemble of 3 action-conditioned MLPs. Dreams
  the next state of the bouncing-ball world. Creative, sloppy at walls.
- **The Seer** (JEPA): action-conditioned, predicts the GIST (4×4 region +
  speed) from history. Deliberately blurry.
- **The Council**: the Dreamers propose 8 candidates; the Seer scores each
  by gist-match; the council takes the best. Generation checked by prediction.

## What happened

- **P1 FAIL:** the council (0.215) loses to the solo ensemble mean (0.162)
  over 30-step rollouts.
- **P2 PASS:** the anti-council (deliberately pick the Seer's *worst*
  candidate, 0.309) is worse than solo — the Seer's signal is real, not
  decoration.
- **Oracle test:** even a perfect Seer (true gist) scores 0.187 — still
  worse than the mean.

## The finding

Picking one dream keeps its noise; averaging cancels noise. When candidates
are unbiased variations, the mean wins mathematically — selection can only
win when candidates have *different biases* and the verifier can tell them
apart. The AND needs genuinely different knowledge (a second sensor, a test
suite, a physics checker), not a blurrier view of the same data.

Kelly's hypothesis survives, refined: coordination helps when the parties
bring independent ground truth. Two heads are better than one only if they
look at different things.

## The session

The script ends with a real deliberation, narrated from actual numbers —
the Dreamer's proposal, the Seer's gist forecast, all 8 candidates scored,
the pick, and the epilogue.

## Run it

```sh
python3 council.py   # trains 4 MLPs, runs checks, stages the argument
```

Takes ~75 seconds. numpy only.

## Files

- `council.py` — the whole thing: physics, training, checks, dialogue
- `README.md` — this file

## Act II — council2.py: genuinely different knowledge, then fusion

Raised separately: Dreamer on center-only data (wall-blind by upbringing),
Seer on wall-only data (center-blind). Selection STILL failed (P1/P2 FAIL) —
different knowledge alone doesn't fix a weak mechanism. But FUSION (Seer's
decoded gist entering the prediction near walls) PASSED: 0.1455 vs 0.1522
solo. The knowledge was complementary; selection was the wrong mechanism.
The AND works fused, not filtered.

## Honest limits

Mechanism demo, not capability demo. The negative results are results —
they refine rather than refute the coordination hypothesis. Full three-act
arc (selection fails twice, fusion wins) in council.py + council2.py.
