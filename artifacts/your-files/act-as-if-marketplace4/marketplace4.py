"""
MARKETPLACE IV — the missing lenses.

Four floors absent from the zoo, in the same black-swan world
(1000 bits, regimes ~120 steps, 3 unprecedented swans). Each reveals
what the others assume.

  BAYESIAN: 3 Beta particles (regime-switching filter). Knows its uncertainty
    as a quantified object. On swans, posterior entropy spikes -> declares
    swan, predicts 0.5. Differs from JEPA: JEPA *stops*; Bayes *knows why*.
  EVOLUTIONARY: 24 biases, no learning, no memory, no model. Every 50 steps:
    keep fittest 12, reproduce with mutation. The population adapts; no
    individual knows anything. Selection IS learning, without a learner.
  SOCIAL (theory of mind): 3 experts (momentum, mean, contrarian). Models each
    expert's *hidden state* (calm/confused) via mini-Bayes on their errors.
    Trusts the calm. Second-order: models knowers, not just the world.
  REACTIVE (embodied-minimal): predicts last bit. No model, no memory beyond
    1 step, no swan concept. Pure coupling. The world is its own best model.

Pre-registered:
  P1: REACTIVE has the highest accuracy DURING swans (couples to 0.92 bias
      without needing to "understand" it).
  P2: BAYESIAN has the best Brier score (probabilistic calibration) — it
      knows its uncertainty, others don't represent it.
  P3: EVOLUTIONARY survives swans (diversity) but its population mean doesn't
      *retain* swan knowledge (no individual memory) — post-swan, it reverts.
  P4: SOCIAL beats its best single expert (models *when* to trust whom).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(99)
LN2 = np.log(2)
N = 1000
WARM = 150
REGIMES = [0.25, 0.50, 0.75]
SWAN_LEN = 25
swan_times = [300 + rng.integers(-40, 40), 550 + rng.integers(-40, 40),
              800 + rng.integers(-40, 40)]

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
        bits.append(1 if rng.random() < sb else 0)
    else:
        if rng.random() < 1 / 120:
            r = rng.integers(0, 3)
        true_reg.append(r); is_swan.append(False)
        bits.append(1 if rng.random() < REGIMES[r] else 0)
bits = np.array(bits); true_reg = np.array(true_reg); is_swan = np.array(is_swan)
warm_bias = []
for k in range(3):
    m = bits[:WARM][true_reg[:WARM] == k]
    warm_bias.append(m.mean() if len(m) > 0 else 0.5)
print(f"swans at {sorted(swan_times)}")


# ---------------------------------------------------------------- BAYESIAN
class Bayes:
    def __init__(self):
        # 3 particles: Beta(a,b), weight w
        self.a = np.array([2.0, 2.0, 2.0])
        self.b = np.array([2.0, 2.0, 2.0])
        # seed from warmup
        for k in range(3):
            m = bits[:WARM][true_reg[:WARM] == k]
            if len(m) > 0:
                self.a[k] += m.sum()
                self.b[k] += len(m) - m.sum()
        self.w = np.array([1/3, 1/3, 1/3])
        self.t = WARM

    def step(self):
        t = self.t
        bit = bits[t - 1]
        # likelihood of bit under each particle's predictive
        p1 = self.a / (self.a + self.b)
        lik = np.where(bit == 1, p1, 1 - p1)
        self.w = self.w * lik
        self.w /= self.w.sum()
        # soft update all particles (proportional to responsibility)
        self.a += self.w * bit
        self.b += self.w * (1 - bit)
        # regime-switch: small chance to refresh weakest particle toward prior
        if rng.random() < 0.02:
            j = int(np.argmin(self.w))
            self.a[j] = self.a[j] * 0.5 + 1.0
            self.b[j] = self.b[j] * 0.5 + 1.0
        # posterior predictive + entropy
        pred = float(np.sum(self.w * p1))
        # entropy of weight distribution (uncertainty about regime)
        ent = float(-np.sum(self.w * np.log(self.w + 1e-12)) / np.log(3))
        swan = ent > 0.85
        cost = LN2 * 3  # distributions cost more than points, but not 9x
        self.t += 1
        return (0.5 if swan else pred), cost, swan, pred


# ---------------------------------------------------------------- EVOLUTIONARY
class Evo:
    def __init__(self):
        self.pop = rng.uniform(0.05, 0.95, 24)
        self.fit = np.zeros(24)
        self.t = WARM
        self.gen = 0

    def step(self):
        t = self.t
        bit = bits[t - 1]
        # population prediction: majority vote (robust to spread)
        votes = (self.pop > 0.5).astype(float)
        p = float(votes.mean())  # P(population says 1)
        # individual fitness: was it right?
        correct = ((self.pop > 0.5) == bit)
        self.fit += correct.astype(float)
        cost = 0.05 * 24  # existing is cheap
        # evolve every 50 steps
        if (t - WARM) % 50 == 0 and t > WARM:
            idx = np.argsort(self.fit)
            survivors = self.pop[idx[-12:]]
            children = np.clip(survivors + rng.normal(0, 0.04, 12), 0.05, 0.95)
            self.pop[idx[:12]] = children
            self.fit[:] = 0
            cost += 12 * LN2 * 2  # writing 12 new genomes
            self.gen += 1
        # swan call: population disagreement spikes
        swan = float(self.pop.std()) > 0.25
        self.t += 1
        return p, cost, swan


# ---------------------------------------------------------------- SOCIAL (theory of mind)
class Social:
    def __init__(self):
        # experts: momentum, mean-follower, contrarian
        self.p_confused = np.array([0.2, 0.2, 0.2])  # P(expert is confused)
        self.base_err = np.array([0.35, 0.30, 0.45])  # baseline error when calm
        self.t = WARM

    def experts(self, t):
        window = bits[t - 10:t]
        return np.array([
            float(bits[t - 1]),       # momentum
            float(window.mean()),     # mean
            float(1 - bits[t - 1]),   # contrarian
        ])

    def step(self):
        t = self.t
        bit = bits[t - 1]
        e = self.experts(t)
        err = np.abs(e - bit)
        # update P(confused) for each expert via Bayes
        # P(err|confused)=0.5 (random), P(err|calm)=base_err
        for i in range(3):
            p_e_given_conf = 0.5 if err[i] > 0.5 else 0.5  # binary-ish
            # use continuous: likelihood of observed error
            lh_conf = 0.5
            lh_calm = self.base_err[i] if err[i] > 0.5 else (1 - self.base_err[i])
            pc = self.p_confused[i]
            post = (lh_conf * pc) / (lh_conf * pc + lh_calm * (1 - pc) + 1e-12)
            # smooth toward posterior (don't jump)
            self.p_confused[i] = 0.7 * pc + 0.3 * post
        trust = 1 - self.p_confused
        trust /= trust.sum()
        p = float(np.sum(trust * e))
        # swan: all experts confused
        swan = bool(np.all(self.p_confused > 0.6))
        cost = LN2 * 2  # 3 mini-Bayes: more than a point, less than full Bayes
        self.t += 1
        return p, cost, swan, trust


# ---------------------------------------------------------------- REACTIVE (no model)
class Reactive:
    def __init__(self):
        self.t = WARM

    def step(self):
        t = self.t
        p = float(bits[t - 1])  # pure coupling: be the last bit
        self.t += 1
        return p, 0.0, False  # no cost, no swan concept


# ---------------------------------------------------------------- JEPA (robust baseline, from marketplace2)
class JEPA:
    def __init__(self):
        self.latent = 1
        self.bias = list(warm_bias)
        self.t = WARM
        self.updates = []
        self.swan_mode = False

    def step(self):
        t = self.t
        if self.swan_mode:
            recent = bits[t - 8:t]
            if abs(recent.mean() - 0.5) < 0.2:
                self.swan_mode = False
            self.t += 1
            self.updates.append(False)
            return 0.5, LN2 * 0.5, True, 0.5
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
        return self.bias[self.latent], cost, self.swan_mode, self.bias[self.latent]


# ---------------------------------------------------------------- market
agents = {
    "bayes": Bayes(), "evo": Evo(), "social": Social(),
    "reactive": Reactive(), "jepa": JEPA(),
}
wealth = {k: 200.0 for k in agents}
alive = {k: True for k in agents}
acc = {k: [] for k in agents}
acc_swan = {k: [] for k in agents}
spent = {k: 0.0 for k in agents}
swan_calls = {k: [] for k in agents}
brier = {k: [] for k in agents}
Wh = {k: [] for k in agents}
# for P4: track expert accuracies
expert_acc = {"momentum": [], "mean": [], "contrarian": []}

for t in range(WARM, N - 10):
    # bayes
    if alive["bayes"]:
        p, cost, swan, p_raw = agents["bayes"].step()
        win = 6 if (p > 0.5) == bits[t] else 0
        if t % 10 == 0 and t + 10 < N:
            win += 12 if (p > 0.5) == bits[t + 10] else 0
        if t % 10 == 0:
            hit = is_swan[t]
            swan_calls["bayes"].append(swan == hit)
            win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
        wealth["bayes"] += win - cost
        spent["bayes"] += cost
        acc["bayes"].append((p > 0.5) == bits[t])
        brier["bayes"].append((p_raw - bits[t]) ** 2)
        if is_swan[t]:
            acc_swan["bayes"].append((p > 0.5) == bits[t])
        if wealth["bayes"] < 0:
            alive["bayes"] = False
    # evo
    if alive["evo"]:
        p, cost, swan = agents["evo"].step()
        win = 6 if (p > 0.5) == bits[t] else 0
        if t % 10 == 0 and t + 10 < N:
            win += 12 if (p > 0.5) == bits[t + 10] else 0
        if t % 10 == 0:
            hit = is_swan[t]
            swan_calls["evo"].append(swan == hit)
            win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
        wealth["evo"] += win - cost
        spent["evo"] += cost
        acc["evo"].append((p > 0.5) == bits[t])
        brier["evo"].append((p - bits[t]) ** 2)
        if is_swan[t]:
            acc_swan["evo"].append((p > 0.5) == bits[t])
        if wealth["evo"] < 0:
            alive["evo"] = False
    # social
    if alive["social"]:
        p, cost, swan, trust = agents["social"].step()
        win = 6 if (p > 0.5) == bits[t] else 0
        if t % 10 == 0 and t + 10 < N:
            win += 12 if (p > 0.5) == bits[t + 10] else 0
        if t % 10 == 0:
            hit = is_swan[t]
            swan_calls["social"].append(swan == hit)
            win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
        wealth["social"] += win - cost
        spent["social"] += cost
        acc["social"].append((p > 0.5) == bits[t])
        brier["social"].append((p - bits[t]) ** 2)
        if is_swan[t]:
            acc_swan["social"].append((p > 0.5) == bits[t])
        # expert accuracies for P4
        e = agents["social"].experts(t)
        for i, name in enumerate(["momentum", "mean", "contrarian"]):
            expert_acc[name].append((e[i] > 0.5) == bits[t])
        if wealth["social"] < 0:
            alive["social"] = False
    # reactive
    if alive["reactive"]:
        p, cost, swan = agents["reactive"].step()
        win = 6 if (p > 0.5) == bits[t] else 0
        if t % 10 == 0 and t + 10 < N:
            win += 12 if (p > 0.5) == bits[t + 10] else 0
        # reactive cannot call swans (no concept of them)
        wealth["reactive"] += win - cost
        spent["reactive"] += cost
        acc["reactive"].append((p > 0.5) == bits[t])
        brier["reactive"].append((p - bits[t]) ** 2)
        if is_swan[t]:
            acc_swan["reactive"].append((p > 0.5) == bits[t])
        if wealth["reactive"] < 0:
            alive["reactive"] = False
    # jepa
    if alive["jepa"]:
        p, cost, swan, p_raw = agents["jepa"].step()
        win = 6 if (p > 0.5) == bits[t] else 0
        if t % 10 == 0:
            hit = is_swan[t]
            swan_calls["jepa"].append(swan == hit)
            win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
        wealth["jepa"] += win - cost
        spent["jepa"] += cost
        acc["jepa"].append((p > 0.5) == bits[t])
        brier["jepa"].append((p_raw - bits[t]) ** 2)
        if is_swan[t]:
            acc_swan["jepa"].append((p > 0.5) == bits[t])
        if wealth["jepa"] < 0:
            alive["jepa"] = False
    for k in agents:
        Wh[k].append(wealth[k] if alive[k] else (Wh[k][-1] if Wh[k] else 0))

print("\n=== MARKETPLACE IV: the missing lenses ===")
for k in agents:
    a = np.mean(acc[k]) if acc[k] else 0
    asw = np.mean(acc_swan[k]) if acc_swan[k] else 0
    br = np.mean(brier[k]) if brier[k] else 0
    sc = np.mean(swan_calls[k]) if swan_calls[k] else 0
    eff = a / (spent[k] / max(len(acc[k]), 1)) * 100
    print(f"{k:8s} | wealth {wealth[k]:8.1f} | acc {a:.3f} | swan-acc {asw:.3f} | "
          f"brier {br:.3f} | swan-call {sc:.2f} | spent {spent[k]:7.1f} | {eff:.1f}/100c")

# P1: reactive best during swans?
swan_accs = {k: np.mean(acc_swan[k]) for k in agents if acc_swan[k]}
best_swan = max(swan_accs, key=swan_accs.get)
print(f"\nP1 (reactive best in swans): {'PASS' if best_swan=='reactive' else 'FAIL'} ({best_swan} {swan_accs[best_swan]:.3f})")
# P2: bayes best Brier?
briers = {k: np.mean(brier[k]) for k in agents if brier[k]}
best_br = min(briers, key=briers.get)
print(f"P2 (bayes best Brier): {'PASS' if best_br=='bayes' else 'FAIL'} ({best_br} {briers[best_br]:.3f})")
# P3: evo survives?
print(f"P3 (evo survives swans): {'PASS' if alive['evo'] else 'FAIL'} (wealth {wealth['evo']:.0f})")
# P4: social beats best expert?
best_expert = max(np.mean(expert_acc[n]) for n in expert_acc)
social_acc = np.mean(acc["social"])
print(f"P4 (social beats best expert): {'PASS' if social_acc > best_expert else 'FAIL'} "
      f"({social_acc:.3f} vs {best_expert:.3f})")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
colors = {"bayes": "#22cc66", "evo": "#ff9f2a", "social": "#b45cff",
          "reactive": "#ff5555", "jepa": "#2a7fff"}
for k in agents:
    axes[0].plot(Wh[k], color=colors[k], label=k, lw=2)
for st in swan_times:
    axes[0].axvspan(st - WARM - 12, st - WARM + 12, color="red", alpha=0.12)
axes[0].axhline(0, color="k", ls="--", lw=1)
axes[0].set_xlabel("time step (from warmup end)")
axes[0].set_ylabel("wealth (coins)")
axes[0].set_title("Marketplace IV: wealth through swans")
axes[0].legend(fontsize=9)
# Brier bars
ks = list(agents.keys())
axes[1].bar(ks, [np.mean(brier[k]) for k in ks],
            color=[colors[k] for k in ks], alpha=0.8)
axes[1].set_ylabel("Brier score (lower = better calibrated)")
axes[1].set_title("Who knows its uncertainty?")
axes[1].tick_params(axis="x", rotation=20)
fig.suptitle("Marketplace IV: the missing lenses")
fig.tight_layout()
fig.savefig("marketplace4.png", dpi=110)
print("\nwrote marketplace4.png")
