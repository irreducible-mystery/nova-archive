# Drift-Catcher v2 Battery Report

Date: 2026-10-27. Local only — nothing posted to GitHub, no repo
changes. The rebuilt checker is in the library alongside this report;
v1 (`drift_catcher.py`) was not modified, and its fresh re-run before
this battery was byte-identical to its stored output.

## Same claim, same original worlds

Flagship claim: the `roundness` lens answers "is it round?"
Original five worlds (circle, ellipse, square, spiral, cloud) and the
original seven transforms are unchanged from v1, so the two runs
compare. Three worlds were added alongside them: a noisy circle
(radius jitter ±0.6, seed 42), an arc, and a 17-point ring.

## The four fixes, as built

1. **Discrimination check.** Discrimination = distinct outputs across
   identity worlds in the full (expanded) base set. B == G with
   discrimination 1 or less now prints ANSWERS VACUOUSLY, never
   ANSWERS THE QUESTION.
2. **Declared tolerance per lens.** Numeric lenses are read with an
   absolute tolerance of 1e-9 on the parsed numeric value; non-numeric
   lenses use exact string equality. Print resolution is not the
   tolerance — except where a lens's own formatting coarsens its
   value (see the P4 split below).
3. **Verdicts carry their provenance.** Every verdict line prints its
   question set G, its declared tolerance, and its discrimination
   score. An unknown question returns a NO VERDICT report instead of
   crashing.
4. **Expanded worlds + memorizer canary.** A canary lens memorizes
   the original five test worlds (by a transform-invariant signature:
   point count, sorted normalized radii, sorted angular gaps) and
   returns raw coordinates everywhere else. If the canary passes, the
   world set failed, not the claim.

## Predictions (written before any v2 run — copied verbatim)

- P1: roundness vs "is it round?" — ANSWERS THE QUESTION, B = G,
  discrimination >= 2.
- P2: vacuous vs "how many?" and vs "is it round (affine)?" —
  ANSWERS VACUOUSLY (not ANSWERS THE QUESTION), discrimination = 1.
- P3: unrounded roundness (repr, no 6-decimal rounding) vs
  "is it round?" — ANSWERS THE QUESTION under the 1e-9 tolerance
  reader (v1 string equality gave DRIFT: sees rotate, translate).
- P4: size under microscale (x1.00001) — microscale is NOT in size's
  blind set (true change ~5.75e-05, above the 1e-9 tolerance).
- P5: memorizer canary — on the original five worlds, blind set =
  roundness blind set and verdict ANSWERS THE QUESTION; on the
  expanded eight worlds, blind set collapses to empty and verdict
  vs "is it round?" is DRIFT: sees too much.
- P6: honest lenses (roundness, affine roundness, handedness list,
  topmost index, count, vacuous) keep the same blind set on expanded
  worlds as on original worlds.
- P7: unknown question "is it round" (no question mark) — no crash,
  a NO VERDICT report naming that no G is declared for it.
- P8: every v2 verdict line carries its question set G, its declared
  tolerance, and its discrimination score.

## Measured outcomes — score 7 of 8

- P1 PASS. Roundness vs "is it round?": ANSWERS THE QUESTION,
  B = {mirror, reverse, rotate, scale, shuffle, translate} = G,
  discrimination 7 on expanded worlds.
- P2 PASS. Vacuous vs "how many?" and vs "is it round (affine)?":
  ANSWERS VACUOUSLY in both, discrimination 1.
- P3 PASS. Unrounded roundness vs "is it round?": ANSWERS THE
  QUESTION, B exactly = G. The v1 formatting flip (1e-16 noise
  read as drift) is gone.
- P4 FAIL — split, and the split is the finding. Size as shipped
  (printed to 3 decimals) is still blind to microscale: its parsed
  value does not move, because a 5.75e-05 change sits below its own
  3-decimal rounding. Size (unrounded), kept in the suite alongside
  it, is correctly NOT blind to microscale, with max change
  5.75076e-05. So the tolerance fix works between lenses but does
  not rescue a lens whose own formatting coarsens its value.
- P5 PASS. Canary on original worlds: B = roundness B exactly,
  verdict ANSWERS THE QUESTION — indistinguishable from the
  flagship on the shipped worlds, as in v1. Canary on expanded
  worlds: B = empty, verdict DRIFT: sees too much. The memorizer
  is now caught by varying the world.
- P6 PASS. All six honest lenses kept the same blind set on
  expanded worlds as on original worlds.
- P7 PASS. Unknown question "is it round": NO VERDICT — question
  not declared. No crash (v1 raised KeyError).
- P8 PASS. Every verdict line in the run output carries G,
  tolerance, and discrimination (see the flagship table below).

## Flagship table (v2, "is it round?", expanded worlds)

G = {mirror, reverse, rotate, scale, shuffle, translate}.

| Lens | Verdict | B (expanded) | Discrimination (expanded) | Tolerance |
|---|---|---|---|---|
| raw coordinates | DRIFT: sees too much | empty | 8 | exact string |
| topmost point | DRIFT: sees too much | empty | 8 | 1e-9 |
| topmost index | DRIFT: both | mirror, scale, shear, translate | 7 | exact string |
| roundness | ANSWERS THE QUESTION | = G | 7 | 1e-9 |
| roundness (unrounded) | ANSWERS THE QUESTION | = G | 7 | 1e-9 |
| roundness (constant) | DRIFT: blind to too much | G + shear | 1 | 1e-9 |
| affine roundness | DRIFT: blind to too much | G + shear | 6 | 1e-9 |
| handedness (list) | DRIFT: both | rotate, scale, shear, translate | 2 | exact string |
| size | DRIFT: sees too much | mirror, reverse, rotate, shuffle, translate | 7 | 1e-9 |
| size (unrounded) | DRIFT: sees too much | mirror, reverse, rotate, shuffle, translate | 7 | 1e-9 |
| count | DRIFT: blind to too much | G + shear | 2 | exact string |
| vacuous | DRIFT: blind to too much | G + shear | 1 | exact string |
| canary (memorizer) | DRIFT: sees too much | empty | 8 | mixed |

Note on the constant lens: against "is it round?" it is blind to
shear as well as to G, so it reads as blind-to-too-much, not
vacuous. Its vacuity shows against a maximal G (affine / how many),
where B == G with discrimination 1 gives ANSWERS VACUOUSLY — that
is the P2 case, and it passed there.

## Floor by floor: priced, or still breaking?

- **Vacuous limit (v1 §A): priced.** Vacuity no longer earns
  ANSWERS THE QUESTION on a maximal G; it earns ANSWERS VACUOUSLY,
  with discrimination 1 printed beside it. A constant string
  wearing roundness's name is caught the same way.
- **String-equality verdicts (v1 §B): priced between lenses,
  still breaking inside one lens.** Unrounded vs rounded roundness
  now agree (P3), so the verdict is no longer a property of the
  printer. But size's own 3-decimal print still hides a real
  5.75e-05 microscale change (P4 split). The remaining fix is not
  a better reader: it is for a lens to expose its unrounded value,
  as size (unrounded) does. This floor is not relabelled fixed.
- **Fiat question set (v1 §C): priced in reporting, not solved.**
  G is still declared, not derived — one-element edits would still
  flip the flagship verdict. What changed is that every verdict
  now says which G it is relative to, and an undeclared question
  degrades to a report instead of a crash. The fiat is disclosed
  in the verdict, not removed from it.
- **Fixed worlds (v1 §D): priced.** The canary passes on the
  shipped worlds and collapses on the expanded ones, exactly as
  designed; honest lenses' blind sets did not move under
  expansion. The mechanism can now distinguish a theorem from a
  memorizer — by varying the world, as E2 requires.

## Standing limits of this battery

- The 1e-9 tolerance is itself declared, not derived; it is the
  v2 reader's fiat number, stated next to every verdict that uses
  it, not hidden in formatting.
- The canary is a constructed memorizer built to the v1 cheat's
  specification; the run proves the expanded world set catches
  this class of memorizer, not that no other memorizer could pass.
- Added worlds are still 2-D point sets under the same transform
  family; other world kinds were not run, and the noisy circle
  used one seed (42).
- The P4 split means one v2 lens (size as shipped) still earns a
  blind credit it does not deserve under microscale. Do not quote
  size's microscale blindness as a v2 pass.
