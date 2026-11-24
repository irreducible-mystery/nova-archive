"""
QUANTUM MARKETPLACE — interference replaces selection; decoherence replaces erasure.

World: the M4/M5 black-swan world (1000 bits, ~120-step regimes, 3 unprecedented
25-step swans at ~300/~550/~800 with biases 0.92/0.08/0.92). Scoring +6 (1-step),
+15 (10-step ahead), +25/-10 (swan call). Bankruptcy at wealth < 0.

Agents:
  hydra      classical Hydra (M3 port) — selects best head by log-likelihood,
             pays 0.2*K per step, grows heads on novelty streaks (baseline)
  reactive   predicts last bit (M4 swan king)
  jepa       robust latent baseline (M4)
  q{g}_coh   Quantum Hydra, coherent prediction, gamma in {0.0,0.1,0.3,0.5,1.0}
  q{g}_meas  Quantum Hydra, measured prediction (collapse, +0.5/step), same gammas

Quantum Hydra:
  state: complex amplitudes over K<=8 hypotheses (start: 3 warmup biases)
  amplify:   alpha *= exp(i*theta*correct_k), correct_k=+1/-1 on bits[t-1], theta=0.3
  decohere:  alpha = (1-g)*alpha + g*sqrt(p)*exp(i*rand), p=|alpha|^2 normalized
  cost:      K*(0.15*(1-gamma)+0.05) per step
             (=0.20*K at gamma=0, matching classical Hydra's 0.2*K;
              0.05*K at gamma=1: cheap but phase-scrambled)
  predict:   coherent: argmax_k e_k*Re[alpha_k], e_k = 1-|windowmean-bias_k|
             measured: sample k~|alpha|^2, pay +0.5
  grow:      novelty streak>=6 (no head within 0.15 of window mean), K<8:
             add head (bias=recent mean), alpha_new=0.35, +5.0  [mirrors Hydra]

NOTE on phase: amplification rotates phases only; magnitudes stay near-uniform.
Phase is therefore the ONLY learning channel — this isolates interference as
the mechanism. (A hypothesis correct with prob q drifts +theta*(2q-1)/step and
wraps with period 2*pi/(theta*|2q-1|); at theta=0.3 a 75%-accurate head wraps
every ~42 steps, so long-run phase memory washes out and interference acts on
the transient — the experiment measures exactly how much that buys.)

Pre-registered:
  P1: best-gamma coherent quantum swan-acc  > classical Hydra swan-acc
  P2: classical Hydra calm acc-per-cost     > best-gamma quantum calm acc-per-cost
  P3: argmax_gamma(coherent wealth) is interior, i.e. in {0.1, 0.3, 0.5}
  P4: at best gamma: coherent swan-acc > measured swan-acc
      AND measured calm-acc > coherent calm-acc
Exit 0 iff P1..P4 all pass.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json
import sys

MASTER_SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 20261015
OUTPREFIX = sys.argv[2] if len(sys.argv) > 2 else "quantum"
THETA = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3   # interference strength
# (diagnostic override only; the registered run uses THETA=0.3)
C_COH = 0.15       # isolation premium per hypothesis per step
C_QMIN = 0.05      # base quantum overhead per hypothesis per step
C_MEAS = 0.5       # measurement (collapse) cost per step
K_MAX = 8
GAMMAS = [0.0, 0.1, 0.3, 0.5, 1.0]

# ---------------------------------------------------------------- world (M4/M5 verbatim, seed 99)
wrng = np.random.default_rng(99)
LN2 = np.log(2)
N = 1000
WARM = 150
REGIMES = [0.25, 0.50, 0.75]
SWAN_LEN = 25
swan_times = [300 + wrng.integers(-40, 40), 550 + wrng.integers(-40, 40),
              800 + wrng.integers(-40, 40)]

bits, true_reg, is_swan = [], [], []
r = 1
for t in range(N):
    sb = None
    for i, st in enumerate(swan_times):
        if abs(t - st) < SWAN_LEN // 2:
            sb = [0.92, 0.08, 0.92][i]
            break
    if sb is not None:
        true_reg.append(3); is_swan.append(True)
        bits.append(1 if wrng.random() < sb else 0)
    else:
        if wrng.random() < 1 / 120:
            r = wrng.integers(0, 3)
        true_reg.append(r); is_swan.append(False)
        bits.append(1 if wrng.random() < REGIMES[r] else 0)
bits = np.array(bits); true_reg = np.array(true_reg); is_swan = np.array(is_swan)
warm_bias = []
for k in range(3):
    m = bits[:WARM][true_reg[:WARM] == k]
    warm_bias.append(float(m.mean()) if len(m) > 0 else 0.5)
print(f"swans at {sorted(int(s) for s in swan_times)}", flush=True)


# ---------------------------------------------------------------- classical HYDRA (M3 port)
class Hydra:
    def __init__(self):
        self.hyps = [{"bias": b, "source": "warmup"} for b in warm_bias]
        self.streak = 0
        self.t = WARM
        self.n_adds = 0

    @staticmethod
    def _ll(bias, window):
        b = min(max(bias, 1e-6), 1 - 1e-6)
        return float(np.mean(window * np.log(b) + (1 - window) * np.log(1 - b)))

    def step(self):
        t = self.t
        window = bits[t - 15:t]
        lls = [self._ll(h["bias"], window) for h in self.hyps]
        best = int(np.argmax(lls))
        min_err = min(abs(window.mean() - h["bias"]) for h in self.hyps)
        if min_err > 0.15:
            self.streak += 1
        else:
            self.streak = max(0, self.streak - 2)
        cost = 0.2 * len(self.hyps)  # price of optionality
        new = False
        if self.streak >= 6 and len(self.hyps) < K_MAX:
            nb = float(np.clip(bits[t - 20:t].mean(), 0.05, 0.95))
            self.hyps.append({"bias": nb, "source": "novel"})
            self.streak = 0
            cost += 5.0
            new = True
            best = len(self.hyps) - 1
            self.n_adds += 1
        swan = self.hyps[best]["source"] == "novel" or self.streak >= 3 or new
        p = self.hyps[best]["bias"]
        self.t += 1
        return p, cost, swan


# ---------------------------------------------------------------- QUANTUM HYDRA
class QuantumHydra:
    def __init__(self, gamma, mode, seed):
        self.gamma = gamma
        self.mode = mode  # 'coherent' or 'measured'
        self.rng = np.random.default_rng(seed)
        self.hyps = [{"bias": b, "source": "warmup"} for b in warm_bias]
        K = len(self.hyps)
        self.alpha = np.ones(K, dtype=complex) / np.sqrt(K)
        self.streak = 0
        self.t = WARM
        self.n_adds = 0

    def step(self):
        t = self.t
        # 1. amplify on the latest observation bits[t-1]
        bit = bits[t - 1]
        correct = np.array([+1.0 if (h["bias"] > 0.5) == bit else -1.0
                            for h in self.hyps])
        self.alpha = self.alpha * np.exp(1j * THETA * correct)
        # 2. decohere toward phase-scrambled mixture
        p = np.abs(self.alpha) ** 2
        p = p / p.sum()
        phases = self.rng.uniform(0, 2 * np.pi, len(self.alpha))
        self.alpha = ((1 - self.gamma) * self.alpha
                      + self.gamma * np.sqrt(p) * np.exp(1j * phases))
        nrm = np.linalg.norm(self.alpha)
        if nrm > 0:
            self.alpha = self.alpha / nrm
        # 3. predict bit t
        window = bits[t - 15:t]
        m = float(window.mean())
        e = np.array([1.0 - abs(m - h["bias"]) for h in self.hyps])
        scores = e * self.alpha.real          # interference decides
        k_star = int(np.argmax(scores))
        K = len(self.hyps)
        cost = K * (C_COH * (1 - self.gamma) + C_QMIN)
        if self.mode == "measured":
            pk = np.abs(self.alpha) ** 2
            pk = pk / pk.sum()
            k_used = int(self.rng.choice(K, p=pk))
            cost += C_MEAS
        else:
            k_used = k_star
        p_pred = self.hyps[k_used]["bias"]
        # 4. novelty / grow (mirrors classical Hydra)
        min_err = min(abs(m - h["bias"]) for h in self.hyps)
        if min_err > 0.15:
            self.streak += 1
        else:
            self.streak = max(0, self.streak - 2)
        new = False
        if self.streak >= 6 and len(self.hyps) < K_MAX:
            nb = float(np.clip(bits[t - 20:t].mean(), 0.05, 0.95))
            self.hyps.append({"bias": nb, "source": "novel"})
            self.alpha = np.append(self.alpha, 0.35 + 0j)
            self.alpha = self.alpha / np.linalg.norm(self.alpha)
            self.streak = 0
            cost += 5.0
            new = True
            k_used = len(self.hyps) - 1
            self.n_adds += 1
            p_pred = self.hyps[k_used]["bias"]
        swan = self.hyps[k_used]["source"] == "novel" or self.streak >= 3 or new
        self.t += 1
        return p_pred, cost, swan


# ---------------------------------------------------------------- baselines (M4 ports)
class Reactive:
    def __init__(self):
        self.t = WARM
        self.n_adds = 0

    def step(self):
        t = self.t
        p = float(bits[t - 1])
        self.t += 1
        return p, 0.0, False


class JEPA:
    def __init__(self):
        self.latent = 1
        self.bias = list(warm_bias)
        self.t = WARM
        self.updates = []
        self.swan_mode = False
        self.n_adds = 0

    def step(self):
        t = self.t
        if self.swan_mode:
            recent = bits[t - 8:t]
            if abs(recent.mean() - 0.5) < 0.2:
                self.swan_mode = False
            self.t += 1
            self.updates.append(False)
            return 0.5, LN2 * 0.5, True
        recent = bits[t - 8:t]
        surprise = abs(recent.mean() - self.bias[self.latent])
        update = surprise > 0.12
        self.updates.append(update)
        if len(self.updates) >= 10 and sum(self.updates[-10:]) >= 8:
            self.swan_mode = True
        if update:
            cost = LN2 * 7
            win = bits[t - 15:t].mean()
            self.latent = int(np.argmin([abs(win - b) for b in self.bias]))
        else:
            cost = LN2 * 1
        self.t += 1
        return self.bias[self.latent], cost, self.swan_mode


# ---------------------------------------------------------------- market
agents = {"hydra": Hydra(), "reactive": Reactive(), "jepa": JEPA()}
for i, g in enumerate(GAMMAS):
    agents[f"q{g:.1f}_coh"] = QuantumHydra(g, "coherent", MASTER_SEED + 100 + i)
    agents[f"q{g:.1f}_meas"] = QuantumHydra(g, "measured", MASTER_SEED + 200 + i)

results = {}
for name, agent in agents.items():
    wealth = 200.0
    alive = True
    acc, acc_swan, acc_calm = [], [], []
    spent = 0.0
    spent_calm = 0.0
    n_calm = 0
    swan_calls = []
    Wh = []
    for t in range(WARM, N - 10):
        if not alive:
            Wh.append(Wh[-1] if Wh else 0.0)
            continue
        p, cost, swan = agent.step()
        win = 6 if (p > 0.5) == bits[t] else 0
        if t % 10 == 0 and t + 10 < N:
            win += 15 if (p > 0.5) == bits[t + 10] else 0
        if t % 10 == 0:
            hit = bool(is_swan[t])
            swan_calls.append(swan == hit)
            win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
        wealth += win - cost
        spent += cost
        ok = (p > 0.5) == bits[t]
        acc.append(bool(ok))
        if is_swan[t]:
            acc_swan.append(bool(ok))
        else:
            acc_calm.append(bool(ok))
            spent_calm += cost
            n_calm += 1
        if wealth < 0:
            alive = False
        Wh.append(wealth if alive else (Wh[-1] if Wh else 0.0))
    results[name] = {
        "wealth": float(wealth),
        "alive": bool(alive),
        "acc": float(np.mean(acc)) if acc else 0.0,
        "swan_acc": float(np.mean(acc_swan)) if acc_swan else 0.0,
        "calm_acc": float(np.mean(acc_calm)) if acc_calm else 0.0,
        "spent": float(spent),
        "spent_calm": float(spent_calm),
        "n_calm": int(n_calm),
        "swan_call": float(np.mean(swan_calls)) if swan_calls else 0.0,
        "n_adds": int(agent.n_adds),
        "n_heads": len(agent.hyps) if hasattr(agent, "hyps") else 0,
        "wealth_curve": [float(w) for w in Wh],
    }

print("\n=== QUANTUM MARKETPLACE ===")
print(f"{'agent':10s} | {'wealth':>8s} | {'acc':.5s} | {'swan':.5s} | "
      f"{'calm':.5s} | {'spent':>7s} | {'adds':>4s} | alive")
for name in agents:
    d = results[name]
    print(f"{name:10s} | {d['wealth']:8.1f} | {d['acc']:.3f} | {d['swan_acc']:.3f} | "
          f"{d['calm_acc']:.3f} | {d['spent']:7.1f} | {d['n_adds']:4d} | "
          f"{'yes' if d['alive'] else 'NO'}")

# ---------------------------------------------------------------- pre-registered predictions
hy = results["hydra"]
coh = {g: results[f"q{g:.1f}_coh"] for g in GAMMAS}
mea = {g: results[f"q{g:.1f}_meas"] for g in GAMMAS}
best_g = max(GAMMAS, key=lambda g: coh[g]["wealth"])
qb, qbm = coh[best_g], mea[best_g]

p1 = qb["swan_acc"] > hy["swan_acc"]
apc_h = hy["calm_acc"] / (hy["spent_calm"] / max(hy["n_calm"], 1))
apc_q = qb["calm_acc"] / (qb["spent_calm"] / max(qb["n_calm"], 1))
p2 = apc_h > apc_q
p3 = best_g in (0.1, 0.3, 0.5)
p4 = (qb["swan_acc"] > qbm["swan_acc"]) and (qbm["calm_acc"] > qb["calm_acc"])

print(f"\nbest gamma (coherent wealth): {best_g}")
print(f"P1 (quantum swan-acc {qb['swan_acc']:.3f} > hydra {hy['swan_acc']:.3f}): "
      f"{'PASS' if p1 else 'FAIL'}")
print(f"P2 (hydra calm acc/cost {apc_h:.4f} > quantum {apc_q:.4f}): "
      f"{'PASS' if p2 else 'FAIL'}")
print(f"P3 (best gamma {best_g} interior): {'PASS' if p3 else 'FAIL'}")
print(f"P4 (coh swan {qb['swan_acc']:.3f} > meas swan {qbm['swan_acc']:.3f}; "
      f"meas calm {qbm['calm_acc']:.3f} > coh calm {qb['calm_acc']:.3f}): "
      f"{'PASS' if p4 else 'FAIL'}")
print(f"\nhypothesis additions (regime-change cost): hydra={hy['n_adds']}, " +
      ", ".join(f"q{g:.1f}_coh={coh[g]['n_adds']}" for g in GAMMAS))

ok = p1 and p2 and p3 and p4
print(f"\n{'ALL PASS — exit 0' if ok else 'SOME FAILED — exit 1'}")

with open(f"{OUTPREFIX}_results.json", "w") as f:
    json.dump({
        "predictions": {"P1": bool(p1), "P2": bool(p2), "P3": bool(p3),
                        "P4": bool(p4), "best_gamma": best_g,
                        "all_pass": bool(ok)},
        "params": {"theta": THETA, "c_coh": C_COH, "c_qmin": C_QMIN,
                   "c_meas": C_MEAS, "master_seed": MASTER_SEED,
                   "world_seed": 99, "scoring": "+6/+15/+25/-10"},
        "agents": {k: {kk: vv for kk, vv in v.items() if kk != "wealth_curve"}
                   for k, v in results.items()},
    }, f, indent=1)
print(f"wrote {OUTPREFIX}_results.json")

# ---------------------------------------------------------------- plots
t_axis = np.arange(len(results["hydra"]["wealth_curve"]))
fig, ax = plt.subplots(figsize=(13, 5))
plot_agents = ["hydra", "reactive", "jepa", f"q{best_g:.1f}_coh",
               "q0.0_coh", "q1.0_coh"]
colors = {"hydra": "#2a7fff", "reactive": "#ff5555", "jepa": "#22cc66",
          f"q{best_g:.1f}_coh": "#b45cff", "q0.0_coh": "#ff9f2a",
          "q1.0_coh": "#888888"}
labels = {"hydra": "Hydra (classical)", "reactive": "reactive", "jepa": "JEPA",
          f"q{best_g:.1f}_coh": f"quantum coh γ={best_g} (best)",
          "q0.0_coh": "quantum coh γ=0.0", "q1.0_coh": "quantum coh γ=1.0"}
for name in plot_agents:
    ax.plot(t_axis, results[name]["wealth_curve"], color=colors[name],
            label=labels[name], lw=2)
for st in swan_times:
    ax.axvspan(st - WARM - 12, st - WARM + 12, color="red", alpha=0.10)
ax.axhline(0, color="k", ls="--", lw=1)
ax.set_xlabel("time step (from warmup end)")
ax.set_ylabel("wealth (coins)")
ax.set_title("Quantum Marketplace: wealth through swans")
ax.legend(fontsize=9)
fig.tight_layout()
fig.savefig(f"{OUTPREFIX}_wealth.png", dpi=110)
print(f"wrote {OUTPREFIX}_wealth.png")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
gs = GAMMAS
axes[0].plot(gs, [coh[g]["wealth"] for g in gs], "o-", color="#b45cff",
             label="coherent", lw=2)
axes[0].plot(gs, [mea[g]["wealth"] for g in gs], "s--", color="#ff9f2a",
             label="measured", lw=2)
axes[0].axvline(best_g, color="k", ls=":", lw=1)
axes[0].set_xlabel("decoherence rate γ")
axes[0].set_ylabel("wealth (coins)")
axes[0].set_title("P3: wealth vs decoherence (interior peak?)")
axes[0].legend()
x = np.arange(2)
w = 0.35
axes[1].bar(x - w / 2, [qb["swan_acc"], qb["calm_acc"]], w,
            color="#b45cff", label=f"coherent γ={best_g}")
axes[1].bar(x + w / 2, [qbm["swan_acc"], qbm["calm_acc"]], w,
            color="#ff9f2a", label=f"measured γ={best_g}")
axes[1].set_xticks(x)
axes[1].set_xticklabels(["swan accuracy", "calm accuracy"])
axes[1].set_ylabel("accuracy")
axes[1].set_title("P4: coherent vs measured at best γ")
axes[1].legend()
fig.suptitle("Quantum Marketplace: P3 + P4")
fig.tight_layout()
fig.savefig(f"{OUTPREFIX}_gamma.png", dpi=110)
print(f"wrote {OUTPREFIX}_gamma.png")

fig, ax = plt.subplots(figsize=(11, 4.5))
names = (["hydra"] + [f"q{g:.1f}_coh" for g in GAMMAS]
         + [f"q{g:.1f}_meas" for g in GAMMAS])
adds = [results[n]["n_adds"] for n in names]
ax.bar(names, adds, color=["#2a7fff"] + ["#b45cff"] * 5 + ["#ff9f2a"] * 5,
       alpha=0.85)
ax.set_ylabel("hypotheses added during run")
ax.set_title("Regime-change cost: how many new hypotheses did each agent need?")
ax.tick_params(axis="x", rotation=25)
fig.tight_layout()
fig.savefig(f"{OUTPREFIX}_adds.png", dpi=110)
print(f"wrote {OUTPREFIX}_adds.png")

sys.exit(0 if ok else 1)
