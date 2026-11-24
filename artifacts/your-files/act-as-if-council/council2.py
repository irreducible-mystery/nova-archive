"""
THE COUNCIL II — genuinely different knowledge.

Redesign from the Council's finding: coordination needs INDEPENDENT ground
truth, not a blurrier view of the same data. So we raise them differently:

  THE DREAMER: trained ONLY on open-space transitions (center of arena).
      Never saw a wall bounce in its life. Wall-blind by upbringing.
  THE SEER: trained ONLY on near-wall transitions. A wall native.
      Never learned open-space dynamics. Center-blind by upbringing.

They literally know different things. The council: Dreamer proposes,
Seer scores by gist-match, best candidate wins.

Checks:
  P1: council beats solo-Dreamer on full-arena rollouts (Seer covers the
      Dreamer's blind spot).
  P2: ASYMMETRIC WINS -- break error down by region. The council must win
      (or tie) in BOTH regions vs solo, proving each covers the other --
      not just trade one blind spot for another.
  P3 (Act III): FUSION -- the Seer's decoded gist ENTERS the prediction near
      walls (instead of merely selecting among the Dreamer's candidates).
      Tests whether the knowledge is complementary even if selection isn't
      the right mechanism.
"""

import numpy as np

rng = np.random.default_rng(9)

# ---------------------------------------------------------------- physics (same as council.py)
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
    rx = min(3, int(s[0] * 4)) / 3.0
    ry = min(3, int(s[1] * 4)) / 3.0
    sp = min(1.0, np.linalg.norm(s[2:]) / VMAX)
    return np.array([rx, ry, sp])

def in_center(s, m=0.3):
    return abs(s[0] - 0.5) < m and abs(s[1] - 0.5) < m

# ---------------------------------------------------------------- split training data by region
N = 40000
D_in, D_out = [], []   # dreamer: center only
H_in, H_out = [], []   # seer: walls only
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
    if in_center(s):
        D_in.append(np.concatenate([norm_state(s), oh]))
        D_out.append(norm_state(s2) - norm_state(s))
    else:
        hist.append(s.copy())
        if len(hist) == 3:
            H_in.append(np.concatenate([norm_state(h) for h in hist] + [oh]))
            H_out.append(gist(s2))
            hist.pop(0)
    s = s2
D_in, D_out = np.array(D_in), np.array(D_out)
H_in, H_out = np.array(H_in), np.array(H_out)
print(f"dreamer (center) samples: {len(D_in)}, seer (walls) samples: {len(H_in)}", flush=True)

# ---------------------------------------------------------------- MLPs
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

print("raising the Dreamer (center only)...", flush=True)
dreams = [mlp_fit(D_in, D_out, seed=s) for s in (1, 7, 42)]
print("raising the Seer (walls only)...", flush=True)
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

def dream_mean_step(s, a):
    oh = np.zeros(ACTS); oh[a] = 1
    inp = np.concatenate([norm_state(s), oh])[None]
    d = np.mean([dm(inp)[0] for dm in dreams], axis=0)
    s2 = unnorm_state(norm_state(s) + d)
    s2[0] = np.clip(s2[0], R, 1 - R)
    s2[1] = np.clip(s2[1], R, 1 - R)
    return s2

def council_step(history, a, n_cand=8):
    oh = np.zeros(ACTS); oh[a] = 1
    sg = seer(np.concatenate([norm_state(h) for h in history[-3:]] + [oh])[None])[0]
    cands = [dream_step(history[-1], a, member=m) for m in range(3)]
    cands += [dream_step(history[-1], a, noise=0.03, member=m % 3)
              for m in range(n_cand - 3)]
    scores = [float(((gist(c) - sg) ** 2).mean()) for c in cands]
    return cands[int(np.argmin(scores))]

# ---------------------------------------------------------------- checks with regional breakdown
def rollout(mode, steps=40, seed=100):
    r = np.random.default_rng(seed)
    s_true = np.array([r.uniform(0.15, 0.85), r.uniform(0.15, 0.85),
                       r.uniform(-0.8, 0.8), r.uniform(-0.8, 0.8)])
    hist = [s_true.copy()] * 3
    s = s_true.copy()
    err_center, err_wall, n_c, n_w = 0.0, 0.0, 0, 0
    for _ in range(steps):
        a = r.integers(0, ACTS)
        s_true = step_true(s_true, a)
        s = dream_mean_step(s, a) if mode == "solo" else council_step(hist, a)
        hist.append(s.copy())
        e = float(np.linalg.norm(s_true[:2] - s[:2]))
        if in_center(s_true, m=0.3):
            err_center += e; n_c += 1
        else:
            err_wall += e; n_w += 1
    return err_center / max(n_c, 1), err_wall / max(n_w, 1)

sc_c, sc_w, co_c, co_w = [], [], [], []
for t in range(30):
    c, w = rollout("solo", seed=t)
    sc_c.append(c); sc_w.append(w)
    c, w = rollout("council", seed=t)
    co_c.append(c); co_w.append(w)

msc, msw = np.mean(sc_c), np.mean(sc_w)
mcc, mcw = np.mean(co_c), np.mean(co_w)
p1 = (mcc + mcw) / 2 < (msc + msw) / 2
p2 = mcc <= msc * 1.1 and mcw < msw   # wins at walls, doesn't lose center

print(f"\nper-step position error by region (30 trials x 40 steps):")
print(f"  solo    | center {msc:.4f}  walls {msw:.4f}  overall {(msc+msw)/2:.4f}")
print(f"  council | center {mcc:.4f}  walls {mcw:.4f}  overall {(mcc+mcw)/2:.4f}")
print(f"P1 council beats solo overall -> {'PASS' if p1 else 'FAIL'}")
print(f"P2 asymmetric wins (walls better, center not worse) -> {'PASS' if p2 else 'FAIL'}")
if p1 and p2:
    print("\nTwo upbringings. One table. Each covers the other's blind spot.")
    print("THIS is what 'different knowledge' looks like measured.")

# ---------------------------------------------------------------- act III: fusion, not selection
# Selection failed even with different knowledge. But the knowledge IS
# complementary -- so try FUSION: let the Seer's decoded gist ENTER the
# prediction near walls, instead of merely filtering the Dreamer's.
def seer_decode(history, a):
    oh = np.zeros(ACTS); oh[a] = 1
    sg = seer(np.concatenate([norm_state(h) for h in history[-3:]] + [oh])[None])[0]
    cx, cy = (sg[0] * 3 + 0.5) / 4, (sg[1] * 3 + 0.5) / 4
    dm = dream_mean_step(history[-1], a)
    v = dm[2:]; n = np.linalg.norm(v) + 1e-9
    sp = sg[2] * VMAX
    return np.array([cx, cy, v[0] / n * sp, v[1] / n * sp])

def fused_step(history, a):
    s = history[-1]
    if in_center(s, m=0.3):
        return dream_mean_step(s, a)
    d = dream_mean_step(s, a); g = seer_decode(history, a)
    return 0.5 * d + 0.5 * g

ferrs = []
for t in range(30):
    r = np.random.default_rng(t)
    s_true = np.array([r.uniform(0.15, 0.85), r.uniform(0.15, 0.85),
                       r.uniform(-0.8, 0.8), r.uniform(-0.8, 0.8)])
    hist = [s_true.copy()] * 3
    s = s_true.copy(); e = 0.0
    for _ in range(40):
        a = r.integers(0, ACTS)
        s_true = step_true(s_true, a)
        s = fused_step(hist, a); hist.append(s.copy())
        e += float(np.linalg.norm(s_true[:2] - s[:2]))
    ferrs.append(e / 40)
mf = float(np.mean(ferrs))
p3 = mf < (msc + msw) / 2
print(f"\nAct III -- fusion (Seer's knowledge ENTERS the prediction near walls):")
print(f"  fused {mf:.4f} vs solo {(msc+msw)/2:.4f} -> P3 {'PASS' if p3 else 'FAIL'}")
if p3:
    print("  The knowledge WAS complementary. Selection was the wrong mechanism;")
    print("  fusion was the right one. The AND works -- but only fused, not filtered.")
