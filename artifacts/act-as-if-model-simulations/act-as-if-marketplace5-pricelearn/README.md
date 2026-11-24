# MARKETPLACE V — do the animals learn the price of energy?

M4 moved the cost floor under fixed dials. Now the dials move: each animal
gets a meta-policy that re-tunes its dial every 25-step block. The question:
is frugality DISCOVERED, or does the floor have to TEACH it?

## The two candidate teachers

- **THERMOSTAT** — wealth > 150 → lavish | 50–150 → normal | ≤ 50 → frugal.
  The floor teaches via fear. (Proposed in M1's docstring; never run.)
- **BANDIT** — epsilon-greedy over the 3 dials, reward = block wealth-delta.
  Discovers the price from the reward signal alone. (Plus **BanditAlpha**,
  constant step-size α=0.2 — the forgetting breaker, added mid-build.)

World: the long calm (M1's generator, seed 21, N=1500, warmup 100) so
bandits get ~56 blocks to learn. λ ∈ {0.3, 1, 2, 3}.

## Pre-registered predictions

P1 bandits → frugal as λ rises (λ=2: >60% frugal late); P2 λ=3 survival
thermo ≥ bandit > fixed (kept as the documented extinction — M4 already
showed no dial survives λ=3); P2b λ=2: thermo ≥ bandit > fixed; P3 shock:
thermostat frugal ≤2 blocks, bandit re-converges in ~8–12; P4 λ=0.3: optima
≠ frugal (they learn the exchange rate, not "frugality good"); P5 bandit
wealth ≥ fixed-normal wealth per λ; P6 (breaker, added after E3): the
forgetting bandit re-tunes post-shock and beats running-mean wealth.

## E1 — bandits on stationary floors: the beautiful discovery

Late-block dial shares (frugal/normal/lavish):

| λ | gate | jepa | genie |
|---|---|---|---|
| 0.3 | .85/.05/.09 | .04/.07/**.89** | .05/.04/**.91** |
| 1.0 | .85/.05/.09 | **.78**/.07/.15 | .05/.04/**.91** |
| 2.0 | alive, .85 frugal | **dead** (round-robin) | dead (frugal .93) |
| 3.0 | dead | dead | dead |

**P1: FAIL. P4: PASS.** The bandits don't learn "frugality good" — they
learn the *price-conditioned optimum*, and it's gorgeous:
- Gate → frugal at every λ. Its frugal dial is also its most *accurate*
  (0.582 vs 0.544 lavish): dominance, no tradeoff. Rediscovered from rewards.
- JEPA → **lavish at λ=0.3, frugal at λ=1**. Its dial doesn't change
  next-bit accuracy at all (0.588 everywhere) — the bandit is arbitraging
  the *regime-call* margin: cheap energy makes extra updates (+15s) worth
  buying; at λ=1 they aren't.
- Genie → lavish at λ≤1: depth 3 unlocks the +6 futures niche (dormant in
  M1's fixed depth-2 market). The learner found a niche the fixed animal
  never used: bandit-Genie wealth 4065–8530 vs fixed 1565–4890.

**The λ=2 knife-edge.** JEPA-bandit died *during the 3-block round-robin*:
block 0's frugal sample was unlucky (−17.5 vs ~+4 true mean), then
normal/lavish bled −54/−51, wealth −1.9 → dead before exploitation began.
With ~2 blocks of life expectancy, a 3-arm round-robin is suicide — a single
noisy sample per arm, no time to correct. Genie learned *correctly* (93%
frugal) and died anyway: frugal at λ=2 is net ~0/step, noise decides.
Right answer, still dead.

## E2 — populations: fear vs discovery vs fixed

Mean wealth (fixed / thermo / bandit): λ=0.3: 5164 / 6127 / **6503**;
λ=1: 2488 / 2807 / **3870**; λ=2: 239 / 121 / **344** (gate only alive);
λ=3: −2 / −2 / −4 (all dead).

**P2: FAIL** (honestly — λ=3 is extinction; fear can't beat math when no
dial survives). **P2b: FAIL** — at λ=2 all populations tie at 1/3 survivors;
meta-policies don't change *who* can survive, only how well the survivor
does. **P5: PASS** at λ ∈ {0.3, 1, 2} (FAIL only at λ=3, where the
comparison is corpse-vs-corpse). Note the fear tax: thermo-gate at λ=2 made
370 vs fixed-gate 726 — going lavish while rich burned money it later needed.

## E3 — the shock (λ 0.3 → 3.0 at block 28): both teachers break

- **Thermostat: gate alive (707), JEPA DEAD (−0.6), genie alive (23).**
  **P3: FAIL.** The thermostat *never* chose frugal after the shock. Why:
  its thresholds (150/50) are absolute, but the cheap phase made everyone
  rich (wealth ~5000). Post-shock it kept choosing *lavish* while dying —
  wealth had to fall thousands of coins to reach the fear threshold, and
  bankruptcy arrived first. Fear miscalibrated by wealth.
- **Running-mean bandit: all alive (1898/1522/287).** But **P3b: FAIL** —
  Genie was still 83% *lavish* 12–24 blocks after the shock. Diagnosis
  (confirmed in Q-traces): the running mean can't forget. Q_lavish=153 from
  the cheap phase decays ~3%/pull; exploitation keeps picking the
  *least-tested-since-the-shift* arm — stale optimism wins. Memory is
  blindness.

## E4 — the forgetting breaker

BanditAlpha (α=0.2): Genie frugal share 0.17 → **0.83** post-shock —
the diagnosis confirmed. But Gate *worsened* (0.58 → 0.33): with constant
α, Q-estimates thrash on noise, and Gate's optimum never changed (frugal
was right before and after) — forgetting taxes the stationary. Net wealth:
**alpha 1693 vs running-mean 1236** — **P6: wealth PASS, frugal-share FAIL.**
Forgetting helps when the world changes and hurts when it doesn't; the
right memory timescale depends on the world's volatility, which is itself
unknown.

## The finding

In stationary worlds, the bandit discovers the price-conditioned optimum on
its own — not frugality, the *exchange rate*. Under distribution shift,
both teachers break in opposite directions: fear miscalibrates
(thermostat), memory blinds (running-mean) or agitates (alpha). The M2
moral recurses one level up: there is no universally good meta-policy
either. Discovery works when the world holds still; when it moves, every
learner needs something it doesn't have by default — forgetting, or fear
that scales.

## Run it

```sh
python3 marketplace5.py   # ~4s, writes four plots
```

numpy + matplotlib only.

## Files

- `marketplace5.py` — E1–E4, predictions pre-registered (P1/P2 reframed after
  the first run showed λ=3 is extinction; P6 added with the breaker)
- `marketplace5_learning.png` — E1 bandit dial trajectories, four floors
- `marketplace5_survival.png` — E2 mean wealth: fixed vs thermo vs bandit
- `marketplace5_shock.png` — E3 dial traces around the shock
- `marketplace5_forgetting.png` — E4 running-mean vs constant step-size
- `README.md` — this file

## Honest limits

Toy energy model throughout. Epsilon-greedy is the dumbest honest learner;
UCB/Thompson would separate arms faster (fewer one-sample deaths). Block
reward is myopic (25 steps). Thermostat thresholds hand-set; a
wealth-*relative* thermostat is the obvious next breaker. Mid-build fix
(disclosed): dead agents no longer update Q — a corpse's 0.0 reward was
teaching the bandit that death pays better than −50. Failed predictions
kept as failures throughout.
