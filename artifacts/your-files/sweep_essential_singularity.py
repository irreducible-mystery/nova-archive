#!/usr/bin/env python3
"""Part 3 of the number-systems sweep coda: the essential singularity e^{1/z}
at z=0 -- the one blowup the catalog left as 'unknown'.

Casorati-Weierstrass / Picard's great theorem: near an essential singularity
a function takes EVERY value (Picard: every value except possibly one,
infinitely often) in every punctured neighborhood. We measure it two ways:

  1. On the circle |z| = r, compute the winding number of the image curve
     theta -> e^{1/(r e^{itheta})} around several target values, via phase
     unwrapping of (w - t). Each unit of winding forces a near-pass of t;
     theory says ~1/(pi*r) windings.
  2. Approach along rays z = t*e^{i phi}, t -> 0+: report log-modulus and
     argument of e^{1/z} directly (no overflow possible). The 'limit'
     depends on the path; along the imaginary axis there is no limit at all.

Honest notes:
  - e^{1/z} never equals 0 (Picard's one exception for this function).
    The wildest blowup still has one value it never touches.
  - Winding counts near-passes of the curve, not exact solutions of
    e^{1/z} = t; by continuity each winding forces arbitrarily close hits.
"""

import cmath
import math

TARGETS = [1 + 0j, -1 + 0j, 1j, 2 + 3j, 0.5 - 0.25j]


def image(theta, r):
    z = r * complex(math.cos(theta), math.sin(theta))
    return cmath.exp(1 / z)


def winding(r, t, n=400_000):
    """Winding number of theta -> e^{1/(r e^{itheta})} around target t."""
    total = 0.0
    prev = None
    for j in range(n):
        a = cmath.phase(image(2 * math.pi * j / n, r) - t)
        if prev is not None:
            delta = a - prev
            while delta > math.pi:
                delta -= 2 * math.pi
            while delta <= -math.pi:
                delta += 2 * math.pi
            total += delta
        prev = a
    return total / (2 * math.pi)


def main():
    print("=== winding of e^{1/z} on |z| = r around targets (400k samples) ===")
    print("theory: arg(e^{1/z}) = -(sin theta)/r sweeps [-1/r, 1/r] ->")
    print("        ~1/(pi*r) full windings; near-passes scale with windings.")
    print()
    header = "r       " + "".join(f"{str(t):>14}" for t in TARGETS)
    print(header)
    for r in [0.5, 0.1, 0.05, 0.01, 0.005]:
        row = f"{r:<8}"
        for t in TARGETS:
            w = winding(r, t)
            row += f"{w:>14.1f}"
        theory = 1 / (math.pi * r)
        print(f"{row}   (theory ~{theory:.1f})")
    print()
    print("=== approach along rays: z = t * e^{i phi}, t -> 0+ ===")
    print("log|e^{1/z}| = cos(phi)/t,  arg(e^{1/z}) = -sin(phi)/t  (exact, no overflow)")
    print()
    for phi_deg in [0, 45, 90, 135, 180]:
        phi = math.radians(phi_deg)
        parts = []
        for t in [0.1, 0.01, 0.001]:
            logmod = math.cos(phi) / t
            arg = -math.sin(phi) / t
            parts.append(f"log|w|={logmod:+.0f} arg={arg:+.0f}rad")
        print(f"phi = {phi_deg:>3} deg:  " + "   ->   ".join(parts))
    print()
    print("reading: phi=0   log|w| -> +inf  (blows to infinity);")
    print("         phi=180 log|w| -> -inf  (collapses to 0, never touching it);")
    print("         phi=90  |w|=1 forever, arg spins -1000 rad by t=0.001:")
    print("                 no limit at all -- the curve wraps the unit circle")
    print("                 infinitely often, taking every value on it.")
    print()
    print("Picard's exception: e^{1/z} != 0 for all z -- the one value the")
    print("wildest blowup never touches. Compare: the gap stays empty.")


if __name__ == "__main__":
    main()
