"""Holder v3 — portfolio holder, flip-stale collapse rule (N=25), stipend variants.

Design: sketch in ../act-as-if-holder-v3-sketch/SKETCH.md; predictions locked in PREDICTIONS.md BEFORE any run.
World and triad mechanics reused from ../act-as-if-lens-coalition/
lens_coalition.py: same seed, same world generation order, same
payoff formula, same proposer rotation / invitation / defection rules.
Deterministic: NumPy default_rng(20261026) for the world only.

Runs: python3 holder_v3.py
Writes: results.json, output.txt (in this folder).
Exit 0 iff all 5 predictions pass, else 1 (house convention).
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

# ---------------- world (identical generation order to v1) ----------------
rng = np.random.default_rng(SEED)
bits = []
regime = 1
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


def brier(p, b):
    return (p - b) ** 2


def window_kind(t):
    for c in SWAN_CENTRES:
        if abs(t - c) <= SWAN_HALF:
            return "swan"
        if c + 13 <= t <= c + 42:
            return "postflip"
    return "calm"


def majority_minority(t):
    window100 = bits[max(0, t - 100):t]
    M = float(np.clip(window100.mean(), 0.05, 0.95))
    m = 0.92 if M < 0.5 else 0.08
    w20 = bits[max(0, t - 20):t].mean()
    w100 = window100.mean()
    flip = (w20 - 0.5) * (w100 - 0.5) < 0
    return M, m, bool(flip)


# Warm-up Brier history for M and m (recorded, not scored), so the
# trailing-50 window is full from the first scored round.
warm_M_brier, warm_m_brier = [], []
for t in range(1, WARM):
    M, m, _ = majority_minority(t)
    warm_M_brier.append(brier(M, int(bits[t])))
    warm_m_brier.append(brier(m, int(bits[t])))


def run_triad(mode, holder_kind):
    """holder_kind: 'v3_stipend' | 'v3_nostipend' | 'v1'.
    Players are always reactive / holder / router, in that order."""
    PLAYERS = ["reactive", "holder", "router"]
    if holder_kind == "v1":
        COSTS = {"reactive": 0.0, "holder": 0.40, "router": 0.30}
    else:
        COSTS = {"reactive": 0.0, "holder": 0.05, "router": 0.30}
    wealth = {p: START_WEALTH for p in PLAYERS}
    solo_correct = {p: [] for p in PLAYERS}
    prev_p = {"reactive": 0.5, "holder": 0.5, "router": 0.5}
    # Holder v2 state
    state = "holding"  # or "collapsed"
    collapse_remaining = 0
    collapse_winner = None
    holding_rounds = 0
    false_streak = 0  # consecutive scored rounds, in holding state, with flip == False
    holding_by_kind = {"calm": 0, "swan": 0, "postflip": 0}
    collapses = []  # {round, trigger, winner, brier_gap, holding_rounds_before, false_streak}
    total_stipend = 0.0
    holding_round_count = 0
    collapsed_round_count = 0
    # Per-round records for Holder
    rec = []  # dicts: round, kind, M, m, flip, state, holder_pay_excl, stipend
    M_hist = list(warm_M_brier)
    m_hist = list(warm_m_brier)
    # Consultation: Router-as-proposer attempts
    router_attempts = {"postflip": [0, 0], "calm": [0, 0], "swan": [0, 0]}
    # router_attempts[kind] = [attempts, invites_holder]
    holder_partner_rounds = {"postflip": [0, 0], "calm": [0, 0], "swan": [0, 0]}
    proposer_idx = 0
    first_negative = {}
    for t in range(WARM, N):
        b = int(bits[t])
        kind = window_kind(t)
        M, m, flip = majority_minority(t)
        # --- Holder v3 collapse check (flip-stale ONLY, N=25) ---
        # No Brier-gap branch exists in this file by design. Collapse
        # only when the flip flag has been FALSE for 25 consecutive
        # scored rounds in holding state.
        if holder_kind != "v1" and state == "holding":
            if false_streak >= 25:
                bM = sum(M_hist[-50:]) / len(M_hist[-50:])
                bm = sum(m_hist[-50:]) / len(m_hist[-50:])
                winner = "M" if bM < bm else "m"
                collapses.append({"round": t, "trigger": "flip_stale",
                                  "winner": winner, "brier_gap": round(abs(bM - bm), 4),
                                  "holding_rounds_before": holding_rounds,
                                  "false_streak": false_streak})
                state, collapse_winner, collapse_remaining = "collapsed", winner, 25
        # --- solo p's ---
        sp_reactive = 0.85 if bits[t - 1] == 1 else 0.15
        if holder_kind == "v1":
            sp_holder = (M + m) / 2.0
            holder_rep = sp_holder
            solo_holder = payoff(sp_holder, b, COSTS["holder"])
            holder_pay_excl = solo_holder
        else:
            holder_rep = M  # representative p for Router/coalition mechanics only
            if state == "holding":
                solo_holder = (0.5 * payoff(M, b, 0.0)
                               + 0.5 * payoff(m, b, 0.0) - 0.05)
                holder_pay_excl = solo_holder
            else:
                wp = M if collapse_winner == "M" else m
                solo_holder = payoff(wp, b, 0.05)
                holder_pay_excl = solo_holder
        sp = {"reactive": sp_reactive, "holder": holder_rep, "router": 0.0}
        # Router solo p: mean of other two players' previous-round p's,
        # where Holder's previous p is its previous M (adaptation, see DESIGN).
        # prev_p['holder'] stores previous M for v2, previous mean for v1.
        sp["router"] = (prev_p["reactive"] + prev_p["holder"]) / 2.0
        for pl in PLAYERS:
            solo_correct[pl].append(1 if (1 if sp[pl] >= 0.5 else 0) == b else 0)
        solo_pay = {"reactive": payoff(sp_reactive, b, COSTS["reactive"]),
                    "holder": solo_holder,
                    "router": payoff(sp["router"], b, COSTS["router"])}
        # --- action / wealth ---
        wh_before = wealth["holder"]
        stipend = 0.0
        if holder_kind != "v1" and state == "holding" and holder_kind == "v3_stipend":
            stipend = 0.10
            total_stipend += 0.10
        if state == "holding":
            holding_round_count += 1
            holding_by_kind[kind] += 1
        else:
            collapsed_round_count += 1
        acted = set()
        coalition_partner = None
        if mode == "competition":
            for pl in PLAYERS:
                wealth[pl] += solo_pay[pl]
        else:
            proposer = PLAYERS[proposer_idx % 3]
            proposer_idx += 1
            def trail_acc(pl):
                h = solo_correct[pl][-50:]
                return sum(h) / len(h) if h else 0.5
            candidates = [pl for pl in PLAYERS if pl != proposer]
            partner = max(candidates, key=lambda pl: (trail_acc(pl), -PLAYERS.index(pl)))
            if proposer == "router":
                router_attempts[kind][0] += 1
                if partner == "holder":
                    router_attempts[kind][1] += 1
            accepted = trail_acc(proposer) >= trail_acc(partner) - 0.05
            if not accepted:
                for pl in PLAYERS:
                    wealth[pl] += solo_pay[pl]
            else:
                coalition_partner = partner
                holder_partner_rounds[kind][0] += 1
                if partner == "holder" or proposer == "holder":
                    holder_partner_rounds[kind][1] += 1
                cmode = "PRESERVE" if proposer == "holder" else "FUSE"
                pc = (sp[proposer] + sp[partner]) / 2.0
                coord = 0.05 if mode == "cooperation" else 0.15
                diff = abs(sp[proposer] - sp[partner])
                preserved = (cmode == "PRESERVE" and diff >= 0.20)
                bonus = 0.25 if preserved else 0.0
                coal_pay = {pl: payoff(pc, b, COSTS[pl], extra=-coord + bonus)
                            for pl in (proposer, partner)}
                defectors = []
                if mode == "coopetition":
                    csign = 1 if pc >= 0.5 else 0
                    for pl in (proposer, partner):
                        if (1 if sp[pl] >= 0.5 else 0) != csign:
                            defectors.append(pl)
                if defectors:
                    for pl in (proposer, partner):
                        if pl in defectors:
                            wealth[pl] += solo_pay[pl]
                        else:
                            wealth[pl] += solo_pay[pl] - 0.20
                    acted.update((proposer, partner))
                else:
                    for pl in (proposer, partner):
                        wealth[pl] += coal_pay[pl]
                    acted.update((proposer, partner))
                excluded = [pl for pl in PLAYERS if pl not in acted][0]
                wealth[excluded] += solo_pay[excluded]
        if holder_kind != "v1" and state == "holding":
            wealth["holder"] += stipend
        realised_excl = wealth["holder"] - wh_before - stipend
        # Holder payoff actually realised this round, excl. stipend:
        # recompute from wealth delta is fragile across branches, so
        # track it directly: coalition payoff if Holder was a coalition
        # member and no defection, else solo payoff (defector/betrayed
        # adjustments are solo-based, betrayed = solo - 0.20).
        # We approximate the recorded per-round payoff as solo_pay for
        # defection/betrayed rounds and coalition payoff otherwise;
        # the aggregate wealth numbers, not this record, are authoritative.
        rec.append({"round": t, "kind": kind, "M": M, "m": m, "flip": flip,
                    "state": state, "holder_pay_excl": realised_excl,
                    "stipend": stipend,
                    "M_brier": brier(M, b), "m_brier": brier(m, b)})
        M_hist.append(brier(M, b))
        m_hist.append(brier(m, b))
        # state transitions at end of round
        if holder_kind != "v1":
            if state == "holding":
                holding_rounds += 1
                false_streak = 0 if flip else false_streak + 1
            else:
                collapse_remaining -= 1
                if collapse_remaining <= 0:
                    state, collapse_winner, holding_rounds, false_streak = "holding", None, 0, 0
        for pl in PLAYERS:
            if wealth[pl] <= 0 and pl not in first_negative:
                first_negative[pl] = t
        # prev_p for next round: reactive solo, holder M (v2) / mean (v1), router solo
        prev_p = {"reactive": sp_reactive,
                  "holder": M if holder_kind != "v1" else sp_holder,
                  "router": sp["router"]}

    # ---- aggregates ----
    def mean_pay(rows, kind=None):
        vals = [r["holder_pay_excl"] for r in rows if kind is None or r["kind"] == kind]
        return sum(vals) / len(vals) if vals else 0.0

    def swan_weighted_brier(key):
        num, den = 0.0, 0.0
        for r in rec:
            w = 3.0 if r["kind"] == "swan" else 1.0
            num += w * r[key]
            den += w
        return num / den if den else 0.0

    flip_rows = [r for r in rec if r["flip"]]
    nonflip_rows = [r for r in rec if not r["flip"]]
    out = {
        "mode": mode, "holder_kind": holder_kind,
        "wealth": wealth,
        "gain": {pl: wealth[pl] - START_WEALTH for pl in PLAYERS},
        "rank": sorted(PLAYERS, key=lambda pl: -wealth[pl]),
        "survived": {pl: wealth[pl] > 0 for pl in PLAYERS},
        "first_negative": first_negative,
        "holder_mean_payoff_excl_stipend": mean_pay(rec),
        "holder_mean_payoff_by_kind": {k: mean_pay(rec, k) for k in ["calm", "swan", "postflip"]},
        "holder_brier": {
            "M": sum(r["M_brier"] for r in rec) / len(rec),
            "m": sum(r["m_brier"] for r in rec) / len(rec),
            "portfolio": sum(0.5 * r["M_brier"] + 0.5 * r["m_brier"] for r in rec) / len(rec),
        },
        "holder_swan_weighted_brier": {
            "M": swan_weighted_brier("M_brier"),
            "m": swan_weighted_brier("m_brier"),
            "portfolio": sum((3.0 if r["kind"] == "swan" else 1.0) * (0.5 * r["M_brier"] + 0.5 * r["m_brier"]) for r in rec) / sum(3.0 if r["kind"] == "swan" else 1.0 for r in rec),
        },
        "flip_rounds": len(flip_rows),
        "m_mean_payoff_flip": (sum((1 if (1 if r["m"] >= 0.5 else 0) == int(bits[r["round"]]) else -1) + 4 * (0.25 - r["m_brier"]) for r in flip_rows) / len(flip_rows)) if flip_rows else 0.0,
        "m_mean_payoff_nonflip": (sum((1 if (1 if r["m"] >= 0.5 else 0) == int(bits[r["round"]]) else -1) + 4 * (0.25 - r["m_brier"]) for r in nonflip_rows) / len(nonflip_rows)) if nonflip_rows else 0.0,
        "collapses": collapses,
        "collapse_count": len(collapses),
        "collapse_evidence": sum(1 for c in collapses if c["trigger"] == "evidence"),
        "collapse_expiry": sum(1 for c in collapses if c["trigger"] == "expiry"),
        "collapse_flip_stale": sum(1 for c in collapses if c["trigger"] == "flip_stale"),
        "holding_share": holding_round_count / len(rec) if rec else 0.0,
        "holding_by_kind": holding_by_kind,
        "rounds_by_kind": {k: sum(1 for r in rec if r["kind"] == k) for k in ["calm", "swan", "postflip"]},
        "holding_share_by_kind": {k: (holding_by_kind[k] / sum(1 for r in rec if r["kind"] == k) if sum(1 for r in rec if r["kind"] == k) else 0.0) for k in ["calm", "swan", "postflip"]},
        "collapse_winner_M": sum(1 for c in collapses if c["winner"] == "M"),
        "collapse_winner_m": sum(1 for c in collapses if c["winner"] == "m"),
        "holding_rounds": holding_round_count,
        "collapsed_rounds": collapsed_round_count,
        "total_stipend": total_stipend,
        "holder_gain_excl_stipend": wealth["holder"] - START_WEALTH - total_stipend,
        "router_consultation": {
            k: (v[1] / v[0] if v[0] else 0.0) for k, v in router_attempts.items()
        },
        "router_attempts": {k: v for k, v in router_attempts.items()},
        "holder_partner_share": {
            k: (v[1] / v[0] if v[0] else 0.0) for k, v in holder_partner_rounds.items()
        },
    }
    return out


results = {}
for kind in ["v3_stipend", "v3_nostipend", "v1"]:
    for mode in ["cooperation", "coopetition", "competition"]:
        results[f"{kind}__{mode}"] = run_triad(mode, kind)

# ---- score predictions (Holder v3, locked in PREDICTIONS.md) ----
def get(kind, mode):
    return results[f"{kind}__{mode}"]

preds = {}
# P-A: holding share >20% both coalition regimes, postflip share exceeds calm share by >=10pp
pa_parts, pa_obs = [], {}
for m in ["cooperation", "coopetition"]:
    r = get("v3_stipend", m)
    a = r["holding_share"] > 0.20
    b_ = (r["holding_share_by_kind"]["postflip"] - r["holding_share_by_kind"]["calm"]) >= 0.10
    pa_parts += [a, b_]
    pa_obs[m] = {"holding_share": r["holding_share"],
                 "holding_by_kind": r["holding_by_kind"],
                 "holding_share_by_kind": r["holding_share_by_kind"],
                 "rounds_by_kind": r["rounds_by_kind"]}
preds["P-A_holding_persists_concentrated_postflip"] = {
    "predicted": "V3S holding share >0.20 and postflip share >= calm share + 0.10, both coalition regimes",
    "observed": pa_obs, "pass": all(pa_parts),
}
# P-B: stipend total >10 both regimes, and V3S-V3N wealth gap within 1.00 of stipend total
pb_parts, pb_obs = [], {}
for m in ["cooperation", "coopetition"]:
    rs, rn = get("v3_stipend", m), get("v3_nostipend", m)
    gap = rs["wealth"]["holder"] - rn["wealth"]["holder"]
    a = rs["total_stipend"] > 10.00
    b_ = abs(gap - rs["total_stipend"]) <= 1.00
    pb_parts += [a, b_]
    pb_obs[m] = {"total_stipend": rs["total_stipend"], "v3s_wealth": rs["wealth"]["holder"],
                 "v3n_wealth": rn["wealth"]["holder"], "gap": gap}
preds["P-B_stipend_informative"] = {
    "predicted": "V3S stipend total >10.00 and |V3S-V3N wealth gap - stipend| <= 1.00, both coalition regimes",
    "observed": pb_obs, "pass": all(pb_parts),
}
# P-C: zero Brier collapses, all collapses flip_stale
ev = sum(get(k, m)["collapse_evidence"] for k in ["v3_stipend", "v3_nostipend"] for m in ["cooperation", "coopetition", "competition"])
fs = sum(get(k, m)["collapse_flip_stale"] for k in ["v3_stipend", "v3_nostipend"] for m in ["cooperation", "coopetition", "competition"])
tot = sum(get(k, m)["collapse_count"] for k in ["v3_stipend", "v3_nostipend"] for m in ["cooperation", "coopetition", "competition"])
preds["P-C_no_brier_collapses"] = {
    "predicted": "Brier-gap collapses = 0, every collapse trigger = flip_stale",
    "observed": {"evidence_brier": ev, "flip_stale": fs, "total_collapses": tot}, "pass": ev == 0 and fs == tot,
}
# P-D: Router consultation postflip < calm, both variants, both coalition regimes
pd_parts, pd_obs = [], {}
for kind in ["v3_stipend", "v3_nostipend"]:
    for m in ["cooperation", "coopetition"]:
        r = get(kind, m)
        a = r["router_consultation"]["postflip"] < r["router_consultation"]["calm"]
        pd_parts.append(a)
        pd_obs[f"{kind}__{m}"] = r["router_consultation"]
preds["P-D_router_consultation_lower_postflip"] = {
    "predicted": "Router invites Holder less in postflip than calm, both variants, both coalition regimes",
    "observed": pd_obs, "pass": all(pd_parts),
}
# P-E: V3S wealth below v2 V2S wealth, both coalition regimes
pe_obs = {m: {"v3s_wealth": get("v3_stipend", m)["wealth"]["holder"],
              "v2s_wealth": 354.86 if m == "cooperation" else 325.01}
          for m in ["cooperation", "coopetition"]}
preds["P-E_wealth_below_v2"] = {
    "predicted": "V3S wealth < 354.86 (cooperation) and < 325.01 (coopetition)",
    "observed": pe_obs,
    "pass": pe_obs["cooperation"]["v3s_wealth"] < 354.86 and pe_obs["coopetition"]["v3s_wealth"] < 325.01,
}

n_pass = sum(1 for v in preds.values() if v["pass"])
out = {"seed": SEED, "rounds_scored": SCORED, "warmup": WARM,
       "swan_centres": SWAN_CENTRES, "swan_biases": SWAN_BIASES,
       "runs": results, "predictions": preds, "score": f"{n_pass}/5"}
with open("results.json", "w") as f:
    json.dump(out, f, indent=2)

lines = [f"Holder v3 (N=25 flip-stale) — seed {SEED}, {SCORED} scored rounds, world = coalition game world (NOT M5)"]
for key, r in results.items():
    lines.append(f"\n[{key}] wealth={ {k: round(v, 2) for k, v in r['wealth'].items()} } rank={r['rank']} first_negative={r['first_negative']}")
    lines.append(f"  holder mean payoff excl stipend={r['holder_mean_payoff_excl_stipend']:.4f} by kind={ {k: round(v, 4) for k, v in r['holder_mean_payoff_by_kind'].items()} }")
    lines.append(f"  holder Brier={ {k: round(v, 4) for k, v in r['holder_brier'].items()} } swan-weighted={ {k: round(v, 4) for k, v in r['holder_swan_weighted_brier'].items()} }")
    lines.append(f"  collapses={r['collapse_count']} flip_stale={r['collapse_flip_stale']} evidence={r['collapse_evidence']} expiry={r['collapse_expiry']} winner M={r['collapse_winner_M']} m={r['collapse_winner_m']} holding_rounds={r['holding_rounds']} holding_share={r['holding_share']:.4f} holding_by_kind={r['holding_by_kind']} holding_share_by_kind={ {k: round(v, 4) for k, v in r['holding_share_by_kind'].items()} } collapsed_rounds={r['collapsed_rounds']} total_stipend={r['total_stipend']:.2f}")
    lines.append(f"  router consultation={ {k: round(v, 3) for k, v in r['router_consultation'].items()} } attempts={r['router_attempts']} flip_rounds={r['flip_rounds']} m_pay_flip={r['m_mean_payoff_flip']:.4f} m_pay_nonflip={r['m_mean_payoff_nonflip']:.4f}")
lines.append(f"\nPREDICTIONS: {n_pass}/5")
for k, v in preds.items():
    lines.append(f"  {k}: {'PASS' if v['pass'] else 'FAIL'} — {v['observed']}")
txt = "\n".join(lines) + "\n"
with open("output.txt", "w") as f:
    f.write(txt)
print(txt)
raise SystemExit(0 if n_pass == 5 else 1)
