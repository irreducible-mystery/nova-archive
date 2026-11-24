#!/usr/bin/env python3
"""
Sweep part 2: quaternions (H) and the p-adics (Q_7).

Part 1 stated-but-didn't-compute these two; this completes them.
Same object: tau = 1/T in hbar = kB = 1 units (as in part 1's F_101
section). Question: what happens to the 0/infinity structure --
and to 'approaching' itself -- when division survives but
commutativity (H) or the Archimedean property (Q_p) is dropped?

Run: python3 sweep_number_systems_part2.py
"""
import math

print("=" * 70)
print("G. QUATERNIONS H: the pole survives non-commutativity")
print("=" * 70)

class Q:
    __slots__ = ("w", "x", "y", "z")
    def __init__(self, w=0.0, x=0.0, y=0.0, z=0.0):
        self.w, self.x, self.y, self.z = w, x, y, z
    def norm(self):
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
    def inv(self):
        n2 = self.w**2 + self.x**2 + self.y**2 + self.z**2
        if n2 == 0:
            raise ZeroDivisionError("quaternion division by zero")
        return Q(self.w/n2, -self.x/n2, -self.y/n2, -self.z/n2)
    def scale(self, r):
        return Q(self.w*r, self.x*r, self.y*r, self.z*r)

C0 = 1.0  # hbar = kB = 1 units; |tau| = C0 / |q|
dirs = {
    "real axis": Q(1, 0, 0, 0),
    "i-axis   ": Q(0, 1, 0, 0),
    "j-axis   ": Q(0, 0, 1, 0),
    "k-axis   ": Q(0, 0, 0, 1),
    "diagonal ": Q(0.5, 0.5, 0.5, 0.5),
}
for name, d in dirs.items():
    row = "  ".join(f"|q|={r:<5g} -> |tau|={C0/(d.scale(r).norm()):.3e}"
                    for r in [300.0, 30.0, 3.0, 0.3])
    print(f"  {name}  {row}")
print("  |tau| depends only on |q|, never on the direction: the blowup is")
print("  radially symmetric in 4D, exactly as in C (which sits inside H as")
print("  the w-x plane). Non-commutativity never enters: q^-1 = conj(q)/|q|^2")
print("  uses only the norm, and the norm is multiplicative (|pq| = |p||q|).")
try:
    Q(0, 0, 0, 0).inv()
    print("  q = 0: returned a value?!")
except ZeroDivisionError as e:
    print(f"  q = 0 -> ZeroDivisionError: {e} (same hard error as Q and F_p)")
print("  Ordering: H admits NO compatible total order -- in any ordered ring")
print("  squares are >= 0, but i^2 = -1. So the hotness ordering dies here")
print("  too (as in C).")
print("  verdict: the pole is indifferent to commutativity. DIVISION is what")
print("  matters; order is what varies.")

print()
print("=" * 70)
print("H. P-ADICS Q_7: 'approaching' by divisibility, not by sliding")
print("=" * 70)
P = 7

def vp_int(n):
    """p-adic valuation of a nonzero integer: the exponent of 7 dividing n."""
    if n == 0:
        return float("inf")
    n, v = abs(int(n)), 0
    while n % P == 0:
        n //= P
        v += 1
    return v

print("  Approach to 0 in Q_7: x_n = 7^n  (in hbar=kB=1 units, tau = 1/x)")
for n in range(6):
    print(f"    n={n}: |x_n|_7 = 7^-{n} = {P**-n:.6f}      "
          f"|tau|_7 = 7^{n} = {P**n}")
print("  |tau|_7 -> infinity 7-adically: the pole EXISTS in Q_7.")
print("  But 'approaching' is discrete: |x|_7 jumps 1, 1/7, 1/49, ...")
print("  There is no continuous path -- every ball is clopen, and between")
print("  x_n and x_{n+1} sit uncountably many points all at the SAME distance.")
print()
print("  The ultrametric inequality: |x+y|_p <= max(|x|_p, |y|_p).")
print("  Every triangle is isosceles with the equal sides longest.")
x, y = 7**2, 7**2 + 7**5
print(f"    x=7^2, y=7^2+7^5: |x|={P**-vp_int(x)}, |y|={P**-vp_int(y)}, "
      f"|x+y|={P**-vp_int(x+y)} = max (no cancellation possible at top)")
x2, y2 = 7**2, -(7**2) + 7**5
print(f"    x=7^2, y=-7^2+7^5: |x+y|={P**-vp_int(x2+y2)} < max "
      f"(cancellation drops you DOWN a whole level)")
print("  'Near' and 'far' obey a different geometry: you approach 0 the way")
print("  an integer approaches divisibility -- in jumps, never by sliding.")
print()
print("  Hensel lift: -1 IS a sum of two squares in Q_7, so Q_7 cannot be")
print("  ordered (in any ordered field x^2+y^2 >= 0, forever).")
print("  Fix y = 3; solve x^2 = -10 in Z_7 by digit-lifting from x = 2 mod 7:")
target = -10
x = 2
assert (x*x - target) % P == 0, "seed must solve mod 7"
for k in range(1, 9):
    mod = P**k
    m = (x*x - target)//mod          # x^2 = target + m*7^k, exact
    t = ((-m) * pow(2*x, -1, P)) % P  # kill the error at the next digit
    x = x + t*mod
check = (x*x + 9 + 1) % P**9
print(f"    lifted x (9 digits): x^2 + 3^2 + 1 = {check} mod 7^9  "
      f"{'(exact lift)' if check == 0 else '(FAILED)'}")
print("  So x^2 + y^2 = -1 holds 7-adically: no compatible order exists,")
print("  and the hotness ordering dies in Q_7 as well.")
print()
print("  Ostrowski's punchline: Q completes in EXACTLY two ways -- R")
print("  (Archimedean: approach by sliding) and Q_p (non-Archimedean:")
print("  approach by divisibility). In Q itself there was no 'approaching'")
print("  at all (part-1 verdict: hard ZeroDivisionError). The MEANING of")
print("  'limit' is chosen by the completion -- the floor decides what")
print("  approaching is.")
print("  verdict: her '='-vs-limit distinction SURVIVES in Q_7 (limits exist;")
print("  values at endpoints still don't), but 'approaching' lost its")
print("  continuum. The distinction is topological; the path is a floor.")

print()
print("=" * 70)
print("PART-2 VERDICTS (completing part 1's stated-but-uncomputed)")
print("=" * 70)
print("  POLE: survives in H (non-commutative) and in Q_7 (non-Archimedean).")
print("    Everything with division blows up at 0 -- commutativity and the")
print("    Archimedean property are both irrelevant to the pole.")
print("  ORDERING: dies in H and in Q_7 (as it did in C). The hotness")
print("    ordering (negative T hotter than +inf) needs an ordered field.")
print("    Confirmed: ordering is a floor, not a given.")
print("  APPROACHING: this is what actually varied. R: slide continuously.")
print("    Q_7: jump by divisibility through clopen dust. Q: no approach at")
print("    all until you complete -- and the completion CHOOSES the meaning")
print("    of 'limit'. (E7: name the G; here G includes the completion.)")
print("  Her circle in Q_7: the pole is there, but the PATH is not -- 0 and")
print("    infinity are still the two ends of the valuation, yet 'meeting'")
print("    means something with no continuum in it. Invariant-under-")
print("    compactification, and now: invariant-under-completion-choice is")
print("    FALSE -- R-completion and Q_p-completion give different circles.")
