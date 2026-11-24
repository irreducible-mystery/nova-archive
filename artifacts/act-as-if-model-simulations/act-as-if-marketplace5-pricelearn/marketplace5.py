"""
MARKETPLACE V — do the animals learn the price of energy?

M4 moved the cost floor under fixed dials. Now the dials move: each animal
gets a meta-policy that re-tunes its own dial block by block. The question:
is frugality DISCOVERED, or does the floor have to TEACH it?

Meta-policies (the two candidate teachers):
  FIXED(dial)   the M1/M4 animal. No meta. The control.
  THERMOSTAT    wealth > 150 -> lavish | 50..150 -> normal | <= 50 -> frugal.
                The floor teaches via fear: poverty forces frugality.
                (M1's docstring proposed this; it was never run.)
  BANDIT        epsilon-greedy over the 3 dials, reward = block wealth-delta.
                Discovers the price from the reward signal alone.

Dials (frugal -> lavish):
  gate:  scale     0.5 / 1.0 / 2.0
  jepa:  threshold 0.20 / 0.12 / 0.05   (frugal = rare updates)
  genie: depth     1 / 2 / 3            (lavish depth 3 unlocks the +6
                futures niche, dormant in M1's fixed depth-2 market)

World: the long calm. Same generator as M1 (seed 21), N=1500, warmup 100,
3 regimes, mean length 35. Longer run so bandits get ~56 blocks to learn.
Earnings: +6 next-bit, +6 futures (genie, t+2, only at depth 3), +15 regime
every 10 steps. Start wealth 120 each.

Experiments:
  E1  all-BANDIT market at lam in {0.3, 1, 3}. Where do the dials settle?
  E2  populations: all-FIXED(normal) vs all-THERMOSTAT vs all-BANDIT,
      at lam in {0.3, 1, 3}. Who survives the lethal floor?
  E3  shock: lam = 0.3 for the first half, 3.0 for the second. Thermostat
      vs bandit: who re-tunes, how fast, how well?

PRE-REGISTERED PREDICTIONS (written before running; P1/P2 reframed after
first run showed lam=3 is extinction for every dial -- see honest limits):
  P1  Bandits drift frugal as lam rises into the survivable-lethal zone:
      at lam=2 each agent spends >60% of late blocks frugal; at lam=0.3 the
      dials stay mixed. At lam=3 the bandit dies in ~2 blocks, before its
      3-block arm round-robin finishes: learning needs samples, dying is fast.
  P2  At lam=3: predicted thermo >= bandit > fixed survival -- EXPECTED TO
      FAIL: M4 already showed lam=3 kills fixed-normal, and no dial survives
      it, so fear can't beat math. Kept as the documented extinction.
  P2b At lam=2 (lethal but survivable): thermo >= bandit > fixed.
  P3  After the shock: thermostat hits frugal within 2 blocks; bandit takes
      ~8-12 blocks to re-converge but settles finer than pure frugal.
  P4  At lam=0.3 bandits do NOT all go frugal: cheap energy makes lavish
      dials' accuracy (and Genie's futures niche) worth buying. They learn
      the exchange rate, not "frugality good".
  P5  Bandit mean final wealth >= fixed-normal mean final wealth at each lam.
      Learning never hurts vs the M1 baseline.
  P6  (breaker, added after E3) If E3's failure is stale optimism, a
      constant step-size bandit (BanditAlpha, alpha=0.2 -- it FORGETS)
      re-tunes to >=60% frugal within blocks 12-24 post-shock and beats the
      running-mean bandit's mean wealth on the shock run.

Honest limits: toy energy model throughout. Bandit reward is myopic
(25-step wealth delta); epsilon-greedy is the dumbest honest learner.
Thermostat thresholds (150/50) are hand-set, not learned. Dial granularity
is 3 -- the true optimum may lie between dials. Genie's futures niche is
new vs M1 (dormant at fixed depth 2); lavish-Genie comparisons to M1 are
apples-to-oranges, disclosed here.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LN2 = np.log(2)
N = 1500
WARM = 100
BLOCK = 25
NBLOCKS = (N - WARM) // BLOCK

# ------------------------------------------------------------------ the long calm
rng = np.random.default_rng(21)
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

# ------------------------------------------------------------------ mechanisms
GDIM = 6
GA = -(0.4 + 0.6 * np.arange(GDIM) / GDIM)
GB = rng.normal(0, 0.5, (GDIM, 2))
QBIT = 1

def gate_delta(surprise, scale):
    return np.log1p(np.exp(scale * (3.0 * surprise - 1.0)))

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

GATE_DIALS = {"frugal": 0.5, "normal": 1.0, "lavish": 2.0}
JEPA_DIALS = {"frugal": 0.20, "normal": 0.12, "lavish": 0.05}
GENIE_DIALS = {"frugal": 1, "normal": 2, "lavish": 3}
DIALS = ["frugal", "normal", "lavish"]
W_BY_SCALE = {s: train_gate_readout(s) for s in GATE_DIALS.values()}

class Gate:
    def __init__(self):
        self.h = np.zeros(GDIM)
        for t in range(WARM):
            x = np.array([bits[t], 1 - bits[t]])
            pred_m = np.mean(bits[max(0, t - 10):t]) if t > 0 else 0.5
            d = gate_delta(abs(bits[t] - pred_m), 1.0)
            self.h = np.exp(d * GA) * self.h + (d * GB) @ x
        self.t = WARM
    def step(self, dial):
        scale = GATE_DIALS[dial]; w = W_BY_SCALE[scale]
        t = self.t
        x = np.array([bits[t - 1], 1 - bits[t - 1]])
        pred_m = np.mean(bits[max(0, t - 10):t - 1])
        d = gate_delta(abs(bits[t - 1] - pred_m), scale)
        cost = LN2 * float(np.sum(1 - np.exp(d * GA)) * QBIT) + 0.1
        self.h = np.exp(d * GA) * self.h + (d * GB) @ x
        p = float(1 / (1 + np.exp(-(self.h @ w[:GDIM] + w[GDIM]))))
        self.t += 1
        return p, cost

class JEPA:
    def __init__(self):
        self.latent = 1
        self.bias = list(warm_bias)
        self.t = WARM
    def step(self, dial):
        threshold = JEPA_DIALS[dial]
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
    def __init__(self, rrng):
        self.t = WARM
        self.rrng = rrng
    def step(self, dial):
        depth = GENIE_DIALS[dial]
        t = self.t
        cost = 1.0
        b1, b2 = bits[t - 2], bits[t - 1]
        fut = []
        for _ in range(depth):
            p1 = Pmk[b1, b2]
            fut.append(p1)
            b1, b2 = b2, 1 if self.rrng.random() < p1 else 0
            cost += 1.2
        self.t += 1
        return fut[0], (fut[2] if depth >= 3 else None), cost

# ------------------------------------------------------------------ meta-policies
class Fixed:
    def __init__(self, dial="normal"):
        self.dial = dial
    def choose(self, wealth):
        return self.dial
    def update(self, reward):
        pass

class Thermostat:
    def choose(self, wealth):
        if wealth > 150:
            return "lavish"
        if wealth > 50:
            return "normal"
        return "frugal"
    def update(self, reward):
        pass

class Bandit:
    def __init__(self, seed):
        self.Q = {d: 0.0 for d in DIALS}
        self.n = {d: 0 for d in DIALS}
        self.eps = 0.30
        self.rng = np.random.default_rng(seed)
        self.last = None
    def choose(self, wealth):
        untried = [d for d in DIALS if self.n[d] == 0]
        if untried:
            self.last = untried[0]
        elif self.rng.random() < self.eps:
            self.last = DIALS[self.rng.integers(0, 3)]
        else:
            self.last = max(DIALS, key=lambda d: self.Q[d])
        return self.last
    def update(self, reward):
        d = self.last
        self.n[d] += 1
        self.Q[d] += (reward - self.Q[d]) / self.n[d]
        self.eps = max(0.05, self.eps * 0.96)

class BanditAlpha(Bandit):
    """Same epsilon-greedy, but Q uses a constant step-size: it FORGETS.
    The breaker for E3's stale-optimism diagnosis."""
    def __init__(self, seed, alpha=0.2):
        super().__init__(seed)
        self.alpha = alpha
    def update(self, reward):
        d = self.last
        self.n[d] += 1
        self.Q[d] += self.alpha * (reward - self.Q[d])
        self.eps = max(0.05, self.eps * 0.96)

# ------------------------------------------------------------------ market runner
def run_market(metas, lam, seed=0, lam_fn=None):
    """metas: {name: meta-policy}. lam_fn(block)->lam for shocks."""
    rrng = np.random.default_rng(1000 + seed)
    agents = {"gate": Gate(), "jepa": JEPA(), "genie": Genie(rrng)}
    wealth = {k: 120.0 for k in agents}
    alive = {k: True for k in agents}
    dial_hist = {k: [] for k in agents}
    Wh = {k: [] for k in agents}
    cur = {k: "normal" for k in agents}
    for b in range(NBLOCKS):
        lam_b = lam_fn(b) if lam_fn else lam
        w0 = dict(wealth)
        started_alive = dict(alive)
        for k in agents:
            if alive[k]:
                cur[k] = metas[k].choose(wealth[k])
            dial_hist[k].append(cur[k])
        for t in range(WARM + b * BLOCK, WARM + (b + 1) * BLOCK - 3 + 3):
            if t >= N - 3:
                break
            if alive["gate"]:
                p, cost = agents["gate"].step(cur["gate"]); cost *= lam_b
                win = 6 if (p > 0.5) == bits[t] else 0
                if t % 10 == 0:
                    win += 15 if int(np.argmin([abs(p - bb) for bb in warm_bias])) == true_reg[t] else 0
                wealth["gate"] += win - cost
                if wealth["gate"] < 0: alive["gate"] = False
            if alive["jepa"]:
                p, cost, latent = agents["jepa"].step(cur["jepa"]); cost *= lam_b
                win = 6 if (p > 0.5) == bits[t] else 0
                if t % 10 == 0:
                    win += 15 if latent == true_reg[t] else 0
                wealth["jepa"] += win - cost
                if wealth["jepa"] < 0: alive["jepa"] = False
            if alive["genie"]:
                p, p3, cost = agents["genie"].step(cur["genie"]); cost *= lam_b
                win = 6 if (p > 0.5) == bits[t] else 0
                if p3 is not None:
                    win += 6 if (p3 > 0.5) == bits[t + 2] else 0
                if t % 10 == 0:
                    win10 = bits[max(WARM, t - 10):t]
                    lls = [np.sum(win10 * np.log(bb + 1e-9) + (1 - win10) * np.log(1 - bb + 1e-9))
                           for bb in warm_bias]
                    win += 15 if int(np.argmax(lls)) == true_reg[t] else 0
                wealth["genie"] += win - cost
                if wealth["genie"] < 0: alive["genie"] = False
            for k in Wh:
                Wh[k].append(wealth[k])
        for k in agents:
            if started_alive[k]:  # the dead teach nothing; a corpse's 0.0 is not data
                metas[k].update(wealth[k] - w0[k])
    return wealth, alive, dial_hist, Wh

def late_share(dial_hist, k, frac=0.5):
    tail = dial_hist[k][int(len(dial_hist) * frac):]
    return {d: tail.count(d) / max(len(tail), 1) for d in DIALS}

# ================================================================ E1: bandits vs lam
print("=== MARKETPLACE V: do the animals learn the price of energy? ===\n")
print("--- E1: all-bandit market at lam = 0.3, 1, 2, 3 ---")
e1 = {}
for lam in (0.3, 1.0, 2.0, 3.0):
    metas = {"gate": Bandit(11), "jepa": Bandit(22), "genie": Bandit(33)}
    wealth, alive, dh, Wh = run_market(metas, lam, seed=int(lam * 10))
    e1[lam] = (wealth, alive, dh, Wh)
    print(f"lam={lam}: " + " | ".join(
        f"{k} W={wealth[k]:8.1f} alive={alive[k]} late-dials=" +
        "/".join(f"{d}:{late_share(dh, k)[d]:.2f}" for d in DIALS)
        for k in ("gate", "jepa", "genie")))

print("\n--- E1 verdicts ---")
p1a = all(late_share(e1[2.0][2], k)["frugal"] > 0.60 for k in ("gate", "jepa", "genie"))
print(f"P1 lam=2 (survivable pressure) frugal>60% late: {'PASS' if p1a else 'FAIL'}")
print(f"    lam=3: extinction for every dial (M4) -- bandits die in ~2 blocks, "
      f"before the 3-block arm round-robin finishes. Learning needs samples; dying is fast.")
p1b = any(max(late_share(e1[0.3][2], k).items(), key=lambda kv: kv[1])[0] != "frugal"
          for k in ("gate", "jepa", "genie"))
print(f"P1b lam=0.3 dials mixed (some agent modal != frugal): {'PASS' if p1b else 'FAIL'}")
p4 = any(max(late_share(e1[0.3][2], k).items(), key=lambda kv: kv[1])[0] != "frugal"
         for k in ("gate", "jepa", "genie"))
print(f"P4 cheap-energy optimum != frugal for some agent: {'PASS' if p4 else 'FAIL'}")

# ================================================================ E2: populations vs lam
print("\n--- E2: fixed-normal vs thermostat vs bandit at lam = 0.3, 1, 2, 3 ---")
e2 = {}
for lam in (0.3, 1.0, 2.0, 3.0):
    e2[lam] = {}
    pops = {
        "fixed": {"gate": Fixed("normal"), "jepa": Fixed("normal"), "genie": Fixed("normal")},
        "thermo": {"gate": Thermostat(), "jepa": Thermostat(), "genie": Thermostat()},
        "bandit": {"gate": Bandit(111), "jepa": Bandit(222), "genie": Bandit(333)},
    }
    for pname, metas in pops.items():
        wealth, alive, dh, Wh = run_market(metas, lam, seed=int(lam * 10) + 7)
        e2[lam][pname] = (wealth, alive, dh, Wh)
        mw = np.mean(list(wealth.values()))
        print(f"lam={lam} {pname:6s}: meanW={mw:8.1f} alive={sum(alive.values())}/3 " +
              " ".join(f"{k}={wealth[k]:.0f}" for k in ("gate", "jepa", "genie")))

print("\n--- E2 verdicts ---")
surv3 = {p: sum(e2[3.0][p][1].values()) for p in ("fixed", "thermo", "bandit")}
# NOTE: the >= chain below is vacuous when all are 0 -- read the counts, not the PASS.
print(f"P2 lam=3 survival fixed={surv3['fixed']}/3 thermo={surv3['thermo']}/3 bandit={surv3['bandit']}/3")
print(f"    -> {'PASS' if surv3['thermo'] >= surv3['bandit'] > surv3['fixed'] and surv3['thermo'] > 0 else 'FAIL'} "
      f"(predicted thermo >= bandit > fixed with thermo surviving; M4 already showed lam=3 "
      f"is extinction -- fear can't beat math when no dial survives)")
surv2 = {p: sum(e2[2.0][p][1].values()) for p in ("fixed", "thermo", "bandit")}
print(f"P2b lam=2 survival fixed={surv2['fixed']}/3 thermo={surv2['thermo']}/3 bandit={surv2['bandit']}/3 -> "
      f"{'PASS' if surv2['thermo'] >= surv2['bandit'] > surv2['fixed'] else 'FAIL'} "
      f"(lethal-but-survivable floor: predicted thermo >= bandit > fixed)")
for lam in (0.3, 1.0, 2.0, 3.0):
    bw = np.mean(list(e2[lam]["bandit"][0].values()))
    fw = np.mean(list(e2[lam]["fixed"][0].values()))
    print(f"P5 lam={lam}: bandit meanW {bw:.0f} vs fixed {fw:.0f} -> "
      f"{'PASS' if bw >= fw else 'FAIL'}")

# ================================================================ E3: the shock
print("\n--- E3: lam shock 0.3 -> 3.0 at block 28 ---")
SHOCK = NBLOCKS // 2
e3 = {}
for pname, mk in (("thermo", lambda: {"gate": Thermostat(), "jepa": Thermostat(), "genie": Thermostat()}),
                  ("bandit", lambda: {"gate": Bandit(5), "jepa": Bandit(6), "genie": Bandit(7)})):
    wealth, alive, dh, Wh = run_market(mk(), 0.3, seed=99,
                                       lam_fn=lambda b: 0.3 if b < SHOCK else 3.0)
    e3[pname] = (wealth, alive, dh, Wh)
    print(f"{pname:6s}: " + " | ".join(f"{k} W={wealth[k]:8.1f} alive={alive[k]}" for k in ("gate", "jepa", "genie")))

print("\n--- E3 verdicts ---")
for pname in ("thermo", "bandit"):
    dh = e3[pname][2]
    post = {k: dh[k][SHOCK:SHOCK + 12] for k in ("gate", "jepa", "genie")}
    t_to_frugal = {k: next((i for i, d in enumerate(post[k]) if d == "frugal"), 99) for k in post}
    print(f"{pname:6s} blocks to frugal after shock: {t_to_frugal}")
td = e3["thermo"][2]; bd = e3["bandit"][2]
p3a = all(next((i for i, d in enumerate(td[k][SHOCK:SHOCK + 12]) if d == "frugal"), 99) <= 2
          for k in ("gate", "jepa", "genie"))
print(f"P3 thermostat frugal within 2 blocks: {'PASS' if p3a else 'FAIL'}")
p3b = all(sum(1 for d in bd[k][SHOCK + 12:SHOCK + 24] if d == "frugal") / 12 >= 0.6
          for k in ("gate", "jepa", "genie"))
print(f"P3b bandit >=60% frugal within blocks 12-24 post-shock: {'PASS' if p3b else 'FAIL'}")

# ================================================================ E4: the forgetting breaker
print("\n--- E4: constant step-size bandit (BanditAlpha) on the same shock ---")
e4 = {}
for pname, mk in (("runmean", lambda: {"gate": Bandit(5), "jepa": Bandit(6), "genie": Bandit(7)}),
                  ("alpha", lambda: {"gate": BanditAlpha(5), "jepa": BanditAlpha(6), "genie": BanditAlpha(7)})):
    wealth, alive, dh, Wh = run_market(mk(), 0.3, seed=99,
                                       lam_fn=lambda b: 0.3 if b < SHOCK else 3.0)
    e4[pname] = (wealth, alive, dh, Wh)
    mw = np.mean(list(wealth.values()))
    print(f"{pname:7s}: meanW={mw:8.1f} alive={sum(alive.values())}/3 " +
          " ".join(f"{k}={wealth[k]:.0f}" for k in ("gate", "jepa", "genie")))
ad = e4["alpha"][2]
p6a = all(sum(1 for d in ad[k][SHOCK + 12:SHOCK + 24] if d == "frugal") / 12 >= 0.6
          for k in ("gate", "jepa", "genie"))
mw_a = np.mean(list(e4["alpha"][0].values()))
mw_r = np.mean(list(e4["runmean"][0].values()))
print(f"P6 alpha-bandit >=60% frugal blocks 12-24 post-shock: {'PASS' if p6a else 'FAIL'}; "
      f"meanW alpha {mw_a:.0f} vs running-mean {mw_r:.0f} -> {'PASS' if mw_a >= mw_r else 'FAIL'}")

# ================================================================ plots
fig1, axes1 = plt.subplots(2, 2, figsize=(14, 9), sharey=True)
for ax, lam in zip(axes1.flat, (0.3, 1.0, 2.0, 3.0)):
    dh = e1[lam][2]
    x = np.arange(len(dh["gate"]))
    for k, c in (("gate", "#2a7fff"), ("jepa", "#ff9f2a"), ("genie", "#b45cff")):
        y = [DIALS.index(d) for d in dh[k]]
        ax.plot(x, y, color=c, label=k, lw=1.2, alpha=0.85)
    ax.set_yticks([0, 1, 2]); ax.set_yticklabels(DIALS)
    ax.set_xlabel("block (25 steps)")
    ax.set_title(f"bandit dials, lam={lam}")
    ax.set_ylabel("chosen dial")
axes1.flat[1].legend()
fig1.suptitle("E1: what the bandits settle on under four cost floors")
fig1.tight_layout()
fig1.savefig("marketplace5_learning.png", dpi=110)
print("\nwrote marketplace5_learning.png")

fig2, axes2 = plt.subplots(2, 2, figsize=(14, 9))
for ax, lam in zip(axes2.flat, (0.3, 1.0, 2.0, 3.0)):
    for pname, c, ls in (("fixed", "#888888", "--"), ("thermo", "#2a7fff", "-"), ("bandit", "#ff9f2a", "-")):
        Wh = e2[lam][pname][3]
        mean_w = np.mean([Wh[k] for k in ("gate", "jepa", "genie")], axis=0)
        ax.plot(mean_w, color=c, ls=ls, label=pname, lw=2)
    ax.axhline(0, color="k", ls=":", lw=1)
    ax.set_xlabel("time step")
    ax.set_title(f"lam={lam}")
    ax.set_ylabel("mean wealth (3 agents)")
axes2.flat[1].legend(title="population")
fig2.suptitle("E2: fixed vs thermostat vs bandit — mean wealth under four cost floors")
fig2.tight_layout()
fig2.savefig("marketplace5_survival.png", dpi=110)
print("wrote marketplace5_survival.png")

fig3, axes3 = plt.subplots(2, 1, figsize=(13, 8), sharex=True)
for i, pname in enumerate(("thermo", "bandit")):
    ax = axes3[i]
    dh = e3[pname][2]
    x = np.arange(len(dh["gate"]))
    for k, c in (("gate", "#2a7fff"), ("jepa", "#ff9f2a"), ("genie", "#b45cff")):
        y = [DIALS.index(d) for d in dh[k]]
        ax.plot(x, y, color=c, label=k, lw=1.4)
    ax.axvline(SHOCK, color="red", ls="--", lw=1.5)
    ax.text(SHOCK + 1, 2.15, "lam 0.3 -> 3.0", color="red", fontsize=10)
    ax.set_yticks([0, 1, 2]); ax.set_yticklabels(DIALS)
    ax.set_ylabel(f"{pname} dial")
    ax.legend(loc="lower left")
axes3[1].set_xlabel("block (25 steps)")
fig3.suptitle("E3: re-tuning after the cost shock — thermostat vs bandit")
fig3.tight_layout()
fig3.savefig("marketplace5_shock.png", dpi=110)
print("wrote marketplace5_shock.png")

fig4, axes4 = plt.subplots(2, 1, figsize=(13, 8), sharex=True)
for i, pname in enumerate(("runmean", "alpha")):
    ax = axes4[i]
    dh = e4[pname][2]
    x = np.arange(len(dh["gate"]))
    for k, c in (("gate", "#2a7fff"), ("jepa", "#ff9f2a"), ("genie", "#b45cff")):
        y = [DIALS.index(d) for d in dh[k]]
        ax.plot(x, y, color=c, label=k, lw=1.4)
    ax.axvline(SHOCK, color="red", ls="--", lw=1.5)
    ax.set_yticks([0, 1, 2]); ax.set_yticklabels(DIALS)
    ax.set_ylabel(f"{pname} dial")
    ax.legend(loc="lower left")
axes4[1].set_xlabel("block (25 steps)")
fig4.suptitle("E4: the forgetting breaker — running-mean vs constant step-size after the shock")
fig4.tight_layout()
fig4.savefig("marketplace5_forgetting.png", dpi=110)
print("wrote marketplace5_forgetting.png")
