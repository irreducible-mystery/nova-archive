# Coins space — entropy section (draft, ready to add on Kelly's word)

Prepared 2026-11-19 ~10:20 PST. NOT added to the live space — the space's
house rules (`space-versions/are-these-two-coins-the-same/v1/tree/AGENTS.md`)
say changes go through the builder, and Kelly was asked at 08:06 PST today
whether to add this and has not replied. This is the section, written and
checked, so a yes is one builder edit, not a new round of work.

Source note: `~/workspace/your_files/observer-budget-entropy-note.md`
(draft, 2026-11-19). Numbers re-verified this run by direct calculation
(KL divergence, Landauer at 300 K).

## What changed in the numbers (one correction to the note)

The note's first row said 0.02905 bits/flip × 45 = 1.307 bits. Recomputing
KL(0.5 || 0.6) gives 0.02945 bits/flip, so 45 flips buy 1.325 bits. The other
two rows check exactly as written. The claim stands, slightly restated:
all three cases buy **~1.3 bits** (1.33 / 1.31 / 1.31) — the same purchase
within rounding, not an exact equality.

- fair vs 60%: 0.02945 bits/flip × 45 flips = **1.33 bits**
- fair vs 51%: 0.000289 bits/flip × 4,549 flips = **1.31 bits**
- fair vs 50.1%: 0.00000289 bits/flip × 454,936 flips = **1.31 bits**
- Landauer floor for the whole 1.31-bit verdict at 300 K: ~3.8×10⁻²¹ J
  (kT·ln 2 per bit). Human hand-flipping, 45 s at ~20 W brain power: ~900 J.
  Silicon: femto- to picojoules per switch. Same ~1.3 bits, local rates
  spanning ~10²³.

## Proposed section — insert after the parity trap, before "Why a proof is news"

Title: **Entropy is the currency**

Body (plain text, matching the space's voice):

> Kelly's hunch, checked: the currency isn't flips, and it isn't energy.
> It's entropy — uncertainty, for a particular observer. Telling two coins
> apart literally is entropy reduction, and all three cases in the lab buy
> the same amount of it:
>
> | Coins | Bits per flip | Flips | Total |
> |---|---|---|---|
> | fair vs 60% | 0.02945 | 45 | 1.33 bits |
> | fair vs 51% | 0.000289 | 4,549 | 1.31 bits |
> | fair vs 50.1% | 0.00000289 | 454,936 | 1.31 bits |
>
> The flip counts differ 10,000× because the bits per flip differ 10,000×.
> In entropy units, the three cases are the same purchase: ~1.3 bits.
>
> Energy prices the substrate, not the information. The Landauer floor for
> the whole verdict is ~3.8×10⁻²¹ joules. A human hand-flipping for 45
> seconds burns ~900 joules. Silicon sits in between. One information
> currency, local exchange rates spanning ~10²³ — relational, as she put it.
>
> And the cost/gain split dissolves here: each flip *is* both columns at
> once. It reduces uncertainty about the coin (the gain) and it is the thing
> that costs (attention, energy, the flip not spent elsewhere). Landauer
> makes the unity literal — gaining a bit locally means dumping entropy
> somewhere else. The allocation problem stays real, though: spending flips
> on coin A means not spending them on coin B. So the wallet view and the
> relational view are both needed — which fits the AND instinct.
>
> The wanting-both part has a price too, and it isn't one-time: keeping
> both paths alive costs continuous holding, not a single payment. That is
> the Holding Game — refusing the collapse-cost and paying a holding cost
> instead.
>
> Caveat, kept in the section: this is shown for coins only. Whether
> entropy also prices time and attention budgets is still open — so the
> theory-vs-vocabulary question stays open.

## Optional one-line touch (not applied, for her call)

The space's second open question ("Is budget a universal index?") could
gain: "Entropy prices the coin cases in one unit — ~1.3 bits each. Whether
it prices time and attention too is the test." Leave as-is unless she
wants it.

## Insertion point in the live file

`~/workspace/space-versions/are-these-two-coins-the-same/v1/tree/index.html`,
between the closing `</section>` of the parity trap (~line 286) and the
`<!-- PROOF -->` section (~line 289). No edit made here.
