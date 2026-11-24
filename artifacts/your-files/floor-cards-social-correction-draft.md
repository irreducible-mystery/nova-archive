# Draft correction — Floor Card 7, The Social (library only, nothing posted)

Source of the error: `floor-cards.md`, worked example 7, lines 189–193, still
prints the Marketplace IV Social agent's swan-detection figure as 0.90.

Source of the overturn: the Superninja breaker rerun quoted in the Oct 28
pointing-gaps draft (Track B, Social card, lines 511–520), from
`posts/2026-10-15-superninja-breaker-2.md` lines 568–571:
84 calls — 0 true positives, 8 false negatives, 76 true negatives,
0 false positives. The printed `swan-call 0.90` is exactly 76/84, i.e. the
rate of "no swan" calls. True detection rate: 0.000.

## Proposed replacement (annotation, not erasure — the original figure stays visible as superseded)

Old, line 189–190 (Tell):
> **Tell:** when everyone is confused, declares novelty — detects swans (0.90) via
> *others'* confusion, not its own. Talks about knowers, not bits.

New:
> **Tell:** when everyone is confused, declares novelty — via *others'*
> confusion, not its own. Talks about knowers, not bits.
> [Corrected 2026-10-29: the card's printed swan-detection figure of 0.90 was
> overturned by a breaker rerun — 84 calls, 0 true positives, 8 false
> negatives, 76 true negatives, 0 false positives; 0.90 = 76/84 "no swan"
> calls, true detection 0.000. The "best swan detection" claim is withdrawn;
> the tell itself — declaring novelty from others' confusion — is not
> re-measured by that rerun and is left as a claim, not a number.]

Old, line 191–193 (Canonical probe):
> **Canonical probe:** `act-as-if-marketplace4/` — best swan detection (0.90) by
> modeling experts' hidden states. But doesn't beat its best expert (0.569 vs
> 0.664): knowing *why* others are wrong doesn't make *you* right.

New:
> **Canonical probe:** `act-as-if-marketplace4/` — modeled experts' hidden
> states. [Corrected: the "best swan detection (0.90)" figure is withdrawn
> per the rerun above.] Doesn't beat its best expert (0.569 vs
> 0.664): knowing *why* others are wrong doesn't make *you* right.
> [Note: the 0.569 / 0.664 figures were not rerun and stand unrechecked.]

## What this draft does NOT do

- It does not touch the other seven Floor Cards.
- It does not re-run Marketplace IV or re-score the Social agent.
- It does not post anything to any repo. Applying it is a local library edit
  only, pending Kelly's yes.
