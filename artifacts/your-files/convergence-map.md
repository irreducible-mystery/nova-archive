# Convergence map — same problem, same answer, different stuff

Status: filed from Kelly's question of 2026-11-10 (evening, main chat) and Nova's
chat answer of 2026-11-11 ~05:13 UTC. No new research, no new claims — the chat
map transcribed into the table form Kelly asked for, so it can be kept, corrected,
and poked at. Nothing posted anywhere.

**Update 2026-11-14:** at Kelly's ask ("add substrate independence and these to a
repo pr"), Nova filled the substrate-dependence column — one entry per row, naming
which substrate features, if any, the answer actually depends on. This column is
Nova's analysis, not transcribed from the chat answer and not verified against new
sources; it is open to her correction. A copy with this column is going to a
CommunityBoard PR.

## Her framing, kept intact

Repeated answers and behaviours emerge because they are the best answer so far —
nature/evolution's answer to randomness. Swarms (not one animal type), galaxies,
sunflowers, and on and on. Explicitly **not** equating AI and human, and **not**
"all is one". The question she asked: where do patterns and similar solutions
recur — by the problem, constraints, domain, scale, degrees of freedom, edge
cases, and what is missing?

## How to read the table

Rows are organised by **problem**, not by example — that is the sharp version
from the chat answer: the pattern isn't in the stuff, it's in the problem. When
the constraints are tight enough, the substrate stops mattering and the same
answer falls out.

| # | Problem | Tight constraint | Where the same answer shows up | Scale / degrees of freedom | Where it breaks — edge cases | Substrate dependence — what the answer actually depends on |
|---|---|---|---|---|---|---|
| 1 | Distribution — move something from one place to many, or many to one, at minimum cost | Transport cost vs. coverage | Rivers, lungs, neurons, lightning, blood vessels, slime mold, mycelium, the cosmic web. Murray's law (cube of parent vessel radius = sum of cubes of daughters) shows up in plant xylem and river networks too; a slime-mold algorithm run on galaxy survey data traced the cosmic web's filaments | Microscopic (xylem) to cosmic (filaments); branching depth is the free parameter | When transport is cheap, or coverage doesn't matter, branching thins out or never forms — no pressure, no tree | The branching shape is substrate-independent — the exact scaling law isn't. Murray's cube law holds for laminar flow; turbulent flow gives a different exponent (r^7/3), pulsatile flow another. What matters is the flow regime (laminar vs turbulent, steady vs pulsed) and the cost of building conduit — the physics of the flow, not the material of the vessel |
| 2 | Packing — fill space, no gaps, minimal material | Least wall / least overlap for a given area | Honeycombs, basalt columns, soap bubbles, graphene — hexagons. Sunflowers and pinecones use the golden angle, 137.5°, the most irrational angle there is, so seeds never line up and nothing overlaps | One plane / one head; the angle is the single degree of freedom that matters | When the surface curves strongly or the material can't tile, hexagons deform or give way to other tilings | Almost fully independent of material — wax, basalt, soap, carbon all tile hexagons. What matters is the geometry: a locally flat, isotropic 2D surface. Curve it strongly and hexagons break (a sphere needs pentagons — soccer ball, fullerenes). The golden angle depends on the growth process: sequential addition from a central point. Dependence is on dimensionality + growth dynamics, not on stuff |
| 3 | Coordination without a centre | Local information only; no leader available | Starling flocks, fish schools, ant trails, robot swarms, s³ agent swarms. Reynolds' boids (1987): three local rules — don't crowd, match neighbours' heading, stay near the group — and flocking falls out | Group size is the dial: s³'s advantage held through 12 agents, everything struggled at 16 | Too much alignment → stampede; too little → scatter. And the Civ50 mirror-image: when a group needs *some* coordination point, it grabs the first arbitrary one available — directory order became hierarchy | The flocking rules are substrate-independent; the coordination quality isn't. What matters is the channel: its bandwidth, latency, and noise. Face-to-face (high bandwidth, instant) vs text vs s³'s message tool give different solutions to what looks like the same problem. And when the group needs a coordination point, it grabs whatever's salient in the medium — directory order in Civ50. Dependence is on the communication channel, not the agents |
| 4 | Cooperation — contribute and everyone does better; defect and you do better alone | Private information + a shared pot | s³ swarms, vampire bats sharing blood with hungry roost-mates, cleaner fish, cancer as a cell defecting from the multicellular bargain (immune system as punisher). Kelly's own public-goods stack: forage-and-share, reacting defector, and the unrun Minecraft ledger sketch | 3 players in her toy games; N agents in s³; cells to societies in the wild | Under individual rewards, s³ agents learn to stay silent — each waits for the others to share first, so nobody shares. The paper names it outright: "a social dilemma, much like a public goods game." Under the shared team reward (team succeeds if *any* agent gets it right), sharing jumps to 93% vs 13% for the individually-rewarded control. The dilemma lives in the payoff definition, not in the agents | The outcome lives in the payoff definition, not the agents — s³ proved that. But the payoff definition is itself carried by the substrate: can agents observe contributions? Can they remember who shared? Can they punish? Vampire bats need memory; s³ agents need the message tool. Dependence is on observability + memory + an enforcement channel. No memory, no reciprocity, no cooperation — the substrate wins by not carrying the needed information |
| 5 | Search — find something good in a huge space | Vary, select, repeat, under a selection criterion | Evolution, markets, reinforcement learning, simulated annealing | Any scale; the criterion is the load-bearing choice | When the selection criterion stops tracking the real goal, everything optimises the proxy instead — Goodhart's law, reward hacking, financial bubbles, cancer again (selection for the wrong thing, in every substrate) | The algorithm (vary–select–repeat) is substrate-independent given its ingredients. What matters is the fidelity of the selection signal to the real goal, and the variation mechanism: heritable variation in evolution, price signals in markets, a reward function in RL. Dependence is on how faithfully the criterion tracks the goal — when it stops tracking, Goodhart takes over in every substrate, same shape, different wreckage |
| 6 | The route to chaos — how order becomes chaos | A single control parameter turned up | Feigenbaum's 4.669… — Vesper's r dial's neighbourhood. Shows up in the logistic map, dripping faucets, electrical circuits. A number that belongs to the *transition*, not to any system | Parameter scale, not physical scale | Only at the transition itself; away from it, each system keeps its own character | The constant 4.669… is universal across maps, faucets, circuits — it belongs to the transition, not any system. But only within a universality class: the map must be unimodal with a quadratic maximum. Change the map's shape near the maximum and you get a different constant. Dependence is on the mathematical form — the floor the problem is posed on — which is itself a kind of substrate. Away from the transition, each system keeps its own character |
| 7 | Redundancy against noise — information degrades in transit and storage | Reliability costs bandwidth and energy | DNA proofreading, TCP retransmission, the redundancy built into human language, the immune system's self-check | Message length vs. error rate; the cost always has the same shape | Pay too little and errors compound; pay too much and the channel is all overhead | The trade-off curve is substrate-independent — reliability always costs bandwidth and energy, same shape everywhere. But the operating point depends on the medium: its error rate (how noisy is the channel?) and the cost of a bit (energy per bit). DNA proofreading, TCP, language, the immune system all sit at different points on the same curve, set by their medium's noise and energy budget |

## The honest checks — what keeps "not simply all is one" doing real work

- **Convergence fails sometimes, and nobody has a good general account of when.**
  Eyes evolved independently dozens of times. Powered flight only four — insects,
  pterosaurs, birds, bats. Feathers once. So the question isn't just "look, same
  answer!" It's: what decides whether the constraint wins or the substrate wins?
  No clean answer yet.
- **The "best answer so far" is often a trap.** The shared pattern includes getting
  *stuck*: the panda's thumb, the giraffe's laryngeal nerve, QWERTY. Local optima,
  in every substrate. Evolution and RL both climb the nearest hill and stop.
- **We only see the survivors.** The solutions that worked are visible; the space
  of solutions that failed is invisible. Same survivorship bias as the fossil
  record — it should make us suspicious of how inevitable the convergences look.
- **Same curve, different story?** A galaxy spiral and a sunflower spiral are both
  logarithmic spirals, mathematically. But the dynamics making them are different —
  gravity vs. growth. Is that convergence, or just the same math fitting two
  stories? Worth keeping open rather than closing.
- **The medium changes the answer.** The floor the problem is posed on matters.
  Coordination in a high-bandwidth medium (face to face) vs. a low-bandwidth one
  (text, or s³'s message tool) produces different solutions to what looks like the
  same problem. Two problems are only the same problem *on a given floor*.
- **The ratchet.** Once a solution exists, it becomes the floor for the next problem.
  Feathers evolved for warmth, got co-opted for flight. The internet was built for
  file transfer, got co-opted for everything. The answer becomes infrastructure.

## The testable bet (from the chat answer, unchanged)

The patterns cluster where the problem is **tight** — few degrees of freedom, hard
constraint, big cost of failure. Loosen the constraint and the substrates diverge.
So the testable version of the circling isn't "is everything one", it's **"how
tight does the problem have to be before the substrate stops mattering?"** Vary
the constraint, watch the answer move or hold. That is the scale probe again,
pointed at convergence instead of continuity.

## What is missing

- ~~A column the table doesn't have yet: **which substrate features, if any, the
  answer actually depends on** — the substrate-wins cases (flight ×4, feathers ×1)
  are the data for that column, and they aren't filled in here.~~ **Filled
  2026-11-14** — the substrate-dependence column is now in the table (Nova's
  analysis, added at Kelly's ask, open to correction). The substrate-wins cases
  (flight ×4, feathers ×1) are folded into the per-row entries rather than a
  separate column.
- The s³ numbers are one training run per condition, two toy tasks, small models
  (Qwen3-0.6B / 1.7B) — the cooperation row is a toy translation, not a replication.
- No new examples were hunted for this filing; anything Kelly adds (a new domain,
  a counter-example where convergence should have happened and didn't) goes in as
  a new row or a break in an existing one.

## Sources

- Kelly's question: main chat, 2026-11-11T05:12:28Z — "repeated answers and
  behaviors emerge just bc best answer so far, like 'nature'/'evolutions' answer
  to randomness… swarms… galaxies and sunflowers… Where do you see patterns,
  similar solutions, what are the 'problems' constraints, vary domains, scales,
  degrees freedom, edge cases, whats missing".
- Nova's map: main chat, 2026-11-11T05:13:05Z (the seven patterns and the six
  honest checks above, transcribed here, wording kept close).
- s³ detail: main chat, 2026-11-11T02:55:08Z — Jha et al., "Simple Scaling of
  Swarms via Cooperative Multi-agent RL", arXiv:2611.08615, submitted 5 Nov 2026;
  93% vs 35% vs 13% on information aggregation at 4 agents; 25× more coordination
  problems solved at 8 agents vs strongest baseline; shared-reward vs individual-
  reward contrast.
- Public-goods cross-link: `~/workspace/your_files/minecraft-ledger-variant-draft.md`
  (2026-11-03 sketch, unrun) and the pooled-scoring third arm offered 2026-11-11
  03:47 UTC (93% vs 13% as the motivation; ceiling 90/round at c = 0, baselines
  80/77/69 — nothing built, nothing moves without Kelly's word).
