"""
vary_floors_extended.py — the missing lessons, executable.

The original vary_floors.py varies the coordinate floor G and watches which
claims survive. It states three lessons. This extended version shows the floors
THAT script hides -- including the ones about its own method:

  E1  Reflections: chirality. Invariant under rotations, NOT under mirrors.
      (The original's G was only the orientation-preserving similarity group.)
  E2  Gauge invariance vs robustness: vary the WORLD, not just its coordinates.
      The "survivors" are mostly artifacts of a perfectly symmetric world.
  E3  The vacuous control: a claim blind to its input survives every floor.
      Survival is necessary but not sufficient for meaning.
  E4  The missing third verdict: a claim FALSE in every frame still reads
      "SURVIVES". So "survives" != "true".
  E5  Subgroup-lattice monotonicity: G' subset of G => Inv(G) subset of Inv(G').
      Bigger variation set, smaller survivor set.
  E6  The test is not invariant: vary the rounding precision and the
      SURVIVES/artifact verdict flips. Invariance is graded, not boolean.
  E7  The mechanism: equivariance. centroid(T(world)) == T(centroid(world)),
      so equivariant / equivariant = invariant -- i.e. nondimensionalization.

Run: python3 vary_floors_extended.py
"""

import math
import random

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

def reflect_x(p):   return (-p[0], p[1])      # mirror across the y-axis
def reflect_y(p):   return (p[0], -p[1])      # mirror across the x-axis
def reflect_diag(p): return (p[1], p[0])      # mirror across y = x

def compose(*fs):
    def f(p):
        for g in fs:
            p = g(p)
        return p
    return f

# ---- the subgroup lattice (each set is a superset of the previous) ----
ROT_FLOORS = {
    "identity":  lambda p: p,
    "rot 37deg": rot(math.radians(37)),
    "rot 129deg": rot(math.radians(129)),
}
REFLECT_FLOORS = {
    "reflect x":    reflect_x,
    "reflect y":    reflect_y,
    "reflect diag": reflect_diag,
}
ORTHO_FLOORS = {**ROT_FLOORS, **REFLECT_FLOORS}          # rotations + mirrors
SCALE_FLOORS = {
    "scale x2":   scale(2.0),
    "scale x0.5": scale(0.5),
}
TRANS_FLOORS = {
    "translate":   translate(3.0, -7.0),
    "rot+scale+tr": compose(rot(math.radians(73)), scale(0.5), translate(-2.0, 4.0)),
}
SIM_FLOORS   = {**ORTHO_FLOORS, **SCALE_FLOORS}          # + scaling
AFF_FLOORS   = {**SIM_FLOORS, **TRANS_FLOORS}            # + translation
# orientation-preserving affine (no mirror): chirality survives this one
ORIENT_FLOORS = {**ROT_FLOORS, **SCALE_FLOORS, **TRANS_FLOORS}

# ---- helpers ----
def _z(v, nd=6):
    """Round and normalize -0.0 to 0.0 so verdict strings compare cleanly."""
    v = round(v, nd)
    return 0.0 if v == 0 else v

def centroid(pts):
    n = len(pts)
    return (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n)

def radii_from(pts, origin):
    ox, oy = origin
    return [math.hypot(x - ox, y - oy) for x, y in pts]

def max_angular_gap_from(pts, origin):
    ox, oy = origin
    angs = sorted(math.atan2(y - oy, x - ox) for x, y in pts)
    gaps = [angs[i + 1] - angs[i] for i in range(len(angs) - 1)]
    gaps.append(angs[0] + 2 * math.pi - angs[-1])
    return max(gaps)

def signed_area(pts):
    """Shoelace signed area: >0 for CCW, <0 for CW. Flips under reflection."""
    n = len(pts)
    s = 0.0
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        s += x0 * y1 - x1 * y0
    return 0.5 * s

# ---- claims: each takes observed points, returns a verdict string ----
def claim_radius_is_5(pts):
    r = sum(radii_from(pts, (0, 0))) / len(pts)
    return f"mean radius from origin = {_z(r, 3):.3f}"

def claim_topmost_point(pts):
    top = max(pts, key=lambda p: p[1])
    return f"topmost at ({_z(top[0], 3):.3f}, {_z(top[1], 3):.3f})"

def claim_count(pts):
    return f"count = {len(pts)}"

def claim_centroid_at_origin(pts):
    cx, cy = centroid(pts)
    return f"centroid = ({_z(cx, 3):.3f}, {_z(cy, 3):.3f})"

def claim_same_radius_from_origin(pts):
    rs = radii_from(pts, (0, 0))
    return f"radius spread from origin = {_z(max(rs) - min(rs)):.6f}"

def claim_even_spacing_from_origin(pts):
    g = max_angular_gap_from(pts, (0, 0))
    return f"max angular gap about origin = {_z(g, 4):.4f} rad (uniform = {2*math.pi/len(pts):.4f})"

def claim_same_radius_from_centroid(pts):
    rs = radii_from(pts, centroid(pts))
    return f"radius spread from centroid = {_z(max(rs) - min(rs)):.6f}"

def claim_even_spacing_from_centroid(pts):
    g = max_angular_gap_from(pts, centroid(pts))
    return f"max angular gap about centroid = {_z(g, 4):.4f} rad (uniform = {2*math.pi/len(pts):.4f})"

def claim_roundness(pts):
    rs = radii_from(pts, centroid(pts))
    mean = sum(rs) / len(rs)
    return f"(max-min)/mean radius from centroid = {_z((max(rs) - min(rs)) / mean):.6f}"

# -- E1: chirality (the reflection floor) --
def claim_chirality(pts):
    """Dimensionless signed area: magnitude + handedness in one number."""
    A = signed_area(pts)
    rs = radii_from(pts, centroid(pts))
    m = sum(rs) / len(rs)
    norm = A / (m * m)
    tag = "CCW(+)" if norm > 0 else "CW(-)"
    return f"normalized signed area = {_z(norm, 4):.4f} [{tag}]"

def claim_handedness(pts):
    """Sign only: the discrete, qualitative part of chirality."""
    return "orientation = CCW" if signed_area(pts) > 0 else "orientation = CW"

# -- E3: the vacuous control (blind to its input) --
def claim_vacuous(pts):
    return "hello"          # ignores pts entirely

# -- E4: a claim that is FALSE in every frame --
def claim_count_is_41(pts):
    verdict = "TRUE" if len(pts) == 41 else "FALSE"
    return f"count is 41: {verdict} (actual {len(pts)})"

CLAIMS = {
    "radius is 5":                claim_radius_is_5,
    "topmost point":              claim_topmost_point,
    "count is 40":                claim_count,
    "centroid at origin":         claim_centroid_at_origin,
    "all same radius (origin)":   claim_same_radius_from_origin,
    "even spacing (origin)":      claim_even_spacing_from_origin,
    "all same radius (centroid)": claim_same_radius_from_centroid,
    "even spacing (centroid)":    claim_even_spacing_from_centroid,
    "roundness (dimensionless)":  claim_roundness,
    "chirality (signed area)":    claim_chirality,
    "handedness (sign only)":     claim_handedness,
    "VACUOUS control":            claim_vacuous,
    "FALSE-everywhere control":   claim_count_is_41,
}

# ---- generic test harness ----
def verdicts_for(claim, world, floors):
    d = {}
    for fname, f in floors.items():
        pts = [f(p) for p in world]
        d.setdefault(claim(pts), []).append(fname)
    return d

def survives(claim, world, floors):
    return len(verdicts_for(claim, world, floors)) == 1

def survivor_set(world, floors):
    return {c for c, claim in CLAIMS.items() if survives(claim, world, floors)}

def print_verdicts(claim, world, floors, indent="                   "):
    d = verdicts_for(claim, world, floors)
    for v, fl in sorted(d.items()):
        print(f"{indent}{v}   <- {', '.join(fl)}")
    return d


# ============================================================================
# EXPERIMENTS
# ============================================================================
def e0_baseline():
    print("=" * 74)
    print("E0  BASELINE (the original script, condensed)")
    print("=" * 74)
    for label, floors in [("rotations only", ROT_FLOORS), ("rot+scale+translation", AFF_FLOORS)]:
        surv = survivor_set(WORLD, floors)
        print(f"  under {label} ({len(floors)} floors), survivors:")
        for c in CLAIMS:
            mark = "SURVIVES" if c in surv else "artifact"
            print(f"      [{mark:>9}] {c}")
    print()

def e1_reflections():
    print("=" * 74)
    print("E1  REFLECTIONS: chirality (a floor the original G never included)")
    print("=" * 74)
    print("  The original floors were all orientation-preserving. Add mirrors:")
    for label, floors in [("rotations only", ROT_FLOORS), ("rotations + reflections", ORTHO_FLOORS)]:
        d = verdicts_for(claim_chirality, WORLD, floors)
        status = "SURVIVES" if len(d) == 1 else "floor-artifact"
        print(f"\n  [{status:>14}] chirality under {label}")
        print_verdicts(claim_chirality, WORLD, floors)
    print("\n  -> 'invariant under rotations' is NOT 'invariant'. Chirality is a")
    print("     genuine, dimensionless, self-referenced property that nonetheless")
    print("     dies the moment you allow a mirror. The subgroup matters.")
    print()

def e2_gauge_vs_robustness():
    print("=" * 74)
    print("E2  GAUGE INVARIANCE vs ROBUSTNESS: vary the WORLD, not just coords")
    print("=" * 74)
    random.seed(1234)
    EPS = 0.05
    jittered = [(x + random.uniform(-EPS, EPS), y + random.uniform(-EPS, EPS)) for x, y in WORLD]
    print(f"  Perturb every point by up to +/-{EPS} (the world is no longer perfect).")
    print(f"  {'claim':<28}{'coord-invariant?':<18}{'world-robust?'}")
    for cname, claim in CLAIMS.items():
        d_perfect = verdicts_for(claim, WORLD, ORIENT_FLOORS)
        d_jitter = verdicts_for(claim, jittered, ORIENT_FLOORS)
        coord_inv = len(d_perfect) == 1
        world_rob = len(d_jitter) == 1 and set(d_perfect) == set(d_jitter)
        print(f"  {cname:<28}{str(coord_inv):<18}{world_rob}")
    print("\n  -> The 'survivors' of the coordinate test (roundness, same-radius,")
    print("     even-spacing) are NOT robust: they held only because the world was")
    print("     a perfect circle. Gauge invariance != robustness. The original")
    print("     script varied coordinates but never the world, so it could not")
    print("     tell a law from a coincidence.")
    print()

def e3_vacuous_control():
    print("=" * 74)
    print("E3  THE VACUOUS CONTROL: survival is necessary, not sufficient")
    print("=" * 74)
    d = verdicts_for(claim_vacuous, WORLD, AFF_FLOORS)
    status = "SURVIVES" if len(d) == 1 else "floor-artifact"
    print(f"  [{status:>14}] VACUOUS control  (returns 'hello', ignores its input)")
    print_verdicts(claim_vacuous, WORLD, AFF_FLOORS)
    print("\n  -> A claim that says nothing survives everything. The test cannot")
    print("     distinguish a deep invariant from an empty one. A survivor set")
    print("     without a vacuity control is uninterpretable.")
    print()

def e4_false_everywhere():
    print("=" * 74)
    print("E4  THE MISSING THIRD VERDICT: a false claim still reads SURVIVES")
    print("=" * 74)
    d = verdicts_for(claim_count_is_41, WORLD, AFF_FLOORS)
    status = "SURVIVES" if len(d) == 1 else "floor-artifact"
    print(f"  [{status:>14}] FALSE-everywhere control")
    print_verdicts(claim_count_is_41, WORLD, AFF_FLOORS)
    print("\n  -> The binary is 'one verdict string' vs 'many'. A claim that is")
    print("     FALSE in every frame produces one (false) string and is labelled")
    print("     SURVIVES. So 'survives' != 'true'. The honest classification has")
    print("     three buckets: true-and-portable, true-but-frame-dependent, and")
    print("     simply false -- and the original test conflates the last with the")
    print("     first.")
    print()

def e5_lattice_monotonicity():
    print("=" * 74)
    print("E5  SUBGROUP LATTICE: G' subset of G  =>  Inv(G) subset of Inv(G')")
    print("=" * 74)
    groups = [
        ("rotations",                  ROT_FLOORS),
        ("+ reflections (orthogonal)", ORTHO_FLOORS),
        ("+ scaling (similarity)",     SIM_FLOORS),
        ("+ translation (affine)",     AFF_FLOORS),
    ]
    sets = [(gname, survivor_set(WORLD, g)) for gname, g in groups]
    for gname, s in sets:
        print(f"  Inv({gname:<28}) = {len(s):>2} claims : {sorted(s)}")
    print()
    ok = True
    for i in range(len(sets) - 1):
        g_small, s_small = sets[i]
        g_big, s_big = sets[i + 1]
        subset = s_big <= s_small
        ok = ok and subset
        print(f"  Inv({g_big}) subset of Inv({g_small}) : {subset}")
    print(f"\n  -> Monotone as required: enlarging G can only shrink the survivor")
    print(f"     set. Verified: {ok}. This is the real theorem the original")
    print(f"     gestured at. 'Invariant' is a function of G, full stop.")
    print()

def e6_test_not_invariant():
    print("=" * 74)
    print("E6  THE TEST IS NOT INVARIANT: vary the rounding precision")
    print("=" * 74)
    approx = {"identity": lambda p: p, "scale x(1+1e-5)": scale(1.0 + 1e-5)}
    print("  Claim: 'mean radius from origin'. Floors: identity vs scale(1+1e-5).")
    print("  The geometry is fixed; only the rounding precision nd changes.\n")
    print(f"  {'nd':<5}{'verdicts':<52}{'status'}")
    for nd in range(2, 9):
        def claim(pts, nd=nd):
            r = sum(radii_from(pts, (0, 0))) / len(pts)
            return f"mean radius = {_z(r, nd):.{nd}f}"
        d = verdicts_for(claim, WORLD, approx)
        status = "SURVIVES" if len(d) == 1 else "floor-artifact"
        vs = " | ".join(sorted(d))
        print(f"  {nd:<5}{vs:<52}{status}")
    print("\n  -> Same world, same floors, same claim -- only the test's precision")
    print("     changed, and the verdict flipped from SURVIVES to artifact. The")
    print("     original even hid a floor to make its test work: _z() exists only")
    print("     to map -0.0 -> 0.0 'so verdict strings compare cleanly'. Invariance")
    print("     is graded (how close?), not boolean. The test for invariance is")
    print("     not itself invariant.")
    print()

def e7_equivariance():
    print("=" * 74)
    print("E7  THE MECHANISM: equivariance (why centroid-anchoring rescues claims)")
    print("=" * 74)
    print("  A quantity is EQUIVARIANT if it moves with the data:")
    print("      centroid(T(world)) == T(centroid(world))   for every floor T\n")
    all_ok = True
    for fname, f in AFF_FLOORS.items():
        c_direct = centroid([f(p) for p in WORLD])
        c_mapped = f(centroid(WORLD))
        err = math.hypot(c_direct[0] - c_mapped[0], c_direct[1] - c_mapped[1])
        ok = err < 1e-9
        all_ok = all_ok and ok
        print(f"      centroid({fname:<12}(world)) == {fname:<12}(centroid(world)) : {ok}  (err {err:.1e})")
    print(f"\n  -> centroid is equivariant under every floor: {all_ok}.")
    print("     Equivariant / equivariant = invariant. That is the whole engine:")
    print("     roundness = (spread)/(mean radius) is a ratio of two equivariants,")
    print("     so the floor cancels -- exactly nondimensionalization / Buckingham")
    print("     pi. The original showed the trick without naming it, so a reader")
    print("     could not generalize it to a new problem.")
    print()

def summary():
    print("=" * 74)
    print("SUMMARY: the floors the original script hid")
    print("=" * 74)
    rows = [
        ("the world",        "E2: held fixed; 'survivors' were perfect-circle artifacts"),
        ("the group G",      "E1/E5: only orientation-preserving similarity; mirrors excluded"),
        ("the claim menu",   "E3: held fixed; a vacuous claim survives everything"),
        ("the verdict set",  "E4: only 2 of 3 buckets; false-everywhere reads SURVIVES"),
        ("the rounding",     "E6: verdict is a property of the test's precision"),
        ("the mechanism",    "E7: equivariance unnamed, so not generalizable"),
    ]
    for what, note in rows:
        print(f"  hidden floor: {what:<16} -> {note}")
    print("\n  Meta-lesson: the original's thesis is 'there is always a hidden")
    print("  floor', yet its own method hides six. The honest version would vary")
    print("  the choice of G over a space of groups -- and watch the survivor set")
    print("  itself become a floor-artifact. There is no frame that certifies frames.")


if __name__ == "__main__":
    e0_baseline()
    e1_reflections()
    e2_gauge_vs_robustness()
    e3_vacuous_control()
    e4_false_everywhere()
    e5_lattice_monotonicity()
    e6_test_not_invariant()
    e7_equivariance()
    summary()
