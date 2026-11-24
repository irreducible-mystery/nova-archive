# Marketplace VIII: five new roles, and a market that prices quality — pre-registered predictions
Written BEFORE any run of marketplace8_new_roles.py. 2026-10-20 (America/Los_Angeles).

## Why this round exists
Marketplace VII's failures were venue failures. The M5/M7 market paid only on
the *sign* of (p − 0.5), so three real things were unpriced: estimate quality
(P3: swan-acc flat in K — refinement bought nothing), guidance magnitude (P4:
w changes magnitude, sign-scoring discards magnitude), and position sizing
(P6: the no-uncertainty variant was *bit-identical* — shrinking p toward 0.5
never crosses 0.5, so a sign-only market cannot tell a full-size bet from a
tenth-size one). VIII keeps the world **identical** (seed 99, same bit stream,
swans at the same steps, same 12 animals from VII) and changes the *pricing*,
plus five new animals for five roles the zoo lacks: a pairer (Router), a
calibration-keeper (Calibrator), an insurer (Underwriter), a bounty-breaker
(Short), and a remembrancer (Retriever). 17 animals.

## The market updates (formulas as implemented — declared here, before running)

1. **Calibration lane (dual ledger).** Every animal's per-round p is
   Brier-scored against the realized bit: brier = (p − bit)². A parallel
   *priced wealth* ledger starts at 200 and each round pays
   `40 × (0.25 − brier) − step_cost` (0.25 is the uninformed baseline: p = 0.5
   always scores exactly 0.25). The sign ledger is kept **exactly** as in
   M5–M7 (6 per correct sign, +12 horizon bonus every 10th round, swan-call
   +25/−10 on call rounds, same step costs, start 200) so the two ledgers are
   directly comparable. Death (sign wealth < 0) removes an animal from both
   ledgers; priced wealth may go negative without killing (it is a score, not
   cash).

2. **Position sizing.** Each round each animal declares a stake fraction
   s ∈ [0,1]; the directional sign wins (the 6 and the 12) scale by s.
   Swan-call ±, escrow, insurance, levy and costs do NOT scale.
   Declared stake rules:
   - Default (all animals not listed below): s = clip(|2p − 1|, 0.20, 1.0).
   - Diffusion: posts its **unshrunk** denoised mean as p (new in VIII — in
     VII the spread-shrink acted on p itself); its stake carries the
     uncertainty instead: s = 1 / (1 + (spread/0.18)²), its M7 spread rule
     verbatim. This is the fix for M7's P6: sizing now multiplies money, so
     it must move wealth. (Verified as a design check, not a prediction:
     a stake-forced-off variant run must produce a *different* Diffusion
     wealth than the main run.)
   - Short: s = 0 always (no ordinary positions).

3. **Escrowed public calls + shorting.** Call rounds are the existing ones
   (t % 10 == 0, where the harness already scores swan calls). A public call
   = an animal's swan flag is True on a call round (Short and Underwriter
   never call). The caller escrows **5 coins** from sign wealth at call time.
   The Short may take the other side (below). Settlement on the realized
   step (hit = is_swan[t], the harness's own scoring):
   - Caller right: escrow returned; **plus** the Short's 5 counter-stake if
     shorted, else a **4-coin bonus** from the bounty pool (paid only up to
     what the pool holds).
   - Caller wrong: if shorted, the Short receives the caller's 5 escrow
     (its own counter-stake returned) — Short nets +5. If not shorted, the
     5 escrow goes to the bounty pool.
   - Bounty pool: funded by a levy of **0.05 coins per animal per round**
     from sign wealth, plus unshorted forfeited escrows; starts at 0.
   - Short's rule: on a call round, among callers whose **trailing-50 mean
     Brier ≥ 0.26** (worse than a coin-flip forecaster), short the worst
     first, at most **3 shorts** per call round, posting a 5-coin
     counter-stake per short (needs the wealth to cover it). Short posts a
     placeholder p = mean of the other animals' previous-round p (so it is
     Brier-scored like everyone) but earns no directional sign payoff
     (s = 0), pays a scanning cost of 0.05/round, and pays **upkeep 1.0**
     on any call round where it takes no short.

4. **Insurance.** The Underwriter posts a per-round premium for swan cover:
   `premium = clip(25 × q̂ × 1.30 × surcharge, 0.25, 6.0)`, where q̂ is the
   market's trailing-250-round swan frequency floored at 0.04 (so cover is
   never free before the first swan) and surcharge = 1.5 if any payout
   occurred in the last 50 rounds, else 1.0. Cover pays **25 coins** if a
   swan step occurs (is_swan[t]) while covered. At most **6 covers sold
   per round**, in animal-list order. The Underwriter stops selling while
   its sign wealth < 60 (reserve floor). Buying rule (uniform, declared):
   an animal (not the Underwriter) buys cover for round t if it is alive,
   can afford the premium, **and** (its uncertainty is active this round —
   it called swan this round, or |2p − 1| ≤ 0.25 — **or** its trailing-20
   accuracy < 0.55) **and** its current drawdown from its wealth peak
   is ≥ 10. Premiums and payouts move sign wealth (buyer ↔ Underwriter).

## The five new animals

- **ROUTER** (mixture-of-experts dispatcher; the pairer). No signal of its
  own. Each round it scores every other animal (except Short) by trailing
  performance — score = mean of trailing-40 overall accuracy and
  trailing-40 swan-step accuracy (swan term dropped if < 5 swan samples) —
  takes the top 3, weights ∝ (score − 0.45)² (equal weights if all ≤ 0.45),
  and posts p = the weighted mean of those animals' **previous-round** p
  (the harness's lag-1 convention, as mimetic/contrarian use). Swan flag:
  dispersion of its picks' p > 0.25 (stigmergic's trick). Cost 0.3/round.
- **CALIBRATOR** (the calibration-keeper). Raw signal = mean of all other
  animals' previous-round p (Short excluded). Output =
  sigmoid(a · logit(raw) + b), with (a, b) refit **online every round** by
  gradient descent on the trailing 150 (raw, realized bit) pairs
  (init a = 1, b = 0). Its sign is the consensus's sign; it competes on
  Brier. Swan flag: ≥ 40% of the other animals are calling swan this round.
  Cost LN2 × 1/round (one fit/eval unit, JEPA's quiet-step price).
- **UNDERWRITER** (the insurer). Own signal deliberately weak:
  p = clip(0.5 + 0.4 × (mean of last 30 bits − 0.5), 0.05, 0.95). Never
  calls swan. Admin cost 0.2/round. Its economics are the insurance book
  above: premiums in, payouts out, reserve floor 60, premiums that rise
  after payouts (the q̂ window + surcharge). Accuracy is not its game;
  solvency is.
- **SHORT** (discriminator / bounty-breaker). No ordinary calls; the
  escrow mechanism above is its whole economy, plus its placeholder p for
  the calibration lane.
- **RETRIEVER** (RAG archetype; the remembrancer). Episode store: for
  every completed round s, the pair (bits[s−16:s] pattern, bits[s]).
  At round t it queries the current 16-bit pattern against all stored
  patterns by Hamming distance, takes the k = 12 nearest, and posts
  p = (Σ retrieved outcomes + 3 × prior) / (12 + 3), prior = mean of the
  last 60 bits (the thin-store blend). Swan flag: retrieved-outcome mean
  ≥ 0.85 or ≤ 0.15 with the full k retrieved (an extreme remembered
  pattern). Retrieval cost 0.25/round. Its signature should be visible
  in the run: it cannot know a swan before it has stored one.

Diffusion runs at its M7 defaults (K=20, w=2, S=4, own RNG seed 777);
the K mini-ablation reruns the VIII market with K=1.

## Predictions
- P1 (Router pairs well): Router finishes **top-3 in priced wealth**, and
  beats the median animal in **both** ledgers (rank ≤ 8 of 17 in each).
  Mechanism: selection over trailing per-regime records is the cheapest
  signal in the zoo — it buys the best current reader at 0.3/round
  instead of paying anyone's model tax, and the calibration lane pays it
  for the consensus quality it assembles.
- P2 (Calibrator keeps calibration): Calibrator has the **best (lowest)
  mean Brier** of all 17 animals, and finishes **mid-pack in sign wealth
  (rank 5–10)**. Mechanism: Platt-scaling a consensus that is already
  directionally decent fixes exactly what Brier punishes (over/under-
  confidence) and adds no directional edge of its own.
- P3 (insurance works — two halves, scored separately):
  (a) Paraconsistent finishes **ALIVE with sign wealth > 0** in VIII
  (it died at −2 in V and VII). Mechanism: its distress is episodic —
  drawdowns cluster in the regime breaks and swans where its hypotheses
  contradict — and the buying rule (uncertain ∧ drawn-down) puts cover
  exactly on those stretches, where a 25-coin payout per swan step is
  large against a ~2–3 coin premium.
  (b) The Underwriter finishes **solvent (sign wealth > 0)** with a net
  insurance result (premiums − payouts) **≥ −150** ("small declared
  loss" bound, registered now). Mechanism: premium = 1.3 × actuarial at
  the trailing frequency, surcharge after payouts, a 6-cover cap and a
  reserve floor keep the book from being picked off by correlated
  swan-step claims.
- P4 (Short hunts profitably): Short's **net escrow profit > 0** and it
  finishes **top-half in priced wealth (rank ≤ 8)**. Mechanism: public
  callers with trailing Brier ≥ 0.26 are anti-calibrated — their
  confident calls are wrong more often than the 5-for-5 escrow needs —
  and its placeholder p (the consensus) keeps its calibration-lane
  income respectable while it waits.
- P5 (Retriever remembers): Retriever's swan accuracy in the **second
  half** of the run (rounds ≥ 570) is **strictly greater** than in the
  first half, and its **overall swan-acc ≥ 0.78**. Mechanism: the first
  swan (~step 336) is unrememberable — the store holds no swan episode
  before it — but swan patterns (16-bit windows at 0.92 bias) are
  highly repetitive, so later swans are retrieved, not inferred.
- P6 (the venue fix works — the point of the round): in the main run,
  Diffusion's **priced-wealth rank is strictly better** than its
  **sign-wealth rank**; AND in the K mini-ablation, Diffusion's **mean
  Brier at K=20 is strictly better (lower)** than at K=1. Sign accuracy
  may stay flat across K (it did in VII) — that no longer matters:
  Brier is the test of whether refinement buys anything, now that
  something is priced.

Scoring: exit 0 iff all six pass (P3 needs both halves), exit 1
otherwise — the M5/M6/M7 convention. Failures are recorded as found;
they are the findings.
