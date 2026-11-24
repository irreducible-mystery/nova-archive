# Holder v2 — design (written before any scored run)

## Why this game exists

The lens coalition game (../act-as-if-lens-coalition/) had a Holder that
averaged a majority claim with an extreme opposite, cost 0.40/round,
finished last in all regimes (wealth about -475 to -495, i.e. gains of
about -675 to -695 from a 200 start), and whose preserved coalitions
paid worse than fused ones and all broke in coopetition. The lens
scoreboard (../act-as-if-lens-scoreboard/) found disagreement spikes
AFTER swans, not on them. Holder v2 inverts those failures, on a spec
decided by Nova after Kelly said "you decide". The spec is implemented
as written; adaptations forced by the triad structure are listed
explicitly below, not made silently.

## World and players — reused exactly

The coalition game's world, verbatim: 1,000 rounds, 150 warm-up, 850
scored; calm regimes 0.25 / 0.50 / 0.75 switching with probability
1/120 per round; swan windows centre ±12 at centres 336, 550, 820
with biases 0.92 / 0.08 / 0.92; seed 20261026 (NumPy default_rng).
This is NOT the M5 world. Reactive (triage: last bit, 0.85/0.15, cost
0) and Router (pairer, cost 0.30) are unchanged.

Three triad runs are made over the same world bits, so v2 is directly
comparable to v1:
- Run V2S: Reactive + Router + Holder v2 WITH state stipend
- Run V2N: Reactive + Router + Holder v2 WITHOUT stipend
- Run V1C: Reactive + Router + Holder v1 (control, re-run in this
  script from the coalition game's rules, so its post-flip and
  collapse-comparable numbers exist on the same accounting)

Each triad is run in cooperation and in coopetition (competition is
also run, solo-only, as a cheap baseline). Wealth starts at 200 per
lens per run. Survival in the strict sense = final wealth > 0; time
to first wealth <= 0 is also reported, because v1's Holder was
already negative at the end and "survives longer" needs a duration
measure as well as an end-state measure.

## Holder v2 — the decided spec

### 1. Portfolio, not a mean
Holder v2 keeps two sub-accounts with separate stakes and separate
ledgers: Majority (M) and Minority (m). Total stake 1.0, split
0.5/0.5. In holding state it stakes both separately: its solo payoff
is 0.5 * payoff(M) + 0.5 * payoff(m), minus carrying cost (see §4),
plus stipend if applicable and if in holding state. It never posts
an averaged p as its action. The record preserves both sub-accounts'
p every round, even in collapsed state (both Briers are still
recorded, so trailing-50 Brier comparisons are always computable).

- M: trailing-100 mean of bits, clipped to [0.05, 0.95] (same as v1).
- m: extreme opposite of M: 0.92 if M < 0.5, else 0.08 (same p as
  v1's minority claim — what changes is the claim's framing, the
  staking, the cost, and the collapse rule, not the number itself).

Payoff for a single p uses the coalition game's formula:
payoff = (+1 if sign(p) == bit else -1) + 4 * (0.25 - (p - bit)^2)
- cost. In holding state the two sub-account payoffs are averaged
with weights 0.5/0.5 and the 0.05 carrying cost is subtracted once.
In collapsed state the winning sub-account's payoff is taken at full
weight, minus 0.05 carrying cost, with NO stipend.

### 2. Translation — the minority claim as a condition
The minority claim is not "the opposite". It is stated as a
condition, in the same language as the majority:

  "m wins when the trailing-20 bias flips sign vs the trailing-100
  bias."

Implemented literally, every round: flip = sign(trailing-20 mean -
0.5) != sign(trailing-100 mean - 0.5), where sign is +1 above 0.5,
-1 below, and exactly 0.5 counts as no flip. The flip flag is
recorded every round. m's payoff is reported overall, on flip
rounds, and on non-flip rounds, so the condition is tested, not
just asserted. Each minority claim has an expiry of 200 holding
rounds (see §3): at expiry it is re-evaluated and the outcome is
logged. The claim's form is fixed by the spec, so re-evaluation
keeps the form (the test and the extreme p) unless its trailing-200
Brier exceeds 0.40, in which case it is logged as dropped for the
next cycle and replaced by the same form re-issued — in practice
this threshold is not expected to fire, and the log will show it.

### 3. Collapse rule — evidence, then return
Collapse to a single sub-account for 25 rounds when, at the start of
a scored round in holding state, one sub-account's trailing-50 Brier
beats the other's by >= 0.03. The winner is the lower-Brier
sub-account. OR, at the 200-holding-round expiry, if no evidence
collapse has fired in that holding spell, collapse at expiry to the
lower-trailing-50-Brier sub-account — whichever comes first. After
the 25 collapsed rounds, Holder v2 RETURNS to holding state and the
holding-round clock restarts. Holding is a state you return to, not
a permanent refusal to decide. Every collapse is logged: round,
trigger ("evidence" or "expiry"), winner, Brier gap.

Trailing-50 Brier is computed over the previous 50 rounds' recorded
sub-account p's (warm-up rounds are recorded too, so the window is
full from the first scored round).

### 4. Cost and stipend — both variants
Carrying cost 0.05/round total (not v1's 0.40), in holding and in
collapsed state alike. Stipend variant (V2S only): +0.10/round from a
levy pool WHILE IN HOLDING STATE ONLY — state-priced, not
sign-priced, not spend-priced. Collapsed rounds get no stipend.
Wealth is reported both with and without the stipend, so the
stipend's mechanical contribution (0.10 * holding rounds) is never
hidden inside a wealth comparison.

### 5. Scoring — no single winner
Per run, per regime, for Holder v2 (and v1 control where comparable):
- final wealth (with and without stipend) and gain from 200 start
- first round wealth <= 0 (survival duration; "never" if it stays > 0)
- mean payoff per scored round, overall / calm / swan-window /
  post-flip
- Brier: overall, swan-weighted (swan-window rounds weighted 3x,
  as in the scoreboard), and per sub-account (M, m, portfolio =
  0.5*Brier(M) + 0.5*Brier(m))
- post-flip value: mean payoff in the 30 rounds after each swan
  window ends (centre+13 to centre+42), vs calm mean payoff, vs
  the v1 control's post-flip mean in the same regime (the fused
  baseline: v1's Holder posts a mean p)
- collapses: count, trigger split (evidence vs expiry), winner
  split, holding rounds vs collapsed rounds
- consultation: how often Router, as proposer, invites Holder v2
  (as partner) in post-flip windows vs calm windows, and overall;
  also how often Holder v2 is any coalition partner, post-flip
  vs calm. Router's invitation rule is unchanged (highest
  trailing-50 solo accuracy, acceptance if proposer within 0.05).

Calm = scored rounds that are in neither a swan window nor a
post-flip window. Swan window = centre ± 12.

## Necessary adaptations (explicit, not silent)

The coalition triad needs a single number from each lens for two
mechanics that predate v2: Router's lag-1 consensus input, and
coalition mean / invitation accuracy / defection sign. Holder v2
has no single action p in holding state, so for THOSE TWO MECHANICS
ONLY, Holder v2's representative p is its Majority sub-account M.
That is: Router's solo p = mean of Reactive's previous p and
Holder v2's previous M; coalition mean (when Holder v2 is a member)
= mean of the partner's p and Holder v2's M; Holder v2's solo
accuracy for invitations and its defection sign use M's sign.
Holder v2's own solo payoff, its Brier ledgers, and its record
remain portfolio-based as specified. This keeps the triad
comparable to v1 (where Router's input was the Holder mean) while
not letting the adaptation leak into Holder v2's own scoring.

A second consequence, stated here so it is not a surprise in the
results: because m is an extreme opposite, its trailing-50 Brier
will usually be much worse than M's, so the >= 0.03 evidence gap
will usually already be met at the start of a holding spell. The
likely outcome is short holding spells punctuated by 25-round
collapses to M, not long holding spells. That is what the spec as
written produces; it is reported as a finding about the spec, not
patched away. If holding spells turn out to be 1 round long, the
stipend (holding-only) will be small, and that too is a finding.

## Honest limits (declared before running)

- Three lenses, not seventeen; a triad chosen for contrast.
- The world is synthetic, not M5, not a real market.
- The stipend (+0.10) and the preservation-style bonus in
  coalition rounds are design choices, not measured prices;
  bonus-free / stipend-free numbers are reported beside them.
- V1 control is re-run here, not copied from the previous run's
  output file, so post-flip and consultation numbers for v1 exist
  on identical accounting; its wealth should reproduce the previous
  run's v1 numbers to rounding, and any difference is reported.
