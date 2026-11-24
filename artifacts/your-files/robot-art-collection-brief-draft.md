# Collection brief — DRAFT, local only, nothing posted or filmed

Derived strictly from the calibration clips package reviewed 2026-11-01
(`~/workspace/your_files/robot-art-calibration-clips-package.md`). This turns
that review package into the brief to use once Kelly approves the matrix and
gate. No new criteria added.

## What to collect

~30 clips, 30–60 seconds each:

- Positive (~8): held attention in the wild — street performer, busker crowd,
  shop-window gawkers. Expect human ratings 4–5.
- Mixed (~6): partial attention — market browsing, gallery visitors drifting.
  Expect mid-range ratings.
- Negative (~6) — load-bearing, do not skip: people near something and
  ignoring it — café tables by a screen, a queue facing away, commuters by an
  ad. Expect low ratings despite long presence. Without this row the fit
  learns "busy = interesting" and dwell dominates.
- Empty (~4): a thing with nobody attending to it — empty plinth, waiting
  room, closed shop.
- Wildcard (~6): whatever surprised you; rated and annotated like the rest.

## How to collect and rate

- Film consenting adults or public events only.
- Keep the *tracks* (presence, facing fraction, motion energy, distance,
  social events, phone-raised fraction), not faces. Keeping the video after
  annotation is Kelly's call.
- Raters (3–5) watch each clip once and answer one question: "How interesting
  was this to the people in it?" — 1 (not at all) to 5 (riveted). They rate
  the people's interest, not their own.
- Annotate before looking at the ratings where possible: annotate blind, fit
  sighted. One annotator for the whole batch.

## The gate this collection must pass (all four)

1. ≥ 15 clips with both tracks and ratings (fewer is a pilot, not a verdict).
2. Inter-rater agreement ≥ 0.4 (mean pairwise correlation across raters).
3. Held-out correlation r ≥ 0.5 — predicted score vs. mean human rating on
   the unseen third of clips.
4. No single weight above ~0.6.

Synthetic check that must also hold: held > grabbed > walkthrough > empty
(means from the scoring core: 1.469 / 0.284 / 0.128 / 0.000).

## If it fails

- Low agreement: narrower clip selection or more raters; re-pilot with 5 clips
  and tighter instructions before scaling up.
- Low held-out r: the features don't capture what humans see — fix the
  features, not the robot's policy.
- Dwell dominates: the negative row was missing or weak — re-shoot it, don't
  tune around it.

## What passing buys

The next build step only: the perception front-end (person tracking → head
pose → motion energy). It does not validate attention measurement as complete
and claims nothing about physical robots.

*Draft prepared 2026-11-01 from the package only. Awaiting Kelly's review of
the package itself before any use.*
