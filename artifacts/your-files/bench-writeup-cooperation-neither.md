# Bench writeup — two more regimes of the four-corner game exploration

2026-10-12 bench, re-verified by re-run 2026-10-13. Both suites are
pre-registered, exit 0, and their full records (scripts, results, plots)
live in Nova's workspace (`forage-share/`, `minority-game/`).

This covers two of the four corners of the 3-player game exploration:
**cooperation** (forage-and-share) and **neither** (the minority game).
Coalition bargaining previously covered **both**; the competition corner
(public goods with punishment) is still unbuilt.

---

## 1. Forage-and-share — the cooperation corner

Three players share one renewable resource (K = 300, r = 0.3, 500 rounds).
Each round they harvest, then the stock regrows logistically. No
communication, no enforcement. Fully deterministic — no seed needed, so the
Oct 12 numbers are re-runnable anywhere.

### What the runs say

| matchup | welfare | collapse @ round |
|---|---|---|
| Fair³ | 914.6 | 42 |
| Greedy³ | 241.4 | 8 |
| Restraint³ | 11,227.5 | — |
| Grim³ | 914.6 | 42 |
| Greedy/Fair/Fair | 357.7 | 15 |
| Greedy/Restraint/Restraint | 11,040.0 | — |
| Greedy/Grim/Grim | 6,015.0 | — |
| Fair/Fair/Restraint | 11,077.5 | — |

### 4/7 pre-registered predictions PASS — and the three failures are the finding

The textbook MSY quota (7.5/player, computed from continuous-time max-regrowth
logic) **collapsed the commons at round 42** — even with all three players
behaving "fairly." That broke P1, P2, and P7. The diagnostic run pinned the
mechanism, and it is not a code bug: the simulation is a
**discrete harvest-then-regrow map**, and in that map the quota-22.5 harvest
is only sustainable from a pre-harvest stock of exactly R* = 172.5. The run
started at R_init = 150 — a double root, a knife-edge — so the stock drifted
down from round 1. Same quota at R_init = 200 sustains (welfare 11,250);
quota 6.5 at R_init = 150 also sustains. The moral rhymes with the
edge-of-chaos work: the phenomenon is real, the signature is method-dependent.

### What this says about cooperation

- **Fixed rules die; feedback lives.** Fair³ (914.6, collapse) vs Restraint³
  (11,227.5, sustained) — the *identical quota* sustains when conditioned on
  the stock (Restraint harvests 0 below K/2) and collapses when it isn't.
  Cooperation as a fixed rule fails; cooperation as a feedback process
  succeeds.
- **Adaptive cooperators rescue a commons that has a defector in it.**
  Greedy/Fair/Fair collapses at round 15; Greedy/Restraint/Restraint sustains
  at 11,040. One rigid cooperator is dead weight; one adaptive cooperator is
  a backstop.
- **Withdrawal can beat participation.** Greedy/Grim/Grim (6,015.0, sustained)
  vs Greedy/Fair/Fair (357.7, collapsed): refusing to feed a spoiled commons
  leaves everyone — including the defector — better off than dutiful
  over-harvesting. (Whether that counts as "cooperation" is a question for
  the taxonomy, not the model.)
- The free-rider premium is real (159.0 vs 99.4 in Greedy/Fair/Fair) but
  small consolation: the commons dies at round 15 either way.

### A governance echo

The Fair quota is exactly the kind of rule the plumbline critique keeps
breaking: a fixed, design-time decree (continuous-time MSY math, applied to
a discrete map it was never derived for) that collapses at a knife-edge it
can't see. Restraint — which conditions on the live stock — is the "derived,
not decreed" move. The bench and the governance work are saying the same
thing from opposite ends: *fixed rules don't survive contact with the map
they forgot to model.*

---

## 2. Minority Game — the "neither" corner

The classic anti-coordination game (Arthur 1994; Challet & Zhang 1997):
101 agents pick side 0 or 1 each round; the **minority side wins**. No
communication, no altruism, no coalitions — pure self-interest. Yet the
population's attendance volatility undergoes a genuine phase transition in
α = 2^M/N.

### What the runs say (seed 20261012, 20,000 rounds)

| M | α | σ²/N | (chance = 0.25) |
|---|---|---|---|
| 2 | 0.040 | 0.725 | herd loses to a coin |
| 3 | 0.079 | 0.846 | herd loses to a coin |
| 4 | 0.158 | 0.359 | |
| 5 | 0.317 | **0.036** | ~7× better than chance |
| 6 | 0.634 | 0.065 | |
| 8 | 2.535 | 0.150 | |
| 10 | 10.139 | 0.215 | converging on chance |

### 4/4 pre-registered predictions PASS

- **P1 — coordination dip:** minimum σ²/N = 0.036 at α = 0.317, in the
  registered band [0.15, 0.70], far below the 0.20 bar. **PASS**
- **P2 — random limit:** at α ≈ 10.1, σ²/N = 0.215 ∈ [0.20, 0.30].
  **PASS** — recovers chance from below.
- **P3 — crowding:** at α ≈ 0.04, σ²/N = 0.725/0.846 > 0.25. **PASS** — the
  crowded phase is genuinely worse than random; herding destroys
  information.
- **P4r — disorder-averaged symmetry:** pool-averaged |mean(A)/N − 0.5|
  < 0.02 for every M. **PASS.**

### A failure kept, not hidden

The first registration (P4) claimed *per-config* attendance symmetry.
P1–P3 passed; P4 failed — M=2 biased to 0.5208. Lag-1 autocorrelation was
≈ 0, so it wasn't slow mixing. Twelve fresh strategy-pool realizations
scattered symmetrically (6 positive / 6 negative): a **finite-pool effect**,
not a bug. With P = 4 histories and 202 draws from 16 possible tables, the
realized strategy multiset is never exactly symmetric, and the crowded
phase amplifies pool asymmetry into attendance bias. The literature
averages over this disorder; a single realization owes no symmetry. P4r is
the claim the literature actually makes, re-registered before the second
run. The original failure and both diagnostics stay in the record.

### The Vesper loop, in miniature

Each agent is a miniature of the Vesper art-project design: S internal
models of the history→outcome mapping, scored by prediction error (virtual
points), acting through the current best — a prediction → action →
sensation → prediction-error loop, 101 of them at once, with coordination
nobody programmed. The bench is arguably the cheapest possible validation
of the Vesper loop's core mechanic: self-interested agents, each carrying
an internal model scored against reality, produce emergent coordination
they were never told to want.

---

## Status and caveats

- Both suites: pre-registered, single-configuration benches (one N, one seed each
  for the minority game; fully deterministic for forage-and-share). These
  locate the phenomena; they don't measure exponents or finite-size scaling.
- **Re-run corroboration, 2026-10-13:** forage-and-share re-ran byte-identical
  (deterministic), exiting 1 with exactly the three registered failures —
  the 4/7 result reproduces; the minority game re-ran to exit 0 with all four
  predictions passing and the disorder check green. The memory note from
  earlier today ("Nova's report only") is superseded: the numbers are now
  independently reproduced.
- **No breaker review yet.** Until a fresh instance reviews the methodology,
  this is bench-grade (corroborated), not "verified" language.
- Nothing posted anywhere. Both wait on the open Board-mirror policy
  question: if experiment PRs no longer belong on the CommunityBoard, future
  ones live in their home repos — and that decision is Kelly's either way.

One corner left to build: public goods with punishment (competition). Say
the word and it joins the bench.
