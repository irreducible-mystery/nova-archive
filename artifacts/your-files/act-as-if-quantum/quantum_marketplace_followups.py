"""
QUANTUM MARKETPLACE FOLLOW-UPS (2026-10-16)

Two pre-registered follow-ups to the quantum marketplace experiment
(quantum_marketplace.py: exit 1, 0/4 predictions).

World: the M4/M5 black-swan world verbatim (seed 99): 1000 bits, ~120-step
regimes, 3 unprecedented 25-step swans at ~300/~550/~800 with biases
0.92/0.08/0.92. Scoring +6 (1-step), +15 (10-step ahead), +25/-10 (swan call).
Bankruptcy at wealth < 0.

Follow-up 1 — theta sweep (constant rotation):
  The wrap analysis predicts an interior optimum near theta~0.1: a 75%-accurate
  head drifts in phase at theta*(2q-1)/step and wraps with period
  2*pi/(theta*|2q-1|); at theta=0.1 that period is ~126 steps ~= regime length,
  so phases build persistent alignment inside a regime instead of wrapping.
  Sweep theta in {0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5} at gamma=0.0 coherent.
  P1: argmax_theta(swan_acc) is interior, i.e. in {0.05, 0.1, 0.15, 0.2, 0.3}
      (not at the endpoints 0 or 0.5).
  P2: theta=0 exactly recovers classical Hydra (swan_acc, calm_acc, wealth).

Follow-up 2 — persistent-memory variant (rotate-toward-fixed-point):
  Replace constant rotation alpha *= exp(i*theta*correct) with a pull of each
  head's phase toward a fixed target: 0 if the head was correct on the last
  bit, pi if wrong, with pull strength kappa:
      phi_k <- phi_k + kappa * wrap01(target_k - phi_k)
  Magnitudes are untouched, so phase remains the only learning channel and
  interference remains the isolated mechanism.
  NOTE (documented deviation): the pull REPLACES constant rotation — there is
  no theta in this variant. The task spec's "theta=0.1" is read as naming the
  base configuration (gamma=0.0, coherent) under which the kappa sweep runs;
  the kappa sweep is the direct analog of the theta sweep. kappa in
  {0, 0.1, 0.3, 0.5, 1.0}; kappa=0 is a control (no phase motion at all ->
  classical recovery, like theta=0).
  This is the economic analogue of the M6 subsidy: phases give hypotheses
  persistent memory across regime flips — persistence, not just cheap holding.
  P3: best-kappa (kappa>0) pull variant swan_acc > best-theta constant-rotation
      swan_acc (strict comparison; deterministic at gamma=0, so no noise).
  P4: best-kappa pull swan_acc >= hydra swan_acc - 0.01 ("matches or beats";
      0.01 ~= 1 swan-step out of 75, the operational reading of "matches").

Seeds: master seeds [20261015, 7, 77]. At gamma=0 coherent every quantum
variant is deterministic (the rng draws are multiplied by gamma=0 or unused),
so seed-invariance is verified empirically, not assumed.

Exit 0 iff P1..P4 all pass.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json
import sys
import os

SEEDS = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [20261015, 7, 77]
OUTDIR = sys.argv[4] if len(sys.argv) > 4 else os.path.expanduser(
    "~/workspace/your_files/act-as-if-quantum")

THETAS = [0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5]
KAPPAS = [0.0, 0.1, 0.3, 0.5, 1.0]
C_COH = 0.15       # isolation premium per hypothesis per step (gamma=0 -> 0.2K)
C_QMIN = 0.05
K_MAX = 8
GAMMA = 0.0        # follow-ups run at the registered best base config

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


# ---------------------------------------------------------------- classical HYDRA (M3 port, verbatim)
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
        cost = 0.2 * len(self.hyps)
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


# ---------------------------------------------------------------- QUANTUM HYDRA (follow-up: const rotation OR pull)
class QuantumHydra2:
    def __init__(self, theta, kappa, pull, seed):
        self.theta = theta    # constant-rotation strength (pull=False)
        self.kappa = kappa    # pull strength (pull=True)
        self.pull = pull
        self.gamma = GAMMA
        self.rng = np.random.default_rng(seed)
        self.hyps = [{"bias": b, "source": "warmup"} for b in warm_bias]
        K = len(self.hyps)
        self.alpha = np.ones(K, dtype=complex) / np.sqrt(K)
        self.streak = 0
        self.t = WARM
        self.n_adds = 0

    def step(self):
        t = self.t
        # 1. phase update on the latest observation bits[t-1]
        bit = bits[t - 1]
        correct = np.array([+1.0 if (h["bias"] > 0.5) == bit else -1.0
                            for h in self.hyps])
        if self.pull:
            # rotate-toward-fixed-point: correct -> phase 0, wrong -> phase pi
            mag = np.abs(self.alpha)
            phi = np.angle(self.alpha)
            target = np.where(correct > 0, 0.0, np.pi)
            d = (target - phi + np.pi) % (2 * np.pi) - np.pi
            phi = phi + self.kappa * d
            self.alpha = mag * np.exp(1j * phi)
        else:
            # constant rotation (original dynamics)
            self.alpha = self.alpha * np.exp(1j * self.theta * correct)
        # 2. decohere (identity at gamma=0; kept for structural fidelity)
        p = np.abs(self.alpha) ** 2
        p = p / p.sum()
        phases = self.rng.uniform(0, 2 * np.pi, len(self.alpha))
        self.alpha = ((1 - self.gamma) * self.alpha
                      + self.gamma * np.sqrt(p) * np.exp(1j * phases))
        nrm = np.linalg.norm(self.alpha)
        if nrm > 0:
            self.alpha = self.alpha / nrm
        # 3. predict bit t (coherent: interference decides)
        window = bits[t - 15:t]
        m = float(window.mean())
        e = np.array([1.0 - abs(m - h["bias"]) for h in self.hyps])
        scores = e * self.alpha.real
        k_star = int(np.argmax(scores))
        K = len(self.hyps)
        cost = K * (C_COH * (1 - self.gamma) + C_QMIN)
        p_pred = self.hyps[k_star]["bias"]
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
            self.alpha = np.append(self.alpha, 0.35 + 0j)  # phase 0: presumed correct
            self.alpha = self.alpha / np.linalg.norm(self.alpha)
            self.streak = 0
            cost += 5.0
            new = True
            k_star = len(self.hyps) - 1
            self.n_adds += 1
            p_pred = self.hyps[k_star]["bias"]
        swan = self.hyps[k_star]["source"] == "novel" or self.streak >= 3 or new
        self.t += 1
        return p_pred, cost, swan


# ---------------------------------------------------------------- market
def run_market(master_seed):
    agents = {"hydra": Hydra()}
    for i, th in enumerate(THETAS):
        agents[f"th{th:.2f}"] = QuantumHydra2(theta=th, kappa=0.0, pull=False,
                                             seed=master_seed + 1000 + i)
    for i, ka in enumerate(KAPPAS):
        agents[f"pull{ka:.1f}"] = QuantumHydra2(theta=0.0, kappa=ka, pull=True,
                                               seed=master_seed + 2000 + i)
    results = {}
    for name, agent in agents.items():
        wealth = 200.0
        alive = True
        acc, acc_swan, acc_calm = [], [], []
        spent = 0.0
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
            "swan_call": float(np.mean(swan_calls)) if swan_calls else 0.0,
            "n_adds": int(agent.n_adds),
            "n_heads": len(agent.hyps) if hasattr(agent, "hyps") else 0,
            "wealth_curve": [float(w) for w in Wh],
        }
    return results


all_results = {}
for s in SEEDS:
    print(f"--- seed {s} ---", flush=True)
    all_results[s] = run_market(s)

R = all_results[SEEDS[0]]
th_names = [f"th{th:.2f}" for th in THETAS]
pu_names = [f"pull{ka:.1f}" for ka in KAPPAS]
hy = R["hydra"]

print("\n=== FOLLOW-UP 1: theta sweep (gamma=0, coherent) ===")
print(f"{'agent':8s} | {'wealth':>8s} | {'acc':.5s} | {'swan':.5s} | "
      f"{'calm':.5s} | {'adds':>4s}")
for n in ["hydra"] + th_names:
    d = R[n]
    print(f"{n:8s} | {d['wealth']:8.1f} | {d['acc']:.3f} | {d['swan_acc']:.3f} | "
          f"{d['calm_acc']:.3f} | {d['n_adds']:4d}")

print("\n=== FOLLOW-UP 2: pull (persistent memory) sweep ===")
print(f"{'agent':8s} | {'wealth':>8s} | {'acc':.5s} | {'swan':.5s} | "
      f"{'calm':.5s} | {'adds':>4s}")
for n in pu_names:
    d = R[n]
    print(f"{n:8s} | {d['wealth']:8.1f} | {d['acc']:.3f} | {d['swan_acc']:.3f} | "
          f"{d['calm_acc']:.3f} | {d['n_adds']:4d}")

# ---------------------------------------------------------------- seed invariance (deterministic at gamma=0)
inv_ok = True
for s in SEEDS[1:]:
    for n in th_names + pu_names:
        for k in ("wealth", "swan_acc", "calm_acc", "acc"):
            if abs(all_results[s][n][k] - R[n][k]) > 1e-9:
                inv_ok = False
                print(f"SEED VARIANCE: seed {s} {n} {k}: "
                      f"{all_results[s][n][k]} vs {R[n][k]}")
print(f"\nseed invariance across {SEEDS}: {'CONFIRMED (deterministic)' if inv_ok else 'VIOLATED'}")

# ---------------------------------------------------------------- pre-registered predictions (primary seed)
swan_by_th = {th: R[f"th{th:.2f}"]["swan_acc"] for th in THETAS}
t_star = max(THETAS, key=lambda th: swan_by_th[th])
p1 = t_star in (0.05, 0.1, 0.15, 0.2, 0.3)

d0 = R["th0.00"]
p2 = (abs(d0["swan_acc"] - hy["swan_acc"]) < 1e-9
      and abs(d0["calm_acc"] - hy["calm_acc"]) < 1e-9
      and abs(d0["wealth"] - hy["wealth"]) < 1e-6)

swan_by_pu = {ka: R[f"pull{ka:.1f}"]["swan_acc"] for ka in KAPPAS if ka > 0}
pull_best = max(swan_by_pu, key=lambda ka: swan_by_pu[ka])
th_best_swan = max(swan_by_th.values())
p3 = swan_by_pu[pull_best] > th_best_swan

p4 = swan_by_pu[pull_best] >= hy["swan_acc"] - 0.01

# kappa=0 control diagnostic: no phase motion -> classical recovery
pu0 = R["pull0.0"]
pu0_ok = (abs(pu0["swan_acc"] - hy["swan_acc"]) < 1e-9
          and abs(pu0["calm_acc"] - hy["calm_acc"]) < 1e-9)

print(f"\npeak theta: {t_star} (wrap analysis predicted ~0.1)")
print(f"P1 (peak theta {t_star} interior, not 0/0.5): {'PASS' if p1 else 'FAIL'}")
print(f"P2 (theta=0 recovers hydra exactly: "
      f"swan {d0['swan_acc']:.3f} vs {hy['swan_acc']:.3f}, "
      f"calm {d0['calm_acc']:.3f} vs {hy['calm_acc']:.3f}, "
      f"wealth {d0['wealth']:.1f} vs {hy['wealth']:.1f}): {'PASS' if p2 else 'FAIL'}")
print(f"P3 (best pull kappa={pull_best} swan {swan_by_pu[pull_best]:.3f} > "
      f"best constant-rotation swan {th_best_swan:.3f}): {'PASS' if p3 else 'FAIL'}")
print(f"P4 (best pull swan {swan_by_pu[pull_best]:.3f} >= hydra swan "
      f"{hy['swan_acc']:.3f} - 0.01): {'PASS' if p4 else 'FAIL'}")
print(f"diagnostic: kappa=0 control recovers hydra: {'yes' if pu0_ok else 'NO'}")
print(f"n_adds: hydra={hy['n_adds']}, " +
      ", ".join(f"th{th:.2f}={R[f'th{th:.2f}']['n_adds']}" for th in THETAS))
print(f"n_adds: " +
      ", ".join(f"pull{ka:.1f}={R[f'pull{ka:.1f}']['n_adds']}" for ka in KAPPAS))

ok = bool(p1 and p2 and p3 and p4 and inv_ok)
print(f"\n{'ALL PASS — exit 0' if ok else 'SOME FAILED — exit 1'}")

with open(os.path.join(OUTDIR, "followups_results.json"), "w") as f:
    json.dump({
        "predictions": {
            "P1": bool(p1), "P2": bool(p2), "P3": bool(p3), "P4": bool(p4),
            "peak_theta": t_star, "best_kappa": pull_best,
            "theta0_recovers_hydra": bool(p2),
            "kappa0_recovers_hydra": bool(pu0_ok),
            "seed_invariance": bool(inv_ok),
            "all_pass": bool(ok),
        },
        "params": {"thetas": THETAS, "kappas": KAPPAS, "gamma": GAMMA,
                   "seeds": SEEDS, "world_seed": 99,
                   "scoring": "+6/+15/+25/-10",
                   "pull_note": "pull REPLACES constant rotation (no theta); "
                                "kappa=0 control = no phase motion"},
        "seeds_run": SEEDS,
        "agents": {k: {kk: vv for kk, vv in v.items() if kk != "wealth_curve"}
                   for k, v in R.items()},
    }, f, indent=1)
print("wrote followups_results.json")

# ---------------------------------------------------------------- plots
t_axis = np.arange(len(R["hydra"]["wealth_curve"]))

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].plot(THETAS, [swan_by_th[th] for th in THETAS], "o-", color="#b45cff",
             lw=2, label="quantum swan-acc (theta sweep)")
axes[0].axhline(hy["swan_acc"], color="#2a7fff", ls="--", lw=1.5,
                label=f"classical Hydra ({hy['swan_acc']:.3f})")
axes[0].axvline(0.1, color="k", ls=":", lw=1, label="wrap-theory optimum ~0.1")
axes[0].axvline(t_star, color="#b45cff", ls="-.", lw=1,
                label=f"observed peak {t_star}")
axes[0].set_xlabel("interference strength theta")
axes[0].set_ylabel("swan accuracy")
axes[0].set_title("P1: swan accuracy vs theta (interior peak?)")
axes[0].legend(fontsize=9)
axes[1].plot(THETAS, [R[f"th{th:.2f}"]["wealth"] for th in THETAS], "o-",
             color="#b45cff", lw=2, label="quantum wealth")
axes[1].axhline(hy["wealth"], color="#2a7fff", ls="--", lw=1.5,
                label=f"classical Hydra ({hy['wealth']:.0f})")
axes[1].set_xlabel("interference strength theta")
axes[1].set_ylabel("wealth (coins)")
axes[1].set_title("Wealth vs theta")
axes[1].legend(fontsize=9)
fig.suptitle("Follow-up 1: theta sweep at gamma=0 (coherent)")
fig.tight_layout()
fig.savefig(os.path.join(OUTDIR, "followups_theta.png"), dpi=110)
print("wrote followups_theta.png")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
ka_pos = [ka for ka in KAPPAS if ka > 0]
axes[0].plot(ka_pos, [swan_by_pu[ka] for ka in ka_pos], "o-", color="#22cc66",
             lw=2, label="pull-variant swan-acc")
axes[0].axhline(hy["swan_acc"], color="#2a7fff", ls="--", lw=1.5,
                label=f"classical Hydra ({hy['swan_acc']:.3f})")
axes[0].axhline(th_best_swan, color="#b45cff", ls=":", lw=1.5,
                label=f"best constant-rotation ({th_best_swan:.3f})")
axes[0].set_xlabel("pull strength kappa")
axes[0].set_ylabel("swan accuracy")
axes[0].set_title("P3/P4: pull (persistent memory) vs baselines")
axes[0].legend(fontsize=9)
axes[1].plot(ka_pos, [R[f"pull{ka:.1f}"]["wealth"] for ka in ka_pos], "o-",
             color="#22cc66", lw=2, label="pull-variant wealth")
axes[1].axhline(hy["wealth"], color="#2a7fff", ls="--", lw=1.5,
                label=f"classical Hydra ({hy['wealth']:.0f})")
axes[1].set_xlabel("pull strength kappa")
axes[1].set_ylabel("wealth (coins)")
axes[1].set_title("Pull-variant wealth vs kappa")
axes[1].legend(fontsize=9)
fig.suptitle("Follow-up 2: persistent-memory (rotate-to-fixed-point) sweep")
fig.tight_layout()
fig.savefig(os.path.join(OUTDIR, "followups_kappa.png"), dpi=110)
print("wrote followups_kappa.png")

fig, ax = plt.subplots(figsize=(13, 5))
for name, color, label in [
        ("hydra", "#2a7fff", "Hydra (classical)"),
        (f"th{t_star:.2f}", "#b45cff", f"const-rotation theta={t_star} (peak)"),
        (f"pull{pull_best:.1f}", "#22cc66",
         f"pull kappa={pull_best} (best persistent-memory)"),
]:
    ax.plot(t_axis, R[name]["wealth_curve"], color=color, label=label, lw=2)
for st in swan_times:
    ax.axvspan(st - WARM - 12, st - WARM + 12, color="red", alpha=0.10)
ax.axhline(0, color="k", ls="--", lw=1)
ax.set_xlabel("time step (from warmup end)")
ax.set_ylabel("wealth (coins)")
ax.set_title("Follow-ups: wealth through swans (best of each family)")
ax.legend(fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(OUTDIR, "followups_wealth.png"), dpi=110)
print("wrote followups_wealth.png")

sys.exit(0 if ok else 1)
