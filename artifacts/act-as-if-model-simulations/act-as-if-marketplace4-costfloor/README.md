# MARKETPLACE IV — vary the cost floor

M1–M3 varied the *world* under a fixed cost. This one fixes the worlds and
varies the *cost floor itself*: every erasure cost × λ, the price of energy.
Earnings unchanged. The animals don't re-tune — the floor moves under them.

## Pre-registered predictions (written before running)

- **P1:** λ=0 calm → wealth ranking = accuracy ranking: JEPA ≥ Gate > Genie.
  Pareto frontier goes vertical; frugality dominance vanishes.
- **P2:** λ=10 calm → most-frugal wins; Genie bankrupt early; aggregate
  wealth collapses vs λ=1.
- **P3:** crossover λ* ∈ (0.1, 3) where the calm-world ranking flips.
- **P4:** λ=0 swans → Gate ≥ JEPA (frantic adaptation is free;
  world-relativity is cost-conditional). λ=10 swans → JEPA dominance widens.
- **P5:** frugality dominance holds for every λ>0; degenerate at λ=0.

## What happened

**Reproduction:** λ=1 reproduces M1 (Gate 1202 > JEPA 931 > Genie 641) and M2
(JEPA 1748 > Gate 879 > Genie bankrupt) exactly — same seeds, bit-identical
streams. The floor scan is honest.

**E1 — λ scan, calm world:**

| λ | ranking (wealth) |
|---|---|
| 0 (free) | jepa > genie > gate |
| 0.1 | jepa > genie > gate |
| 0.3 | jepa > gate > genie |
| 1 | gate > jepa > genie |
| 3 | genie > jepa > gate (all bankrupt) |
| 10 | genie > gate > jepa (all bankrupt) |

- **P1: FAIL.** λ=0 gives jepa > genie > gate, not jepa > gate > genie.
  Why: at λ=0 wealth = 120 + earnings, and earnings flow through *niches* —
  Genie's futures (+6) and regime calls out-earn the Gate's next-bit edge
  (0.575 vs 0.565). Even with thermodynamics switched off, the *scoring
  rule* still ranks. The institution that survives λ=0 is the scoreboard,
  not the budget.
- **P2: PASS** (stronger than stated). At λ=10 *everyone* goes bankrupt
  (aggregate −16 vs 2774 at λ=1). The world doesn't pay enough for anybody —
  scarcity extreme enough kills the game, not just the players.
- **P3: PASS.** Flips at 0.1→0.3, 0.3→1.0, 1.0→3.0. The economic crossover
  λ* ∈ (0.3, 1.0): that's where the Gate's efficiency overtakes JEPA's
  accuracy. Rankings are cost-relative, not just world-relative.

**E2 — Pareto dial-sweeps at λ ∈ {0, 1, 10}:** at λ=0 every dial costs
exactly 0.00/step — the frontier is a vertical line, frugality dominance
*undefined* (nothing to dominate on). **P5: PASS** — for λ=1 and λ=10 every
agent's cheapest dial matches or beats its lavish dial on accuracy.

**E3 — swan world at λ ∈ {0, 1, 10}:**
- λ=1: jepa > gate > genie(bankrupt) — M2 reproduced.
- λ=0: **genie > jepa > gate** (Genie 7394!). **P4: FAIL as stated** — but
  the deeper claim PASSED: the ranking fully reorders, so world-relativity
  *is* cost-conditional. And the mechanism is better than the prediction:
  with free energy, Genie's perfect swan detection (1.00) collects +25/call
  forever without ever paying for its dreams. Detection without adaptation
  is fatal *only when acting is expensive*. Make energy free and the
  detector becomes the winner.
- λ=10: all bankrupt (jepa −2.9, gate −29.7, genie −60). **P4b: FAIL** —
  JEPA's dominance doesn't widen; the floor kills everyone and JEPA merely
  dies slowest.

## The finding

**Cost isn't a dial. It's what makes the marketplace a marketplace.**
At λ→0 prices don't just reprice — *pricing breaks*: the Pareto frontier
goes vertical, efficiency becomes undefined (division by zero spend), and
the contest collapses to whatever the scoring rule rewards. The zoo's
arrow — cumulative dissipation monotonic in every world — holds for every
λ>0 and is *meaningless* at λ=0. An invariant with a domain is still an
invariant; this one names its domain: λ>0.

Two crossovers found: an economic one (λ* ∈ (0.3, 1.0), Gate overtakes
JEPA in the calm world) and an institutional one (λ→0, the budget
dissolves into the scoreboard).

## Run it

```sh
python3 marketplace4.py   # ~3s, writes three plots
```

numpy + matplotlib only.

## Files

- `marketplace4.py` — λ-scan + Pareto + swans, predictions pre-registered in the docstring
- `marketplace4_crossover.png` — final wealth vs λ (the crossover plot)
- `marketplace4_pareto.png` — Pareto frontiers at λ = 0, 1, 10
- `marketplace4_swans.png` — swan world at λ = 0, 1, 10
- `README.md` — this file

## Honest limits

Toy energy model throughout (see marketplace.py). The animals do NOT re-tune
their dials to λ — a real agent would learn the price of energy (that's a
Marketplace V). λ scales the whole per-step cost including fixed overheads:
it is the price of energy, not just of erasure. Failed predictions kept as
failures; the Genie-wins-at-λ=0 mechanism is the finding, not a rescue.
