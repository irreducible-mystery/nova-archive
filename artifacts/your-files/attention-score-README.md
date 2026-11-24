# Attention-score core — the load-bearing measurement

The robot piece stands or falls on one thing: can we *measure* the thing we're
going to optimize? This folder is the scoring core, built to run **before any
robot exists** — on a laptop, against synthetic tracks today and webcam footage
as soon as the perception front-end lands.

## What's here

- **`attention_score.py`** — the composite score `A(t)`:
  `w1·dwell + w2·oriented + w3·stillness + w4·proximity + w5·social`,
  per ~10-second window, **normalized by the occupancy baseline** (so the robot
  can't learn "exist in a busy gallery" instead of "be interesting").
  Phone-raised is computed as its own channel, not folded into the score blindly.
- The **`Track` dataclass** — the contract a perception front-end fills in:
  per-person, per-window aggregates (presence, facing fraction, motion energy,
  distance, social events, phone-raised fraction). YOLO/MediaPipe later is a
  drop-in, not a rewrite.
- **`fit_weights()`** — learns the weights from human "how interesting was this
  clip" ratings (constrained least squares, no sklearn needed). The robot
  learns *which kind* of attention to value; the score itself is learned.
- **`validate()`** — synthetic discrimination check with known ground truth.

Run it: `python3 attention_score.py` (needs only numpy).

## What the check shows

With neutral prior weights (stillness + orientation lead):

```
held         mean A(t) = 1.469   # 2 people, facing, still, close
grabbed      mean A(t) = 0.284   # 5 people, 3s stare, then leave
walkthrough  mean A(t) = 0.128   # 1 person crossing, not facing
empty        mean A(t) = 0.000
```

`held > grabbed > walkthrough > empty` — the discrimination the piece stands
on. The mechanism is visible in the terms: the *oriented* term separates
grabbed from walkthrough (facing, not just present — the café-effect
correction), and the *stillness* term separates held from grabbed (sustained
absorption, not a spike). Reward the held, not the grabbed.

## The calibration experiment (the first real build gate)

The synthetic check proves the scoring *machinery* discriminates. It does not
prove the score tracks what humans actually find interesting. That is the
weekend experiment, and it has to come before any robot:

1. **Collect ~30 short clips** (30–60s each) of people around *anything* —
   a street performer, a shop window, an empty plinth. Variety matters more
   than subject.
2. **Human ratings:** 3–5 raters, one question per clip — *"how interesting was
   this to the people in it?"* 1–5. Average the raters.
3. **Run the perception front-end** on the same clips → Track aggregates →
   feature rows.
4. **Fit the weights** with `fit_weights()` against the ratings. Check the
   correlation on held-out clips. If it doesn't track human judgment, the
   robot would optimize a number nobody grounded — fix the features, not the
   robot.

One honest trap, found in the demo: if the calibration set has no
high-dwell/low-attention clips (people sitting nearby texting — the café
effect), the fit learns "busy = interesting" and dwell dominates the weights.
**The calibration set must include negative examples of occupancy without
attention**, or the robot will learn to perform in crowds rather than hold a
gaze.

## What's deliberately not here

- The perception front-end (person track → head pose → motion energy). That's
  the next build step; the `Track` contract is its spec.
- The two-timescale architecture (fast intrinsic curiosity in seconds, slow
  attention in minutes, contextual bandit over behavior-modes). The score is
  the slow loop's currency; the fast loop spends a different one.
- Privacy handling (edge processing only, pose skeletons not faces, no
  storage, visible attention meter). Non-negotiable for the real build;
  out of scope for the scoring core.

## Budget note

None of this needs a Jetson. The scoring core runs on any laptop; the
perception front-end wants a webcam and, for real-time multi-person tracking,
a modest GPU or a Coral TPU — not the robot board. Buy the Jetsons when the
robots get bodies, not before.
