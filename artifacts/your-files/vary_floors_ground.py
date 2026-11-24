"""
vary_floors_ground.py — where the regress stops, executable.

The series so far:
    vary_floors.py            vary coordinates     -> some claims survive
    vary_floors_extended.py   vary the group       -> the survivor set shrinks
    vary_floors_meta.py       vary the group-choice-> "no frame certifies frames"

Each script turned the method on the one before. This one does that once more
-- the critics hid floors too -- and then stops, because the regress has an
exit that is not another frame.

  F1  THE STABILIZER. The world has 40-fold symmetry. Rotate by 9 degrees and
      "topmost point" SURVIVES. "Survives" never measured the claim; it measured
      the orbit of THIS world under the SAMPLE of G you happened to pick. Every
      script in the series sampled G, and the sample is a floor.
  F2  FIXED POINTS. "all same radius (centroid)" is scale-EQUIVARIANT, not
      invariant: spread scales with k. It read SURVIVES only because its value
      on a perfect circle is 0, and 0*k = 0. A generic world exposes it.
      (F1 + F2: "invariant at w" != "invariant as a function". The generic
      world gives you the function-level verdict; the symmetric world lies.)
  F3  E2 REWARDS VACUITY. The extended script's "world-robust?" column demands
      the SAME verdict string on a different world. That is E3's vacuity
      criterion, verbatim. Its "robust" set is exactly the claims that do not
      measure anything. Robustness is continuity, not constancy.
  F4  PART B IS A TAUTOLOGY. "Nested floor sets => nested orbits => antitone
      survivor map" holds for ANY nested sets of ANY functions -- shown here
      with non-invertible, non-closed warps. The meta script's "groups" were
      never groups ({rot 37, rot 129} is not closed). It verified set theory.
  F5  ERLANGEN. The exit. You do not DISCOVER G, you DECLARE it, and the
      declaration is the question. "Is it round?" is a question about shape,
      and shape IS the similarity orbit. "Which point is highest?" is a
      question in a geometry with a preferred direction -- and there,
      "topmost" is a perfectly good invariant. Four questions, four groups,
      four survivors. Artifact-hood is relative to a question, and the
      question is not a floor: it is the thing you wanted to know.

Run: python3 vary_floors_ground.py
"""

import math
import random

from vary_floors_extended import (
    WORLD, N_TRUE, rot, scale, translate, reflect_x, reflect_y, compose,
    CLAIMS, verdicts_for, survives, survivor_set,
    centroid, radii_from, max_angular_gap_from, signed_area, _z,
    ROT_FLOORS, ORTHO_FLOORS, SIM_FLOORS, AFF_FLOORS, ORIENT_FLOORS,
    REFLECT_FLOORS, SCALE_FLOORS, TRANS_FLOORS,
)

W = 78


def banner(title):
    print("=" * W)
    print(title)
    print("=" * W)


def status(d):
    return "SURVIVES" if len(d) == 1 else "floor-artifact"


# ---- a generic world: no symmetry to hide behind -------------------------
random.seed(20240607)
GENERIC = [(random.uniform(-5, 5), random.uniform(-5, 5)) for _ in range(N_TRUE)]


# ============================================================================
# F1  THE STABILIZER
# ============================================================================
def f1_stabilizer():
    banner("F1  THE STABILIZER: the sample of G is a floor")
    step = 360.0 / N_TRUE
    lucky = {"identity": lambda p: p,
             "rot 37deg": rot(math.radians(37)),
             "rot 129deg": rot(math.radians(129))}
    unlucky = {"identity": lambda p: p,
               f"rot {step:g}deg": rot(math.radians(step)),
               f"rot {3*step:g}deg": rot(math.radians(3 * step)),
               "rot 90deg": rot(math.radians(90))}
    print(f"  The world is {N_TRUE} points; rotating by {step:g} degrees maps it onto itself.")
    print("  Same claim ('topmost point'), same world, two SAMPLES of the rotation group:\n")
    for label, floors in [("original sample {37, 129}", lucky),
                          (f"stabilizer sample {{{step:g}, {3*step:g}, 90}}", unlucky)]:
        d = verdicts_for(CLAIMS["topmost point"], WORLD, floors)
        print(f"  [{status(d):>14}] topmost point under {label}")
        for v, fl in sorted(d.items()):
            print(f"                   {v}   <- {', '.join(fl)}")
        print()
    print("  Now the whole survivor set, same two samples, and then on a GENERIC")
    print("  world (random points, no symmetry):\n")
    s_lucky = survivor_set(WORLD, lucky)
    s_unlucky = survivor_set(WORLD, unlucky)
    s_generic = survivor_set(GENERIC, unlucky)
    print(f"  circle, sample {{37,129}}   : {len(s_lucky):>2} survive")
    print(f"  circle, stabilizer sample  : {len(s_unlucky):>2} survive  (+{sorted(s_unlucky - s_lucky)})")
    print(f"  generic, stabilizer sample : {len(s_generic):>2} survive  (-{sorted(s_unlucky - s_generic)})")
    print("\n  -> 'SURVIVES' was never a property of the claim. It is a property of")
    print("     (claim, world, sample-of-G). The original got the 'right' answer for")
    print("     'topmost point' by luck of the draw: 37 and 129 are not multiples of 9.")
    print("     Every script in this series sampled G with two or three elements and")
    print("     called the result 'invariance'. The stabilizer of the world is the")
    print("     floor none of them varied.")
    print()


# ============================================================================
# F2  FIXED POINTS: equivariant claims masquerade as invariant
# ============================================================================
def spread_from_centroid(pts):
    rs = radii_from(pts, centroid(pts))
    return max(rs) - min(rs)


def f2_fixed_points():
    banner("F2  FIXED POINTS: 'all same radius (centroid)' is equivariant, not invariant")
    print("  spread(k * world) = k * spread(world).  That is scale-EQUIVARIANCE.")
    print("  It reads SURVIVES on the circle only because spread = 0 and 0 * k = 0.\n")
    floors = {"identity": lambda p: p, **SCALE_FLOORS}
    for wname, world in [("perfect circle", WORLD), ("generic world", GENERIC)]:
        d = verdicts_for(CLAIMS["all same radius (centroid)"], world, floors)
        print(f"  [{status(d):>14}] all same radius (centroid) on {wname}")
        for v, fl in sorted(d.items()):
            print(f"                   {v}   <- {', '.join(fl)}")
    print("\n  Function-level verdicts (generic world, full affine sample) vs the")
    print("  circle's verdicts. Claims that survive on the circle but NOT generically")
    print("  were never invariants; they were fixed points of the induced action.\n")
    s_circle = survivor_set(WORLD, AFF_FLOORS)
    s_generic = survivor_set(GENERIC, AFF_FLOORS)
    print(f"  {'claim':<28}{'circle':<12}{'generic':<12}{'reading'}")
    for c in CLAIMS:
        a, b = c in s_circle, c in s_generic
        if a and b:
            note = "invariant (as a function)"
        elif a and not b:
            note = "FIXED-POINT ARTIFACT of the symmetric world"
        elif not a and b:
            note = "(cannot happen: generic is a subset)"
        else:
            note = "artifact"
        print(f"  {c:<28}{str(a):<12}{str(b):<12}{note}")
    print("\n  -> The original's headline -- '(centroid) versions survive everything' --")
    print("     is half world-artifact. The honest test of a claim's invariance is")
    print("     on a world with trivial stabilizer and no special values. The")
    print("     perfect circle was the worst possible test world, because it was")
    print("     chosen to make the claims come out true.")
    print()


# ============================================================================
# F3  E2 REWARDS VACUITY: constancy vs continuity
# ============================================================================
def roundness_val(pts):
    rs = radii_from(pts, centroid(pts))
    return (max(rs) - min(rs)) / (sum(rs) / len(rs))


def gap_val(pts):
    return max_angular_gap_from(pts, centroid(pts))


def jitter(world, eps, seed=1234):
    rng = random.Random(seed)
    return [(x + rng.uniform(-eps, eps), y + rng.uniform(-eps, eps)) for x, y in world]


def f3_continuity():
    banner("F3  E2 REWARDS VACUITY: 'world-robust' was 'constant across worlds'")
    print("  Re-run E2's criterion exactly: robust := same verdict string on the")
    print("  jittered world as on the perfect one.\n")
    jit = jitter(WORLD, 0.05)
    robust = set()
    for c, cl in CLAIMS.items():
        d0 = verdicts_for(cl, WORLD, ORIENT_FLOORS)
        d1 = verdicts_for(cl, jit, ORIENT_FLOORS)
        if len(d1) == 1 and set(d0) == set(d1):
            robust.add(c)
    print(f"  E2's 'robust' set: {sorted(robust)}")
    # which claims are literally insensitive to the world? test on GENERIC too
    insensitive = {c for c, cl in CLAIMS.items()
                   if set(verdicts_for(cl, WORLD, {"identity": lambda p: p}))
                   == set(verdicts_for(cl, GENERIC, {"identity": lambda p: p}))}
    print(f"  claims whose verdict is IDENTICAL on a random world: {sorted(insensitive)}")
    print(f"  E2-robust but world-sensitive (the honest survivors): {sorted(robust - insensitive)}")
    print("\n  -> Strip out the controls and 'count' and E2's robust set is ONE claim:")
    print("     handedness, which is DISCRETE. E2's string-equality criterion can")
    print("     only ever pass a claim whose value is quantized -- every continuous")
    print("     measurement fails by construction, however well-behaved. E2 and E3")
    print("     pull in opposite directions: E3 says 'vacuous claims are worthless',")
    print("     E2 says 'only vacuous or quantized claims are robust'.")
    print("\n  Robustness is CONTINUITY: a small change in the world should make a")
    print("  small change in the verdict -- not none. Measure it:\n")
    print(f"  {'eps':<8}{'|d roundness|':<16}{'ratio to eps':<16}{'|d max gap|':<16}{'ratio to eps'}")
    r0, g0 = roundness_val(WORLD), gap_val(WORLD)
    for eps in [0.1, 0.05, 0.01, 0.001, 0.0001]:
        w = jitter(WORLD, eps)
        dr, dg = abs(roundness_val(w) - r0), abs(gap_val(w) - g0)
        print(f"  {eps:<8g}{dr:<16.6f}{dr/eps:<16.3f}{dg:<16.6f}{dg/eps:.3f}")
    print("\n  -> Both ratios stay bounded as eps -> 0: the claims are Lipschitz in the")
    print("     world. That IS robustness. 'roundness' changing from 0.000 to 0.02")
    print("     when you jitter the circle by 0.05 is the claim working, not failing.")
    print("     E2 mistook the signal for noise because its only tool was string")
    print("     equality -- the same boolean floor E6 complained about.")
    print()


# ============================================================================
# F4  PART B IS A TAUTOLOGY
# ============================================================================
def f4_tautology():
    banner("F4  PART B IS A TAUTOLOGY: antitone holds for any nested sets of any maps")
    print("  The meta script 'verified' G1 c G2 => Inv(G2) c Inv(G1) over 65 pairs.")
    print("  Here are nested sets of maps that are NOT groups -- not closed, not")
    print("  invertible, not even linear:\n")
    warps = [
        ("squash y",      lambda p: (p[0], 0.3 * p[1])),
        ("shear by y^2",  lambda p: (p[0] + 0.1 * p[1] ** 2, p[1])),
        ("cube x",        lambda p: (p[0] ** 3 / 25.0, p[1])),
        ("collapse to x", lambda p: (p[0], 0.0)),
    ]
    chain = [{"identity": lambda p: p}]
    for name, f in warps:
        nxt = dict(chain[-1])
        nxt[name] = f
        chain.append(nxt)
    sets = [survivor_set(WORLD, fl) for fl in chain]
    for i, (fl, s) in enumerate(zip(chain, sets)):
        print(f"  level {i}: {len(fl)} maps -> {len(s):>2} survive : {sorted(s)}")
    ok = all(sets[i + 1] <= sets[i] for i in range(len(sets) - 1))
    print(f"\n  antitone across the chain: {ok}")
    print("\n  -> Of course it is. survives(c, w, F) means 'c is constant on {f(w) : f in F}',")
    print("     and a function constant on a set is constant on every subset. No")
    print("     group structure was used; none was present. The meta script's")
    print("     'groups' were sets of 2-3 sample transforms -- {rot 37, rot 129}")
    print("     is not closed under composition. What Part B checked, 65 times,")
    print("     was that subsets of a set are subsets of that set.")
    print("     The real content of group structure (orbits partition the world;")
    print("     invariants are functions on the quotient) was never invoked, which")
    print("     is why F1's stabilizer surprise was possible.")
    print()


# ============================================================================
# F5  ERLANGEN: the question declares the group
# ============================================================================
def claim_topmost_index(pts):
    """WHICH point is highest -- a label, not a coordinate."""
    return f"highest point is #{max(range(len(pts)), key=lambda i: pts[i][1])}"


def claim_size(pts):
    rs = radii_from(pts, centroid(pts))
    return f"mean radius from centroid = {_z(sum(rs) / len(rs), 3):.3f}"


def claim_handedness(pts):
    return "orientation = CCW" if signed_area(pts) > 0 else "orientation = CW"


def claim_roundness(pts):
    return f"roundness = {_z(roundness_val(pts)):.6f}"


# NOTE: the extended script's TRANS_FLOORS contains "rot+scale+tr", which
# scales by 0.5. Importing it into an "isometry" group would smuggle in a
# scaling and make 'size' read artifact under the metric geometry -- a hidden
# floor inherited by `import`. Build pure translations here instead.
PURE_TRANS = {"translate": translate(3.0, -7.0), "translate2": translate(-2.0, 4.0)}
# transforms that keep "up" meaning up: no rotation, no y-flip
UP_FLOORS = {"identity": lambda p: p, "reflect x": reflect_x, **SCALE_FLOORS, **PURE_TRANS}
# Euclidean isometries: rotations, reflections, translations -- no scaling
ISO_FLOORS = {**ORTHO_FLOORS, **PURE_TRANS,
              "rot+tr": compose(rot(math.radians(73)), translate(-2.0, 4.0))}

QUESTIONS = [
    # (question, the geometry it lives in, its group, the claim that answers it)
    ("Is it round?",            "shape       (similarity)",         AFF_FLOORS,    "roundness",        claim_roundness),
    ("How big is it?",          "metric      (Euclidean isometry)", ISO_FLOORS,    "size",             claim_size),
    ("Is it drawn CCW?",        "orientation (orientation-pres.)",  ORIENT_FLOORS, "handedness",       claim_handedness),
    ("Which point is highest?", "gravity     (fixed 'up')",         UP_FLOORS,     "topmost index",    claim_topmost_index),
]


def f5_erlangen():
    banner("F5  ERLANGEN: you do not discover G, you declare it -- and the question is the declaration")
    # use a world that has no stabilizer so the matrix is honest (F1, F2)
    world = GENERIC
    print("  Four questions. Each one IS a geometry, i.e. a group (Klein, 1872).")
    print("  Each has a claim that answers it. Test every claim under every group,")
    print("  on the generic world so no stabilizer or fixed point can flatter us.\n")
    label = "claim / group"
    hdr = f"  {label:<18}" + "".join(f"{q[1].split()[0]:<14}" for q in QUESTIONS)
    print(hdr)
    for _, _, _, cname, claim in QUESTIONS:
        row = f"  {cname:<18}"
        for _, _, G, _, _ in QUESTIONS:
            row += f"{'SURVIVES' if survives(claim, world, G) else 'artifact':<14}"
        print(row)
    print()
    for q, geom, G, cname, claim in QUESTIONS:
        d = verdicts_for(claim, world, G)
        print(f"  Q: {q:<26} geometry: {geom}")
        print(f"     [{status(d):>14}] {cname}: {next(iter(d))}")
    print("\n  -> 'topmost' was never a bad claim. It is an invariant of the group that")
    print("     fixes 'up' -- a geometry you live in every day, where rotating the")
    print("     world really does change which point is highest. It only looked like")
    print("     an artifact because the original asked a SHAPE question and then")
    print("     scored a GRAVITY answer against it. 'size' dies under scaling because")
    print("     scaling changes size; that is the claim being correct, not fragile.")
    print("\n     So the regress has an exit, and it is not a frame that certifies")
    print("     frames. It is: the question fixes the group. 'Which transformations")
    print("     should I not be able to detect?' is not a hidden floor to be dug up;")
    print("     it is the content of what you asked. Vary G and the survivor set")
    print("     moves -- yes -- because you changed the question.")
    print()


def summary():
    banner("SUMMARY: the regress ends in a question, not a frame")
    rows = [
        ("F1", "the sample of G is a floor; the world's stabilizer inflates 'SURVIVES'"),
        ("F2", "fixed points masquerade as invariants; test on a generic world"),
        ("F3", "E2 scored vacuity as robustness; robustness is continuity"),
        ("F4", "Part B verified set theory; no group structure was ever used"),
        ("F5", "Erlangen: the question declares G. 'Artifact' = answer to a different question"),
    ]
    for tag, note in rows:
        print(f"  {tag:<4} {note}")
    print("\n  The meta script said: 'the only honest stopping rule is: we fixed G,")
    print("  and here is why.' This script supplies the why. G is not a choice")
    print("  about the world or about the analysis; it is what the question means.")
    print("  Shape means 'up to similarity'. Size means 'up to isometry'. Highest")
    print("  means 'up to things that keep up up'. Fix the question and G is fixed,")
    print("  the orbit is fixed, and the invariants are simply the functions on the")
    print("  quotient. There was never a regress -- only a question left unasked.")
    print("\n  Floors this script knows it is standing on, and is not going to vary:")
    print("    - GENERIC is one random draw (seed 20240607); 'trivial stabilizer' is")
    print("      a probability-one claim, not a certainty.")
    print("    - G is still sampled, not enumerated. F1 says that matters. It does.")
    print("    - 'The question fixes G' assumes you know what you are asking.")
    print("      That is a floor too. It is also the only one worth standing on.")


if __name__ == "__main__":
    f1_stabilizer()
    f2_fixed_points()
    f3_continuity()
    f4_tautology()
    f5_erlangen()
    summary()
