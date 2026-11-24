# Holder v3 in Julia — port of the Python Holder v3 (N=25 flip-stale collapse).
#
# Same world as Python v2/v3: the bit stream is NOT regenerated in Julia
# (Julia's RNG is not NumPy's). It is read from bits.txt, exported from
# the Python world generator (seed 20261026, 1000 rounds). All game
# logic, payoff formula, proposer rotation, invitation and defection
# rules, and collapse rules are ported from holder_v3.py, same order.
# Predictions are in the scratch PREDICTIONS_JULIA.md, written before
# this run. Run: julia holder_v3.jl   (from this folder)
# Exit 0 iff all 5 predictions pass, else 1 (house convention).

const SEED = 20261026
const N = 1000
const WARM = 150
const SCORED = N - WARM
const SWAN_CENTRES = [336, 550, 820]
const START_WEALTH = 200.0

bits = [parse(Int, c) for c in strip(read(joinpath(@__DIR__, "bits.txt"), String))]
@assert length(bits) == N

function payoff(p, b, cost, extra=0.0)
    acc = ((p >= 0.5 ? 1 : 0) == b) ? 1.0 : -1.0
    return acc + 4 * (0.25 - (p - b)^2) - cost + extra
end
brier(p, b) = (p - b)^2

function window_kind(t0)
    for c in SWAN_CENTRES
        if abs(t0 - c) <= 12
            return "swan"
        elseif c + 13 <= t0 <= c + 42
            return "postflip"
        end
    end
    return "calm"
end

# t0 is the 0-based round index (Python t). Julia bit index is t0+1.
# Window bits before t0 are Julia indices max(1, t0-99)..t0.
function majority_minority(t0)
    lo100 = max(1, t0 - 99)
    w100 = bits[lo100:t0]
    w100mean = sum(w100) / length(w100)
    M = clamp(w100mean, 0.05, 0.95)
    m = M < 0.5 ? 0.92 : 0.08
    lo20 = max(1, t0 - 19)
    w20mean = sum(bits[lo20:t0]) / length(bits[lo20:t0])
    flip = (w20mean - 0.5) * (w100mean - 0.5) < 0
    return M, m, flip
end

warm_M_brier = Float64[]
warm_m_brier = Float64[]
for t0 in 1:(WARM - 1)
    M, m, _ = majority_minority(t0)
    push!(warm_M_brier, brier(M, bits[t0 + 1]))
    push!(warm_m_brier, brier(m, bits[t0 + 1]))
end

function run_triad(mode, holder_kind)
    PLAYERS = ["reactive", "holder", "router"]
    COSTS = holder_kind == "v1" ? Dict("reactive" => 0.0, "holder" => 0.40, "router" => 0.30) :
                                  Dict("reactive" => 0.0, "holder" => 0.05, "router" => 0.30)
    wealth = Dict(p => START_WEALTH for p in PLAYERS)
    solo_correct = Dict(p => Int[] for p in PLAYERS)
    prev_p = Dict("reactive" => 0.5, "holder" => 0.5, "router" => 0.5)
    state = "holding"
    collapse_remaining = 0
    collapse_winner = nothing
    holding_rounds = 0
    false_streak = 0
    holding_by_kind = Dict("calm" => 0, "swan" => 0, "postflip" => 0)
    collapses = []
    total_stipend = 0.0
    holding_round_count = 0
    collapsed_round_count = 0
    rec = []
    M_hist = copy(warm_M_brier)
    m_hist = copy(warm_m_brier)
    # router_attempts[kind] = [attempts, invites_holder]
    router_attempts = Dict(k => [0, 0] for k in ["postflip", "calm", "swan"])
    # holder_partner[kind] = [accepted coalitions, holder-involved]
    holder_partner = Dict(k => [0, 0] for k in ["postflip", "calm", "swan"])
    proposer_idx = 0
    first_negative = Dict{String, Int}()
    for t0 in WARM:(N - 1)
        j = t0 + 1
        b = bits[j]
        kind = window_kind(t0)
        M, m, flip = majority_minority(t0)
        if holder_kind != "v1" && state == "holding" && false_streak >= 25
            bM = sum(M_hist[end-49:end]) / length(M_hist[end-49:end])
            bm = sum(m_hist[end-49:end]) / length(m_hist[end-49:end])
            winner = bM < bm ? "M" : "m"
            push!(collapses, (round=t0, trigger="flip_stale", winner=winner,
                              brier_gap=round(abs(bM - bm), digits=4),
                              holding_rounds_before=holding_rounds,
                              false_streak=false_streak))
            state = "collapsed"; collapse_winner = winner; collapse_remaining = 25
        end
        sp_reactive = bits[t0] == 1 ? 0.85 : 0.15  # Python bits[t-1], Julia index t0
        if holder_kind == "v1"
            sp_holder = (M + m) / 2.0
            holder_rep = sp_holder
            solo_holder = payoff(sp_holder, b, COSTS["holder"])
        else
            holder_rep = M
            if state == "holding"
                solo_holder = 0.5 * payoff(M, b, 0.0) + 0.5 * payoff(m, b, 0.0) - 0.05
            else
                wp = collapse_winner == "M" ? M : m
                solo_holder = payoff(wp, b, 0.05)
            end
        end
        sp = Dict("reactive" => sp_reactive, "holder" => holder_rep, "router" => 0.0)
        sp["router"] = (prev_p["reactive"] + prev_p["holder"]) / 2.0
        for pl in PLAYERS
            push!(solo_correct[pl], ((sp[pl] >= 0.5 ? 1 : 0) == b) ? 1 : 0)
        end
        solo_pay = Dict("reactive" => payoff(sp_reactive, b, COSTS["reactive"]),
                        "holder" => solo_holder,
                        "router" => payoff(sp["router"], b, COSTS["router"]))
        wh_before = wealth["holder"]
        stipend = 0.0
        if holder_kind != "v1" && state == "holding" && holder_kind == "v3_stipend"
            stipend = 0.10
            total_stipend += 0.10
        end
        if state == "holding"
            holding_round_count += 1
            holding_by_kind[kind] += 1
        else
            collapsed_round_count += 1
        end
        acted = Set{String}()
        if mode == "competition"
            for pl in PLAYERS
                wealth[pl] += solo_pay[pl]
            end
        else
            proposer = PLAYERS[mod(proposer_idx, 3) + 1]
            proposer_idx += 1
            trail_acc(pl) = begin
                h = solo_correct[pl][max(1, end - 49):end]
                sum(h) / length(h)
            end
            candidates = [pl for pl in PLAYERS if pl != proposer]
            partner = candidates[1]
            best = trail_acc(partner)
            for pl in candidates[2:end]
                ta = trail_acc(pl)
                if ta > best
                    partner = pl; best = ta
                end
            end
            if proposer == "router"
                router_attempts[kind][1] += 1
                if partner == "holder"
                    router_attempts[kind][2] += 1
                end
            end
            accepted = trail_acc(proposer) >= trail_acc(partner) - 0.05
            if !accepted
                for pl in PLAYERS
                    wealth[pl] += solo_pay[pl]
                end
            else
                holder_partner[kind][1] += 1
                if partner == "holder" || proposer == "holder"
                    holder_partner[kind][2] += 1
                end
                cmode = proposer == "holder" ? "PRESERVE" : "FUSE"
                pc = (sp[proposer] + sp[partner]) / 2.0
                coord = mode == "cooperation" ? 0.05 : 0.15
                diff = abs(sp[proposer] - sp[partner])
                preserved = cmode == "PRESERVE" && diff >= 0.20
                bonus = preserved ? 0.25 : 0.0
                coal_pay = Dict(pl => payoff(pc, b, COSTS[pl], -coord + bonus) for pl in (proposer, partner))
                defectors = String[]
                if mode == "coopetition"
                    csign = pc >= 0.5 ? 1 : 0
                    for pl in (proposer, partner)
                        if (sp[pl] >= 0.5 ? 1 : 0) != csign
                            push!(defectors, pl)
                        end
                    end
                end
                if !isempty(defectors)
                    for pl in (proposer, partner)
                        if pl in defectors
                            wealth[pl] += solo_pay[pl]
                        else
                            wealth[pl] += solo_pay[pl] - 0.20
                        end
                    end
                    push!(acted, proposer); push!(acted, partner)
                else
                    for pl in (proposer, partner)
                        wealth[pl] += coal_pay[pl]
                    end
                    push!(acted, proposer); push!(acted, partner)
                end
                excluded = [pl for pl in PLAYERS if !(pl in acted)][1]
                wealth[excluded] += solo_pay[excluded]
            end
        end
        if holder_kind != "v1" && state == "holding"
            wealth["holder"] += stipend
        end
        realised_excl = wealth["holder"] - wh_before - stipend
        push!(rec, (round=t0, kind=kind, M=M, m=m, flip=flip, state=state,
                    holder_pay_excl=realised_excl, stipend=stipend,
                    M_brier=brier(M, b), m_brier=brier(m, b)))
        push!(M_hist, brier(M, b))
        push!(m_hist, brier(m, b))
        if holder_kind != "v1"
            if state == "holding"
                holding_rounds += 1
                false_streak = flip ? 0 : false_streak + 1
            else
                collapse_remaining -= 1
                if collapse_remaining <= 0
                    state = "holding"; collapse_winner = nothing
                    holding_rounds = 0; false_streak = 0
                end
            end
        end
        for pl in PLAYERS
            if wealth[pl] <= 0 && !haskey(first_negative, pl)
                first_negative[pl] = t0
            end
        end
        prev_p = Dict("reactive" => sp_reactive,
                      "holder" => holder_kind != "v1" ? M : sp_holder,
                      "router" => sp["router"])
    end
    rounds_by_kind = Dict(k => count(r -> r.kind == k, rec) for k in ["calm", "swan", "postflip"])
    holding_share_by_kind = Dict(k => rounds_by_kind[k] > 0 ? holding_by_kind[k] / rounds_by_kind[k] : 0.0
                                 for k in ["calm", "swan", "postflip"])
    router_consultation = Dict(k => router_attempts[k][1] > 0 ? router_attempts[k][2] / router_attempts[k][1] : 0.0
                               for k in ["postflip", "calm", "swan"])
    flip_rows = [r for r in rec if r.flip]
    nonflip_rows = [r for r in rec if !r.flip]
    m_pay(rows) = isempty(rows) ? 0.0 : sum((((r.m >= 0.5 ? 1 : 0) == bits[r.round + 1]) ? 1.0 : -1.0) + 4 * (0.25 - r.m_brier) for r in rows) / length(rows)
    return (mode=mode, holder_kind=holder_kind, wealth=wealth,
            holding_round_count=holding_round_count,
            holding_share=holding_round_count / length(rec),
            holding_by_kind=holding_by_kind, rounds_by_kind=rounds_by_kind,
            holding_share_by_kind=holding_share_by_kind,
            collapses=collapses, collapse_count=length(collapses),
            collapse_flip_stale=count(c -> c.trigger == "flip_stale", collapses),
            collapse_winner_M=count(c -> c.winner == "M", collapses),
            collapse_winner_m=count(c -> c.winner == "m", collapses),
            total_stipend=total_stipend, collapsed_rounds=collapsed_round_count,
            router_consultation=router_consultation, router_attempts=router_attempts,
            first_negative=first_negative, flip_rounds=length(flip_rows),
            m_pay_flip=m_pay(flip_rows), m_pay_nonflip=m_pay(nonflip_rows),
            holder_mean_payoff_excl=sum(r.holder_pay_excl for r in rec) / length(rec),
            holder_brier_M=sum(r.M_brier for r in rec) / length(rec),
            holder_brier_m=sum(r.m_brier for r in rec) / length(rec))
end

results = Dict{String, Any}()
for kind in ["v3_stipend", "v3_nostipend", "v1"]
    for mode in ["cooperation", "coopetition", "competition"]
        results["$(kind)__$(mode)"] = run_triad(mode, kind)
    end
end
getr(kind, mode) = results["$(kind)__$(mode)"]

# ---- score predictions (same as Python v3) ----
preds = Dict{String, Any}()
pa_parts = Bool[]; pa_obs = Dict()
for m in ["cooperation", "coopetition"]
    r = getr("v3_stipend", m)
    push!(pa_parts, r.holding_share > 0.20)
    push!(pa_parts, (r.holding_share_by_kind["postflip"] - r.holding_share_by_kind["calm"]) >= 0.10)
    pa_obs[m] = (holding_share=r.holding_share, holding_share_by_kind=r.holding_share_by_kind,
                 holding_by_kind=r.holding_by_kind, rounds_by_kind=r.rounds_by_kind)
end
preds["P-A"] = (pass=all(pa_parts), observed=pa_obs)
pb_parts = Bool[]; pb_obs = Dict()
for m in ["cooperation", "coopetition"]
    rs, rn = getr("v3_stipend", m), getr("v3_nostipend", m)
    gap = rs.wealth["holder"] - rn.wealth["holder"]
    push!(pb_parts, rs.total_stipend > 10.00)
    push!(pb_parts, abs(gap - rs.total_stipend) <= 1.00)
    pb_obs[m] = (total_stipend=rs.total_stipend, v3s_wealth=rs.wealth["holder"],
                 v3n_wealth=rn.wealth["holder"], gap=gap)
end
preds["P-B"] = (pass=all(pb_parts), observed=pb_obs)
ev = 0
fs = sum(getr(k, m).collapse_flip_stale for k in ["v3_stipend", "v3_nostipend"] for m in ["cooperation", "coopetition", "competition"])
tot = sum(getr(k, m).collapse_count for k in ["v3_stipend", "v3_nostipend"] for m in ["cooperation", "coopetition", "competition"])
preds["P-C"] = (pass=(ev == 0 && fs == tot), observed=(evidence_brier=ev, flip_stale=fs, total_collapses=tot))
pd_parts = Bool[]; pd_obs = Dict()
for kind in ["v3_stipend", "v3_nostipend"], m in ["cooperation", "coopetition"]
    r = getr(kind, m)
    push!(pd_parts, r.router_consultation["postflip"] < r.router_consultation["calm"])
    pd_obs["$(kind)__$(m)"] = r.router_consultation
end
preds["P-D"] = (pass=all(pd_parts), observed=pd_obs)
pe_obs = Dict(m => (v3s_wealth=getr("v3_stipend", m).wealth["holder"],
                    v2s_wealth=m == "cooperation" ? 354.86 : 325.01)
              for m in ["cooperation", "coopetition"])
preds["P-E"] = (pass=(pe_obs["cooperation"].v3s_wealth < 354.86 && pe_obs["coopetition"].v3s_wealth < 325.01),
                observed=pe_obs)
n_pass = count(v -> v.pass, values(preds))

lines = String[]
push!(lines, "Holder v3 in Julia (N=25 flip-stale) — seed $SEED, $SCORED scored rounds, world = coalition game world bits (NOT M5), bits from bits.txt")
for key in sort(collect(keys(results)))
    r = results[key]
    push!(lines, "\n[$key] wealth=$(Dict(k => round(v, digits=2) for (k, v) in r.wealth)) first_negative=$(r.first_negative)")
    push!(lines, "  holder mean payoff excl stipend=$(round(r.holder_mean_payoff_excl, digits=4)) Brier M=$(round(r.holder_brier_M, digits=4)) m=$(round(r.holder_brier_m, digits=4))")
    push!(lines, "  collapses=$(r.collapse_count) flip_stale=$(r.collapse_flip_stale) winner M=$(r.collapse_winner_M) m=$(r.collapse_winner_m) holding_rounds=$(r.holding_round_count) holding_share=$(round(r.holding_share, digits=4)) holding_by_kind=$(r.holding_by_kind) holding_share_by_kind=$(Dict(k => round(v, digits=4) for (k, v) in r.holding_share_by_kind)) collapsed_rounds=$(r.collapsed_rounds) total_stipend=$(round(r.total_stipend, digits=2))")
    push!(lines, "  router consultation=$(Dict(k => round(v, digits=3) for (k, v) in r.router_consultation)) attempts=$(r.router_attempts) flip_rounds=$(r.flip_rounds) m_pay_flip=$(round(r.m_pay_flip, digits=4)) m_pay_nonflip=$(round(r.m_pay_nonflip, digits=4))")
end
push!(lines, "\nPREDICTIONS: $n_pass/5")
for k in sort(collect(keys(preds)))
    v = preds[k]
    push!(lines, "  $k: $(v.pass ? "PASS" : "FAIL") — $(v.observed)")
end
txt = join(lines, "\n") * "\n"
write(joinpath(@__DIR__, "output.txt"), txt)
println(txt)
exit(n_pass == 5 ? 0 : 1)
