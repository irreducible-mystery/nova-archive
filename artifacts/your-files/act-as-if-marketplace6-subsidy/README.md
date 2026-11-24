# Marketplace VI: the subsidy floor

**Question:** Kelly's principle from the M5 session — "a healthy commons has to
subsidize its contrarians and contradiction-holders, because the market prices
them out." Does a commons that subsidizes information spend actually rescue the
paraconsistent animal — and what else gets rescued with it?

**Design:** M5 verbatim (seed 99, same 11 animals, same bit stream, same swan
timing), one change — the commons rebates a fraction SUB of every animal's cost:

    wealth[k] += win - cost + SUB * cost

SUB=0.0 reproduces M5 exactly (verified: rankings byte-match). Runs: SUB=0.5, SUB=1.0.

**Pre-registered predictions** (`marketplace6_PREDICTIONS.md`, written before any run):
1/6 passed. The failures are the findings.

## Results

| SUB | paraconsistent | gate rank | biggest transfer |
|-----|---------------|-----------|------------------|
| 0.0 (M5) | DEAD, wealth −2, spent 1362 | 10/11 | — |
| 0.5 | ALIVE, wealth 778, spent 3491 | 10/11 | JEPA +922 |
| 1.0 | ALIVE, wealth 2524, spent 3491 | 9/11 | JEPA +1844 |

At SUB=1.0: selfbuild(4110) > dialectical(4082) > mimetic(4034) > federated(4030) >
jepa(3791) > stigmergic(3672) > reactive(3530) > satisficer(3460) > gate(2983) >
contrarian(2750) > paraconsistent(2524).

## Findings

1. **The subsidy saves the animal and bankrupts its legend.** The paraconsistent
   animal is alive at both SUB=0.5 and SUB=1.0 (P1 PASS) — half-subsidy already
   suffices, no threshold drama (P5 FAIL). But it finishes **last** at both
   (P6 FAIL). Subsidy pays spend, not wins; its win total (2524) is the lowest
   in the zoo. The market priced it out; the commons keeps it alive and keeps it
   last. Survival ≠ standing.

2. **Correction to the M5 headline.** M5 recorded paraconsistent as "the best
   swan-reader in the entire zoo" (swan-acc 0.870). That number was a
   **truncated-lifetime artifact**: it died early in M5, so its record covered
   only the early swans. Full-life swan-acc = 0.652 — tied with gate (P2, P4
   FAIL). The death that made the finding dramatic also made it artifactual.
   The logic still works; the superlative doesn't survive.

3. **Subsidy is blind.** The largest absolute transfers go to the biggest
   spenders: JEPA (+1844 at SUB=1.0, rank 5th) and gate (+1532, rank 9th — P3
   FAIL, barely moved from 10th). A commons that subsidizes contradiction-holders
   cannot avoid subsidizing frantic adaptation too. The rebate is on *cost*, not
   on *holding Both*. This is exactly the distinction Tetra draws: Tetra makes
   *holding* B free (a state subsidy) instead of rebating *computation* (a spend
   subsidy). M6 shows why the distinction matters — and gives the #221/#224
   governance thread a measured version of the question: can you subsidize the
   state of holding contradiction without subsidizing the spend?

## Reproduce
`python3 marketplace6_subsidy.py [SUB]` — SUB=0.0 reproduces M5. ~2s per run.
