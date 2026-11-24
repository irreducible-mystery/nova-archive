"""
vary_floors.py — "vary the floor, watch what survives," executable.

One world: N points on a circle of radius R (unknown to the claims).
Several floors: different coordinate choices (rotations, scalings, translations).
Several claims: each is tested under every floor.

The output shows, mechanically:
  - which claims survive every floor change (invariants),
  - which were floor-artifacts all along,
  - and the subtle one: a claim can be invariant under rotations but NOT
    under translations — so the survivor set depends on the variation set.
    There is no "invariant" full stop; only invariant-under-G.

Run: python3 vary_floors.py
"""

import math
import random

random.seed(20261016)

# ---- the world (what's "there"; the claims don't get to see this directly) ----
R_TRUE = 5.0
N_TRUE = 40
ANGLES = [2 * math.pi * i / N_TRUE for i in range(N_TRUE)]
WORLD = [(R_TRUE * math.cos(a), R_TRUE * math.sin(a)) for a in ANGLES]

# ---- floors: coordinate transformations applied to every observation ----
def rot(theta):
    c, s = math.cos(theta), math.sin(theta)
    return lambda p: (c * p[0] - s * p[1], s * p[0] + c * p[1])

def scale(k):
    return lambda p: (k * p[0], k * p[1])

def translate(dx, dy):
    return lambda p: (p[0] + dx, p[1] + dy)

def compose(*fs):
    def f(p):
        for g in fs:
            p = g(p)
        return p
    return f

FLOORS = {
    "identity":      lambda p: p,
    "rotated 37deg": rot(math.radians(37)),
    "rotated 129deg": rot(math.radians(129)),
    "scaled x2":     scale(2.0),
    "translated":    translate(3.0, -7.0),
    "rot+scale+tr":  compose(rot(math.radians(73)), scale(0.5), translate(-2.0, 4.0)),
}

# ---- claims: each takes observed points, returns a verdict string ----
def claim_radius_is_5(pts):
    rs = [math.hypot(x, y) for x, y in pts]
    r = sum(rs) / len(rs)
    return f"mean radius = {r:.3f}"

def claim_topmost_point(pts):
    top = max(pts, key=lambda p: p[1])
    return f"topmost at ({top[0]:.3f}, {top[1]:.3f})"

def claim_count(pts):
    return f"count = {len(pts)}"

def _z(v):
    v = round(v, 9)
    return 0.0 if v == 0 else v  # -0.0 == 0 -> normalize to 0.0

def claim_centroid_at_origin(pts):
    cx = _z(sum(p[0] for p in pts) / len(pts))
    cy = _z(sum(p[1] for p in pts) / len(pts))
    return f"centroid = ({cx:.3f}, {cy:.3f})"

def claim_all_same_radius(pts):
    rs = [math.hypot(x, y) for x, y in pts]
    spread = max(rs) - min(rs)
    return f"radius spread = {spread:.6f}"

def claim_total_angle(pts):
    angs = sorted(math.atan2(y, x) for x, y in pts)
    gaps = [angs[i + 1] - angs[i] for i in range(len(angs) - 1)]
    return f"max angular gap = {max(gaps):.4f} rad (uniform would be {2*math.pi/len(pts):.4f})"

CLAIMS = {
    "radius is 5":        claim_radius_is_5,
    "topmost point":      claim_topmost_point,
    "count is 40":        claim_count,
    "centroid at origin": claim_centroid_at_origin,
    "all same radius":    claim_all_same_radius,
    "even spacing":       claim_total_angle,
}

# rotation-only vs full variation sets, to show invariance is relative to G
ROTATION_FLOORS = {k: v for k, v in FLOORS.items() if k.startswith("identity") or k.startswith("rotated")}
ALL_FLOORS = FLOORS

def run(floors, label):
    print(f"=== {label} ({len(floors)} floors) ===")
    for cname, claim in CLAIMS.items():
        verdicts = set()
        for fname, f in floors.items():
            pts = [f(p) for p in WORLD]
            verdicts.add(claim(pts))
        status = "SURVIVES" if len(verdicts) == 1 else "floor-artifact"
        print(f"  [{status:>13}] {cname}")
        if len(verdicts) > 1:
            for v in sorted(verdicts):
                print(f"                  e.g. {v}")
        else:
            print(f"                  {next(iter(verdicts))}")
    print()

if __name__ == "__main__":
    run(ROTATION_FLOORS, "varying rotations only")
    run(ALL_FLOORS, "varying rotations + scale + translation")
    print("Note: 'centroid at origin' survives rotations but not translations.")
    print("There is no invariant full stop — only invariant-under-G.")
