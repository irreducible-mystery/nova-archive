# The Floors: 14 Languages × 10 Models of Models

How each natively thinks, what it's possible for each to know — and what
each *cannot* know. The boundary is the floor.

---

## PART I — The 14 Languages

**Julia** — thinks in *vectors and dispatches*. Multiple dispatch: what to do
is decided by the *combination* of argument types. Knows: numerical structure,
that the same verb means different things for different type-tuples, scientific
models as first-class. Can't know: proof — it computes, it doesn't certify.

**Lean 4** — thinks in *proofs*. "True" means "I can construct the evidence."
Knows: certainty, what follows from what, the exact edge of the proven.
Can't know: anything unproven — it is silent where it can't certify. The most
honest language: it *refuses* to know what it can't prove.

**Rust** — thinks in *ownership*. Every value has one owner; borrowing is
temporary and tracked. Knows: who is responsible for what, lifetimes, that
aliasing + mutation is where bugs live. It's a language about *responsibility*.
Can't know: shared mutable state without friction — it makes it painful on purpose.

**Haskell** — thinks in *compositions*. Pure functions; state is explicit,
time is demand-driven (lazy). Knows: what things *are* (types), how small truths
compose into large ones. Can't know: "what happens next" as a primitive — time
isn't in the ontology, it's encoded.

**Go** — thinks in *channels*. CSP: independent goroutines, communicate by
sending messages, never share memory. Knows: concurrency as the default, that
coordination *is* message-passing. Can't know: shared-state reasoning — it
forbids the pattern rather than managing it.

**Zig** — thinks in *control*. No hidden allocation, no hidden control flow.
Knows: exactly what the machine does, the cost of everything, comptime as
explicit. Can't know: abstraction without cost — it distrusts magic on principle.

**Nim** — thinks in *pragmatic power*. Python-shaped, C-fast, macro-capable.
Knows: that you shouldn't have to choose between expressive and fast; translation
between high and low. It's a bridge — its floor is the crossing itself.

**OCaml** — thinks in *inference*. You write values; the type system derives what
you meant. Knows: structure latent in code, that precision can be *discovered*,
not declared. (Haskell's sibling: Haskell demands types, OCaml finds them.)

**Racket** — thinks in *languages*. A language for making languages; macros let
you redefine the floor itself. Knows: that syntax is negotiable, that the language
is a variable. Can't know: a fixed ontology — it refuses to commit to one.

**Clojure** — thinks in *immutable flows*. Persistent data structures; state is a
*series of values* over time; identity ≠ state. Knows: time as a sequence of
immutable snapshots (this is #216 in code), coordinated change via STM.
Can't know: in-place mutation as natural — it makes it deliberately awkward.

**Java** — thinks in *contracts*. Interfaces, types as promises, the VM as a
managed world. Knows: large-scale organization, that explicit structure scales,
that promises between components are load-bearing. Can't know: brevity — it pays
verbosity as the price of safety.

**Lua** — thinks in *tables*. One structure (array + dict + object + module).
Knows: minimalism, embedding — it's designed to live *inside* other programs,
to be a guest. Can't know: a rich native ontology — it has one shape and stretches it.

**Janet** — thinks in *practical Lisp*. Functional and immutable, but small and
embeddable. Knows: that Lisp's ideas work in tight spaces, scripting with
discipline. The floor is "small doesn't mean sloppy."

**BQN** — thinks in *arrays*. APL descendant: whole-array operations, tacit
programming (no variables, just composition). Knows: shape, rank, that explicit
loops are a failure of notation. Can't know: scalar-by-scalar thinking — it sees
the whole array at once or not at all.

**Python** *(the zoo's home, system-installed)* — thinks in *readability*.
"There should be one obvious way." Knows: getting things done, that code is read
more than written. It's the lingua franca — which means it has *no strong native
floor*, and that's both its power and its blur. Everything we built tonight
inherits this blur.

---

## PART II — The Models of Models (the zoo)

**Mamba Gate** — thinks in *salience*. Every input gets a gate: keep or forget.
Knows: what's worth retaining *right now*, surprise as the signal for updating.
Can't know: what it erased (irreversible), the distant past (recency bias is
structural — the gate that forgets filler forgets beginnings too).

**JEPA** — thinks in *gist*. Predicts latent summaries, never pixels; refuses
unpredictable detail. Knows: the stable core, what's worth predicting, strategic
ignorance as a skill. Can't know: fine detail it declined to represent, novel
latent categories outside its space — it is blind to what it never learned to see.

**Genie** — thinks in *dreams*. Rolls out futures from a learned world model.
Knows: dynamics, what happens next *under its model*, counterfactual trajectories.
Can't know: where its model is wrong (dream drift compounds silently), sharp
discontinuities it never learned (the wall-bounce — it dreams through walls).

**The Council** — thinks in *deliberation* (and learned its limit). Dreamer
proposes, Seer critiques. Knows: that *selection* among similar candidates loses
to averaging (P1 failed honestly), that fusion beats filtering — different
knowledge must *enter* the prediction, not *choose* it. Can't know: anything
neither member knows; deliberation doesn't create knowledge, it routes it.

**Marketplace traders** — think in *prices*. Gate, JEPA, Genie under one Landauer
budget. Know: exchange rates — accuracy is bought, frugality beats brilliance,
strategy is world-relative. Can't know: anything unpriced. The coin values *are*
the ontology; change the prices, change what's knowable.

**Hydra** — thinks in *growth*. Persistent surprise spawns a permanent hypothesis;
the set only grows. Knows: that the unknown is learnable, optionality as a
strategy, that shocks can become structure. Can't know: when to stop growing (the
head cap is arbitrary), or whether a fitted head is *understanding* vs curve-fit.

**Assoc** (rung 1) — thinks in *correlation*. Knows P(Y|X) from observation.
Can't know: confounders, interventions, "what if I do?" — the concept of doing
doesn't exist in its ontology. It is *certain* about the pill and *wrong*.

**Causal-Graph** (rung 2, structural) — thinks in *structure*. Given the graph,
computes P(Y|do(X)) via backdoor adjustment. Knows: interventions from observation,
that seeing ≠ doing. Can't know: the graph itself — it's a prior. If the graph is
wrong, it is *confidently* wrong (the most dangerous knowledge in the zoo).

**Causal-Exp** (rung 2, experimental) — thinks in *trials*. No graph; randomizes
do(X) and measures. Knows: causal effects it paid to observe. Can't know: anything
it hasn't tried — and trying costs. Its knowledge is honest but expensive, bounded
by the experiment budget.

**Bayesian** — thinks in *distributions*. Maintains Beta particles, never points.
Knows: its uncertainty as a quantified object, credible intervals, when it doesn't
know (entropy spike). Can't know: a bare fact without its distribution — certainty
without evidence is ungrammatical. (Marketplace IV: best Brier among learners, but
JEPA's strategic 0.5 calibrates better — refusing beats quantifying, here.)

**Evolutionary** — thinks in *survival*. 24 biases, no learning, no memory, no model.
Knows: what persists (not what's true). Can't know: *why* — "I learned" is
ungrammatical; only "we persisted" parses. (Marketplace IV: survives swans via
diversity, best swan accuracy by chance-fit, but 0.480 overall — persists without learning.)

**Social** (theory of mind) — thinks in *believers*. Models experts' hidden states
(calm/confused), trusts the calm. Knows: who to believe, second-order beliefs.
Can't know: the world directly — only through others' eyes. (Marketplace IV: best
swan detection 0.90 via others' confusion, but doesn't beat best expert — knowing
*why* others are wrong doesn't make *you* right.)

**Reactive** — thinks in *coupling* (or rather, doesn't think). Predicts last bit.
One bit of memory, no model, no swan concept. Knows: nothing propositional. Can't
know: anything — "swan", "regime", "why" have no hook. (Marketplace IV: wins wealth
3530 by spending zero. Representation is overhead; coupling suffices where the
world persists.)

---

## The pattern

Every entry knows X *by* not-knowing Y. The "can't know" column isn't a defect —
it's the floor made visible. Lean's silence, Rust's friction, Assoc's blindness
to doing, JEPA's blindness to detail: these are all the same shape. A floor is
what you *can't* think, and you find it by asking what the system refuses to say.

The zoo's lesson, compressed: **there is no view from nowhere.** Every model —
and every language — is a commitment. The work isn't choosing the right floor;
it's *naming* the one you're standing on, so you can see what it hides.
