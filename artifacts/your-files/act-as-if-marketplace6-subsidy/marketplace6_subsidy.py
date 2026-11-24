"""
MARKETPLACE V — organization structures.

Eight new animals for the act-as-if zoo, in the black-swan world
(1000 bits, regimes ~120 steps, 3 unprecedented swans — the marketplace4
world, seed 99, so results are comparable to M4). Each animal is an
*organization structure* for turning evidence into action.

  PARACONSISTENT (Belnap 4-valued: T/F/Both/Neither): holds contradictory
    hypotheses without exploding. When evidence conflicts it holds Both
    and acts on the overlap. Contradiction is expensive (2x), suspension
    is cheap (0.5x). Governance: the agent that can hold "held AND lapsed"
    during a transition.
  SELF-BUILD: starts with ZERO hypotheses. Builds them from prediction
    error, paying construction cost (5.0) not selection cost. Emergence
    vs imposition, as an agent.
  DIALECTICAL: thesis + antithesis, periodic synthesis of a third position
    (not averaging — a new hypothesis dissolving the opposition).
    Synthesis costs 3.0; holding tension costs 0.5/step.
  STIGMERGIC: no world model. Writes traces to a shared field, reads
    others' traces. Coordinates through the surface, not messages.
    Write 0.2, read 0.1, traces decay.
  FEDERATED: 3 sub-agents, each seeing a slice of the stream. Local
    decisions free; sharing a summary costs 0.3. Lightweight aggregator.
  CONTRARIAN: observes consensus (lag-1 mean of others), bets the opposite.
    The value of dissent. Costs 0.2 to observe.
  SATISFICER: threshold 0.60 trailing accuracy. Above it: coast (near-free).
    Below it: adapt minimally. When is "good enough" better than optimal?
  MIMETIC: no own model. Copies the best recent performer with 1-step lag.
    Norm-following as strategy. Costs 0.2 to observe.

Baselines (ported): GATE (Mamba-style, retrained on this warmup), JEPA,
REACTIVE (zero-cost, from M4).

PRE-REGISTERED (written before running):
  P1: paraconsistent swan-accuracy > gate swan-accuracy
      (holds contradiction vs frantic adaptation).
  P2: self-build accuracy(first 200 live steps) < 0.52 AND
      accuracy(last 200) > accuracy(first 200) + 0.03 AND n_built >= 3
      (construction takes time, then pays).
  P3: stigmergic swan-call accuracy >= 0.55 AND total spent < 400
      (traces match confusion-reading at lower cost).
  P4: contrarian calm accuracy < 0.52 AND
      contrarian swan accuracy > contrarian calm accuracy
      (loses in calm, wins relatively in swans).
  P5: satisficer total spent is the minimum among all agents except
      reactive (whose zero cost is definitional).
  P6: at checkpoints t in {300,...,900}, mimetic wealth < max wealth
      (tracks but never leads).

Exit 0 iff all pass; exit 1 otherwise, the failure as the finding.
Seed: 99 (world), 1001 (gate init). Deterministic.
"""

import numpy as np
import sys
SUB = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import deque

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
print(f"swans at {sorted(swan_times)}  (same world as M4)")


# ================================================================ PARACONSISTENT
class Paraconsistent:
    """Belnap 4-valued hypotheses. Holds Both, acts on the overlap."""
    def __init__(self):
        self.bias = list(warm_bias)
        self.f = [0, 0, 0]      # evidence for
        self.a = [0, 0, 0]      # evidence against
        self.t = WARM

    def step(self):
        t = self.t
        bit = bits[t - 1]
        for i in range(3):
            pred1 = self.bias[i] > 0.5
            if pred1 == bit:
                self.f[i] += 1
            else:
                self.a[i] += 1
        vals = []
        for i in range(3):
            if self.f[i] > 0 and self.a[i] == 0:
                vals.append("T")
            elif self.a[i] > 0 and self.f[i] == 0:
                vals.append("F")
            elif self.f[i] > 0 and self.a[i] > 0:
                vals.append("B")
            else:
                vals.append("N")
        num, den = 0.0, 0.0
        for i, v in enumerate(vals):
            w = {"T": 1.0, "B": 2.0, "F": 0.0, "N": 0.0}[v]
            num += w * self.bias[i]; den += w
        p = num / den if den > 0 else 0.5
        nB = sum(1 for v in vals if v == "B")
        nN = sum(1 for v in vals if v == "N")
        nT = sum(1 for v in vals if v == "T")
        nF = sum(1 for v in vals if v == "F")
        cost = LN2 * (nT * 1.0 + nB * 2.0 + nF * 1.0 + nN * 0.5)
        swan = nB >= 2
        self.t += 1
        return p, cost, swan


# ================================================================ SELF-BUILD
class SelfBuild:
    """Zero hypotheses at birth. Builds from surprise; construction costs."""
    BUILD_COST = 5.0

    def __init__(self):
        self.hyps = []  # dicts: bias, err (deque)
        self.n_built = 0
        self.t = WARM

    def best(self):
        if not self.hyps:
            return None
        return min(self.hyps, key=lambda h: np.mean(h["err"]) if h["err"] else 1.0)

    def step(self):
        t = self.t
        bit = bits[t - 1]
        for h in self.hyps:
            h["err"].append(abs((h["bias"] > 0.5) - bit))
        b = self.best()
        surprise = abs(bits[t - 8:t].mean() - (b["bias"] if b else 0.5))
        cost = 0.1
        swan = False
        if b is None or surprise > 0.15:
            if len(self.hyps) >= 8:
                self.hyps.sort(key=lambda h: np.mean(h["err"]) if h["err"] else 1.0)
                self.hyps.pop(0)
            nb = float(np.clip(bits[t - 15:t].mean(), 0.05, 0.95))
            self.hyps.append({"bias": nb, "err": deque(maxlen=30)})
            self.n_built += 1
            cost += self.BUILD_COST
            if surprise > 0.30:
                swan = True
        b = self.best()
        p = b["bias"] if b else 0.5
        self.t += 1
        return p, cost, swan


# ================================================================ DIALECTICAL
class Dialectical:
    """Thesis + antithesis; synthesis is a third position, not an average."""
    def __init__(self):
        self.thesis = float(warm_bias[1])
        self.antithesis = 1.0 - self.thesis
        self.synth = None
        self.err_t = deque(maxlen=20)
        self.err_a = deque(maxlen=20)
        self.err_s = deque(maxlen=20)
        self.n_synth = 0
        self.t = WARM

    def step(self):
        t = self.t
        bit = bits[t - 1]
        self.err_t.append(abs((self.thesis > 0.5) - bit))
        self.err_a.append(abs((self.antithesis > 0.5) - bit))
        if self.synth is not None:
            self.err_s.append(abs((self.synth > 0.5) - bit))
        cost = LN2 + 0.5  # evaluation + holding the tension
        swan = False
        mt = np.mean(self.err_t) if self.err_t else 1
        ma = np.mean(self.err_a) if self.err_a else 1
        if len(self.err_t) == 20 and mt > 0.45 and ma > 0.45:
            # both fail: synthesize a third position from the recent stream
            self.synth = float(np.clip(bits[t - 15:t].mean(), 0.05, 0.95))
            self.err_s = deque(maxlen=20)
            self.n_synth += 1
            cost += 3.0
            swan = True
        cands = [("t", self.thesis, mt), ("a", self.antithesis, ma)]
        if self.synth is not None and self.err_s:
            cands.append(("s", self.synth, np.mean(self.err_s)))
        p = min(cands, key=lambda c: c[2])[1]
        self.t += 1
        return p, cost, swan


# ================================================================ STIGMERGIC
class Stigmergic:
    """No world model. Reads the shared trace field; writes its own mark."""
    def __init__(self, field):
        self.field = field  # name -> deque of (t, p); maintained by market
        self.t = WARM

    def step(self):
        t = self.t
        others = []
        for name, dq in self.field.items():
            if name == "stigmergic":
                continue
            for (tt, p) in dq:
                if t - 20 <= tt < t:
                    others.append(p)
        cost = 0.1  # read
        if others:
            p = float(np.mean(others))
            swan = float(np.std(others)) > 0.25
        else:
            p, swan = 0.5, False
        cost += 0.2  # write own mark (market loop records it)
        self.t += 1
        return p, cost, swan


# ================================================================ FEDERATED
class Federated:
    """3 sub-agents, strided slices. Local free; summaries cost."""
    def __init__(self):
        self.t = WARM

    def step(self):
        t = self.t
        ps, confs = [], []
        for i in range(3):
            idx = [t - 1 - i - 3 * j for j in range(10) if t - 1 - i - 3 * j >= 0]
            sl = bits[idx]
            pi = float(sl.mean())
            ci = 1.0 / (1.0 + float(sl.std()))
            ps.append(pi); confs.append(ci)
        ps, confs = np.array(ps), np.array(confs)
        p = float(np.sum(confs * ps) / confs.sum())
        cost = 0.3 * 3  # three summaries shared upward
        swan = bool(np.max(ps) - np.min(ps) > 0.4)
        self.t += 1
        return p, cost, swan


# ================================================================ CONTRARIAN
class Contrarian:
    """Bets against the lag-1 consensus. The value of dissent."""
    def __init__(self):
        self.t = WARM

    def step(self, prev_p):
        t = self.t
        others = [p for k, p in prev_p.items() if k != "contrarian"]
        consensus = float(np.mean(others)) if others else 0.5
        p = float(np.clip(1.0 - consensus, 0.02, 0.98))
        cost = 0.2
        swan = abs(consensus - 0.5) > 0.3
        self.t += 1
        return p, cost, swan


# ================================================================ SATISFICER
class Satisficer:
    """0.60 trailing accuracy. Above: coast. Below: minimal adapt."""
    THRESH = 0.60

    def __init__(self):
        self.hist = deque(maxlen=50)
        self.t = WARM

    def step(self):
        t = self.t
        acc = float(np.mean(self.hist)) if len(self.hist) >= 20 else 0.0
        if acc >= self.THRESH:
            p = float(bits[t - 1])  # coast: pure coupling
            cost = 0.05
        else:
            recent = bits[t - 10:t].mean()
            p = float(np.clip(0.7 * bits[t - 1] + 0.3 * recent, 0.02, 0.98))
            cost = 0.5
        swan = acc < 0.45 and len(self.hist) >= 20
        self.t += 1
        return p, cost, swan

    def observe(self, correct):
        self.hist.append(1.0 if correct else 0.0)


# ================================================================ MIMETIC
class Mimetic:
    """Copies the trailing-20 accuracy leader, 1-step lag."""
    def __init__(self):
        self.t = WARM

    def step(self, prev_p, trail_acc):
        t = self.t
        cands = {k: v for k, v in trail_acc.items() if k != "mimetic" and v is not None}
        leader = max(cands, key=cands.get) if cands else None
        p = float(prev_p.get(leader, 0.5)) if leader else 0.5
        cost = 0.2
        self.t += 1
        return p, cost, False, leader


# ================================================================ baselines
class Reactive:
    def __init__(self):
        self.t = WARM

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


class Gate:
    """Mamba-style selective gate, retrained on THIS world's warmup."""
    def __init__(self):
        grng = np.random.default_rng(1001)
        self.GDIM = 6
        self.GA = -(0.4 + 0.6 * np.arange(self.GDIM) / self.GDIM)
        self.GB = grng.normal(0, 0.5, (self.GDIM, 2))

        def gate_delta(surprise, scale):
            return np.log1p(np.exp(scale * (3.0 * surprise - 1.0)))

        self._gd = gate_delta
        h = np.zeros(self.GDIM)
        states, ys = [], []
        for t in range(WARM):
            x = np.array([bits[t], 1 - bits[t]])
            pred_m = np.mean(bits[max(0, t - 10):t]) if t > 0 else 0.5
            d = gate_delta(abs(bits[t] - pred_m), 1.0)
            h = np.exp(d * self.GA) * h + (d * self.GB) @ x
            states.append(h.copy()); ys.append(bits[t])
        Xa = np.column_stack([np.array(states), np.ones(WARM)])
        ys = np.array(ys)
        w = np.zeros(self.GDIM + 1)
        for _ in range(800):
            p = 1 / (1 + np.exp(-Xa @ w))
            w -= 0.5 * Xa.T @ (p - ys) / WARM
        self.w = w
        # roll state through warmup
        self.h = np.zeros(self.GDIM)
        for t in range(WARM):
            x = np.array([bits[t], 1 - bits[t]])
            pred_m = np.mean(bits[max(0, t - 10):t]) if t > 0 else 0.5
            d = gate_delta(abs(bits[t] - pred_m), 1.0)
            self.h = np.exp(d * self.GA) * self.h + (d * self.GB) @ x
        self.t = WARM

    def step(self):
        t = self.t
        x = np.array([bits[t - 1], 1 - bits[t - 1]])
        pred_m = np.mean(bits[max(0, t - 10):t - 1])
        d = self._gd(abs(bits[t - 1] - pred_m), 1.0)
        erase = float(np.sum(1 - np.exp(d * self.GA)) * 1.0)
        cost = LN2 * erase + 0.1
        self.h = np.exp(d * self.GA) * self.h + (d * self.GB) @ x
        p = float(1 / (1 + np.exp(-(self.h @ self.w[:self.GDIM] + self.w[self.GDIM]))))
        swan = abs(bits[t - 1] - pred_m) > 0.35
        self.t += 1
        return p, cost, swan


# ================================================================ market
field = {}          # stigmergic trace field: name -> deque((t, p))
prev_p = {}         # lag-1 predictions for contrarian / mimetic
trail = {}          # trailing-20 correctness deques for mimetic leader
CHECKPOINTS = [300, 400, 500, 600, 700, 800, 900]
mimetic_check = {}

agents = {}
agents["paraconsistent"] = Paraconsistent()
agents["selfbuild"] = SelfBuild()
agents["dialectical"] = Dialectical()
agents["federated"] = Federated()
agents["contrarian"] = Contrarian()
agents["satisficer"] = Satisficer()
agents["mimetic"] = Mimetic()
agents["gate"] = Gate()
agents["jepa"] = JEPA()
agents["reactive"] = Reactive()
# stigmergic needs the field; create after others exist
agents["stigmergic"] = Stigmergic(field)

names = list(agents.keys())
for k in names:
    field[k] = deque(maxlen=25)
    trail[k] = deque(maxlen=20)

wealth = {k: 200.0 for k in names}
alive = {k: True for k in names}
acc = {k: [] for k in names}
acc_swan = {k: [] for k in names}
acc_calm = {k: [] for k in names}
spent = {k: 0.0 for k in names}
swan_calls = {k: [] for k in names}
Wh = {k: [] for k in names}
first200 = {k: [] for k in names}
last200 = {k: [] for k in names}

for t in range(WARM, N - 10):
    step_p, step_cost, step_swan = {}, {}, {}
    # --- order: baselines + independents first, then lag-dependent readers
    order1 = ["gate", "jepa", "reactive", "paraconsistent", "selfbuild",
              "dialectical", "federated", "satisficer", "stigmergic"]
    for k in order1:
        if not alive[k]:
            continue
        a = agents[k]
        if k == "stigmergic":
            p, cost, swan = a.step()
        else:
            r4 = a.step()
            p, cost, swan = r4[0], r4[1], r4[2]
        step_p[k], step_cost[k], step_swan[k] = p, cost, swan
    # contrarian + mimetic read lag-1 consensus/leader
    if alive["contrarian"]:
        p, cost, swan = agents["contrarian"].step(prev_p)
        step_p["contrarian"], step_cost["contrarian"], step_swan["contrarian"] = p, cost, swan
    if alive["mimetic"]:
        tc = {k: (float(np.mean(trail[k])) if len(trail[k]) >= 10 else None) for k in names}
        p, cost, swan, leader = agents["mimetic"].step(prev_p, tc)
        step_p["mimetic"], step_cost["mimetic"], step_swan["mimetic"] = p, cost, swan
    # --- score
    for k in names:
        if not alive[k]:
            continue
        p, cost, swan = step_p[k], step_cost[k], step_swan[k]
        win = 6 if (p > 0.5) == bits[t] else 0
        if t % 10 == 0 and t + 10 < N:
            win += 12 if (p > 0.5) == bits[t + 10] else 0
        if t % 10 == 0 and k != "reactive":
            hit = is_swan[t]
            swan_calls[k].append(swan == hit)
            win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
        wealth[k] += win - cost + SUB * cost
        spent[k] += cost
        correct = (p > 0.5) == bits[t]
        acc[k].append(correct)
        trail[k].append(1.0 if correct else 0.0)
        if is_swan[t]:
            acc_swan[k].append(correct)
        else:
            acc_calm[k].append(correct)
        if k == "satisficer":
            agents["satisficer"].observe(correct)
        if t - WARM < 200:
            first200[k].append(correct)
        if t >= N - 10 - 200:
            last200[k].append(correct)
        if wealth[k] < 0:
            alive[k] = False
        field[k].append((t, p))
    prev_p = dict(step_p)
    if t in CHECKPOINTS:
        top = max(wealth[k] for k in names if alive[k])
        mimetic_check[t] = (wealth["mimetic"], top)
    for k in names:
        Wh[k].append(wealth[k] if alive[k] else (Wh[k][-1] if Wh[k] else 0))

print("\n=== MARKETPLACE VI: subsidy floor (SUB=%g) ===" % SUB)
for k in names:
    a = np.mean(acc[k]) if acc[k] else 0
    asw = np.mean(acc_swan[k]) if acc_swan[k] else 0
    ac = np.mean(acc_calm[k]) if acc_calm[k] else 0
    sc = np.mean(swan_calls[k]) if swan_calls[k] else 0
    print(f"{k:14s} | wealth {wealth[k]:8.1f} | acc {a:.3f} | calm {ac:.3f} | "
          f"swan-acc {asw:.3f} | swan-call {sc:.2f} | spent {spent[k]:7.1f} | "
          f"{'ALIVE' if alive[k] else 'DEAD'}")

results = {}
# P1: paraconsistent swan-acc > gate swan-acc
pa = np.mean(acc_swan["paraconsistent"]) if acc_swan["paraconsistent"] else 0
ga = np.mean(acc_swan["gate"]) if acc_swan["gate"] else 0
results["P1"] = (pa > ga, f"paraconsistent {pa:.3f} vs gate {ga:.3f}")
# P2: self-build starts poor, improves, builds >= 3
f2 = np.mean(first200["selfbuild"]) if first200["selfbuild"] else 0
l2 = np.mean(last200["selfbuild"]) if last200["selfbuild"] else 0
nb = agents["selfbuild"].n_built
results["P2"] = (f2 < 0.52 and l2 > f2 + 0.03 and nb >= 3,
                 f"first200 {f2:.3f} <0.52, last200 {l2:.3f} > first+0.03, built {nb}")
# P3: stigmergic swan-call >= 0.55 and spent < 400
sc3 = np.mean(swan_calls["stigmergic"]) if swan_calls["stigmergic"] else 0
results["P3"] = (sc3 >= 0.55 and spent["stigmergic"] < 400,
                 f"swan-call {sc3:.2f} >=0.55, spent {spent['stigmergic']:.1f} <400")
# P4: contrarian calm < 0.52 and swan-acc > calm
cc = np.mean(acc_calm["contrarian"]) if acc_calm["contrarian"] else 0
cs = np.mean(acc_swan["contrarian"]) if acc_swan["contrarian"] else 0
results["P4"] = (cc < 0.52 and cs > cc, f"calm {cc:.3f} <0.52, swan {cs:.3f} > calm")
# P5: satisficer min spend among non-reactive
others = {k: spent[k] for k in names if k != "reactive"}
results["P5"] = (spent["satisficer"] == min(others.values()),
                 f"satisficer {spent['satisficer']:.1f} vs min-other "
                 f"{min(others.values()):.1f} ({min(others, key=others.get)})")
# P6: mimetic never leads at checkpoints
p6ok = all(mw < tw for mw, tw in mimetic_check.values())
results["P6"] = (p6ok, f"checkpoints: "
                 + ", ".join(f"{t}:{mw:.0f}<{tw:.0f}" for t, (mw, tw) in mimetic_check.items()))

print("\n--- pre-registered predictions ---")
allpass = True
for k, (ok, detail) in results.items():
    print(f"{k}: {'PASS' if ok else 'FAIL'} ({detail})")
    allpass = allpass and ok

# wealth ranking
rank = sorted(names, key=lambda k: wealth[k], reverse=True)
print("\nwealth ranking: " + " > ".join(f"{k}({wealth[k]:.0f})" for k in rank))

fig, axes = plt.subplots(1, 2, figsize=(15, 5))
colors = {"paraconsistent": "#b45cff", "selfbuild": "#22cc66", "dialectical": "#ff9f2a",
          "stigmergic": "#2a7fff", "federated": "#ff5555", "contrarian": "#ff2a7f",
          "satisficer": "#8a8a8a", "mimetic": "#c9a227", "gate": "#2adfff",
          "jepa": "#7fff2a", "reactive": "#555555"}
for k in names:
    axes[0].plot(Wh[k], color=colors[k], label=k, lw=1.8)
for st in swan_times:
    axes[0].axvspan(st - WARM - 12, st - WARM + 12, color="red", alpha=0.12)
axes[0].axhline(0, color="k", ls="--", lw=1)
axes[0].set_xlabel("time step (from warmup end)")
axes[0].set_ylabel("wealth (coins)")
axes[0].set_title("Marketplace V: wealth through swans")
axes[0].legend(fontsize=8, ncol=2)
ks = names
axes[1].bar(ks, [spent[k] for k in ks], color=[colors[k] for k in ks], alpha=0.85)
axes[1].set_ylabel("total coins spent (cost)")
axes[1].set_title("Who paid what for their organization?")
axes[1].tick_params(axis="x", rotation=25)
fig.suptitle("Marketplace VI: subsidy floor (SUB=%g)" % SUB)
fig.tight_layout()
fig.savefig(f"marketplace6_sub{SUB:.1f}.png", dpi=110)
print(f"\nwrote marketplace6_sub{SUB:.1f}.png")

import sys
sys.exit(0 if allpass else 1)
