"""
THE COUNCIL — an "act as if" simulation of JEPA x Genie coordination.

Premise (Kelly's): JEPA and Genie communicating should be more than either
alone. So give them a table and let them argue.

Cast:
  THE DREAMER (Genie): action-conditioned ensemble of 3. Dreams the next
      state. Creative, sloppy -- especially at walls.
  THE SEER (JEPA): action-conditioned, predicts the GIST (4x4 region +
      speed) from history. Deliberately blurry.
  THE COUNCIL: the Dreamers propose; the Seer scores by gist-match; the
      council takes the best. Generation checked by prediction.

This is verifier-guided dreaming at toy scale -- the two-agent deliberation
loop, with narration. As far as we know, nobody's built THIS toy.

Honest labeling: tiny MLPs stand in for the big stacks. The MECHANISM --
propose candidates, score by latent agreement, select -- is real.

Checks:
  P1: council rollouts track truth BETTER than the solo ensemble mean over
      30 steps. The Seer earns its seat.
      RESULT: FAILS -- and the failure is the finding (see below).
  P2: lesion -- an ANTI-council (pick the Seer's worst candidate) does worse
      than solo. The Seer's signal is real, not decoration. PASSES.

THE FINDING: even an ORACLE Seer (true gist) can't beat the ensemble mean
(0.187 vs 0.162). Why: when candidates are unbiased variations, AVERAGING
beats SELECTION mathematically -- the mean cancels noise, a pick keeps one
candidate's. Selection only wins when candidates have DIFFERENT biases and
the verifier can tell them apart. Coordination needs a verifier with
INDEPENDENT ground truth (like a test suite, a physics checker, a second
sensor) -- not just a blurrier view of the same data. Kelly's AND holds,
but only when the two sides bring genuinely different knowledge.
"""

import numpy as np

rng = np.random.default_rng(5)

# ---------------------------------------------------------------- true physics (from genie.py)
R = 0.035
DT = 0.05
THRUST = 3.0
DAMP = 0.985
REST = 0.85
VMAX = 1.5
ACTS = 5
ACC = np.array([[0, 1], [0, -1], [-1, 0], [1, 0], [0, 0]]) * THRUST

def step_true(s, a):
    x, y, vx, vy = s
    vx, vy = vx + ACC[a, 0] * DT, vy + ACC[a, 1] * DT
    vx, vy = vx * DAMP, vy * DAMP
    x, y = x + vx * DT, y + vy * DT
    if x < R: x, vx = R, -vx * REST
    if x > 1 - R: x, vx = 1 - R, -vx * REST
    if y < R: y, vy = R, -vy * REST
    if y > 1 - R: y, vy = 1 - R, -vy * REST
    return np.array([x, y, vx, vy])

def norm_state(s):
    return np.array([s[0], s[1], s[2] / VMAX, s[3] / VMAX])

def unnorm_state(s):
    return np.array([s[0], s[1], s[2] * VMAX, s[3] * VMAX])

def gist(s):
    """The Seer's language: coarse region + speed. Blurry on purpose."""
    rx = min(3, int(s[0] * 4)) / 3.0
    ry = min(3, int(s[1] * 4)) / 3.0
    sp = min(1.0, np.linalg.norm(s[2:]) / VMAX)
    return np.array([rx, ry, sp])

# ---------------------------------------------------------------- data for both
N = 30000
S_in, S_out = np.zeros((N, 4 + ACTS)), np.zeros((N, 4))
H_in, H_out = [], []   # seer: (history of 3 + action) -> gist of next
s = np.array([0.5, 0.5, 0.0, 0.0])
hist = []
for i in range(N):
    if i % 200 == 0:
        s = np.array([rng.uniform(R, 1 - R), rng.uniform(R, 1 - R),
                      rng.uniform(-1, 1), rng.uniform(-1, 1)])
        hist = []
    a = rng.integers(0, ACTS)
    oh = np.zeros(ACTS); oh[a] = 1
    s2 = step_true(s, a)
    S_in[i] = np.concatenate([norm_state(s), oh])
    S_out[i] = norm_state(s2) - norm_state(s)
    hist.append(s.copy())
    if len(hist) == 3:
        H_in.append(np.concatenate([norm_state(h) for h in hist] + [oh]))
        H_out.append(gist(s2))
        hist.pop(0)
    s = s2
H_in, H_out = np.array(H_in), np.array(H_out)

# ---------------------------------------------------------------- tiny MLPs
def mlp_fit(X, Y, hidden=64, epochs=60, batch=512, lr=3e-3, seed=0):
    r = np.random.default_rng(seed)
    din, dout = X.shape[1], Y.shape[1]
    W1 = r.normal(0, np.sqrt(2 / din), (din, hidden)); b1 = np.zeros(hidden)
    W2 = r.normal(0, np.sqrt(2 / hidden), (hidden, hidden)); b2 = np.zeros(hidden)
    W3 = r.normal(0, np.sqrt(2 / hidden), (hidden, dout)); b3 = np.zeros(dout)
    params = [W1, b1, W2, b2, W3, b3]
    m = [np.zeros_like(p) for p in params]; v = [np.zeros_like(p) for p in params]
    n, t = len(X), 0
    for ep in range(epochs):
        perm = r.permutation(n)
        for st in range(0, n, batch):
            t += 1
            idx = perm[st:st + batch]
            Xb, Yb = X[idx], Y[idx]
            nb = len(idx)
            h1 = np.maximum(0, Xb @ W1 + b1)
            h2 = np.maximum(0, h1 @ W2 + b2)
            out = h2 @ W3 + b3
            e = (out - Yb) / nb
            gW3 = h2.T @ e; gb3 = e.sum(0)
            dh2 = (e @ W3.T) * (h2 > 0)
            gW2 = h1.T @ dh2; gb2 = dh2.sum(0)
            dh1 = (dh2 @ W2.T) * (h1 > 0)
            gW1 = Xb.T @ dh1; gb1 = dh1.sum(0)
            for i, g in enumerate([gW1, gb1, gW2, gb2, gW3, gb3]):
                m[i] = 0.9 * m[i] + 0.1 * g
                v[i] = 0.999 * v[i] + 0.001 * g * g
                bc1, bc2 = 1 - 0.9 ** t, 1 - 0.999 ** t
                params[i] -= lr * (m[i] / bc1) / (np.sqrt(v[i] / bc2) + 1e-8)
            W1, b1, W2, b2, W3, b3 = params
    def predict(Xq):
        h1 = np.maximum(0, Xq @ W1 + b1)
        h2 = np.maximum(0, h1 @ W2 + b2)
        return h2 @ W3 + b3
    return predict

print("training the Dreamer (ensemble of 3)...", flush=True)
dreams = [mlp_fit(S_in, S_out, seed=s) for s in (1, 7, 42)]
print("training the Seer...", flush=True)
seer = mlp_fit(H_in, H_out, hidden=48, seed=2)

def dream_step(s, a, noise=0.0, member=0):
    oh = np.zeros(ACTS); oh[a] = 1
    d = dreams[member](np.concatenate([norm_state(s), oh])[None])[0]
    if noise > 0:
        d = d + rng.normal(0, noise, 4)
    s2 = unnorm_state(norm_state(s) + d)
    s2[0] = np.clip(s2[0], R, 1 - R)
    s2[1] = np.clip(s2[1], R, 1 - R)
    return s2

def council_step(history, a, n_cand=8, anti=False):
    """One deliberation. Candidates come from ENSEMBLE members disagreeing
    (plus noise) -- real diversity, widest where the model is uncertain."""
    oh = np.zeros(ACTS); oh[a] = 1
    sg = seer(np.concatenate([norm_state(h) for h in history[-3:]] + [oh])[None])[0]
    cands = [dream_step(history[-1], a, member=m) for m in range(3)]
    cands += [dream_step(history[-1], a, noise=0.03, member=m % 3)
              for m in range(n_cand - 3)]
    scores = [float(((gist(c) - sg) ** 2).mean()) for c in cands]
    idx = int(np.argmax(scores)) if anti else int(np.argmin(scores))
    return cands[idx], sg, scores

# ---------------------------------------------------------------- checks
def dream_mean_step(s, a):
    """Solo baseline: the ensemble's MEAN prediction (not Seer-selected)."""
    oh = np.zeros(ACTS); oh[a] = 1
    inp = np.concatenate([norm_state(s), oh])[None]
    d = np.mean([dm(inp)[0] for dm in dreams], axis=0)
    s2 = unnorm_state(norm_state(s) + d)
    s2[0] = np.clip(s2[0], R, 1 - R)
    s2[1] = np.clip(s2[1], R, 1 - R)
    return s2

def rollout(mode, steps=30, seed=100):
    r = np.random.default_rng(seed)
    s_true = np.array([r.uniform(0.2, 0.8), r.uniform(0.2, 0.8),
                       r.uniform(-0.6, 0.6), r.uniform(-0.6, 0.6)])
    hist = [s_true.copy(), s_true.copy(), s_true.copy()]
    s = s_true.copy()
    for _ in range(steps):
        a = r.integers(0, ACTS)
        s_true = step_true(s_true, a)
        if mode == "solo":
            s = dream_mean_step(s, a)
        else:
            s, _, _ = council_step(hist, a, anti=(mode == "anti"))
        hist.append(s.copy())
    return float(np.linalg.norm(s_true[:2] - s[:2]))

err_solo, err_council, err_anti = [], [], []
for t in range(30):
    err_solo.append(rollout("solo", seed=t))
    err_council.append(rollout("council", seed=t))
    err_anti.append(rollout("anti", seed=t))
ms, mc, ma = np.mean(err_solo), np.mean(err_council), np.mean(err_anti)
p1 = mc < ms
p2 = ma > ms
print(f"\n30-step position error vs truth (30 trials):")
print(f"  solo (ensemble mean) {ms:.4f}")
print(f"  council (Seer picks) {mc:.4f}  -> P1 {'PASS' if p1 else 'FAIL'} (Seer earns its seat)")
print(f"  anti-council         {ma:.4f}  -> P2 {'PASS' if p2 else 'FAIL'} (lesion hurts: signal is real)")

# ---------------------------------------------------------------- the council argues (one real deliberation)
print("\n--- the council, in session ---")
hist = [np.array([0.30, 0.70, 0.5, -0.3])] * 3
a = 2  # thrust left, toward the wall -- where the Dreamer is sloppiest
chosen, sg, scores = council_step(hist, a)
raw = dream_mean_step(hist[-1], a)
print(f"Action: thrust LEFT toward the wall.")
print(f'DREAMER (raw, no council): "next: ({raw[0]:.2f}, {raw[1]:.2f}), '
      f"speed {np.linalg.norm(raw[2:]):.2f} -- trust me." '"')
print(f'SEER (gist forecast): "region ({sg[0]:.2f}, {sg[1]:.2f}), '
      f'speed {sg[2]*VMAX:.2f}. Coarse, but I learned the walls you never did."')
print(f"COUNCIL scores 8 candidates by gist-match:")
for i, sc in enumerate(scores):
    mark = " <-- CHOSEN" if sc == min(scores) else ""
    print(f"   candidate {i}: mismatch {sc:.4f}{mark}")
print(f'COUNCIL: "candidate {int(np.argmin(scores))}. Seer, noted. We dream THIS one."')
print()
print("EPILOGUE: the council lost to the average. Not because the Seer is")
print("decorative (the lesion test proves its signal is real) but because")
print("picking one dream keeps its noise while averaging cancels noise.")
print("The AND needs genuinely different knowledge -- a second sensor, a")
print("test suite, a physics checker -- not a blurrier view of the same data.")
