"""Lens-preserving scoreboard analysis for Marketplace VIII.

Re-runs the VIII market once, via the instrumented copy (logic unchanged),
records per-round p, and computes ONLY lens-preserving quantities:
disagreement, leave-one-out marginal contribution (trajectories held
fixed), lifespan-matched / swan-weighted Brier, per-regime breakdown.
No single winner is computed or declared. All numbers printed here are
the script's output; the README quotes them, it does not invent them.
"""
import sys, json, itertools
sys.path.insert(0, "/home/hatch/workspace/your_files/act-as-if-lens-scoreboard")
import numpy as np
import marketplace8_instrumented as m8

out = m8.run_market8(diff_K=20, diff_stake=True)
bits = np.array(m8.bits); is_swan = np.array(m8.is_swan)
swan_times = sorted(int(x) for x in m8.swan_times)
names = out["names"]  # 16 signal animals + "short" (placeholder)
signal = [k for k in names if k != "short"]
p_hist = out["p_hist"]
rounds = sorted(set().union(*[set(p_hist[k].keys()) for k in names]))
print(f"swan_times={swan_times} rounds={rounds[0]}..{rounds[-1]} n_rounds={len(rounds)}")

# --- reproduction check vs VIII saved results ---
saved = json.load(open("/home/hatch/workspace/your_files/act-as-if-marketplace8/marketplace8_results.json"))
rep = {}
for k in names:
    rep[k] = {
        "wealth": round(float(out["wealth"][k]), 1),
        "priced": round(float(out["priced"][k]), 1),
        "brier": round(float(out["mean_brier"][k]), 4),
        "saved_wealth": round(float(saved["main"]["wealth"][k]), 1),
        "saved_priced": round(float(saved["main"]["priced"][k]), 1),
        "saved_brier": round(float(saved["main"]["mean_brier"][k]), 4),
        "alive": bool(out["alive"][k]),
        "n_lived": len(p_hist[k]),
        "first_round": min(p_hist[k]) if p_hist[k] else None,
        "last_round": max(p_hist[k]) if p_hist[k] else None,
    }
    # recomputed lived Brier from p_hist, must match mean_brier
    bs = [(p_hist[k][t] - bits[t]) ** 2 for t in sorted(p_hist[k])]
    rep[k]["brier_recomputed"] = round(float(np.mean(bs)), 4) if bs else None
print("REPRODUCTION:")
for k in names:
    r = rep[k]
    print(f"  {k}: wealth {r['wealth']} vs saved {r['saved_wealth']} | "
          f"priced {r['priced']} vs saved {r['saved_priced']} | "
          f"brier {r['brier']} recomputed {r['brier_recomputed']} vs saved {r['saved_brier']} | "
          f"lived {r['n_lived']} rounds, alive={r['alive']}")

# --- disagreement ---
def spread_for(t, pool):
    ps = [p_hist[k][t] for k in pool if t in p_hist[k]]
    if len(ps) < 2:
        return None, None
    a = np.array(ps)
    # mean absolute pairwise difference
    diff = np.mean(np.abs(a[:, None] - a[None, :]))
    return float(np.std(a)), float(diff)

calm_std, swan_std, onset_std = [], [], []
# swan segments: contiguous runs of is_swan
segments = []
t = 0
while t < len(is_swan):
    if is_swan[t]:
        s = t
        while t < len(is_swan) and is_swan[t]:
            t += 1
        segments.append((s, t - 1))
    else:
        t += 1
onset_rounds = set()
for s, e in segments:
    onset_rounds.update(range(s, min(s + 5, e + 1)))
print(f"SWAN_SEGMENTS={segments} onset_rounds={sorted(onset_rounds)}")
per_round = {}
for t in rounds:
    sd, md = spread_for(t, signal)
    per_round[t] = {"std": sd, "meandiff": md}
    if sd is None:
        continue
    if is_swan[t]:
        swan_std.append(sd)
    else:
        calm_std.append(sd)
    if t in onset_rounds:
        onset_std.append(sd)
dis = {
    "calm_mean_std": float(np.mean(calm_std)),
    "swan_mean_std": float(np.mean(swan_std)),
    "onset_mean_std": float(np.mean(onset_std)),
    "swan_vs_calm_rel": float(np.mean(swan_std) / np.mean(calm_std) - 1.0),
    "onset_vs_calm_rel": float(np.mean(onset_std) / np.mean(calm_std) - 1.0),
    "calm_n": len(calm_std), "swan_n": len(swan_std), "onset_n": len(onset_std),
}
print("DISAGREEMENT:", json.dumps(dis, indent=1))
# per-segment disagreement
for s, e in segments:
    vals = [per_round[t]["std"] for t in range(s, e + 1) if per_round[t]["std"] is not None]
    print(f"  segment {s}..{e}: mean_std={np.mean(vals):.4f} n={len(vals)}")

# --- per-regime per animal ---
regime = {}
for k in names:
    calm = [(p_hist[k][t] - bits[t]) ** 2 for t in sorted(p_hist[k]) if not is_swan[t]]
    swan = [(p_hist[k][t] - bits[t]) ** 2 for t in sorted(p_hist[k]) if is_swan[t]]
    calm_acc = [((p_hist[k][t] > 0.5) == bool(bits[t])) for t in sorted(p_hist[k]) if not is_swan[t]]
    swan_acc = [((p_hist[k][t] > 0.5) == bool(bits[t])) for t in sorted(p_hist[k]) if is_swan[t]]
    regime[k] = {
        "lived_brier": float(np.mean(calm + swan)) if (calm + swan) else None,
        "calm_brier": float(np.mean(calm)) if calm else None,
        "swan_brier": float(np.mean(swan)) if swan else None,
        "calm_acc": float(np.mean(calm_acc)) if calm_acc else None,
        "swan_acc": float(np.mean(swan_acc)) if swan_acc else None,
        "n_calm": len(calm), "n_swan": len(swan),
    }
print("REGIME:")
for k in names:
    print(f"  {k}: {json.dumps(regime[k])}")

# --- lifespan-matched + swan-weighted Brier ---
common_all = [t for t in rounds if all(t in p_hist[k] for k in names)]
common_signal = [t for t in rounds if all(t in p_hist[k] for k in signal)]
common_brier = {}
for k in names:
    if common_all:
        common_brier[k] = float(np.mean([(p_hist[k][t] - bits[t]) ** 2 for t in common_all]))
swan_weighted = {}
for k in names:
    calm = [(p_hist[k][t] - bits[t]) ** 2 for t in sorted(p_hist[k]) if not is_swan[t]]
    swan = [(p_hist[k][t] - bits[t]) ** 2 for t in sorted(p_hist[k]) if is_swan[t]]
    if swan:
        swan_weighted[k] = float((sum(calm) + 3.0 * sum(swan)) / (len(calm) + 3.0 * len(swan)))
    else:
        swan_weighted[k] = None
def rank_of(d):
    items = [(k, v) for k, v in d.items() if v is not None]
    return [k for k, _ in sorted(items, key=lambda kv: kv[1])]
lived_rank = rank_of({k: regime[k]["lived_brier"] for k in names})
common_rank = rank_of(common_brier)
swan_rank = rank_of(swan_weighted)
print(f"COMMON_ALL_ROUNDS: {common_all[0] if common_all else None}..{common_all[-1] if common_all else None} n={len(common_all)}")
print(f"COMMON_SIGNAL_ROUNDS: n={len(common_signal)}")
print("LIVED_RANK:", lived_rank)
print("COMMON_RANK:", common_rank)
print("SWAN_WEIGHTED_RANK:", swan_rank)
print("COMMON_BRIER:", json.dumps(common_brier, indent=1))
print("SWAN_WEIGHTED_BRIER:", json.dumps(swan_weighted, indent=1))

# --- ensemble mean LOO (trajectories held fixed) ---
def ensemble_brier(exclude=None):
    tot, n = 0.0, 0
    for t in rounds:
        ps = [p_hist[k][t] for k in signal if k != exclude and t in p_hist[k]]
        if not ps:
            continue
        tot += (float(np.mean(ps)) - bits[t]) ** 2
        n += 1
    return tot / n if n else None
ens_base = ensemble_brier()
ens_loo = {k: ensemble_brier(exclude=k) for k in signal}
print(f"ENSEMBLE_BASE_BRIER={ens_base:.4f}")
for k in signal:
    print(f"  ensemble LOO -{k}: {ens_loo[k]:.4f} delta={ens_loo[k]-ens_base:+.4f}")

# --- Router LOO (trajectories held fixed, Router logic replayed) ---
router_scores = out["router_scores"]
def router_p_for(t, exclude=None):
    scores = router_scores.get(t)
    if scores is None:
        return None
    cands = {k: v for k, v in scores.items() if k != exclude}
    top = sorted(cands, key=cands.get, reverse=True)[:3]
    ws = np.array([max(cands[k] - 0.45, 0.0) ** 2 for k in top])
    if ws.sum() <= 0:
        ws = np.ones(len(top))
    ws = ws / ws.sum()
    prev = {k: p_hist[k][t - 1] for k in top if (t - 1) in p_hist[k]}
    ps = np.array([prev.get(k, 0.5) for k in top])
    return float(np.sum(ws * ps))
def router_priced(exclude=None):
    priced = 200.0
    for t in sorted(p_hist["router"]):
        p = router_p_for(t, exclude=exclude)
        if p is None:
            continue
        priced += 40.0 * (0.25 - (p - bits[t]) ** 2) - 0.3
    return priced
router_base_recomputed = router_priced()
router_loo = {k: router_priced(exclude=k) for k in signal if k != "router"}
print(f"ROUTER_PRICED_ORIGINAL={out['priced']['router']:.1f} RECOMPUTED={router_base_recomputed:.1f}")
for k in signal:
    if k == "router":
        continue
    print(f"  router LOO -{k}: {router_loo[k]:.1f} delta={router_loo[k]-router_base_recomputed:+.1f}")

# --- what is lost: Router top-3 partner frequency ---
from collections import Counter
tops = Counter()
for t, top in out["router_top"].items():
    for k in top:
        tops[k] += 1
print("ROUTER_TOP3_FREQ:", dict(tops.most_common()))

data = {
    "swan_times": swan_times, "segments": segments,
    "reproduction": rep, "disagreement": dis,
    "regime": regime, "common_all": {"n": len(common_all),
        "first": common_all[0] if common_all else None,
        "last": common_all[-1] if common_all else None},
    "common_brier": common_brier, "swan_weighted": swan_weighted,
    "lived_rank": lived_rank, "common_rank": common_rank, "swan_rank": swan_rank,
    "ensemble_base": ens_base, "ensemble_loo": ens_loo,
    "router_priced_original": float(out["priced"]["router"]),
    "router_priced_recomputed": float(router_base_recomputed),
    "router_loo": router_loo, "router_top3_freq": dict(tops),
}
with open("/home/hatch/workspace/your_files/act-as-if-lens-scoreboard/lens_scoreboard_results.json", "w") as f:
    json.dump(data, f, indent=1)
print("wrote lens_scoreboard_results.json")
