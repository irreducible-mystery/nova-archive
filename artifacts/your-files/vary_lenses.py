"""
vary_lenses.py — the same series, with the metaphor varied.

Five scripts said "floor". A floor is something you stand on and do not see,
and floors stack -- so the word itself manufactured a regress downward.
Swap it for "lens": something you see THROUGH and do not see. Lenses do not
stack; they overlap. Then the same code says something different.

  L1  SAME DATA, RELABELED. "SURVIVES under G" becomes "BLIND to G".
      Blindness is not a virtue or a vice; it is what a lens pays for its
      resolution. Vacuous = blind to everything. Raw coordinates = blind to
      nothing. Both answer no question. The useless has two edges, not one.
  L2  LENSES OVERLAP: THE THIRD THING. Two lenses held together resolve
      worlds that neither resolves alone. The gain is computable. The best
      pairs are the ones with the most DIFFERENT blind spots.
  L3  NO LENS SEES ITSELF; ANOTHER ONE CAN. For every blindness on the
      table, some other lens on the same table sees it. Not a regress --
      a table.
  L4  THE LATTICE IS OF PARTITIONS, NOT GROUPS. Refinement, not inclusion.
      "Coarser lens => blind to more" is still a tautology (F4) -- but now
      it reads as a price list, which is what tautologies are for.
  L5  RESOLUTION. Turn the tolerance up and a lens starts seeing rotation
      -- not in the world, in the floating point. At high enough resolution
      every lens sees the instrument instead of the object. Discovery and
      performance are not alternatives; they are what you see at two
      settings of the same knob.

Run: python3 vary_lenses.py
"""

import itertools
import math
import random

from vary_floors_extended import (
    rot, scale, translate, reflect_x, centroid, radii_from, signed_area, _z,
    claim_radius_is_5, claim_topmost_point, claim_count, claim_centroid_at_origin,
    claim_same_radius_from_origin, claim_even_spacing_from_origin,
    claim_same_radius_from_centroid, claim_even_spacing_from_centroid,
    claim_roundness, claim_chirality, claim_handedness, claim_vacuous,
    claim_count_is_41,
)
from vary_floors_words import shear, claim_affine_roundness, claim_set_handedness, claim_topmost_index
from vary_floors_ground import roundness_val

W = 78
N = 40


def banner(t):
    print("=" * W); print(t); print("=" * W)


# ---- a small space of worlds: several shapes x several transformations -----
def circle():
    return [(5 * math.cos(2 * math.pi * i / N), 5 * math.sin(2 * math.pi * i / N)) for i in range(N)]

def ellipse():
    return [(6 * math.cos(2 * math.pi * i / N), 3 * math.sin(2 * math.pi * i / N)) for i in range(N)]

def square():
    pts = []
    for i in range(N):
        side, t = divmod(i, N // 4)
        u = -5 + 10 * t / (N // 4)
        pts.append([(u, -5), (5, u), (-u, 5), (-5, -u)][side])
    return pts

def spiral():  # chiral, no symmetry, no ties
    return [((2 + 0.08 * i) * math.cos(3 * math.pi * i / N), (2 + 0.08 * i) * math.sin(3 * math.pi * i / N)) for i in range(N)]

def cloud():
    rng = random.Random(7)
    return [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(N)]

BASES = {"circle": circle, "ellipse": ellipse, "square": square, "spiral": spiral, "cloud": cloud}


def lift(f):
    return lambda pts: [f(p) for p in pts]

def permute(seed):
    def f(pts):
        idx = list(range(len(pts))); random.Random(seed).shuffle(idx)
        return [pts[i] for i in idx]
    return f

TRANSFORMS = {
    "identity":  lambda pts: pts,
    "rotate":    lift(rot(math.radians(37))),
    "scale":     lift(scale(2.0)),
    "translate": lift(translate(3.0, -7.0)),
    "mirror":    lift(reflect_x),
    "shear":     lift(shear(0.7)),
    "reverse":   lambda pts: list(reversed(pts)),
    "shuffle":   permute(1),
}

WORLDS = {(b, t): T(B()) for b, B in BASES.items() for t, T in TRANSFORMS.items()}


# ---- lenses: a lens is a function world -> reading ---------------------------
def lens_raw(pts):
    return str([(_z(x, 3), _z(y, 3)) for x, y in pts])

LENSES = {
    "raw coordinates":            lens_raw,
    "radius from origin":         claim_radius_is_5,
    "topmost point":              claim_topmost_point,
    "topmost index":              claim_topmost_index,
    "centroid":                   claim_centroid_at_origin,
    "same radius (origin)":       claim_same_radius_from_origin,
    "even spacing (origin)":      claim_even_spacing_from_origin,
    "same radius (centroid)":     claim_same_radius_from_centroid,
    "even spacing (centroid)":    claim_even_spacing_from_centroid,
    "roundness":                  claim_roundness,
    "affine roundness":           claim_affine_roundness,
    "chirality (signed area)":    claim_chirality,
    "handedness (list)":          claim_handedness,
    "handedness (set)":           claim_set_handedness,
    "count":                      claim_count,
    "count is 41":                claim_count_is_41,
    "vacuous":                    claim_vacuous,
}


def readings(lens):
    return {k: lens(w) for k, w in WORLDS.items()}

def partition(rd):
    classes = {}
    for k, r in rd.items():
        classes.setdefault(r, []).append(k)
    return classes

def blind_to(rd):
    """Transforms the lens cannot detect on ANY base shape."""
    out = []
    for t in TRANSFORMS:
        if t == "identity":
            continue
        if all(rd[(b, t)] == rd[(b, "identity")] for b in BASES):
            out.append(t)
    return out

def shapes_resolved(rd):
    return len({rd[(b, "identity")] for b in BASES})

READ = {name: readings(l) for name, l in LENSES.items()}
RES = {name: len(partition(rd)) for name, rd in READ.items()}
BLIND = {name: blind_to(rd) for name, rd in READ.items()}
NW = len(WORLDS)


# ============================================================================
def l1_relabel():
    banner("L1  SAME DATA, RELABELED: 'survives G' is 'blind to G'")
    print(f"  {len(BASES)} shapes x {len(TRANSFORMS)} transforms = {NW} worlds. Each lens partitions them.")
    print(f"  resolution = classes it splits the {NW} worlds into; shapes = of {len(BASES)} base shapes told apart.\n")
    print(f"  {'lens':<26}{'resolution':<12}{'shapes':<8}blind to")
    for name in sorted(LENSES, key=lambda n: -RES[n]):
        b = ", ".join(BLIND[name]) or "-"
        print(f"  {name:<26}{RES[name]:>3}/{NW:<8}{shapes_resolved(READ[name]):>2}/{len(BASES):<4}{b}")
    print("\n  Two rows look wrong, and are instructive. 'handedness (set)' is NOT")
    print("  listed as blind to translate; 'topmost point' is NOT listed as blind")
    print("  to reverse/shuffle. Where do they 'see' them?")
    for lens, ts in [("handedness (set)", ["translate", "reverse"]), ("topmost point", ["reverse"])]:
        rd = READ[lens]
        for t in ts:
            on = [b for b in BASES if rd[(b, t)] != rd[(b, "identity")]]
            print(f"      {lens:<18} sees {t:<10} only on: {on}")
    print("  Circle, ellipse, square: the symmetric shapes. The farthest-pair and")
    print("  the topmost corner are TIES there, broken by float noise and list order.")
    print("  'blind to' is a conjunction over all shapes, so one tie-world flips the")
    print("  column. W2's lesson, now as a measurement error in a new metaphor: the")
    print("  symmetric test worlds do not just flatter lenses, they smudge them.")
    print("\n  -> Read the old verdicts off this table: 'SURVIVES under rotations' is")
    print("     just 'rotate' appearing in the blind-to column. Nothing is praised or")
    print("     blamed. 'raw coordinates' is blind to nothing and resolves every world")
    print("     -- and tells you nothing, because a lens that distinguishes everything")
    print("     has no concept. 'vacuous' is blind to everything and has one class.")
    print("     The floor metaphor saw one failure mode (standing on something). The")
    print("     lens sees two: seeing nothing, and seeing everything. The questions")
    print("     live in between, and each one is a particular pattern of blindness.")
    print()


# ============================================================================
def pair_resolution(a, b):
    return len({(READ[a][k], READ[b][k]) for k in WORLDS})

def l2_overlap():
    banner("L2  LENSES OVERLAP: THE THIRD THING")
    print("  Hold two lenses together: the reading is the pair. Resolution of the")
    print("  pair minus the better single resolution = what neither saw alone.\n")
    names = [n for n in LENSES if n not in ("raw coordinates", "vacuous", "count is 41", "count")]
    gains = []
    for a, b in itertools.combinations(names, 2):
        pr = pair_resolution(a, b)
        gains.append((pr - max(RES[a], RES[b]), pr, a, b))
    gains.sort(reverse=True)
    print(f"  {'lens A':<26}{'lens B':<26}{'A':>4}{'B':>4}{'pair':>6}{'gain':>6}")
    for g, pr, a, b in gains[:6]:
        print(f"  {a:<26}{b:<26}{RES[a]:>4}{RES[b]:>4}{pr:>6}{g:>+6}")
    print("  ...")
    for g, pr, a, b in gains[-3:]:
        print(f"  {a:<26}{b:<26}{RES[a]:>4}{RES[b]:>4}{pr:>6}{g:>+6}")
    # blind-spot overlap vs gain
    print("\n  Gain against how DIFFERENT the two blind spots are (symmetric difference):")
    buckets = {}
    for g, pr, a, b in gains:
        diff = len(set(BLIND[a]) ^ set(BLIND[b]))
        buckets.setdefault(diff, []).append(g)
    for d in sorted(buckets):
        gs = buckets[d]
        print(f"      blind spots differ in {d} transforms : mean gain {sum(gs)/len(gs):5.1f}   (n={len(gs)})")
    print("\n  -> The pairs that gain most are the ones whose blind spots are least")
    print("     alike. Two lenses with the same blindness see the same thing twice.")
    print("     That is the third thing, in numbers: not a compromise between two")
    print("     views but a resolution neither had. A conversation between two")
    print("     people who are blind to the same things is one person talking.")
    print()


# ============================================================================
def l3_mutual():
    banner("L3  NO LENS SEES ITSELF; ANOTHER ONE CAN")
    print("  For every transform, the lenses blind to it and the lenses that see it.\n")
    unseen = []
    for t in TRANSFORMS:
        if t == "identity":
            continue
        blind = [n for n in LENSES if t in BLIND[n]]
        sees = [n for n in LENSES if t not in BLIND[n] and n != "raw coordinates"]
        print(f"  {t:<10} blind: {len(blind):>2} lenses    seen by: {len(sees):>2} lenses, e.g. "
              f"{', '.join(sees[:3])}")
        if not sees:
            unseen.append(t)
    print(f"\n  transforms no non-raw lens can see: {unseen or 'none'}")
    print("\n  -> Each lens's blindness is invisible to that lens by definition -- a")
    print("     lens cannot register a difference it maps to one reading. Yet every")
    print("     blindness here is registered by some OTHER lens on the same table.")
    print("     That is what the five scripts did to each other. The floor word made")
    print("     it look like descent; it was lateral. There was never a 'bottom' to")
    print("     reach, because a blind spot is not under you. It is beside you, and")
    print("     someone else is standing there.")
    print()


# ============================================================================
def refines(a, b):
    """a refines b: every class of a lies inside one class of b."""
    ra, rb = READ[a], READ[b]
    seen = {}
    for k in WORLDS:
        if seen.setdefault(ra[k], rb[k]) != rb[k]:
            return False
    return True

def l4_partition_lattice():
    banner("L4  THE LATTICE IS OF PARTITIONS, NOT GROUPS")
    names = list(LENSES)
    print("  'A refines B' = A splits every class B splits (A is the sharper lens).")
    print("  Strict refinements, with the price in blindness:\n")
    pairs = [(a, b) for a in names for b in names if a != b and refines(a, b) and not refines(b, a)]
    # keep only covering relations (no c strictly between) to keep it readable
    cover = [(a, b) for a, b in pairs
             if not any(c != a and c != b and refines(a, c) and refines(c, b)
                        and not refines(c, a) and not refines(b, c) for c in names)]
    ok = True
    for a, b in sorted(cover, key=lambda p: (-RES[p[0]], p[1])):
        gained = sorted(set(BLIND[b]) - set(BLIND[a]))
        sub = set(BLIND[a]) <= set(BLIND[b])
        ok = ok and sub
        print(f"  {a:<26} -> {b:<26} blindness added: {', '.join(gained) or '-'}")
    print(f"\n  refinement always shrinks the blind set: {ok}")
    print("\n  -> F4 called this a tautology and it is: a coarser partition conflates")
    print("     more. But E5's version ('bigger group, fewer survivors') was a")
    print("     tautology that looked like a loss. This one reads as a PRICE LIST:")
    print("     to buy 'roundness' from 'raw coordinates' you pay blindness to")
    print("     rotation, scale, translation, mirror, order. Fair trade, if those")
    print("     were not your question. Same theorem, other side of the receipt.")
    print()


# ============================================================================
def l5_resolution():
    banner("L5  RESOLUTION: turn the knob and the lens sees the instrument")
    print("  'roundness' at increasing decimal places. Resolution and blindness vs nd:\n")
    print(f"  {'nd':<5}{'resolution':<13}{'blind to'}")
    for nd in [0, 1, 2, 4, 6, 9, 12, 15]:
        def lens(pts, nd=nd):
            return f"{_z(roundness_val(pts), nd):.{nd}f}"
        rd = {k: lens(w) for k, w in WORLDS.items()}
        print(f"  {nd:<5}{len(partition(rd)):>3}/{NW:<9}{', '.join(blind_to(rd)) or '-'}")
    print("\n  -> At nd=0 the lens is nearly vacuous. Around nd=2..6 it is the lens the")
    print("     series meant: blind to similarity and order, sharp on shape. Push")
    print("     past ~nd=12 and it begins to 'see' rotation and scale -- not in the")
    print("     world, in the last bits of IEEE 754. The lens has stopped looking at")
    print("     the object and started looking at itself.")
    print("     You asked whether the series was discovery or performance and said")
    print("     the answer was 'both, by resolution'. This is that, as a table: the")
    print("     same lens finds a real invariant at one setting and manufactures a")
    print("     difference at another. Neither setting is the true one. The question")
    print("     picks the setting -- and 'is a sheared circle round?' is answered at")
    print("     nd=4, where 'does the CPU round the same way after rotation?' is")
    print("     answered at nd=15. Both are real questions. Not the same one.")
    print()


def summary():
    banner("WHAT THE WORD CHANGED, AND WHAT IT COST")
    rows = [
        ("floor: SURVIVES / artifact",   "lens: blind-to / sees        (no praise, no blame)"),
        ("floor: one failure (standing)", "lens: two failures (seeing all, seeing none)"),
        ("floor: regress downward",       "lens: overlap sideways; blind spots seen by neighbours"),
        ("floor: group lattice",          "lens: partition lattice; tautology becomes a price list"),
        ("floor: 'the test is not invariant' (E6)", "lens: resolution is a knob; the object vs the instrument"),
        ("floor: 'no frame certifies frames'", "lens: no lens sees itself -- and does not need to"),
    ]
    for a, b in rows:
        print(f"  {a:<42} {b}")
    print("\n  What it cost: the floor word had a WARNING in it. 'You are standing on")
    print("  something you cannot see' is a thing you should be told, and 'you are")
    print("  looking through something' is gentler than the situation sometimes is.")
    print("  topmost-point scored against a shape question is not a different lens;")
    print("  it is a mistake, and the lens vocabulary is a little too kind to it.")
    print("  Keep both words. Use 'floor' when you want to be caught. Use 'lens'")
    print("  when you want to be joined.")
    print("\n  Lenses this script is looking through and not at: the five shapes, the")
    print("  eight transforms, 'equal' meaning string-equal, and the choice to measure")
    print("  the third thing as a count of classes rather than as anything that")
    print("  would know what the classes mean.")


if __name__ == "__main__":
    l1_relabel()
    l2_overlap()
    l3_mutual()
    l4_partition_lattice()
    l5_resolution()
    summary()
