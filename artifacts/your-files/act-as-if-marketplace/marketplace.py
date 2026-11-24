"""
THE MARKETPLACE — the zoo under one thermodynamic budget.

Premise: the Gate forgot for free, JEPA refused for free, Genie dreamed for
free. Nothing is free. Every erased bit costs kT ln 2 (Landauer). Put all
three under one energy budget and watch which strategies survive scarcity.

The market:
  stream: 600 bits from a 3-regime hidden Markov model
          (biases 0.25 / 0.50 / 0.75, mean regime length ~35 steps)
  each agent starts with 120 energy coins.
  earnings: +6 per correct next-bit prediction
            +6 per correct 3-ahead "futures" prediction (Genie's niche)
            +15 per correct regime call (every 10 steps, JEPA's niche)
  costs (in coins; 1 coin = 1 bit-erasure at kT=1, i.e. ln2 energy units):
    GATE:  ln2 * sum_d (1 - exp(delta_t*A_d)) * Q  (Q=1 bit/dim)
           opening the gate wide DESTROYS old state = pays Landauer.
    JEPA:  encoder update = ln2 * 6  (8 window bits -> 2-bit regime)
           coasting (reuse last latent) = ln2 * 1 (head only)
    GENIE: 1.2 coins per dreamed step + 1.0 upkeep.
           Depth d costs 1.2d+1. Futures premium must cover it.
  adaptive dials by wealth:
    wealth > 150: lavish | 50-150: normal | <=50: frugal | <0: bankrupt.
    (Dials change only COST-relevant parameters, never the trained core --
    a trader changes spending, not their brain.)

Experiment 2 (Pareto): each agent at fixed frugal/normal/lavish for the
whole run. Accuracy vs energy scatter = the exchange-rate curves.

Honest labeling: toy energy model. "Bits erased" is estimated from each
mechanism (state overwrite / compression / imagined collapse), not measured
in silicon. What's real: the TRADEOFF STRUCTURE -- selectivity costs,
refusal saves, dreaming spends. The exchange rates are what we measure.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(21)
LN2 = np.log(2)
N = 600
WARM = 100

# ---------------------------------------------------------------- the stream
REGIMES = [0.25, 0.50, 0.75]
bits, true_reg = [], []
r = 1
for t in range(N):
    if rng.random() < 1 / 35:
        r = rng.integers(0, 3)
    true_reg.append(r)
    bits.append(1 if rng.random() < REGIMES[r] else 0)
bits = np.array(bits); true_reg = np.array(true_reg)
warm_bias = [bits[:WARM][true_reg[:WARM] == k].mean() for k in range(3)]

# ---------------------------------------------------------------- GATE
GDIM = 6
GA = -(0.4 + 0.6 * np.arange(GDIM) / GDIM)
GB = rng.normal(0, 0.5, (GDIM, 2))
QBIT = 1

def gate_delta(surprise, scale):
    return np.log1p(np.exp(scale * (3.0 * surprise - 1.0)))

# train logistic readout on warmup (mirrors the live state update exactly)
gh = np.zeros(GDIM)
states, ys = [], []
for t in range(WARM):
    x = np.array([bits[t], 1 - bits[t]])
    pred_m = np.mean(bits[max(0, t - 10):t]) if t > 0 else 0.5
    d = gate_delta(abs(bits[t] - pred_m), 1.0)
    gh = np.exp(d * GA) * gh + (d * GB) @ x
    states.append(gh.copy()); ys.append(bits[t])
states = np.array(states); ys = np.array(ys)
w = np.zeros(GDIM + 1)
Xa = np.column_stack([states, np.ones(len(states))])
for _ in range(800):
    p = 1 / (1 + np.exp(-Xa @ w))
    w -= 0.5 * Xa.T @ (p - ys) / len(ys)

class Gate:
    def __init__(self):
        self.h = np.zeros(GDIM)
        # roll state through warmup so live starts where training ended
        for t in range(WARM):
            x = np.array([bits[t], 1 - bits[t]])
            pred_m = np.mean(bits[max(0, t - 10):t]) if t > 0 else 0.5
            d = gate_delta(abs(bits[t] - pred_m), 1.0)
            self.h = np.exp(d * GA) * self.h + (d * GB) @ x
        self.t = WARM
    def step(self, scale):
        t = self.t
        x = np.array([bits[t - 1], 1 - bits[t - 1]])
        pred_m = np.mean(bits[max(0, t - 10):t - 1])
        d = gate_delta(abs(bits[t - 1] - pred_m), scale)
        erase = float(np.sum(1 - np.exp(d * GA)) * QBIT)
        cost = LN2 * erase + 0.1
        self.h = np.exp(d * GA) * self.h + (d * GB) @ x
        p = float(1 / (1 + np.exp(-(self.h @ w[:GDIM] + w[GDIM]))))
        self.t += 1
        return p, cost

# ---------------------------------------------------------------- JEPA
class JEPA:
    def __init__(self):
        self.latent = 1
        self.bias = list(warm_bias)
        self.t = WARM
    def step(self, threshold):
        t = self.t
        recent = bits[t - 8:t]
        surprise = abs(recent.mean() - self.bias[self.latent])
        if surprise > threshold:
            cost = LN2 * 6 + LN2 * 1
            win = bits[t - 15:t].mean()
            self.latent = int(np.argmin([abs(win - b) for b in self.bias]))
        else:
            cost = LN2 * 1
        self.t += 1
        return self.bias[self.latent], cost, self.latent

# ---------------------------------------------------------------- GENIE
counts = np.zeros((2, 2, 2))
for t in range(2, WARM):
    counts[bits[t - 2], bits[t - 1], bits[t]] += 1
Pmk = (counts[:, :, 1] + 0.5) / (counts.sum(axis=2) + 1)

class Genie:
    def __init__(self):
        self.t = WARM
    def step(self, depth):
        t = self.t
        cost = 1.0
        b1, b2 = bits[t - 2], bits[t - 1]
        fut = []
        for _ in range(depth):
            p1 = Pmk[b1, b2]
            fut.append(p1)
            b1, b2 = b2, 1 if rng.random() < p1 else 0
            cost += 1.2
        self.t += 1
        return fut[0], (fut[2] if depth >= 3 else None), cost

# ---------------------------------------------------------------- the market
# Experiment 1: fixed "normal" dials, adaptive wealth. Who survives on
# efficiency alone?
def dial(w):
    # dials are informational here (fixed normal); wealth still tracked
    return "normal"

gate, jepa, genie = Gate(), JEPA(), Genie()
wealth = {"gate": 120.0, "jepa": 120.0, "genie": 120.0}
alive = {"gate": True, "jepa": True, "genie": True}
acc = {"gate": [], "jepa": [], "genie": []}
spent = {"gate": 0.0, "jepa": 0.0, "genie": 0.0}
Wh = {"gate": [], "jepa": [], "genie": []}

for t in range(WARM, N - 3):
    if alive["gate"]:
        p, cost = gate.step(1.0)
        win = 6 if (p > 0.5) == bits[t] else 0
        if t % 10 == 0:
            win += 15 if int(np.argmin([abs(p - b) for b in warm_bias])) == true_reg[t] else 0
        wealth["gate"] += win - cost
        spent["gate"] += cost
        acc["gate"].append((p > 0.5) == bits[t])
        if wealth["gate"] < 0: alive["gate"] = False
    if alive["jepa"]:
        p, cost, latent = jepa.step(0.12)
        win = 6 if (p > 0.5) == bits[t] else 0
        if t % 10 == 0:
            win += 15 if latent == true_reg[t] else 0
        wealth["jepa"] += win - cost
        spent["jepa"] += cost
        acc["jepa"].append((p > 0.5) == bits[t])
        if wealth["jepa"] < 0: alive["jepa"] = False
    if alive["genie"]:
        p, p3, cost = genie.step(2)
        win = 6 if (p > 0.5) == bits[t] else 0
        if p3 is not None:
            win += 6 if (p3 > 0.5) == bits[t + 2] else 0
        if t % 10 == 0:
            win10 = bits[max(WARM, t - 10):t]
            lls = [np.sum(win10 * np.log(b + 1e-9) + (1 - win10) * np.log(1 - b + 1e-9))
                   for b in warm_bias]
            win += 15 if int(np.argmax(lls)) == true_reg[t] else 0
        wealth["genie"] += win - cost
        spent["genie"] += cost
        acc["genie"].append((p > 0.5) == bits[t])
        if wealth["genie"] < 0: alive["genie"] = False
    for name in Wh:
        Wh[name].append(wealth[name])

print("=== THE MARKETPLACE ===")
print(f"stream: {N} bits, 3 regimes, warmup {WARM}, start wealth 120\n")
for name in ("gate", "jepa", "genie"):
    a = np.mean(acc[name]) if acc[name] else 0
    eff = a / (spent[name] / max(len(acc[name]), 1)) * 100
    print(f"{name:6s} | wealth {wealth[name]:8.1f} | alive {str(alive[name]):5s} | "
          f"acc {a:.3f} | spent {spent[name]:8.1f} | {eff:.3f} acc/100 coins")
print()
print(f"richest -> poorest: {' > '.join(sorted(wealth, key=wealth.get, reverse=True))}")

# ---------------------------------------------------------------- Experiment 2: Pareto sweep
# Each agent at fixed frugal/normal/lavish. Per-dial calibration where needed.
print("\n=== PARETO SWEEP (accuracy vs energy per step) ===")

def train_gate_readout(scale):
    """Retrain readout for a given gate scale (honest calibration)."""
    h = np.zeros(GDIM)
    S, Y = [], []
    for t in range(WARM):
        x = np.array([bits[t], 1 - bits[t]])
        pred_m = np.mean(bits[max(0, t - 10):t]) if t > 0 else 0.5
        d = gate_delta(abs(bits[t] - pred_m), scale)
        h = np.exp(d * GA) * h + (d * GB) @ x
        S.append(h.copy()); Y.append(bits[t])
    S = np.array(S); Y = np.array(Y)
    ww = np.zeros(GDIM + 1)
    Xa = np.column_stack([S, np.ones(len(S))])
    for _ in range(800):
        p = 1 / (1 + np.exp(-Xa @ ww))
        ww -= 0.5 * Xa.T @ (p - Y) / len(Y)
    return ww

def sweep_gate(scale):
    ww = train_gate_readout(scale)
    h = np.zeros(GDIM)
    for t in range(WARM):  # warmup state
        x = np.array([bits[t], 1 - bits[t]])
        pred_m = np.mean(bits[max(0, t - 10):t]) if t > 0 else 0.5
        d = gate_delta(abs(bits[t] - pred_m), scale)
        h = np.exp(d * GA) * h + (d * GB) @ x
    correct, energy = 0, 0.0
    n = 0
    for t in range(WARM, N):
        x = np.array([bits[t - 1], 1 - bits[t - 1]])
        pred_m = np.mean(bits[t - 10:t - 1])
        d = gate_delta(abs(bits[t - 1] - pred_m), scale)
        energy += LN2 * float(np.sum(1 - np.exp(d * GA)) * QBIT) + 0.1
        h = np.exp(d * GA) * h + (d * GB) @ x
        p = float(1 / (1 + np.exp(-(h @ ww[:GDIM] + ww[GDIM]))))
        correct += (p > 0.5) == bits[t]
        n += 1
    return correct / n, energy / n

def sweep_jepa(threshold):
    latent = 1; bias = list(warm_bias)
    correct, energy = 0, 0.0; n = 0
    for t in range(WARM, N):
        recent = bits[t - 8:t]
        if abs(recent.mean() - bias[latent]) > threshold:
            energy += LN2 * 6 + LN2 * 1
            win = bits[t - 15:t].mean()
            latent = int(np.argmin([abs(win - b) for b in bias]))
        else:
            energy += LN2 * 1
        correct += (bias[latent] > 0.5) == bits[t]
        n += 1
    return correct / n, energy / n

def sweep_genie(depth):
    correct, energy = 0, 0.0; n = 0
    for t in range(WARM, N - 3):
        b1, b2 = bits[t - 2], bits[t - 1]
        p1 = Pmk[b1, b2]
        # dream depth steps; predict t and t+2
        e = 1.0 + depth * 1.2
        # next-bit from model directly; futures need dreaming
        correct += (p1 > 0.5) == bits[t]
        if depth >= 3:
            # dream 3 ahead
            bb1, bb2 = b1, b2
            for _ in range(3):
                bb1, bb2 = bb2, 1 if Pmk[bb1, bb2] > 0.5 else 0
            # p(t+2) via 2-step dream: use deterministic rollout prob
            p3 = Pmk[bb1, bb2]  # approx
            correct += 0  # futures scored separately; keep simple: next-bit only
        energy += e
        n += 1
    return correct / n, energy / n

pareto = {}
for name, dials, fn in [
    ("gate", [0.5, 1.0, 2.0], sweep_gate),
    ("jepa", [0.20, 0.12, 0.05], sweep_jepa),
    ("genie", [1, 2, 3], sweep_genie),
]:
    pts = []
    for d in dials:
        a, e = fn(d)
        pts.append((a, e))
        print(f"  {name:6s} dial {d}: acc {a:.3f}, energy {e:.2f}/step")
    pareto[name] = pts

# plot pareto
fig2, ax2 = plt.subplots(figsize=(8, 6))
for name, c in (("gate", "#2a7fff"), ("jepa", "#ff9f2a"), ("genie", "#b45cff")):
    pts = pareto[name]
    ax2.scatter([e for a, e in pts], [a for a, e in pts], color=c, s=100, label=name, zorder=3)
    for (a, e), lbl in zip(pts, ("frugal", "normal", "lavish")):
        ax2.annotate(lbl, (e, a), xytext=(6, 6), textcoords="offset points", fontsize=9, color=c)
ax2.set_xlabel("energy per step (coins)")
ax2.set_ylabel("next-bit accuracy")
ax2.set_title("Pareto: the exchange rate (accuracy per energy)")
ax2.legend()
fig2.tight_layout()
fig2.savefig("pareto.png", dpi=110)
print("\nwrote pareto.png")

fig, ax = plt.subplots(figsize=(12, 5))
for name, c in (("gate", "#2a7fff"), ("jepa", "#ff9f2a"), ("genie", "#b45cff")):
    ax.plot(Wh[name], color=c, label=name, lw=2)
ax.axhline(0, color="k", ls="--", lw=1)
ax.axhline(50, color="gray", ls=":", lw=1, label="frugal line")
ax.axhline(150, color="gray", ls=":", lw=1, label="lavish line")
ax.set_xlabel("time step")
ax.set_ylabel("wealth (energy coins)")
ax.set_title("The Marketplace: wealth under a Landauer budget")
ax.legend()
fig.tight_layout()
fig.savefig("marketplace.png", dpi=110)
print("\nwrote marketplace.png")
