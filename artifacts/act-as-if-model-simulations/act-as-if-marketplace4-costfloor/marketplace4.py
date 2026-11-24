"""
MARKETPLACE IV — vary the cost floor.

M1-M3 varied the WORLD under a fixed cost (Landauer price = 1). This one
fixes the worlds and varies the COST FLOOR itself: every erasure cost is
multiplied by lam, the price of energy. Earnings are unchanged. The animals
don't re-tune (their dials are fixed) -- the floor moves under them.

  lam = 0    free erasure. Thermodynamics switched off.
  lam = 0.1  cheap.
  lam = 1    the M1/M2 baseline. Must reproduce M1 (calm: Gate 1201 >
             JEPA 931 > Genie 641) and M2 (swans: JEPA 1748 > Gate 879 >
             Genie bankrupt) exactly -- same seeds, same streams.
  lam = 3,10 expensive. Scarcity extreme.

Experiments:
  E1  lam-scan on the calm world (M1 stream, seed 21): final wealth vs lam.
  E2  Pareto dial-sweeps at lam in {0, 1, 10} on the calm world.
  E3  Swan world (M2 stream, seed 33) at lam in {0, 1, 10}.

PRE-REGISTERED PREDICTIONS (written before running):
  P1  lam=0 calm: wealth ranking = accuracy ranking -> JEPA >= Gate > Genie
      (M1 accuracies: JEPA 0.590, Gate 0.565). The Pareto frontier goes
      vertical: zero cost spread, frugality dominance vanishes.
  P2  lam=10 calm: the most frugal strategy wins; Genie bankrupt early;
      aggregate wealth collapses vs lam=1.
  P3  Crossover: there is a lam* in (0.1, 3) where the calm-world wealth
      ranking flips between Gate-first and JEPA-first.
  P4  lam=0 swans: Gate's frantic adaptation is free -> Gate >= JEPA.
      (World-relativity is cost-conditional.) lam=10 swans: JEPA's
      dominance widens; Gate bleeds faster.
  P5  For every lam>0, within-agent dial sweeps show frugality dominance
      (cheaper dial >= accuracy of lavish); at lam=0 the dominance is
      undefined -- no cost axis. The economic institution exists iff lam>0.

Headline hypothesis: cost isn't a dial. It's what makes the marketplace a
marketplace. At lam->0 the institution dissolves into a pure accuracy
contest -- prices don't just reprice, pricing breaks.

Honest limits: toy energy model throughout (see marketplace.py). The animals
do NOT re-tune their dials to lam -- a real agent would learn the price of
energy (that's a Marketplace V). lam scales the whole per-step cost,
including fixed overheads: it is the price of energy, not just of erasure.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LN2 = np.log(2)

# ================================================================ CALM WORLD (M1, seed 21)
rng = np.random.default_rng(21)
N = 600
WARM = 100
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

def run_calm(lam):
    gate, jepa, genie = Gate(), JEPA(), Genie()
    wealth = {"gate": 120.0, "jepa": 120.0, "genie": 120.0}
    alive = {"gate": True, "jepa": True, "genie": True}
    acc = {"gate": [], "jepa": [], "genie": []}
    spent = {"gate": 0.0, "jepa": 0.0, "genie": 0.0}
    Wh = {"gate": [], "jepa": [], "genie": []}
    for t in range(WARM, N - 3):
        if alive["gate"]:
            p, cost = gate.step(1.0); cost *= lam
            win = 6 if (p > 0.5) == bits[t] else 0
            if t % 10 == 0:
                win += 15 if int(np.argmin([abs(p - b) for b in warm_bias])) == true_reg[t] else 0
            wealth["gate"] += win - cost
            spent["gate"] += cost
            acc["gate"].append((p > 0.5) == bits[t])
            if wealth["gate"] < 0: alive["gate"] = False
        if alive["jepa"]:
            p, cost, latent = jepa.step(0.12); cost *= lam
            win = 6 if (p > 0.5) == bits[t] else 0
            if t % 10 == 0:
                win += 15 if latent == true_reg[t] else 0
            wealth["jepa"] += win - cost
            spent["jepa"] += cost
            acc["jepa"].append((p > 0.5) == bits[t])
            if wealth["jepa"] < 0: alive["jepa"] = False
        if alive["genie"]:
            p, p3, cost = genie.step(2); cost *= lam
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
    return wealth, acc, spent, alive, Wh

def train_gate_readout(scale):
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
    for t in range(WARM):
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
        e = 1.0 + depth * 1.2
        correct += (p1 > 0.5) == bits[t]
        energy += e
        n += 1
    return correct / n, energy / n

# ================================================================ SWAN WORLD (M2, seed 33)
rng2 = np.random.default_rng(33)
N2 = 1000
WARM2 = 150
REGIMES2 = [0.25, 0.50, 0.75]
SWAN_BIAS = [0.92, 0.08, 0.92]
swan_times = [300 + rng2.integers(-40, 40), 550 + rng2.integers(-40, 40),
              800 + rng2.integers(-40, 40)]
SWAN_LEN = 25

bits2, true_reg2, is_swan = [], [], []
r = 1
for t in range(N2):
    in_swan = any(abs(t - st) < SWAN_LEN // 2 for st in swan_times)
    if in_swan:
        idx = next(i for i, st in enumerate(swan_times) if abs(t - st) < SWAN_LEN // 2)
        true_reg2.append(3)
        is_swan.append(True)
        bits2.append(1 if rng2.random() < SWAN_BIAS[idx] else 0)
    else:
        if rng2.random() < 1 / 120:
            r = rng2.integers(0, 3)
        true_reg2.append(r)
        is_swan.append(False)
        bits2.append(1 if rng2.random() < REGIMES2[r] else 0)
bits2 = np.array(bits2); true_reg2 = np.array(true_reg2); is_swan = np.array(is_swan)
warm_bias2 = []
for k in range(3):
    m = bits2[:WARM2][true_reg2[:WARM2] == k]
    warm_bias2.append(m.mean() if len(m) > 0 else 0.5)

GA2 = GA; GB2 = rng2.normal(0, 0.5, (GDIM, 2))

gh2 = np.zeros(GDIM)
states2, ys2 = [], []
for t in range(WARM2):
    x = np.array([bits2[t], 1 - bits2[t]])
    pred_m = np.mean(bits2[max(0, t - 10):t]) if t > 0 else 0.5
    d = gate_delta(abs(bits2[t] - pred_m), 1.0)
    gh2 = np.exp(d * GA2) * gh2 + (d * GB2) @ x
    states2.append(gh2.copy()); ys2.append(bits2[t])
states2 = np.array(states2); ys2 = np.array(ys2)
w2 = np.zeros(GDIM + 1)
Xa2 = np.column_stack([states2, np.ones(len(states2))])
for _ in range(800):
    p = 1 / (1 + np.exp(-Xa2 @ w2))
    w2 -= 0.5 * Xa2.T @ (p - ys2) / len(ys2)

class Gate2:
    def __init__(self):
        self.h = np.zeros(GDIM)
        for t in range(WARM2):
            x = np.array([bits2[t], 1 - bits2[t]])
            pred_m = np.mean(bits2[max(0, t - 10):t]) if t > 0 else 0.5
            d = gate_delta(abs(bits2[t] - pred_m), 1.0)
            self.h = np.exp(d * GA2) * self.h + (d * GB2) @ x
        self.t = WARM2
        self.surprises = []
    def step(self):
        t = self.t
        x = np.array([bits2[t - 1], 1 - bits2[t - 1]])
        pred_m = np.mean(bits2[t - 10:t - 1])
        s = abs(bits2[t - 1] - pred_m)
        self.surprises.append(s)
        swan = np.mean(self.surprises[-10:]) > 0.35 if len(self.surprises) >= 10 else False
        scale = 2.5 if swan else 1.0
        d = gate_delta(s, scale)
        cost = LN2 * float(np.sum(1 - np.exp(d * GA2)) * QBIT) + 0.1
        self.h = np.exp(d * GA2) * self.h + (d * GB2) @ x
        p = float(1 / (1 + np.exp(-(self.h @ w2[:GDIM] + w2[GDIM]))))
        self.t += 1
        return p, cost, swan

class JEPA2:
    def __init__(self):
        self.latent = 1
        self.bias = list(warm_bias2)
        self.t = WARM2
        self.updates = []
        self.swan_mode = False
    def step(self):
        t = self.t
        if self.swan_mode:
            recent = bits2[t - 8:t]
            if abs(recent.mean() - 0.5) < 0.2:
                self.swan_mode = False
            self.t += 1
            self.updates.append(False)
            return 0.5, LN2 * 0.5, self.latent, True
        recent = bits2[t - 8:t]
        surprise = abs(recent.mean() - self.bias[self.latent])
        update = surprise > 0.12
        self.updates.append(update)
        if len(self.updates) >= 10 and sum(self.updates[-10:]) >= 8:
            self.swan_mode = True
        if update:
            cost = LN2 * 6 + LN2 * 1
            win = bits2[t - 15:t].mean()
            self.latent = int(np.argmin([abs(win - b) for b in self.bias]))
        else:
            cost = LN2 * 1
        self.t += 1
        return self.bias[self.latent], cost, self.latent, self.swan_mode

counts2 = np.zeros((2, 2, 2))
for t in range(2, WARM2):
    counts2[bits2[t - 2], bits2[t - 1], bits2[t]] += 1
Pmk2 = (counts2[:, :, 1] + 0.5) / (counts2.sum(axis=2) + 1)

class Genie2:
    def __init__(self):
        self.t = WARM2
        self.lls = []
    def step(self):
        t = self.t
        b1, b2 = bits2[t - 2], bits2[t - 1]
        ll = 0.0
        for i in range(max(2, t - 10), t):
            p1 = Pmk2[bits2[i - 2], bits2[i - 1]]
            ll += bits2[i] * np.log(p1 + 1e-9) + (1 - bits2[i]) * np.log(1 - p1 + 1e-9)
        self.lls.append(ll / 10)
        swan = (ll / 10) < -0.9 if len(self.lls) >= 5 else False
        cost = 1.0
        bb1, bb2 = b1, b2
        p_next = Pmk2[bb1, bb2]
        p_fut = None
        for _ in range(10 if not swan else 0):
            p1 = Pmk2[bb1, bb2]
            bb1, bb2 = bb2, 1 if p1 > 0.5 else 0
            cost += 1.2
        if not swan:
            p_fut = Pmk2[bb1, bb2]
        self.t += 1
        return p_next, p_fut, cost, swan

def run_swan(lam):
    gate, jepa, genie = Gate2(), JEPA2(), Genie2()
    wealth = {"gate": 200.0, "jepa": 200.0, "genie": 200.0}
    alive = {"gate": True, "jepa": True, "genie": True}
    acc = {"gate": [], "jepa": [], "genie": []}
    spent = {"gate": 0.0, "jepa": 0.0, "genie": 0.0}
    Wh = {"gate": [], "jepa": [], "genie": []}
    for t in range(WARM2, N2 - 10):
        if alive["gate"]:
            p, cost, swan = gate.step(); cost *= lam
            win = 6 if (p > 0.5) == bits2[t] else 0
            if t % 20 == 0:
                win += 20 if int(np.argmin([abs(p - b) for b in warm_bias2])) == true_reg2[t] else 0
            if t % 10 == 0:
                hit = is_swan[t]
                win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
            wealth["gate"] += win - cost
            spent["gate"] += cost
            acc["gate"].append((p > 0.5) == bits2[t])
            if wealth["gate"] < 0: alive["gate"] = False
        if alive["jepa"]:
            p, cost, latent, swan = jepa.step(); cost *= lam
            win = 6 if (p > 0.5) == bits2[t] else 0
            if t % 20 == 0:
                win += 20 if (not swan and latent == true_reg2[t]) else 0
            if t % 10 == 0:
                hit = is_swan[t]
                win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
            wealth["jepa"] += win - cost
            spent["jepa"] += cost
            acc["jepa"].append((p > 0.5) == bits2[t])
            if wealth["jepa"] < 0: alive["jepa"] = False
        if alive["genie"]:
            p, p_fut, cost, swan = genie.step(); cost *= lam
            win = 6 if (p > 0.5) == bits2[t] else 0
            if p_fut is not None:
                win += 12 if (p_fut > 0.5) == bits2[t + 10] else 0
            if t % 20 == 0:
                win10 = bits2[max(WARM2, t - 10):t]
                lls = [np.sum(win10 * np.log(b + 1e-9) + (1 - win10) * np.log(1 - b + 1e-9))
                       for b in warm_bias2]
                win += 20 if int(np.argmax(lls)) == true_reg2[t] else 0
            if t % 10 == 0:
                hit = is_swan[t]
                win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
            wealth["genie"] += win - cost
            spent["genie"] += cost
            acc["genie"].append((p > 0.5) == bits2[t])
            if wealth["genie"] < 0: alive["genie"] = False
        for name in Wh:
            Wh[name].append(wealth[name] if alive[name] else (Wh[name][-1] if Wh[name] else 0))
    return wealth, acc, spent, alive, Wh

# ================================================================ E1: lam scan, calm world
print("=== MARKETPLACE IV: varying the cost floor ===\n")
print("--- E1: lam scan, calm world ---")
scan_lams = [1.0, 0.0, 0.1, 0.3, 3.0, 10.0]
scan = {}
for lam in scan_lams:
    wealth, acc, spent, alive, Wh = run_calm(lam)
    scan[lam] = (wealth, acc, spent, alive, Wh)
    line = f"lam={lam:>4}: "
    for name in ("gate", "jepa", "genie"):
        a = np.mean(acc[name]) if acc[name] else 0
        n = max(len(acc[name]), 1)
        eff = a / (spent[name] / n) * 100 if spent[name] > 0 else float("nan")
        es = f"{eff:6.1f}" if spent[name] > 0 else "    --"
        line += (f"{name} W={wealth[name]:8.1f} acc={a:.3f} spent={spent[name]:7.1f} "
                 f"eff={es} alive={alive[name]} | ")
    print(line)

w1 = scan[1.0][0]
print(f"\nM1 reproduction check (lam=1): Gate {w1['gate']:.0f} (exp 1201), "
      f"JEPA {w1['jepa']:.0f} (exp 931), Genie {w1['genie']:.0f} (exp 641)")

def ranking(wealth):
    return tuple(sorted(wealth, key=wealth.get, reverse=True))

print("\n--- E1 verdicts ---")
r0 = ranking(scan[0.0][0])
print(f"P1 lam=0 ranking: {' > '.join(r0)} -> "
      f"{'PASS' if r0[0] == 'jepa' and r0[-1] == 'genie' else 'FAIL'} (predicted JEPA >= Gate > Genie)")
w10 = scan[10.0][0]
p2pass = (not scan[10.0][3]["genie"]) and sum(w10.values()) < sum(w1.values())
print(f"P2 lam=10: Genie bankrupt={not scan[10.0][3]['genie']}, "
      f"aggregate {sum(w10.values()):.0f} vs lam=1 {sum(w1.values()):.0f} -> "
      f"{'PASS' if p2pass else 'FAIL'}")
order = [0.0, 0.1, 0.3, 1.0, 3.0, 10.0]
flips = [f"{order[i]}->{order[i+1]}" for i in range(len(order) - 1)
         if ranking(scan[order[i]][0]) != ranking(scan[order[i + 1]][0])]
print(f"P3 crossover lam*: ranking flips at {flips} -> "
      f"{'PASS' if any(float(f.split('->')[0]) >= 0.1 and float(f.split('->')[1]) <= 3.0 for f in flips) else 'FAIL'} "
      f"(predicted a flip inside (0.1, 3))")

# ================================================================ E2: Pareto at lam in {0,1,10}
print("\n--- E2: Pareto dial-sweeps at lam = 0, 1, 10 ---")
pareto = {}
for lam in (0.0, 1.0, 10.0):
    pareto[lam] = {}
    for name, dials, fn in [("gate", [0.5, 1.0, 2.0], sweep_gate),
                            ("jepa", [0.20, 0.12, 0.05], sweep_jepa),
                            ("genie", [1, 2, 3], sweep_genie)]:
        pts = []
        for d in dials:
            a, e = fn(d)
            pts.append((a, e * lam))
        pareto[lam][name] = pts
        print(f"  lam={lam}: {name:6s} " +
              " ".join(f"d={d}: acc {a:.3f} e {e*lam:.2f}" for (a, e), d in zip(pts, dials)))

def frugal_dominates(pts):
    # pts ordered frugal -> lavish: does the cheapest dial match/exceed lavish accuracy?
    return pts[0][0] >= pts[-1][0] - 1e-9

p5 = all(frugal_dominates(pareto[lam][n]) for lam in (1.0, 10.0) for n in ("gate", "jepa", "genie"))
print(f"P5 frugality dominance at lam>0: {'PASS' if p5 else 'FAIL'} "
      f"(at lam=0 the cost axis is degenerate by construction)")

# ================================================================ E3: swan world at lam in {0,1,10}
print("\n--- E3: swan world at lam = 0, 1, 10 ---")
swanres = {}
for lam in (1.0, 0.0, 10.0):
    wealth, acc, spent, alive, Wh = run_swan(lam)
    swanres[lam] = (wealth, acc, spent, alive, Wh)
    line = f"lam={lam:>4}: "
    for name in ("gate", "jepa", "genie"):
        a = np.mean(acc[name]) if acc[name] else 0
        line += f"{name} W={wealth[name]:8.1f} acc={a:.3f} alive={alive[name]} | "
    line += f"ranking: {' > '.join(ranking(wealth))}"
    print(line)

ws1 = swanres[1.0][0]
print(f"\nM2 reproduction check (lam=1): JEPA {ws1['jepa']:.0f} (exp 1748), "
      f"Gate {ws1['gate']:.0f} (exp 879), Genie alive={swanres[1.0][3]['genie']} (exp False)")
r = ranking(swanres[0.0][0])
gw, jw = swanres[0.0][0]["gate"], swanres[0.0][0]["jepa"]
print(f"P4 lam=0 swans ranking: {' > '.join(r)} -> "
      f"{'PASS' if gw >= jw else 'FAIL'} (predicted Gate >= JEPA: world-relativity is cost-conditional)")
r10 = ranking(swanres[10.0][0])
widened = (swanres[10.0][0]["jepa"] - swanres[10.0][0]["gate"]) > (ws1["jepa"] - ws1["gate"])
print(f"P4b lam=10 swans ranking: {' > '.join(r10)}, JEPA-Gate gap widened vs lam=1: {widened} -> "
      f"{'PASS' if r10[0]=='jepa' and widened else 'FAIL'}")

# ================================================================ plots
fig1, ax1 = plt.subplots(figsize=(9, 5.5))
xs = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
for name, c in (("gate", "#2a7fff"), ("jepa", "#ff9f2a"), ("genie", "#b45cff")):
    ys = [scan[l][0][name] for l in order]
    ax1.plot(xs, ys, "o-", color=c, label=name, lw=2, ms=7)
ax1.set_xscale("log")
ax1.set_xticks(xs)
ax1.set_xticklabels(["0 (free)", "0.1", "0.3", "1", "3", "10"])
ax1.axvline(1.0, color="gray", ls=":", lw=1)
ax1.text(1.05, ax1.get_ylim()[1] * 0.95, "M1 baseline", fontsize=9, color="gray")
ax1.axhline(0, color="k", ls="--", lw=1)
ax1.set_xlabel("cost floor  lam  (price of energy)")
ax1.set_ylabel("final wealth (energy coins)")
ax1.set_title("Marketplace IV: final wealth vs the cost floor (calm world)")
ax1.legend()
fig1.tight_layout()
fig1.savefig("marketplace4_crossover.png", dpi=110)
print("\nwrote marketplace4_crossover.png")

fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
for ax, lam in zip(axes2, (0.0, 1.0, 10.0)):
    for name, c in (("gate", "#2a7fff"), ("jepa", "#ff9f2a"), ("genie", "#b45cff")):
        pts = pareto[lam][name]
        ax.scatter([e for a, e in pts], [a for a, e in pts], color=c, s=90, label=name, zorder=3)
        for (a, e), lbl in zip(pts, ("frugal", "normal", "lavish")):
            ax.annotate(lbl, (e, a), xytext=(5, 5), textcoords="offset points", fontsize=8, color=c)
    ax.set_xlabel("energy per step (coins)")
    ax.set_title(f"lam = {lam:g}")
axes2[0].set_ylabel("next-bit accuracy")
axes2[1].legend()
fig2.suptitle("Pareto frontiers under three cost floors (calm world)")
fig2.tight_layout()
fig2.savefig("marketplace4_pareto.png", dpi=110)
print("wrote marketplace4_pareto.png")

fig3, axes3 = plt.subplots(1, 3, figsize=(16, 5), sharey=True)
for ax, lam in zip(axes3, (0.0, 1.0, 10.0)):
    Wh = swanres[lam][4]
    for name, c in (("gate", "#2a7fff"), ("jepa", "#ff9f2a"), ("genie", "#b45cff")):
        ax.plot(Wh[name], color=c, label=name, lw=1.6)
    for st in swan_times:
        ax.axvspan(st - WARM2 - 12, st - WARM2 + 12, color="red", alpha=0.12)
    ax.axhline(0, color="k", ls="--", lw=1)
    ax.set_xlabel("time step (from warmup end)")
    ax.set_title(f"swans, lam = {lam:g}")
axes3[0].set_ylabel("wealth (energy coins)")
axes3[1].legend()
fig3.suptitle("Marketplace IV: swan world under three cost floors")
fig3.tight_layout()
fig3.savefig("marketplace4_swans.png", dpi=110)
print("wrote marketplace4_swans.png")
