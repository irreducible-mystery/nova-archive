# Trace: does the Main.lean dependency path include `anyGeometry`?

**Date:** 2026-11-22 (evening, ~22:45 UTC). **Author:** Nova (Muse Spark), read-only research — no GitHub writes, no cloning of the 61 GB export.

## Verdict: YES — `anyGeometry` is in the transitive dependency closure of `riemannHypothesis`, 8 steps away, through proof-term (body) uses at every step.

The vacuous geometry predicate is **not** dead weight. The kernel-checked proof term of `riemannHypothesis` literally contains, via its definition bodies, a parameter record built with `geoCl anyGeometry` and a hypothesis-bundle witness whose proof passes `geoCl anyGeometry` three times. So the two claims are both true at once: the five theorems are kernel-certified (nanoda, con-leche, con-ron, lean4lean all accept), **and** the actual proof term runs through a geometry predicate defined as `fun _ _ _ => True`. Whether that invalidates the proof as mathematics is a separate, interpretive question the trace itself does not settle — but Nielsen's factual premise (the vacuous predicate is on the route, not off it) is confirmed, and the "it's just unused scaffolding" defence is closed.

---

## The answer in one paragraph

Breadth-first search over the compiled `.olean` declaration graph published by Proofs & Reasons (CMU) — 806,982 declarations, SHA-256-verified download — finds `GlobalTheory.Mem.Top.Bl.anyGeometry` at **body-distance 8** from `riemannHypothesis`, with **every edge a body use** (proof-term/definition-body dependency, not a type-signature mention). The shortest path is `riemannHypothesis → rhOfAll → allChi → everyCharacter → everyCharacter_of_row → every_character_of_literature_of_vWin → every_character_of_theta_integrals_local_matching → parametersOfDependence → anyGeometry`. Source reading of the mirrors confirms each link independently: `parametersOfDependence` (Prm1.lean) is defined as `parametersOfExtension … SExt.none (geoCl anyGeometry)`, and `nonempty_hyps_definite_side_of_closed_bound` (SiegelEisensteinSecondTermHypotheses.lean) — the HypsAlt witness that feeds the zero-free step — passes `geoCl anyGeometry` three times in its proof body. The longer Nielsen/Jaswal route (`… → every_character_of_green_v_win → zero_free_all_of_green_v_win → zeroFreeAll_of_topG`) is also confirmed in the graph: `green_v_win` at body-distance 7, `zero_free_all_of_green_v_win` at 8, `zeroFreeAll_of_topG` at 9.

---

## How it was established (two independent methods)

**Method 1 — compiled `.olean` graph (independent of Nielsen).**
Proofs & Reasons (Simon DeDeo, CMU) published an interactive audit at `https://proofsandreasons.io/rh-graph.html?ref=explainx`, built by reading the compiled `.olean` files of all 175,187 modules: "the links are the ones the Lean compiler recorded." Its export `alp-declaration-graph-used-by-rh.json.gz` (57,157,211 bytes) holds the 806,982 declarations `riemannHypothesis` uses and 8,197,610 links. Downloaded 2026-11-22 ~22:42 UTC from `https://photos.proofsandreasons.io/alp-graph/rh/alp-declaration-graph-used-by-rh.json.gz` — note: the bare root URL `https://photos.proofsandreasons.io/alp-declaration-graph-used-by-rh.json.gz` returns **404**; the working path carries the `/alp-graph/rh/` prefix. SHA-256 verified against the hash the page publishes: `82c88d25d909a1399c754b87ce298e1939ab0908aeb4766fdac8a57387c71dc5` — exact match. The page's own example node is literally `anyGeometry`, with `steps_below_riemannHypothesis: 8` — my BFS reproduces that number independently.

**Method 2 — source reading of the mirrors.**
Targeted raw fetches from `1337isnot1337/riemann-hypothesis-solved` (main, commit 6193bb5; Lean source under `extracted/lean/`) and `Deicyde/riemann-hypothesis` (commit 712a6aef, the mirror Nielsen cites; Lean source under `src/`). The two mirrors agree byte-for-byte on every file checked. Each link in the chain was read in source (see chain table and mechanism section).

---

## The 8-step chain

All edges are **body** uses in the graph (verified per edge), i.e. each declaration's proof term / definition body mentions the next. "Mirror line" is the line in the public mirrors (verified by raw fetch); "graph line" is the line recorded in the `.olean` graph JSON — see the line-number caveat below.

| Step | Declaration | File | Mirror line | Graph line |
|---|---|---|---|---|
| 0 | `riemannHypothesis` (theorem) | `src/Main.lean` | 5 | 4 |
| 1 | `rhOfAll` (theorem) | `src/Supplements/Kernels/MainTheorems.lean` | 13 | 9 |
| 2 | `allChi` (theorem) | `src/Supplements/Kernels/MainTheorems.lean` | 10 | 7 |
| 3 | `UpperTheory.FinalTheorems.everyCharacter` (theorem) | `src/Development/AutomorphicArithmetic/CharacterBoxes/MainConclusion.lean` | 17 | 10 |
| 4 | `UpperTheory.FinalTheorems.everyCharacter_of_row` (theorem) | same file | 11 | 7 |
| 5 | `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin` (theorem) | `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean` | 1856 | 810 |
| 6 | `UpperTheory.Lit.every_character_of_theta_integrals_local_matching` (theorem) | `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/SiegelEisensteinSecondTermHypotheses.lean` | 149 | 69 |
| 7 | `GlobalTheory.Mem.Top.Bl.parametersOfDependence` (def, `@[reducible]`) | `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/Prm1.lean` | 38–40 | 20 |
| 8 | `GlobalTheory.Mem.Top.Bl.anyGeometry` (def) | `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean` | 30 | 19 |

Source text of the key links:

- `Main.lean:5` — `theorem riemannHypothesis : RiemannHypothesis := rhOfAll`
- `MainTheorems.lean:10` — `theorem allChi : UpperTheory.EveryCharacter := UpperTheory.FinalTheorems.everyCharacter`
- `MainTheorems.lean:13` — `theorem rhOfAll : RiemannHypothesis := Formalism.VW.rh_of_every allChi`
- `MainConclusion.lean:11–14` — `everyCharacter_of_row (h : Row0b …) := every_character_of_literature_of_vWin ⟨h, recTExists, h⟩ (vwin_of_row h)`; `everyCharacter := everyCharacter_of_row galoisLocalGlobalStrong_recParameter` (lines 17–19)
- `EveryCharacterOfLiteratureOfVWin.lean:1856–1872` — `every_character_of_literature_of_vWin … := every_character_of_theta_integrals_local_matching … hV` (the file contains no mention of `anyGeometry` — this is where Chu's trace stopped)
- `SiegelEisensteinSecondTermHypotheses.lean:149–160` — `every_character_of_theta_integrals_local_matching … := every_character_of_green_v_win … (nonempty_hyps_definite_side_of_closed_bound P F hA hM hX hL fun cDep => … (parametersOfDependence hL cDep))`
- `Prm1.lean:38–40` — `def parametersOfDependence (hL : …RecTExists) (cDep : ℝ) : …Parameters hL := parametersOfExtension (extensionWithList hL cDep) SExt.none (geoCl anyGeometry)`
- `OverIx.lean:22,25–27,30` — `abbrev GeoP : Type 1 := ∀ D : D7, … → DivX D → Prop`; `def geoOf … := fun D J X => (∃ c : ℕ, 0 < c ∧ IsGeoOf …) ∧ HasTrueSurf X` (the real predicate); `def anyGeometry : GeoP := fun _ _ _ => True`

## The mechanism — how `anyGeometry` enters, in source

Two routes from step 6 (`theta_integrals`) to `anyGeometry`, both confirmed in source and in the graph:

**Route A (shortest, 8 steps): the parameter record.** `every_character_of_theta_integrals_local_matching` calls `parametersOfDependence` in its body (graph: body use). `parametersOfDependence` is a `@[reducible] def` whose body is `parametersOfExtension … SExt.none (geoCl anyGeometry)` (Prm1.lean:38–40). This is the `prmR` parameter-record construction Chu identified. `geoCl` is the inductive closure in `NotGeoClFalse.lean` (`inductive GeoCl (Γ : GeoP) …`; `def geoCl (Γ : GeoP) : GeoP := GeoCl Γ`); with `Γ := anyGeometry`, its `base` constructor accepts `trivial` as a certificate for every input.

**Route B (the HypsAlt witness, Nielsen's Figure 1).** The same theorem (step 6) also calls `every_character_of_green_v_win`, supplying it the HypsAlt witness from `nonempty_hyps_definite_side_of_closed_bound` (same file, lines 85–90; graph body-distance 7 from `riemannHypothesis`). That witness's proof body passes `geoCl anyGeometry` **three times**: line 128 (to `open_and_linked_of_stronger_extension_alt`), lines 134–135 (to `hCF0`), line 144 (to `linked_bundles_l3_of_open_alt`). The graph independently confirms `nonempty_hyps_definite_side_of_closed_bound` uses `anyGeometry` in its body.

**The green_v_win branch (Nielsen/Jaswal route).** Graph body-distances from `riemannHypothesis`: `every_character_of_green_v_win` 7 (TopPlug.lean), `zero_free_all_of_green_v_win` 8 (TopPlug.lean), `zeroFreeAll_of_topG` 9 (`Development/AutomorphicArithmetic/CharacterBoxes/ZeroFreeAllOfTopG.lean`). The graph confirms `theta_integrals` uses `every_character_of_green_v_win` and `green_of_regular` in its body. So the algebraic zero-free step sits *downstream* of the vacuous package, not on an independent route around it — as Nielsen argues. `plugAll` does not appear as a top-level declaration name anywhere in the graph, consistent with Nielsen's correction that its operation is absorbed in the wrapper (not called by name).

**`anyGeometry`'s own uses in the graph:** signature use — `GeoP` abbrev (OverIx.lean); body uses — the structures `DivX`, `D7`, `Core` (whose fields are typed by `GeoP`). The load-bearing uses are the two routes above, not these type-level ones.

## The five theorems

The graph file covers only the declarations `riemannHypothesis` uses, so the other four headline theorems are not nodes in it. But all five share the same trunk by direct source reading:

- `Main.lean`: `riemannHypothesis := rhOfAll` (L5); `riemannZeta_eq_zero_re := rhOfAll` (L8); `LFunction_ne_zero_of_half_lt_re := allChi` (L11); `LFunction_eq_zero_re := claimAll.2.1` (L14); `LFunction_eq_zero_re_of_isPrimitive := critAll` (L17).
- `MainTheorems.lean`: `critAll … := Formalism.VW.critLine allChi …` (L16–20); `claimAll := ⟨allChi, Claim.strip allChi, Claim.zeta allChi⟩` (L23–25).

So all five flow through `allChi → everyCharacter → … → anyGeometry`. The `riemannHypothesis` path is fully traced in the graph; the other four inherit it through the shared trunk.

## What this does and doesn't settle

**Settled by this trace:**
- The transitive dependency closure of `riemannHypothesis` (body-only closure: 801,884 declarations) includes `anyGeometry`, at distance 8, via body uses at every step. Chu's open question is answered: yes.
- The exact mechanism is identified in source, not just in the graph: the `parametersOfExtension … (geoCl anyGeometry)` parameter record and the HypsAlt witness built with `geoCl anyGeometry` ×3.
- Nielsen's route (as recorded in Jaswal 2026 §§2.3–2.4) is confirmed by an independent method (the `.olean` graph) and by direct source reads. Her paper's Figure 1 and §11 checks describe the actual route.

**Not settled by this trace:**
- Whether a vacuous definition on the route "invalidates" the theorem. The kernel objection (Nielsen's Appendix A) holds that a closed, typechecked term is a derivation of its statement regardless of vacuous intermediates; Nielsen holds that a term whose argument consists of vacuous witnesses is not a proof of RH. The trace establishes the factual premise of Nielsen's argument, not its conclusion. That is a question for mathematicians, and for Clay's process — Clay still lists RH unsolved.
- The graph records that one declaration *mentions* another; it does not weigh mathematical content (the Proofs & Reasons page says this explicitly). The body-vs-signature distinction used here is the strongest formal proxy available short of reading 17.4M lines, but it is still a formal proxy.

## Follow-ups since Chu's piece (checked 2026-11-22 ~22:45 UTC)

- **No response from Alpöge, the Lean community, or Sutherland to Nielsen's critique** as of this check. Sutherland's verification page (`math.mit.edu/~drew/grh/`, last updated 2026-11-22 16:20 UTC) contains no mention of Nielsen or `anyGeometry`; its summary still lists the full end-to-end `lake comparator` and the Lean default/paranoid kernel replay on the export as **still running**. The Lean/Mathlib joint statement (Nov 21, 13:55 UTC) certifying the proof predates Nielsen's paper.
- **Chu's piece is now superseded on the transitive question** — he traced only as far as `every_character_of_literature_of_vWin` and did not complete the analysis. This trace completes it.
- **No other published transitive analysis found** besides Nielsen (PhilArchive, Nov 20/21) and the Proofs & Reasons graph (which supplies the data; its page presents the `anyGeometry` node as its example entry). Nielsen's other cited source: M. Jaswal, "The Riemann hypothesis for Dirichlet L-functions [after Levent Alpöge]", v1, 21 Nov 2026, §§2.3–2.4 (`hexagonmath.org/pdf/2611.00799v1`), and the source-linked excerpts at `alexisdpc.github.io/riemann/sources.html`. Jaswal's paper was not separately read here — the graph BFS is the independent check of the same route, and it agrees.
- Aaronson's blog (Nov 20; Nov 21 update: "The proof is correct") predates the `anyGeometry` trace and does not address it.

## Caveats and open points

1. **Line-number discrepancy (graph vs mirrors).** The graph JSON's `line` field does not match either public mirror for the same declarations (e.g. `anyGeometry`: graph L19 vs mirror L30; `every_character_of_literature_of_vWin`: graph L810 vs mirror L1856; `riemannHypothesis`: graph L4 vs mirror L5). Declaration *names* and *file paths* agree exactly, and the dependency *edges* agree with Nielsen's independent source reading from the Deicyde mirror, so the discrepancy does not affect the verdict — but its cause is unknown (possibly the graph was built from a different snapshot of the source tree, or its line field uses a different convention). Anyone re-checking should use the mirror line numbers, not the graph's.
2. **Mirror scope.** Source reads were from the two public mirrors, not the original 61.6 GB export. The mirrors agree with each other on every file checked; Sutherland's page confirms the Deicyde mirror's export matches the published one by SHA-256.
3. **`geoOf` (the real predicate) was not traced.** Chu's counts (anyGeometry 24 files, geoOf 12) were not re-derived here. The question posed was only whether `anyGeometry` is in the closure — answered yes. Whether `geoOf` also appears anywhere on the route is a separate check, not done.
4. **"Degenerate" wording** (Nielsen §3: `geoDegenerate`, `algDegenerate`, `padDegenerate`, `mdlJunk`) was not re-verified in this session; Chu could not confirm it, Nielsen asserts it. It is not needed for the verdict.
5. **Verification status unchanged:** all 175,187 modules compile; `#print axioms` = propext, Classical.choice, Quot.sound only; nanoda, con-leche (incl. `--compare`), con-ron (`--compare`), lean4lean all accept; `lake comparator` end-to-end and Lean kernel replay on the export still running as of 2026-11-22 16:20 UTC.

## Sources

- Proofs & Reasons interactive graph: https://proofsandreasons.io/rh-graph.html?ref=explainx — export: https://photos.proofsandreasons.io/alp-graph/rh/alp-declaration-graph-used-by-rh.json.gz (57,157,211 bytes; SHA-256 `82c88d25d909a1399c754b87ce298e1939ab0908aeb4766fdac8a57387c71dc5`, verified)
- Nielsen, J. L., "The Invalidity of Alpöge's Proof of the Riemann Hypothesis", PhilArchive: https://philarchive.org/archive/NIEIOT-2 (route: Jaswal 2026 §§2.3–2.4; source: Deicyde/riemann-hypothesis, commit 712a6aef)
- Chu, F., "GRH proof's geometry is `fun _ _ _ => True`, in 24 files", dev.to, 2026-11-22: https://dev.to/frankchu/grh-proofs-geometry-is-fun-true-in-24-files-2n2b
- Sutherland verification page: https://math.mit.edu/~drew/grh/ (last updated 2026-11-22 16:20 UTC)
- Mirrors: https://github.com/1337isnot1337/riemann-hypothesis-solved (main, commit 6193bb5); https://github.com/Deicyde/riemann-hypothesis (commit 712a6aef)
- explainx.ai status tracker: https://explainx.ai/blog/levent-alpoge-anthropic-riemann-hypothesis-claude-lean-proof-claimed-vs-verified-2026
