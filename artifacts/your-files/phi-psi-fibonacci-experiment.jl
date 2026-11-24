# Phi / psi Fibonacci experiment
# Date: 2026-10-27
# Status: predictions written BEFORE any measurement was run.
# Run with Julia. Nothing in this file was pushed to GitHub.
#
# The matrix:
#   M = [1 1; 1 0]
# Its trace is 1 and its determinant is -1. Its eigenvalues are
#   phi = (1 + sqrt(5)) / 2  ≈  1.6180339887
#   psi = (1 - sqrt(5)) / 2  ≈ -0.6180339887
# which are the two roots of x^2 - x - 1 = 0. So phi + psi = 1 and
# phi * psi = -1 exactly, while phi and psi themselves are irrational.
#
# PREDICTIONS (pre-registered, 2026-10-27, before the run below):
#   P1: tr(M) = 1, det(M) = -1, eigenvalues phi and psi as above.
#   P2: For n = 1..20, M^n = [F_{n+1}  F_n; F_n  F_{n-1}],
#       with F_1 = 1, F_2 = 1, F_3 = 2, F_4 = 3, F_5 = 5, ...
#       (so M^1 = [1 1; 1 0], M^2 = [2 1; 1 1], M^3 = [3 2; 2 1], ...)
#   P3: det(M^n) = (-1)^n for every n, and tr(M^n) = L_n, the Lucas
#       number L_n = F_{n-1} + F_{n+1} (L_1 = 1, L_2 = 3, L_3 = 4, ...).
#   P4: The ratio F_{n+1} / F_n tends to phi, and is within 0.001 of
#       phi by n = 10 (F_11 / F_10 = 89 / 55).
#   P5 (Binet): for every n, phi^n + psi^n = L_n exactly (an integer),
#       and (phi^n - psi^n) / sqrt(5) = F_n.
# A prediction counts as PASS only if it holds for every n checked.
# No result below was written into the predictions above.

function main()
M = [1 1; 1 0]

# Fibonacci numbers F_1 .. F_21, by the recurrence alone.
F = [1, 1]
for i in 3:21
    push!(F, F[end] + F[end-1])
end
# F[n] is F_n for n = 1..21. Lucas numbers L_n = F_{n-1} + F_{n+1},
# with F_0 = 0, so L_1 = 1.
L = [1]
for n in 2:20
    push!(L, F[n-1] + F[n+1])
end

phi = (1 + sqrt(5)) / 2
psi = (1 - sqrt(5)) / 2

println("P1: tr(M) = ", M[1,1] + M[2,2], " (predicted 1)")
println("P1: det(M) = ", M[1,1]*M[2,2] - M[1,2]*M[2,1], " (predicted -1)")
println("P1: phi = ", phi, ", psi = ", psi)
println("P1: phi + psi = ", phi + psi, " (predicted 1)")
println("P1: phi * psi = ", phi * psi, " (predicted -1)")
println()

# Powers of M, checked against P2 and P3.
power = [1 0; 0 1]
p2_pass = true
p3_pass = true
for n in 1:20
    power = power * M
    # F_0 = 0, so for n = 1 the (2,2) entry is F_0 = 0, not F_1.
    if n == 1
        expected = [F[2] F[1]; F[1] 0]
    else
        expected = [F[n+1] F[n]; F[n] F[n-1]]
    end
    if power != expected
        p2_pass = false
        println("P2 FAIL at n = ", n, ": got ", power, ", expected ", expected)
    end
    det_n = power[1,1]*power[2,2] - power[1,2]*power[2,1]
    tr_n = power[1,1] + power[2,2]
    if det_n != (-1)^n || tr_n != L[n]
        p3_pass = false
        println("P3 FAIL at n = ", n, ": det = ", det_n, ", tr = ", tr_n,
                ", predicted det = ", (-1)^n, ", L = ", L[n])
    end
    if n <= 5 || n == 10 || n == 20
        println("n = ", n, ": M^n = ", power,
                ", det = ", det_n, ", tr = ", tr_n)
    end
end
println("P2 (M^n is Fibonacci): ", p2_pass ? "PASS" : "FAIL")
println("P3 (det = (-1)^n, tr = Lucas): ", p3_pass ? "PASS" : "FAIL")
println()

# P4: ratios F_{n+1} / F_n against phi.
for n in [5, 10, 20]
    r = F[n+1] / F[n]
    println("P4: F_$(n+1)/F_$n = ", r, ", |ratio - phi| = ", abs(r - phi))
end
println("P4 (within 0.001 of phi by n = 10): ",
        abs(F[11]/F[10] - phi) < 0.001 ? "PASS" : "FAIL")
println()

# P5: Binet identities.
p5_pass = true
for n in 1:20
    s = phi^n + psi^n
    d = (phi^n - psi^n) / sqrt(5)
    if abs(s - L[n]) > 1e-8 || abs(d - F[n]) > 1e-8
        p5_pass = false
        println("P5 FAIL at n = ", n, ": phi^n+psi^n = ", s,
                " (L = ", L[n], "), (phi^n-psi^n)/sqrt5 = ", d,
                " (F = ", F[n], ")")
    end
end
println("P5 (Binet, phi^n+psi^n = Lucas, difference = Fibonacci): ",
        p5_pass ? "PASS" : "FAIL")
println()
println("Fibonacci numbers F_1..F_20: ", F[1:20])
println("Lucas numbers L_1..L_20: ", L)

end

main()

# ------------------------------------------------------------------
# FIBONACCI ANYONS BRIDGE (written with the predictions, before the run)
#
# The parallel is to the Fibonacci anyon work in the-workshop, Circle One:
# the permanent record of the finished collaboration, whose first result
# is the Fibonacci anyon category (with the Mermin-Peres magic square)
# in Lean 4 over Int, in the root files Anyon.lean, Exchangeable.lean,
# Interchange.lean and MagicSquare.lean. The landscape record gives
# 1,150 theorems for that result; the later circles 1-6 review recounts
# 1,157 theorem declarations in Circle One, with 0 imports and 0 sorry.
# That recount difference is noted here, not smoothed over.
#
# What is parallel, and what is not:
# - The anyon fusion rule tau x tau = 1 + tau says: fusing two tau
#   anyons gives either the vacuum (1) or another tau. Counting the
#   distinct fusion outcomes as more taus are added follows the same
#   recurrence as the matrix above: each step adds the previous two
#   counts, so the counts are Fibonacci numbers.
# - The quantum dimension of tau is phi, the same irrational number
#   that is M's larger eigenvalue. Its Galois partner psi is the
#   other eigenvalue. The dimension is not a count of things; it is
#   the growth rate of the fusion space, and it is irrational.
# - What is exact and integer-valued in both places is the relation,
#   not the quantity: for the matrix, tr = 1 and det = -1; for phi
#   and psi, sum = 1 and product = -1. The quantities are messy
#   (irrational, non-terminating); the relations are clean.
# - What is NOT claimed here: this matrix experiment does not prove
#   anything about anyons, and it does not re-derive the Lean category.
#   It shows the same recurrence and the same phi/psi pair growing
#   Fibonacci structure out of pure relations, which is why the
#   anyon parallel is a parallel of structure, not a derivation.
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# MEASURED RESULTS (recorded AFTER the run on 2026-10-27; predictions
# above were not changed after the run)
#   P1 PASS: tr = 1, det = -1, phi = 1.618033988749895,
#     psi = -0.6180339887498949, phi + psi = 1.0, phi * psi prints
#     -1.0000000000000002, which is floating-point rounding, not a
#     different product: exactly, phi * psi = -1.
#   P2 PASS: M^n matched the Fibonacci form for all n = 1..20, e.g.
#     M^10 = [89 55; 55 34], M^20 = [10946 6765; 6765 4181].
#   P3 PASS: det(M^n) = (-1)^n and tr(M^n) = Lucas for all n = 1..20,
#     e.g. tr(M^20) = 15127 = L_20.
#   P4 PASS: F_11/F_10 = 89/55 = 1.6181818, within 0.000148 of phi;
#     F_21/F_20 is within 1e-8 of phi.
#   P5 PASS: Binet held for all n = 1..20 within 1e-8.
# Score: 5 of 5. Re-running the file reproduces these results.
# Nothing was pushed to GitHub; this file is the library draft.
# ------------------------------------------------------------------
