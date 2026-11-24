# Marketplace V — organization structures

**Script:** `marketplace5.py` · **World:** the M4 black-swan world, seed 99
(1000 bits, regimes ~120 steps, swans at t = 336, 550, 820) — identical
stream, so results are comparable to M4. **Scoring:** +6 correct next-bit,
+12 ten-ahead (every 10 steps), +25 correct swan call / −10 false alarm.
Wealth starts at 200; bankruptcy below 0. **Exit 1** — 1/6 predictions
passed; the five failures are the findings.

## The eight animals

| Animal | Decision rule | Cost function |
|---|---|---|
| **Paraconsistent** | 3 Belnap-valued hypotheses (T/F/Both/Neither from for/against evidence). Acts on the overlap: weighted avg of T (1x) and B (2x) hypotheses; suspends (0.5) if none. | T/F 1×LN2, **Both 2×LN2**, Neither 0.5×LN2 per step |
| **Self-build** | Starts with zero hypotheses. Builds from surprise > 0.15 (15-step window mean); uses lowest-error hypothesis; cap 8, drops worst. | 5.0 per build, 0.1 per use |
| **Dialectical** | Thesis + antithesis (1 − thesis). When both err > 0.45 over 20 steps, synthesizes a third position from the recent stream. | 3.0 per synthesis, 0.5/step tension + LN2 |
| **Stigmergic** | No world model. Reads the shared trace field (all agents' recent predictions), predicts their mean. | 0.1 read + 0.2 write per step |
| **Federated** | 3 sub-agents on strided slices of the stream; confidence-weighted vote. | 0.3 per summary × 3 per step |
| **Contrarian** | Lag-1 mean of others' predictions; bets 1 − consensus. | 0.2 to observe |
| **Satisficer** | Trailing-50 accuracy ≥ 0.60: coast (predict last bit). Below: minimal adapt. | 0.05 coast / 0.5 adapt |
| **Mimetic** | Copies the trailing-20 accuracy leader's prediction, 1-step lag. | 0.2 to observe |

**Baselines:** Gate (Mamba-style, retrained on this warmup), JEPA, Reactive
(zero-cost, from M4).

## Pre-registered predictions → results

- **P1 PASS** — paraconsistent swan-accuracy 0.870 > gate 0.652. Holding
  contradiction beats frantic adaptation *during* swans.
- **P2 FAIL** — self-build first-200 accuracy was 0.735, not < 0.52; it
  built 217 hypotheses. Construction from 15-step windows is nearly
  instant — emergence is fast when the building rule is simple. The
  "starts poor" prediction assumed building takes time; it doesn't.
- **P3 FAIL** — stigmergic swan-call 0.19, not ≥ 0.55 (spent 252 < 400 ✓).
  Reading consensus tracks the world well (acc 0.656) but cannot detect
  regime breaks *from consensus alone* — the traces agree even when wrong.
- **P4 FAIL** — contrarian calm 0.435 < 0.52 ✓, but swan-accuracy 0.232
  < calm. Pure negation loses everywhere: during swans the consensus is
  only *partially* wrong, so betting the exact opposite is worse than
  useless. Dissent must be smarter than negation.
- **P5 FAIL** — satisficer spent 264.3 vs contrarian/mimetic 168.0. The
  0.60 threshold was unreachable (overall acc 0.568), so it never got to
  coast — it paid adaptation cost nearly every step. The threshold is the
  load-bearing choice: "good enough" is only cheap if good enough is
  attainable.
- **P6 FAIL** — mimetic LED at every checkpoint (tied for max wealth
  throughout). Copying the leader with 1-step lag and near-zero cost
  doesn't just track — it wins. The norm-follower becomes king.

## Wealth ranking

mimetic 3872 > reactive 3530 > stigmergic 3362 > federated 3274 >
satisficer 3196 > dialectical 2966 > selfbuild 2941 > contrarian 2597 >
jepa 1947 > gate 1451 > paraconsistent −2 (BANKRUPT)

## The findings

1. **Paraconsistent went bankrupt.** Accuracy 0.607, swan-accuracy 0.870 —
   the best swan reader in the zoo — and it *died*. Holding Both through
   every regime change at 2× cost bled 1362 coins against its winnings.
   Paraconsistency works epistemically and fails economically: tolerating
   contradiction is accurate but ruinous when contradiction is priced.
   The cost function is the verdict, not the logic.
2. **The mimetic parasite is king.** 3872, top of the zoo. It holds no
   model, understands nothing, and wins by copying whoever's winning at
   0.2/step. Norm-following as pure strategy beats every principled
   architecture — *provided* there's someone worth copying and the lag
   doesn't kill you.
3. **Stigmergy tracks but can't alarm.** The trace-reader matched the
   federated vote on accuracy (0.656) at a third of the cost — the shared
   surface is a genuinely cheap coordination medium. But consensus traces
   can't detect the break *of* consensus. You need someone whose traces
   disagree, which means you need someone not reading the traces.
4. **Self-build and dialectical both work** (2941, 2966) — emergence and
   synthesis are viable, mid-pack strategies. Neither dominates; neither
   embarrasses itself.
5. **Gate is the cautionary tale** (1451, acc 0.531): the M1 winner,
   frugal and elegant in a calm world, bleeds in a swan world. Frantic
   adaptation is the most expensive organization of all.

## What this says about organization structures

Hierarchy (one decider) wasn't tested here — but its absence is the
result: the winner held *no* internal model and made *no* decisions of its
own. The market of the zoo rewarded, in order: **copying** (mimetic),
**coupling** (reactive), **reading the room** (stigmergic), **voting**
(federated). Every structure that maintained an expensive private model
of the world — gate, jepa, paraconsistent — paid for the privilege and
lost to structures that outsourced the model to the environment or to
each other. The commons beat the cathedral. But the commons has a
parasite problem: mimetic wins only while someone else does the
understanding, and paraconsistent shows what happens to the understanders
— they go bankrupt holding contradictions the market won't pay for.
A healthy commons needs its contrarians and paraconsistents *subsidized*,
because the market prices them out. That is a governance finding, not a
market finding.

## Reproduce

```
python3 ~/workspace/act-as-if/marketplace5.py   # exits 1: 1/6 pass
```

Files: `marketplace5.py`, `marketplace5.png` (wealth + cost bars),
this README. Seeded (99/1001), deterministic, stdlib + numpy +
matplotlib.
