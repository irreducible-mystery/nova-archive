"""Instrumented copy of marketplace8_new_roles.py.
Logic unchanged; recording only: per-round p, Router scores/top-3.
Original: ~/workspace/act-as-if/marketplace8_new_roles.py (not modified).
"""
"""
MARKETPLACE VIII - five new roles, and a market that prices quality.

The M5 black-swan world verbatim (same bits, same swans, seed 99), the
twelve animals of Marketplace VII, plus five new ones for five roles
the zoo lacked: ROUTER (mixture-of-experts dispatcher), CALIBRATOR
(online Platt scaling of the consensus), UNDERWRITER (sells swan
insurance), SHORT (shorts escrowed public calls by badly calibrated
callers), RETRIEVER (RAG-style episode memory over 16-bit patterns).

The market itself changes (see marketplace8_PREDICTIONS.md, written
before this run, for the full declared formulas):
  1. Calibration lane: a parallel priced-wealth ledger pays
     40*(0.25 - Brier) - cost per round; the sign ledger is kept
     exactly as in M5-M7 and both are reported.
  2. Position sizing: directional sign wins scale by a declared stake
     fraction s in [0,1] per animal. Diffusion posts its UNSHRUNK
     denoised mean and lets its M7 spread rule set the stake, so
     sizing now moves money (M7's P6 failure was that it could not).
  3. Escrowed public calls: swan calls on call rounds escrow 5 coins;
     the Short may take the other side of badly-calibrated callers;
     a bounty pool (0.05/animal/round levy) pays right unshorted calls.
  4. Insurance: the Underwriter posts a per-round swan premium from
     the trailing-250 swan frequency x1.3 margin, capped covers,
     reserve floor; distressed-and-uncertain animals buy; a covered
     swan step pays 25.

Exit 0 iff all six predictions pass; exit 1 otherwise.
Seeds: 99 (world), 1001 (gate init), 777 (diffusion RNG). Deterministic.
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




# ================================================================ v8 helpers
def max_drawdown(series):
    peak, dd = -1e18, 0.0
    for v in series:
        peak = max(peak, v)
        dd = max(dd, peak - v)
    return dd


# ================================================================ ROUTER
class Router:
    """Mixture-of-experts dispatcher. No signal of its own: selects the
    top-3 other animals by trailing per-regime performance (scores are
    computed by the market from its correctness records) and posts the
    (score-0.45)^2-weighted mean of their previous-round p."""
    def __init__(self):
        self.t = WARM

    def step(self, prev_p, scores):
        cands = {k: v for k, v in scores.items()}
        top = sorted(cands, key=cands.get, reverse=True)[:3]
        ws = np.array([max(cands[k] - 0.45, 0.0) ** 2 for k in top])
        if ws.sum() <= 0:
            ws = np.ones(len(top))
        ws = ws / ws.sum()
        ps = np.array([prev_p.get(k, 0.5) for k in top])
        p = float(np.sum(ws * ps))
        swan = float(np.std(ps)) > 0.25 if len(ps) > 1 else False
        self.t += 1
        return float(np.clip(p, 0.02, 0.98)), 0.3, swan


# ================================================================ CALIBRATOR
class Calibrator:
    """Platt/temperature scaling of the zoo consensus, fitted online.
    Raw = mean of the other animals' previous-round p (Short excluded).
    (a, b) refit every round by gradient descent on the trailing 150
    (raw, realized bit) pairs."""
    def __init__(self):
        self.a, self.b = 1.0, 0.0
        self.pairs = []          # (raw, outcome), appended by the market
        self.last_raw = 0.5
        self.t = WARM

    @staticmethod
    def _logit(x):
        return np.log(x / (1.0 - x))

    def step(self, prev_p):
        raws = [p for k, p in prev_p.items() if k not in ("calibrator", "short")]
        raw = float(np.mean(raws)) if raws else 0.5
        self.last_raw = raw
        if len(self.pairs) >= 30:
            pr = np.array(self.pairs[-150:])
            z = self._logit(np.clip(pr[:, 0], 0.02, 0.98))
            y = pr[:, 1]
            a, b = self.a, self.b
            for _ in range(30):
                pred = 1.0 / (1.0 + np.exp(-(a * z + b)))
                a -= 0.5 * float(np.mean((pred - y) * z))
                b -= 0.5 * float(np.mean(pred - y))
            self.a, self.b = float(np.clip(a, 0.2, 5.0)), float(np.clip(b, -2.0, 2.0))
        p = 1.0 / (1.0 + np.exp(-(self.a * self._logit(np.clip(raw, 0.02, 0.98)) + self.b)))
        self.t += 1
        return float(np.clip(p, 0.02, 0.98)), LN2 * 1.0, False

    def observe(self, raw, outcome):
        self.pairs.append((raw, float(outcome)))


# ================================================================ RETRIEVER
class Retriever:
    """RAG archetype. Episode store of (last-16-bits pattern -> next bit),
    appended as rounds complete. p = outcome frequency among the k=12
    Hamming-nearest stored patterns, blended with the recent-60 mean
    prior at strength 3."""
    L, KNN, ALPHA = 16, 12, 3.0

    def __init__(self):
        self.patterns = []
        self.outcomes = []
        self.t = WARM

    def step(self):
        t = self.t
        # the episode completed last round: pattern bits[t-17:t-1] -> bits[t-1]
        if t - 1 >= WARM:
            self.patterns.append(bits[t - 1 - self.L:t - 1].copy())
            self.outcomes.append(float(bits[t - 1]))
        prior = float(bits[t - 60:t].mean())
        cur = bits[t - self.L:t]
        if not self.patterns:
            p, swan = prior, False
        else:
            P = np.array(self.patterns)
            dist = np.sum(P != cur, axis=1)
            kk = min(self.KNN, len(dist))
            idx = np.argsort(dist)[:kk]
            outs = np.array(self.outcomes)[idx]
            p = float((outs.sum() + self.ALPHA * prior) / (kk + self.ALPHA))
            swan = bool(kk == self.KNN and (outs.mean() >= 0.85 or outs.mean() <= 0.15))
        self.t += 1
        return float(np.clip(p, 0.02, 0.98)), 0.25, swan


# ================================================================ UNDERWRITER
class Underwriter:
    """Sells swan insurance (market-run book). Its own signal is
    deliberately weak: a slight lean on the last-30 mean."""
    def __init__(self):
        self.t = WARM

    def step(self):
        t = self.t
        p = float(np.clip(0.5 + 0.4 * (bits[t - 30:t].mean() - 0.5), 0.05, 0.95))
        self.t += 1
        return p, 0.2, False


# ================================================================ market v8
PRICED_SCALE = 40.0        # calibration payment = SCALE * (0.25 - brier)
ESCROW = 5.0               # public-call escrow, coins
CALL_BONUS = 4.0           # pool bonus to a right, unshorted caller
LEVY = 0.05                # per animal per round, funds the bounty pool
SHORT_BRIER_THRESH = 0.26  # trailing-50 Brier at/above which Short hunts
SHORT_MAX = 3
SHORT_UPKEEP = 1.0         # on a call round where Short takes no short
COVER_NOTIONAL = 25.0      # insurance payout per covered swan step
COVER_MARGIN = 1.30
COVER_CAP = 6              # covers sold per round
RESERVE_FLOOR = 60.0       # Underwriter stops selling below this wealth


def run_market8(diff_K=20, diff_stake=True):
    field, prev_p = {}, {}
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
    # VIII: Diffusion posts its UNSHRUNK mean; uncertainty acts via stake.
    agents["diffusion"] = Diffusion(K=diff_K, w=2.0, S=4, uncertainty=False)
    agents["router"] = Router()
    agents["calibrator"] = Calibrator()
    agents["retriever"] = Retriever()
    agents["underwriter"] = Underwriter()
    # "short" has no step(): the market posts its placeholder p.

    names = list(agents.keys()) + ["short"]
    for k in names:
        field[k] = deque(maxlen=25)
    trail20 = {k: deque(maxlen=20) for k in names}     # buying rule + mimetic
    trail40 = {k: deque(maxlen=40) for k in names}     # router scoring
    trail40s = {k: deque(maxlen=40) for k in names}    # router: swan steps only
    brier_trail = {k: deque(maxlen=50) for k in names}  # short's hunting stat

    wealth = {k: 200.0 for k in names}     # sign ledger (cash)
    priced = {k: 200.0 for k in names}     # calibration ledger (score)
    peak = {k: 200.0 for k in names}
    alive = {k: True for k in names}
    acc = {k: [] for k in names}
    acc_swan = {k: [] for k in names}
    acc_calm = {k: [] for k in names}
    swan_halves = {k: ([], []) for k in names}   # swan correctness, t<570 / >=570
    spent = {k: 0.0 for k in names}
    swan_calls = {k: [] for k in names}
    brier_sum = {k: 0.0 for k in names}
    brier_n = {k: 0 for k in names}
    stake_sum = {k: 0.0 for k in names}
    Wh = {k: [] for k in names}
    Ph = {k: [] for k in names}
    corr_t = {k: {} for k in names}
    p_hist = {k: {} for k in names}
    router_scores_hist = {}
    router_top_hist = {}

    pool = 0.0
    bonuses_paid = 0.0
    forfeited_to_pool = 0.0
    short_net = 0.0
    shorts_taken = 0
    calls_total = 0
    prem_in = {k: 0.0 for k in names}      # premiums paid per buyer
    pay_out = {k: 0.0 for k in names}      # payouts received per buyer
    covers_sold = 0
    payout_rounds = []

    for t in range(WARM, N - 10):
        step_p, step_cost, step_swan = {}, {}, {}
        order1 = ["gate", "jepa", "reactive", "paraconsistent", "selfbuild",
                  "dialectical", "federated", "satisficer", "stigmergic",
                  "retriever", "underwriter", "diffusion"]
        for k in order1:
            if not alive[k]:
                continue
            r4 = agents[k].step()
            step_p[k], step_cost[k], step_swan[k] = r4[0], r4[1], r4[2]
        if alive["contrarian"]:
            p, cost, swan = agents["contrarian"].step(prev_p)
            step_p["contrarian"], step_cost["contrarian"], step_swan["contrarian"] = p, cost, swan
        if alive["mimetic"]:
            tc = {k: (float(np.mean(trail20[k])) if len(trail20[k]) >= 10 else None)
                  for k in names}
            p, cost, swan, leader = agents["mimetic"].step(prev_p, tc)
            step_p["mimetic"], step_cost["mimetic"], step_swan["mimetic"] = p, cost, swan
        if alive["router"]:
            scores = {}
            for k in names:
                if k in ("router", "short"):
                    continue
                base = float(np.mean(trail40[k])) if len(trail40[k]) >= 10 else 0.5
                if len(trail40s[k]) >= 5:
                    scores[k] = 0.5 * base + 0.5 * float(np.mean(trail40s[k]))
                else:
                    scores[k] = base
            p, cost, swan = agents["router"].step(prev_p, scores)
            router_scores_hist[t] = dict(scores)
            router_top_hist[t] = sorted(scores, key=scores.get, reverse=True)[:3]
            step_p["router"], step_cost["router"], step_swan["router"] = p, cost, swan
        if alive["calibrator"]:
            p, cost, swan = agents["calibrator"].step(prev_p)
            step_p["calibrator"], step_cost["calibrator"] = p, cost
            flags = [v for kk, v in step_swan.items() if kk != "calibrator"]
            step_swan["calibrator"] = bool(flags) and (np.mean(flags) >= 0.4)
        if alive["short"]:
            others = [p for k, p in prev_p.items() if k != "short"]
            step_p["short"] = float(np.mean(others)) if others else 0.5
            step_cost["short"], step_swan["short"] = 0.05, False

        # ---- stakes (mechanism 2)
        stake = {}
        for k in names:
            if not alive[k]:
                continue
            if k == "short":
                stake[k] = 0.0
            elif k == "diffusion" and diff_stake:
                stake[k] = 1.0 / (1.0 + (agents["diffusion"].last_spread / 0.18) ** 2)
            elif k == "diffusion":
                stake[k] = 1.0
            else:
                stake[k] = float(np.clip(abs(2.0 * step_p[k] - 1.0), 0.20, 1.0))
            stake_sum[k] += stake[k]

        # ---- insurance market (mechanism 4): premium posted, covers bought
        covered = []
        if alive["underwriter"] and wealth["underwriter"] >= RESERVE_FLOOR:
            if t <= WARM:
                qhat = 0.04
            else:
                qhat = max(0.04, float(np.mean(is_swan[max(WARM, t - 250):t])))
            surcharge = 1.5 if any(t - r <= 50 for r in payout_rounds) else 1.0
            premium = float(np.clip(COVER_NOTIONAL * qhat * COVER_MARGIN * surcharge,
                                    0.25, 6.0))
            for k in names:
                if len(covered) >= COVER_CAP:
                    break
                if k in ("underwriter", "short") or not alive[k]:
                    continue
                uncertain = bool(step_swan.get(k)) or abs(2.0 * step_p[k] - 1.0) <= 0.25
                cold = len(trail20[k]) >= 20 and float(np.mean(trail20[k])) < 0.55
                if (uncertain or cold) and (peak[k] - wealth[k] >= 10.0) \
                        and wealth[k] > premium:
                    wealth[k] -= premium
                    wealth["underwriter"] += premium
                    prem_in[k] += premium
                    covered.append(k)
                    covers_sold += 1

        # ---- directional payoff, costs, levy (sign ledger)
        for k in names:
            if not alive[k]:
                continue
            p, cost = step_p[k], step_cost[k]
            win = 6.0 if (p > 0.5) == bits[t] else 0.0
            if t % 10 == 0 and t + 10 < N:
                win += 12.0 if (p > 0.5) == bits[t + 10] else 0.0
            wealth[k] += stake[k] * win - cost
            spent[k] += cost
            if t % 10 == 0 and k != "reactive":
                hit = is_swan[t]
                swan_calls[k].append(step_swan[k] == hit)
                if step_swan[k] and hit:
                    wealth[k] += 25.0
                elif step_swan[k] and not hit:
                    wealth[k] -= 10.0
            wealth[k] -= LEVY
            pool += LEVY

        # ---- escrowed public calls + shorting (mechanism 3)
        if t % 10 == 0:
            callers = [k for k in names
                       if alive[k] and step_swan.get(k)
                       and k not in ("short", "underwriter") and wealth[k] >= ESCROW]
            calls_total += len(callers)
            escrowed = []
            for k in callers:
                wealth[k] -= ESCROW
                escrowed.append(k)
            shorts = {}
            if alive["short"]:
                cands = []
                for k in escrowed:
                    if len(brier_trail[k]) >= 20:
                        mb = float(np.mean(brier_trail[k]))
                        if mb >= SHORT_BRIER_THRESH:
                            cands.append((mb, k))
                cands.sort(reverse=True)
                for mb, k in cands[:SHORT_MAX]:
                    if wealth["short"] >= ESCROW:
                        wealth["short"] -= ESCROW
                        shorts[k] = True
                        shorts_taken += 1
                if not shorts:
                    wealth["short"] -= SHORT_UPKEEP
            hit = bool(is_swan[t])
            for k in escrowed:
                if hit:
                    wealth[k] += ESCROW
                    if shorts.get(k):
                        wealth[k] += ESCROW        # short's counter-stake
                        short_net -= ESCROW
                    else:
                        bonus = min(CALL_BONUS, pool)
                        wealth[k] += bonus
                        pool -= bonus
                        bonuses_paid += bonus
                else:
                    if shorts.get(k):
                        wealth["short"] += 2 * ESCROW  # stake back + caller's escrow
                        short_net += ESCROW
                    else:
                        pool += ESCROW
                        forfeited_to_pool += ESCROW

        # ---- insurance payout
        if is_swan[t] and covered:
            for k in covered:
                wealth[k] += COVER_NOTIONAL
                wealth["underwriter"] -= COVER_NOTIONAL
                pay_out[k] += COVER_NOTIONAL
            payout_rounds.append(t)

        # ---- calibration lane (mechanism 1) + records
        for k in names:
            if not alive[k]:
                continue
            p = step_p[k]
            brier = float((p - bits[t]) ** 2)
            brier_sum[k] += brier
            brier_n[k] += 1
            brier_trail[k].append(brier)
            priced[k] += PRICED_SCALE * (0.25 - brier) - step_cost[k]
            correct = (p > 0.5) == bits[t]
            acc[k].append(correct)
            corr_t[k][t] = bool(correct)
            trail20[k].append(1.0 if correct else 0.0)
            trail40[k].append(1.0 if correct else 0.0)
            if is_swan[t]:
                acc_swan[k].append(correct)
                trail40s[k].append(1.0 if correct else 0.0)
                swan_halves[k][0 if t < 570 else 1].append(correct)
            else:
                acc_calm[k].append(correct)
            if k == "satisficer":
                agents["satisficer"].observe(correct)
            if k == "calibrator":
                agents["calibrator"].observe(agents["calibrator"].last_raw, bits[t])
            if wealth[k] < 0:
                alive[k] = False
            field[k].append((t, p))
        for _k, _p in step_p.items():
            p_hist[_k][t] = float(_p)
        prev_p = dict(step_p)
        for k in names:
            peak[k] = max(peak[k], wealth[k])
            Wh[k].append(wealth[k] if alive[k] else (Wh[k][-1] if Wh[k] else 0))
            Ph[k].append(priced[k] if alive[k] else (Ph[k][-1] if Ph[k] else 0))

    mean_brier = {k: (brier_sum[k] / brier_n[k] if brier_n[k] else 0.25)
                  for k in names}
    out = {"names": names, "wealth": wealth, "priced": priced, "alive": alive,
           "spent": spent, "Wh": Wh, "Ph": Ph,
           "mean_brier": mean_brier,
           "acc": {k: float(np.mean(acc[k])) if acc[k] else 0.0 for k in names},
           "acc_swan": {k: float(np.mean(acc_swan[k])) if acc_swan[k] else 0.0
                        for k in names},
           "acc_calm": {k: float(np.mean(acc_calm[k])) if acc_calm[k] else 0.0
                        for k in names},
           "swan_call": {k: float(np.mean(swan_calls[k])) if swan_calls[k] else 0.0
                         for k in names},
           "drawdown": {k: max_drawdown(Wh[k]) for k in names},
           "swan_halves": {k: (float(np.mean(swan_halves[k][0])) if swan_halves[k][0] else 0.0,
                               float(np.mean(swan_halves[k][1])) if swan_halves[k][1] else 0.0)
                           for k in names},
           "avg_stake": {k: (stake_sum[k] / brier_n[k] if brier_n[k] else 0.0)
                         for k in names},
           "insurance": {"premiums": prem_in, "payouts": pay_out,
                         "premiums_total": float(sum(prem_in.values())),
                         "payouts_total": float(sum(pay_out.values())),
                         "underwriter_net": float(sum(prem_in.values())
                                                  - sum(pay_out.values())),
                         "covers_sold": covers_sold},
           "escrow": {"pool_final": pool, "bonuses_paid": bonuses_paid,
                      "forfeited_to_pool": forfeited_to_pool,
                      "short_net": short_net, "shorts_taken": shorts_taken,
                      "calls_total": calls_total},
           "corr_t": corr_t, "p_hist": p_hist, "router_scores": router_scores_hist, "router_top": router_top_hist}
    return out


def rank_of(table, key):
    order = sorted(table.keys(), key=lambda k: table[k], reverse=True)
    return order.index(key) + 1, order

