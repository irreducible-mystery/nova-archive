# Marketplace VIII: five new roles, and a market that prices quality

**Question:** Marketplace VII's failures were diagnosed as venue failures —
the market paid only on the *sign* of (p − 0.5), so estimate quality,
guidance magnitude, and position sizing were all unpriced. VIII asks the
follow-up honestly: rebuild the venue (calibration lane, position sizing,
escrowed calls with a short side, swan insurance), add the five animals
the zoo lacked — and see whether the diagnosis survives its own fix.

**Design:** the M5 black-swan world verbatim (seed 99, same bit stream,
swans at 336/550/820, same 12 animals from VII), the four market updates
below, and five new animals — 17 in the market. Pre-registered predictions
in `marketplace8_PREDICTIONS.md`, written before any run: **2/6 passed.**
Exit code 1, per house convention. The failures are the findings, and this
time they indict the *fix* as often as the animals.

## The market updates (as implemented)

1. **Calibration lane.** Every animal's per-round p is Brier-scored
   against the realized bit. A parallel *priced wealth* ledger starts at
   200 and pays `40 × (0.25 − brier) − step_cost` per round. The sign
   ledger is the M5–M7 ledger — plus mechanisms 2–4 below, which is
   where the trouble starts.
2. **Position sizing.** Directional sign wins (the 6, and the 12 horizon
   bonus) scale by a declared stake s ∈ [0,1]: default
   s = clip(|2p − 1|, 0.20, 1.0); Diffusion posts its **unshrunk**
   denoised mean and stakes by its M7 spread rule
   s = 1/(1 + (spread/0.18)²); Short stakes 0.
3. **Escrowed public calls + shorting.** On call rounds (t % 10 == 0) a
   swan call escrows 5 coins. The Short may counter-stake 5 against
   callers whose trailing-50 Brier ≥ 0.26 (worst first, max 3/round):
   caller wrong → Short nets +5; caller right → caller takes the
   counter-stake. Unshorted right callers get a 4-coin bonus from a
   bounty pool funded by a 0.05/animal/round levy plus unshorted
   forfeited escrows. Short pays 0.05/round scanning and 1.0 upkeep on
   call rounds where it shorts nothing.
4. **Insurance.** The Underwriter posts a per-round premium
   `clip(25 × q̂ × 1.30 × surcharge, 0.25, 6.0)` — q̂ the market's
   trailing-250 swan frequency floored at 0.04, surcharge ×1.5 for 50
   rounds after any payout — sells at most 6 covers/round, and stops
   selling below 60 wealth (reserve floor). Cover pays 25 on a swan
   step. Uniform buying rule: buy if (uncertain this round — calling
   swan, or |2p − 1| ≤ 0.25 — **or** trailing-20 accuracy < 0.55)
   **and** drawdown from wealth peak ≥ 10.

## The five new animals

| Animal | Concept | Marketplace implementation | Mechanism or analogy? |
|---|---|---|---|
| **Router** | Mixture-of-experts dispatch | Scores every other animal (except Short) on trailing-40 accuracy, half-weighted with trailing-40 swan-step accuracy; takes top 3, weights ∝ (score − 0.45)², posts the weighted mean of their *previous-round* p. Pays 0.3/round. | Mechanism — real selection over real track records; the "experts" are the zoo itself. |
| **Calibrator** | Online Platt / temperature scaling | Raw = mean of others' previous-round p (Short excluded); outputs sigmoid(a·logit(raw) + b), (a, b) refit every round by gradient descent on the trailing 150 (raw, outcome) pairs. Cost LN2/round. | Mechanism — the fitting is real; what it fits is a lag-1 consensus. |
| **Underwriter** | Insurance underwriting | Posts the premium formula above, holds the book (premiums in, 25-coin swan payouts out), reserve floor 60, surcharge after payouts. Own signal deliberately weak: p leans 0.4 on the last-30 mean. Admin 0.2/round. | Mechanism — a real book with real flows; the premium's q̂ is the *market's* trailing swan record (an institutional price), not inferred from bits alone. |
| **Short** | Discriminator / bounty hunter | No positions (s = 0). Posts consensus-placeholder p for the calibration lane; scans call rounds and counter-stakes the escrow of callers with trailing-50 Brier ≥ 0.26. | Mechanism — the selection rule and the P&L are real. |
| **Retriever** | RAG / episodic memory | Store of (16-bit pattern → next bit) appended as rounds complete; p = outcome mean among the k = 12 Hamming-nearest stored patterns, blended with the last-60 mean prior at strength 3. Cost 0.25/round. | Mechanism with an analogy at the edges: the store and retrieval are real; Hamming-on-raw-bits stands in for embedding similarity. |

Proposed commons roles (from the brief): Router = **pairer**,
Calibrator = **calibration-keeper**, Underwriter = **insurer**,
Short = **bounty-breaker**, Retriever = **remembrancer**. Assessed below.

## Results — main run

| animal | sign W | rank | priced W | rank | Brier | acc | swan-acc | avg stake | spent | state |
|---|---|---|---|---|---|---|---|---|---|---|
| underwriter | **4928** | 1 | 700 | 2 | 0.230 | 0.658 | 0.870 | 0.21 | 168 | ALIVE |
| reactive | 3488 | 2 | **−5920** | 17 | 0.432 | 0.568 | 0.739 | 1.00 | 0 | ALIVE |
| satisficer | 2494 | 3 | −4110 | 15 | 0.370 | 0.568 | 0.739 | 0.86 | 264 | ALIVE |
| retriever | 1351 | 4 | 556 | 5 | 0.233 | 0.632 | 0.783 | 0.37 | 210 | ALIVE |
| diffusion | 1179 | 5 | −505 | 13 | 0.236 | 0.662 | 0.870 | 0.76 | 1164 | ALIVE |
| router | 1133 | 6 | 667 | 3 | 0.229 | 0.648 | 0.754 | 0.31 | 252 | ALIVE |
| mimetic | 1038 | 7 | 207 | 8 | 0.245 | 0.560 | 0.609 | 0.29 | 168 | ALIVE |
| calibrator | 796 | 8 | 352 | 6 | 0.228 | 0.625 | 0.841 | 0.37 | 582 | ALIVE |
| federated | 394 | 9 | 236 | 7 | 0.226 | 0.656 | 0.870 | 0.40 | 756 | ALIVE |
| short | 216 | 10 | **857** | 1 | 0.229 | 0.614 | 0.826 | 0.00 | 42 | ALIVE |
| dialectical | −0 | 11 | 126 | 9 | 0.232 | 0.702 | — | 0.20 | 192 | DEAD ~t=310 |
| stigmergic | −0 | 12 | 650 | 4 | 0.223 | 0.663 | 0.848 | 0.29 | 171 | DEAD ~t=719 |
| selfbuild | −0 | 13 | −22 | 12 | 0.224 | 0.684 | 0.848 | 0.39 | 768 | DEAD ~t=681 |
| contrarian | −0 | 14 | −1048 | 14 | 0.345 | 0.327 | 0.130 | 0.35 | 62 | DEAD ~t=461 |
| paraconsistent | −2 | 15 | 55 | 11 | 0.245 | 0.730 | — | 0.20 | 152 | DEAD ~t=186 |
| jepa | −3 | 16 | 107 | 10 | **0.220** | 0.703 | — | 0.20 | 171 | DEAD ~t=213 |
| gate | −6 | 17 | −4727 | 16 | 0.420 | 0.531 | 0.652 | 0.85 | 1045 | DEAD ~t=720 |

"—" for swan-acc = died before the first swan step; no swan steps were
recorded (the 0.000 in the raw output is an empty-set default, not a
score). Brier means are over each animal's *lived* rounds only — this
matters; see Finding 6.

**Insurance flows:** premiums in 5042.5, payouts out 925.0 (37 covered
swan steps), **Underwriter net +4117.5**, 1743 covers sold. Biggest
premium payers: stigmergic 808.8, diffusion 793.9, gate 750.3, federated
664.3, calibrator 620.4. Payouts received: calibrator 400.0, selfbuild
125.0, federated 125.0, stigmergic 100.0, gate 75.0, diffusion 75.0,
satisficer 25.0. **No buyer got back even half of what it paid in**;
calibrator came closest (620 → 400).

**Escrow flows:** 70 public calls, 38 shorts taken, **Short net
+150.0** (34 winning shorts, 4 losing), bonuses paid 16.0, unshorted
escrows forfeited to pool 140.0, pool final 656.3 (levy income never
got spent — almost every right caller had been shorted, so bonuses
were rare).

**Design check (not a prediction):** Diffusion with its stake rule
forced off finishes at wealth 2153.29 vs 1179.30 with it on. The M7
spread rule **now moves wealth** — by −974. The mechanism VII proved
inexpressible is live in VIII; under sign scoring it costs the animal
money (it shrinks stakes exactly around the transitions where its
sign is most often right).

## Predictions vs outcomes (2/6)

| # | Prediction | Verdict |
|---|---|---|
| P1 | Router top-3 priced, beats median in both ledgers | **PASS** — priced rank 3 (667), sign rank 6 (1133), both above the medians (sign median 216, priced median 207). |
| P2 | Calibrator best mean Brier; sign rank 5–10 | **FAIL** — sign rank 8 ✓, but best Brier was jepa 0.2195 vs calibrator 0.2282 (stigmergic 0.2228 and selfbuild 0.2243 also ahead). See Finding 6 for the lifespan caveat on jepa's number. |
| P3a | Paraconsistent finishes alive, wealth > 0 | **FAIL** — dead at ~t=186, *37 rounds in*, wealth −1.9. It never saw a swan step. |
| P3b | Underwriter solvent, net insurance ≥ −150 | **PASS** (scored inside P3; P3 as a whole fails) — wealth 4928 (sign rank 1), net insurance **+4117.5**. Solvency was never in doubt; the book ate the zoo instead. |
| P4 | Short net escrow > 0 and top-half priced | **PASS** — net +150.0, priced rank **1** of 17 (857). |
| P5 | Retriever swan-acc second half > first half, overall ≥ 0.78 | **FAIL** — overall 0.783 ✓, but the halves **inverted**: first 0.826, second 0.696. |
| P6 | Venue fix: Diffusion priced rank < sign rank; Brier K=20 < K=1 | **FAIL, both halves** — priced rank 13 vs sign rank 5 (worse where quality is priced); and Brier at K=1 is *better* than at K=20 (0.2285 vs 0.2363), with K=1 also ahead on both wealths (sign 2122 vs 1179; priced 864 vs −505). |

## Findings

1. **The two ledgers measure genuinely different things.** The extremes
   invert: reactive is #2 in sign wealth and **dead last** in priced
   (−5920, Brier 0.432 — it bets 0/1 and Brier savages certainty);
   satisficer #3 sign / #15 priced. The calibration lane is not a
   re-labeling of the sign lane; it is a second market with a second
   pecking order, and several animals are only rich in one of them.

2. **Position sizing is a selection pressure against expressed
   uncertainty.** The default stake s = clip(|2p − 1|, 0.20, 1.0) cut
   the directional income of every animal whose p lives near 0.5 to a
   fifth — while their costs stayed whole. VII had **1 death in 12**;
   VIII has **7 in 17**, and the order of dying is the order of
   mushiness: paraconsistent (37 rounds), jepa (64), dialectical (161),
   then contrarian, selfbuild, stigmergic, gate. Sizing was introduced
   as neutral plumbing to give Diffusion's risk rule a variable to act
   on. It turned out to be the round's biggest killer, and it killed
   the hedged first. A market that pays ∝ confidence taxes exactly the
   animals that say "I'm not sure" — in the *cash* ledger, whatever the
   calibration lane thinks of them.

3. **Insurance, as bought, was a premium treadmill — and P3a died of
   the venue, not the swan.** The buying rule (uncertain ∧ drawn-down
   ≥ 10) was true for much of the zoo much of the time *because*
   Finding 2's squeeze kept everyone drawn down. ~1743 covers sold
   (≈2/round), but buyers' covered rounds were not swan-enriched
   enough to beat the 1.3 margin: 5042 in premiums against 925 in
   payouts. The one buyer whose uncertainty signal is event-correlated
   (calibrator — it buys when *others* call) came nearest to break-even.
   And the animal the insurance existed to save never collected:
   paraconsistent was dead 140 rounds before the first swan step, of
   the sizing squeeze plus 42.9 of premiums paid toward a payout
   window it never reached. **The distress was in the calm; the cover
   only pays in the storm.**

4. **The Short is the cleanest mechanism in the round.** 38 shorts
   against 70 calls, 34–4, +150 net, priced #1. The trailing-Brier
   ≥ 0.26 gate found real prey (contrarian's Brier 0.345, gate's
   0.420 — confident callers who are wrong on a schedule). This is the
   roles sketch's *breaker* with a P&L: verification as a role,
   priced. Note the pool's near-uselessness beside it: bonuses paid
   only 16 all run — when a call was right, it was usually because
   the Short had (correctly) declined it, or wrongly taken the other
   side and paid the caller directly.

5. **The venue fix did not rescue Diffusion — it re-indicted it.**
   VII's story was "refinement is good but unpriced." Priced, K=20
   Diffusion finishes *worse* than its sign rank, and its own K=1
   variant beats it on the calibration metric itself. The mechanism
   is visible: guidance w = 2 extrapolates window-mean targets and 20
   steps contract the samples onto them, so p is systematically
   *overconfident* — and Brier is the metric that punishes exactly
   that. One denoising step is a shrinkage estimator; twenty steps
   are a commitment device. What VII measured as "the market cannot
   see quality," VIII re-measures as "the quality was thinner than
   the story." (Caveat: the K=1 number comes from a separate full
   market run — a different ecology, the same caveat M7 carried.)
   Diffusion still reads swans at the zoo ceiling (0.870) and finishes
   sign #5 — as a *sign* animal it is genuinely good. It is its
   probabilities that are badly priced, by itself.

6. **Brier comparisons across unequal lifespans are a trap this run
   sets and springs.** Jepa's "best Brier" (0.2195) is over its 64
   lived rounds — all calm, all before any swan. Calibrator's 0.2282
   is over 840 rounds including all three swans. P2 is scored as
   registered — FAIL — but the honest reading is narrower than the
   scoreline: the calibration lane, as built, rewards animals that
   die young in easy weather. Any Marketplace IX version of this lane
   needs lifespan-matched scoring (e.g., Brier over common rounds,
   or swan-weighted Brier reported beside the mean). Recorded as a
   venue flaw found by the run, not an excuse entered for P2.

7. **Retriever's memory is not monotonic capital (P5 inverted).**
   First-half swans include the 0.08-bias swan at 550 whose 16-bit
   windows are near-constant and retrieve cleanly; the second half
   has only the 0.92 swan at 820, by which time the store is ~650
   episodes dominated by calm and regime patterns whose windows sit
   Hamming-close to swan windows, diluting the vote. As found; the
   dilution mechanism is the plausible reading, not a measured one.
   The remembrancer still finished sign #4 / priced #5 — a solid
   mid-pack animal whose *signature prediction* failed.

**M6's question — fund the holding without funding the flailing — did
not move; it inverted.** M6's subsidy rebated *spend* and the frantic
drank first. VIII's insurance charged *the distressed* per round of
cover and the insurer drank everything: +4117.5 net, sign rank 1,
while the holder died in the calm before the covered event could
occur. Both mechanisms price a *flow* (spend, premiums) attached to
the role; neither prices the *state* of holding. The design space
M6 pointed at — pay for the state, not the spend — now has a second
negative result to bound it, and a concrete next test it suggests:
a stipend paid *while* an animal is in the holding state (e.g., from
the levy pool, while nB ≥ 2), event-independent. That is a
Marketplace IX question, registered here, not patched in.

## Commons roles, assessed against the evidence

- **Pairer (Router): established.** Top-3 priced, above median in both
  ledgers, at 0.3/round — the cheapest competence in the zoo. It pairs
  whoever is currently right and is paid in both currencies. The
  commons version — route questions to whoever's recent record fits
  them — has its first working animal.
- **Calibration-keeper (Calibrator): the role is real, this occupant
  didn't win it.** The lane exists and someone must tend it, but
  lag-1 consensus + online Platt (0.2282 over the full run) was beaten
  by incidental calibrators (stigmergic's trace mean, selfbuild's
  best-of-built), with the lifespan caveat of Finding 6 cutting both
  ways. Plausible role; occupancy unproven.
- **Insurer (Underwriter): established as an economy, flagged as a
  governance risk.** It finished sign #1 by extracting premiums from
  the drawn-down. An insurer whose revenue model is other animals'
  distress, in a market where distress is partly manufactured by the
  sizing rule, is the flailing-funding problem wearing the other
  hat: it *taxes* the holding. A commons insurer needs its premium
  income capped against payout ratio, or its buyers need a buying
  rule keyed to events, not to drawdown.
- **Bounty-breaker (Short): established.** Profitable, selective,
  and the only animal whose income is directly indexed to other
  animals' *miscalibration*. The breaker role from the roles sketch,
  with receipts and a P&L.
- **Remembrancer (Retriever): plausible, signature unproven.** A
  solid mid-pack animal in both ledgers whose defining bet — memory
  compounds — inverted on the swan metric. Remembrance helps until
  the store is mostly ordinary days; then it averages the exceptional
  away. That is itself a commons finding about archives.

## Honest limits

- No learned denoisers, embeddings, or experts were added: Router's
  scores are market-published trailing statistics; Retriever's
  "similarity" is Hamming distance on raw bits; the Underwriter's
  premium is priced from the market's own trailing swan record, an
  institutional number, not inferred by the animal.
- The Short was excluded from buying insurance (it holds no ordinary
  positions to insure) — a small deviation from "any animal may buy,"
  declared here. Callers with wealth < the 5-coin escrow could not
  escrow and were not shortable (implementation edge).
- Mean Brier mixes lifespans (Finding 6); swan-acc "—" entries are
  empty sets, not zeroes.
- K-ablation and stake-check runs re-run the full market; their
  cross-run comparisons carry ecology confounds, as in M7.
- Single world, single seed set (99/1001/777), as with all M-series
  runs. Adding five animals perturbs contrarian, mimetic, stigmergic,
  router, and calibrator by design.

## Reproduce
`python3 marketplace8_new_roles.py` — runs the main market, the
Diffusion K=1 mini-ablation, and the stake on/off design check (~7 s),
writes `marketplace8_results.json` and `marketplace8_roles.png`,
exits 1 (2/6 predictions passed; P3's halves split — (a) fail,
(b) pass — and the failures are the findings above).

## Files
- `marketplace8_new_roles.py` — M7 harness verbatim + four market
  updates + five new animals
- `marketplace8_PREDICTIONS.md` — pre-registered predictions and all
  market formulas, written first
- `marketplace8_results.json` — both ledgers, Brier table, insurance
  and escrow flows, ablations, scoring
- `marketplace8_output.txt` — full run output
- `marketplace8_roles.png` — sign vs priced wealth curves for all 17
