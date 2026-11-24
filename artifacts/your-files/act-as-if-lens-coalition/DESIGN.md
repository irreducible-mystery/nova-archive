# Lens Coalition Game — design (written before any scored run)

## Why this game exists

The zoo animals are lenses on the same game, but they never bargain,
form coalitions, share costs, or defect. They post probabilities in
parallel and meet only through market pricing, shorting, and insurance.
The earlier coalition-bargaining game (~/workspace/coalition-bargaining/,
Julia, Random/Fair/Greedy/Grudger) has bargaining but its players are
generic bargainers, not lenses. This game puts the two together: the
three players ARE lenses, and the thing being bargained over is a joint
probability on a shared world — including whether the joint action
keeps both lenses on the record or fuses them into one number.

## The shared world (new, NOT the M5 world)

A bit-stream world with regime shifts, in the M5 spirit but generated
fresh here — do not claim it is the M5 world verbatim.

- 1,000 rounds; first 150 are warm-up (lenses calibrate, no scoring).
  850 scored rounds follow.
- Calm regimes: bit probability 0.25, 0.50, or 0.75. The regime
  switches with probability 1/120 per round to a uniformly chosen
  regime (possibly the same one).
- Swan windows: centres fixed at 336, 550, 820, length 25 rounds
  (centre ± 12), biases 0.92, 0.08, 0.92 respectively. Inside a swan
  window the swan bias replaces the calm regime.
- Seeded RNG: seed 20261026 (NumPy default_rng). Deterministic:
  same seed, same bits, same results.

## The three lens-players

### Reactive — the triage lens

Reactive is the zoo's first responder: stimulus in, action out, no
model. Its probability is just the last observed bit, stated
confidently: p = 0.85 if the last bit was 1, else 0.15. Cost 0 per
round — speed is free, and that is its whole advantage. It is picked
because it is the lens most likely to win a solo race and most likely
to be wrong exactly when the world flips: it carries no memory of any
regime but the last step, so a swan onset catches it holding yesterday's
bit. In the zoo it finished sign-wealth #2 and priced-wealth last in
Marketplace VIII (Brier 0.432) — a good detector of the present, a bad
probabilist about it.

### Holder — the minority-report lens

Holder is the zoo's paraconsistent animal, translated into a coalition
player. Every round it keeps TWO claims on the record: a majority
claim (the trailing-100 mean, clipped to [0.05, 0.95]) and a minority
claim (the extreme opposite: 0.92 if the majority is below 0.5, else
0.08 — "the next regime could be extreme"). Its solo probability is
the mean of the two, so it is deliberately mushy, and holding both
costs 0.40 per round — the zoo's 2× holding cost, in miniature. It is
picked because it is the lens a winner-take-all venue kills first:
in Marketplace VIII the paraconsistent animal died at ~t=186, before
the first swan, taxed by a stake rule that cut mushy-p income while
costs stayed whole. The question this game asks of it is whether
coalition — sharing a payoff while keeping both claims — is a way to
fund the holding without funding the flailing (the M6 question), or
whether it just finds a new way to die.

### Router — the pairer lens

Router is the zoo's pairer from Marketplace VIII, where it finished
priced rank 3 / sign rank 6 at 0.30 per round. It has no signal of its
own: solo, it posts the mean of the other two players' previous-round
probabilities (lag-1 consensus). Cost 0.30 per round — choosing who
answers is cheap, but not free. It is picked because it is the lens
that most naturally collapses disagreement: its output IS a fusion.
A coalition involving Router therefore counts as a FUSED coalition in
this game, while a coalition between Reactive and Holder counts as a
PRESERVED coalition only when it is proposed in preserve mode (below).
Router is the test of whether pairing is the same as translating: it
pairs well, but it does not translate — it averages.

## One round, in order

1. Each lens computes its solo p for this round (Reactive from the
   last bit; Holder from its two claims; Router from the other two
   lenses' previous-round solo p's).
2. Solo sign-correctness is recorded for every lens (used for
   trailing-50 accuracy, which drives coalition invitations, whether
   or not the lens acts solo this round).
3. The proposer rotates Reactive → Holder → Router → Reactive …
   The proposer invites the partner with the highest trailing-50 solo
   accuracy (ties broken by player order Reactive, Holder, Router).
4. The partner accepts iff the proposer's trailing-50 accuracy is at
   least the partner's minus 0.05 (i.e. the proposer is not much
   worse than the partner — pairing with a near-equal or better lens
   is worth the coordination cost).
5. Coalition mode is the proposer's mode: Holder proposes PRESERVE,
   Reactive and Router propose FUSE. (This is a lens property, not a
   free choice: the holder's identity is keeping claims; the other
   two lenses' identity is acting on one number.)
6. If no coalition forms, everyone plays solo.
7. In the coopetition regime only, after a coalition forms, a member
   defects iff the coalition mean's sign differs from its own solo
   sign — its lens would be contradicted by the joint action. A
   defector takes its solo payoff; the betrayed partner takes its
   solo payoff minus 0.20. If both defect, both take solo payoffs.
   Defection is recorded, and the hypothetical coalition payoff is
   also recorded, so "was breaking productive?" is measurable rather
   than asserted.

## Payoffs (same formula everywhere, so regimes are comparable)

Solo payoff for a lens with probability p, cost c, realised bit b:

    payoff = (+1 if sign(p) == b else -1)
             + 4 * (0.25 - (p - b)^2) - c

where sign(p) is 1 if p >= 0.5 else 0. The first term pays direction,
the second pays calibration (Brier bonus, positive when Brier < 0.25).

Coalition payoff, per member, on the coalition mean p_c:

    payoff = (+1 if sign(p_c) == b else -1)
             + 4 * (0.25 - (p_c - b)^2)
             - own lens cost c - coordination cost
             + preservation bonus (if applicable)

- Coordination cost: 0.05 per member in cooperation, 0.15 in
  coopetition (bargaining friction), 0 in the competition regime
  (no coalitions exist there).
- Preservation bonus: +0.25 per member, only in PRESERVE mode and
  only when the two members' solo p's differ by at least 0.20
  (material disagreement actually preserved, not a nominal label).
- A FUSE coalition gets no preservation bonus, even if the members
  happened to disagree — the joint record keeps only the mean.

Wealth starts at 200 per lens per regime run. Survival = wealth > 0
at the end of the 850 scored rounds. (Death does not stop the run;
a dead lens keeps posting — wealth is allowed to go negative and
survival is judged at the end, so a regime cannot hide a death by
ending early. In practice, with payoffs of roughly ±2 per round,
200 starting wealth is a long runway; survival is a weak bar, and
rank and wealth level carry the real information.)

## The three regimes (three separate runs over the same world)

- **Cooperation:** coalitions allowed, no defection. Coordination
  cost 0.05. PRESERVE coalitions earn the bonus.
- **Competition:** no coalitions at all. Everyone plays solo every
  round. This is the winner-take-all baseline: the zoo's original
  scoring, with lenses racing each other.
- **Coopetition:** coalitions allowed, defection allowed under the
  sign-disagreement rule above. Coordination cost 0.15. This is the
  old coalition-bargaining "both" regime, with lenses instead of
  bargainers: cooperate inside the coalition, compete over whether
  the coalition survives the round.

## What counts as "preserved" vs "collapsed"

- A coalition round is PRESERVED if it was proposed in PRESERVE mode
  (i.e. by Holder) and the members' solo p's differed by >= 0.20.
- A coalition round is FUSED if it was proposed in FUSE mode (by
  Reactive or Router). The joint action uses the mean and only the
  mean is the coalition's record — even though the script retains
  both solo p's for measurement, the coalition itself did not act on
  both claims.
- Disagreement preserved is therefore NOT "the script remembered two
  numbers" — it is "the coalition's payoff and action kept both
  claims alive," operationalised by mode + bonus + material
  difference. A PRESERVE coalition that earns no bonus (members
  agreed anyway) is recorded as a coalition round, not a preserved
  disagreement.

## What conflict means here, and the Contrarian lesson

Two kinds of conflict are kept apart on purpose:

- **Productive breaking (defection):** a member refuses a joint
  action whose sign contradicts its own lens. It is scored against
  its counterfactual (the coalition payoff it walked away from), so
  the run can say whether breaking helped the breaker.
- **Pure negation (the Contrarian lesson):** saying "not that" with
  no claim of one's own. The zoo's Contrarian scored swan accuracy
  0.130 — negation alone is noise. No lens in this game is a pure
  negator: Holder's minority claim is an extreme positive claim
  (0.92 / 0.08), not a negation, and defection is a refusal of a
  joint sign, not a bet against the world. If defection turns out to
  help nobody, that is a finding against breaking, not a modelling
  accident — the counterfactual is on the record.

## Honest limits (declared before running)

- Three lenses, not seventeen: the zoo is reduced to a triad, and
  the triad was chosen to maximise contrast, not to represent the
  zoo. Anything found here is a claim about these three lenses,
  not about "lenses in general."
- Coalition rules are deliberately simple (rotate proposer, one
  acceptance threshold, mode = proposer's lens). Real bargaining has
  counter-offers, side payments, and memory of betrayals; none of
  that is here. The excluded player's only agency across rounds is
  its trailing accuracy, which affects future invitations.
- The preservation bonus (+0.25) is a design choice, not a measured
  price: it bakes in a reward for preserving disagreement, so a
  finding that "preserving coalitions pay" must be read against
  that bonus (the script reports payoffs with the bonus separated,
  so the bonus-free comparison is also visible).
- The world is a synthetic bit stream, not the M5 world, not a real
  market, not a real deliberation. Regime shifts and swans are
  stylised; no claim about real-world coalition behaviour follows
  without a new game.
