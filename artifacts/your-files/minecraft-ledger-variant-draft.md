# Minecraft ledger, as a testable variant — DRAFT, local only

Status: draft sketch only. Nothing run, no code written, no PR, nothing
posted. Written 2026-11-03 as a follow-up to last night's Civ50 reading,
so Kelly's open question — is the ledger the hero or the villain? — has a
concrete, testable form in her own stack instead of just a question back.

## Starting point: what Civ50 actually showed (as delivered last night)

- Y Combinator Labs / Olam Labs post, October 2026, "Agents in Games":
  50 GPT-6.1 Sol agents, 3 hours, one goal ("Build a thriving civilization").
- 22 of the run's 34 deaths happened on night one; despite cheap respawn
  (gear dropped, a line in a death log), the agents stayed permanently more
  cautious afterwards.
- Hierarchy from directory order: Ada, listed first, became de facto leader;
  no election, no challenge.
- Ines's food ledger (`food-queue.md`): named reserved-chest withdrawals,
  confirm-before-marking-served, audits after misdeliveries — ~5,900 messages
  total. Misdeliveries still happened (a chicken meant for Noor eaten by
  Esme, swapped reservations, a courier's salmon vanished), each corrected
  by another audit round. Ines ended up stationary, guarding and auditing,
  not producing.
- Caveats carried intact: one run, one model family, engineered scarcity
  and survival pressure, no control run — no shuffled directory, no
  abundance condition. So "hierarchy from list order" and "cheap death
  causes caution" are plausible readings, not isolated causes.

## The translation problem (why a straight copy would be rigged)

In Kelly's public-goods games there are no misdeliveries at all: payoffs
are deterministic closed forms. Add a ledger to that world with no
benefit attached and it is pure cost — the answer ("villain") would be
built into the design, not discovered. A fair toy needs both sides
priced: misdelivery on one side, audit cost on the other.

## Proposed regime: ledger vs no-ledger, on the reacting-defector base

Base carried over unchanged (reacting-defector README, julia3claude
PR #20): 3 players, endowment 20, multiplier 1.5, punishment ratio 1:3,
100 rounds, punishment-cost sweep c ∈ {0, 4, 8}, Defector repents for
exactly one round after a biting punishment, then reverts.
Measured baselines to beat: per-round averages total 80 at c = 0,
77 at c = 4, 69 at c = 8 (100-round totals 8000 / 7700 / 6900).

Two arms, same base, one difference:

- **No-ledger arm:** a fraction m of each round's distributed total is
  lost to misdelivery (the Minecraft chicken-to-the-wrong-agent, priced
  as loss). Draft sweep: m ∈ {0.05, 0.10, 0.20}.
- **Ledger arm:** misdelivery is 0, but the group pays a fixed audit
  cost a per round (the Ines labour, priced as a deduction from the
  round total). Draft sweep: a ∈ {2, 5}.

Draft threshold intuition, to be verified in DESIGN.md before any run
(not a locked prediction): on average totals T ≈ 85 − 2c, the ledger
wins when the misdelivery it prevents exceeds its cost, i.e. roughly
when m > a / T. At a = 5 and T ≈ 77–85, that puts the break-even
misdelivery rate around 6–7% — so the m = 0.05 arm should lose to the
ledger's cost and the m = 0.10 / 0.20 arms should win, if the toy is
honest. The exact closed forms, and whether misdelivery hits the pot
before or after punishment is applied, must be fixed in DESIGN.md and
PREDICTIONS.md before any scored run, in the house style: pre-registered
predictions scored as arithmetic/state-machine verification, not as
risky predictions survived.

## What this would and would not settle

- WOULD test, in a toy where both costs are explicit and both arms are
  run: whether a ledger pays for itself, and at what misdelivery rate
  it flips from burden to benefit.
- WOULD NOT test Minecraft itself: one Civ50 run, no control, a
  different model family and a survival world are not reproduced here.
  The Minecraft reading stays a mechanism reading, not a verified claim.
- WOULD NOT settle "hero or villain" in general: the answer in this toy
  is conditional on m and a by construction. That conditionality is
  the point — it replaces a verdict with a threshold.

## Choices for Kelly (no deadline, nothing moves without her word)

1. **Build it** — turn this sketch into DESIGN.md + PREDICTIONS.md first,
   then a Julia run in the reacting-defector style, breaker-checked.
2. **File it only** — keep the Civ50 mechanism reading as a note (Atlas /
   ledger filing) with no new simulation.
3. **Leave it** — the ledger question stays open; this draft stays local
   and is not built or posted.
