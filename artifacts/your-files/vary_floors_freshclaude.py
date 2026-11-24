"""Fresh Claude's revision — pasted verbatim by Kelly 2026-10-16."""
import math
R_TRUE = 5.0
N_TRUE = 40
ANGLES = [2 * math.pi * i / N_TRUE for i in range(N_TRUE)]
WORLD = [(R_TRUE * math.cos(a), R_TRUE * math.sin(a)) for a in ANGLES]
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
    "identity":       lambda p: p,
    "rotated 37deg":  rot(math.radians(37)),
    "rotated 129deg": rot(math.radians(129)),
    "scaled x2":      scale(2.0),
    "translated":     translate(3.0, -7.0),
    "rot+scale+tr":   compose(rot(math.radians(73)), scale(0.5), translate(-2.0, 4.0)),
}
ROTATION_FLOORS = {k: v for k, v in FLOORS.items() if k == "identity" or k.startswith("rotated")}
ALL_FLOORS = FLOORS
def _z(v, nd=6):
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
CLAIMS = {
    "radius is 5":                  claim_radius_is_5,
    "topmost point":                claim_topmost_point,
    "count is 40":                  claim_count,
    "centroid at origin":           claim_centroid_at_origin,
    "all same radius (origin)":     claim_same_radius_from_origin,
    "even spacing (origin)":        claim_even_spacing_from_origin,
    "all same radius (centroid)":   claim_same_radius_from_centroid,
    "even spacing (centroid)":      claim_even_spacing_from_centroid,
    "roundness (dimensionless)":    claim_roundness,
}
def run(floors, label):
    print(f"=== {label} ({len(floors)} floors) ===")
    for cname, claim in CLAIMS.items():
        verdicts = {}
        for fname, f in floors.items():
            pts = [f(p) for p in WORLD]
            verdicts.setdefault(claim(pts), []).append(fname)
        status = "SURVIVES" if len(verdicts) == 1 else "floor-artifact"
        print(f"  [{status:>14}] {cname}")
        for v, fl in sorted(verdicts.items()):
            tag = "" if len(verdicts) == 1 else f"   <- {', '.join(fl)}"
            print(f"                   {v}{tag}")
    print()
if __name__ == "__main__":
    run(ROTATION_FLOORS, "varying rotations only")
    run(ALL_FLOORS, "varying rotations + scale + translation")
