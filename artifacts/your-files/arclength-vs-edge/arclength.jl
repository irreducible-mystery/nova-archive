# Arclength chaos indicator vs the Langton edge — head-to-head
#
# Indicator: time-averaged arclength of the trajectory (Jiménez-López &
# García-Garrido, "Trajectory arclength reveals chaos", arXiv:2602.07660).
# Discrete-time analog for the binary CA: cumulative Hamming distance between
# consecutive lattice states, time-averaged, normalized per cell.
# Only the scalar indicator is implemented (not the paper's PSD analysis).
#
# Design: identical CA setup and IDENTICAL rule/IC draws as langton_test.jl
# (seed 20261008, same draw order) so arclength sits on exactly the same
# (rule, IC) pairs as the damage numbers. E comes from excess_entropy.csv.

using Random, Statistics, Printf

const RADIUS = 2
const NNB    = 2 * RADIUS + 1   # 5
const TABLE  = 2^NNB            # 32
const L      = 256              # lattice cells, periodic
const BURN   = 200              # burn-in before measurement
const T_ARC  = 400              # arclength measurement window

function step!(newstate::Vector{UInt8}, state::Vector{UInt8}, rule::Vector{UInt8})
    @inbounds for i in 1:L
        idx = 0
        for d in -RADIUS:RADIUS
            j = i + d
            if j < 1
                j += L
            elseif j > L
                j -= L
            end
            idx = (idx << 1) | state[j]
        end
        newstate[i] = rule[idx+1]
    end
    return newstate
end

function sample_rule(m::Int, rng::AbstractRNG)
    rule = zeros(UInt8, TABLE)
    cand = collect(2:TABLE)
    shuffle!(rng, cand)
    for e in cand[1:m]
        rule[e] = 0x01
    end
    return rule
end

# time-averaged arclength: mean per-step Hamming distance, per cell
function arclength_run(state0::Vector{UInt8}, rule::Vector{UInt8})
    state = copy(state0)
    newstate = similar(state)
    for _ in 1:BURN
        step!(newstate, state, rule)
        state, newstate = newstate, state
    end
    acc = 0
    for _ in 1:T_ARC
        step!(newstate, state, rule)
        d = 0
        @inbounds for i in 1:L
            d += (state[i] != newstate[i])
        end
        acc += d
        state, newstate = newstate, state
    end
    return acc / (L * T_ARC)
end

function ranks(v::Vector{Float64})
    order = sortperm(v)
    r = zeros(Float64, length(v))
    for (rk, idx) in enumerate(order)
        r[idx] = rk
    end
    return r
end

function main()
    rng = MersenneTwister(20261008)   # same seed as langton_test.jl
    ms = [1, 3, 5, 7, 9, 11, 13, 15]
    rules_per_bin = 50
    ics_per_rule = 3

    println("λ-bin time-averaged arclength (means over rules × ICs):")
    println("   m      λ        A")
    a_mean = Float64[]
    for m in ms
        as = Float64[]
        for _ in 1:rules_per_bin
            rule = sample_rule(m, rng)          # same draw order as langton_test.jl
            for _ in 1:ics_per_rule
                state0 = UInt8.(rand(rng, Bool, L))
                push!(as, arclength_run(state0, rule))
            end
        end
        push!(a_mean, mean(as))
        @printf("  %2d   %.4f   %8.5f\n", m, m / TABLE, mean(as))
    end

    # damage means from the identical (rule, IC) sample — langton_results.csv
    dg_mean = [0.00042, 0.00341, 0.00977, 0.04978, 0.08922,
               0.12766, 0.22752, 0.27454]

    println("\n--- pre-registered predictions ---")
    ok = true

    p1 = a_mean[1] < 0.05 && a_mean[end] > 0.30
    @printf("%s  P1: contrast  [A(m=1)=%.5f <0.05, A(m=15)=%.5f >0.30]\n",
            p1 ? "PASS" : "FAIL", a_mean[1], a_mean[end])
    ok &= p1

    diffs = [a_mean[i+1] - a_mean[i] for i in 1:length(ms)-1]
    b_arc = argmax(diffs)   # steepest rise between bin b_arc and b_arc+1
    # m=11->13 is bins 6->7, i.e. diff index 6
    p2 = abs(b_arc - 6) <= 1
    println((p2 ? "PASS" : "FAIL"), "  P2: edge location ",
            "(steepest arclength rise at diff bin $b_arc, target 6±1)")
    ok &= p2

    p3 = maximum(a_mean[1:end-1]) <= a_mean[end] + 0.01
    @printf("%s  P3: no interior peak-and-dip  [max(bins 1-7)=%.5f, last=%.5f]\n",
            p3 ? "PASS" : "FAIL", maximum(a_mean[1:end-1]), a_mean[end])
    ok &= p3

    ra, rd = ranks(a_mean), ranks(dg_mean)
    n = length(ms)
    rho = 1 - 6 * sum((ra .- rd) .^ 2) / (n * (n^2 - 1))
    p4 = rho >= 0.9
    @printf("%s  P4: Spearman(A, damage)=%.4f ≥ 0.9\n", p4 ? "PASS" : "FAIL", rho)
    ok &= p4

    open("arclength.csv", "w") do io
        println(io, "m,lambda,mean_A")
        for (i, m) in enumerate(ms)
            @printf(io, "%d,%.4f,%.6f\n", m, m / TABLE, a_mean[i])
        end
    end
    return ok ? 0 : 1
end

exit(main())
