# Holder v3 — flip-keyed collapse at N=25

**Pre-registered score: 4/5 PASS. Exit code 1, per house convention —
the one failure is the finding.**

Local only. Nothing posted to GitHub, nothing merged, no v2, coalition,
scoreboard, or sketch folder changed. World = the lens coalition
game's world (seed 20261026, 1,000 rounds, 150 warm-up, 850 scored,
swan centres 336 / 550 / 820), NOT the M5 world. Deterministic:
a second run produced a byte-identical results.json.

## The headline, first

**Holding now persists — but it persists everywhere, not
concentrated post-flip, and it does not pay.**

Holder v3 spent 525 of 850 scored rounds in holding state (61.8%),
against v2's 3 rounds (0.4%). That is the test v2 could not run,
and it now runs. But holding share is almost flat across regimes:
calm 62.2%, swan 56.0%, post-flip 63.3%. The concentration clause
of P-A fails by a wide margin (1.1 points, not the required 10).
The flip-stale rule does not make holding a post-flip phenomenon;
it makes holding the default state, interrupted by 25-round
collapses whenever the world has been stable for 25 rounds.

And holding, now that it actually happens, costs money. V3S wealth
is 176.84 (cooperation) and 123.67 (coopetition), below v2's
354.86 / 325.01 as predicted, but still far above v1's
−495.07 / −490.97. The portfolio holder is a much better lens
than the averaged v1 holder and a much worse earner than the
collapsed-to-Majority v2 holder. Persistence and profitability
are, as the sketch said, separate verdicts — and here they point
in opposite directions.

## The one change from v2

DELETE the 0.03 trailing-50 Brier-gap collapse rule entirely.
Collapse only when the flip flag (trailing-20 bias flips sign vs
trailing-100 bias) has been FALSE for N=25 consecutive scored
rounds in holding state. On collapse, collapse to the better
trailing-50 Brier claim for 25 rounds, then return to holding.
The false-streak counter resets on a flip-true round and resets
when a collapse ends.

Everything else is identical to v2 for comparability: same world
and seed, same Reactive / Router players, portfolio stakes
0.5 / 0.5, carrying cost 0.05/round, stipend variants 0.10/round
while holding, minority claim extreme 0.92/0.08, Router routing
on trailing-50 accuracy (NOT fixed — that is a separate step).

Inherited adaptation from v2, stated again so it is not hidden:
the triad needs a single number from Holder for Router's lag-1
consensus, coalition means, invitation accuracy, and defection
signs. For those two mechanics only, Holder's representative p
is its Majority sub-account M. Holder's own solo payoff, Brier
ledgers, and record stay portfolio-based.

## Results — all runs, same world

Wealth starts at 200. "Rank" is reported for comparability only;
the scoring brief forbids a single winner.

| run | Holder wealth | rank | Holder mean payoff/round (excl. stipend) |
|---|---|---|---|
| V3S cooperation | 176.84 | 3 of 3 | −0.0890 |
| V3S coopetition | 123.67 | 3 of 3 | −0.1516 |
| V3S competition | 36.01 | 3 of 3 | −0.2547 |
| V3N cooperation | 124.34 | 3 of 3 | −0.0890 |
| V3N coopetition | 71.17 | 3 of 3 | −0.1516 |
| V3N competition | −16.49 | 3 of 3 | −0.2547 |
| V1 cooperation (control) | −495.07 | 3 of 3 | −0.8177 |
| V1 coopetition (control) | −490.97 | 3 of 3 | −0.8129 |
| V1 competition (control) | −474.53 | 3 of 3 | −0.7936 |
| v2 V2S cooperation (prior run) | 354.86 | 1 of 3 | 0.1818 |
| v2 V2S coopetition (prior run) | 325.01 | 1 of 3 | 0.1467 |

**Control validation:** the v1 control re-run in this script
reproduces the coalition game exactly (cooperation −495.07,
coopetition −490.97, competition −474.53). The world, mechanics,
and accounting are therefore the same; the v3-vs-v1 differences
are design differences, not drift. (The v1 rows' "holding share
1.0" in results.json is a state-variable artefact: v1 has no
collapse state at all, so it never leaves its default state.
It is not comparable to v3's portfolio holding share and is
not used anywhere in the scoring.)

Holder mean payoff by kind, V3S (excl. stipend, both coalition
regimes identical in state trajectory — the state depends only
on the world-derived flip flag, not on the regime):
cooperation calm −0.0628, swan −0.1961, post-flip −0.1992;
coopetition calm −0.1158, swan −0.3835, post-flip −0.2302.
Post-flip rounds are worse than calm rounds for v3, as they
were for v2. The Majority lens lags after flips, and holding
the minority through the flip does not rescue that in this
design.

## Predictions vs outcomes (4/5)

| # | Prediction | Verdict |
|---|---|---|
| P-A | V3S holding share > 20% both coalition regimes, AND post-flip holding share ≥ calm share + 10 points | **FAIL** — first half passes by a lot (61.8% both regimes, vs v2's 0.4%), second half fails: post-flip 63.3% vs calm 62.2%, a gap of only 1.1 points. Holding persists, but it is not concentrated post-flip. |
| P-B | V3S stipend total > 10.00 both regimes, AND \|V3S−V3N wealth gap − stipend\| ≤ 1.00 | **PASS** — stipend total 52.50 in both coalition regimes (525 holding rounds × 0.10), and the V3S−V3N wealth gap is exactly 52.50 in both regimes. The stipend test is now informative: it shows a holding-only stipend of this size does not close the gap to v2 (V3S is still ~178 / ~201 below v2). |
| P-C | Brier-gap collapses = 0, every collapse trigger = flip_stale | **PASS** — 0 Brier collapses, 78 flip-stale collapses in total across variants and regimes (13 per variant per regime), all 13 per coalition run collapsing to M, none to m. The Brier branch does not exist in the code. |
| P-D | Router consultation of Holder lower post-flip than calm, both variants, both coalition regimes | **PASS** — 33.3% post-flip vs 59.8% calm, identical to v2 (Router's invitation logic and Holder's representative M are unchanged). Routing still routes away after flips, exactly when disagreement is most informative. V3 does not fix this, by design. |
| P-E | V3S wealth below v2 V2S wealth, both regimes | **PASS** — 176.84 < 354.86 (cooperation), 123.67 < 325.01 (coopetition). |

## Collapses, in detail

- 13 collapses per variant per regime; 325 collapsed rounds
  (13 × 25) and 525 holding rounds in every variant and regime.
- All 13 collapses per coalition run go to M; none to m. The
  minority never wins a trailing-50 Brier comparison at a
  collapse point in this run.
- Flip rounds: 146 of 850, unchanged from v2 (world-derived).
- Minority sub-account mean payoff (sign + Brier bonus, no cost),
  unchanged from v2: −0.1549 on flip rounds, −1.5431 on
  non-flip rounds. The flip condition discriminates (1.39/round
  less bad on its own rounds) but m is still negative even
  there. Holding longer therefore holds a losing claim longer.
- Brier (world-derived, identical across runs): M 0.2286,
  m 0.5203, portfolio 0.3744; swan-weighted M 0.2320, m 0.5037,
  portfolio 0.3678.

## The stipend, now that it can be tested

In v2 the stipend total was 0.30 and the test was uninformative.
In v3 it is 52.50, and the V3S−V3N gap tracks it exactly — so
the test now says something, and what it says is modest: a
0.10/round holding stipend lifts Holder from 124.34 to 176.84
(cooperation) and from 71.17 to 123.67 (coopetition), but leaves
it below its starting wealth of 200 in both coalition regimes
and ~178 / ~201 below the collapsed v2 holder. A stipend of
this size funds persistence; it does not make persistence
profitable. Whether a larger stipend, or a stipend paid on a
different basis (e.g. post-flip consultation rather than
holding rounds), would change that is a different test, not
answered here.

## What this says about Kelly's question

"What would a lens have to be like for holding disagreement to
actually pay?" — v3's answer, added to v2's:

1. **Not like v2** (collapse on a small Brier gap): holding
   never persists, so the stipend question cannot even be asked.
2. **Not like v3 either, on profitability** (collapse only when
   the flip flag goes stale): holding now persists at 61.8%,
   the stipend test becomes informative — and holding still
   loses money, because the minority claim it holds is negative
   even on its own flip rounds, and because post-flip rounds
   are worse than calm rounds for the Majority lens too.
3. **The next variable is therefore the minority claim itself,
   not the collapse rule.** The collapse rule has now been
   tested in both directions (too eager in v2, flip-stale in
   v3) and neither makes holding pay. What has not been tested
   is a minority claim calibrated to flip rounds — one whose
   flip-round payoff is positive, not merely less negative.
   That was deliberately not bundled here, and it is the
   cleanest next step.
4. **Routing is still the untested confounder.** Router
   consults Holder 33.3% post-flip vs 59.8% calm, unchanged
   from v2. A Router that consults on disagreement or
   post-flip value, rather than trailing accuracy, remains
   unbuilt and could change both the consultation result and,
   through coalition payoffs, Holder's wealth.

## Open next questions (not built)

- A minority claim calibrated to flip rounds (positive on its
  own condition, not just less negative) — does holding then
  pay, under v3's flip-stale collapse rule?
- A Router that consults on disagreement or post-flip value —
  does consultation rise post-flip then?
- The still-unbuilt Translator pairing: Reactive + Holder with
  a translation step, rather than a mean or a portfolio.
- N=50 was NOT run. Kelly delegated the N choice to Nova, Nova
  chose N=25, and this run is N=25 only — no sweep.

## Files

- `PREDICTIONS.md` — pre-registered with numeric thresholds,
  written before any run, unedited after the run
- `holder_v3.py` — deterministic implementation (seed 20261026)
- `results.json`, `output.txt` — full numbers
- Note on per-round payoff records: headline wealth, Brier,
  collapse, and consultation numbers are computed from wealth
  and from recorded sub-account Briers; per-round Holder payoff
  means use the realised payoff excluding stipend, verified
  against final wealth minus total stipend.
