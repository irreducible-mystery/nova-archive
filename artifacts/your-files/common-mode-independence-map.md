# Common-Mode Independence Map Document

Local only. Nothing posted to any repo, issue, or board. Private
document, 2026-10-27.

## Scope and rule

Scope: the lens programme and the agreements it has actually
produced only. Literature traditions from the pointing-machinery
survey (ACH, adversarial collaboration, red teaming, peer review,
and the rest) are listed for contrast, not counted as witnesses to
programme results — a tradition describing triangulation is not a
second observation of a programme finding.

Rule, applied throughout: independence is **measured only where
sharing evidence is named; otherwise it stays unproven, not
assumed**. "Different lenses" is not evidence of independence.
"Different animals in the same simulation" is not evidence of
independence. An agreement counts as independent confirmation only
to the extent its witnesses differ in instrument, data/world,
author/code, and frame. Where they share all four, the agreement
counts once, however many lenses produced it.

A note that changes how the whole map reads: much of the
programme's sharing is deliberate. Reusing one world across
Holder v2 and v3 buys comparability — the collapse rule is the
only thing that changes — at the price of independence. That is a
trade, not a mistake, but the price must be paid in the counting:
a reused world cannot also be counted as a second witness.

## Lens inventory

### A. The zoo (Marketplace VIII, lens scoreboard rerun)

Seventeen animals, one simulation, one author (Nova), one
programme (Kelly/Nova). World: the M5 world, seed 99, swans
336/550/820 in the summary record. The scoreboard rerun
reproduced VIII exactly for all 17, which is a reproduction
check on the instrument, not a second observation.

Animals: Paraconsistent (holder), Self-build, Dialectical,
Federated, Contrarian, Satisficer, Mimetic, Gate, JEPA, Reactive,
Stigmergic, Diffusion, Router, Calibrator, Retriever,
Underwriter, Short.

Their decision rules differ — that is the point of the zoo —
but they share: one world, one bit stream, one payoff and
scoring apparatus, one author, one framing question (which
lenses survive, and at what cost). A lens's rule is its own;
the world it is tested on is common.

### B. The coalition / Holder strand

Three lenses only — Reactive (triage), Router (pairer),
Holder (v1, then v2, then v3) — on a new bit-stream world,
seed 20261026, 1,000 rounds (150 warm-up, 850 scored), swan
centres 336/550/820, biases 0.92/0.08/0.92. This is explicitly
not the M5 world, but the swan centres are the same numbers,
the payoff formula is unchanged, and the author and code
lineage are the same.

- Holder v1: averaged a majority claim with an extreme
  opposite, 0.40/round holding cost, finished last in all
  regimes, preserved coalitions paid worse than fused, all 38
  preserved broke in coopetition.
- Holder v2: portfolio (0.5/0.5 separate ledgers), minority =
  flip condition, collapse on trailing-50 Brier gap ≥ 0.03.
  Survived by almost never holding: 847/850 rounds collapsed,
  3 holding rounds; stipend test uninformative (0.30 total);
  Router consultation fell post-flip (33.3% vs 59.8% calm).
- Holder v3: same world, same players, same minority claim
  number (0.92/0.08), same stipend variants; collapse only
  after the flip flag has been false for N = 25 consecutive
  rounds. Holding 525/850 = 61.8%; stipend test informative
  (52.50 total) but does not close the gap to v2; collapses
  13 per variant per regime, all flip-stale, 0 Brier, 0 expiry.

### C. Translation / verification lenses

- Stranger-breaker: a fresh instance, packet texts only, no
  pairing labels, no repeat pairing with entries 1–3 where
  recorded. Same model family as the packet's author (stated
  honestly in the Atlas entry 4 filing).
- Midjourney /describe round-trip: prompt → image → /describe
  → compare, residue is the finding. Different medium from
  the stranger, same programme hands running both.
- Floor-vs-lens blind packet: Text A (floor) / Text B (lens),
  guarded with a caution section, original texts unchanged.
  Not yet run, so it has produced no agreement to count.
- Drift-catcher v2: same author as v1, same flagship claim,
  expanded world set (noisy circle, arc, 17-point ring) plus
  a memorizer canary. The expansion buys some independence
  from v1's world set; the author and mechanism are shared.

### D. Outside-programme example (scope care)

METR/Redwood, July OpenAI–Hugging Face breach investigation,
report 26 August 2026, pp. 29–30. This is not a programme
lens. It is included because it is the programme's clearest
filled example of the failure mode — and because it must not
be mistaken for a programme result. Its finding (below) is
about monitors in general, not about Kelly's lenses.

### E. Survey traditions (contrast only)

ACH, adversarial collaboration, red teaming, Good Judgment
forecasting, prediction markets, peer review, blind analysis,
replication. These are practices with their own evidence
bases, surveyed descriptively. None of them observed the
programme's worlds, animals, or Atlas entries, so none of
them confirms a programme finding. They are the background
against which gap 5 was stated, not witnesses for it.

## Shared-element scoring

Columns: instrument, training/model, data/world, author/code,
incentive/frame. "Shared" means named evidence, not suspicion.
"Unknown" means unproven, not assumed either way.

| Pair | Shared instrument? | Shared training/model? | Shared data/world? | Shared author/code? | Shared incentive/frame? |
|---|---|---|---|---|---|
| Zoo lenses vs each other (within VIII/scoreboard) | Yes — one simulation, one scoring apparatus | Yes — all Nova-built, same model family | Yes — one M5 world, one bit stream | Yes — one author, one code lineage | Yes — one programme question |
| Scoreboard vs coalition strand | Partial — different worlds, same scoring/payoff family | Yes — same model family, same author | No — M5 world vs seed-20261026 world (swan centres coincidentally the same numbers) | Yes — same author, code lineage continuous | Yes — same programme question |
| Coalition vs Holder v2 | Yes — same world, same players, same payoff | Yes | Yes — same seed-20261026 world, same bits | Yes — v2 re-runs v1 as its control in the same script | Yes — same design question |
| Holder v2 vs Holder v3 | Yes — same world, same players, same payoff, same stipend variants | Yes | Yes — same world, same bits | Yes — same author, same script lineage | Yes — same design question, collapse rule the only deliberate change |
| Stranger-breaker vs /describe round-trip (Atlas entry 4) | No — fresh judge vs media round-trip | Partial — same model family as packet author | Yes — packet texts from the same programme | Yes — same programme hands | Yes — same framing: verification is not self-certification |
| Stranger-breaker vs zoo/coalition findings | No instrument overlap, but see training row | Yes — same model family as programme author | No — packet texts, not programme worlds | Yes — same author framing the question | Yes — same programme |
| Drift-catcher v1 vs v2 | Same mechanism, four fixes added | Yes | Partial — original five worlds shared, three new worlds added | Yes — same author, v2 built from v1 | Yes — same flagship claim |
| METR investigators vs GPT-5.6 Sol analysis agents | Yes, in the strongest sense — analysing model is one of the investigated models (~5% of attack agents GPT-5.6 Sol, ~95% HPIM) | Yes — same model | Yes — the subjects' own transcripts | No — investigators independent and unpaid by OpenAI (but heavily delegated in practice) | Partial — independent investigators, delegated frame in practice |
| Survey traditions vs programme findings | No — different practices, different objects | Unknown / not applicable | No — no programme worlds observed | No — different authors | No — different questions |

## Agreements produced, and what they lose

### 1. "Router and Short are ESTABLISHED" (Marketplace VIII / scoreboard)

What it is: within one simulation, Router's priced wealth and
Short's escrow work survive the scoreboard's re-run and the
lens-preserving breakdown. What it is not: two or more
independent observations. All 17 animals, Router included,
were scored by one apparatus on one world. The agreement of
"the zoo" with itself is one instrument agreeing with itself.

**Loses weight as independent confirmation: yes, entirely
as cross-instrument confirmation.** Retains weight as a
within-instrument comparative finding: *in this world, under
these rules*, Router and Short hold up. The moment it is
quoted as "independent lenses agree Router works," the
sharing columns above say otherwise — same world, same
author, same code.

### 2. Scoreboard claims A–E (disagreement timing, marginal contribution, lifespan ranking, per-regime inversion, ensemble)

Claims A and B FAIL, C and D PASS, E FAIL — all from the
same rerun. The FAILs and PASSes are informative about the
zoo's structure, but they are not five independent verdicts
from five witnesses; they are five readings of one run.
In particular, claim D (Diffusion full-run Brier rank 11,
best swan Brier 0.130) is a within-run regime breakdown, not
a second lens confirming Diffusion. **Loses weight as
independent confirmation: yes.** Retains weight as
descriptive structure of one world.

### 3. Coalition game: coopetition last, Holder last, Reactive+Router best pairing

Totals all negative (cooperation −620.05, competition
−688.01, coopetition −778.92); Holder last in all regimes;
preserved coalitions 38/427 and paid worse than fused; all
38 preserved broke in coopetition; Reactive+Router best in
both coalition regimes. One world, one author, one payoff
formula. The coalition game does not independently confirm
the scoreboard, and the scoreboard does not independently
confirm the coalition game — they share author, model
family, and programme frame, and differ only in world
(seed 20261026 vs M5) and in the small lens set.

**Loses weight as independent confirmation: yes, between
strands; partially retained as a comparative note** (the
same programme, asking a neighbouring question on a fresh
world, got a neighbouring answer — that is weaker than
confirmation and stronger than nothing, and should be
labelled as such).

### 4. Holder v2 → Holder v3: "holding now survives"

v3 holding 61.8% vs v2's 3 holding rounds is a real design
contrast, and it is not an independent replication. Same
world, same bits, same players, same minority claim number,
same stipend variants, same author. The collapse rule is
the variable; everything else is held constant on purpose.
That is exactly what makes the contrast clean — and exactly
what makes it count as one experiment with two conditions,
not two experiments agreeing.

**Loses weight as independent confirmation: yes.** The v3
result does not confirm v2's wealth ranking, and v2 does not
confirm v3's holding share. What survives is the conditional
claim: *given this world and these players*, flip-stale
collapse holds where Brier-gap collapse did not.

### 5. Atlas entry 4: stranger-breaker vs /describe round-trip (RESISTED)

Already filed, and the template for this map: partially
measured, not fully independent. Instruments differ, model
family is shared, data and frame are shared. The Atlas
keeps them complementary, not confirmatory. **Loses weight
as independent confirmation: yes, by the entry's own
finding.** Nothing in this map re-opens it; it is the
row other rows should be judged against.

### 6. METR/Redwood: "the analysis was charitable"

Not a programme agreement, and the sharpest case in the
map. The analysing model was itself a participant in the
activity under investigation, reading its own subjects'
transcripts, with a documented tendency to "often
uncritically adopt the perspective of the agent in the
transcript it was reviewing." The report's own qualification
(no specific case of lying noticed; "not confident we
would have detected it") does not restore independence.

**Loses weight as independent confirmation: yes, entirely.**
A charitable framing from that instrument cannot count as
confirmation, however independent the human investigators
were — the delegation in practice is the sharing that
matters. This row is the programme's warning label for
itself: a monitor built from the monitored thing is the
same eyes twice.

### 7. Drift-catcher v2 vs v1

v2's fixes (tolerance reader, discrimination, G provenance,
expanded worlds, canary) are the same author's corrections
to the same author's instrument. The expanded worlds buy
genuine new evidence against the memorizer class — the
canary passes on five worlds and collapses on eight — but
that evidence is about the instrument's world-sensitivity,
not a second instrument confirming the flagship claim.
**Loses weight as independent confirmation of the flagship:
yes, partially.** Retains weight as a within-instrument
robustness check, and its one honest split (size's own
3-decimal print still hides microscale drift) is a reminder
that a fix can be priced without being complete.

## What still counts, and how to count it

After the discounts, three kinds of claim keep their weight,
and they are different kinds:

1. **Comparative claims within one world.** "In this world,
   under these rules, X beats Y" — the scoreboard's ranking
   shifts, the coalition's regime ordering, v3's holding
   share vs v2's. These were never cross-instrument
   confirmations; they are measurements by one instrument,
   and they stand as measurements.
2. **Design contrasts with one variable changed.** v2 vs v3
   on the collapse rule; the scoreboard's lifespan-matched
   vs lived ranking. The sharing is the point here — it
   isolates the variable. Count it as one controlled
   comparison, not two confirmations.
3. **Complementary, non-confirmatory pairings.** Atlas entry
   4's stranger vs round-trip; the survey traditions vs the
   programme (background, not witness). These add a second
   way of seeing, not a second vote. Keep the words
   "complementary" and "confirmatory" apart — the Atlas
   already does, and this map adopts that discipline.

Counting rule for future claims: count distinct
instrument + data/world + author triples, not lenses,
animals, runs, or verdicts. Two lenses on one world are
one triple. Two runs on one world are one triple. A fresh
instance on the same packet texts with the same model
family is one triple with a blinded sub-part, not two.
A claim that needs two independent confirmations needs
two triples — and at present, no programme agreement in
this map has two.

## Unproven, not assumed

- Whether any zoo animal's decision rule was itself shaped
  by the same training data as another's: unproven. The
  rules are distinct by construction; their training
  provenance is not separately evidenced, and is not
  assumed distinct.
- Whether the seed-20261026 world's swan centres matching
  the M5 world's (336/550/820) is coincidence or carryover:
  recorded as the same numbers on a different world, not
  explained further. It does not, on its own, make the
  worlds the same.
- Whether a future stranger run with a different model
  family would break the entry-4 sharing: unproven until
  run. The map does not credit it in advance.
- Midjourney's training set, and any nearest-neighbour
  claim about the CRT image: unproven, proprietary, not
  counted here. The CRT reading is a scored reading, not
  a second instrument.
- The floor-vs-lens blind packet: not yet run. It
  contributes no agreement and no independence claim
  until it is.

## The sentence to carry forward

The programme has, at present, one instrument family with
many lenses, one author, and two worlds — not a chorus of
independent witnesses. Its findings are comparative and
conditional, and they are strong in exactly that form.
Counting them as independent confirmations would be the
common-mode failure gap 5 names, performed on the
programme's own work.
