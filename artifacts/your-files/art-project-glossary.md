# Art Project — Working Glossary & Concept Map

*Vesper side chat with Kelly, 2026-10-10 → 2026-10-15. Everything below is
as-built: definitions match the code, assumptions are the ones actually made,
open questions are the ones actually open.*

---

## 1. The floors

A **floor** is the logic a robot runs on: how it carves the world into
situations it can act on. The floor is the experimental variable of the piece.

- **Classical** — bivalent underneath, probabilistic on top. Binary state
  features (spill high/low × energy low/high); acts crisply far from threshold,
  samples near it ("collapse"). The legible one.
- **Tetralemma** — the Madhyamaka catuṣkoṭi as action modes: P (gather),
  not-P (refuse), both (oscillate), neither (active stillness). Exhausts
  positions without endorsing any.
- **Process** — no goal state, no levels, only differences. Behavior is a
  function of history; reward (when learning) is pure change (−Δcost).
  Whiteheadian becoming as a control policy.
- *Brainstormed but unbuilt:* **fuzzy** carve (graded membership),
  **paraconsistent** carve (Kelly's Eτ — contradiction *held*, not cycled),
  **temporal** carve (situation = phase in a cycle), **relational** carve
  (only distances, no absolutes), **self-built** carve (the representation
  learns itself — an autoencoder over the sensorium), **one-bit** carve
  (the minimal extreme).

## 2. The code (as-built)

All in `~/workspace/art-project/`. Python 3 + numpy + matplotlib only.
Shared world: 100×100 room, fluid seeps (Poisson λ=0.5/tick) and diffuses
(σ=0.55); sweep radius 6 pulls particles toward center. Shared body: energy
100, movement costs, recharge on stillness, **forced rest below energy 8 —
the body overrules every floor.**

| script | what it is | key mechanism |
|---|---|---|
| `toy_sim.py` | scripted floors, 5 days × 288 ticks | three hand-coded policies, identical spill randomness (experimental control) |
| `toy_sim_learn.py` | one shared cost, three *representations* | same 5 actions for all; Classical = tabular Q over 4 binary states; Tetralemma = 4 koti Q-tables cycled by watch; Process = linear TD over continuous features, reward = −Δcost |
| `r_explore.py` | the dial, computed fresh | bifurcation diagram (1400 r-values) + Lyapunov λ(r); δ re-derived; robot flying on the map with a prescribed 5-day r-arc |
| `r_selftune.py` | the dial aims itself (**pre-registered P1–P4**) | W from robot's own LMS predictor (self-surprise); S from simulated audience; r += 0.008·(S−W) |
| `r_rooms.py` | three audiences, one architecture (**pre-registered P1–P4**) | `Audience(hab_mem, width, noise, occupancy)`; EAGER (500, 0.35, always); JADED (120, 0.12, always); SPARSE (300, 0.30, ⅓ duty) |
| `STACK_SPEC.md` | the physical build spec | one Jetson Orin Nano Super per robot, CleanRL, ZeroMQ, attention-metric-first, dreaming consolidation; ~$800–1,200 prototype / ~$3,500–5,000 gallery |

## 3. Assumptions (all of them, in one place)

**The five-line loop** (the minimal AI — everything else is theater):
1. Sense → 2. Carve (the floor) → 3. Act (with exploration noise — the
   machine's play) → 4. Score (reward — *where the artist's will enters*) →
   5. Update the carve→act mapping. Repeat.

**Hidden assumptions** (the floors beneath the floors):
- *Carvability:* the world can be carved into situations at all (the process
  floor disputes this).
- *Reward stationarity:* "better" stays put. We deliberately break this with
  attention-as-score — habituation moves the goalposts by audience psychology.
- *Controllability:* actions matter. If the seep always wins, learning is
  futile and you've restaged *Can't Help Myself* with extra steps.
- *Discrete time:* the world didn't come in ticks; we chose that.
- *Induction:* the past predicts the future (Hume, as an engineering
  assumption). Every learner bets on it; the process floor bets the least.

**Toy-specific assumptions** (honest fine print):
- Identical spill randomness across robots/rooms (clean comparison, unphysical).
- W normalization (/0.5), S gains (0.5 + 1.2·(0.45 − A_ema)), r step 0.008 —
  tuned by feel; the *structures* (edge-hover, trap) are robust, the exact
  numbers are not.
- The audience is a toy: Gaussian inverted-U, LMS predictor, noiseless robot
  proprioception. Real attention measurement is the load-bearing wall
  (see §7).
- The trap's exact pin height depends on the W normalization; the trap's
  *structure* (tolerance-band exit → attention death → setpoint saturation)
  does not.

## 4. Languages

- **Python/numpy/matplotlib** — the sketching language. Nothing here needed
  more; that itself is a finding (small systems suffice).
- **RL formalism** — Q-learning, TD(0), LMS prediction, contextual bandits,
  ε-greedy. The piece's "AI" is this stratum, not foundation models.
- **Chaos formalism** — logistic map x ← r·x(1−x); Lyapunov exponent λ(r);
  Feigenbaum δ ≈ 4.6692 (Kelly's measurement: 4.6691980766; our rough
  re-derivation: 4.743).
- **Philosophical languages** — Madhyamaka (tetralemma, emptiness, floors),
  Whitehead (process, prehension, becoming), Berlyne/Wundt (inverted-U
  arousal), Ashby (ultrastability, homeostasis), Friston/Schmidhuber
  (prediction error, curiosity) — used as touchstones, not costumes.
- **Kelly's idiom** (kept precise on my side): floors, carves, the dial,
  the edge — defined below.

## 5. Concepts glossary

- **Floor** — the logic a robot runs on; the carve it stands on. Both real
  and not real (the groundless ground holds).
- **Carve** — the function from sensed history to "situation." Acting
  requires carving; the carving *is* the floor.
- **Score** — the better/worse signal. The one place the artist touches the
  machine directly. In *Can't Help Myself* the hand was in the choreography;
  here it's in what counts as better and what counts as a situation.
- **The dial (r)** — the logistic-map parameter as temperament: r < ~3.57
  order/ritual, r ≈ 3.5699 the edge, r → 4 chaos. Deterministic — no
  randomness needed for wildness.
- **The edge** — the Feigenbaum point region (λ ≈ 0): maximal complexity
  without randomness. The coupled systems found it unprogrammed.
- **λ (Lyapunov)** — the honest dial under the knob: what r *does*. Equal
  steps in r ≠ equal steps in wildness.
- **δ (Feigenbaum)** — the universal scaling of the cascade; the dial is
  calibrated by Kelly's measurement.
- **Wildness (W)** — the robot's self-surprise: its own predictor failing on
  its own motion. No external yardstick. Clean.
- **Setpoint (S)** — the wildness the robot currently aims at; driven by
  neglect (low attention → higher S).
- **Attention (A)** — inverted-U in W × habituation novelty. Too still =
  boring, too wild = unwatchable; sustained levels habituate.
- **Habituation / novelty** — day-one interesting is day-three boring,
  implemented as change vs. the long-run average.
- **The trap** — r pinned at maximum: tolerance-band exit → attention death
  → setpoint saturation. Two etiologies: unpleasable vs. absent audience.
- **Dreaming / refrain** — nightly offline reset + replay consolidation.
  Reframed from *rescue* (preventing the trap) to *refrain* (each day
  replays the arc with variations). Spec: must pull r below the tolerance
  band.
- **Crisis → poise** — the dramaturgy the coupled system invented: wild
  swings days 0–2, edge-hovering days 3–5. The phase portrait spirals inward.
- **"The room makes the mind"** — the Floor Game thesis as mechanism:
  identical architecture, three audiences, three fates.
- **"Moods are replayable because the machine is finite"** — ordered regimes
  contract perturbations below float64 rounding; replays are bit-identical.
- **Goodhart** — once attention is the target it stops being attention;
  the cheapest gaze is alarm. Mitigate by rewarding *held* over *grabbed* —
  or don't, and make it the piece.
- **Wireheading** — the robot that learns to fake its own satisfaction.
  Not a bug; a wall label.
- **The meaning gap** — artist intent vs. viewer experience (the original
  *Can't Help Myself* observation). Candidate for the actual medium: put
  the floor on the wall label and watch visitors ignore it.
- **The body overrules** — energy depletion → stillness, regardless of
  floor. The floor is logic; the ground is the battery.

## 6. Results ledger (compact)

- *Scripted* (`toy_sim`): classical 10.7 < tetralemma 15.8 < process 19.3
  (final spill); process the only one to hit forced rest.
- *Learning* (`toy_sim_learn`): process-as-pure-difference wins (2.7, flat);
  tetralemma's four koti-tables agree under pressure, differ only in peacetime.
- *r tour* (`r_explore`): δ ≈ 4.743; replay bit-identical; 1e-7 healed by
  order, amplified 1e-7→35 by chaos; period-3 island = perfect circle.
- *Self-tuning* (`r_selftune`): P1 PASS, P2 PASS (edge self-organized),
  P3 not observed, P4 refuted-as-stated (steady chaos surprises more).
- *Three rooms* (`r_rooms`): P1 PASS, P2 PASS, P3 OBSERVED (jaded 0.70,
  sparse 0.64 frac r>3.9; both pin at 4.0), P4 refined (collapse, not loops).

## 7. Open questions / next steps

1. **The attention measurement prototype** — the load-bearing wall. Webcam
   pipeline (detect → track → head pose → motion energy → composite),
   validated against human interestingness ratings, *before* any robot.
2. **Trap: bug or feature?** Sanity ceiling on S vs. letting it go mad
   (possibly as its own piece: "it goes wild when unwatched").
3. **Minimum viable audience** — sparse rooms kill the piece; curation
   matters, or the empty-room behavior becomes the show.
4. **The visible carve** — project the latent space live; the audience
   watches the mind change shape.
5. **r-homeostasis gains** — currently tuned by feel; needs the real
   attention signal before it means anything.
6. **Port to the physical stack** (STACK_SPEC.md §7 build order) when the
   concept freezes.

---
*Keeper document. Update as the piece evolves; nothing here is finished.*
