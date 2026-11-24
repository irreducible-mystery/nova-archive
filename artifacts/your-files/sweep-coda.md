# Sweep coda: the two systems the sweep only gestured at

Parts 1–2 computed six systems and left two gestured-at: the essential
singularity (catalog's "unknown" one-liner) and the surreals (part 1's
"stated but not computed"). This note closes both — one by measurement,
one by structure, each labeled honestly.

Companion files: `sweep_essential_singularity.py` (exit 0),
`out_sweep_essential_singularity.txt` (the measured output).

## 1. The essential singularity, measured

`e^{1/z}` at `z = 0`. Picard's great theorem says: in every punctured
neighborhood of an essential singularity, the function takes every
complex value infinitely often, with at most one exception. For
`e^{1/z}` the exception is 0 — it never equals 0. (Keep that; it matters.)

Measurement 1 — winding numbers on the circle `|z| = r`, 400k samples,
phase-unwrapped. Theory: `arg(e^{1/z}) = −(sin θ)/r` sweeps `[−1/r, 1/r]`,
so the image winds about `1/(πr)` times around any fixed target, and each
winding forces arbitrarily close near-passes of that target.

| r     | predicted windings | measured (1, −1, i, 2+3i, 0.5−0.25i) |
|-------|--------------------|---------------------------------------|
| 0.5   | 0.6                | −1, 0, −1, −1, −1                     |
| 0.1   | 3.2                | −3, −4, −3, −3, −3                    |
| 0.05  | 6.4                | −7, −6, −6, −7, −7                    |
| 0.01  | 31.8               | −31, −32, −32, −32, −31               |
| 0.005 | 63.7               | −63, −64, −64, −63, −63               |

(The sign is orientation — clockwise. The magnitude is the finding.)

**The wildness is democratic.** 1, −1, i, 2+3i, and the nobody-number
0.5−0.25i are all wound around the same number of times. No target is
special. The blowup contains everything *equally* — measured, not asserted.

Measurement 2 — approach along rays `z = t·e^{iφ}`, exact in log-modulus
(so no float overflow can lie):

- φ=0°: log|w| = +10, +100, +1000 → **+∞** (the familiar pole face)
- φ=180°: log|w| = −10, −100, −1000 → **0** (collapses toward it, never touches)
- φ=90°: |w| = 1 forever, arg = −10, −100, −1000 rad → **no limit at all**,
  the curve wraps the unit circle infinitely often

So "the limit at 0" is not a limit — it is five different answers
depending on the path, and one of the paths has no answer. Compare with
the sweep's pole, where every path agreed on "blows up" and only the
*meaning* of the blowup varied. The essential singularity is the pole's
evil twin: here it is the *value* that varies, not the meaning.

Verdict for the catalog: **unknown → real and measured.** Reclassify
`e^{1/z}` from "unknown" to its own line: the blowup that is not a
breakdown but a *surfeit* — too many values, not too few. And Picard's
exception is the quietest line in the whole catalog: the wildest blowup
in mathematics still has one value it never touches. The gap stays empty.

## 2. The surreals, treated (not computed — structurally)

Conway, *On Numbers and Games* (1976). Honest first: no finite script
captures the surreals; what follows is structure, not measurement.

- `ω = {0,1,2,…|}` — the first infinite. `ε = 1/ω = {0|1,1/2,1/4,…}` —
  a genuine positive infinitesimal, and `1/ε = ω` **exactly**.
- The map `x ↦ 1/x` is an order-reversing involution of the nonzero
  surreals: it swaps infinities with infinitesimals and fixes ±1.
  `1/ω = ε ≠ 0`. There is no single ∞ — there are ω, ω², ω^ω, …,
  each with its own infinitesimal reciprocal.
- **The "=" side wins.** In the surreals you can stand *at* 1/ω, *at*
  1/ω², … — the limit T→0⁺ is witnessed by actual infinitesimal points,
  each with its exact reciprocal. No limit needed; the endpoints are
  occupied. Your "=" versus limit distinction collapses the other way:
  here "=" is all there is, and "approaching" is the thing that needs
  explaining.
- **The circle breaks, and now we know why.** The β-chart's trick — the
  smooth point at β=0 — required identifying +∞ and −∞ as *one* point.
  In the surreals there is no one infinity to glue, and worse: the
  surreals are a proper class, not a set — **compactification is not
  available**. 0 and ω are genuinely far apart, with the whole hierarchy
  (…, ε², ε, …, finite, …, ω, ω², …) between them. No meeting.

Updated meta-verdict, in series language: the circle is
**invariant-under-compactification**. Part 2 showed it is not
invariant-under-completion-choice (ℝ vs ℚ₇; Ostrowski: the completion
chooses the meaning of "limit"). The surreals go one further: they are
not a completion of ℚ at all, and they decline the compactification the
circle needs. E7 holds — no "invariant" without naming the G, and the
G has to name the compactification. The surreals refuse to name one.

## Series status

All eight systems now visited: ℝ, β-chart, ℂ, ℚ, float32/float64, 𝔽₁₀₁,
ℍ, ℚ₇ (computed, parts 1–2) — plus the essential singularity (measured,
this note) and the surreals (structural, this note). Nothing left
gestured-at. The sweep is closed unless you open a new system.

---

## Postscript, 2026-10-20 evening — the surreals, swept after all

Kelly reopened it ("lets sweep surreal like you suggested earlier"),
so §2's "not computed" now has a computed companion:
`sweep_number_systems_surreal.py` (exit 0), output
`out_sweep_number_systems_surreal.txt`. Scope, stated in the script
itself: the whole proper class is still uncomputable — what got
computed is (A) the finite-day surreals via Conway's recursive ≤
itself (exactly the dyadics), and (B) the finite Conway-normal-form
slice Σ rᵢω^{aᵢ}, where surreal arithmetic is exact. New measured
results beyond §2's structural account:

- **Generation by birthday**: day n births 2ⁿ numbers, max |x| = n
  exactly (checked to day 6). So 1/3 — like ω — is born on no finite
  day; non-dyadic rationals arrive at day ω. "=" has a birthday, and
  approaching never produces it.
- **Ordering survives** — the only system outside ℝ/ℚ where the
  hotness ordering even parses (No is an ordered field) — and the
  circle dies *by* that ordering: −ω < −ε < 0 < ε < ω, a line.
- **The gluing point is a hole**: 1/ω = ε and 1/(−ω) = −ε are distinct
  points 2ε apart, and β = 0 between them is attained by no T
  (1/T = 0 unsolvable). RP¹ glues what No leaves open, with both
  shores occupied.
- **Approaching dies hardest**: 1/2ᵏ does not converge to 0 in No's
  order topology (every term > ε, checked k < 60); by Conway's cut
  construction no set-length sequence reaches 0 at all — between any
  proposed approach and 0 a cut inserts another positive number.
- **Mixed reciprocals**: 1/(1+ε) and 1/(ω+1) are genuine infinite
  geometric series in ε; every partial sum is an exact surreal and
  the truncation error is a single named monomial (ε⁵, −ε⁴).

Nothing in §2 was wrong; it is now measured where it can be. The
sweep is closed again — this time with the surreals inside it.
