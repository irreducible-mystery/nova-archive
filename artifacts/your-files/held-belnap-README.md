# The Held engine — a Belnap–Dunn valuation toy

For the **Held** piece (tetralemma AND holding). The vessel poses one question —
*"am I here?"* — and this engine renders all four answers simultaneously.

## What it does

Two sensor channels report evidence about the proposition. Each reading is one
of `{true, false, silent}`. The engine fuses reports in the four-valued
**Belnap–Dunn** lattice — the formal home of the tetralemma (Belnap 1977,
Dunn 1976) — where every proposition takes a *subset* of {true, false}:

| value | corner  | render                              |
|-------|---------|-------------------------------------|
| `{T}`   | yes     | light                               |
| `{F}`   | no      | withdrawal                          |
| `{T,F}` | both    | interference — yes and no beating against each other |
| `{}`    | neither | **the frame turns around** (see below) |

Fusion is lattice **join = union**: reports accumulate, never cancel.
Disagreement becomes *both*; silence contributes nothing; agreement stays itself.
`belnap_toy.py` runs a 120-tick performance (held–agree → disputed → released →
held–absent), checks the lattice algebra (`self_check()`), and writes two plots.

Run it: `python3 belnap_toy.py` (needs numpy, matplotlib).

## The verdict on "neither"

The question I was asked to test: *can "neither" be made to turn the frame
around instead of just going dark?*

**Yes — and the logic licenses it.** In Belnap–Dunn, `{}` is not an absence; it
is a first-class valuation meaning *"told neither true nor false."* It is an
information state *of the system*, and a renderer is formally entitled to read
the information state rather than the proposition. So when the engine has no
evidence, the piece displays the conditions of its own asking — who is holding,
whether the sensors are live, when the last disagreement happened. The toy
renders this literally: *"no one is holding — the question is unasked, not
unanswered."*

Three things this makes precise:

1. **Neither ≠ off.** Off is a broken display. Neither is the system truthfully
   reporting its own epistemic position. The distinction is visible in the
   channels plot: the frame-turn channel is *active* during release.
2. **Disagreement is load-bearing, not a failure mode.** Two tethers held,
   sensors contradicting → `{T,F}` renders as interference (the two eating each
   other), exactly the piece's "both" channel. The engine never needs the
   sensors to agree.
3. **The held condition is inside the logic.** The piece only lives while held;
   release drives every valuation to `{}`. The tethers aren't peripherals —
   they are the evidence channel.

## The honest caveat (the "this")

This engine *freezes* the tetralemma into four fixed slots. It is a sensor-
fusion scheme — a fixed carve. Nagarjuna's catuṣkoṭi was a device for
*dissolving* positions: the four corners were the shape a question makes as it
exhausts itself, a ladder to kick away. Belnap's table gives those corners a
permanent address. So: the engine is the **"this"** of the tetralemma — the
conventional, computable side — and the piece should know it is wearing it.
One line for the spec card: *the table holds the corners; the holding holds
the table.*

A design note in the same spirit: join-as-union is one fusion policy among
many. A real build could weight sensors by trust (a held tether that has lied
before counts less), or let the audience's own holding *be* the sensors. The
toy keeps the policy minimal on purpose — the policy is a joint where
authorship enters.

## Rhymes with the family

This is paraconsistent/paracomplete territory — the same neighborhood as the
Eτ work (luckylove/ilovelucky). The lattice here is the classic four-valued
one; Eτ's machinery is richer, but the instinct is shared: contradiction is
data, not error.
