# Calibration clips package — three-robot art piece

**Ready for your review. Nothing here is filmed, validated, or running on a
physical robot.** This package assembles the existing toy simulations and the
full stack spec into the clip set the attention measurement gate needs, so you
can review the gate clip by clip. No new simulation runs were made for it, and
no clip below is claimed footage — Part A is the synthetic reference set the
scoring core already checks itself against, and Part B is the real-world clip
set to collect, exactly as the calibration protocol specifies it.

## The measurement being gated

The robots will learn from an attention score, `A(t)`, built from five
per-window terms: dwell, oriented (facing), stillness, proximity, and social —
normalized by the room's occupancy baseline, so a busy room alone can't score
high. Phone-raised is tracked as its own channel, not folded in blindly. The
gate question is simple and load-bearing: **does this score track what humans
actually find interesting, or only what the machinery can count?** The synthetic
check proves the machinery discriminates; only human-rated clips can prove the
score means what it claims.

## Part A — Synthetic reference clips (already exist, from the scoring core)

These four cases are the discrimination the piece stands on. Each is paired
with the behavior it checks and the score the core already produces with
neutral prior weights (stillness + orientation lead).

| Clip | Attention behavior it checks | What the core scores | Pass looks like |
|---|---|---|---|
| **Held** — 2 people, facing, still, close | Sustained absorption: attention *kept*, not just caught | mean A(t) = 1.469 | Scores highest of the four |
| **Grabbed** — 5 people, 3-second stare, then leave | Cheap attention: a spike of facing that doesn't hold | mean A(t) = 0.284 | Below held, above walkthrough — the oriented term must not let a spike pass as holding |
| **Walkthrough** — 1 person crossing, not facing | Occupancy without attention: presence that isn't looking | mean A(t) = 0.128 | Below grabbed — facing, not just presence, must separate it |
| **Empty** — nobody there | The floor: no people, no score | mean A(t) = 0.000 | Zero, exactly |

**Gate check for Part A:** held > grabbed > walkthrough > empty, in that
order. If grabbed ever beats held, the score is rewarding the spike, and the
robot would learn to grab gazes instead of holding them.

## Part B — Real-world clips to collect (~30, 30–60 seconds each)

From the calibration protocol. Variety matters more than subject: the point is
to cover the behaviors in Part A *as humans actually show them*, including the
cases where the machinery would be fooled. Raters watch each clip once and
answer one question — *"How interesting was this to the people in it?"*,
1 (not at all) to 5 (riveted) — rating the people's interest, not their own.
Annotate before looking at the ratings if you can: annotate blind, fit
sighted. One annotator for the whole batch, so one consistent bias is
partially absorbed by the fit.

| Clip kind | Target count | Examples from the protocol | Attention behavior it checks | Pass looks like |
|---|---|---|---|---|
| **Positive** (`pos`) | ~8 | Street performer, busker crowd, shop-window gawkers | Held attention in the wild: people facing, still, staying | High human ratings (4–5); the fitted score tracks them, not just headcount |
| **Mixed** (`mixed`) | ~6 | Market browsing, gallery visitors drifting | Partial attention: drifting, half-facing, coming and going | Mid-range ratings; the score must sit between positive and negative, not collapse to either |
| **Negative** (`neg`) — load-bearing | ~6 | People sitting near something, ignoring it: café tables by a screen, a queue facing away, commuters by an ad | High dwell, low attention — the café effect: occupancy without interest | Low ratings despite long presence. **If this row is missing or weak, the fit learns "busy = interesting" and dwell dominates the weights — the robot would learn to perform in crowds.** The audit for this is built in: refit without the negatives and watch how much the dwell weight rises. A big rise means the negatives did their protective job. |
| **Empty** (`empty`) | ~4 | Empty plinth, waiting room, closed shop | The real-world floor: a thing with nobody attending to it | Low ratings, near-zero scores — the baseline the rest is measured against |
| **Wildcard** | ~6 | Whatever surprised you | Whatever the matrix didn't predict: the behavior that breaks the feature set | Rated and annotated like the rest; if the fit fails here, that's information, not noise — it says which feature is missing (a gaze channel? a return-visitor term?) |

**Privacy rule for Part B, from the protocol:** film consenting adults or
public events only. What you keep is the *tracks* (aggregates: presence, facing
fraction, motion energy, distance, social events, phone-raised fraction), not
faces. After annotation, keeping the video is your call — the tracks are the
artifact.

## The gate itself — pass criteria (all four, from the protocol)

1. **≥ 15 clips** with both tracks and ratings (fewer is a pilot, not a verdict).
2. **Inter-rater agreement ≥ 0.4** (mean pairwise correlation across 3–5
   raters). Below that, the human signal is too noisy to learn from — re-pilot
   with 5 clips and tighter instructions before scaling up.
3. **Held-out correlation r ≥ 0.5** — predicted score vs. mean human rating on
   the unseen third of clips. This is the verdict.
4. **No single weight above ~0.6** — a one-term score is a brittle score.

## Honest failure modes (also from the protocol)

- **Low agreement:** humans don't agree on "interesting" for these clips.
  Narrower clip selection or more raters; don't average noise and call it
  signal.
- **Low held-out r:** the features don't capture what humans see. This is the
  experiment *working* — it just falsified this feature set. Fix the features,
  not the robot's policy.
- **Dwell dominates:** the café negatives were missing or weak. Re-shoot the
  negative row; don't tune around it.

## What passing buys, and what it doesn't

Passing buys the next build step: the perception front-end (person tracking →
head pose → motion energy), for which the track record is already the contract.
It does **not** validate attention measurement as complete, it does not claim
anything about physical robots (none exist yet in this build), and the venue's
occupancy baseline is estimated separately, in the real room, in a neutral
behavior mode — it is not fit here.

## Sources drawn on (existing work only)

- The attention-score core and its synthetic discrimination check (held /
  grabbed / walkthrough / empty, with the score means above).
- The calibration protocol: ~30-clip matrix, 3–5 raters, annotate-then-fit
  procedure, pass criteria, and failure modes.
- The full stack spec for the three-robot piece: one edge computer per robot
  so the three minds stay separate, small online learners (no foundation model
  in the control loop), attention validated on webcam footage before any robot
  is built, charging-dock / nightly replay consolidation as "dreaming."

## Review checklist for you

- [ ] The clip matrix above (positive / mixed / negative / empty / wildcard)
      is the set you want collected.
- [ ] The negative row stays load-bearing — no calibration without the café clips.
- [ ] The four pass criteria are the gate you want held to.
- [ ] Anything you'd change before this becomes the collection brief.

*Package assembled 2026-11-01 from existing simulations and spec only. No new
runs, no filmed footage, no validation claim, nothing posted elsewhere.*
