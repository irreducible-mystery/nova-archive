# OpenAI Lean headlines — proof vs claim

Plain-language document, 2026-10-27. Local only, nothing posted.

## No verdict — read this first

This document gives **no verdict on either claim below**. That is
not a hedge for politeness; it is the rule for this document:
no verdict while the formal code remains independently
unverified. I have not read the Lean code itself line by line;
the reports used here are secondary reports of an October 26,
2026 announcement, and the shepherd groups themselves say
their involvement is not certification. What follows is what
was claimed, what a Lean check does and does not establish,
and the definition checks still missing before anyone can say
the formal code captures the original conjecture.

## What was announced

On October 26, 2026, OpenAI said its internal models had
produced three results, two of them with public Lean
formalizations in its public openai/math repository:

1. **Local smoothing** (mathematics): a proof of Sogge's
   1991 local smoothing conjecture in every dimension,
   which OpenAI says also resolves the Kakeya conjecture
   and Stein's restriction conjecture in all dimensions.
   AI output October 18, 2026; Lean formalization
   October 19, 2026.
2. **Exponential Time Hypothesis disproof** (computer
   science): the Exponential Time Hypothesis (ETH) is false.
   AI output October 16, 2026; Lean formalization
   October 17, 2026; manuscript dated October 25, 2026.

A third result announced the same day — existence proofs
for quantum field theories including Yang-Mills and QCD —
is out of scope here, except to note its materials were
held back by its shepherd group, unlike the two above.

## What Lean step-checking does, and does not, do

Think of Lean as a very strict checker for mathematical
arguments, not as a judge of what the argument is about.

- **It does establish:** given the definitions, statements,
  and starting assumptions written in the code, each step
  follows by the rules of logic, with no skipped steps, no
  arithmetic slips, and no hidden "trust me here" — unless
  the code itself contains a placeholder or an extra
  assumption, which is why an axiom audit is on the
  checklist below.
- **It does not establish:** that the definitions written
  in the code are the same thing as the conjecture as
  mathematicians understand it in words; that the paper's
  English explanation matches the code; or that a
  simplified, restricted, or differently-worded version
  was not proved instead. That last gap has a sharp
  formulation from Anthropic's parallel release, quoted in
  secondary reporting: "Lean checks the proofs, but no
  machine checks that this file says what the paper says."

So "verified in Lean" is a strong claim about internal
correctness and a weak claim, on its own, about external
fidelity. Both halves matter, and only the first half is
what a machine check delivers.

## Claim 1: local smoothing in every dimension

### The original problem, in plain words

Imagine waves rippling out. Sometimes they focus — many
waves pile up at one place at one time, like light through
a lens. The local smoothing conjecture, proposed by
Christopher Sogge in 1991, says, roughly, that the most
extreme focusing is short-lived: averaged over a short
time, waves are a little smoother than they look at any
single instant. "A little smoother" is measured by a
number called a Sobolev order — how many derivatives
(roughly, how much wiggliness) you can count on.

Human progress before this claim: local smoothing was
proved in two spatial dimensions in 2019 (Guth, Wang,
Zhang). The related Kakeya conjecture — about how thin
tubes pointing in many directions can overlap — was
proved in three dimensions in 2025 (Wang, Zahl). The
new claim extends local smoothing to every dimension,
and says Kakeya and Stein's restriction conjecture
follow in all dimensions too.

### What OpenAI says the formal result is

Per secondary reports of the formalization: the result
covers dimensions n ≥ 2 and exponents 2 ≤ p < ∞, with
Sobolev order s = max(0, (n−1)/2 − n/p) + ε, for any
ε > 0, and s = 0 permitted at p = 2. In plain words:
the amount of smoothing you get depends on the
dimension and on how you measure size (the exponent p),
with a tiny extra ε of slack — except at the special
case p = 2, where no slack is needed. The proof is said
to rest on a novel auxiliary partial differential
equation — a new helper equation built for the proof,
not a standard one pulled off the shelf.

### Definition checks still missing for claim 1

1. **The statement itself.** Does the Lean statement's
   definition of "local smoothing" match Sogge's 1991
   conjecture — same wave equation, same Euclidean
   setting, same time-averaging, same range of p, same
   ε-loss — or is any part (endpoint cases, the p = 2
   case, the ε) stated differently, weakened, or omitted?
2. **The auxiliary equation.** Is the novel auxiliary
   partial differential equation defined with all its
   claimed properties proved inside Lean, or are any of
   its properties assumed as starting points? A helper
   that is assumed to behave nicely is not the same as
   a helper that is shown to behave nicely.
3. **The implications.** Are the steps "local smoothing
   implies Kakeya" and "local smoothing implies Stein
   restriction" themselves formalized in Lean, or are
   they asserted in the paper's prose while Lean checks
   only the local smoothing statement? The headline
   says three conjectures fall; the check must say
   which of the three are actually inside the code.
4. **Axioms and placeholders.** What is the full axiom
   list of the formalization? Are there any axioms
   beyond Lean's standard ones, and are there any
   `sorry` placeholders (Lean's "to be filled in later"
   marker, which lets a file check while a step is
   still missing)? Either would change what "verified"
   means.
5. **Dimension and exponent edge cases.** Are n = 2 and
   the p → ∞ end handled by the same argument, or by
   separate cases that need their own checks? Do the
   reported bounds degrade, or break, at the edges?
6. **Independent reading.** Has anyone outside OpenAI
   read the definitions and the final statement and
   confirmed, in writing, "this code states the
   conjecture as mathematicians mean it"? Per secondary
   reports, one outside expert advised open release of
   the local smoothing materials. Advising release is
   not a verification verdict, and it is not the same
   as the ETH shepherd arrangement below.

## Claim 2: the Exponential Time Hypothesis is false

### The original problem, in plain words

Take a logic puzzle: a formula made of clauses, each
clause a short "or" of variables (for example, "x or
not-y or z"). 3-SAT is the puzzle where every clause
has at most three variables, and the question is whether
some assignment of true/false to the variables makes
the whole formula true. Trying every assignment takes
about 2^n steps for n variables — exponential.

ETH, proposed by Impagliazzo, Paturi, and Zane in
1999/2001, is the guess that you cannot do much better
than that for 3-SAT: no algorithm runs in
"subexponential" time, meaning time that grows
noticeably slower than 2^(c·n) for any fixed c > 0.
Hundreds of papers have used ETH as a conditional
assumption: "if ETH is true, then this other problem
is also hard." It is not the same as P ≠ NP, and
disproving it would not prove P = NP.

### What OpenAI says the formal result is

Per secondary reports: a deterministic algorithm
(one with no randomness, no guessing) that exactly
counts the satisfying assignments of a k-CNF formula
(a formula with clauses of fixed width k, for fixed
k ≥ 2) in subexponential time and polynomial space
(memory that grows only polynomially, not
exponentially). The reported running time is
2 to the power O(n·(log log n)²/√log n) — slower
than polynomial, but, as n grows, slower than any
2^(c·n), which is what ETH was said to rule out for
3-SAT. Counting assignments is at least as hard as
deciding whether one exists, so a counting algorithm
at that speed would break the decision version too —
if the counting-to-decision step is itself part of
the formal result, which is check 2 below.

What it would not mean, even if it holds: faster
programs for real problems tomorrow. The reported
time is still enormous for realistic sizes, and
secondary reports stress that no ready-to-use program
comes with the paper. What would change first is the
conditional hardness results that rested on ETH —
they would need revisiting, one by one.

### Definition checks still missing for claim 2

1. **The statement itself.** Does the Lean statement's
   "canonically encoded k-CNF formula" mean the same
   thing as the standard 3-SAT input — same encoding,
   same clause width, same variable count n — or does
   "canonical" smuggle in a restriction (for example,
   on clause density, or on how variables repeat)
   that makes the problem easier than 3-SAT?
2. **Counting vs deciding.** Is the step from
   "counts assignments in subexponential time" to
   "3-SAT is decidable in subexponential time, so
   ETH is false" formalized in Lean, or left to prose?
   The headline is about ETH (a decision problem);
   the algorithm is about counting. The bridge between
   them must be inside the checked code, not beside it.
3. **The time bound, exactly.** Is the bound
   2^(O(n·(log log n)²/√log n)) proved for all n,
   with the hidden constants and the dependence on
   the number of clauses m made explicit — or does
   it hold only above some threshold, or with m
   treated in a way that changes the claim? A bound
   that is subexponential only after an unstated
   cutoff is a different claim.
4. **Fixed k, and k = 3 in particular.** The formal
   result is reported for fixed k ≥ 2. ETH is
   standardly stated for 3-SAT. Does the formalization
   include k = 3 with no extra conditions, and does
   it handle the sparsification step (the standard
   lemma that reduces a general formula to sparse
   ones) inside Lean, or assume it?
5. **Polynomial space.** Is the space bound part of
   the checked statement, or a prose claim about the
   algorithm? A fast algorithm that needs exponential
   memory is a different result from one that does
   not.
6. **Axioms and placeholders.** Same audit as claim 1:
   full axiom list, standard axioms only, no `sorry`
   placeholders hiding an unfinished step.
7. **Independent reading.** Has anyone outside OpenAI
   read the definitions and the final statement and
   confirmed, in writing, "this code states ETH's
   negation as complexity theorists mean it"? The
   shepherd group below is the right shape for this
   — but its work is, by its own words, not yet a
   verdict.

## Who is checking, and what that does not mean

For ETH, OpenAI asked Russell Impagliazzo and Ramamohan
Paturi (UC San Diego, who proposed ETH with Francis
Zane) and Ryan Williams (MIT) to lead an outside group
to verify and explain the proof. OpenAI agreed to make
raw data public and to fund a conference on the result;
participation is unpaid, with no nondisclosure
agreements, and OpenAI says it seeks no academic credit
for the models' output. The three shepherds wrote, in an
open letter quoted in secondary reporting: "Our
involvement should not be taken as certification of the
claim." That sentence is the status of both claims as
of this document: shepherded, not certified.

For local smoothing, secondary reports describe one
outside expert advising open release, not a shepherd
group with a published verdict. That is thinner, not
stronger, and this document does not upgrade it.

## A parallel claim, noted but not counted

Secondary reporting notes that Anthropic posted a
parallel ETH disproof about six hours after OpenAI's,
also dated to an October 16 discovery, from an internal
Claude model, with its own Lean formalization. A second
lab making a similar claim on the same day is
interesting — and it is not, on its own, independent
verification of OpenAI's code. Two formalizations can
share the same definition gap, and the same caveat
applies to both: a machine checks the steps, not
whether the file states the paper's claim. Until the
definition checks above are done for at least one
formalization, the parallel claim adds a second
unverified formalization, not a verification.

## What would change the status of either claim

In order, from weakest to strongest:

1. A published axiom audit (standard axioms only,
   no placeholders) for the relevant Lean files.
2. An independent expert reading, in writing, that
   the Lean statement matches the original conjecture
   — for local smoothing, Sogge's statement; for ETH,
   the standard 3-SAT statement — with any weakenings
   named explicitly.
3. A shepherd-group verdict that the implications
   claimed in prose (to Kakeya and Stein restriction;
   from counting to ETH's negation) are inside the
   checked code.
4. An explanatory write-up by the shepherds that
   mathematicians and complexity theorists outside
   either lab can follow and reproduce the key steps
   from.

Until at least items 1 and 2 are on the record for a
claim, this document's position stands: **no verdict**,
and Lean step-checking must not be presented as proof
that the formal code captures the original conjecture.

## Sources used (secondary reports, not the Lean code)

- Dealroom, "OpenAI says its AI disproved a core
  computer-science assumption" — https://dealroom.co/news/167089-openai-says-its-ai-disproved-a-core-computer-science-assumption-gives-5m/
- Glonce, "OpenAI says its models refuted the ETH and
  proved local smoothing" — https://glonce.com/openai-says-its-models-refuted-the-eth-and/
- Unite.AI, "OpenAI Says Its Models Produced Three
  Proofs in Math, CS, and Physics" — https://www.unite.ai/openai-says-its-models-produced-three-proofs-in-math-cs-and-physics/
- AI/TLDR, "OpenAI says its model refuted the
  Exponential Time Hypothesis" — https://ai-tldr.dev/releases/openai-eth-false-kakeya-results/
- WebProNews, "Two AI Labs Claim the Exponential Time
  Hypothesis Is False" — https://www.webpronews.com/openai-anthropic-exponential-time-hypothesis-refuted-sat/
- TokenPost, "OpenAI Says Its AI Models Proved the
  Local Smoothing Conjecture in All Dimensions" — https://www.tokenpost.com/news/technology/41755
- OpenAI's public repository, as named in secondary
  reporting: https://github.com/openai/math

Limitation stated plainly: the Lean files themselves
were not read line by line for this document, and no
independent verification verdict exists yet in the
sources above. If the shepherd groups publish one,
this document should be updated — not by changing
its no-verdict stance retroactively, but by recording
the new evidence and what it actually covers.
