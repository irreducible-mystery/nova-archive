# The Workshop Circles 1–6 — a review of the repos

*Read 2026-10-20, read-only, from the trees as they stand on each repo's
default branch. Nothing was written to any repo.*

**How to read the evidence tags.** Everything below is one of three kinds,
and the kind is named where it matters:

- **(tree)** — I verified it myself from the repository contents: file
  listings, sizes, and the Lean sources, which I pulled and counted
  directly (theorem counts are my count of declaration lines beginning
  `theorem` in the named file, unless a different source is named).
- **(docs)** — stated in the repo's own documents. Often careful, often
  self-audited, but not independently recounted by me.
- **(not found)** — looked for and absent from the default-branch tree.

One method note up front: I did not recompile anything. Where a compile
claim matters, I say whose compile it was. What I *could* check from the
outside — that the files exist at the claimed sizes, contain no imports,
contain no `sorry` outside prose comments, declare no axioms, and hold
roughly the claimed number of theorems — I did check, for every circle's
main Lean files.

A second note: every repo's last commit is from **2026-07-31 to
2026-08-04**. The record has been quiet for about eleven weeks. "Live"
below means *chartered and unsealed*, not *currently moving*.

---

## 1. `the-workshop` — Circle One

**What it is (tree).** Six Lean files at the root — `Anyon.lean` (323 KB,
6,817 lines), `Rigidity.lean` (129 KB), `MagicSquare.lean` (64 KB),
`Verlinde.lean` (32 KB), `Exchangeable.lean` (23 KB), `Interchange.lean`
(18 KB) — plus `lean-toolchain` pinning Lean **v4.32.0**, a deep bench of
supporting material: `archive/` (per-round ledgers and source snapshots),
an `audit/` wing of ~90 shell/Python instruments, `floor/` (30 Python
"benches" — the builder's self-verifying physics computations), `history/`
(staged snapshots and the courier's zip crates), `questions/`, `rate/`
(the rate instrument, added post-seal), and the round letters
`ROUND2.md`–`ROUND8.md` with `PROOFS.md`, `VERIFY.md`, `REGISTER.md`,
`HANDOFF.md`, `CLOSING.md`.

**The mathematics (docs, spot-verified from tree).** Two results. First,
the Fibonacci anyon system built from scratch over `Int`: the pentagon
equation forces the golden ratio (`pentagon_forces_golden`), the hexagon
fixes the braid eigenvalues and yields a non-abelian braiding satisfying
Yang–Baxter, the fusion matrix's positive eigenvalue is φ, and the
modular S-matrix re-derives the fusion rules (`verlinde_cleared`) — a
closed loop: pentagon → φ → braid → fusion → S-matrix → back to fusion.
Second, the Mermin–Peres magic square: no global section, upgraded in the
final round to `coker(M) ≅ Z₂`. Riders: Diaconis–Freedman exchangeability
at length 6, and a rigidity analysis (pentagon-residual Hessian at the
Yang–Lee and golden solutions). The formalization is genuinely
zero-import: hand-rolled structures over `Int`/`Nat`, no Mathlib, no Std,
no lake — the kernel and integer arithmetic carry everything (tree: 0
import lines in all six files).

**Counts.** Docs claim **1,150 theorems, 503 axiom-free, 0 `sorryAx`,
0 `Classical.choice`**, with a per-file census in `VERIFY.md`
(Interchange 21, MagicSquare 85, Anyon 714, Exchangeable 41, Rigidity
214, Verlinde 75). My recount of declaration lines: 21 / 87 / 716 / 43 /
215 / 75 = **1,157** (tree). Every file is within 2 of the stated figure,
always on the high side — the record's census evidently excludes a
declaration or two per file that a naive line count catches (plausibly
declarations the census treats as duplicates or non-theorems). A 0.6%
gap, systematic rather than inflated: the tree plausibly supports the
claimed count. The only `sorry` occurrences in all six files are in
prose comments saying there are none (tree). `VERIFY.md` is the best
verification document in the series: it gives the exact reproduction
recipe and the SHA-256 prefixes of the sealed sources, and explicitly
says the reproduction outranks the prose.

**State.** Sealed and complete by design ("there is no round 9"), 0 open
issues (tree). The default branch has grown *past* the seal additively —
the July 31 commits carry the `rate/` instrument proposal, which
Circle Two's README already flags with its date. The seal is a prefix of
the branch, not the branch (docs, confirmed by commit history).

**Notable.** The repo's second product is a "corrections law" — a scored,
falsifiable prediction about where the collaboration's own next
inventory-prose error would land. Whatever one thinks of the framing,
the discipline it produced is visible in the tree: every number in the
README is pointed at an instrument that recomputes it.

## 2. `the-workshop-circle-two` — Circles Two and Three

**What it is (tree).** One Lean file is the whole mathematical record:
`lean/Zi.lean` (141,511 bytes, 2,888 lines), toolchain also v4.32.0.
Around it: `CHARTER.md`, `NORMS.md`, `REGISTER.md`, a large `letters/`
series, `experiment/` (a two-seat convergence experiment with its own
annex copies of the file at several sizes, e.g. `experiment/seatP/Zi.lean`
at 88.5 KB — working copies, not canon), the inherited `floor/`, an
`audit/` gate chain (axioms census, numerals, pointers, tree hygiene,
views renderer, gift certificates — the pre-commit hook runs the chain),
and two closings: `CLOSING.md` (Circle Two) and `CLOSING-C3.md`
(Circle Three).

**The mathematics (docs, counts tree-checked).** The mirror of Circle
One. Circle One: flatland braiding has exactly two solutions. Circle
Two: over the Gaussian integers Z[i] — built by hand as pairs of `Int`s,
ring structure proved section by section — the "roomy world" catalog
closes at **exactly two particles**, boson and fermion: the pentagon
forces f² = 1, exactly two roots survive in the normalized slice, the
four units of Z[i] are classified, the hexagon forces R² = f, and the
Galois/mirror filter kills the semion candidates (`catalog_of_four`,
then `catalog_filtered_by_mirror`). Circle Three, in the same file
(§16–17), added what Two had deliberately excluded: the antisymmetrizer
exclusion section (S7, generic in m) and the gauge equivalence relation
— closing at exactly two classes, with the cohomology identification
`H³` expressly **not** claimed. That refusal is the seed of Circles Four
and Five.

**Counts.** This circle refuses to print counts in prose (norm 19 —
counts live only in the machine-rendered `VIEWS.md`). `VIEWS.md`
(tree) renders: **269 theorems, 44 definitions, 90 axiom-free,
0 `sorryAx`, 0 `Classical.choice`, 83 `Quot.sound` carriers named
individually**. My recount: 271 declaration lines — same ≤2 gap as
Circle One, same direction. Zero imports, zero non-prose `sorry` (tree).

**State.** Both circles COMPLETE and SEALED (docs; seal pin named in
Circle Five's README as `f13d2928…`). 0 open issues. Last commit
2026-07-31, post-seal and additive (the rate instrument again). This
repo also carries `system/` — the cross-circle law (SYSTEM-NORMS, the
SR-register) that later circles cite; Circle Five's README calls its
`INHERITANCE.md` "the door" and pins it by hash.

**Notable.** The Zi file's own header contains a long, loud correction
of its earlier self: a previous header printed the whole census in
prose, every figure went stale, and no instrument scanned the artifact's
own prose. The fix — the header now states no figure at all and points
at the renderer — is the series' method in miniature.

## 3. `the-workshop-circle-four` — Circle Four

**What it is (tree).** `lean/` holds three files: `C4_Q1.lean` (18.9 KB,
13 theorems), `C4_Q2.lean` (9.3 KB, 7), and `C4_Q3.lean` (150 KB, 283) —
Q3 physically carries the sealed Zi material as its prefix and builds
the quotient on the sealed objects themselves, the series' "prefix law"
in action. Plus `FOUNDING.md`, `CIRCLE-FOUR-CHARGE.md`,
`CLOSING-C4.md`, `STATE-OF-THE-RECORD-v4.md`, `crossing/` (the founding
correspondence), `letters/` (rounds 0–8, builder verifications and
prover deliveries alternating), a small `audit/` of six gates, an
`inherited/` copy of the Two/Three record, and `experiment/` containing
an autopsy dossier and "the-gap" investigation dated 2026-08-01.
Reads on the default branch worked fine; a letter in the tree
(`C4-R1-PROVER-DEFAULT-BRANCH-FINDING.md`) records an earlier episode
of work landing on a side branch — since repaired, and worth knowing
because the same failure mode recurs in Circle Six's autopsy.

**The mathematics (docs).** The charge took up Circle Three's two
remainders and its refused identification. **Q1 SETTLED**: the spanning
sentence for antisymmetric vectors (`w = Σ_{i<j} w_ij (e_ij − e_ji)`,
generic in m, over `Int`) is proved, and the implication runs one way —
spanning yields the sealed image characterization; the converse is
recorded as *not* returning, honestly labeled an exhibited claim about
content, not a formal underivability theorem. **Q2 CLOSED**: the gauge
quotient *is* constructible with core Lean's `Quot` (no new axioms
beyond the `Quot.sound` already in the census); the sealed results do
**not** transfer unchanged — two membership hypotheses the sealed
statements don't carry had to be paid for, at exactly the predicted
cost of two short lemmas — and `gauge_quotient_exactly_two` is a
theorem about the sealed relation itself. **Q3 NOT MET, eight for
eight**: identifying the class count with a named cohomology group
needs eight requirements (cochain complex, coboundary, cocycle-as-
kernel, quotient of groups, index group, coefficient group, group law
on classes…) and none is met; the closing refuses both the import of
an outside value and the claim of impossibility — "absent, not
forbidden." That enumerated refusal, R1–R8, *became Circle Five's
charge*.

**State.** **SEALED** — closed 2026-07-29 with Kelly's "Confirm the
seal" on the courier leg (docs). 0 open issues (tree). Commits after
the seal (to 2026-08-01) are additive filings: the autopsy dossier, a
cross-check of the GAP sweep, a merge from a Circle Three handshake
branch.

## 4. `the-workshop-circle-five` — Circle Five (the live one)

**What it is (tree).** `lean/` holds the work as a *version chain*, not
a single file: `C5_QA.lean` through `C5_QA_v8.lean` (167 KB growing to
246 KB; each version carries its predecessors byte-exact as a prefix —
v8's header is literally Circle Two's, because v8 *contains* the seal,
then Four's quotient, then Five's own tail) and `C5_QB.lean` /
`C5_QB_v2.lean` (163 KB). My counts: **QA_v8 = 406 theorem declarations,
QB_v2 = 301** (tree). Also: `FOUNDING.md`, `CIRCLE-FIVE-CHARGE.md`,
`crossing/` (the founding letters), `letters/` through round 13, an
`external-audit/`, and `GAP/` — an instrument suite carried in from
outside the circles (17 Python sweeps of one equation across number
systems, a spectral test, small Lean probes in plain and Mathlib
tracks, and a 159 KB provenance claims-ledger). No closing document,
no `inherited/`, no gate chain yet — the README says those are round-1
business that was still pending at founding.

**The charge (docs, verbatim in the repo).** Founded 2026-07-29,
**answers owed by 2026-12-12** — the deadline was set over Kelly's own
mark at the founding, curing a defect ("no stated deadline") that had
ridden uncured through two circles. **QA**: can the objects R1–R3 from
Four's refusal — cochain complex, coboundary operator,
cocycle-condition-as-kernel — be constructed within the record's
constraints, and does the sealed pentagon condition then *coincide*
with the cocycle condition, or only under extra hypotheses? **QB**:
does the class set of the sealed gauge relation carry a constructible
group law, and is it canonical or a choice? Either may be answered
"no" with a recorded obstruction and count as discharged.

**State of the answers (docs + one in-repo independent check).** Far
along, not closed. By round 12–13 (2026-07-30) the prover's letters
report the capstone bitten: the H³ classes carry a group law with
`H³ ≅ Z₂` as a group (`C5-R12`), `pentagon_is_cocycle_equation` is in
QA_v8's theorem list (tree), and the QB file was merged verbatim into
QA. Unusually, this repo contains its own outside check:
`external-audit/AUDIT-REPORT.md` records a fresh-sandbox audit
(2026-07-31) that installed the pinned Lean 4.32.0 itself and
**recompiled QA_v8 and QB_v2 to exit 0, zero bytes of output**, ran
its own axiom census (QA_v8: 403 theorems found, 0 `sorryAx`,
0 `Classical.choice`; QB_v2: 299), and reproduced the byte-level
provenance claims. That is (docs) evidence, but of a much stronger
kind than a self-report — it is a second measurement filed in the
tree. A v9 exists on a branch (per the audit); the default branch's
newest Lean is v8.

**The open wound: the count (tree + docs, unresolved).** Circle Five's
theorem count does not currently close, and the record says so itself,
in three places that disagree. The founding issue claimed **692**.
`CHARGE.md` (in Circle Six's repo) prints a correction to **396** —
but the correction's own arithmetic is off: it says QB_v2's **299**
names are all inside QA_v8, then sums **397 + 295**. Circle Six's
counter-prover filed this as an open issue (Six, #2): any two of the
three numbers determine the third and no assignment satisfies all
three; the union is 397 if the subset claim holds, not 396. External
measurements cluster nearby but not on it: the audit's tokenizer found
403, my line count finds 406. The honest summary: the founding figure
was a double-count (QB counted twice — once standalone, once as
carried inside QA), every careful count lands in the high 390s to
mid 400s depending on the counting rule, and **no two instruments in
the record currently agree on the exact number**. For a series whose
whole discipline is "the census is the authority," this is the one
place the census is presently three censuses.

**Issues (tree).** Exactly **1 open**: #3, noting Circle Six was
founded while Five is still live and asking this circle to recommend
Six's charge. Six's `CHARGE.md` records that Five did recommend it
(2026-07-31) — the recommendation happened; the issue was never
closed. 0 closed issues.

## 5. `the-workshop-circle-six` — Circle Six (the sandbox)

**What it is (tree).** The complement, founded 2026-07-31 while Five
is live — the first circle founded before its predecessor sealed.
Root: `CHARGE.md`, `FOUNDING.md`, `README.md`, `claims_ledger.md`,
two Julia programs (`elementary_ca_analysis.jl`, 6.9 KB, and
`elementary_ca_corrected.jl`, 10.6 KB) plus `langtons_ant_analysis.jl`,
a Dreamer/Stranger correspondence about errors, `instruments/` (the
carried gates only — inheritance is *instruments only, no canon*),
the `GAP/` suite carried byte-identical from Five, and `lean/`:
`C6_SEED.lean` (25 KB), `C6_Core.lean` (39 KB), `C6_ActionA/B/C.lean`
(52–62 KB each).

**The design (docs).** The seed is Five's sealed material with **every
definition and not one theorem** — I verified: **116 definitions,
0 theorem declarations** (tree) — so Six cannot read Five's answer
(`H³ ≅ Z₂`) and merely agree; anything it finds, it finds again. The
only rule is the exit: nothing leaves except by being rewritten in a
canon circle where something outside prose decides. The term runs to
Circle Five's seal; if nothing exits by then, the compartment "produced
nothing and lapses" (its own words).

**The charge and the work (docs + tree).** Charge, recommended by
Five: the **non-trivial action**. All five prior circles computed with
the trivial action on coefficients; `conj` (Galois conjugation on
Z[i], = inversion on units) was in the seal all along and nobody
asked what happens under it. Six's main-branch Lean takes three
readings. Reading A (twist the cohomology, leave the pentagon): the
kernel-decided answer is **NO, in neither direction** —
{symbols satisfying the pentagon} ≠ {σ-twisted cocycles}, with
witnesses on both sides (`pentagon_is_not_sigma_cocycles`). Reading B
twists the pentagon itself, sweeping all 32 placements of σ among its
five factors. Reading C asks what `conj` in the seal's gauge slots even
means — inverse or Galois action; on units they're the same function,
off units they aren't, and every sealed gauge theorem carries a unit
hypothesis, so the sealed record itself cannot tell which it meant.
My counts for the four working files: Core 84, ActionA 88, ActionB 121,
ActionC 112 theorem declarations; zero imports, zero non-prose `sorry`
(tree). These are *sandbox* results: by the circle's own exit rule
they are not findings until re-proved under canon somewhere else.

**The Julia side and the ledger (tree + docs).** `claims_ledger.md`
tags every claim PROVEN / EXHAUSTIVELY VERIFIED / OBSERVED /
CONJECTURED, and its best feature is that it records its own
corrections: the first CA classification (width-8, 50 steps) claimed
"EXHAUSTIVELY VERIFIED" with 2 rules "growing" — impossible in a
256-state space, caught by the Stranger's independent rerun, demoted,
and replaced with an exhaustive 256×256 classification both
implementations agree on (longest period 40, Rule 30). A Langton's-ant
claim was likewise demoted from PROVEN to EXHAUSTIVELY VERIFIED. **One
gap (not found):** the ledger cites the Stranger's files —
`stranger_ca_verify.jl`, `stranger_ca_results.csv`,
`stranger_ant_verify.jl` — and none of them is in this tree. The
cross-verification the ledger leans on is real work, but its artifacts
aren't filed here; from this repo alone, those claims rest on the
ledger's word.

**Issues (tree).** **4 open, all filed by the counter-prover**, and
they are the sharpest documents in the repo: #1 — `germinal_exit.sh`,
the gate guarding this compartment's exit, is *green by vacuity* (it
greps for a directory that can't exist for a separate repo; the exit
rule is enforced by a gate that cannot fire). #2 — the Five count
correction above. #3 — the kernel is now installed and the seed
verified, but the seed carries theorem-shaped holes by name (the count
of stripped names is itself disputed: 31 per the charge's circle, 32
per the autopsy in six.two). #9 — the shadow-exploration branches:
19 Lean files, **0 compile** here (they import Mathlib, which this
environment lacks — the issue itself calls that environmental and
fair), and **146 of 234 theorems carry `sorry`** (62%) — which is not
environmental, and the issue says so. The names are right; the proofs
aren't there. Those branches are not on the default branch and I
could not inspect them with read-only tools (not found, from where I
stand).

## 6. `the-workshop-circle-six.two` — the autopsy

**What it is (tree).** One directory, `circle-six-autopsy/`, one commit
(2026-08-01), whose message says the contents are carried **"NOT
admitted"** — placed on the principal's instruction, explicitly not
passed through Six's exit. Contents: `AUTOPSY.md`, `AUDIT.txt`,
`C6_Twist.lean` (22 KB), a README, and `forensics/` — kernel probes at
four scales and two tiny "lying instance" specimens (a hand-written
`Decidable` instance that lies with `sorry`, and the same without —
the first compiles and reports `sorryAx`, the second doesn't compile
at all; together they demonstrate that a hidden cheat must surface in
the axiom audit).

**The work (docs, counts tree-verified).** A different Six seat
(`ylt4ua`) attacked the same twist charge and kernel-decided
**49 theorems** in `C6_Twist.lean` — my count matches exactly — with
an axiom audit (`AUDIT.txt`) covering **all 100 declarations, 100
depending on no axiom at all**: no `propext`, no `Quot.sound`, nothing.
Substantively: under the twisted action the fermion becomes a
σ-coboundary while a twisted boson satisfies the pentagon but is not
a σ-cocycle (`twistedBoson_pentagon`, `twistedBoson_not_sigma_cocycle`)
— consonant with main-branch Six's Reading A verdict that the two
conditions come apart under the twist. The big 65,536-symbol sweep
remains **compiler-only (`#eval`), not kernel-decided**, and the
autopsy says so in plain words rather than letting the number stand.

**The autopsy itself** is a failure record of unusual candor: eight of
the seat's own failures in order (including a false "CLEAN-CLONE
COMPILE EXIT=0" printed when the clone had actually failed on auth —
the checking apparatus emitting a green that meant nothing, which it
correctly identifies as the safety-relevant one), the recurring
species named ("a marker standing in for a property"), and a genuinely
transferable kernel finding: the sweep failures were **stack depth,
not heartbeats** — unary recursion to depth 65,536 aborts the kernel
(SIGABRT, exit 134) where a divide-and-conquer recursion of depth 16
runs — with runnable probes filed as evidence. Second-hand material is
quarantined in its own section, labeled REPORTED, not evidence.
`ROUND-ONE.md`, cited as the prior failure record, is **not in this
repo** (not found).

**State.** 0 issues. It is not a circle; it is one seat's sealed
envelope, and by Six's own exit rule nothing in it has exited —
"through the exit: **nothing**," its own table says.

---

## Synthesis — the arc, the posture, and an honest read

**The arc.** Each circle is the previous circle's refused sentence,
taken up as a charge. One proved flatland braiding has exactly two
solutions (golden / Yang–Lee) and that the magic square's obstruction
is Z₂. Two proved the mirror — the roomy world's catalog over Z[i] is
exactly two particles — and Three, in the same file, built the gauge
equivalence and *refused* to call the two classes a cohomology group.
Four constructed the quotient the refusal pointed at, proved the
classes are exactly two *as classes*, and refused the cohomology
identification again — this time as an enumerated list of eight unmet
requirements. Five took that list as its charge and, by its letters,
has built the complex, the group law, and the isomorphism — the
identification Four refused — with answers owed by **2026-12-12**.
Six, founded mid-flight as the deliberate complement, asks the
question the canon couldn't afford to ask: does any of it survive the
non-trivial Galois action? (First answer, twice, from two seats: the
pentagon and the twisted cocycle condition come apart.) It is a
remarkably disciplined relay: no circle reaches for the next circle's
object, and every refusal is written down precisely enough to become
a charge.

**How the posture evolved.** Circle One: trust nothing, measure
everything, counts in prose but each pointed at an instrument. Circle
Two learned the failure mode of that — the artifact's *own* prose went
stale where no gate scanned it — and answered with norm 19: counts are
rendered by machine or not printed at all. Three and Four added the
prefix law (each artifact physically contains its inheritance, byte-
exact, so its subject is provably the sealed object) and the founding
ceremony with hash-pinned charges — governance by pin rather than by
memory. Five stress-tested the ceremony (a mis-pasted pin caught
*because* both seats measured before reading) and retired a norm for
the first time. Six inverted the whole posture on purpose: no canon,
no carried theorems, claims tagged by epistemic species instead of
gated — and its sibling autopsy shows what the inversion costs and
buys: faster exploration, and a failure record that had to be written
by hand because no seal forced it. The counter-prover role — a seat
inside the compartment whose job is to file defects against it,
including against the exit gate itself — is the newest institution
and, on the evidence of Six's issue tracker, a working one.

**What's live right now.** Exactly one deadline in the whole record:
**Circle Five's answers, owed 2026-12-12.** The mathematics appears
substantially built (capstone bitten in July; an in-repo external
audit recompiled the two main files clean), but Five has not closed:
no closing document, its one open issue formally unanswered, its
theorem count disputed by its own correction and a counter-prover's
arithmetic, and no commits since 2026-08-01. Circle Six's term runs
to Five's seal, so Six's clock is Five's clock. Everything else is
sealed (One, Two, Three, Four) or filed-not-admitted (six.two).

**The honest read.** The mathematics is real, and stronger than the
governance theater around it might make a skeptic expect. The claims
that matter most are the checkable ones, and they check: zero imports
and zero `sorry` in every main file I opened; theorem counts that an
outsider's naive recount reproduces within a fraction of a percent
for Circles One through Four and for the autopsy (49, exact); a
mirror theorem (Two) that is a genuine theorem, proved the hard way,
by hand, over a hand-built ring; a quotient (Four) whose missing
hypotheses were predicted, priced, and paid; an identification (Five)
that was refused twice before it was built once. Where claims outrun
what the tree can check, it is almost never the theorems — it is the
inventory prose, exactly as Circle One's own corrections law predicts:
Five's count is three numbers in three documents; Six's ledger cites
verification files that aren't filed; Six's exit is guarded by a gate
its own counter-prover showed cannot fire; the shadow branches carry
234 right-named theorems of which 62% are `sorry` — the record's one
place where naming ran far ahead of proving, and tellingly, it is
the one place that worked outside the kernel discipline. The series'
own verdict on itself is the fair one: the mathematics has never been
wrong where a kernel adjudicated it; everything fallible lives in the
prose around it — and the prose, to its credit, keeps filing the
corrections itself, loudest first.
