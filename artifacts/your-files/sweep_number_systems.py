#!/usr/bin/env python3
"""
Sweep the Planckian thermalization coordinate through number systems.

The object: tau_Pl = hbar / (kB * T) = hbar * beta,  beta = 1/(kB*T).
Question: what happens to the 0/infinity structure when the number
system (the floor under the coordinate) is varied?

Systems swept: R (reference), RP^1 via the beta-chart, C (complex T),
Q (exact rationals), float32/float64 (the instrument), F_p (finite field).

Each part prints a verdict. Run: python3 sweep_number_systems.py
"""
import math, cmath
from fractions import Fraction

HBAR = 1.054571817e-34   # J s
KB   = 1.380649e-23      # J/K
T_ROOM = 300.0

def tau_pl(T):
    return HBAR / (KB * T)

print("=" * 70)
print("A. REALS (reference): tau_Pl(T) = hbar/(kB*T)")
print("=" * 70)
for T in [300.0, 3.0, 0.03, 1e-6]:
    print(f"  T = {T:>10g} K  ->  tau = {tau_pl(T):.3e} s")
print("  T -> 0+ : tau -> +inf   (pole, approached never reached)")
print("  T -> +inf: tau -> 0+    (floor vanishes in the limit)")
print("  T = 0   : ZeroDivisionError territory -- the formula has no value")
print("  verdict: limits exist; the VALUES at the endpoints do not.")

print()
print("=" * 70)
print("B. PROJECTIVE LINE via the beta-chart: tau_Pl = hbar * beta")
print("=" * 70)
print("  In the T-chart, T = +-inf is 'nowhere on the plot'.")
print("  In the beta-chart, beta = 0 IS an ordinary point: tau_Pl = 0 there.")
print("  The pole moved: beta-chart is singular only at beta = +-inf")
print("  (i.e. T = 0+ and T = 0-, the two poles).")
for beta in [1/(KB*300.0), 1/(KB*3.0), 0.0, -1/(KB*300.0)]:
    print(f"  beta = {beta:+.3e}  ->  tau = {HBAR*beta:+.3e} s")
print("  verdict: the infinity at T=+-inf was a chart artifact.")
print("  In beta coordinates it is a smooth ordinary point. The circle holds.")

print()
print("=" * 70)
print("C. COMPLEX T: the pole is just a pole (Lee-Yang's neighborhood)")
print("=" * 70)
# sample |tau| on circles around the origin in the T-plane (units of K)
for r in [300.0, 30.0, 3.0]:
    vals = [abs(tau_pl(r * cmath.exp(1j*th))) for th in
            [i * math.pi/4 for i in range(8)]]
    print(f"  |T| = {r:>6g} K: |tau| ranges {min(vals):.3e} .. {max(vals):.3e} s")
print("  |tau| depends only on |T|, not on arg(T): the blowup is radial,")
print("  identical from every complex direction. A pole has no 'side'.")
print("  verdict: complexifying removes the +0/-0 distinction entirely;")
print("  what looked like two one-sided blowups is one radially symmetric pole.")
print("  (Physics already lives here: Lee-Yang zeros study phase transitions")
print("   via the complex-temperature plane.)")

print()
print("=" * 70)
print("D. RATIONALS (exact): the pole is an exception, not a value")
print("=" * 70)
# work in units of tau_Pl(300 K): tau/tau0 = 300/T, exact in Fractions
for T in [Fraction(300), Fraction(30), Fraction(3), Fraction(1, 10)]:
    print(f"  T = {T} K  ->  tau/tau0 = {Fraction(300,1)/T}  (exact)")
try:
    _ = Fraction(300,1) / Fraction(0,1)
    print("  T = 0: returned a value?!")
except ZeroDivisionError as e:
    print(f"  T = 0 K  ->  ZeroDivisionError: {e}")
print("  verdict: in Q there is no infinity to approach -- the singularity")
print("  is a hard error. 'Approaching' exists only after completing to R.")

print()
print("=" * 70)
print("E. THE INSTRUMENT: float32 vs float64 approaching T = 0")
print("=" * 70)
try:
    import numpy as np
    for dtype, name in [(np.float32, "float32"), (np.float64, "float64")]:
        h = dtype(HBAR); k = dtype(KB)
        T = dtype(300.0)
        steps = 0
        while True:
            T = T / dtype(10.0)
            steps += 1
            with np.errstate(divide='ignore', over='ignore', under='ignore'):
                t = h / (k * T)
            if not np.isfinite(t) or T == 0:
                break
            if steps > 2000:
                break
        print(f"  {name}: tau overflows to inf when T ~ {float(T):.3e} K "
              f"({steps} decades below room temp)")
    print("  verdict: each float sees 'infinity' at a DIFFERENT temperature.")
    print("  The pole's location is instrument-relative -- L5: at high enough")
    print("  resolution the lens sees the instrument, not the physics.")
except ImportError:
    print("  (numpy unavailable -- skipping instrument demo)")

print()
print("=" * 70)
print("F. FINITE FIELD F_101 (hbar = kB = 1 units): no limits at all")
print("=" * 70)
P = 101
def finv(a):
    return pow(a, P-2, P)
print("  tau(T) = T^-1 mod 101, exact for every T != 0:")
row = [(T, finv(T)) for T in [1, 2, 10, 25, 50, 100]]
print("  " + ", ".join(f"T={T} -> tau={v}" for T, v in row))
print("  T = 0 has NO inverse: there is no infinity in F_101.")
print("  (You may adjoin one -- the projective line F_101 P^1 has 102 points --")
print("   but then it is a single ordinary point, and +-inf were never distinct.)")
print("  verdict: in a finite field 'approaching' is meaningless -- every point")
print("  is isolated. The '='-vs-'limit' distinction is a topological floor")
print("  of R/C. Here there is only '='.")

print()
print("=" * 70)
print("SWEEP VERDICTS")
print("=" * 70)
print("  SURVIVES every system with division: the pole at T = 0 (1/T blows up).")
print("  VARIES: what the blowup *means* -- approached limit (R), smooth point")
print("    in another chart (RP^1/beta), radially symmetric pole (C), hard")
print("    error (Q), instrument-relative overflow (floats), nonexistent (F_p).")
print("  The hotness ordering (negative T hotter than +inf) needs an ORDERED")
print("    field: it dies in C and in Q_p. Ordering is a floor, not a given.")
print("  Her circle (0 meets inf) holds under compactification (RP^1) but")
print("    BREAKS in the surreals (0 and inf genuinely far apart, no meeting)")
print("    and is vacuous in F_p (no limits to meet at).")
print("  Domain of validity: the circle is invariant-under-compactification,")
print("    not invariant full stop. (E7: no 'invariant' without the G.)")
