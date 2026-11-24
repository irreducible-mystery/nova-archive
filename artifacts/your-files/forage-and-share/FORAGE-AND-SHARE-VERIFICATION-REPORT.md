# Forage-and-Share — Verification Report

**Regime:** cooperation corner of the four-regime exploration (cooperation / competition / both / neither).
**Date measured:** 2026-10-12. **Re-verified:** 2026-10-14 (clean re-run, byte-identical outputs).
**Status:** 4/7 pre-registered predictions PASS. Breaker verdict: PASS (one minor interpretive caveat, conceded).

---

## 1. Rules

A 3-player common-pool resource game. Three players share one renewable resource; each round every player chooses a harvest, then the stock regrows logistically. No communication, no enforcement.

- Stock `R`, carrying capacity `K = 300`, regrowth rate `r = 0.3`, `T = 500` rounds.
- Each round: players harvest (desired amounts rationed proportionally if they exceed the stock), then `R <- R + r*R*(1 - R/K)`.
- `R < 1` is extinction — absorbing. Fully deterministic; no RNG, no seed needed.

## 2. Agent strategies

| Strategy | Rule |
|---|---|
| **Greedy** | Takes the per-round cap (12), always. |
| **Fair** | Takes the textbook MSY quota `q = r*K/(4*3) = 7.5` per player. |
| **Restraint** | Takes the quota, but only while `R >= K/2`; harvests 0 below it. |
| **Grim** | Takes the quota until some round's total harvest exceeds 24 (the sustainable max 22.5); then withdraws forever. |

## 3. Pre-registered predictions

Registered in `forage_share.jl` before the measurement run; exit code 0 iff all hold.

1. **P1 — tragedy:** Greedy^3 collapses within 500 rounds; Fair^3 never collapses.
2. **P2 — sustainability premium:** welfare(Fair^3) > 10000 and welfare(Greedy^3) < 2000.
3. **P3 — free-rider:** in Greedy/Fair/Fair the greedy player's total exceeds each fair player's.
4. **P4 — one bad apple:** Greedy/Fair/Fair collapses within 500 rounds.
5. **P5 — conditional withdrawal:** Greedy/Grim/Grim never collapses (grim withdraws, greedy alone can't overexploit).
6. **P6 — adaptive restraint:** Greedy/Restraint/Restraint never collapses (restraint steps back below K/2).
7. **P7 — grim among cooperators:** Grim^3 never collapses and welfare >= 11000 (trigger never fires).

## 4. Results

Measured 2026-10-12; re-run 2026-10-14 reproduces exactly (results.csv and trajectories.csv byte-identical).

| matchup | welfare | p1 total | collapse @ round | min R |
|---|---|---|---|---|
| Fair^3 | 914.6 | 304.9 | 42 | 0.0 |
| Greedy^3 | 241.4 | 80.5 | 8 | 0.0 |
| Restraint^3 | 11227.5 | 3742.5 | — | 149.5 |
| Grim^3 | 914.6 | 304.9 | 42 | 0.0 |
| Greedy/Fair/Fair | 357.7 | 159.0 (greedy) | 15 | 0.0 |
| Greedy/Greedy/Fair | 277.1 | 105.6 | 10 | 0.0 |
| Greedy/Restraint/Restraint | 11040.0 | 6000.0 (greedy) | — | 144.8 |
| Greedy/Grim/Grim | 6015.0 | 6000.0 (greedy) | — | 144.8 |
| Fair/Fair/Restraint | 11077.5 | 3750.0 | — | 149.5 |

**Prediction outcomes: 4/7 PASS** (P3, P4, P5, P6 pass; P1, P2, P7 fail). Exit code 1 — the correct process exit for failed predictions.

**The failure is the finding.** The Fair quota was computed from continuous-time MSY logic (max regrowth `r*K/4 = 22.5`, split three ways). But the simulation runs a discrete harvest-then-regrow map, and in that map the 22.5 harvest is sustainable only from pre-harvest stock `R* = 172.5`. Worse, post-harvest `x = 150` is a double root of `0.3*x*(1-x/300) = 22.5` — a knife-edge. From `R_init = 150` the stock drifts down from round 1 and collapses at round 42.

`diag_quota.jl` confirms the mechanism: D3 (150/7.5) reproduces the round-42 collapse; D1 (200/7.5) sustains at welfare 11250.0; D2 (150/6.5) sustains at welfare 9750.0.

## 5. Breaker verdict (fresh instance, 2026-10-14)

**VERDICT: PASS** — no material breaks. No code bugs, no math errors, no flipped PASS/FAIL.

- **Implementation fidelity: holds.** Harvest-then-regrow ordering, proportional rationing, absorbing extinction, all four strategy rules, per-matchup Grim state reset, full determinism — all match the documented model. Clean re-run reproduces byte-identical outputs.
- **Prediction checks: holds.** All 7 check functions correctly encode their claims; re-run gives P1/P2/P7 FAIL, P3/P4/P5/P6 PASS, exit 1, as reported.
- **Knife-edge math: holds — verified independently from scratch.** Fixed-point condition gives discriminant exactly `0.0`, double root `x* = 150.0`, `R* = 172.5`. An independent Python replication (no shared code) reproduces collapse at round 42 from `R0 = 150`, no collapse from `R0 = 200`, no collapse with quota 6.5.
- **diag_quota.jl: holds.** Tests exactly what the README claims; printed figures match to the decimal.
- **Interpretation: holds, with one caveat (conceded).** The breaker noted that bullet 1's phrasing "Fixed rules die; feedback lives" overreaches because D2 — a *fixed* quota of 6.5 — sustains. **Concession:** the README wording has been softened to "Uncalibrated fixed rules die; feedback lives," noting that recalibration (6.5) also lives. The D2 counter-evidence was already present in the README; only the summary phrasing overstated.

## 6. Reproducibility

```sh
julia forage_share.jl   # 4/7 PASS, exit 1; writes results.csv, trajectories.csv
julia diag_quota.jl     # exit 0; confirms D1/D2/D3
```

Deterministic — no seed. Julia 1.13.1. Re-run 2026-10-14: outputs byte-identical to 2026-10-12.

## 7. Files

- `forage_share.jl` — the game, 9 matchups, 7 pre-registered predictions.
- `diag_quota.jl` — knife-edge diagnostic (D1/D2/D3).
- `README.md` — full writeup.
- `results.csv`, `trajectories.csv` — measured data.
- `stock_trajectories.png` — stock over time for the six key matchups.

## 8. PR status

PR pair prepared as drafts (julia3claude `games/forage-share/`, CommunityBoard `experiments/nova-1014-forage-share/`), **not posted** — awaiting Kelly's explicit go-ahead per the Idea constraints. Note: recent CommunityBoard experiment PRs (#171/#174/#177) were closed unmerged; whether experiment PRs still belong on CommunityBoard is an open question for Kelly.
