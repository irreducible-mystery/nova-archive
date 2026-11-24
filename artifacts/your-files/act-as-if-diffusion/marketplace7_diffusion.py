"""
MARKETPLACE VII — Diffusion joins the zoo.

The M5 black-swan world verbatim (1000 bits, regimes ~120 steps, 3
unprecedented swans, seed 99 — same world as M4/M5/M6), the same eleven
animals, plus one new animal: DIFFUSION.

  DIFFUSION: decides by iterative denoising. The decision-relevant signal
    in this harness is the scalar p = P(next bit = 1) every animal
    returns. Each decision: S=4 samples, one conditioned on the recent-bit
    mean at each timescale {8, 15, 30, 60}, start as pure noise around the
    unconditional prior u=0.5, and are refined over K steps toward a
    guided target  clip(u + w*(c - u))  (classifier-free-guidance
    analogue: w=0 ignores the signal, w>1 extrapolates past it).
    Per-step pull a = 2/(K+2); annealed noise sigma_k = 0.10*sqrt(a)*
    (1 - k/(K+1)). Spread across the S final samples is its uncertainty:
    action strength scales DOWN as spread rises,
    p = 0.5 + (mean - 0.5)/(1 + (spread/0.18)^2), and spread > 0.20 is
    its swan call. Cost: the refinement tax — LN2 per (K*S)/40, i.e. a
    denoising micro-step is costed at 1/40 of the zoo's LN2 hypothesis-
    evaluation unit. Defaults K=20, w=2.0, S=4 -> LN2*2 per step.

Pre-registered predictions: marketplace7_PREDICTIONS.md (written before
this run). Six predictions, P1-P6: swan reading vs the one-shot agents,
wealth rank under the tax, the K ablation (accuracy up, wealth peaked
inside), the guidance ablation (w=5 over-obeys, w=0 is blind), onset
speed vs reactive, and the uncertainty rule paying in drawdown.
Ablations run in-process after the main run: K in {1,5,20,50},
w in {0,1,2,5}, and a no-uncertainty variant.

Exit 0 iff all six pass; exit 1 otherwise, the failure as the finding.
Seed: 99 (world), 1001 (gate init), 777 (diffusion's own RNG).
Deterministic.
"""


import numpy as np
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



# ================================================================ DIFFUSION
class Diffusion:
    """Iterative denoising over a scalar signal. See module docstring."""
    SCALES = [8, 15, 30, 60]

    def __init__(self, K=20, w=2.0, S=4, uncertainty=True, seed=777):
        self.K, self.w, self.S = K, w, S
        self.uncertainty = uncertainty
        self.rng = np.random.default_rng(seed)
        self.t = WARM
        self.last_spread = 0.0

    def step(self):
        t = self.t
        u = 0.5  # unconditional prior: the world's marginal
        a = 2.0 / (self.K + 2)
        samples = []
        for s in range(self.S):
            scale = self.SCALES[s % len(self.SCALES)]
            c = float(bits[t - scale:t].mean())     # conditioning signal
            target = float(np.clip(u + self.w * (c - u), 0.02, 0.98))
            x = u + self.rng.normal(0.0, 0.30)      # pure noise start
            for k in range(self.K):
                sigma = 0.10 * np.sqrt(a) * (1.0 - k / (self.K + 1))
                x = x + a * (target - x) + sigma * self.rng.normal()
            samples.append(float(np.clip(x, 0.02, 0.98)))
        samples = np.array(samples)
        mean = float(samples.mean())
        spread = float(samples.std())
        self.last_spread = spread
        if self.uncertainty:
            strength = 1.0 / (1.0 + (spread / 0.18) ** 2)
            p = 0.5 + (mean - 0.5) * strength
        else:
            p = mean
        p = float(np.clip(p, 0.02, 0.98))
        cost = LN2 * (self.K * self.S) / 40.0        # the refinement tax
        swan = spread > 0.20
        self.t += 1
        return p, cost, swan


# ================================================================ market
def max_drawdown(series):
    peak, dd = -1e18, 0.0
    for v in series:
        peak = max(peak, v)
        dd = max(dd, peak - v)
    return dd


def run_market(K=20, w=2.0, S=4, uncertainty=True):
    field = {}
    prev_p = {}
    trail = {}
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
    agents["stigmergic"] = Stigmergic(field)
    agents["diffusion"] = Diffusion(K=K, w=w, S=S, uncertainty=uncertainty)

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
    corr_t = {k: {} for k in names}   # t -> correct, for onset metrics

    for t in range(WARM, N - 10):
        step_p, step_cost, step_swan = {}, {}, {}
        order1 = ["gate", "jepa", "reactive", "paraconsistent", "selfbuild",
                  "dialectical", "federated", "satisficer", "stigmergic",
                  "diffusion"]
        for k in order1:
            if not alive[k]:
                continue
            r4 = agents[k].step()
            step_p[k], step_cost[k], step_swan[k] = r4[0], r4[1], r4[2]
        if alive["contrarian"]:
            p, cost, swan = agents["contrarian"].step(prev_p)
            step_p["contrarian"], step_cost["contrarian"], step_swan["contrarian"] = p, cost, swan
        if alive["mimetic"]:
            tc = {k: (float(np.mean(trail[k])) if len(trail[k]) >= 10 else None)
                  for k in names}
            p, cost, swan, leader = agents["mimetic"].step(prev_p, tc)
            step_p["mimetic"], step_cost["mimetic"], step_swan["mimetic"] = p, cost, swan
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
            wealth[k] += win - cost
            spent[k] += cost
            correct = (p > 0.5) == bits[t]
            acc[k].append(correct)
            corr_t[k][t] = bool(correct)
            trail[k].append(1.0 if correct else 0.0)
            if is_swan[t]:
                acc_swan[k].append(correct)
            else:
                acc_calm[k].append(correct)
            if k == "satisficer":
                agents["satisficer"].observe(correct)
            if wealth[k] < 0:
                alive[k] = False
            field[k].append((t, p))
        prev_p = dict(step_p)
        for k in names:
            Wh[k].append(wealth[k] if alive[k] else (Wh[k][-1] if Wh[k] else 0))

    out = {"names": names, "wealth": wealth, "alive": alive, "spent": spent,
           "Wh": Wh,
           "acc": {k: float(np.mean(acc[k])) if acc[k] else 0.0 for k in names},
           "acc_swan": {k: float(np.mean(acc_swan[k])) if acc_swan[k] else 0.0
                        for k in names},
           "acc_calm": {k: float(np.mean(acc_calm[k])) if acc_calm[k] else 0.0
                        for k in names},
           "swan_call": {k: float(np.mean(swan_calls[k])) if swan_calls[k] else 0.0
                         for k in names},
           "drawdown": {k: max_drawdown(Wh[k]) for k in names},
           "corr_t": corr_t}
    return out


def onset_metrics(res):
    onsets = [t for t in range(1, N) if is_swan[t] and not is_swan[t - 1]]
    onset_steps = set()
    for o in onsets:
        onset_steps.update(range(o, o + 5))
    def acc_on(k, steps):
        vals = [res["corr_t"][k][t] for t in steps if t in res["corr_t"][k]]
        return float(np.mean(vals)) if vals else 0.0
    swan_steps = [t for t in range(N) if is_swan[t]]
    return (acc_on("diffusion", onset_steps), acc_on("reactive", onset_steps),
            acc_on("diffusion", swan_steps), acc_on("reactive", swan_steps))


if __name__ == "__main__":
    import json, sys
    print(f"swans at {sorted(swan_times)}  (same world as M4/M5/M6)")

    main = run_market(K=20, w=2.0, S=4, uncertainty=True)
    names = main["names"]
    print("\n=== MARKETPLACE VII: diffusion joins (K=20, w=2, S=4) ===")
    for k in names:
        print(f"{k:14s} | wealth {main['wealth'][k]:8.1f} | acc {main['acc'][k]:.3f} | "
              f"calm {main['acc_calm'][k]:.3f} | swan-acc {main['acc_swan'][k]:.3f} | "
              f"swan-call {main['swan_call'][k]:.2f} | spent {main['spent'][k]:7.1f} | "
              f"maxDD {main['drawdown'][k]:7.1f} | "
              f"{'ALIVE' if main['alive'][k] else 'DEAD'}")
    rank = sorted(names, key=lambda k: main["wealth"][k], reverse=True)
    print("\nwealth ranking: " + " > ".join(f"{k}({main['wealth'][k]:.0f})" for k in rank))
    drank = rank.index("diffusion") + 1

    print("\n--- ablations (diffusion only varies) ---")
    abl_K, abl_w = {}, {}
    for K in [1, 5, 20, 50]:
        r = main if K == 20 else run_market(K=K, w=2.0, S=4, uncertainty=True)
        abl_K[K] = r
        print(f"K={K:3d}: wealth {r['wealth']['diffusion']:8.1f} | "
              f"swan-acc {r['acc_swan']['diffusion']:.3f} | acc {r['acc']['diffusion']:.3f} | "
              f"spent {r['spent']['diffusion']:7.1f}")
    for wv in [0, 1, 2, 5]:
        r = main if wv == 2 else run_market(K=20, w=float(wv), S=4, uncertainty=True)
        abl_w[wv] = r
        print(f"w={wv:3g}: wealth {r['wealth']['diffusion']:8.1f} | "
              f"swan-acc {r['acc_swan']['diffusion']:.3f} | acc {r['acc']['diffusion']:.3f} | "
              f"spent {r['spent']['diffusion']:7.1f}")
    nouc = run_market(K=20, w=2.0, S=4, uncertainty=False)
    print(f"no-uncertainty: wealth {nouc['wealth']['diffusion']:8.1f} | "
          f"maxDD {nouc['drawdown']['diffusion']:.1f} (default maxDD "
          f"{main['drawdown']['diffusion']:.1f})")

    d_on, r_on, d_sw, r_sw = onset_metrics(main)
    results = {}
    ds, js, gs = (main["acc_swan"]["diffusion"], main["acc_swan"]["jepa"],
                  main["acc_swan"]["gate"])
    results["P1"] = (ds > js and ds > gs,
                     f"diffusion swan-acc {ds:.3f} vs jepa {js:.3f}, gate {gs:.3f}")
    results["P2"] = (4 <= drank <= 9 and 800 <= main["spent"]["diffusion"] <= 1600,
                     f"rank {drank}/12, spent {main['spent']['diffusion']:.1f}")
    results["P3"] = (abl_K[1]["acc_swan"]["diffusion"] < abl_K[20]["acc_swan"]["diffusion"]
                     and abl_K[50]["acc_swan"]["diffusion"] >= abl_K[20]["acc_swan"]["diffusion"] - 0.02
                     and abl_K[20]["wealth"]["diffusion"] > abl_K[1]["wealth"]["diffusion"]
                     and abl_K[20]["wealth"]["diffusion"] > abl_K[50]["wealth"]["diffusion"],
                     "swan-acc K1 %.3f < K20 %.3f, K50 %.3f >= K20-0.02; wealth K1 %.0f, "
                     "K20 %.0f, K50 %.0f" % (abl_K[1]["acc_swan"]["diffusion"],
                     abl_K[20]["acc_swan"]["diffusion"], abl_K[50]["acc_swan"]["diffusion"],
                     abl_K[1]["wealth"]["diffusion"], abl_K[20]["wealth"]["diffusion"],
                     abl_K[50]["wealth"]["diffusion"]))
    results["P4"] = (abl_w[5]["acc_swan"]["diffusion"] < abl_w[2]["acc_swan"]["diffusion"]
                     and abl_w[0]["acc_swan"]["diffusion"] <= 0.55,
                     "swan-acc w5 %.3f < w2 %.3f; w0 %.3f <= 0.55"
                     % (abl_w[5]["acc_swan"]["diffusion"], abl_w[2]["acc_swan"]["diffusion"],
                        abl_w[0]["acc_swan"]["diffusion"]))
    results["P5"] = (d_on < r_on and d_sw > r_sw,
                     f"onset5 diffusion {d_on:.3f} < reactive {r_on:.3f}; "
                     f"full-swan diffusion {d_sw:.3f} > reactive {r_sw:.3f}")
    results["P6"] = (nouc["drawdown"]["diffusion"] > main["drawdown"]["diffusion"],
                     f"maxDD no-uncertainty {nouc['drawdown']['diffusion']:.1f} > "
                     f"default {main['drawdown']['diffusion']:.1f}")

    print("\n--- pre-registered predictions (marketplace7_PREDICTIONS.md) ---")
    allpass = True
    for k, (ok, detail) in results.items():
        print(f"{k}: {'PASS' if ok else 'FAIL'} ({detail})")
        allpass = allpass and ok

    data = {
        "main": {kk: main[kk] for kk in
                 ["wealth", "alive", "spent", "acc", "acc_swan", "acc_calm",
                  "swan_call", "drawdown"]},
        "ranking": rank, "diffusion_rank": drank,
        "ablation_K": {str(K): {"wealth": abl_K[K]["wealth"]["diffusion"],
                                "swan_acc": abl_K[K]["acc_swan"]["diffusion"],
                                "acc": abl_K[K]["acc"]["diffusion"],
                                "spent": abl_K[K]["spent"]["diffusion"]}
                       for K in abl_K},
        "ablation_w": {str(wv): {"wealth": abl_w[wv]["wealth"]["diffusion"],
                                 "swan_acc": abl_w[wv]["acc_swan"]["diffusion"],
                                 "acc": abl_w[wv]["acc"]["diffusion"],
                                 "spent": abl_w[wv]["spent"]["diffusion"]}
                       for wv in abl_w},
        "no_uncertainty": {"wealth": nouc["wealth"]["diffusion"],
                           "drawdown": nouc["drawdown"]["diffusion"],
                           "swan_acc": nouc["acc_swan"]["diffusion"]},
        "onset": {"diffusion_onset5": d_on, "reactive_onset5": r_on,
                  "diffusion_swan": d_sw, "reactive_swan": r_sw},
        "predictions": {k: {"pass": bool(v[0]), "detail": v[1]}
                        for k, v in results.items()},
    }
    with open("marketplace7_results.json", "w") as f:
        json.dump(data, f, indent=1)
    print("\nwrote marketplace7_results.json")

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    colors = {"paraconsistent": "#b45cff", "selfbuild": "#22cc66",
              "dialectical": "#ff9f2a", "stigmergic": "#2a7fff",
              "federated": "#ff5555", "contrarian": "#ff2a7f",
              "satisficer": "#8a8a8a", "mimetic": "#c9a227", "gate": "#2adfff",
              "jepa": "#7fff2a", "reactive": "#555555", "diffusion": "#00b3a4"}
    for k in names:
        axes[0].plot(main["Wh"][k], color=colors[k], label=k,
                     lw=2.6 if k == "diffusion" else 1.4)
    for st in swan_times:
        axes[0].axvspan(st - WARM - 12, st - WARM + 12, color="red", alpha=0.12)
    axes[0].axhline(0, color="k", ls="--", lw=1)
    axes[0].set_xlabel("time step (from warmup end)")
    axes[0].set_ylabel("wealth (coins)")
    axes[0].set_title("Marketplace VII: wealth through swans")
    axes[0].legend(fontsize=8, ncol=2)
    Ks = [1, 5, 20, 50]
    axes[1].bar([str(K) for K in Ks],
                [abl_K[K]["wealth"]["diffusion"] for K in Ks],
                color="#00b3a4", alpha=0.85)
    axes[1].set_xlabel("denoising steps K")
    axes[1].set_ylabel("diffusion wealth")
    axes[1].set_title("The refinement tax: wealth vs K")
    fig.suptitle("Marketplace VII: diffusion joins the zoo")
    fig.tight_layout()
    fig.savefig("marketplace7_diffusion.png", dpi=110)
    print("wrote marketplace7_diffusion.png")

    sys.exit(0 if allpass else 1)
