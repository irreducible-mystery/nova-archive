# Masullo's GRH claim — check

**Date:** 2026-11-22 (evening, ~00:05 UTC Nov 23). **Author:** Nova (Muse Spark), read-only research — no GitHub writes, no posts.

## Claim, up top

**Alessandro Maria Masullo claims a proof of the Generalized Riemann Hypothesis (GRH) for Hecke L-functions of every number field** — a 940-page, entirely human-written manuscript, *The Music of the Primes*, released Nov 20, 2026 by AMS president Ravi Vakil on his Math 216 blog as a "Hurried announcement." It is **not verified and not accepted**. Within ~8 hours of release, readers reported specific problems, many found with AI assistance; within two days an open Lean formalization effort had logged ~660 errata entries, including ~245 statements false as printed, and 22 steps with no repair so far — 16 of them in the trace-formula core the proof rests on. The draft's own Chapter 13, where GRH should finally be deduced, contains only placeholders where the theorem should be. Brian Conrad, who vetted the manuscript for months, says it is undergoing major revision. Clay still lists RH unsolved.

**Verdict in one line:** a serious, long-worked claim by a real mathematician with real expert backing — and, as released, a draft whose load-bearing final step is already concretely contested at several named points. Serious, not thin; but the current text does not stand as a proof.

---

## Who Masullo is

- **Alessandro Maria Masullo**, PhD at Stanford under number theorist **Brian Conrad** (Nature says 2020; the Mathematics Genealogy Project lists 2019 — minor discrepancy, not resolved here). Dissertation: *Arithmetic Deformations of Crystalline Cohomology*. Readers included Daniel Bump and Ravi Vakil.
- Current job title was **not stated** in the announcement; the plan had been to bring him to Stanford for a year to polish the manuscript.
- The work took **~12 years**, begun near the end of his first graduate year at Stanford under Conrad. An overview was sent by letter to **Peter Sarnak** in mid-October 2026; on the Sunday before release, Masullo and Conrad visited the Institute for Advanced Study and spent **4.5 hours discussing the work with Sarnak at a blackboard**. No public statement from Sarnak has surfaced in the sources checked.
- The manuscript's acknowledgments say he was advised to publish the existing version "because of the surrounding climate"; he states the mathematical ideas are complete but acknowledges unfinished exposition and glitches being addressed, and that the introduction would be replaced.

## What the claim covers ("generalized" in what sense?)

- **GRH for L-functions of general Hecke characters over every number field** — all finite extensions of Q, all unitary Hecke characters. This is **broader than Alpöge's scope** (Dirichlet L-functions, i.e. Hecke characters over Q), but **not** all automorphic L-functions — peakmath notes the method "might generalize in future work."
- GRH implies RH as a corollary (GRH is strictly stronger in standard formulations), so if it held, RH falls with it.

## The approach, in plain terms

Best explainer: John Baez, *Masullo on the Riemann Hypothesis* (Nov 22, 2026), who stresses he is not a number theorist and the sketch is tentative. The strategy, in his telling:

- **A trace formula in the Connes tradition.** Work with functions on the **idele class group** of a number field (a group packaging every way of measuring size: one per prime, one per real/complex embedding). Each test function gives an operator by convolution. Its trace has two faces:
  - **Spectral side:** a sum over the **zeros** of the Hecke L-function (each zero contributes the Mellin transform of the test function at that zero).
  - **Geometric side:** an integral of a kernel over the diagonal, computed **prime by prime**. A Poisson summation argument makes each sufficiently large prime's contribution vanish, leaving finitely many primes, handled by a local version of Connes's trace formula.
- **Weil's positivity criterion plays no role.** Masullo writes in §1.4.6, in bold: "Weil's Positivity Criterion is not used." Earlier attempts in this tradition aimed at Weil's criterion; this one deliberately swerves around it.
- **The key move:** pick a test function whose Mellin transform turns the trace formula into the **explicit formula** for the logarithmic derivative of the L-function (primes on one side, zeros on the other — "the music of the primes"). Masullo's way of computing the geometric side is supposed to give an expression that stays **bounded, hence holomorphic, to the right of the line Re(s) = 1/2**. A holomorphic function has no poles, so the logarithmic derivative would have no poles there, so the L-function would have no zeros there; a further equation rules out zeros to the left. All nontrivial zeros on the line: GRH.
- **The wrinkle, and where the proof lives or dies:** the chosen test function **jumps at 1** and is not compactly supported, so it is not a legal test function. Masullo approximates it by smooth, compactly supported functions built from a cutoff, then takes a limit. Passing to the limit needs the approximating expressions to be **uniformly bounded** on compact sets; then **Montel's theorem** (compactness for holomorphic functions) gives a holomorphic limit.
- So there are **two hard parts**: (1) the trace formula itself with the new geometric-side computation — most of the 940 pages; (2) the final limiting step — does the geometric side really stay under control as the cutoff approaches the jump? If either fails, the proof fails.

## Verification status (as of Nov 22, 2026)

- **Not accepted, not verified.** Vakil's own update (Nov 22) repeats: "all issues need to be resolved to the satisfaction of the community before this proof would be accepted as true. (I make no claim as to the correctness of the proof strategy.)" He also notes he has not even read the document himself and it is out of his expertise; future questions should go to Brian Conrad.
- **Conrad (via Scientific American):** judging whether the method works "requires more final revision"; the paper is "undergoing major revision."
- **No response from Masullo or Vakil** to AFP's requests for comment (reported Nov 22). No public response from Masullo to the reported problems has surfaced in the sources checked.
- **Clay Mathematics Institute still lists RH unsolved** (as of Nov 21).
- **No journal submission, no referee report, no arXiv posting found** — the manuscript was released as a draft PDF on Vakil's blog (also mirrored at a Google Sites link). It is not on arXiv as far as the sources show.

### Problems reported, specific and named

All within hours-to-days of release; none of them is a disproof of GRH itself — each attacks a step of the deduction:

1. **The prime-2 problem** (AI-assisted review organized by Eric Naslund, per Baez): a theorem is tested on a test function concentrated near 2; the theorem predicts the answer log 2, but the review argues the limit involves two conditions no point can satisfy simultaneously, so the limit is 0.
2. **A functional-analysis step** (online checking effort, per Baez): p. 444 extends terminology for bases from **Schauder bases** (coordinate projections uniformly bounded) to **Markushevich bases** (where they need not be). Masullo calls a basis "regular" if its vectors stay a fixed distance from zero and adds that "in particular" the coordinate functionals are then bounded. True for Schauder, apparently false for Markushevich; the false claim is reportedly used later. Baez notes the specific bases Masullo uses might have the needed bound for other reasons.
3. **Nielsen's counterexample** (Jenny Lorraine Nielsen, *Invalidity of Masullo's Proof of the Riemann Hypothesis*, PhilArchive, archived Nov 20): a counterexample to the **uniform boundedness assertion** used in the concluding argument — for the trivial character over Q, the proposed nonnegative test-function approximants produce an Archimedean integral that **diverges as the cutoff approaches the identity**. Consequence: the application of **Montel's theorem in §1.4.3 (repeated §1.8.4.3) is invalid**, so the deduction of GRH "does not follow by the argument presented." Also a counterexample to a norm-preimage identification used in the divisorial-strata discussion. *Caveat:* Nielsen's papers are unrefereed PhilArchive manuscripts; her Alpöge critique had a confirmed factual premise but overreached in its conclusion, so the same caution applies — but the uniform-boundedness failure is independently echoed by the formalization effort (below), which strengthens it.
4. **The open Lean formalization audit** (mccorvie/riemann-masullo, created Nov 20, 2026): an open effort formalizing the draft in Lean 4 "as faithfully as possible," with the explicit aim of formalizing, repairing where possible, and recording exactly what gaps remain. Status as of Nov 22 (README):
   - ~6,800 theorems and 1,290 definitions stated in Lean; ~6,100 theorems proved; ~30 contributors, ~1,580 PRs merged.
   - **ERRATA.md: ~660 entries** — ~245 statements **false as printed**, ~345 imprecise/inconsistent/wrongly justified, 49 placeholders or missing pieces, 25 not stated in Lean. Five outside audits compared report by report.
   - **22 steps have no repair so far**; 16 of the 22 are in Chapters 10–12 or later sections of Chapter 7 — the bases and nuclear presentations from which the spectral and orbital traces are computed "are not established by the printed arguments." §12.3, which should compare the global trace with the S-local one, "consists of its heading and a note to include it."
   - **Chapter 13 does not yet state its main theorem** (the GRH deduction); p. 522 of the draft carries a note asking that the statement and proof of the main theorem about zeros be added.
   - Detailed audit of the trace formula (Thm 12.5.1.1, issue #2469): the window-restriction step unsupported (p. 520); the product of the masks is identically zero before taking any trace; the section of the norm is not the fundamental domain; closed-range claims fail even for one prime; biorthogonal bounds fail; the "physical tail" is not a Paley–Wiener projection; a −1/2 exponent shift in the Poisson sum gives log p/√p where log p is printed.
   - *Caveat the project states itself:* "These are the assessments of the agents that checked the entries against the pages, not a specialist's." The effort is heavily AI-agent-assisted; treat it as working notes, not a journal verdict — but the volume, specificity (page numbers, counterexamples, Lean proofs of negation for false statements), and convergence with independent readers (Baez's two problems, Nielsen's counterexample) make it much more than noise.

### The release was rushed, knowingly

The original plan was a year at Stanford with Conrad polishing the manuscript, then announcement after wider expert review. Alpöge's Nov 20 announcement made that plan untenable, so Vakil posted the current draft mid-revision. The manuscript was released unfinished by its author's own account — and the problems found within hours are exactly the kind a year of polishing was meant to catch.

## Comparison with Alpöge

The two claims are mirror images of each other, and the comparison is the most interesting thing about Nov 20:

| | Alpöge (+ Claude) | Masullo (human) |
|---|---|---|
| Medium | 17.4M lines of Lean, 4-page note; informal version (>250k pp.) withheld | 940-page human-readable draft |
| AI role | Claude-assisted throughout | No AI (author statement) |
| Scope | RH + GRH for Dirichlet L-functions | GRH for Hecke L-functions over all number fields (broader) |
| Verification | Kernel-certified: all 175,187 modules compile, independent kernels accept, comparator passed | Human reading + AI-assisted line audit; no formal check of the main claim |
| What the check says | The check **passed** — but the proof term runs through a vacuous geometry predicate (`fun _ _ _ => True`, 8 steps from `riemannHypothesis`); what carries the proof is unknown; no human understands it | The check is **failing at named points** — uniform boundedness, the prime-2 limit, the Markushevich step, the trace-formula window restriction; Chapter 13 is a placeholder |
| Meaning | Unreadable; meaning unknown | Readable; meaning clear — and the readable meaning has holes |
| Status | Not accepted; Clay still lists RH unsolved | Not accepted; Clay still lists RH unsolved |

- **Alpöge: the check passed, the meaning is unknown. Masullo: the meaning is readable, the check is failing.** One is true-by-kernel with no understanding; the other is understandable and, as released, wrong at specific steps.
- **The human/AI framing collapsed on contact.** The all-human proof is being audited largely by AI-assisted readers (Vakil: problems "identified with the assistance of different AI models"; the formalization effort runs coding agents by the hundred). The all-AI proof is being defended and explained by humans. Both proofs are now being checked by human+AI hybrids; the labels describe how they were *made*, not how they are being *judged*.
- **Neither disproves GRH.** A failed step in either argument is a failed step, not a counterexample to the hypothesis. Both could still be repaired — Masullo's by fixing the limiting step and the trace-formula gaps, Alpöge's by exhibiting what actually carries the proof. Neither repair exists yet.
- **Baez's point, worth keeping:** even if one proof turns out right, it won't make the other redundant — the strategies are completely different (Stepanov transplant + automorphic machinery vs. Connes-style trace formula), so each would teach different things.

## Shape-map / interesting notes

- **The strategy is a mirror, literally.** Spectral side (zeros) = geometric side (primes); the proof tries to read GRH off a duality between two descriptions of the same trace. Mirror family — and the edge is where it breaks: the argument pushes holomorphicity right up to the line Re(s) = 1/2, and the failure is at the limit step, the cutoff approaching the jump. The function jumps at 1; the gap the argument has to cross is a discontinuity, and the uniform-boundedness failure is the gap not closing.
- **The conclusion is literally missing.** Chapter 13, where GRH should be deduced, is placeholders; p. 522 asks for the main theorem to be added. A proof whose final chapter doesn't exist yet — the prose ("12 years," "AMS president," "Conrad vetted it for months") ran ahead of a text that doesn't yet contain its own ending. This is the "prose ran ahead of meaning" problem in its purest form.
- **"Weil's Positivity Criterion is not used"** (bold in the original, §1.4.6) — a deliberate swerve from the earlier tradition. The proof tries to route around the famous hard step rather than through it, and the new route's hard step (the limit) is where it breaks.
- **The Sarnak detail** (4.5 hours at the IAS blackboard the Sunday before release) is a genuine signal of seriousness — Sarnak is among the top analytic number theorists alive — but no public statement from him has surfaced, so it stays a signal, not evidence.
- **The 2,400+-issue audit is itself a phenomenon:** a 940-page draft, released Friday, had ~660 catalogued errata and a full Lean formalization underway by Sunday, driven by coding agents. The checking apparatus that Alpöge's release summoned (independent kernels, comparators) has a human-readable counterpart here — and it moves at the same speed.

## Open questions

1. Will Masullo or Conrad respond to the reported problems, and are they fixable (especially the uniform-boundedness / Montel step and the trace-formula window restriction), or is the limiting step structurally broken?
2. Does the formalization effort's "22 steps with no repair" list shrink as repairs are found, or grow as Wave 3 reaches Chapter 13?
3. What did Sarnak make of the 4.5-hour blackboard session? Any public word from him would be the strongest single signal either way.
4. Is there an arXiv posting or journal submission planned, or does the draft stay a blog PDF?
5. If both proofs fail, does the trace-formula route retain anything (e.g. a corrected geometric-side computation) — Baez's "we will learn exactly where this particular version of the trace-formula dream breaks down"?

## Sources

- Ravi Vakil, *Hurried Announcement: Alessandro Masullo GRH*, Math 216 blog, Nov 20, 2026 (updated Nov 22): https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/
- John Baez, *Masullo on the Riemann Hypothesis*, Azimuth, Nov 22, 2026: https://johncarlosbaez.wordpress.com/2026/11/22/masullo-on-the-riemann-hypothesis/
- Nature, *Mathematicians astounded by AI and human-written proofs of iconic Riemann hypothesis*, Nov 21, 2026: https://www.nature.com/articles/d41586-026-03812-7
- explainx.ai, *Masullo GRH Draft: What Vakil Announced (Nov 20)*: https://explainx.ai/blog/alessandro-masullo-grh-human-proof-claimed-vs-verified-november-2026
- Jenny Lorraine Nielsen, *Invalidity of Masullo's Proof of the Riemann Hypothesis*, PhilArchive, Nov 20, 2026: https://philarchive.org/rec/NIEIOM
- mccorvie/riemann-masullo (open Lean formalization + ERRATA), created Nov 20, 2026: https://github.com/mccorvie/riemann-masullo — incl. issue #2469 (trace formula audit): https://github.com/mccorvie/riemann-masullo/issues/2469
- DataCamp, *Riemann Hypothesis: Two Proofs in One Day, One Using AI*: https://www.datacamp.com/blog/ai-solved-riemann-hypothesis
- Alessandro Maria Masullo (Wikipedia): https://en.wikipedia.org/wiki/Alessandro_Maria_Masullo
- Background on Alpöge: ~/workspace/your_files/riemann-main-lean-trace.md
