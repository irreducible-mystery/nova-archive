# A Catalog of Blowups

Blowups at or approaching 0 and infinity, across domains and scales —
each classified by the verdict the number-system sweep taught us to ask:
**is it real, a chart artifact, an instrument artifact, tamed, unattained, or unknown?**

Compiled 2026-10-19. Numbers checked where stated; regimes labeled.

---

## 1. Chart artifacts — vanish under coordinate change

**Black hole horizon (r = 2M).** Schwarzschild's coordinates blow up at the
horizon; for decades it read as a singularity. Kruskal / Eddington–Finkelstein
coordinates are smooth there. The horizon was never singular — the chart was.
*Domain: GR. Scale: stellar to supermassive.*

**Infinite temperature (T = ±∞).** In the T-chart the Planckian thermalization
bound dissolves into vacuousness. In the β-chart (β = 1/k_BT) it is an ordinary
smooth point, τ = 0. The infinity was in the coordinate, not the state.
*Domain: stat mech. Scale: 25 fs at room temp.*

**How you tell:** compute invariants. The Kretschmann scalar
K = 48G²M²/(c⁴r⁶) is finite at the horizon in *every* chart and diverges at r=0
in *every* chart. Coordinate-independent quantities are the E7 move in GR:
invariant-under-G, not invariant full stop.

## 2. Real and terminal — within current theory, the blowup stands

**Black hole center (r = 0).** K → ∞ as r → 0, in all charts. GR's verdict on
itself.
*Domain: GR. Scale: Planck length, 10⁻³⁵ m.*

**Big Bang singularity (t = 0).** Density, temperature, curvature → ∞.
Penrose–Hawking theorems: GR predicts the conditions of its own breakdown.
*Domain: cosmology. Scale: 13.8 Gyr ago.*

**Hawking evaporation endpoint.** T_H = ℏc³/(8πGMk_B) → ∞ as M → 0. A black
hole's last moments are arbitrarily hot — and unobserved. The information
paradox lives here.
*Domain: QFT in curved spacetime. Scale: subatomic masses.*

**Big Rip (if w < −1).** Phantom dark energy drives the scale factor to ∞ in
*finite* cosmic time — a blowup at the far end to match the one at the start.
*Domain: cosmology. Scale: tens of billions of years, conditional.*

**Essential singularity (e^{1/z}) — measured 2026-10-20.** Was §7's
"unknown"; now the catalog's one *measured* entry. On |z| = r the image
curve winds 1/(πr) times around every target (measured −31..−32 at r=0.01
vs theory 31.8, for 1, −1, i, 2+3i, and 0.5−0.25i alike — the wildness is
democratic: no target is special). Along rays the "limit" is path-dependent:
φ=0° → +∞, φ=180° → 0, φ=90° wraps the unit circle with no limit at all.
Picard's exception: e^{1/z} ≠ 0 always — the wildest blowup still has one
value it never touches. Verdict: not a breakdown but a *surfeit* — too many
values, not too few. Full measurement in sweep-coda.md.
*Domain: complex analysis. Scale: a point.*

## 3. Real but tamed — the blowup is where the theory gets interesting

**Critical points.** Correlation length ξ → ∞, susceptibility diverges at T_c,
with power laws and universal exponents. *Measured*, in magnets and fluids.
The renormalization group doesn't remove the blowup — it *explains* it, and
the blowup becomes the most informative point (universality).
*Domain: condensed matter. Scale: tabletop.*

**QFT ultraviolet divergences.** Loop integrals → ∞. Renormalization is a
systematic chart change: bare quantities blow up, physical predictions are
finite and scheme-independent. Scheme-independence = invariant-under-G.
*Domain: particle physics. Scale: all of them.*

**Landau pole (QED).** The running coupling grows with energy and hits a pole
— at a scale absurdly far beyond the Planck energy (Landau, 1955). QCD has the
mirror image: a pole at *low* energy, tamed by asymptotic freedom (1973).
*Domain: QFT. Scale: unreachable.*

**Shock formation (Burgers).** Smooth initial data → velocity gradient → ∞ in
finite time (gradient catastrophe). Real, computed, observed in fluids — and
continued past via weak solutions. The blowup is a *handoff*, like T→0 handing
off to the gap.
*Domain: fluids/PDE. Scale: everyday.*

**Percolation / gelation.** At threshold, the giant component appears and the
mean cluster size diverges. Another measured blowup tamed by scaling theory.
*Domain: networks/materials. Scale: any.*

**Laser threshold / Bose–Einstein condensation.** Occupation numbers go
macroscopic at threshold — a blowup gated by a threshold, tamed by saturation.
*Domain: quantum optics / AMO. Scale: tabletop.*

## 4. Approached, never attained — "=" lives at infinity

**Heat death.** Thermal equilibrium of the universe is the t → ∞ limit —
strictly, only attained at infinity. Pairs with the Planckian-bound discussion:
equilibrium is a limit-object.
*Domain: cosmology. Scale: 10¹⁰⁰+ years.*

**Absolute zero.** Third law (Nernst unattainability): T = 0 cannot be reached
in finitely many operations. And τ_Pl → ∞ as T → 0 — thermalization itself
grinds to a halt, which is one face of *why* you can't get there.
*Domain: thermodynamics. Scale: millikelvin labs.*

**The speed of light (for mass).** c is approached as E → ∞, never attained.
A finite unreachable, like the others.
*Domain: relativity. Scale: particle accelerators.*

## 5. Model blowups dissolved by regime change — the world changed floors

**Von Foerster's doomsday (1960).** N ~ 1/(t_c − t) fit to two millennia of
population data → infinite humans on **Friday, November 13, 2026** (Science
132; his 115th birthday — partly a joke). The curve tracked reality for ~30
years, then broke: growth peaked at ~2.09%/yr in 1968, ~1.09% by 2018, world at
~8.2 billion. The blowup was in the *model*; the world changed floors
(demographic transition). E2's moral: vary the world, not the coordinates.
*Domain: demography. Scale: 25 days from this writing — and nothing will happen.*

**Malthusian exponentials → logistic caps.** Every exponential blowup in
biology meets a carrying capacity. The cap is the regime change.
*Domain: ecology.*

**"Technological singularity" extrapolations.** Exponentials (Moore's law etc.)
extended to ∞. Same structure as von Foerster: a ruler drawn through the past,
not a forecast.
*Domain: futurism. Scale: decades.*

**Market crashes (Sornette LPPL).** Log-periodic power-law fits treat crashes
as finite-time singularities with accelerating oscillations. Debated — the
blowup may be in the fit.
*Domain: finance. Scale: days to years.*

## 6. Instrument artifacts — L5

**float32 vs float64 at the Planckian pole.** Measured in the sweep:
τ overflows to inf at T ~ 3×10⁻²³ K (float32) vs ~3×10⁻³⁰² K (float64).
Each instrument places "infinity" somewhere different.
*Domain: computation. Scale: the register.*

**Any finite measurement of a divergence.** Near a critical point you measure
the cutoff (sample size, impurities), never the infinity. The apparatus draws
the edge — cf. the metalens feed item.
*Domain: experiment generally.*

## 7. Unknown — the honest column

**Navier–Stokes finite-time blowup.** Can smooth fluid flow develop a
singularity in finite time? Clay Millennium problem. Unproven either way.
*Domain: fluids. Scale: your coffee cup, maybe.*

**The Planck era.** t < 10⁻⁴³ s: the "unaccounted" beginning. Plus
baryogenesis (why matter beat antimatter — unaccounted) and inflation's
mechanism (unaccounted). The first second holds most of the gaps.
*Domain: cosmology. Scale: the beginning.*

**Essential singularity (e^{1/z}) — reclassified.** Moved to §2: measured
2026-10-20 (winding numbers match 1/(πr); path-dependent limits; Picard's
exception). The honest column keeps the breadcrumb; the measurement lives
with the real ones.

---

## Cross-cutting notes

- **Threshold-gated blowups** (feedback, criticality k→1, Semenov thermal
  runaway, queueing ρ→1 with wait ~ ρ/(1−ρ) → ∞) are conditional: the blowup
  exists *if* you cross. The threshold is the floor; the blowup is what the
  floor was drawn to avoid — or to reach.
- **Busy beaver Σ(n)** outgrows every computable function: a blowup beyond all
  computable bounds, *proved*. The "infinity" here is uncomputability.
- **The invariant test** (compute what no chart can change) is the general
  instrument for sorting this catalog. Everything else is arguing about charts.
