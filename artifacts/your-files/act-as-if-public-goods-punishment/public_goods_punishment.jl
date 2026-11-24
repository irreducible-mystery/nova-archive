#!/usr/bin/env julia
#
# public_goods_punishment.jl — 3-player public goods with punishment.
#
# The competition corner of the four-regime map: fixed strategies,
# no learning, no randomness. One round, in order:
#   1. Cooperator contributes 20, Defector contributes 0, Punisher
#      contributes 20. Pot = sum * 1.5, split equally among 3 players.
#   2. Punisher punishes each under-contributor (here: Defector) once,
#      paying c and removing 3c from the target.
# With fixed strategies every round is identical, so 100-round totals
# are exactly 100x the per-round payoffs. Pre-registered predictions
# (PREDICTIONS.md) are checked at the end; exit code 0 iff all hold,
# 1 otherwise (house convention: failures are findings, not errors).
#
# Usage: julia public_goods_punishment.jl [--rounds N] [--seed S]
#   --seed is accepted for house-style compatibility but unused:
#   there is nothing random in this design.

using Printf

function parse_args(args)
    rounds = 100
    seed = 20261030
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
    # Contributions: Cooperator 20, Defector 0, Punisher 20.
    pot = (20 + 0 + 20) * 1.5
    share = pot / 3  # 20.0
    coop = 20 - 20 + share
    def = 20 - 0 + share - 3c
    pun = 20 - 20 + share - c
    total = coop + def + pun
    return (coop=coop, def=def, pun=pun, total=total,
            coop_t=coop * rounds, def_t=def * rounds,
            pun_t=pun * rounds, total_t=total * rounds)
end

function main()
    rounds, seed = parse_args(ARGS)
    println("public goods with punishment: endowment 20, multiplier 1.5, ratio 1:3")
    println("rounds=$rounds seed=$seed (seed unused: design is deterministic)")
    results = Dict{String,Any}()
    for c in (0, 4, 8)
        r = run_game(c, rounds)
        results["c=$c"] = r
        @printf("c=%d  per-round: Cooperator %.1f  Defector %.1f  Punisher %.1f  total %.1f\n",
                c, r.coop, r.def, r.pun, r.total)
        @printf("c=%d  %d-round: Cooperator %.1f  Defector %.1f  Punisher %.1f  total %.1f\n",
                c, rounds, r.coop_t, r.def_t, r.pun_t, r.total_t)
    end
    # Score the pre-registered predictions (per-round values).
    c0, c4, c8 = results["c=0"], results["c=4"], results["c=8"]
    p1 = c0.def == 40 && c0.coop == 20 && c0.pun == 20 && c0.total == 80
    p2 = c4.def == 28 && c4.coop == 20 && c4.pun == 16 && c4.total == 64
    p3 = c8.coop == 20 && c8.def == 16 && c8.pun == 12
    p4 = c0.total > c4.total > c8.total && c0.total == 80 && c4.total == 64 && c8.total == 48
    p5 = c4.def > c4.coop && c8.def < c8.coop  # crossing between c=4 and c=8
    preds = [("P1", p1), ("P2", p2), ("P3", p3), ("P4", p4), ("P5", p5)]
    npass = 0
    for (name, ok) in preds
        println(name, " ", ok ? "PASS" : "FAIL")
        npass += ok ? 1 : 0
    end
    println("score: $npass/5")
    # Machine-readable summary for the README/results file.
    open("results.json", "w") do io
        write(io, "{\n")
        for c in (0, 4, 8)
            r = results["c=$c"]
            write(io, "  \"c=$c\": {\"coop_per_round\": $(r.coop), \"def_per_round\": $(r.def), " *
                      "\"pun_per_round\": $(r.pun), \"total_per_round\": $(r.total), " *
                      "\"coop_total\": $(r.coop_t), \"def_total\": $(r.def_t), " *
                      "\"pun_total\": $(r.pun_t), \"total_total\": $(r.total_t)},\n")
        end
        write(io, "  \"rounds\": $rounds, \"score\": \"$npass/5\", \"predictions\": {")
        write(io, join(["\"$n\": $(ok ? "true" : "false")" for (n, ok) in preds], ", "))
        write(io, "}\n}\n")
    end
    exit(npass == 5 ? 0 : 1)
end

main()
