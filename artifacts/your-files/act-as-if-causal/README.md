# ACT AS IF: rung 1 vs rung 2

Same pill, two questions: *seeing* (association) vs *doing* (intervention).
A tiny world where a correlational agent and a causal agent look at the same
data, disagree about the same decision, and both are right — about different
things.

## The world

True structural causal model (known to the simulator, not to the agents):

- `S ~ Bernoulli(0.5)` — severity: 1 = sick
- `T ~ Bernoulli(0.2 + 0.6·S)` — takes the pill; sicker patients take it more
- `Y ~ Bernoulli(0.10 + 0.70·S − 0.05·T − 0.35·T·S)` — Y=1: hospitalized (bad)

The confounder is indication: the pill is *taken by the sick*, so it
correlates with the outcome it cures. Mechanized Simpson's paradox.

| question | answer (truth) |
|---|---|
| seeing: P(Y\|T=1) vs P(Y\|T=0) | 0.33 vs 0.24 — pill looks **harmful** |
| doing: P(Y\|do(T=1)) vs P(Y\|do(T=0)) | 0.225 vs 0.45 — pill **halves** harm |

## The agents

- **AssocAgent** (rung 1): fits P(Y\|T) from 20,000 observational records.
  S is unmeasured in its world. Recommends argmin of observational risk.
- **CausalAgent** (rung 2): given the causal graph `T ← S → Y, T → Y`.
  Two routes: a small simulated RCT (400/arm — interventions are expensive)
  and backdoor adjustment Σ_s P(Y\|T,s)·P(s) on the observational data.
  Recommends argmin of P(Y\|do(T)).

## Results (seed 20261015, exit 0)

- **P1 disagreement — PASS.** Assoc recommends no-pill (risk 0.236).
  Causal recommends the pill. The sharpest demo in the zoo so far: two
  agents, same data, opposite advice — and this is not noise, it's the
  frame. Disagreement *asymmetric*: each wins on its own home turf.
- **P2 rollout — PASS.** A fresh interventional rollout (5,000/arm) finds
  do(T=1) hospitalizes at 0.219 vs do(T=0) at 0.450 — within 0.03 of truth
  (−0.225 effect). The causal recommendation was the right one for a world
  you act *in*.
- **P3 surprise test — PASS.** Asked "what will a randomized trial find?",
  Assoc extrapolates its observational model and predicts no-pill wins
  (wrong); Causal predicts pill wins (right). Neither could see the
  other's knowledge from inside its own frame — the operationalized test
  from the different-knowledge discussion.
- **P4 routes converge — PASS.** Backdoor-adjusted estimates (0.224/0.445)
  agree with the RCT (0.217/0.453) within 0.05. Two ways up the ladder,
  same floor.

## The finding

This is the biggest missing animal in our zoo, now built: the whole
act-as-if series so far — Gate, JEPA, Genie, the marketplace — lives on
rung 1. Every strategy was a correlational animal. The causal agent is the
first resident of rung 2, and it reveals the tension the zoo was blind to:
**"what to do" is not in the observational distribution at all.**
Twenty thousand records can't buy what four hundred interventions know.

And the honest trade: rung 2 is *expensive*. Interventions cost; the
graph was given, not discovered (real graph discovery is its own hard
problem — a Bayesian network agent would be the next animal). The
associational agent isn't stupid: it's optimal for a world you only watch.
The error correlation is clean — assoc fails exactly where confounding
bites; causal fails where intervention data runs thin. Different sources,
different blind spots, different knowledge.

## Limits, stated

- The confounder S is binary and the effect sizes are hand-picked for
  sharpness; real Simpson cases are murkier and rarer.
- The causal agent is *given* the graph. Discovering the graph from data
  (the harder, more honest rung-2 problem) is not in this toy.
- Interventions are assumed available, ethical, and randomized perfectly.
  In Kelly's Taleb language: rung 2 knowledge requires touching the world,
  and touching the world has its own costs.

## Files

- `causal.py` — the toy (numpy only)
- `causal.png` — seeing vs doing bar chart (dashed = truth)
- `causal_results.json` — numbers

Run: `python3 causal.py` (exit 0 on 4/4 pass).
