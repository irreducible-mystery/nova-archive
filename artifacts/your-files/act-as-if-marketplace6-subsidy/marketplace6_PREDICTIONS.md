# Marketplace VI: subsidy floor — pre-registered predictions
Written BEFORE any run. 2026-10-16 ~03:10 UTC (2026-10-15 20:10 PDT).

## Design
Same world as M5 (seed 99, same 11 animals, same bit stream, same swan timing),
one change: the commons subsidizes information spend.

    wealth[k] += win - cost + SUB * cost

SUB = fraction of each animal's cost the commons rebates every step.
SUB=0.0 reproduces M5 exactly. Runs: SUB=0.5 (half subsidy), SUB=1.0 (full subsidy).

Question: does a commons that subsidizes contradiction-holders rescue the
paraconsistent animal — and what else gets rescued with it?

M5 facts (reproduced 2026-10-16 ~03:08 UTC, rankings byte-match the record):
  paraconsistent: spent 1362.0, wealth -2.0, DEAD, swan-acc 0.870 (best reader in zoo)
  gate:           spent 1531.7 (biggest spender), wealth 1451.3, rank 10/11
  mimetic:        spent  168.0, wealth 3872.0, rank 1
  reactive:       spent    0.0, wealth 3530.0, rank 2

## Predictions
- P1: paraconsistent ALIVE at SUB=1.0. (Direct test. +1362 rebate vs -2.0 wealth.)
- P2: paraconsistent swan-acc >= 0.80 at SUB=1.0. (M5: 0.870; accuracy is
  subsidy-independent — subsidy changes wealth, not skill.)
- P3: gate rank <= 7 at SUB=1.0 (M5: 10th). Mechanism: +1531.7 is the largest
  absolute transfer. Subsidy is blind — it pays spend, not value.
- P4: gate swan-acc < paraconsistent swan-acc at SUB=1.0. (Skill unchanged.)
- P5: paraconsistent DEAD at SUB=0.5. (Dose-dependence: 681 rebate < 1362 bleed.)
- P6: paraconsistent not last at SUB=1.0 (escapes the M5 floor).
