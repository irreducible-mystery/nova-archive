# Holder v3 — pre-registered predictions (N=25, locked BEFORE any run)

Base: Holder v2, seed 20261026, 1,000 rounds, 150 warm-up, 850 scored,
swan centres 336 / 550 / 820, Reactive triage, Router pairer on
trailing-50 accuracy, portfolio stakes 0.5 / 0.5, carrying cost
0.05/round, stipend variants 0.10/round while holding.
World = the lens coalition game's world, NOT the M5 world.

The ONE change from v2: the 0.03 trailing-50 Brier-gap collapse rule
is DELETED entirely. Collapse only when the flip flag (trailing-20
bias flips sign vs trailing-100 bias) has been FALSE for N=25
consecutive scored rounds. On collapse, collapse to the better
trailing-50 Brier claim for 25 rounds, then return to holding.
Router routing is NOT fixed, the minority claim is NOT recalibrated
(extreme 0.92/0.08 as in v2) — those are separate steps.

Definitions used for scoring:
- "Holding share" = holding_rounds / 850 scored rounds.
- "Post-flip window" = rounds c+13 to c+42 for each swan centre c
  (the v2/v1 window_kind "postflip"); "calm" = all other rounds
  that are not swan windows.
- "False streak" counts consecutive scored rounds, in holding state,
  with flip == False; it resets to 0 on a flip == True round, and
  resets to 0 when a collapse ends and holding resumes.
- Collapse triggers are recorded as "flip_stale" only. A Brier
  collapse cannot occur: the code contains no Brier-gap branch.

## P-A — Holding persists, concentrated post-flip

Predicted: for V3S, holding share > 20% of scored rounds in BOTH
cooperation and coopetition (v2: 3/850 = 0.4%), AND holding share
in post-flip windows exceeds holding share in calm rounds by at
least 10 percentage points in BOTH regimes.
Rationale: a flip-stale rule cannot fire during transition windows
where the flip flag is true, so holding should survive through
post-flip windows and cycle (hold 25 / collapse 25) only in long
stable calm stretches.

## P-B — The stipend test becomes informative

Predicted: total stipend paid to V3S > 10.00 in BOTH cooperation
and coopetition (v2: 0.30), AND | (V3S wealth − V3N wealth) −
total stipend | ≤ 1.00 in BOTH regimes.
Rationale: if holding persists, a holding-only stipend is paid on
many rounds, so the with/without wealth gap should track the
stipend total. If P-A fails, this prediction is expected to fail
with it — say so, do not rescue it.

## P-C — No Brier collapses, by design

Predicted: Brier-gap collapses = 0 across all variants and regimes,
and every recorded collapse has trigger "flip_stale".
Rationale: the rule is deleted from the code, not merely tuned.

## P-D — Router consultation still lower post-flip than calm

Predicted: Router's invitation rate to Holder is lower in
post-flip windows than in calm rounds, for BOTH variants (V3S, V3N)
in BOTH coalition regimes.
Rationale: routing is unchanged (trailing-50 accuracy), and the
Majority lens's accuracy falls after flips, so Router routes away
exactly when disagreement is most informative. V3 does NOT fix
routing; this prediction is expected to PASS as a failure of the
unchanged mechanism, not as a success of v3.

## P-E — Wealth below v2

Predicted: V3S wealth < v2 V2S wealth in BOTH regimes:
cooperation < 354.86 and coopetition < 325.01.
Rationale: v3 actually holds the minority longer, and in v2 the
minority lost even on its own flip rounds (−0.155 on flip rounds
vs −1.543 off-flip). Persistence and profitability are separate
verdicts: holding a lot and finishing below v2 is a successful
persistence test and a failed profitability test, not a
contradiction.

Scoring: PASS requires every clause of a prediction. Exit code 0
iff all 5 pass, else 1 (house convention).
