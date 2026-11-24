"""
MARKETPLACE VI — the zero-spend animal meets the cost floor.

Main chat's zoo grew a fourth animal: the REACTIVE. It predicts the last
bit. No model, no memory beyond one step, no concept of swans — and it won
the swan world (wealth 3530) by spending zero. "Representation is overhead;
where the world persists, coupling beats modeling."

This experiment crosses that animal with this side chat's floor: the
Reactive (cost identically 0) is λ-INVARIANT — the price of energy cannot
touch it. It is the λ→∞ asymptote made flesh, Genie's dark twin (no-model
vs full-model), and the decay-without-growth complement (it accumulates
nothing — pure coupling, the anti of Hydra's eternal growth).

Animals: Gate, JEPA, Genie (M4 versions, fixed normal dials) + Reactive.
Reactive: p = last bit, cost = 0, no regime/futures/swan-call earnings
(it has no concepts to earn them with — disclosed, this is the point).

E1: calm world (M1 stream, seed 21), lam in {0, 0.3, 1, 3, 10}.
E2: swan world (M2 stream, seed 33, M2 scoring), lam in {0, 1, 10}.

PRE-REGISTERED PREDICTIONS (written before running):
  P1  Reactive wealth is IDENTICAL across lam within each world
      (structural: cost 0 * lam = 0; earnings don't depend on lam).
  P2  Calm: rank(Reactive) is non-decreasing in lam.
  P3  Swans: rank(Reactive) strictly rises with lam — not first at lam=0
      (bonus collectors beat pure coupling), first at lam=10 (sole
      survivor; it cannot go bankrupt).
  P4  Main's headline ("coupling beats modeling", measured at lam=1) is
      price-conditional: holds at lam>=1, fails at lam=0.

Honest limits: toy energy model throughout. Reactive sits out every niche
earning (regime/futures/swan calls) — its wealth is pure next-bit coupling.
Post-run wording correction (2026-10-15, from the ledger audit): P3's
"strictly rises" was imprecise as preregistered — ordinal rank is
non-decreasing (3rd→1st→1st; saturates at 1st, a ceiling effect) while
dominance strictly increases (gap to 2nd 1362→3113, survivors 3→1).
Endpoints passed as operationalized; the adverb was wrong. Recorded as a
correction, not a silent revision.
Fixed normal dials for the other three (the M4 baseline). The calm stream is
persistent (regimes ~35 steps), which favors coupling by construction —
the world, not just the animal, is on trial here.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LN2 = np.log(2)

# ================================================================ CALM WORLD (seed 21)
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

class Reactive:
    """Predict the last bit. Spend nothing. Accumulate nothing."""
    def __init__(self):
        self.t = WARM
    def step(self):
        t = self.t
        p = float(bits[t - 1])
        self.t += 1
        return p, 0.0

def run_calm(lam):
    gate, jepa, genie, reactive = Gate(), JEPA(), Genie(), Reactive()
    wealth = {"gate": 120.0, "jepa": 120.0, "genie": 120.0, "reactive": 120.0}
    alive = {k: True for k in wealth}
    acc = {k: [] for k in wealth}
    Wh = {k: [] for k in wealth}
    for t in range(WARM, N - 3):
        if alive["gate"]:
            p, cost = gate.step(1.0); cost *= lam
            win = 6 if (p > 0.5) == bits[t] else 0
            if t % 10 == 0:
                win += 15 if int(np.argmin([abs(p - b) for b in warm_bias])) == true_reg[t] else 0
            wealth["gate"] += win - cost
            acc["gate"].append((p > 0.5) == bits[t])
            if wealth["gate"] < 0: alive["gate"] = False
        if alive["jepa"]:
            p, cost, latent = jepa.step(0.12); cost *= lam
            win = 6 if (p > 0.5) == bits[t] else 0
            if t % 10 == 0:
                win += 15 if latent == true_reg[t] else 0
            wealth["jepa"] += win - cost
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
            acc["genie"].append((p > 0.5) == bits[t])
            if wealth["genie"] < 0: alive["genie"] = False
        if alive["reactive"]:
            p, cost = reactive.step()  # cost is 0.0; lam cannot touch it
            win = 6 if (p > 0.5) == bits[t] else 0
            wealth["reactive"] += win
            acc["reactive"].append((p > 0.5) == bits[t])
            if wealth["reactive"] < 0: alive["reactive"] = False  # unreachable: earnings >= 0
        for k in Wh:
            Wh[k].append(wealth[k])
    return wealth, acc, alive, Wh

# ================================================================ SWAN WORLD (seed 33)
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

class Reactive2:
    def __init__(self):
        self.t = WARM2
    def step(self):
        t = self.t
        p = float(bits2[t - 1])
        self.t += 1
        return p, 0.0

def run_swan(lam):
    gate, jepa, genie, reactive = Gate2(), JEPA2(), Genie2(), Reactive2()
    wealth = {"gate": 200.0, "jepa": 200.0, "genie": 200.0, "reactive": 200.0}
    alive = {k: True for k in wealth}
    acc = {k: [] for k in wealth}
    Wh = {k: [] for k in wealth}
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
            acc["genie"].append((p > 0.5) == bits2[t])
            if wealth["genie"] < 0: alive["genie"] = False
        if alive["reactive"]:
            p, cost = reactive.step()
            win = 6 if (p > 0.5) == bits2[t] else 0
            # no swan-call bonus: it has no swan concept. No regime calls either.
            wealth["reactive"] += win
            acc["reactive"].append((p > 0.5) == bits2[t])
            if wealth["reactive"] < 0: alive["reactive"] = False  # unreachable
        for k in Wh:
            Wh[k].append(wealth[k] if alive[k] else (Wh[k][-1] if Wh[k] else 0))
    return wealth, acc, alive, Wh

# ================================================================ E1: calm lam-scan
def ranking(wealth):
    return tuple(sorted(wealth, key=wealth.get, reverse=True))

print("=== MARKETPLACE VI: the zero-spend animal meets the cost floor ===\n")
print("--- E1: calm world, lam = 0, 0.3, 1, 3, 10 ---")
e1 = {}
for lam in (0.0, 0.3, 1.0, 3.0, 10.0):
    wealth, acc, alive, Wh = run_calm(lam)
    e1[lam] = (wealth, acc, alive, Wh)
    ra = np.mean(acc["reactive"]) if acc["reactive"] else 0
    print(f"lam={lam:>4}: " + " | ".join(
        f"{k} W={wealth[k]:8.1f} alive={alive[k]}" for k in ("gate", "jepa", "genie", "reactive")) +
        f" || reactive acc={ra:.3f} || ranking: {' > '.join(ranking(wealth))}")

print("\n--- E1 verdicts ---")
rw = [e1[lam][0]["reactive"] for lam in (0.0, 0.3, 1.0, 3.0, 10.0)]
print(f"P1 reactive wealth across lam: {[f'{x:.0f}' for x in rw]} -> "
      f"{'PASS' if max(rw) - min(rw) < 1e-6 else 'FAIL'} (identical = lam-invariance)")
ranks = [ranking(e1[lam][0]).index("reactive") for lam in (0.0, 0.3, 1.0, 3.0, 10.0)]
print(f"P2 calm reactive rank (0=first) across lam: {ranks} -> "
      f"{'PASS' if all(ranks[i] >= ranks[i + 1] for i in range(4)) else 'FAIL'} "
      f"(predicted rank non-decreasing = index non-increasing)")

# ================================================================ E2: swan lam-scan
print("\n--- E2: swan world, lam = 0, 1, 10 ---")
e2 = {}
for lam in (0.0, 1.0, 10.0):
    wealth, acc, alive, Wh = run_swan(lam)
    e2[lam] = (wealth, acc, alive, Wh)
    print(f"lam={lam:>4}: " + " | ".join(
        f"{k} W={wealth[k]:8.1f} alive={alive[k]}" for k in ("gate", "jepa", "genie", "reactive")) +
        f" || ranking: {' > '.join(ranking(wealth))}")

print("\n--- E2 verdicts ---")
rw2 = [e2[lam][0]["reactive"] for lam in (0.0, 1.0, 10.0)]
print(f"P1b reactive wealth across lam (swans): {[f'{x:.0f}' for x in rw2]} -> "
      f"{'PASS' if max(rw2) - min(rw2) < 1e-6 else 'FAIL'}")
r0 = ranking(e2[0.0][0]).index("reactive")
r10 = ranking(e2[10.0][0]).index("reactive")
print(f"P3 swan reactive rank: lam=0 -> {r0} (0=first), lam=10 -> {r10} -> "
      f"{'PASS' if r0 > 0 and r10 == 0 else 'FAIL'} (not-first at 0, first at 10)")
r1 = ranking(e2[1.0][0]).index("reactive")
print(f"P4 coupling-beats-modeling at lam=1: reactive rank {r1} -> "
      f"{'PASS' if r1 == 0 else 'FAIL'}; at lam=0: rank {r0} -> "
      f"{'PASS' if r0 > 0 else 'FAIL'} (headline holds at lam>=1, fails at lam=0)")

# ================================================================ plots
fig1, ax1 = plt.subplots(figsize=(9, 5.5))
xs = [0.03, 0.3, 1.0, 3.0, 10.0]
order = [0.0, 0.3, 1.0, 3.0, 10.0]
for name, c in (("gate", "#2a7fff"), ("jepa", "#ff9f2a"), ("genie", "#b45cff"), ("reactive", "#2ca02c")):
    ys = [e1[l][0][name] for l in order]
    ax1.plot(xs, ys, "o-", color=c, label=name, lw=2, ms=7)
ax1.set_xscale("log")
ax1.set_xticks(xs)
ax1.set_xticklabels(["0 (free)", "0.3", "1", "3", "10"])
ax1.axhline(0, color="k", ls="--", lw=1)
ax1.set_xlabel("cost floor  lam  (price of energy)")
ax1.set_ylabel("final wealth (energy coins)")
ax1.set_title("Marketplace VI: the zero-spend animal is lam-invariant (calm world)")
ax1.legend()
fig1.tight_layout()
fig1.savefig("marketplace6_calm.png", dpi=110)
print("\nwrote marketplace6_calm.png")

fig2, ax2 = plt.subplots(figsize=(8, 5.5))
xs2 = [0.0, 1.0, 10.0]
for name, c in (("gate", "#2a7fff"), ("jepa", "#ff9f2a"), ("genie", "#b45cff"), ("reactive", "#2ca02c")):
    ys = [e2[l][0][name] for l in xs2]
    ax2.plot(xs2, ys, "o-", color=c, label=name, lw=2, ms=8)
ax2.axhline(0, color="k", ls="--", lw=1)
ax2.set_xlabel("cost floor  lam")
ax2.set_ylabel("final wealth (energy coins)")
ax2.set_title("Marketplace VI: swan world — coupling wins iff spending kills")
ax2.legend()
fig2.tight_layout()
fig2.savefig("marketplace6_swans.png", dpi=110)
print("wrote marketplace6_swans.png")
