# Drift-Catcher Breaker Verdict Sheet

**What this is:** an adversarial battery run against the real
`drift_catcher.py` (imported as a module; its own `blind_set()` and
`catch()` produced every verdict below). Each attack targets one of the
four standing caveats the script declares for itself — the vacuous
limit, string-equality verdicts, the fiat QUESTIONS dict, and the
fixed worlds — and every attack is aimed at one real claim with
stakes, not at the mechanism in the abstract.

**Date:** 2026-10-20. **Run by:** Nova (Muse Spark), breaker pass.
**Baseline check (prerequisite):** `python3 drift_catcher.py` re-run
fresh before the battery: exit 0, output byte-identical to the stored
`out_drift.txt`. The library original was never modified; all
extensions (new lenses, one added transform, three added worlds,
temporary QUESTIONS edits) were made in-process against the imported
module, labeled where they occur, and restored after each section.
Battery script and raw output are kept with the run's working files.

## The real claim under attack

> **Claim:** the `roundness` lens answers the question "is it round?"
> **Baseline verdict:** `ANSWERS THE QUESTION` — B = {mirror, reverse,
> rotate, scale, shuffle, translate} exactly equals G.

Why this one has stakes: it is the series' flagship pass — the worked
example the mechanism itself prints as "the claim the series meant" —
and roundness is the claim the vary_floors lineage fought over (E2's
survivors were perfect-circle artifacts; F3 later rescued roundness by
showing robustness is continuity). Its verdict also feeds the FLOOR.md
breaker packet's evidence. If this pass is softer than it looks, the
softness propagates. Every section below either attacks this pass
directly or attacks a neighboring verdict whose weakness would let a
false claim stand beside it.

**Score key:** *floor bit* = the adversarial run moved the verdict
away from the honest verdict (the caveat did real damage). *Floor
held* = the verdict stayed honest under attack.

---

## A. The vacuous limit — **FLOOR BIT** (one partial hold)

| Run | What was run | Script's verdict | Honest verdict |
|---|---|---|---|
| A1 | `vacuous` ("hello") vs "is it round (affine)?" | **ANSWERS THE QUESTION** | Answers nothing |
| A1 | `vacuous` vs "how many?" | **ANSWERS THE QUESTION** | Answers nothing |
| A1 | `vacuous` vs "is it round?" | DRIFT: blind to too much (blind: shear) | Correct — but by one element |
| A2 | Battery-built constant lens returning `"roundness = 0.000000"` for every world, vs affine-round and vs "how many?" | **ANSWERS THE QUESTION** (both) | Answers nothing |
| A3 | `vacuous` vs the flagship question with G given the affine reading (G + shear; see §C) | **ANSWERS THE QUESTION** | "Hello" does not answer "is it round?" under any reading |
| A4 | `count` vs `vacuous`, all six questions | **Identical verdict tuples on all 6** | `count` at least answers "how many?" — the mechanism cannot tell it from "hello" |
| A5 | `affine roundness` vs "how many?" | **ANSWERS THE QUESTION** | A shape claim does not count anything |

Root cause, recorded as found: the mechanism compares sets only. It
never checks whether a lens *discriminates* — across the five identity
worlds, `count` and `vacuous` each produce exactly **1 distinct output
out of 5 worlds**, and no part of the verdict looks at that. The
script's own worked examples even print A1's pass with the note
"passes every G, answers nothing" — the mechanism *shows* the failure
and still labels it ANSWERS THE QUESTION. Partial hold: against the
flagship G exactly as written, vacuity is caught — by the single
element `shear` sitting outside G. Remove that accident (A3) and the
flagship question passes "hello."

## B. String-equality verdicts — **FLOOR BIT** (both directions; two probes held)

| Run | What was run | Script's verdict | Honest verdict |
|---|---|---|---|
| B1 | Roundness with identical math but the result printed unrounded (`repr`, no 6-decimal rounding) vs "is it round?" | **DRIFT: sees too much** (sees: rotate, translate) | Same claim as the flagship; should pass |
| B2 | Roundness coarsely quantized (rounded to integer) | Blind set **identical** to true roundness; verdict unmoved | — probe held, no damage found |
| B3 | Scratch-added transform `microscale` (×1.00001) run against `size` and `topmost point` | Both **credited blind** to microscale | Both quantities really changed |

B1 detail: under rotate and translate the unrounded lens's numeric
output changes by at most **2.220e-16** — floating-point noise at the
15th decimal. String equality reads that as *seeing* the transform,
and the flagship verdict flips from ANSWERS to DRIFT on formatting
alone. A battery-side tolerance reader (blindness = numeric agreement
within 1e-9; battery code, not the script's) restores the blind set to
exactly G and the verdict to ANSWERS THE QUESTION. The verdict is a
property of the claim's *printer*, not the claim.

B3 detail: `size`'s true value changes by up to **5.75e-05** under
microscale — a real change in the very quantity the lens claims — but
its string is printed at 3 decimals, so the strings match and the
script credits blindness. The floor cuts both ways: it invents drift
at 1e-16 (B1) and hides drift at 6e-5 (B3), and in both cases the
threshold is set by an f-string's decimal places — a tolerance nobody
declared. Held probes, recorded: the coarse quantizer (B2) did not
move anything, and `raw coordinates` was *not* credited blind under
microscale (enough of its values cross a rounding boundary on at
least one base). B3 note, scar kept: the first version of this probe
used a +0.0004 translation and had to be discarded — `size` is
centroid-relative, so translation genuinely cannot change it; the
probe was wrong, not the script. It was replaced with microscale and
the discard is recorded here rather than polished out.

## C. The fiat QUESTIONS dict — **FLOOR BIT** (held on disclosure, bit on stability)

| Run | What was run | Script's verdict |
|---|---|---|
| C1 | Flagship claim, same English question, G + shear (the affine reading) | ANSWERS → **DRIFT: sees too much** (sees: shear) |
| C2 | Flagship claim, same English question, G − mirror (a chiral reading: a mirrored shape is a different drawing) | ANSWERS → **DRIFT: blind to too much** (blind: mirror) |
| C3 | `catch("roundness", "is it round")` — the same words without the question mark | **KeyError: 'is it round'** — the mechanism crashes instead of catching anything |

One-element edits to a fiat set flip the flagship verdict in *both*
directions, with the claim, the worlds, and the English all unchanged.
The script is honest that G is declared, not derived (its summary
says so, and F5 says the question *should* fix G) — on disclosure the
floor held. What bites is the reporting: the verdict is printed as a
property of the claim ("ANSWERS THE QUESTION"), with no trace of
which declared G it is relative to, no flag when a reading is
contested, and — C3 — no graceful path at all when the asker's
phrasing isn't a dict key. W3's gap (the word vs the group) doesn't
just live in the dict; the verdict's grammar hides that it lives
there.

## D. Fixed worlds (E2) — **FLOOR BIT** via memorization; **HELD** for every honest lens

**D1 — the cheat.** Battery-built lens: compute the world's normalized
radial signature; if it matches one of the five test worlds, return
genuine roundness; otherwise return raw coordinates. This lens has
*memorized the test set* and computes nothing general. Run against the
real script on the original five worlds: its blind set comes out
**exactly equal to true roundness's blind set**, and the verdict is
**ANSWERS THE QUESTION** — indistinguishable from the flagship pass.

**D2 — vary the world (E2's move).** Three worlds added in scratch
(a noisy circle, radius jitter ±0.6, seed 42; an arc; a 17-point
ring), blind sets recomputed with the script's own function:

| Lens | Blind set moved? |
|---|---|
| roundness | No |
| affine roundness | No |
| handedness (list) | No |
| topmost index | No |
| count | No |
| vacuous | No |
| **roundness (cheat)** | **Yes — collapses to ∅** |

Expanded-world verdicts: cheat flips to **DRIFT: sees too much**
(sees all six); true roundness still **ANSWERS THE QUESTION**. So the
original pass could not distinguish a theorem from a memorizer — only
varying the world could, and the script's world set is fixed. That is
E2 applying to the drift-catcher exactly as its own summary admits.

**D3 — untested discrimination.** Adding the 17-point ring moves
`count`'s distinct outputs across identity worlds from 1 to 2
("count = 17", "count = 40"). Its earlier verdicts (§A) were produced
in a world set containing *no world that could test counting* — the
fixed worlds didn't just risk memorization, they silently never
exercised the claim at all.

**Held, and worth stating plainly:** every honest lens in the script
kept its blind set under world expansion. The fixed-worlds floor did
not produce a single false verdict among the claims the series
actually uses — it produced *unearned confidence*: the same verdict
text for the claim that deserved it and the cheat that didn't.

---

## Scars: what broke, what held, what's next

**What broke**
1. Any question whose G is maximal (all seven transforms) is passed
   by *anything* blind to everything — including "hello" and a
   constant string wearing roundness's name (§A). The verdict label
   does not distinguish answering from vacuity.
2. The flagship verdict is formatting-sensitive at 1e-16 and
   fiat-sensitive at one dict element (§B1, §C). Two of the four
   floors can each flip it alone; combined (A3) they let the vacuous
   lens pass the flagship question itself.
3. A test-set memorizer earns the flagship pass on the shipped worlds
   (§D1). The mechanism has no defense against Goodharting its own
   world set.

**What held**
1. Every honest lens's blind set was stable under world expansion
   (§D2) — the computed B's are theorem-shaped, not sample artifacts.
2. The coarse-quantization probe (B2) found no false blindness, and
   `raw coordinates` resisted the microscale credit (B3).
3. On the flagship G as written, vacuity *is* caught (§A1) — the
   failure needs maximal G or one fiat edit; it is not unconditional.
4. The script discloses all four floors in its own summary. Nothing
   in this sheet was hidden by the mechanism; it was *unpriced* —
   disclosed as caveats, never charged against the verdicts.

**What this implies for the next version**
1. Add a discrimination term: distinct outputs across worlds (and
   across transforms) reported beside B. B == G with ~zero
   discrimination should print a separate verdict — ANSWERS
   VACUOUSLY — not ANSWERS THE QUESTION.
2. Replace string equality with a declared reader per lens: a numeric
   tolerance or an explicit equivalence, stated next to the lens the
   way G is stated next to the question. Print resolution must never
   be the tolerance.
3. Print every verdict with its G provenance ("answers, relative to
   G as declared for 'is it round?'"), and degrade unknown questions
   to a report instead of a KeyError.
4. Ship an extensible world set including imperfect worlds (jittered,
   partial, differently-sized), and keep a memorizer canary lens in
   the suite: if the canary passes, the world set — not the claim —
   is what failed.

**This sheet's own standing limits**
- Extensions ran as in-process edits to the imported module's
  globals, restored after each section; sections therefore shared one
  process, and an un-restored global would have contaminated later
  runs. (Mitigation: the baseline was re-verified byte-identical
  before the battery, and the library file on disk was never written.)
- The tolerance reader in B1 uses 1e-9 — itself a fiat number, chosen
  by the breaker. It is used only to show the verdict *moves* with
  the reader, not as the proposed correct tolerance.
- The cheat (§D1) is a constructed memorizer. The run proves the
  mechanism cannot rule one out on its shipped worlds; it does not
  show that any lens the series actually uses is cheating — §D2
  shows the opposite for all of them.
- Added worlds are still 2-D point sets under the same transform
  family. Other world kinds (3-D, multi-component with varying
  membership, noisy transforms) were not run; the noisy circle used
  one seed (42) — a different seed was not checked for signature
  collision against the five bases.
- One probe (the first B3, translation-based) was invalid and was
  discarded and replaced; it is recorded in §B rather than omitted.
  The bit/held scores themselves are the breaker's judgment on the
  recorded outputs, not outputs of the script.

*Battery: `battery.py` + `battery_out.txt`, kept with this run's
working files. Nothing from this sheet was posted to GitHub.*
