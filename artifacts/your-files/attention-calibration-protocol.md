# The calibration experiment — turnkey protocol

The attention-score core (see `../attention_score.py` and its README) proves the
scoring *machinery* discriminates held from grabbed from walkthrough on synthetic
tracks. It does not prove the score tracks what humans actually find interesting.
This packet is the first real build gate, as a weekend-sized procedure Kelly can
run: **collect clips → get human ratings → annotate tracks → fit and test.**

Everything here runs with the Python standard library only. No sklearn, no
OpenCV, no webcam needed yet. The annotation is manual — deliberately. The CV
front-end comes later; manual tracks are the bridge, and one annotator's
consistent bias is partially absorbed by the fit.

## What this packet contains

- `annotate.py` — keyboard-driven annotator. Walks a clip window by window
  (10 s), asks a compact set of questions per person, writes per-window Tracks
  (`tracks.jsonl`) and per-clip feature rows (`features.csv`) using the real
  `correlate()` from the scoring core.
- `run_calibration.py` — takes `features.csv` + `ratings.csv`, fits weights with
  the real `fit_weights()`, and reports: inter-rater agreement, learned weights,
  held-out correlation, and the café-effect audit.
- `clips_template.csv` / `ratings_template.csv` — copy and fill in.

## Phase 1 — collect ~30 clips (30–60 s each)

Variety matters more than subject. Aim for this matrix:

| kind     | target | examples                                              |
|----------|--------|-------------------------------------------------------|
| `pos`    | ~8     | street performer, busker crowd, shop-window gawkers   |
| `mixed`  | ~6     | market browsing, gallery visitors drifting            |
| `neg`    | ~6     | **people sitting near something, ignoring it** — café tables by a screen, a queue facing away, commuters by an ad |
| `empty`  | ~4     | empty plinth, waiting room, closed shop               |
| wildcard | ~6     | whatever surprised you                                |

The `neg` row is load-bearing: these are the high-dwell, low-attention clips
that stop the fit from learning "busy = interesting" (the honest trap in the
README). A calibration set without them is worse than useless — it teaches the
robot to perform in crowds.

**Privacy:** film consenting adults or public events only. What you keep is the
*tracks* (aggregates: presence, facing fraction, motion energy…), not faces.
After annotation, keeping the video is your call — the tracks are the artifact.

Fill in `clips.csv`: `clip_id,file,seconds,kind`. `seconds` is optional —
`annotate.py` will ask `ffprobe` if the file exists.

## Phase 2 — human ratings (3–5 raters)

One question per clip, watched once, no conferring, order randomized per rater:

> *"How interesting was this to the people in it?"* — 1 (not at all) to 5 (riveted)

Rate the *people's* interest, not your own. Record in `ratings.csv`:
`clip_id,rater1,rater2,rater3` (add columns for more raters; use 1–5, blank for
"didn't watch"). Annotate *before* looking at the ratings if you can — annotate
blind, fit sighted.

## Phase 3 — annotate tracks

```bash
python3 annotate.py clips.csv
```

Watch each clip in any video player, paused at each 10 s window. The annotator
prompts per window:

```
[cafe_03 / window 2 of 5] people in zone (n, 'skip', 'back', 'quit'): 2
  person 1 — presence facing motion(0-4) dist(m) social phone: 1.0 0.1 2 1.2 0 0.8
  person 2 — presence facing motion(0-4) dist(m) social phone: 0.6 0.0 3 2.5 0 0.0
```

Field meanings (same contract as the `Track` dataclass):

- `presence` 0–1: fraction of the window the person was in the zone
- `facing` 0–1: fraction of present time facing the thing
- `motion` 0–4: 0 statue · 1 settled · 2 shifting · 3 fidgety · 4 pacing
- `dist` meters to the thing (estimate; near/mid/far ≈ 1.5 / 3 / 5)
- `social` count of social events (pointing, laughing, dragging a friend over)
- `phone` 0–1: fraction of present time with phone raised

One person should annotate the whole batch — consistent bias beats mixed bias
here. Expect ~150–200 windows for 30 clips; do it in 2–3 sittings. `back`
redoes a window; `quit` saves progress and exits.

Output: `tracks.jsonl` (the raw record) and `features.csv` (per-clip means of
`dwell, oriented, stillness, proximity, social`, plus `kind` and a
not-fit `phone_mean` diagnostic).

## Phase 4 — fit and test

```bash
python3 run_calibration.py features.csv ratings.csv
```

The runner reports four things:

1. **Inter-rater agreement** — mean pairwise correlation across raters.
   Below ~0.4 the human signal is too noisy to learn from: the question was too
   vague or the clips too ambiguous. Re-pilot with 5 clips and tighter
   instructions before scaling up.
2. **Learned weights** — from the real `fit_weights()` on 2/3 of clips.
   The robot learns *which kind* of attention to value.
3. **Held-out correlation** — predicted score vs mean human rating on the
   unseen 1/3. This is the verdict: **r ≥ 0.5** means the score tracks human
   judgment well enough to optimize. Below that, the honest move is to fix the
   *features* (a gaze-saccade channel? a return-visitor term?) — not the robot.
4. **Café-effect audit** — refits *without* the `neg` clips and reports how
   much the `dwell` weight rises. A big rise means the negatives were doing
   their protective job. If removing them changes nothing, your `neg` clips
   weren't negative enough — go film a café.

## Pass criteria (all four)

- ≥ 15 clips with both tracks and ratings (fewer is a pilot, not a verdict)
- inter-rater agreement ≥ 0.4
- held-out r ≥ 0.5
- no single weight above ~0.6 (a one-term score is a brittle score)

## Honest failure modes

- **Low agreement:** humans don't agree on "interesting" for these clips.
  Narrower clip selection or more raters; don't average noise and call it signal.
- **Low held-out r:** the features don't capture what humans see. This is the
  experiment *working* — it just falsified this feature set. Add or change
  correlates, don't tune the robot's policy against a dead metric.
- **dwell dominates:** the café negatives were missing or weak. The robot
  would learn "find crowds," not "hold gazes." Re-shoot the `neg` row.

## After the gate

Passing calibration buys the next build step: the perception front-end
(YOLO/MediaPipe → head pose → motion energy), for which the `Track` dataclass
is already the contract. The venue's occupancy *baseline* (the normalization in
`score_window`) is estimated separately, in the real room, in a neutral
behavior mode — it is not fit here.
