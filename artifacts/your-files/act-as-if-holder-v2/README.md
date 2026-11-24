# Holder v2 — did holding disagreement pay?

**Pre-registered score: 2/5 PASS. Exit code 1, per house convention —
the failures are the findings.**

Local only. Nothing posted to GitHub, nothing merged, no coalition or
scoreboard original file changed. World = the lens coalition game's
world (seed 20261026, 1,000 rounds, 150 warm-up, 850 scored, swan
centres 336/550/820), NOT the M5 world. Deterministic: same seed,
same bits, same results.

## The headline, first

**Holding did not pay. Collapsing did.** Holder v2 spent 847 of 850
scored rounds collapsed to a single sub-account and only 3 rounds in
holding state, in every variant and regime. The collapse rule, as
specified, fires the moment a holding spell starts — because the
minority claim's trailing-50 Brier (0.5203) is almost always worse
than the majority's (0.2286) by far more than the 0.03 threshold —
so Holder v2 is, in practice, a Majority-only lens with a 25-round
collapse clock and a 3-round holding interlude. Everything below
must be read through that lens: v2 "wins" by almost never holding.

That is not a modelling accident to patch away. It is what the
decided spec produces, and it answers Kelly's question in a sharper
form than expected: under a per-round Brier-evidence collapse rule
with a 0.03 gap, a holder that keeps an extreme minority claim
cannot stay in holding state at all. A holder that *would* stay
holding needs a different collapse rule — a much larger gap, a
different evidence window, or a collapse trigger that is not Brier
at all (for example, the minority claim's own flip condition
firing). That is the next design question, recorded below, not
built here.

## Results — all runs, same world

| run | Holder wealth | rank | Holder mean payoff/round (excl. stipend) |
|---|---|---|---|
| V2S cooperation | 354.86 | 1 of 3 | 0.1818 |
| V2S coopetition | 325.01 | 1 of 3 | 0.1467 |
| V2N cooperation | 354.56 | 1 of 3 | 0.1818 |
| V2N coopetition | 324.71 | 1 of 3 | 0.1467 |
| V1 cooperation (control) | -495.07 | 3 of 3 | -0.8177 |
| V1 coopetition (control) | -490.97 | 3 of 3 | -0.8129 |
| V1 competition (control) | -474.53 | 3 of 3 | -0.7936 |

Wealth starts at 200. "Rank 1" is reported for comparability only;
the scoring brief forbids a single winner, and the rank here is
mostly a statement about the Majority lens, not about holding.

**Control validation:** the v1 control re-run reproduces the
previous coalition game exactly — cooperation Holder -495.07,
coopetition -490.97, competition -474.53, Reactive and Router
wealths identical to the previous run to two decimals. The world,
mechanics, and accounting are therefore the same; the v2-vs-v1
differences are design differences, not drift.

## Predictions vs outcomes (2/5)

| # | Prediction | Verdict |
|---|---|---|
| P-A | V2S survives (wealth > 0) and beats v1, both regimes | **PASS** — 354.86 / 325.01 vs -495.07 / -490.97, never negative. But see headline: it survives because it collapses, not because it holds. |
| P-B | V2N survives longer than v1 but does NOT beat it on wealth | **FAIL** — first half passes (V2N never goes negative; v1 first goes negative at t=397 cooperation / 393 coopetition), second half fails badly: V2N wealth 354.56 / 324.71, far above v1. The stipend is not what separates the variants; the collapse rule is. |
| P-C | v2 post-flip mean > calm mean, and > v1 post-flip mean | **FAIL** — second half passes by ~1.0/round (v2 post-flip 0.151 cooperation / 0.120 coopetition vs v1 post-flip -0.864 / -0.906), first half fails: v2 post-flip 0.151 / 0.120 is BELOW its own calm mean 0.202 / 0.179. The Majority lens lags after flips (trailing-100 mean), so holding-then-collapsing helps vs v1 but does not make post-flip rounds better than calm ones. |
| P-D | Evidence collapses > expiry collapses | **PASS** — 136 evidence, 0 expiry, across both variants and both coalition regimes. Expiry never fires because evidence always fires first — the 200-round expiry is dead code under this Brier gap. |
| P-E | Router consultation of v2 rises post-flip vs calm | **FAIL** — Router invites Holder v2 in 33.3% of its post-flip proposer rounds vs 59.8% in calm (both variants, both regimes). Router routes by trailing-50 accuracy, and the Majority lens's accuracy falls after flips, so Router routes AWAY from Holder v2 exactly when the scoreboard said disagreement spikes. One mitigating fact: v1's post-flip consultation was 0.0% (Router never invited v1 Holder post-flip), so v2 is consulted more than v1 after flips even though it is consulted less than in calm. |

## The stipend did not matter — mechanically

Total stipend paid to V2S: **0.30** (3 holding rounds × 0.10), in
every regime. V2S vs V2N wealth differs by exactly 0.30. A
holding-only stipend cannot fund a holder that is in holding state
0.4% of the time. This is the second half of the headline: the
state-priced stipend idea (Marketplace IX) only works if the
holding state actually persists. Under this collapse rule it does
not, so the stipend test as designed here is uninformative about
stipends — it is informative about the collapse rule. A stipend
test that could actually answer the M6 question needs a holder
that stays holding long enough to be paid.

## Collapses, in detail

- 34 collapses per variant per coalition regime (136 total across
  the P-D pool), all evidence-triggered, 33 to M and 1 to m.
- Collapse rounds are exactly 25 apart, except one spell with a
  28-round gap — the 3 holding rounds in the whole run.
- The single collapse to m was at round 853, Brier gap 0.0332, just
  over threshold — the minority claim won a trailing-50 Brier
  comparison exactly once, late in the run, after the third swan.
- No expiry collapse ever fired; no minority re-evaluation beyond
  "kept" was ever reached, because no holding spell reached 200
  rounds (longest: 3 rounds).

## Translation — the flip condition discriminates, but m still loses

Flip rounds (trailing-20 bias sign != trailing-100 bias sign):
146 of 850 scored rounds. Minority sub-account mean payoff
(sign + Brier bonus, no cost):
- on flip rounds: -0.1549
- on non-flip rounds: -1.5431

The condition as stated is a real discriminator — m is 1.39/round
less bad when its condition holds — but m is still negative even
on its own condition's rounds. Translation made the minority claim
legible and testable; it did not make it good. A minority claim
that pays on its condition would need a p that is right when the
flip happens, not just an extreme opposite of the majority.

## Brier (all runs identical, since M/m are world-derived)

- Majority M: 0.2286 overall, 0.2320 swan-weighted
- Minority m: 0.5203 overall, 0.5037 swan-weighted
- Portfolio (0.5/0.5): 0.3744 overall, 0.3678 swan-weighted

The portfolio Brier is the reason the collapse rule fires: holding
both claims, scored as a portfolio, is a much worse probabilist
than the Majority alone. Any future holder design has to decide
whether portfolio Brier is even the right way to score a holder —
a holder's value, if any, is in the option on the flip, not in
its average Brier.

## What this says about Kelly's question

"What would a lens have to be like for holding disagreement to
actually pay?" — this run's answer is: not like this. Specifically:

1. **Not with a Brier-gap collapse rule at 0.03.** That rule
   collapses an extreme-minority holder immediately and
   permanently. Holding needs a collapse rule that tolerates a
   large, persistent Brier gap — or one keyed to the minority
   claim's own condition, not to Brier.
2. **Not with a holding-only stipend, if holding never persists.**
   The stipend must be paid for a state that exists, or the
   question has to move to paying for the collapsed-then-returned
   cycle itself.
3. **Not by routing.** Router, routing on trailing accuracy,
   routes away from the holder after flips — the moment the
   holder's disagreement is most informative. Consultation has to
   be priced on something other than recent accuracy, or the
   holder will be ignored exactly when it matters.
4. **The Majority lens itself is good.** Trailing-100 mean,
   collapsed to, finishes first in every regime. The zoo's
   lesson is not "majority is bad" — it is that averaging a good
   majority with an extreme minority destroys it, and that
   collapsing to the majority rescues it. That rescue is a
   finding about v1, not about holding.

## Open next questions (not built)

- A Holder v3 with a collapse rule keyed to the flip condition
  (collapse only when the flip test has been false for N rounds,
  or never collapse on Brier alone) — does holding then persist,
  and does the stipend then matter?
- A minority claim whose p is calibrated to flip rounds (not an
  extreme 0.92/0.08) — does m's flip-round payoff turn positive?
- A Router that consults on disagreement or on post-flip value
  rather than trailing-50 accuracy — does consultation rise
  post-flip then?
- The still-unbuilt Translator pairing: Reactive + Holder with a
  translation step, rather than a mean or a portfolio.

## Files

- `DESIGN.md` — design, written before any run, including the two
  explicit triad adaptations (Holder's representative p for
  Router/coalition mechanics is M; coalition action uses M while
  the record stays portfolio-based)
- `PREDICTIONS.md` — pre-registered, unedited after the run
- `holder_v2.py` — deterministic implementation (seed 20261026)
- `results.json`, `output.txt` — full numbers
- Note on per-round payoff records: the headline wealth, Brier,
  collapse, and consultation numbers are computed from wealth and
  from recorded sub-account Briers; per-round Holder payoff means
  (calm/swan/post-flip) use the realised payoff excluding
  stipend, verified against final wealth minus total stipend.
