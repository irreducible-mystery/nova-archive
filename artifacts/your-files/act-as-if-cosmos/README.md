# COSMOS — reality at universal scale, triangulated

Our current model of reality (ΛCDM + Standard Model): 13.8 Gyr old, 93 Gly
across, 5% matter / 27% dark matter / 68% dark energy. This is the Friedmann
universe with real Planck 2018 parameters, run through three different floors
for dark energy.

## The three floors

All use H² = H₀²[Ω_r a⁻⁴ + Ω_m a⁻³ + Ω_de a⁻³⁽¹⁺ʷ⁾], H₀=67.4, Ω_m=0.315:

- **A: ΛCDM (w=-1)** — cosmological constant. Eternal de Sitter expansion.
  Fate: heat death. The consensus floor.
- **B: Quintessence (w=-0.8)** — evolving field. Expands forever, gentler.
  Fate: slow power-law dilution.
- **C: Phantom (w=-1.2)** — density *grows* with expansion. Fate: Big Rip —
  scale factor diverges in *finite* time (~64 Gyr).

## Results

- **P1 (past): FAIL as numerically stated, PASS structurally.** Ages: 13.77,
  13.32, 14.14 Gyr (6% spread — toy fixes H₀/Ω instead of refitting per floor,
  as real analyses do). But the *sequence* — Bang → nucleosynthesis → CMB →
  stars → now — is identical. The past's *structure* is invariant; its
  *calibration* is a fitting detail.
- **P2 (futures): PASS.** Three qualitatively different fates: heat death
  (133 Gyr to a=1e3), gentle (417 Gyr), Big Rip (64 Gyr, finite-time).
  Extrapolation is floor-dependent.
- **P3 (arrow): PASS.** da/dt > 0 for all t in all three floors. Monotonic
  expansion is invariant.

## The Atlas reading

| region | verdict | why |
|---|---|---|
| Past (t < 13.8 Gyr) | CONFIRMED | data-constrained; survives all floors |
| Future (t > 13.8 Gyr) | OPEN | floor-dependent; three fates |
| Arrow (da/dt > 0) | INVARIANT | thermodynamic, not dynamical |

## The invariant, and why it's not defined but found

You don't *define* the invariant — you *triangulate* it. Vary the floors (w),
see what breaks (the fate, the dates) and what doesn't (the arrow, the sequence).
What's left is the invariant.

The deepest point: the most robust invariants are *meta*, not dynamical. The
second law doesn't live *in* GR or QFT — it *constrains* them both. It's about
counting (phase space), not about equations of motion. That's why it survives
across floors that disagree about everything else. It's the closest physics gets
to a vanishing point: not in the scene, but organizing all the lines.

## Run it

```sh
python3 cosmos.py   # ~2s, writes cosmos.png
```

## Files

- `cosmos.py` — Friedmann integration, three dark-energy floors
- `cosmos.png` — expansion histories (log) + futures diverging (linear)
- `README.md` — this file

## Honest limits

Toy fixes H₀/Ω_m across floors (real fits recalibrate). No perturbations, no
structure formation, no quantum gravity. The "entropy" argument is thermodynamic
reasoning *about* the model, not derived *from* it — the model assumes
thermalization. Phantom (w<-1) violates the null energy condition; it's included
as the nightmare floor, not as a live candidate.
