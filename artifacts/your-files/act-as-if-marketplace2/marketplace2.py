"""
THE MARKETPLACE II — long horizon, black swans.

The calm-world exchange rates are priced. Now: a 1000-bit world with long
regimes (mean 120 steps — patience pays) and 3 BLACK SWANS: 25-step bursts
of an unprecedented 4th regime (bias 0.92/0.08, never in warmup). The models'
warmup calibrations don't cover it. They must cope or bleed.

Swan strategies (each agent's choice, priced):
  GATE:  surprise spikes -> scale boosts to 2.5 (frantic adaptation).
         Tries to learn the swan. Pays massive erasure.
  JEPA:  persistent surprise -> "swan mode": predicts 0.5, STOPS updating.
         Strategic ignorance. Admits the unprecedented, saves coins.
  GENIE: likelihood collapses -> depth drops to 1 (dreams are worthless in
         chaos), declares swan. Stops dreaming, saves coins.

Earnings: +6 next-bit | +12 futures (t+10, long horizon) |
          +20 regime (every 20 steps) | +25 swan call / -10 false alarm.
Costs: same Landauer schedule as marketplace.py.

The question: in a swan world, does frantic adaptation beat strategic
ignorance? And how do the exchange rates reprice vs the calm world?
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(33)
LN2 = np.log(2)
N = 1000
WARM = 150

# ---------------------------------------------------------------- stream: long regimes + swans
REGIMES = [0.25, 0.50, 0.75]
SWAN_BIAS = [0.92, 0.08, 0.92]
swan_times = [300 + rng.integers(-40, 40), 550 + rng.integers(-40, 40),
              800 + rng.integers(-40, 40)]
SWAN_LEN = 25

bits, true_reg, is_swan = [], [], []
r = 1
for t in range(N):
    in_swan = any(abs(t - st) < SWAN_LEN // 2 for st in swan_times)
    if in_swan:
        idx = next(i for i, st in enumerate(swan_times) if abs(t - st) < SWAN_LEN // 2)
        true_reg.append(3)
        is_swan.append(True)
        bits.append(1 if rng.random() < SWAN_BIAS[idx] else 0)
    else:
        if rng.random() < 1 / 120:
            r = rng.integers(0, 3)
        true_reg.append(r)
        is_swan.append(False)
        bits.append(1 if rng.random() < REGIMES[r] else 0)
bits = np.array(bits); true_reg = np.array(true_reg); is_swan = np.array(is_swan)
print(f"swans at {sorted(swan_times)}, total swan steps: {is_swan.sum()}")
warm_bias = []
for k in range(3):
    m = bits[:WARM][true_reg[:WARM] == k]
    warm_bias.append(m.mean() if len(m) > 0 else 0.5)  # unseen regime -> max ignorance

# ---------------------------------------------------------------- GATE (with swan-mode boost)
GDIM = 6
GA = -(0.4 + 0.6 * np.arange(GDIM) / GDIM)
GB = rng.normal(0, 0.5, (GDIM, 2))
QBIT = 1

def gate_delta(surprise, scale):
    return np.log1p(np.exp(scale * (3.0 * surprise - 1.0)))

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
        for t in range(WARM):
            x = np.array([bits[t], 1 - bits[t]])
            pred_m = np.mean(bits[max(0, t - 10):t]) if t > 0 else 0.5
            d = gate_delta(abs(bits[t] - pred_m), 1.0)
            self.h = np.exp(d * GA) * self.h + (d * GB) @ x
        self.t = WARM
        self.surprises = []
    def step(self):
        t = self.t
        x = np.array([bits[t - 1], 1 - bits[t - 1]])
        pred_m = np.mean(bits[t - 10:t - 1])
        s = abs(bits[t - 1] - pred_m)
        self.surprises.append(s)
        # swan mode: frantic adaptation
        swan = np.mean(self.surprises[-10:]) > 0.35 if len(self.surprises) >= 10 else False
        scale = 2.5 if swan else 1.0
        d = gate_delta(s, scale)
        cost = LN2 * float(np.sum(1 - np.exp(d * GA)) * QBIT) + 0.1
        self.h = np.exp(d * GA) * self.h + (d * GB) @ x
        p = float(1 / (1 + np.exp(-(self.h @ w[:GDIM] + w[GDIM]))))
        self.t += 1
        return p, cost, swan

# ---------------------------------------------------------------- JEPA (with strategic ignorance)
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
            # strategic ignorance: predict 0.5, pay nothing, check exit
            recent = bits[t - 8:t]
            # exit swan mode if calm returns
            if abs(recent.mean() - 0.5) < 0.2:
                self.swan_mode = False
            self.t += 1
            self.updates.append(False)
            return 0.5, LN2 * 0.5, self.latent, True
        recent = bits[t - 8:t]
        surprise = abs(recent.mean() - self.bias[self.latent])
        update = surprise > 0.12
        self.updates.append(update)
        # enter swan mode if updating frantically
        if len(self.updates) >= 10 and sum(self.updates[-10:]) >= 8:
            self.swan_mode = True
        if update:
            cost = LN2 * 6 + LN2 * 1
            win = bits[t - 15:t].mean()
            self.latent = int(np.argmin([abs(win - b) for b in self.bias]))
        else:
            cost = LN2 * 1
        self.t += 1
        return self.bias[self.latent], cost, self.latent, self.swan_mode

# ---------------------------------------------------------------- GENIE (stops dreaming in chaos)
counts = np.zeros((2, 2, 2))
for t in range(2, WARM):
    counts[bits[t - 2], bits[t - 1], bits[t]] += 1
Pmk = (counts[:, :, 1] + 0.5) / (counts.sum(axis=2) + 1)

class Genie:
    def __init__(self):
        self.t = WARM
        self.lls = []
    def step(self):
        t = self.t
        b1, b2 = bits[t - 2], bits[t - 1]
        # likelihood of recent bits under model
        ll = 0.0
        for i in range(max(2, t - 10), t):
            p1 = Pmk[bits[i - 2], bits[i - 1]]
            ll += bits[i] * np.log(p1 + 1e-9) + (1 - bits[i]) * np.log(1 - p1 + 1e-9)
        self.lls.append(ll / 10)
        swan = (ll / 10) < -0.9 if len(self.lls) >= 5 else False
        depth = 1 if swan else 3
        cost = 1.0
        bb1, bb2 = b1, b2
        p_next = Pmk[bb1, bb2]
        p_fut = None
        # dream for futures (t+10)
        for _ in range(10 if not swan else 0):
            p1 = Pmk[bb1, bb2]
            bb1, bb2 = bb2, 1 if p1 > 0.5 else 0
            cost += 1.2
        if not swan:
            # p(t+10) from deterministic dream rollout
            p_fut = Pmk[bb1, bb2]
        self.t += 1
        return p_next, p_fut, cost, swan

# ---------------------------------------------------------------- the market
gate, jepa, genie = Gate(), JEPA(), Genie()
wealth = {"gate": 200.0, "jepa": 200.0, "genie": 200.0}
alive = {"gate": True, "jepa": True, "genie": True}
acc = {"gate": [], "jepa": [], "genie": []}
spent = {"gate": 0.0, "jepa": 0.0, "genie": 0.0}
swan_calls = {"gate": [], "jepa": [], "genie": []}
Wh = {"gate": [], "jepa": [], "genie": []}

for t in range(WARM, N - 10):
    if alive["gate"]:
        p, cost, swan = gate.step()
        win = 6 if (p > 0.5) == bits[t] else 0
        if t % 20 == 0:
            win += 20 if int(np.argmin([abs(p - b) for b in warm_bias])) == true_reg[t] else 0
        if t % 10 == 0:
            hit = is_swan[t]
            swan_calls["gate"].append(swan == hit)
            win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
        wealth["gate"] += win - cost
        spent["gate"] += cost
        acc["gate"].append((p > 0.5) == bits[t])
        if wealth["gate"] < 0: alive["gate"] = False
    if alive["jepa"]:
        p, cost, latent, swan = jepa.step()
        win = 6 if (p > 0.5) == bits[t] else 0
        if t % 20 == 0:
            win += 20 if (not swan and latent == true_reg[t]) else 0
        if t % 10 == 0:
            hit = is_swan[t]
            swan_calls["jepa"].append(swan == hit)
            win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
        wealth["jepa"] += win - cost
        spent["jepa"] += cost
        acc["jepa"].append((p > 0.5) == bits[t])
        if wealth["jepa"] < 0: alive["jepa"] = False
    if alive["genie"]:
        p, p_fut, cost, swan = genie.step()
        win = 6 if (p > 0.5) == bits[t] else 0
        if p_fut is not None:
            win += 12 if (p_fut > 0.5) == bits[t + 10] else 0
        if t % 20 == 0:
            win10 = bits[max(WARM, t - 10):t]
            lls = [np.sum(win10 * np.log(b + 1e-9) + (1 - win10) * np.log(1 - b + 1e-9))
                   for b in warm_bias]
            win += 20 if int(np.argmax(lls)) == true_reg[t] else 0
        if t % 10 == 0:
            hit = is_swan[t]
            swan_calls["genie"].append(swan == hit)
            win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
        wealth["genie"] += win - cost
        spent["genie"] += cost
        acc["genie"].append((p > 0.5) == bits[t])
        if wealth["genie"] < 0: alive["genie"] = False
    for name in Wh:
        Wh[name].append(max(wealth[name], Wh[name][-1] if Wh[name] else 0) if not alive[name]
                        else wealth[name])

print("\n=== THE MARKETPLACE II: long horizon + black swans ===")
for name in ("gate", "jepa", "genie"):
    a = np.mean(acc[name]) if acc[name] else 0
    eff = a / (spent[name] / max(len(acc[name]), 1)) * 100
    sc = np.mean(swan_calls[name]) if swan_calls[name] else 0
    print(f"{name:6s} | wealth {wealth[name]:8.1f} | alive {str(alive[name]):5s} | "
          f"acc {a:.3f} | swan-call {sc:.2f} | spent {spent[name]:8.1f} | {eff:.2f} acc/100c")
print(f"\nrichest -> poorest: {' > '.join(sorted(wealth, key=wealth.get, reverse=True))}")

fig, ax = plt.subplots(figsize=(13, 5))
for name, c in (("gate", "#2a7fff"), ("jepa", "#ff9f2a"), ("genie", "#b45cff")):
    ax.plot(Wh[name], color=c, label=name, lw=2)
for st in swan_times:
    ax.axvspan(st - WARM - 12, st - WARM + 12, color="red", alpha=0.12)
ax.axhline(0, color="k", ls="--", lw=1)
ax.set_xlabel("time step (from warmup end)")
ax.set_ylabel("wealth (energy coins)")
ax.set_title("Marketplace II: wealth through black swans (red bands)")
ax.legend()
fig.tight_layout()
fig.savefig("marketplace2.png", dpi=110)
print("\nwrote marketplace2.png")
