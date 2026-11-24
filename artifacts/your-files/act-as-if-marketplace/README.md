# THE MARKETPLACE — the zoo under one thermodynamic budget

An "act as if" simulation. Not the models — the *economics*, at a scale
where you can watch the coins move.

## What it is

The Gate forgot for free. JEPA refused for free. Genie dreamed for free.
Nothing is free. Every erased bit costs kT ln 2 (Landauer). This puts all
three under one energy budget — 120 coins each — on the same 600-bit
3-regime Markov stream, and measures who survives scarcity.

Costs (coins = bit-erasures):
- **Gate:** ln2 × state-overwrite per step. Opening the gate wide *destroys*
  old state — selectivity is now an economic decision, not a free lunch.
- **JEPA:** ln2×6 per encoder update, ln2×1 to coast on its last latent.
  Surprise triggers recomputation; calm is free.
- **Genie:** 1.2 per dreamed step + 1.0 upkeep. Depth costs; futures pay.

Earnings: +6 next-bit, +6 futures (t+3, Genie's niche), +15 regime calls
every 10 steps (JEPA's niche).

## What happened

**The market (fixed normal dials):** Gate wins (wealth 1201), then JEPA
(931), then Genie (641). But JEPA is the most *accurate* (0.590 vs 0.565).
Under scarcity, the most efficient wins — not the most accurate.

**The Pareto sweep:** frugality *dominates* everywhere. Gate at sharp
selectivity is both cheaper AND more accurate than lavish. JEPA coasting
gets identical accuracy for less energy — refusal is free. Genie depth
doesn't improve next-bit at all (Markov stream; dreaming far doesn't help
predict near).

**Exchange rates (accuracy per 100 coins):** Gate 30.1 > JEPA 19.9 > Genie
16.9.

## The finding

The currency converter exists and it's measurable. But it's task-relative:
this stream rewards recency and selectivity (the Gate's home turf). A
long-horizon or high-noise task would reprices everything — JEPA's refusal
and Genie's dreaming buy different things. The marketplace doesn't crown a
universal winner; it prices strategies per task. That's the point: the
exchange rate is real, and it's *conditional*.

## Run it

```sh
python3 marketplace.py   # market + Pareto sweep, writes two plots
```

Fast (~2s). numpy + matplotlib only.

## Files

- `marketplace.py` — stream, three traders, market, Pareto sweep
- `marketplace.png` — wealth trajectories
- `pareto.png` — accuracy vs energy per dial
- `README.md` — this file

## Honest limits

Toy energy model — "bits erased" estimated from mechanism, not measured in
silicon. The tradeoff *structure* (selectivity costs, coasting saves,
dreaming spends) is what's real. Absolute coin values are illustrative;
the dominance patterns (frugal wins, efficiency beats accuracy) are robust
to repricing.
