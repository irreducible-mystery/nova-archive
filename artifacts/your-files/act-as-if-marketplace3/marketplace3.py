"""
MARKETPLACE III — is antifragility possible?

The question: can a model GAIN from volatility, not just survive it?
Taleb's bar: fragile = harmed by disorder, robust = unaffected,
antifragile = IMPROVED by disorder (convex payoff in the stressor).

Hypothesis: antifragility requires learnable meta-structure in the
volatility itself. If swans are truly i.i.d. unprecedented, nothing can
gain — robustness (JEPA) is the ceiling. If swans recur (meta-pattern),
an agent that grows permanent hypotheses from shocks can gain.

The agent: HYDRA. Starts with warmup hypotheses. On persistent surprise,
spawns a new hypothesis fitted to the novel regime — and KEEPS it forever.
The hypothesis set only grows. Each shock makes it strictly more capable.
(The record is eternal; selection among hypotheses is the temporal surface.)

Cost of antifragility: selection among K hypotheses costs 0.2*K per step.
Optionality is priced. More heads = more expensive to choose.

Two worlds:
  A: 4 swans, each a fresh unprecedented bias (i.i.d., no meta-structure).
  B: 4 swans drawn from 2 recurring types (meta-structure exists).

Pre-registered:
  P1: World B — Hydra's per-swan wealth delta improves swan 1 -> 4
      (learning curve = antifragile signature). World A — no improvement.
  P2: World A — Hydra total wealth ~= JEPA (no meta-structure, no gain).
  P3: World B — Hydra total wealth > JEPA (converts recurring swans to profit).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LN2 = np.log(2)
N = 1200
WARM = 150
SWAN_LEN = 25
REGIMES = [0.25, 0.50, 0.75]


def make_world(world_type, seed):
    rng = np.random.default_rng(seed)
    swan_times = [300 + rng.integers(-30, 30), 550 + rng.integers(-30, 30),
                  800 + rng.integers(-30, 30), 1050 + rng.integers(-30, 30)]
    if world_type == "A":
        swan_biases = [rng.uniform(0.85, 0.95) if rng.random() < 0.5
                       else rng.uniform(0.05, 0.15) for _ in range(4)]
    else:
        order = rng.permutation([0, 1, 0, 1])
        swan_biases = [[0.92, 0.08][i] for i in order]
    bits, true_reg, is_swan = [], [], []
    r = 1
    for t in range(N):
        sb = None
        for i, st in enumerate(swan_times):
            if abs(t - st) < SWAN_LEN // 2:
                sb = swan_biases[i]
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
    return bits, true_reg, is_swan, swan_times, warm_bias, rng


# ---------------------------------------------------------------- HYDRA
class Hydra:
    def __init__(self, bits, warm_bias):
        self.bits = bits
        self.hyps = [{"bias": b, "source": "warmup"} for b in warm_bias]
        self.streak = 0
        self.t = WARM
        self.n_heads = [len(self.hyps)]

    @staticmethod
    def _ll(bias, window):
        b = min(max(bias, 1e-6), 1 - 1e-6)
        return float(np.mean(window * np.log(b) + (1 - window) * np.log(1 - b)))

    def step(self):
        t = self.t
        window = self.bits[t - 15:t]
        lls = [self._ll(h["bias"], window) for h in self.hyps]
        best = int(np.argmax(lls))
        # novelty: no hypothesis explains the recent window (error-based,
        # because LL is too forgiving when a warmup bias is merely "close")
        min_err = min(abs(window.mean() - h["bias"]) for h in self.hyps)
        if min_err > 0.15:
            self.streak += 1
        else:
            self.streak = max(0, self.streak - 2)
        cost = 0.2 * len(self.hyps)  # price of optionality
        new = False
        if self.streak >= 6 and len(self.hyps) < 8:
            nb = float(np.clip(self.bits[t - 20:t].mean(), 0.05, 0.95))
            self.hyps.append({"bias": nb, "source": "novel"})
            self.streak = 0
            cost += 5.0
            new = True
            best = len(self.hyps) - 1
        swan = self.hyps[best]["source"] == "novel" or self.streak >= 3 or new
        p = self.hyps[best]["bias"]
        self.t += 1
        self.n_heads.append(len(self.hyps))
        return p, cost, swan, best


# ---------------------------------------------------------------- GATE (frantic adapter, from marketplace2)
GDIM = 6
GA = -(0.4 + 0.6 * np.arange(GDIM) / GDIM)


def run_gate(bits, warm_bias, seed):
    rng = np.random.default_rng(seed + 1)
    GB = rng.normal(0, 0.5, (GDIM, 2))

    def gdelta(surprise, scale):
        return np.log1p(np.exp(scale * (3.0 * surprise - 1.0)))

    gh = np.zeros(GDIM)
    states, ys = [], []
    for t in range(WARM):
        x = np.array([bits[t], 1 - bits[t]])
        pm = np.mean(bits[max(0, t - 10):t]) if t > 0 else 0.5
        d = gdelta(abs(bits[t] - pm), 1.0)
        gh = np.exp(d * GA) * gh + (d * GB) @ x
        states.append(gh.copy()); ys.append(bits[t])
    states = np.array(states); ys = np.array(ys)
    w = np.zeros(GDIM + 1)
    Xa = np.column_stack([states, np.ones(len(states))])
    for _ in range(800):
        p = 1 / (1 + np.exp(-Xa @ w))
        w -= 0.5 * Xa.T @ (p - ys) / len(ys)
    h = gh.copy()
    surprises = []
    out = []
    for t in range(WARM, N - 10):
        x = np.array([bits[t - 1], 1 - bits[t - 1]])
        pm = np.mean(bits[t - 10:t - 1])
        s = abs(bits[t - 1] - pm)
        surprises.append(s)
        swan = np.mean(surprises[-10:]) > 0.35 if len(surprises) >= 10 else False
        d = gdelta(s, 2.5 if swan else 1.0)
        cost = LN2 * float(np.sum(1 - np.exp(d * GA))) + 0.1
        h = np.exp(d * GA) * h + (d * GB) @ x
        p = float(1 / (1 + np.exp(-(h @ w[:GDIM] + w[GDIM]))))
        out.append((p, cost, swan))
    return out


# ---------------------------------------------------------------- JEPA (strategic ignorance, from marketplace2)
def run_jepa(bits, warm_bias):
    out = []
    latent = 1
    updates = []
    swan_mode = False
    for t in range(WARM, N - 10):
        if swan_mode:
            recent = bits[t - 8:t]
            if abs(recent.mean() - 0.5) < 0.2:
                swan_mode = False
            out.append((0.5, LN2 * 0.5, 1, True))
            updates.append(False)
            continue
        recent = bits[t - 8:t]
        surprise = abs(recent.mean() - warm_bias[latent])
        update = surprise > 0.12
        updates.append(update)
        if len(updates) >= 10 and sum(updates[-10:]) >= 8:
            swan_mode = True
        if update:
            cost = LN2 * 7
            win = bits[t - 15:t].mean()
            latent = int(np.argmin([abs(win - b) for b in warm_bias]))
        else:
            cost = LN2 * 1
        out.append((warm_bias[latent], cost, latent, swan_mode))
    return out


# ---------------------------------------------------------------- market
def run_market(world_type, seed):
    bits, true_reg, is_swan, swan_times, warm_bias, _ = make_world(world_type, seed)
    hydra = Hydra(bits, warm_bias)
    gate_out = run_gate(bits, warm_bias, seed)
    jepa_out = run_jepa(bits, warm_bias)

    agents = ["hydra", "gate", "jepa"]
    wealth = {a: 200.0 for a in agents}
    alive = {a: True for a in agents}
    acc = {a: [] for a in agents}
    spent = {a: 0.0 for a in agents}
    swan_calls = {a: [] for a in agents}
    Wh = {a: [] for a in agents}
    swan_wealth = {"hydra": []}  # wealth at each swan start/end
    swan_marks = []  # (start_idx, end_idx) in market-time

    # map swan times to market indices
    for st in swan_times:
        s = st - WARM - SWAN_LEN // 2
        e = st - WARM + SWAN_LEN // 2
        swan_marks.append((max(s, 0), e))

    # record hydra wealth at swan boundaries
    hydra_swan_delta = []
    cur_mark = 0

    # --- main loop ---
    hydra = Hydra(bits, warm_bias)
    for i, t in enumerate(range(WARM, N - 10)):
        if alive["hydra"]:
            p, cost, swan, _ = hydra.step()
            win = 6 if (p > 0.5) == bits[t] else 0
            if t % 10 == 0 and t + 10 < N:
                win += 12 if (p > 0.5) == bits[t + 10] else 0
            if t % 20 == 0 and true_reg[t] < 3:
                win += 20 if int(np.argmin([abs(p - b) for b in warm_bias])) == true_reg[t] else 0
            if t % 10 == 0:
                hit = is_swan[t]
                swan_calls["hydra"].append(swan == hit)
                win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
            wealth["hydra"] += win - cost
            spent["hydra"] += cost
            acc["hydra"].append((p > 0.5) == bits[t])
            if wealth["hydra"] < 0:
                alive["hydra"] = False
        if alive["gate"]:
            p, cost, swan = gate_out[i]
            win = 6 if (p > 0.5) == bits[t] else 0
            if t % 20 == 0 and true_reg[t] < 3:
                win += 20 if int(np.argmin([abs(p - b) for b in warm_bias])) == true_reg[t] else 0
            if t % 10 == 0:
                hit = is_swan[t]
                swan_calls["gate"].append(swan == hit)
                win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
            wealth["gate"] += win - cost
            spent["gate"] += cost
            acc["gate"].append((p > 0.5) == bits[t])
            if wealth["gate"] < 0:
                alive["gate"] = False
        if alive["jepa"]:
            p, cost, latent, swan = jepa_out[i]
            win = 6 if (p > 0.5) == bits[t] else 0
            if t % 20 == 0 and true_reg[t] < 3:
                win += 20 if (not swan and latent == true_reg[t]) else 0
            if t % 10 == 0:
                hit = is_swan[t]
                swan_calls["jepa"].append(swan == hit)
                win += 25 if (swan and hit) else (-10 if (swan and not hit) else 0)
            wealth["jepa"] += win - cost
            spent["jepa"] += cost
            acc["jepa"].append((p > 0.5) == bits[t])
            if wealth["jepa"] < 0:
                alive["jepa"] = False
        for a in agents:
            Wh[a].append(wealth[a] if alive[a] else (Wh[a][-1] if Wh[a] else 0))

    # per-swan deltas for hydra
    for (s, e) in swan_marks:
        if e < len(Wh["hydra"]) and s < len(Wh["hydra"]):
            hydra_swan_delta.append(Wh["hydra"][e] - Wh["hydra"][s])

    return {
        "wealth": wealth, "alive": alive, "acc": acc, "spent": spent,
        "swan_calls": swan_calls, "Wh": Wh, "swan_times": swan_times,
        "hydra_swan_delta": hydra_swan_delta, "hydra_heads": hydra.n_heads,
    }


results = {}
for wt in ("A", "B"):
    results[wt] = run_market(wt, seed=77)
    r = results[wt]
    print(f"\n=== WORLD {wt} ({'i.i.d. swans' if wt=='A' else 'recurring swans'}) ===")
    for a in ("hydra", "gate", "jepa"):
        accm = np.mean(r["acc"][a]) if r["acc"][a] else 0
        eff = accm / (r["spent"][a] / max(len(r["acc"][a]), 1)) * 100
        sc = np.mean(r["swan_calls"][a]) if r["swan_calls"][a] else 0
        print(f"{a:6s} | wealth {r['wealth'][a]:8.1f} | alive {str(r['alive'][a]):5s} | "
              f"acc {accm:.3f} | swan-call {sc:.2f} | spent {r['spent'][a]:7.1f} | {eff:.1f} acc/100c")
    print(f"hydra per-swan wealth delta: {[f'{d:+.1f}' for d in r['hydra_swan_delta']]}")
    print(f"hydra final heads: {r['hydra_heads'][-1]}")

# P1 check: monotonic improvement in World B?
dB = results["B"]["hydra_swan_delta"]
dA = results["A"]["hydra_swan_delta"]
print(f"\nP1 (antifragile signature): World B deltas improving? "
      f"{all(dB[i+1] > dB[i] for i in range(len(dB)-1))}  {dB}")
print(f"    World A deltas improving? "
      f"{all(dA[i+1] > dA[i] for i in range(len(dA)-1))}  {dA}")
print(f"P2 (ceiling): World A hydra {results['A']['wealth']['hydra']:.0f} vs "
      f"jepa {results['A']['wealth']['jepa']:.0f}")
print(f"P3 (value): World B hydra {results['B']['wealth']['hydra']:.0f} vs "
      f"jepa {results['B']['wealth']['jepa']:.0f}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
for ax, wt in zip(axes, ("A", "B")):
    r = results[wt]
    for a, c in (("hydra", "#22cc66"), ("gate", "#2a7fff"), ("jepa", "#ff9f2a")):
        ax.plot(r["Wh"][a], color=c, label=a, lw=2)
    for st in r["swan_times"]:
        ax.axvspan(st - WARM - 12, st - WARM + 12, color="red", alpha=0.12)
    ax.axhline(0, color="k", ls="--", lw=1)
    ax.set_title(f"World {wt}: {'i.i.d. swans' if wt=='A' else 'recurring swans'}")
    ax.set_xlabel("time step (from warmup end)")
    ax.legend()
axes[0].set_ylabel("wealth (energy coins)")
fig.suptitle("Marketplace III: can Hydra gain from volatility?")
fig.tight_layout()
fig.savefig("marketplace3.png", dpi=110)
print("\nwrote marketplace3.png")
