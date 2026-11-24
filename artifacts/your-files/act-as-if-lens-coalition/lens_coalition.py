"""Lens Coalition Game — 3 lens-players on a shared bit-stream world.

Design: DESIGN.md. Predictions (pre-registered): PREDICTIONS.md.
Deterministic: NumPy default_rng(20261026) for the world only;
lens rules are deterministic given the bits. No other randomness.

Run: python3 lens_coalition.py
Writes: results.json, output.txt (in this folder).
Exit 0 iff all 6 predictions pass, else 1 (house convention).
"""
import json
import numpy as np

SEED = 20261026
N = 1000
WARM = 150
SCORED = N - WARM
REGIMES = [0.25, 0.50, 0.75]
SWAN_CENTRES = [336, 550, 820]
SWAN_BIASES = [0.92, 0.08, 0.92]
SWAN_HALF = 12
START_WEALTH = 200.0
PLAYERS = ["reactive", "holder", "router"]
COSTS = {"reactive": 0.0, "holder": 0.40, "router": 0.30}

# ---------------- world ----------------
rng = np.random.default_rng(SEED)
bits = []
regime = 1  # start at 0.50
for t in range(N):
    sb = None
    for c, b in zip(SWAN_CENTRES, SWAN_BIASES):
        if abs(t - c) <= SWAN_HALF:
            sb = b
            break
    if sb is not None:
        bits.append(1 if rng.random() < sb else 0)
    else:
        if rng.random() < 1 / 120:
            regime = int(rng.integers(0, 3))
        bits.append(1 if rng.random() < REGIMES[regime] else 0)
bits = np.array(bits)


def payoff(p, b, cost, extra=0.0):
    sign = 1 if p >= 0.5 else 0
    acc = 1.0 if sign == b else -1.0
    return acc + 4 * (0.25 - (p - b) ** 2) - cost + extra


def solo_p(player, t, prev_p):
    """Solo probability for round t (t >= WARM). prev_p: last round's solo p's."""
    if player == "reactive":
        return 0.85 if bits[t - 1] == 1 else 0.15
    if player == "holder":
        window = bits[max(0, t - 100):t]
        majority = float(np.clip(window.mean(), 0.05, 0.95))
        minority = 0.92 if majority < 0.5 else 0.08
        return (majority + minority) / 2.0, majority, minority
    if player == "router":
        others = [prev_p[p] for p in PLAYERS if p != "router"]
        return sum(others) / len(others)
    raise ValueError(player)


def run_regime(mode):
    """mode: 'cooperation' | 'competition' | 'coopetition'."""
    wealth = {p: START_WEALTH for p in PLAYERS}
    # solo p history for trailing accuracy + router lag
    solo_correct = {p: [] for p in PLAYERS}
    prev_p = {"reactive": 0.5, "holder": 0.5, "router": 0.5}
    # aggregates
    solo_payoffs = []          # per-round solo payoff per player (counterfactual baseline)
    coalition_rounds = []      # dicts per coalition round
    defection_rounds = []      # dicts per defection
    preserved_payoffs = []     # per-member payoff on preserved coalition rounds
    fused_payoffs = []         # per-member payoff on fused coalition rounds
    pairing_payoffs = {}       # (pair tuple) -> list of per-member payoffs
    proposer_idx = 0
    for t in range(WARM, N):
        b = int(bits[t])
        # 1. solo p's
        sp = {}
        holder_claims = None
        for pl in PLAYERS:
            out = solo_p(pl, t, prev_p)
            if pl == "holder":
                sp[pl], maj, mino = out
                holder_claims = (maj, mino)
            else:
                sp[pl] = out
        for pl in PLAYERS:
            solo_correct[pl].append(1 if (1 if sp[pl] >= 0.5 else 0) == b else 0)
        solo_pay = {pl: payoff(sp[pl], b, COSTS[pl]) for pl in PLAYERS}
        for pl in PLAYERS:
            solo_payoffs.append((pl, solo_pay[pl]))

        # 2-7. coalition / solo action
        acted = set()
        if mode == "competition":
            for pl in PLAYERS:
                wealth[pl] += solo_pay[pl]
        else:
            proposer = PLAYERS[proposer_idx % 3]
            proposer_idx += 1
            # partner: highest trailing-50 solo accuracy, ties by player order
            def trail_acc(pl):
                h = solo_correct[pl][-50:]
                return sum(h) / len(h) if h else 0.5
            candidates = [pl for pl in PLAYERS if pl != proposer]
            partner = max(candidates, key=lambda pl: (trail_acc(pl), -PLAYERS.index(pl)))
            accepted = trail_acc(proposer) >= trail_acc(partner) - 0.05
            if not accepted:
                for pl in PLAYERS:
                    wealth[pl] += solo_pay[pl]
            else:
                cmode = "PRESERVE" if proposer == "holder" else "FUSE"
                pc = (sp[proposer] + sp[partner]) / 2.0
                coord = 0.05 if mode == "cooperation" else 0.15
                diff = abs(sp[proposer] - sp[partner])
                preserved = (cmode == "PRESERVE" and diff >= 0.20)
                bonus = 0.25 if preserved else 0.0
                coal_pay = {}
                for pl in (proposer, partner):
                    coal_pay[pl] = payoff(pc, b, COSTS[pl], extra=-coord + bonus)
                # defection (coopetition only): member defects if coalition sign != own sign
                defectors = []
                if mode == "coopetition":
                    csign = 1 if pc >= 0.5 else 0
                    for pl in (proposer, partner):
                        if (1 if sp[pl] >= 0.5 else 0) != csign:
                            defectors.append(pl)
                rec = {"round": t, "proposer": proposer, "partner": partner,
                       "mode": cmode, "preserved": preserved, "diff": diff,
                       "coalition_mean": pc, "defectors": defectors,
                       "coal_pay": coal_pay}
                coalition_rounds.append(rec)
                key = tuple(sorted((proposer, partner)))
                if defectors:
                    for pl in (proposer, partner):
                        if pl in defectors:
                            wealth[pl] += solo_pay[pl]
                            drec = {"round": t, "defector": pl,
                                    "solo_payoff": solo_pay[pl],
                                    "hypothetical_coalition_payoff": coal_pay[pl],
                                    "productive": solo_pay[pl] > coal_pay[pl]}
                            defection_rounds.append(drec)
                        else:
                            wealth[pl] += solo_pay[pl] - 0.20
                    acted.update((proposer, partner))
                else:
                    for pl in (proposer, partner):
                        wealth[pl] += coal_pay[pl]
                        (preserved_payoffs if preserved else fused_payoffs).append(coal_pay[pl])
                    pairing_payoffs.setdefault(key, []).extend(
                        [coal_pay[proposer], coal_pay[partner]])
                    acted.update((proposer, partner))
                # excluded player plays solo
                excluded = [pl for pl in PLAYERS if pl not in acted][0]
                wealth[excluded] += solo_pay[excluded]
        prev_p = sp

    # ---- aggregates ----
    total_gain = {pl: wealth[pl] - START_WEALTH for pl in PLAYERS}
    rank = sorted(PLAYERS, key=lambda pl: -wealth[pl])
    solo_mean = {}
    for pl in PLAYERS:
        vals = [v for (p, v) in solo_payoffs if p == pl]
        solo_mean[pl] = sum(vals) / len(vals)
    solo_baseline = sum(v for (_, v) in solo_payoffs) / len(solo_payoffs)
    coal_total = len(coalition_rounds)
    preserved_n = sum(1 for r in coalition_rounds if r["preserved"])
    preserved_share = preserved_n / coal_total if coal_total else 0.0
    pres_mean = sum(preserved_payoffs) / len(preserved_payoffs) if preserved_payoffs else 0.0
    fused_mean = sum(fused_payoffs) / len(fused_payoffs) if fused_payoffs else 0.0
    # bonus-free preserved mean: subtract 0.25 from each preserved payoff
    pres_mean_nobonus = pres_mean - 0.25 if preserved_payoffs else 0.0
    pairing_mean = {f"{a}+{b}": (sum(v) / len(v) if v else 0.0)
                    for (a, b), v in pairing_payoffs.items()}
    # defection stats (only meaningful in coopetition)
    def_rate = len(defection_rounds) / coal_total if coal_total else 0.0
    # defection rounds counted per defector; coalition rounds with >=1 defector:
    broken_rounds = len({r["round"] for r in defection_rounds})
    broken_rate = broken_rounds / coal_total if coal_total else 0.0
    productive = [d for d in defection_rounds if d["productive"]]
    productive_share = len(productive) / len(defection_rounds) if defection_rounds else 0.0

    return {
        "mode": mode,
        "wealth": wealth,
        "total_gain": sum(total_gain.values()),
        "gains": total_gain,
        "rank": rank,
        "survived": {pl: wealth[pl] > 0 for pl in PLAYERS},
        "coalition_rounds": coal_total,
        "preserved_rounds": preserved_n,
        "preserved_share": preserved_share,
        "preserved_mean_payoff": pres_mean,
        "preserved_payoff_n": len(preserved_payoffs),
        "fused_payoff_n": len(fused_payoffs),
        "preserved_mean_payoff_nobonus": pres_mean_nobonus,
        "fused_mean_payoff": fused_mean,
        "solo_baseline_mean": solo_baseline,
        "solo_mean_by_player": solo_mean,
        "pairing_mean_payoff": pairing_mean,
        "defection_events": len(defection_rounds),
        "broken_coalition_rounds": broken_rounds,
        "broken_rate": broken_rate,
        "defection_productive_share": productive_share,
        "coalition_formation_rate": coal_total / SCORED,
    }


results = {m: run_regime(m) for m in ["cooperation", "competition", "coopetition"]}
coop, comp, coopet = results["cooperation"], results["competition"], results["coopetition"]

# ---- score predictions ----
def mean_pairing(res, pair):
    return res["pairing_mean_payoff"].get(pair, 0.0)

rh_coop = [results[m]["pairing_mean_payoff"].get("holder+reactive", None)
           for m in ["cooperation", "coopetition"]]
rh_vals = [v for v in rh_coop if v is not None]
rh_mean = sum(rh_vals) / len(rh_vals) if rh_vals else 0.0
router_pairs = []
for m in ["cooperation", "coopetition"]:
    for k, v in results[m]["pairing_mean_payoff"].items():
        if "router" in k:
            router_pairs.append(v)
router_mean = sum(router_pairs) / len(router_pairs) if router_pairs else 0.0
solo_base = sum(results[m]["solo_baseline_mean"] for m in results) / 3

pres_share_all = [results[m]["preserved_share"] for m in ["cooperation", "coopetition"]]
# Pooled means are COUNT-weighted. A regime with zero intact preserved
# coalitions (coopetition: every preserved coalition broke) contributes
# nothing, rather than a 0.0 placeholder — the first version of this
# block averaged regime means and used 0.0 for the empty set; corrected
# before the README was written, game rules and predictions untouched.
pres_num = sum(results[m]["preserved_mean_payoff"] * results[m]["preserved_payoff_n"]
               for m in ["cooperation", "coopetition"])
pres_den = sum(results[m]["preserved_payoff_n"] for m in ["cooperation", "coopetition"])
fus_num = sum(results[m]["fused_mean_payoff"] * results[m]["fused_payoff_n"]
              for m in ["cooperation", "coopetition"])
fus_den = sum(results[m]["fused_payoff_n"] for m in ["cooperation", "coopetition"])
pres_mean_pooled = pres_num / pres_den if pres_den else 0.0
fus_mean_pooled = fus_num / fus_den if fus_den else 0.0

preds = {}
preds["P1_total_ordering"] = {
    "predicted": "cooperation > coopetition > competition",
    "observed": {m: results[m]["total_gain"] for m in results},
    "pass": coop["total_gain"] > coopet["total_gain"] > comp["total_gain"],
}
preds["P2_holder_survival_rank"] = {
    "predicted": "holder survives all regimes; last in competition, not last in cooperation",
    "observed": {
        "survived": {m: results[m]["survived"]["holder"] for m in results},
        "rank": {m: results[m]["rank"] for m in results},
        "holder_wealth": {m: results[m]["wealth"]["holder"] for m in results},
    },
    "pass": all(results[m]["survived"]["holder"] for m in results)
    and results["competition"]["rank"][-1] == "holder"
    and results["cooperation"]["rank"][-1] != "holder",
}
preds["P3_preserved_minority_and_pays"] = {
    "predicted": "preserved share < 50% in both coalition regimes; preserved mean > fused mean",
    "observed": {
        "preserved_share": {m: results[m]["preserved_share"] for m in ["cooperation", "coopetition"]},
        "preserved_mean": pres_mean_pooled,
        "fused_mean": fus_mean_pooled,
    },
    "pass": all(s < 0.5 for s in pres_share_all) and pres_mean_pooled > fus_mean_pooled,
}
preds["P4_pairing_beats_solo"] = {
    "predicted": "reactive+holder coalition mean > solo baseline; router coalitions do NOT beat solo baseline",
    "observed": {
        "reactive+holder_mean": rh_mean,
        "router_coalition_mean": router_mean,
        "solo_baseline_mean": solo_base,
    },
    "pass": rh_mean > solo_base and router_mean <= solo_base,
}
preds["P5_defection_productive"] = {
    "predicted": "coopetition broken rate in (0%, 50%); defectors beat hypothetical coalition payoff > 50%",
    "observed": {
        "broken_rate": coopet["broken_rate"],
        "defection_events": coopet["defection_events"],
        "productive_share": coopet["defection_productive_share"],
    },
    "pass": 0 < coopet["broken_rate"] < 0.5 and coopet["defection_productive_share"] > 0.5,
}
preds["P6_reactive_wins_competition"] = {
    "predicted": "reactive rank 1 in competition",
    "observed": {"competition_rank": comp["rank"], "competition_wealth": comp["wealth"]},
    "pass": comp["rank"][0] == "reactive",
}

n_pass = sum(1 for v in preds.values() if v["pass"])
out = {
    "seed": SEED, "rounds_scored": SCORED, "warmup": WARM,
    "swan_centres": SWAN_CENTRES, "swan_biases": SWAN_BIASES,
    "regimes": results, "predictions": preds,
    "score": f"{n_pass}/6",
}
with open("results.json", "w") as f:
    json.dump(out, f, indent=2)

lines = []
lines.append(f"Lens Coalition Game — seed {SEED}, {SCORED} scored rounds")
lines.append(f"Swan centres {SWAN_CENTRES}, biases {SWAN_BIASES} (new world, NOT M5 verbatim)")
for m in ["cooperation", "competition", "coopetition"]:
    r = results[m]
    lines.append(f"\n[{m}] total_gain={r['total_gain']:.2f} wealth={ {k: round(v, 2) for k, v in r['wealth'].items()} } rank={r['rank']}")
    lines.append(f"  coalition_rounds={r['coalition_rounds']} ({r['coalition_formation_rate']:.3f}) preserved={r['preserved_rounds']} share={r['preserved_share']:.3f}")
    lines.append(f"  preserved_mean={r['preserved_mean_payoff']:.4f} (no-bonus {r['preserved_mean_payoff_nobonus']:.4f}) fused_mean={r['fused_mean_payoff']:.4f} solo_baseline={r['solo_baseline_mean']:.4f}")
    lines.append(f"  pairings={ {k: round(v, 4) for k, v in r['pairing_mean_payoff'].items()} }")
    lines.append(f"  broken_rate={r['broken_rate']:.3f} defection_events={r['defection_events']} productive_share={r['defection_productive_share']:.3f}")
lines.append(f"\nPREDICTIONS: {n_pass}/6")
for k, v in preds.items():
    lines.append(f"  {k}: {'PASS' if v['pass'] else 'FAIL'} — {v['observed']}")
txt = "\n".join(lines) + "\n"
with open("output.txt", "w") as f:
    f.write(txt)
print(txt)
raise SystemExit(0 if n_pass == 6 else 1)
