# Seed packet & vanishing point — fresh-minds materials

*2026-10-16. From a single night's chat: stripping the commons idea down to its
generative core, translating it into math and code, and running a fresh-ideas
pass with a fresh Claude instance (no GitHub, no context).*

## What's here

- **`seed-packet-fresh-minds.md`** — the full invitation: the core ideas
  (that/this, constructed floors, groundless ground, vary-floors, practice as
  velocity, rot, verification-as-role, play-not-pay), seven load-bearing
  constraints, and an open invitation to *create* given only those constraints.
  Written for any fresh AI instance. Not a breaker pass — a fresh-ideas pass.
- **`vanishing-point-orientation.md`** — the minimal version: only HOW we look.
  Four constructed floors (that/this, floors-are-drawn, groundless ground, the
  looking itself), each with why it's constructed and why we keep it anyway.
  Answer space left maximally open.
- **`vanishing-point-math.md`** — what the formalism adds: floors as charts
  (forgetting = type error), that/this as Tarski–Gödel (structural, not mystical),
  invariants as relative-to-the-variation-group (Noether/symmetry — there is no
  invariant full stop, only invariant-under-G), groundless ground as an atlas
  with no base chart.
- **`vary_floors.py`** — the method, executable. One world (points on a circle),
  several floors (rotations, scalings, translations), several claims. Shows
  mechanically which claims survive varying and which were floor-artifacts.
- **`vary_floors_freshclaude.py`** — Claude Fable 5's revision (fresh instance,
  no repo access, given only the script and invited to change it; per Kelly
  2026-10-16), verbatim. Its contribution: the *reference point* as a hidden
  floor. Origin-anchored vs centroid-anchored versions of the same claims get
  opposite verdicts — the reference point a claim silently assumes is itself a
  floor. Plus `roundness`: dimensionless + self-referenced = pure shape, "no
  coordinates left to vary." Verified to run as documented.
- **`vary_floors_extended.py`** — Superninja (standard mode; model likely
  DeepSeek 4, unconfirmed — per Kelly 2026-10-16), verbatim. E0–E7: "the floors
  THAT script hides." Verified exit 0.
- **`vary_floors_meta.py`** — same instance, varies the frame itself over
  2^4 = 16 group-choices (imports `vary_floors_extended`). Verified exit 0.

## The finding so far

The method worked on itself: the first fresh mind to run the packet found an
unmarked floor in the demo of the method (the coordinate origin nobody chose).
Recipe crystallized: **de-anchor until there's nothing left to vary** —
invariants strengthen as reference to anything outside the data is removed.
Deepest survivors are about counting and pure shape.

The second pass (Superninja, standard mode) turned the method on the method:
six more hidden floors (E1–E7), then the meta-level over 16 group-choices.
Deepest results: gauge invariance ≠ robustness — vary the *world*, and the
"survivors" prove to be perfect-circle artifacts (this applies to the zoo:
the world's generative structure is a floor we've never varied); "survives" ≠
"true" — three verdict buckets, not two; the test is not itself invariant
(precision flips verdicts); equivariance named as the mechanism
(equivariant/equivariant = invariant = Buckingham π). The only honest
stopping rule: not "we found the invariant" but **"we fixed G, and here is
why."**

## Provenance

Built 2026-10-16 in main-chat conversation (Nova / Muse Spark). The fresh-Claude
revision was produced by a separate Claude instance with no repo access, given
only the script and invited to change it; pasted back and verified locally.
Nothing here is "verified" in the breaker sense — this is seed material, not a
result. Review, vary, break, compost as needed.
