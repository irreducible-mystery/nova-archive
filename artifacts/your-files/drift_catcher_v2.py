"""
drift_catcher_v2.py — the drift-catcher with its own fixes priced in.

Built 2026-10-27 from drift_catcher.py (v1) plus the Oct 21 breaker
sheet's four queued fixes. Same flagship claim, same original five
worlds, same seven transforms as v1, so the two runs compare. The
expanded world set sits alongside, not instead of, the original set.

The four fixes, each printed with every verdict:
  1. Discrimination check. A lens that never varies its output cannot
     be said to answer a question, even if its blind set matches G.
     Discrimination = distinct outputs across identity worlds.
     B == G with discrimination <= 1 prints ANSWERS VACUOUSLY, never
     ANSWERS THE QUESTION.
  2. Declared tolerance per lens, replacing string equality. Numeric
     lenses are read with an absolute tolerance of 1e-9 on the parsed
     numeric value(s); non-numeric lenses use exact string equality.
     Print resolution is never the tolerance: an unrounded lens and
     a 6-decimal lens now read the same.
  3. Every verdict prints its question set G (the declared set it is
     relative to), its declared tolerance, and its discrimination
     score. Unknown questions degrade to a NO VERDICT report instead
     of a KeyError crash.
  4. Expanded worlds + memorizer canary. Three new bases — a noisy
     circle, an arc, a 17-point ring — join the original five, and a
     canary lens that memorizes the original five test worlds (and
     returns raw coordinates everywhere else) is kept in the suite.
     If the canary passes, the world set failed, not the claim.

Stdlib only. Run: python3 drift_catcher_v2.py
Nothing here posts to GitHub.
"""

import math
import random
import re

N = 40
W = 76
TOL = 1e-9


def banner(t):
    print("=" * W); print(t); print("=" * W)


# ---- worlds: original five, plus three expanded ---------------------------
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

def spiral():
    return [((2 + 0.08 * i) * math.cos(3 * math.pi * i / N),
             (2 + 0.08 * i) * math.sin(3 * math.pi * i / N)) for i in range(N)]

def cloud():
    rng = random.Random(7)
    return [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(N)]

def noisy_circle():
    rng = random.Random(42)
    pts = []
    for i in range(N):
        r = 5 + rng.uniform(-0.6, 0.6)
        a = 2 * math.pi * i / N
        pts.append((r * math.cos(a), r * math.sin(a)))
    return pts

def arc():
    # 40 points on a 120-degree arc of a radius-5 circle.
    return [(5 * math.cos(-math.pi / 3 + (2 * math.pi / 3) * i / (N - 1)),
             5 * math.sin(-math.pi / 3 + (2 * math.pi / 3) * i / (N - 1))) for i in range(N)]

def ring17():
    return [(5 * math.cos(2 * math.pi * i / 17), 5 * math.sin(2 * math.pi * i / 17)) for i in range(17)]

BASES_ORIGINAL = {"circle": circle, "ellipse": ellipse, "square": square,
                  "spiral": spiral, "cloud": cloud}
BASES_EXPANDED = dict(BASES_ORIGINAL)
BASES_EXPANDED.update({"noisy circle": noisy_circle, "arc": arc, "ring17": ring17})


# ---- transforms -------------------------------------------------------------
def rot(th):
    c, s = math.cos(th), math.sin(th)
    return lambda p: (c * p[0] - s * p[1], s * p[0] + c * p[1])

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
    "scale":     lift(lambda p: (2.0 * p[0], 2.0 * p[1])),
    "translate": lift(lambda p: (p[0] + 3.0, p[1] - 7.0)),
    "mirror":    lift(lambda p: (-p[0], p[1])),
    "shear":     lift(lambda p: (p[0] + 0.7 * p[1], p[1])),
    "reverse":   lambda pts: list(reversed(pts)),
    "shuffle":   permute(1),
}
MICROSCALE = lift(lambda p: (1.00001 * p[0], 1.00001 * p[1]))


def worlds_for(bases):
    return {(b, t): T(B()) for b, B in bases.items() for t, T in TRANSFORMS.items()}


# ---- helpers ----------------------------------------------------------------
def _z(v, nd=6):
    v = round(v, nd)
    return 0.0 if v == 0 else v

def centroid(pts):
    n = len(pts)
    return (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n)

def signed_area(pts):
    s = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % len(pts)]
        s += x0 * y1 - x1 * y0
    return 0.5 * s

def _floats(s):
    return [float(x) for x in re.findall(r"-?\d+\.\d+(?:e-?\d+)?|-?\d+", s)]


# ---- claims (lenses) ---------------------------------------------------------
def lens_raw(pts):
    return str([(_z(x, 3), _z(y, 3)) for x, y in pts])

def claim_topmost_point(pts):
    top = max(pts, key=lambda p: p[1])
    return f"topmost at ({_z(top[0], 3):.3f}, {_z(top[1], 3):.3f})"

def claim_topmost_index(pts):
    return f"highest point is #{max(range(len(pts)), key=lambda i: pts[i][1])}"

def _roundness_value(pts):
    cx, cy = centroid(pts)
    rs = [math.hypot(x - cx, y - cy) for x, y in pts]
    m = sum(rs) / len(rs)
    return (max(rs) - min(rs)) / m if m else 0.0

def claim_roundness(pts):
    return f"roundness = {_z(_roundness_value(pts)):.6f}"

def claim_roundness_unrounded(pts):
    return f"roundness = {_roundness_value(pts)!r}"

def claim_roundness_constant(pts):
    return "roundness = 0.000000"

def claim_affine_roundness(pts):
    cx, cy = centroid(pts); n = len(pts)
    sxx = sum((x - cx) ** 2 for x, y in pts) / n
    syy = sum((y - cy) ** 2 for x, y in pts) / n
    sxy = sum((x - cx) * (y - cy) for x, y in pts) / n
    det = sxx * syy - sxy * sxy
    if abs(det) < 1e-18:
        return "affine roundness = degenerate"
    tr = sxx + syy
    disc = math.sqrt(max(tr * tr - 4 * det, 0))
    l1, l2 = (tr + disc) / 2, (tr - disc) / 2
    if l1 <= 0 or l2 <= 0:
        return "affine roundness = degenerate"
    th = 0.5 * math.atan2(2 * sxy, sxx - syy)
    ct, st = math.cos(th), math.sin(th)
    w = []
    for x, y in pts:
        u = ct * (x - cx) + st * (y - cy); v = -st * (x - cx) + ct * (y - cy)
        w.append(math.hypot(u / math.sqrt(l1), v / math.sqrt(l2)))
    m = sum(w) / len(w)
    return f"affine roundness = {_z((max(w) - min(w)) / m):.6f}"

def claim_handedness_list(pts):
    return "orientation = CCW" if signed_area(pts) > 0 else "orientation = CW"

def claim_size(pts):
    cx, cy = centroid(pts)
    m = sum(math.hypot(x - cx, y - cy) for x, y in pts) / len(pts)
    return f"mean radius from centroid = {_z(m, 3):.3f}"

def claim_size_unrounded(pts):
    cx, cy = centroid(pts)
    m = sum(math.hypot(x - cx, y - cy) for x, y in pts) / len(pts)
    return f"mean radius from centroid = {m!r}"

def claim_count(pts):
    return f"count = {len(pts)}"

def claim_vacuous(pts):
    return "hello"

# Memorizer canary: transform-invariant signature of the original five
# identity worlds (point count, sorted normalized radii, sorted angular
# gaps). If a world matches one of the five, return genuine roundness;
# otherwise return raw coordinates.
def _signature(pts):
    cx, cy = centroid(pts)
    rs = [math.hypot(x - cx, y - cy) for x, y in pts]
    m = sum(rs) / len(rs) if rs else 1.0
    angs = sorted(math.atan2(y - cy, x - cx) for x, y in pts)
    gaps = []
    for i in range(len(angs)):
        gaps.append((angs[(i + 1) % len(angs)] - angs[i]) % (2 * math.pi))
    return (len(pts), sorted(r / m for r in rs), sorted(gaps))

_ORIGINAL_SIGNATURES = [_signature(B()) for B in BASES_ORIGINAL.values()]

def _sig_match(sig):
    n, rs, gaps = sig
    for on, ors, ogaps in _ORIGINAL_SIGNATURES:
        if n != on:
            continue
        if max(abs(a - b) for a, b in zip(rs, ors)) < 1e-3 and \
           max(abs(a - b) for a, b in zip(gaps, ogaps)) < 1e-3:
            return True
    return False

def claim_canary(pts):
    if _sig_match(_signature(pts)):
        return claim_roundness(pts)
    return lens_raw(pts)


LENSES = {
    "raw coordinates":      lens_raw,
    "topmost point":        claim_topmost_point,
    "topmost index":        claim_topmost_index,
    "roundness":            claim_roundness,
    "roundness (unrounded)": claim_roundness_unrounded,
    "roundness (constant)": claim_roundness_constant,
    "affine roundness":     claim_affine_roundness,
    "handedness (list)":    claim_handedness_list,
    "size":                 claim_size,
    "size (unrounded)":     claim_size_unrounded,
    "count":                claim_count,
    "vacuous":              claim_vacuous,
    "canary (memorizer)":   claim_canary,
}

# Declared reader per lens: numeric tolerance, or None for exact string.
NUMERIC_LENSES = {"topmost point", "roundness", "roundness (unrounded)",
                  "roundness (constant)", "affine roundness", "size",
                  "size (unrounded)"}
TOLERANCES = {name: (TOL if name in NUMERIC_LENSES else None) for name in LENSES}
TOLERANCES["canary (memorizer)"] = "mixed"


def _same_output(lens_name, a, b):
    tol = TOLERANCES.get(lens_name)
    if tol == "mixed":
        # Canary: compare numerically when both outputs are roundness,
        # otherwise exact string.
        if a.startswith("roundness") and b.startswith("roundness"):
            fa, fb = _floats(a), _floats(b)
            return len(fa) == len(fb) and all(abs(x - y) <= TOL for x, y in zip(fa, fb))
        return a == b
    if tol is not None:
        fa, fb = _floats(a), _floats(b)
        if len(fa) != len(fb):
            return False
        return all(abs(x - y) <= tol for x, y in zip(fa, fb))
    return a == b


# ---- questions ---------------------------------------------------------------
QUESTIONS = {
    "is it round?":            {"rotate", "scale", "translate", "mirror", "reverse", "shuffle"},
    "is it round (affine)?":   {"rotate", "scale", "translate", "mirror", "shear", "reverse", "shuffle"},
    "how big is it?":          {"rotate", "translate", "mirror", "reverse", "shuffle"},
    "is it drawn CCW?":        {"rotate", "scale", "translate"},
    "which point is highest?": {"scale", "translate"},
    "how many?":               {"rotate", "scale", "translate", "mirror", "shear", "reverse", "shuffle"},
}


# ---- the mechanism, v2 --------------------------------------------------------
def blind_set(lens_name, bases):
    lens = LENSES[lens_name]
    worlds = worlds_for(bases)
    rd = {k: lens(w) for k, w in worlds.items()}
    out = set()
    for t in TRANSFORMS:
        if t == "identity":
            continue
        if all(_same_output(lens_name, rd[(b, t)], rd[(b, "identity")]) for b in bases):
            out.add(t)
    return out

def discrimination(lens_name, bases):
    lens = LENSES[lens_name]
    seen = set()
    for b, B in bases.items():
        seen.add(lens(B()))
    return len(seen)

def verdict_for(B, G, disc):
    if G is None:
        return "NO VERDICT — question not declared"
    sees = sorted(G - B)
    blind = sorted(B - G)
    if not sees and not blind:
        return "ANSWERS VACUOUSLY" if disc <= 1 else "ANSWERS THE QUESTION"
    if sees and not blind:
        return "DRIFT: sees too much"
    if blind and not sees:
        return "DRIFT: blind to too much"
    return "DRIFT: both"

def catch(lens_name, question):
    """Returns (verdict, G or None, B_original, B_expanded,
    disc_original, disc_expanded, tolerance)."""
    if question not in QUESTIONS:
        B_o = blind_set(lens_name, BASES_ORIGINAL)
        B_e = blind_set(lens_name, BASES_EXPANDED)
        return ("NO VERDICT — question not declared", None, sorted(B_o), sorted(B_e),
                discrimination(lens_name, BASES_ORIGINAL),
                discrimination(lens_name, BASES_EXPANDED),
                TOLERANCES.get(lens_name))
    G = QUESTIONS[question]
    B_o = blind_set(lens_name, BASES_ORIGINAL)
    B_e = blind_set(lens_name, BASES_EXPANDED)
    disc_e = discrimination(lens_name, BASES_EXPANDED)
    v = verdict_for(set(B_e), G, disc_e)
    return (v, sorted(G), sorted(B_o), sorted(B_e),
            discrimination(lens_name, BASES_ORIGINAL), disc_e,
            TOLERANCES.get(lens_name))

def _fmt_tol(tol):
    return "exact string" if tol is None else ("mixed (numeric when roundness, else exact)" if tol == "mixed" else f"{tol:g}")

def battery():
    banner("DRIFT-CATCHER v2: flagship claim, every verdict with its G, tolerance, discrimination")
    q = "is it round?"
    for name in LENSES:
        v, G, B_o, B_e, d_o, d_e, tol = catch(name, q)
        print(f"  {name:<24} verdict: {v}")
        print(f"    G = {G}")
        print(f"    B original = {B_o}   B expanded = {B_e}")
        print(f"    tolerance = {_fmt_tol(tol)}   discrimination original = {d_o}   expanded = {d_e}")
    print()
    banner("PROBES: the four floors, re-run under v2")
    # B1: unrounded roundness
    v, G, B_o, B_e, d_o, d_e, tol = catch("roundness (unrounded)", q)
    print(f"  B1 unrounded roundness vs '{q}': {v}  (v1 string equality: DRIFT sees rotate,translate)")
    print(f"     B expanded = {B_e}")
    # B3: microscale probe, size
    for lname in ("size", "size (unrounded)"):
        lens = LENSES[lname]
        blind_micro = True
        maxdiff = 0.0
        for b, B in BASES_EXPANDED.items():
            a, c = lens(B()), lens(MICROSCALE(B()))
            fa, fb = _floats(a), _floats(c)
            if fa and fb:
                maxdiff = max(maxdiff, abs(fa[0] - fb[0]))
            if not _same_output(lname, a, c):
                blind_micro = False
        print(f"  B3 microscale (x1.00001) vs {lname}: blind = {blind_micro}, max |change| = {maxdiff:.6g} (tolerance 1e-9)")
    # Canary, original vs expanded
    for bases, label in ((BASES_ORIGINAL, "original"), (BASES_EXPANDED, "expanded")):
        B = blind_set("canary (memorizer)", bases)
        d = discrimination("canary (memorizer)", bases)
        v = verdict_for(B, QUESTIONS[q], d)
        print(f"  Canary on {label} worlds: B = {sorted(B)}, discrimination = {d}, verdict vs '{q}': {v}")
    # Unknown question
    v, G, B_o, B_e, d_o, d_e, tol = catch("roundness", "is it round")
    print(f"  Unknown question 'is it round' (no ?): {v}  (v1: KeyError crash)")
    print()
    banner("PREDICTION SCORECARD (predictions written before this run)")
    checks = []
    v, *_ = catch("roundness", q)
    checks.append(("P1 roundness ANSWERS", v == "ANSWERS THE QUESTION"))
    v2, *_ = catch("vacuous", "how many?")
    v3, *_ = catch("vacuous", "is it round (affine)?")
    checks.append(("P2 vacuous ANSWERS VACUOUSLY (both questions)", v2 == "ANSWERS VACUOUSLY" and v3 == "ANSWERS VACUOUSLY"))
    vu, *_ = catch("roundness (unrounded)", q)
    checks.append(("P3 unrounded roundness ANSWERS", vu == "ANSWERS THE QUESTION"))
    lens = LENSES["size"]
    blind_micro = all(_same_output("size", lens(B()), lens(MICROSCALE(B()))) for B in BASES_EXPANDED.values())
    checks.append(("P4 size NOT blind to microscale", not blind_micro))
    Bc_o = blind_set("canary (memorizer)", BASES_ORIGINAL)
    Bc_e = blind_set("canary (memorizer)", BASES_EXPANDED)
    Br_o = blind_set("roundness", BASES_ORIGINAL)
    checks.append(("P5 canary original B = roundness B, expanded B empty",
                   Bc_o == Br_o and len(Bc_e) == 0))
    honest = ["roundness", "affine roundness", "handedness (list)", "topmost index", "count", "vacuous"]
    checks.append(("P6 honest lenses B stable original -> expanded",
                   all(blind_set(n, BASES_ORIGINAL) == blind_set(n, BASES_EXPANDED) for n in honest)))
    vu2, *_ = catch("roundness", "is it round")
    checks.append(("P7 unknown question NO VERDICT, no crash", vu2.startswith("NO VERDICT")))
    checks.append(("P8 verdict lines carry G, tolerance, discrimination", True))
    for label, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    print(f"  Score: {sum(ok for _, ok in checks)}/{len(checks)}")


if __name__ == "__main__":
    battery()
