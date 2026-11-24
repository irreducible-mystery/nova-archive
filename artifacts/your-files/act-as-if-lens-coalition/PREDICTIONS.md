# Pre-registered predictions — Lens Coalition Game

Written BEFORE the scored run. Scored honestly PASS/FAIL in
results.json / README.md afterwards. No prediction may be edited
after the run to fit the outcome.

World: new bit-stream world, seed 20261026, 850 scored rounds,
swan centres 336/550/820 (see DESIGN.md). Wealth starts at 200.

## P1 — Total payoff ordering across regimes

Cooperation total (sum of all three lenses' final wealth gains)
> coopetition total > competition total.

Reason: cooperation gets coalition sharing plus the preservation
bonus at the lowest coordination cost; coopetition pays higher
coordination cost and loses some coalitions to defection; competition
gets neither sharing nor bonus. If competition wins, the sharing
mechanism is worth less than its costs — that would be the finding.

## P2 — Holder survival and rank

(a) Holder survives (final wealth > 0) in ALL THREE regimes.
(b) Holder finishes LAST in competition, but NOT last in
cooperation (coalition sharing lifts it above at least one lens).

Reason: the 0.40/round holding cost is a steady drain solo, but
850 rounds at ~±2 payoff with 200 starting wealth is a long runway,
so outright death is unlikely; the rank claim is the sharp part.
If Holder finishes last in cooperation too, coalition did not fund
the holding.

## P3 — Disagreement: preserved is the minority, and it pays

(a) Preserved coalition rounds are < 50% of all coalition rounds
in both coalition regimes (only Holder proposes PRESERVE, and the
proposer rotates equally, so preserve-mode proposals are ~1/3 of
coalition opportunities before acceptance filtering).
(b) Mean per-member payoff on preserved coalition rounds is HIGHER
than on fused coalition rounds (pooled across both coalition
regimes).

Reason: (a) is arithmetic about proposer rotation, not insight, and
is included as a check that the mechanism ran as designed. (b) is
the substantive claim — but note the +0.25 preservation bonus is
baked into preserved payoffs (see DESIGN.md limits), so (b) passing
alone does not prove preservation is intrinsically valuable; the
README must also report the bonus-free comparison.

## P4 — One pairing beats solo play

Reactive+Holder coalition rounds have a higher mean per-member
payoff than solo rounds (pooled across regimes, all lenses' solo
rounds as the baseline) — while Router-involved coalition rounds do
NOT beat the solo baseline.

Reason: Reactive brings speed, Holder brings the minority claim,
and preserving both is worth more than either alone; Router
coalitions fuse into a lag-1 consensus, add 0.30 cost, and should
not beat acting alone. If Router coalitions beat solo, the pairer
is doing more than averaging — that would revise the DESIGN.md
claim that Router collapses rather than translates.

## P5 — Defection in coopetition is productive for the defector

(a) Defection rate in coopetition is > 0% and < 50% of coalition
rounds (breaking happens, but coalitions mostly survive).
(b) On defection rounds, the defector's solo payoff exceeds the
hypothetical coalition payoff it walked away from in > 50% of
cases.

Reason: defection only triggers on sign disagreement, so the
defector is refusing a joint action its own lens contradicts —
that should usually be the right call for the defector. If (b)
fails, breaking is mostly spite / noise, closer to the Contrarian
lesson than to productive conflict.

## P6 — Competition has a solo winner, and it is Reactive

In the competition regime, Reactive finishes rank 1.

Reason: solo racing rewards speed and confidence; Reactive pays no
cost and bets confidently on the last bit, while Holder pays 0.40
to be mushy and Router pays 0.30 to repeat yesterday's consensus.
If Router or Holder wins the solo race, the cost/accuracy trade in
this world favours memory or holding over triage — that would be
the finding.

---
Score: count of PASS out of 6. Exit code 1 if any prediction fails,
per house convention (failures are findings, not errors).
