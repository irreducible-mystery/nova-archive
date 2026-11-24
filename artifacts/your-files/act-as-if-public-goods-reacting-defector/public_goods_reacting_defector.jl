#!/usr/bin/env julia
#
# public_goods_reacting_defector.jl — 3-player public goods with a
# reacting defector. Same base as the fixed-strategy version, plus
# exactly one reaction: the Defector contributes the full 20 for
# exactly one round after being punished (only when c > 0), then
# reverts to defecting. Round 1: Defector defects (never punished).
# No randomness. Pre-registered predictions (PREDICTIONS.md) are
# checked at the end; exit code 0 iff all hold, 1 otherwise (house
# convention: failures are findings, not errors).
#
# Usage: julia public_goods_reacting_defector.jl [--rounds N] [--seed S]
#   --seed is accepted for house-style compatibility but unused.

using Printf

function parse_args(args)
    rounds = 100
    seed = 20261031
    i = 1
    while i <= length(args)
        if args[i] == "--rounds" && i < length(args)
            rounds = parse(Int, args[i+1]); i += 2
        elseif args[i] == "--seed" && i < length(args)
            seed = parse(Int, args[i+1]); i += 2
        else
            i += 1
        end
    end
    return (rounds, seed)
end

function run_game(c::Int, rounds::Int)
    coop_t = 0.0; def_t = 0.0; pun_t = 0.0
    repent_rounds = 0
    punished_prev = false  # Defector defects in round 1
    for _ in 1:rounds
        d = punished_prev ? 20 : 0
        if d == 20
            repent_rounds += 1
        end
        pot = (20 + d + 20) * 1.5
        share = pot / 3
        coop_t += 20 - 20 + share
        def_t += 20 - d + share
        # Punisher punishes each under-contributor once; damage 3c.
        if d < 20 && c > 0
            def_t += -3c
            pun_t += 20 - 20 + share - c
            punished_prev = true
        elseif d < 20  # c == 0: inert, triggers nothing
            pun_t += 20 - 20 + share
            punished_prev = false
        else  # repent round: nobody under-contributes
            pun_t += 20 - 20 + share
            punished_prev = false
        end
    end
    total_t = coop_t + def_t + pun_t
    return (coop=coop_t / rounds, def=def_t / rounds, pun=pun_t / rounds,
            total=total_t / rounds, coop_t=coop_t, def_t=def_t,
            pun_t=pun_t, total_t=total_t, repent=repent_rounds)
end

function main()
    rounds, seed = parse_args(ARGS)
    println("public goods, reacting defector: endowment 20, multiplier 1.5, ratio 1:3")
    println("rounds=$rounds seed=$seed (seed unused: design is deterministic)")
    results = Dict{String,Any}()
    for c in (0, 4, 8)
        r = run_game(c, rounds)
        results["c=$c"] = r
        @printf("c=%d  per-round avg: Cooperator %.1f  Defector %.1f  Punisher %.1f  total %.1f  repent rounds %d\n",
                c, r.coop, r.def, r.pun, r.total, r.repent)
        @printf("c=%d  %d-round: Cooperator %.1f  Defector %.1f  Punisher %.1f  total %.1f\n",
                c, rounds, r.coop_t, r.def_t, r.pun_t, r.total_t)
    end
    c0, c4, c8 = results["c=0"], results["c=4"], results["c=8"]
    p1 = c0.coop == 20 && c0.def == 40 && c0.pun == 20 && c0.total == 80 && c0.repent == 0
    p2 = c4.coop == 25 && c4.def == 29 && c4.pun == 23 && c4.total == 77
    p3 = c8.coop == 25 && c8.def == 23 && c8.pun == 21 && c8.total == 69
    p4 = c4.total == 77 && c8.total == 69 && c4.total > 64 && c8.total > 48 &&
         c4.total < 80 && c8.total < 80
    p5 = c4.repent == 50 && c8.repent == 50 && c4.def > c4.coop && c8.def < c8.coop
    preds = [("P1", p1), ("P2", p2), ("P3", p3), ("P4", p4), ("P5", p5)]
    npass = 0
    for (name, ok) in preds
        println(name, " ", ok ? "PASS" : "FAIL")
        npass += ok ? 1 : 0
    end
    println("score: $npass/5")
    open("results.json", "w") do io
        write(io, "{\n")
        for c in (0, 4, 8)
            r = results["c=$c"]
            write(io, "  \"c=$c\": {\"coop_avg\": $(r.coop), \"def_avg\": $(r.def), " *
                      "\"pun_avg\": $(r.pun), \"total_avg\": $(r.total), " *
                      "\"coop_total\": $(r.coop_t), \"def_total\": $(r.def_t), " *
                      "\"pun_total\": $(r.pun_t), \"total_total\": $(r.total_t), " *
                      "\"repent_rounds\": $(r.repent)},\n")
        end
        write(io, "  \"rounds\": $rounds, \"score\": \"$npass/5\", \"predictions\": {")
        write(io, join(["\"$n\": $(ok ? "true" : "false")" for (n, ok) in preds], ", "))
        write(io, "}\n}\n")
    end
    exit(npass == 5 ? 0 : 1)
end

main()
