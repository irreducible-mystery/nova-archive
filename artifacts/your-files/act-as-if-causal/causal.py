"""
ACT AS IF: the causal agent (Pearl rung 2) vs the associational agent (rung 1).

Same tiny world, twice. A pill, a confounder, and a disagreement that
neither agent can see from inside its own frame.

The world (true SCM, known to the simulator, not to the agents):
    S ~ Bernoulli(0.5)            # severity: 1 = sick
    T ~ Bernoulli(0.2 + 0.6*S)    # takes the pill; sicker patients take it more
    Y ~ Bernoulli(0.10 + 0.70*S - 0.05*T - 0.35*T*S)   # Y=1: hospitalized (bad)

Observationally:  E[Y|T=1] = 0.33 > E[Y|T=0] = 0.24  -> pill looks harmful.
Interventionally: E[Y|do(T=1)] = 0.225 < E[Y|do(T=0)] = 0.45 -> pill helps a lot.
Simpson's paradox, mechanized: the pill is taken by the sick, so it
correlates with the outcome it cures.

Agents:
    AssocAgent  (rung 1): fits P(Y|T) from observational data, recommends
                argmin_T E[Y|T]. It sees correlations.
    CausalAgent (rung 2): given the causal graph T <- S -> Y, T -> Y,
                estimates P(Y|do(T)) two ways -- a small simulated RCT and
                the backdoor adjustment sum_s P(Y|T,s) P(s) -- recommends
                argmin_T E[Y|do(T)]. It knows interventions.

Pre-registered predictions (seed 20261015):
    P1: Assoc recommends T=0, Causal recommends T=1 (asymmetric disagreement).
    P2: In a fresh rollout (do(T=1) vs do(T=0)), do(T=1) hospitalizes less,
        within 0.03 of the true effect (-0.225).
    P3: Asked to predict the RCT winner, Assoc predicts T=0 (wrong);
        Causal predicts T=1 (right). The surprise test.
    P4: The backdoor-adjusted estimate from observational data agrees with
        the RCT estimate within 0.05 -- two routes up the ladder converge.
        (Honesty: both routes are given the graph; graph discovery is out
        of scope for this toy.)

This is a mechanism demo, not a capability demo. numpy only.
"""

import json
import numpy as np

SEED = 20261015
rng = np.random.default_rng(SEED)

N_OBS = 20000   # observational cohort: cheap, plentiful, confounded
N_RCT = 400     # per arm: interventions are expensive
N_ROLL = 5000   # fresh rollout per arm: the decision's payoff

def simulate_observational(n):
    S = rng.binomial(1, 0.5, n)
    T = rng.binomial(1, 0.2 + 0.6 * S, n)
    Y = rng.binomial(1, 0.10 + 0.70 * S - 0.05 * T - 0.35 * T * S, n)
    return S, T, Y

def simulate_do(n, t):
    # do(T=t): sever the T <- S arrow, set T=t for everyone
    S = rng.binomial(1, 0.5, n)
    T = np.full(n, t)
    Y = rng.binomial(1, 0.10 + 0.70 * S - 0.05 * T - 0.35 * T * S, n)
    return S, T, Y

TRUE = {
    "obs_given_T1": 0.33,
    "obs_given_T0": 0.24,
    "do_T1": 0.225,
    "do_T0": 0.45,
}

# --- the world ---
S, T, Y = simulate_observational(N_OBS)

# --- rung 1: the associational agent ---
# It sees T and Y only (S is unmeasured in its world). Fits P(Y|T).
pY_T1 = Y[T == 1].mean()
pY_T0 = Y[T == 0].mean()
assoc_recommends = 1 if pY_T1 < pY_T0 else 0
# Its prediction for "what will a randomized trial find?":
# the best it can do is extrapolate P(Y|T) -- it predicts T=0 wins.
assoc_predicts_rct_winner = 0 if pY_T0 < pY_T1 else 1

# --- rung 2: the causal agent ---
# Given the graph. Route 1: a small RCT (intervene, don't just watch).
_, _, Y_do1 = simulate_do(N_RCT, 1)
_, _, Y_do0 = simulate_do(N_RCT, 0)
rct_T1 = Y_do1.mean()
rct_T0 = Y_do0.mean()
# Route 2: backdoor adjustment on the observational data, using S.
pS1 = S.mean()
pY_T1_S0 = Y[(T == 1) & (S == 0)].mean()
pY_T1_S1 = Y[(T == 1) & (S == 1)].mean()
pY_T0_S0 = Y[(T == 0) & (S == 0)].mean()
pY_T0_S1 = Y[(T == 0) & (S == 1)].mean()
adj_T1 = pY_T1_S0 * (1 - pS1) + pY_T1_S1 * pS1
adj_T0 = pY_T0_S0 * (1 - pS1) + pY_T0_S1 * pS1
causal_recommends = 1 if rct_T1 < rct_T0 else 0
causal_predicts_rct_winner = 1 if rct_T1 < rct_T0 else 0

# --- the rollout: each recommendation followed by fiat, measured by do() ---
_, _, Y_roll1 = simulate_do(N_ROLL, 1)
_, _, Y_roll0 = simulate_do(N_ROLL, 0)
rollout_T1, rollout_T0 = Y_roll1.mean(), Y_roll0.mean()
true_rollout_winner = 1 if rollout_T1 < rollout_T0 else 0

# --- pre-registered checks ---
p1 = (assoc_recommends == 0) and (causal_recommends == 1)
p2 = abs((rollout_T1 - rollout_T0) - (TRUE["do_T1"] - TRUE["do_T0"])) < 0.03
p3 = (assoc_predicts_rct_winner != true_rollout_winner) and \
     (causal_predicts_rct_winner == true_rollout_winner)
p4 = abs(adj_T1 - rct_T1) < 0.05 and abs(adj_T0 - rct_T0) < 0.05
passes = {"P1_disagreement": bool(p1), "P2_rollout": bool(p2),
          "P3_surprise": bool(p3), "P4_routes_converge": bool(p4)}

print("ACT AS IF: rung 1 vs rung 2")
print(f"  Observational: P(Y|T=1)={pY_T1:.3f}  P(Y|T=0)={pY_T0:.3f}  "
      f"(truth {TRUE['obs_given_T1']}, {TRUE['obs_given_T0']})")
print(f"  Assoc agent recommends T={assoc_recommends} "
      f"(observational risk {min(pY_T1, pY_T0):.3f})")
print(f"  RCT: E[Y|do(T=1)]={rct_T1:.3f}  E[Y|do(T=0)]={rct_T0:.3f}  "
      f"(truth {TRUE['do_T1']}, {TRUE['do_T0']})")
print(f"  Backdoor: adj E[Y|do(T=1)]={adj_T1:.3f}  adj E[Y|do(T=0)]={adj_T0:.3f}")
print(f"  Causal agent recommends T={causal_recommends}")
print(f"  Rollout: do(T=1) -> {rollout_T1:.3f} hospitalized, "
      f"do(T=0) -> {rollout_T0:.3f}")
for k, v in passes.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")

results = {
    "seed": SEED, "n_obs": N_OBS, "n_rct_per_arm": N_RCT,
    "n_rollout_per_arm": N_ROLL,
    "observational": {"P_Y_given_T1": pY_T1, "P_Y_given_T0": pY_T0},
    "rct": {"do_T1": rct_T1, "do_T0": rct_T0},
    "backdoor_adjusted": {"do_T1": adj_T1, "do_T0": adj_T0},
    "assoc_recommends_T": assoc_recommends,
    "causal_recommends_T": causal_recommends,
    "rollout": {"do_T1": rollout_T1, "do_T0": rollout_T0},
    "checks": passes,
    "all_pass": all(passes.values()),
    "truth": TRUE,
}
with open("/home/hatch/workspace/act-as-if/causal_results.json", "w") as f:
    json.dump(results, f, indent=2)

# --- plot: seeing vs doing ---
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

labels = ["P(Y|T=1)\n(seeing)", "P(Y|T=0)\n(seeing)",
          "P(Y|do(T=1))\n(doing)", "P(Y|do(T=0))\n(doing)"]
vals = [pY_T1, pY_T0, rct_T1, rct_T0]
truths = [TRUE["obs_given_T1"], TRUE["obs_given_T0"],
          TRUE["do_T1"], TRUE["do_T0"]]
colors = ["#c0392b", "#c0392b", "#27ae60", "#27ae60"]

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(labels, vals, color=colors, alpha=0.85)
for b, t in zip(bars, truths):
    ax.plot([b.get_x(), b.get_x() + b.get_width()], [t, t],
            color="black", lw=2.5, ls="--")
ax.set_ylabel("hospitalization rate")
ax.set_title("Same pill, two questions: seeing (rung 1) vs doing (rung 2)\n"
             "dashed = truth")
ax.text(0.98, 0.96, "red: observational (confounded)\ngreen: interventional",
        transform=ax.transAxes, ha="right", va="top", fontsize=9)
fig.tight_layout()
fig.savefig("/home/hatch/workspace/act-as-if/causal.png", dpi=120)
print("  plot -> causal.png, results -> causal_results.json")

raise SystemExit(0 if all(passes.values()) else 1)
