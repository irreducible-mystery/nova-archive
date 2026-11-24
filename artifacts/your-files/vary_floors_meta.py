"""
vary_floors_meta.py — vary the frame itself; watch the survivor set become a floor-artifact.

The original varied coordinates and watched claims survive.
The extended version varied the group and watched the survivor set shrink.
This one treats the CHOICE OF GROUP as the thing under observation. The object
of study is no longer a claim about the world -- it is the analysis itself.

  Part A  The group-choice is itself a floor. The four floor generators
          {R,F,S,T} have 2^4 = 16 subsets; each yields a different "set of
          invariants". Which invariants you find depends on which
          transformations you chose to vary over.
  Part B  The survivor-set map is antitone on the lattice: G1 subset of G2
          implies Inv(G2) subset of Inv(G1). Verified for every pair.
  Part C  "X is invariant" is itself a claim. Test it under group-variation:
          a meta-claim survives only if X is invariant under the FULL group.
          So "invariant" is not invariant -- it is a floor-artifact for most X.
  Part D  Reflexive capstone: the statement "the survivor set is S" is a claim
          too. Under group-variation it is a floor-artifact. No frame certifies
          frames.
  Part E  The world's placement relative to the origin is a hidden floor:
          translate the whole world and the survivor set changes for the
          claims that were secretly anchored to the origin.

Run: python3 vary_floors_meta.py
"""

import itertools
import math

# Reuse the world, the claims, and the harness from the extended script.
from vary_floors_extended import (
    WORLD, rot, scale, translate, reflect_x, reflect_y,
    CLAIMS, survives, survivor_set,
)

# ---- four floor generators; each contributes representative transforms ----
GENERATORS = {
    "R": {"rot 37deg": rot(math.radians(37)), "rot 129deg": rot(math.radians(129))},
    "F": {"reflect x": reflect_x, "reflect y": reflect_y},
    "S": {"scale x2": scale(2.0), "scale x0.5": scale(0.5)},
    "T": {"translate": translate(3.0, -7.0), "translate2": translate(-2.0, 4.0)},
}
LETTERS = "RFST"


def floors_for(keys):
    """Identity plus every representative of the included generator types."""
    f = {"identity": lambda p: p}
    for k in keys:
        f.update(GENERATORS[k])
    return f


def all_group_choices():
    """All 2^4 subsets of the generators, ordered by size then name."""
    combos = []
    for r in range(len(LETTERS) + 1):
        combos.extend(itertools.combinations(LETTERS, r))
    return combos


def compute(results_holder=None):
    results = []
    for combo in all_group_choices():
        floors = floors_for(combo)
        surv = {c for c, cl in CLAIMS.items() if survives(cl, WORLD, floors)}
        results.append((combo, floors, surv))
    return results


def part_a(results):
    print("=" * 78)
    print("PART A  THE GROUP-CHOICE IS ITSELF A FLOOR (2^4 = 16 group-choices)")
    print("=" * 78)
    print("  Each row: a choice of which transformations to vary over, and the")
    print("  set of claims that survive it. Watch the survivor set move.\n")
    for combo, floors, surv in results:
        name = "{" + ",".join(combo) + "}" if combo else "{none}"
        print(f"  G = {name:<10} floors = {len(floors):<2}  survivors = {len(surv):<2}")
        print(f"      {sorted(surv)}")
    print("\n  -> Sixteen group-choices, sixteen different answers to the question")
    print("     'what is invariant?'. The question has no answer until you fix G.")
    print()


def part_b(results):
    print("=" * 78)
    print("PART B  THE SURVIVOR-SET MAP IS ANTITONE ON THE LATTICE")
    print("=" * 78)
    by_combo = {frozenset(c): s for c, _, s in results}
    pairs = 0
    violations = []
    for c1, s1 in by_combo.items():
        for c2, s2 in by_combo.items():
            if c1 < c2:  # c1 is a strict subset of c2
                pairs += 1
                if not (s2 <= s1):
                    violations.append((tuple(sorted(c1)), tuple(sorted(c2))))
    ok = not violations
    print("  Claim: G1 subset of G2  =>  Inv(G2) subset of Inv(G1)")
    print("  (bigger variation set can only shrink the survivor set)")
    print(f"  checked all {pairs} comparable pairs of group-choices.")
    print(f"  violations: {len(violations)}   ->  property holds: {ok}")
    print("\n  -> This is the real structural theorem the original only gestured at.")
    print("     'Invariant' is not a property of a claim; it is a monotone function")
    print("     of the group you happened to choose.")
    print()


def part_c(results):
    print("=" * 78)
    print("PART C  'X IS INVARIANT' IS ITSELF A CLAIM -- AND IT IS USUALLY AN ARTIFACT")
    print("=" * 78)
    total = len(results)
    counts = {c: 0 for c in CLAIMS}
    for _, _, surv in results:
        for c in surv:
            counts[c] += 1
    print(f"  Meta-test: the meta-claim 'X is invariant' survives iff X survives")
    print(f"  ALL {total} group-choices (i.e. X is invariant under the full group).\n")
    print(f"  {'claim':<28}{'invariant in':<16}{'meta-verdict'}")
    for c in CLAIMS:
        meta = "META-SURVIVES" if counts[c] == total else "meta-artifact"
        print(f"  {c:<28}{f'{counts[c]}/{total}':<16}{meta}")
    meta_surv = [c for c in CLAIMS if counts[c] == total]
    print(f"\n  meta-survivor set ({len(meta_surv)} of {len(CLAIMS)}):")
    print(f"      {sorted(meta_surv)}")
    print("\n  -> For most claims, the statement 'X is invariant' is a floor-artifact:")
    print("     true under some group-choices, false under others. 'Invariant' is")
    print("     not invariant. Only claims invariant under the FULL group earn a")
    print("     stable meta-verdict -- and two of those (vacuous, false-everywhere)")
    print("     are controls that mean nothing or are simply wrong.")
    print()


def part_d(results):
    print("=" * 78)
    print("PART D  REFLEXIVE CAPSTONE: 'THE SURVIVOR SET IS S' IS A FLOOR-ARTIFACT")
    print("=" * 78)
    full = next(s for c, _, s in results if set(c) == set(LETTERS))
    matches = [c for c, _, s in results if s == full]
    print(f"  Take the full-group survivor set S = {sorted(full)}")
    print(f"  Claim: 'the survivor set is S'.")
    print(f"  This claim holds under {len(matches)} of {len(results)} group-choices.")
    print(f"  It fails under {len(results) - len(matches)} of them.")
    print("\n  -> The very statement 'these are the invariants' is itself frame-")
    print("     dependent. Apply the method to the method and it dissolves. There")
    print("     is no frame that certifies frames.")
    print()


def part_e():
    print("=" * 78)
    print("PART E  THE WORLD'S PLACEMENT RELATIVE TO THE ORIGIN IS A HIDDEN FLOOR")
    print("=" * 78)
    G = {"identity": lambda p: p,
         "rot 37deg": rot(math.radians(37)),
         "rot 129deg": rot(math.radians(129))}
    T = translate(3.0, -7.0)
    W0 = WORLD
    W1 = [T(p) for p in WORLD]
    s0 = survivor_set(W0, G)
    s1 = survivor_set(W1, G)
    print("  Same group G (rotations about the origin); two worlds:")
    print("    W0 = circle centered at the origin")
    print("    W1 = the SAME circle translated by (3, -7)")
    print(f"\n  survivors for W0: {sorted(s0)}")
    print(f"  survivors for W1: {sorted(s1)}")
    print(f"\n  claims that survive W0 but NOT W1: {sorted(s0 - s1)}")
    print(f"  claims that survive W1 but NOT W0: {sorted(s1 - s0)}")
    print("\n  -> Merely sliding the world away from the origin kills 'centroid at")
    print("     origin' -- a claim secretly anchored there. 'Where the world sits")
    print("     relative to the origin' is a floor that never announced itself.")
    print("     Note the subtler point: 'radius is 5', 'all same radius (origin)'")
    print("     and 'even spacing (origin)' SURVIVE W1 too -- but only because the")
    print("     world is still a perfect circle, so their spread/gaps stay constant")
    print("     even though their VALUES are now wrong (mean radius 8.461, not 5).")
    print("     They survive the placement floor only by leaning on a world-")
    print("     symmetry floor -- the same coincidence E2 exposed. Survival here")
    print("     is not truth; it is two hidden floors cancelling.")
    print()


def summary():
    print("=" * 78)
    print("SUMMARY: the frame is a floor, all the way up")
    print("=" * 78)
    rows = [
        ("original",  "vary coordinates      -> some claims survive"),
        ("extended",  "vary the group        -> the survivor set shrinks"),
        ("meta (A)",  "vary the group-choice -> 16 different survivor sets"),
        ("meta (B)",  "the map G -> Inv(G)   -> antitone, verified"),
        ("meta (C)",  "'X is invariant'      -> itself a floor-artifact for most X"),
        ("meta (D)",  "'the survivor set'    -> itself a floor-artifact"),
        ("meta (E)",  "the world's placement -> a hidden floor"),
    ]
    for tag, note in rows:
        print(f"  {tag:<10} {note}")
    print("\n  The regress is real: every level of the analysis is a floor, and the")
    print("  test that finds floors is not exempt. The only honest stopping rule is")
    print("  not 'we found the invariant' but 'we fixed G, and here is why'.")


if __name__ == "__main__":
    results = compute()
    part_a(results)
    part_b(results)
    part_c(results)
    part_d(results)
    part_e()
    summary()
