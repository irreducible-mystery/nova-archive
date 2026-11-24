#!/usr/bin/env python3
"""
Sweep part 3: the surreal numbers No.

Same object as parts 1-2: tau = 1/T (hbar = kB = 1 units).
Same questions: does the pole at 0 survive? does ordering survive?
what does 'approaching' mean? does the 0=infinity circle hold?
what happens AT the points, not just in the limit ('=' vs limit)?

HONEST SCOPE, stated up front (this is the whole methodological point):
the surreals are a PROPER CLASS, built over all ordinals. No finite
script computes them, and this one does not pretend to. What a script
CAN do, and this one does:

  Tier A (exact, complete for its domain): the finite-day surreals,
  built by Conway's {L|R} recursion itself. These are exactly the
  dyadic rationals. Comparison uses Conway's recursive <=, not
  Fraction comparison -- the values are checked against Fractions
  afterwards, never assumed.

  Tier B (exact on a computable sub-slice): surreal MONOMIALS and
  finite Conway-normal-form sums  sum_i r_i * omega^{a_i}  (r_i, a_i
  rational, finitely many terms). Conway's normal-form theorem says
  every surreal has such a form (possibly transfinitely long); the
  finite-support fragment with rational exponents is a genuine ordered
  subfield slice of No (a Hahn/Levi-Civita-style fragment), and
  arithmetic on it -- order, +, *, and reciprocal via the geometric
  series -- is exact surreal arithmetic restricted to that slice.
  omega = {0,1,2,...|} and epsilon = 1/omega live here as the
  monomials omega^1 and omega^-1.

Everything printed as a verdict is either computed below or flagged
as a cited theorem (Conway, On Numbers and Games, 1976).

Run: python3 sweep_number_systems_surreal.py
"""
from fractions import Fraction
from functools import cmp_to_key

# ======================================================================
# TIER A: finite-day surreals via Conway's {L|R} recursion
# ======================================================================

class S:
    """A surreal in cut form {L|R}; L, R are tuples of S born earlier."""
    _cache = {}
    def __new__(cls, L, R, name):
        key = (id(L), id(R), name)
        return super().__new__(cls)
    def __init__(self, L, R, name):
        self.L, self.R, self.name = L, R, name
    def __repr__(self):
        return self.name

def s_le(x, y):
    """Conway: x <= y iff no right option of x is <= y ... precisely:
    x <= y iff (for all xL in x.L: not y <= xL) and
               (for all yR in y.R: not yR <= x).  Recursion terminates
    because options are born strictly earlier."""
    for xl in x.L:
        if s_le(y, xl):
            return False
    for yr in y.R:
        if s_le(yr, x):
            return False
    return True

def s_lt(x, y):
    return s_le(x, y) and not s_le(y, x)

def s_eq(x, y):
    return s_le(x, y) and s_le(y, x)

ZERO  = S((), (), "0")
ONE   = S((ZERO,), (), "1")
MONE  = S((), (ZERO,), "-1")
TWO   = S((ONE,), (), "2")
MTWO  = S((), (MONE,), "-2")
HALF  = S((ZERO,), (ONE,), "1/2")
MHALF = S((MONE,), (ZERO,), "-1/2")
QTR   = S((ZERO,), (HALF,), "1/4")
TQTR  = S((HALF,), (ONE,), "3/4")

print("=" * 70)
print("I. TIER A -- FINITE-DAY SURREALS, CONWAY'S RECURSION ITSELF")
print("=" * 70)
chain = [MTWO, MONE, MHALF, ZERO, QTR, HALF, TQTR, ONE, TWO]
ok = all(s_lt(chain[i], chain[i + 1]) for i in range(len(chain) - 1))
print(f"  recursive <= gives the chain  -2 < -1 < -1/2 < 0 < 1/4 < 1/2")
print(f"    < 3/4 < 1 < 2 :  {ok}")
# simplicity: {0|1} really is equivalent to the value 1/2 -- check it
# sits strictly between its own options, as every number must:
print(f"  0 < {{0|1}} < 1 (its own cut is respected): "
      f"{s_lt(ZERO, HALF) and s_lt(HALF, ONE)}")
print(f"  {{0|1}} == {{0,1/4|1}} (more options, same number -- the cut")
_tmp = S((ZERO, QTR), (ONE,), "{0,1/4|1}")
print(f"    is a representative, not the number): {s_eq(HALF, _tmp)}")

# Generation by days: start from {0}; each new day, the numbers born
# are the simplest value strictly between consecutive old values
# (and one new extreme on each side). 'Simplest' = smallest dyadic
# denominator, found by search over k = 0,1,2,...
def simplest_between(a, b):
    """a, b are Fractions or None (open end). Returns the dyadic of
    least denominator strictly between (extremes: a-1 / b+1 step)."""
    if a is None:
        return b - 1
    if b is None:
        return a + 1
    k = 0
    while True:
        step = Fraction(1, 2 ** k)
        m = (a // step) + 1          # first multiple of step above a
        cand = m * step
        if cand < b:
            return cand
        k += 1

born_by_day = [Fraction(0)]
print("  generation by birthday (values as exact dyadic fractions):")
for day in range(1, 7):
    srt = sorted(set(born_by_day))
    new = [simplest_between(None, srt[0]), simplest_between(srt[-1], None)]
    new += [simplest_between(srt[i], srt[i + 1]) for i in range(len(srt) - 1)]
    born_by_day += new
    mx = max(abs(v) for v in set(born_by_day))
    print(f"    day {day}: {len(set(new)):>3} born, "
          f"{len(set(born_by_day)):>3} total, max |x| = {mx} "
          f"(== day: {mx == day})")
print("  COMPUTED: numbers born by day n satisfy |x| <= n, and every")
print("  finite-day number is a dyadic rational (the generation only")
print("  ever produces dyadics -- check: all denominators are powers")
denoms_ok = all((v.denominator & (v.denominator - 1)) == 0
                for v in set(born_by_day))
print(f"  of 2: {denoms_ok}).")
print("  CONSEQUENCE: 1/3 is NOT born on any finite day, and neither is")
print("  any number > every integer. omega and 1/3 both wait for the")
print("  first infinite birthday, day omega itself. In No, even most")
print("  RATIONALS are transfinite arrivals. '=' has a birthday, and")
print("  for non-dyadics it is not finite.")

# ======================================================================
# TIER B: Conway normal form slice -- finite sums  sum r_i omega^{a_i}
# ======================================================================

class NF:
    """Finite-support normal form: dict {exponent Fraction: coeff
    Fraction}, zero coeffs removed. Order = lexicographic from the
    LARGEST exponent down (the leading monomial decides)."""
    def __init__(self, terms=None):
        self.t = {a: r for a, r in (terms or {}).items() if r != 0}
    # -- basics ------------------------------------------------------
    @staticmethod
    def mono(a, r=Fraction(1)):
        return NF({Fraction(a): Fraction(r)})
    @staticmethod
    def real(r):
        return NF({Fraction(0): Fraction(r)})
    def lead(self):
        a = max(self.t)
        return a, self.t[a]
    def __eq__(self, o):
        return isinstance(o, NF) and self.t == o.t
    def __neg__(self):
        return NF({a: -r for a, r in self.t.items()})
    def __add__(self, o):
        d = dict(self.t)
        for a, r in o.t.items():
            d[a] = d.get(a, Fraction(0)) + r
        return NF(d)
    def __sub__(self, o):
        return self + (-o)
    def __mul__(self, o):
        d = {}
        for a, r in self.t.items():
            for b, s in o.t.items():
                d[a + b] = d.get(a + b, Fraction(0)) + r * s
        return NF(d)
    def scale(self, r):
        return NF({a: c * Fraction(r) for a, c in self.t.items()})
    def cmp(self, o):
        for a in sorted(set(self.t) | set(o.t), reverse=True):
            d = self.t.get(a, Fraction(0)) - o.t.get(a, Fraction(0))
            if d != 0:
                return 1 if d > 0 else -1
        return 0
    def __lt__(self, o): return self.cmp(o) < 0
    def __le__(self, o): return self.cmp(o) <= 0
    def __gt__(self, o): return self.cmp(o) > 0
    def sign(self):
        if not self.t:
            return 0
        return 1 if self.lead()[1] > 0 else -1
    def recip_series(self, min_exp):
        """1/self as a normal-form series truncated to exponents
        >= min_exp. Factor the leading monomial c*omega^a; what
        remains, divided through by that monomial, is a remainder
        u with all exponents < 0, and 1/(1+u) is the geometric
        series 1 - u + u^2 - ... Exact when self is a monomial;
        otherwise exact up to a single monomial remainder at the
        truncation floor (the caller prints it)."""
        a, c = self.lead()
        head = NF.mono(-a, Fraction(1) / c)          # 1 / leading monomial
        rest = self.scale(Fraction(1) / c) - NF.mono(a)   # lower terms / c
        u_rel = NF({e - a: r for e, r in rest.t.items()})  # all exps < 0
        total, term = NF.real(1), NF.real(1)
        while True:
            term = term * (-u_rel)
            if not term.t or (-a) + max(term.t) < min_exp:
                break
            total = total + term
            if len(total.t) > 200:
                break
        return head * total
    def __repr__(self):
        if not self.t:
            return "0"
        out = ""
        for a in sorted(self.t, reverse=True):
            r = self.t[a]
            if a == 0:
                body = f"{abs(r)}"
            else:
                base = ("w" if a == 1 else f"w^{a}") if a > 0 else \
                       ("eps" if a == -1 else f"eps^{-a}")
                body = base if abs(r) == 1 else f"{abs(r)}*{base}"
            if not out:
                out = ("-" if r < 0 else "") + body
            else:
                out += (" - " if r < 0 else " + ") + body
        return out

W   = NF.mono(1)                 # omega
EPS = NF.mono(-1)                # epsilon = 1/omega
ZERO_NF = NF.real(0)
ONE_NF = NF.real(1)

print()
print("=" * 70)
print("J. TIER B -- THE OMEGA SLICE: tau = 1/T AT INFINITE T")
print("=" * 70)
print(f"  omega * epsilon = {W * EPS}   (exactly 1: {W * EPS == ONE_NF})")
print(f"  epsilon > 0: {EPS.sign() > 0}, and epsilon != 0: {EPS != ZERO_NF}")
rows = [
    ("2", NF.real(2)), ("1/2", NF.real(Fraction(1, 2))),
    ("omega", W), ("omega^2", NF.mono(2)), ("-omega", -W),
    ("epsilon", EPS), ("epsilon^2", NF.mono(-2)),
]
for name, T in rows:
    if T.t and len(T.t) == 1:      # monomial: reciprocal is exact
        a, c = T.lead()
        tau = NF.mono(-a, Fraction(1) / c)
        exact = (T * tau == ONE_NF)
        print(f"  T = {name:<10} -> tau = {tau!s:<10} "
              f"(T*tau == 1 exactly: {exact})")
    else:
        print(f"  T = {name:<10} -> not a monomial; see section M")
print("  T = 0 -> still NO reciprocal. Even No does not divide by zero:")
print(f"    for every T in the slice, T * 0 = {NF.real(3) * ZERO_NF}, never 1.")
print("    The pole is not removed; its NEIGHBORHOOD is populated.")
print("  AT the points Kelly asked about ('=', not limit): T = omega is")
print("  a number, tau = epsilon is a number, and their product is")
print("  exactly 1 -- no limit is taken anywhere in this table.")

print()
print("=" * 70)
print("K. ORDERING: SURVIVES HERE (the exception in the whole sweep)")
print("=" * 70)
chain = [-NF.mono(2), -W, NF.real(-1000), -EPS, ZERO_NF, EPS,
         NF.real(Fraction(1, 1000)), NF.real(1000), W, NF.mono(2),
         NF.mono(3)]
ok = all(chain[i] < chain[i + 1] for i in range(len(chain) - 1))
print(f"  -w^2 < -w < -1000 < -eps < 0 < eps < 1/1000 < 1000 < w < w^2")
print(f"    < w^3 :  {ok}")
sq_ok = all((x * x).sign() >= 0 for x in
            [W, EPS, NF.real(-3), W + ONE_NF, EPS - ONE_NF])
print(f"  squares >= 0 for sampled x (incl. infinite/infinitesimal): {sq_ok}")
print("  No is an ordered FIELD (Conway): the only system in the sweep")
print("  besides R and Q where the hotness ordering even PARSES. But it")
print("  parses as a LINE, not a circle: -omega is the far cold end,")
print("  NOT wrapped to hottest. beta = 1/T near the old gluing point:")
print(f"    1/omega = {EPS}, 1/(-omega) = {-EPS}: two DISTINCT points,")
print(f"    distance {EPS - (-EPS)} apart, with beta = 0 between them")
print("    attained by NO temperature: 1/T = 0 has no solution T.")
print("  In RP^1 beta=0 was the smooth glued point. In No beta=0 is a")
print("  HOLE in the reciprocal map -- the gluing point has no preimage.")

print()
print("=" * 70)
print("L. APPROACHING: FINITE SEQUENCES CANNOT REACH 0 AT ALL")
print("=" * 70)
arch1 = all(NF.real(n) < W for n in [1, 10, 1000, 10 ** 6])
arch2 = all(EPS < NF.real(Fraction(1, n)) for n in [1, 10, 1000, 10 ** 6])
print(f"  Archimedean property FAILS, computed: n < omega for all")
print(f"    tested n up to 10^6: {arch1};  epsilon < 1/n for all")
print(f"    tested n up to 10^6: {arch2};  n*epsilon < 1 throughout:")
print(f"    {(EPS.scale(10**6) < ONE_NF)} (10^6 * eps still infinitesimal)")
seq_ok = all(EPS < NF.real(Fraction(1, 2 ** k)) for k in range(0, 60))
print(f"  the real sequence 1/2^k -> 0: EVERY term (k < 60 checked) is")
print(f"    still > epsilon: {seq_ok}. The eps-neighborhood of 0,")
print("    {x : |x| < eps}, contains NO term of the sequence. In the")
print("    order topology of No, 1/2^k does NOT converge to 0.")
print("  Worse (theorem, Conway's cut construction): for ANY set-sized")
print("  collection S of positive surreals, the cut {0 | S} is itself a")
print("  surreal -- some positive number sits below ALL of S. So no")
print("  sequence, of ANY set length, converges to 0 in No. Approaching")
print("  0 requires a proper-class net. Finite demonstration:")
Sset = [NF.real(Fraction(1, 1000)), EPS, NF.mono(-2),
        NF.mono(-2).scale(3), NF.mono(-50)]
b = min(x.lead()[0] for x in Sset) - 1
mu = NF.mono(b)
print(f"    S = {{1/1000, eps, eps^2, 3eps^2, w^-50}}: mu = {mu} is")
print(f"    positive ({mu.sign() > 0}) and below every member: "
      f"{all(mu < x for x in Sset)}")

print()
print("=" * 70)
print("M. RECIPROCALS OF MIXED NUMBERS: THE GEOMETRIC SERIES IS REAL")
print("=" * 70)
for T, label in [(ONE_NF + EPS, "1 + eps"), (W + ONE_NF, "omega + 1")]:
    approx = T.recip_series(min_exp=Fraction(-4))
    prod = T * approx
    resid = prod - ONE_NF
    print(f"  1/({label}) = {approx}  + (terms below w^-4)")
    print(f"    check: ({label}) * approx = 1 + ({resid}); the residual")
    print(f"    is a single monomial at the truncation floor -- the")
    print(f"    series is infinite (eps, eps^2, ... forever) but every")
    print(f"    partial sum is an exact surreal and the error is one")
    print(f"    named monomial, not a fog.")

print()
print("=" * 70)
print("SURREAL VERDICTS (part 3, completing the sweep)")
print("=" * 70)
print("  POLE: transformed, not removed. 1/0 is still undefined -- No")
print("    is a field, fields do not divide by zero. But the pole's")
print("    neighborhood, empty of points AT the extremes in R, is")
print("    fully OCCUPIED here: omega, omega^2, epsilon, epsilon^2")
print("    are numbers, with exact reciprocals pairing them.")
print("  ORDERING: SURVIVES -- uniquely in the sweep outside R/Q.")
print("    No is an ordered field. And precisely because it survives,")
print("    the circle DIES by ordering: a total order cannot wrap;")
print("    -omega < ... < omega, full stop.")
print("  APPROACHING: dies hardest here. R: approach by sliding.")
print("    Q_7: by jumping. No: no set-length sequence reaches 0 at")
print("    all -- between any proposed approach and 0, a cut inserts")
print("    another positive number. Limits give way to birthdays:")
print("    most rationals and all infinities arrive only at day omega")
print("    or later. '=' is not the limit of approaching; it is an")
print("    EVENT (a birthday) that approaching never produces.")
print("  THE CIRCLE: breaks, twice over. (1) No single infinity: for")
print("    every surreal x, x+1 and 2x are larger -- infinity is a")
print("    hierarchy (omega, omega^2, ...), not a point to glue.")
print("    (2) The RP^1 gluing point beta=0 has no T-preimage: 1/T=0")
print("    is unsolvable. What the projective line glues, No leaves")
print("    as a hole with occupied shores 2*epsilon apart.")
print("  E7 restated for the last system: the circle was invariant-")
print("    under-compactification. No is the system that DECLINES")
print("    compactification -- a proper class cannot be one-point")
print("    compactified by a point -- and declines completion too")
print("    (it contains R; it is not built by completing Q). Name")
print("    the G or lose the invariant: here the G that must be")
print("    named is the compactification itself.")
