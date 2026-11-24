"""
drift_catcher.py — the mechanism, built.

Three moving parts:
  1. something held fixed:   the QUESTION, stated as the set G of
     transformations the asker does not care about.
     ("Is it round?" means: rotation, scale, translation... shouldn't matter.)
  2. something that varies it: the claim, run across worlds x transforms;
     its ACTUAL blind set B = transforms it cannot detect.
  3. the comparison:          G vs B. Two gaps, two drift modes:
       sees-too-much   (G - B): the claim detects something the question
                       says shouldn't matter -> it answers a NARROWER
                       question than you asked.
       blind-too-much  (B - G): the claim ignores something the question
                       cares about -> it answers a BROADER question, or
                       nothing at all (vacuous = blind to everything).

The ideal B == G never quite happens. The report is the gap.

Lineage: F5 (the question fixes G) + L1 (the blind-to table), assembled
into the thing both were pointing at. Stdlib only.

Run: python3 drift_catcher.py
"""

import math
import random

N = 40
W = 76


def banner(t):
    print("=" * W); print(t); print("=" * W)


# ---- worlds ---------------------------------------------------------------
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

BASES = {"circle": circle, "ellipse": ellipse, "square": square,
         "spiral": spiral, "cloud": cloud}


# ---- transforms (pointwise, lifted to worlds) ------------------------------
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

WORLDS = {(b, t): T(B()) for b, B in BASES.items() for t, T in TRANSFORMS.items()}


# ---- helpers ---------------------------------------------------------------
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


# ---- claims (lenses) --------------------------------------------------------
def lens_raw(pts):
    return str([(_z(x, 3), _z(y, 3)) for x, y in pts])

def claim_topmost_point(pts):
    top = max(pts, key=lambda p: p[1])
    return f"topmost at ({_z(top[0], 3):.3f}, {_z(top[1], 3):.3f})"

def claim_topmost_index(pts):
    return f"highest point is #{max(range(len(pts)), key=lambda i: pts[i][1])}"

def claim_roundness(pts):
    cx, cy = centroid(pts)
    rs = [math.hypot(x - cx, y - cy) for x, y in pts]
    m = sum(rs) / len(rs)
    return f"roundness = {_z((max(rs) - min(rs)) / m):.6f}"

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

def claim_handedness_set(pts):
    c = centroid(pts)
    best, bi, bj = -1, 0, 1
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            dd = (pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2
            if dd > best:
                best, bi, bj = dd, i, j
    x0, y0 = c; x1, y1 = pts[bi]; x2, y2 = pts[bj]
    s = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
    return "orientation = CCW (set)" if s > 0 else "orientation = CW (set)"

def claim_size(pts):
    cx, cy = centroid(pts)
    m = sum(math.hypot(x - cx, y - cy) for x, y in pts) / len(pts)
    return f"mean radius from centroid = {_z(m, 3):.3f}"

def claim_count(pts):
    return f"count = {len(pts)}"

def claim_vacuous(pts):
    return "hello"

LENSES = {
    "raw coordinates":      lens_raw,
    "topmost point":        claim_topmost_point,
    "topmost index":        claim_topmost_index,
    "roundness":            claim_roundness,
    "affine roundness":     claim_affine_roundness,
    "handedness (list)":    claim_handedness_list,
    "handedness (set)":     claim_handedness_set,
    "size":                 claim_size,
    "count":                claim_count,
    "vacuous":              claim_vacuous,
}


# ---- questions: the G the asker means ---------------------------------------
# Each question declares which transformations "shouldn't matter".
# These declarations are floors. They are stated, not derived.
QUESTIONS = {
    "is it round?":            {"rotate", "scale", "translate", "mirror", "reverse", "shuffle"},
    "is it round (affine)?":   {"rotate", "scale", "translate", "mirror", "shear", "reverse", "shuffle"},
    "how big is it?":          {"rotate", "translate", "mirror", "reverse", "shuffle"},
    "is it drawn CCW?":        {"rotate", "scale", "translate"},
    "which point is highest?": {"scale", "translate"},
    "how many?":               {"rotate", "scale", "translate", "mirror", "shear", "reverse", "shuffle"},
}


# ---- the mechanism -----------------------------------------------------------
def blind_set(lens):
    """B: transforms the lens cannot detect on ANY base shape."""
    rd = {k: lens(w) for k, w in WORLDS.items()}
    out = set()
    for t in TRANSFORMS:
        if t == "identity":
            continue
        if all(rd[(b, t)] == rd[(b, "identity")] for b in BASES):
            out.add(t)
    return out

BLIND = {name: blind_set(l) for name, l in LENSES.items()}

def catch(lens_name, question):
    """Run the drift-catcher: compare the claim's blind set B against the
    question's declared indifference set G."""
    B = BLIND[lens_name]
    G = QUESTIONS[question]
    sees_too_much = sorted(G - B)    # detects what shouldn't matter
    blind_too_much = sorted(B - G)   # ignores what matters
    if not sees_too_much and not blind_too_much:
        verdict = "ANSWERS THE QUESTION"
    elif sees_too_much and not blind_too_much:
        verdict = "DRIFT: sees too much"
    elif blind_too_much and not sees_too_much:
        verdict = "DRIFT: blind to too much"
    else:
        verdict = "DRIFT: both"
    return verdict, sees_too_much, blind_too_much, sorted(B)


def demo_table():
    banner("THE DRIFT-CATCHER: every lens against every question")
    print("  B == the claim's blind set (computed). G == the question's declared")
    print("  indifference set (stated). G-B: detects what shouldn't matter.")
    print("  B-G: ignores what matters.\n")
    for q in QUESTIONS:
        print(f"  Q: {q}   G = {sorted(QUESTIONS[q])}")
        for name in LENSES:
            v, s2m, b2m, B = catch(name, q)
            tag = "OK " if v == "ANSWERS THE QUESTION" else "   "
            detail = ""
            if s2m:
                detail += f" sees:{','.join(s2m)}"
            if b2m:
                detail += f" blind:{','.join(b2m)}"
            print(f"    [{tag}] {name:<18} {v:<24}{detail}")
        print()


def worked():
    banner("WORKED EXAMPLES: what the gaps mean")
    cases = [
        ("topmost point", "is it round?",
         "The classic. You asked a shape question; the claim answers a gravity one."),
        ("roundness", "is it round?",
         "The claim the series meant."),
        ("roundness", "is it round (affine)?",
         "Same English word, different G: a sheared circle. W3's lesson, caught."),
        ("handedness (list)", "is it drawn CCW?",
         "Order is data here: reverse/shuffle are correctly OUTSIDE G."),
        ("handedness (set)", "is it drawn CCW?",
         "The set version smuggles order back in via the farthest pair."),
        ("vacuous", "how many?",
         "Blind to everything: passes every G, answers nothing."),
        ("raw coordinates", "is it round?",
         "Blind to nothing: the other failure mode. Sees everything, answers nothing."),
        ("topmost index", "which point is highest?",
         "Note what G leaves out: is list order data, or is the physical point?"),
    ]
    for lens_name, q, note in cases:
        v, s2m, b2m, B = catch(lens_name, q)
        print(f"  claim: {lens_name}  |  question: {q}")
        print(f"    -> {v}")
        if s2m:
            print(f"       sees too much: {s2m}  (narrower question than asked)")
        if b2m:
            print(f"       blind too much: {b2m}  (broader question, or nothing)")
        print(f"    {note}\n")


def summary():
    banner("WHAT GOT BUILT, AND WHAT IT STANDS ON")
    print("  The drift-catcher is F5's 'the question fixes G' turned into a tool:")
    print("  state the question as a set, compute the claim's blind set, read")
    print("  the gap. It does not certify truth. It locates the place where the")
    print("  question you meant and the question your claim answers come apart.")
    print()
    print("  Floors this script knows it stands on and is not varying:")
    print("    - the QUESTIONS dict: English turned into sets by fiat. W3's gap")
    print("      (word vs group) lives here, stated, not solved.")
    print("    - 'same verdict' means string equality (the unexamined reader).")
    print("    - five shapes, seven transforms: a sample, not the space (F1).")
    print("    - the worlds are still fixed. E2's criticism applies to this")
    print("      script exactly as it applied to the first one.")
    print("    - B == G never happens; 'ANSWERS THE QUESTION' is approximate,")
    print("      graded by the size of the gap, not boolean (E6).")
    print()
    print("  Use: when a claim and a question part ways, run this before arguing")
    print("  about the claim. Argue about the gap instead.")


if __name__ == "__main__":
    demo_table()
    worked()
    summary()
