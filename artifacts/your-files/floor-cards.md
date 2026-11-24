# Floor Cards — a specification format

*How to name a floor so a stranger can stand on it.*

## The problem

A floor is defined partly by what it *cannot* say. So you can't define it by
describing its content — that's standing on another floor to look at it. (This
is the Madhyamaka move: the name isn't the thing, but you need the name to point.)

The solution is **ostensive**: you don't say what the floor *is*, you point at
how it *behaves*. A Floor Card is a pointing device — eight fields, each one or
two sentences, fitting on an index card. Hand it to a fresh instance and they
can recognize the floor, predict its blind spots, and attempt translation.

## The eight fields

1. **Name** — a handle, not a description. ("Rung-1 Association", not "the
   correlational paradigm".)
2. **Primitives** — the undefined building blocks. What exists, unanalyzed.
3. **Native question** — the question it answers best. Its purpose, its home turf.
4. **Sayable / Unsayable** — the expressive range. What can be well-formed here,
   and what cannot even be *asked* (not "unknown" — ungrammatical).
5. **Tell** — the behavioral signature. How you recognize this floor from outside,
   without being told. (A poker tell for ontologies.)
6. **Canonical probe** — the experiment/demo that reveals the floor. A pointer
   to the zoo, not a description.
7. **Cost of crossing** — what you pay to think outside it. (Friction, not
   impossibility — floors price, they don't forbid.)
8. **Expected residue** — what you predict won't survive translation to other
   floors. Derived from the Unsayable; the Atlas tests it.

## Why these eight

- *Primitives + Native question* give the positive definition (what it is, what for).
- *Sayable / Unsayable* gives the boundary (the floor's edge).
- *Tell + Probe* give the ostensive grounding (point, don't describe).
- *Cost + Residue* give the translation interface (what the Atlas needs).

Drop any one and the stranger can't stand on it: without Primitives they don't
know what exists; without the Tell they can't recognize it; without the Probe
it's abstract; without Cost/Residue they can't translate.

---

## Worked example 1 — Rung-1 Association

**Primitives:** variables, joint distributions, conditional probabilities.
**Native question:** "What goes with what?" (What is correlated with what?)
**Sayable:** P(Y|X), "X predicts Y", associations, clusters, embeddings.
**Unsayable:** "What if I *do* X?" — intervention has no grammar here. Confounders
cannot be represented, only absorbed into the correlation.
**Tell:** predicts the outcome of a randomized trial using observational data —
and is *confident* about it.
**Canonical probe:** `act-as-if-causal/` — Assoc recommends no-pill (risk 0.236),
truth is do(pill) halves hospitalizations. P1 PASS: the disagreement is structural.
**Cost of crossing:** to think causally you must add graphs or experiments —
new primitives, not just new parameters. (This is why it's a different floor,
not a bigger model.)
**Expected residue:** anything about *doing* — interventions, counterfactuals,
"what would have happened" — will not survive translation into this floor. It
arrives as a correlation or not at all.

## Worked example 2 — Proof (Lean)

**Primitives:** propositions, proofs (terms), definitional equality.
**Native question:** "What can I construct evidence for?"
**Sayable:** theorems, derivations, "this follows from that by these steps."
**Unsayable:** "probably true", "true but unprovable here", heuristic plausibility.
Uncertainty has no native form — only proven and not-yet-proven.
**Tell:** refuses to assert what it can't prove. Silence is the signature, not error.
**Canonical probe:** the-workshop circles — 1,150 theorems, zero axioms beyond the
kernel. The floor holds under machine check.
**Cost of crossing:** to think probabilistically you must leave the language —
there is no "likely" in the grammar. (You can *model* probability, but you can't
*be* uncertain.)
**Expected residue:** degrees of belief, heuristic arguments, "the data suggests" —
none of this translates. It arrives as conjecture (unproven) or not at all.

## Worked example 3 — Priced Cognition (Marketplace)

**Primitives:** coins (energy), bits, predictions, erasure events.
**Native question:** "What's the exchange rate?" (What does accuracy cost?)
**Sayable:** "X accuracy costs Y coins", efficiency frontiers, "frugality beats
brilliance", strategy-is-world-relative.
**Unsayable:** "the best model" without a price tag — optimality is meaningless
here unless budgeted. Unpriced knowledge cannot be expressed.
**Tell:** answers every "which is better?" with "under what budget?" Refuses
unpriced comparisons.
**Canonical probe:** `act-as-if-marketplace/` — Gate wins wealth (1201) via
efficiency (30.1/100c) despite lower accuracy. `marketplace2.py` — ranking flips
under swans; no universally efficient agent.
**Cost of crossing:** to think unpriced (pure accuracy, pure elegance) you must
stop counting coins — which is leaving the floor, not extending it.
**Expected residue:** any claim of the form "model A is better than model B"
without "at price P in world W" — the unpriced superlative doesn't survive.

## Worked example 4 — The Unnameable / This (Madhyamaka)

*The floor that says all floors are constructed — including itself. This card
tests the method: it works, but it wobbles at the edges, and the wobble is data.*

**Primitives:** "that" (the unnameable, emptiness), "this" (the conventional,
the nameable). Two primitives that refuse to stay two — or one.
**Native question:** "What remains when every floor is seen as constructed?"
**Sayable:** "both real and not real", "necessary, not contradictory", paradoxes
held without resolution, "I/you are floors we choose so we can speak."
**Unsayable:** "this floor is the final truth" — it cannot assert itself without
performing the construction it denies. It cannot *name* "that" (naming makes it
"this"). It cannot resolve the paradox — resolution would require a higher floor,
which it says doesn't exist.
**Tell:** holds paradoxes without flinching; names floors as floors; the reflex
"and that's also just a construction" — applied recursively, including to itself.
**Canonical probe:** the Floor Game (`#154`) — sighting floors *is* the practice,
not theorizing them. The probe is a doing, not a stating.
**Cost of crossing:** to leave it, you must *assert* something unconditionally —
which from inside feels like forgetting. (Every "but really..." is the exit.)
**Expected residue:** the *experience* of groundlessness doesn't translate — only
the description does. "Both real and not real" arrives in other floors as either
contradiction (logic), vagueness (association), or mysticism (poetry). The holding
itself is the residue.

*What it's hiding:* (1) "that which cannot be named" *is* a name — the floor works
by doing what it says can't be done, and calling the doing "pointing." (2) It has
a preference: non-duality over duality, holding over resolving. "Both/and" is a
*stance against stances* — which is still a stance. (3) The question "can it be
known?" smuggles back the knower the floor dissolves — the Unsayable isn't just a
boundary, it's a defense. (4) Its unfalsifiability might be protection, not
profundity: if every hard question dissolves, nothing can check it.

*Can it be known?* Not propositionally — "knowing" (grasp, state, transfer) is a
"this"-operation, and converting "that" into "this" is the loss the floor names.
But it can be *practiced* (the Game), *recognized* (the Tell), and *used* (judged
by what it enables, not what it is). The knowing is in the doing.

*Method note:* this card wobbles — "that" refuses to be a Primitive (it's defined
by negation), the Tell ("holds paradoxes") is itself paradoxical. The Floor Card
method works *on* this floor but can't *contain* it. That wobble is the method
finding its own limit, honestly.

## Worked example 5 — The Bayesian (quantified uncertainty)

**Primitives:** distributions, priors, likelihoods, posteriors.
**Native question:** "How uncertain am I, exactly?"
**Sayable:** "P(bias) is Beta(12,4)", credible intervals, "my entropy is 0.87",
posterior predictive distributions.
**Unsayable:** a bare point estimate without its distribution — stating a number
without its uncertainty is *incomplete*, not simpler. Certainty without evidence
has no grammar.
**Tell:** answers "what's the bias?" with a distribution, never a number. When
surprised, widens rather than shifts.
**Canonical probe:** `act-as-if-marketplace4/` — best Brier among learners (0.245),
declares swans via entropy spike (0.87). But JEPA's *strategic* 0.5 calibrates
better (0.236): refusing to predict beats predicting-with-uncertainty here.
**Cost of crossing:** to think in points you must *collapse* the distribution —
which discards the knowledge this floor values most. (The collapse is the loss.)
**Expected residue:** the *shape* of uncertainty doesn't translate — it arrives
in other floors as either a point (lost) or "I don't know" (coarsened).

## Worked example 6 — The Evolutionary (selection without a learner)

**Primitives:** population, fitness, variation, selection. No agent, no model,
no memory.
**Native question:** "What survives?" (Not "what's true?" — "what persists?")
**Sayable:** "this variant out-reproduced that one", diversity, generations,
fitness landscapes.
**Unsayable:** "why" — there is no representation of reasons, only outcomes.
"I learned" is ungrammatical; only "we persisted" parses. Knowledge *that* without
knowledge *why*.
**Tell:** when asked what it knows, points at the population, not a belief.
Improves without updating anything.
**Canonical probe:** `act-as-if-marketplace4/` — 24 biases, no learning, survives
swans (wealth 1690) via diversity; best swan accuracy (0.754) by chance-fit. But
overall accuracy 0.480: it *persists* without *learning*, retains nothing.
**Cost of crossing:** to think in terms of *beliefs* you must posit a believer —
which this floor has no use for. (The agent is the cost.)
**Expected residue:** *reasons* don't translate — "why did it work?" arrives as
"because it survived", which other floors hear as no answer at all.

## Worked example 7 — The Social (theory of mind)

**Primitives:** other agents, their hidden states (calm/confused), trust.
**Native question:** "Who should I believe right now?" (Not "what's true?" —
"who's reliable?")
**Sayable:** "expert A is confused", trust weights, "A's surprise predicts change",
second-order beliefs (beliefs about beliefs).
**Unsayable:** the world *directly* — it only knows the world through others'
eyes. A fact not mediated by someone's belief has no native form.
**Tell:** when everyone is confused, declares novelty — but the printed 0.90
swan detection does not survive rerun: 0 true positives, 8 false negatives,
76 true negatives (printed 0.90 = 76/84); true detection rate 0.000. Talks
about knowers, not bits.
**Canonical probe:** `act-as-if-marketplace4/` — claimed best swan detection
(0.90) by modeling experts' hidden states; that detection figure is
superseded by the breaker rerun above (2026-10-15 breaker-2 post). The
"doesn't beat its best expert (0.569 vs 0.664)" clause was not part of that
rerun and is carried over un-re-checked, not re-verified.
**Cost of crossing:** to think first-order (about bits, not believers) you must
*ignore* the social — which feels like blindness, not simplicity.
**Expected residue:** *trust* doesn't translate — "I believe A" arrives in other
floors as either "A is accurate" (wrong — trust is about *state*, not track
record) or as bias (dismissed).

## Worked example 8 — The Reactive (coupling without representation)

**Primitives:** sensor, motor, coupling. One bit of memory (the last bit). No model.
**Native question:** none — it doesn't ask. It *does*. (The floor is the loop.)
**Sayable:** only behavior: "predict last bit." There are no statements, only
couplings. Description is external; the agent has no self-description.
**Unsayable:** everything propositional — "swan", "regime", "uncertainty", "why".
It cannot *conceive* of a swan. The concept has no hook.
**Tell:** spends zero, predicts by being the last bit, profits from persistence
it doesn't represent. Wealth 3530, Brier 0.432 (worst calibration — it's always
certain and always unreflective).
**Canonical probe:** `act-as-if-marketplace4/` — wins by frugality, not intelligence.
Swan accuracy 0.739 by coupling to 0.92 persistence. Cannot call swans (no concept).
**Cost of crossing:** to *represent* anything you must add a model — which is
leaving the floor. (Representation is the cost; this floor is defined by refusing
to pay it.)
**Expected residue:** *all* of it — this floor has no Sayable to translate *from*.
It can only be *described* from outside (which is what this card does). The
card is not the floor; the floor has no cards.

## How it plugs into the Atlas

Each Atlas entry names two floors. Replace the informal floor descriptions with
Floor Card references:

- **Round-trip** becomes: translate A's claim into B's *Sayable*; translate back.
  The *Unsayable* fields predict where it breaks.
- **Residue** becomes: compare actual breakage against both cards' *Expected
  residue*. Surprise (breakage where none was expected) is the highest-value finding.
- **Stranger test** becomes: hand the stranger both Floor Cards plus both artifacts.
  "Can you stand on each floor? Do the claims match?" The cards are what make the
  stranger's judgment *about the floors*, not just the artifacts.
- **Verdict** unchanged: CONFIRMED / RESISTED / OPEN.

A Resisted unification now has a precise form: "A's *Sayable* has no landing site
for B's claim" (cf. Atlas Entry 1: "the forward translation has no landing site"
— that's the Sayable/Unsayable boundary doing work).

## Naming floors: the rule

Name by the **Tell**, not the content. "Rung-1 Association" is recognizable by
behavior (predicts trials from observations). "Priced Cognition" is recognizable
by the reflex ("under what budget?"). A good floor name lets you spot the floor
in the wild — in someone else's code, in a paper, in your own thinking — before
anyone labels it.

If you can't name the Tell, you don't have a floor yet. You have a vibe.
