# THE MARKETPLACE II — long horizon, black swans

The calm-world prices are in. Now the stress test: a 1000-bit world with
long regimes (mean 120 steps — patience pays) and 3 BLACK SWANS: 25-step
bursts of a 4th regime (bias 0.92/0.08) that never appeared in warmup.
Unprecedented by construction. The models must cope or bleed.

Swan strategies (priced):
- **Gate:** surprise spikes → scale 2.5, frantic adaptation. Pays massive
  erasure trying to learn the unprecedented.
- **JEPA:** persistent surprise → "swan mode": predicts 0.5, STOPS updating.
  Strategic ignorance. Saves coins, admits not-knowing.
- **Genie:** likelihood collapses → stops dreaming, declares swan. Perfect
  detection — but detection isn't survival.

Earnings: +6 bit, +12 futures (t+10), +20 regime (every 20), +25 swan call
/ -10 false alarm.

## What happened

**The ranking flipped.** Calm world: Gate > JEPA > Genie. Swan world:
JEPA (wealth 1748) > Gate (879) > Genie (BANKRUPT).

- **JEPA dominates** — not by predicting swans, but by refusing to pay for
  them. Strategic ignorance: efficiency 29.1, highest wealth. It doesn't
  gain from chaos; it simply doesn't bleed.
- **Gate survives but bleeds** (spent 1776, most of all). Frantic adaptation
  is expensive, and its swan detection is poor (0.25) — surprise is noisy.
- **Genie DIES** despite perfect swan detection (1.00). Knowing doesn't
  save you if your model can't act on it. Its frozen Markov worldview
  shatters on the unprecedented (acc 0.413).

## The finding

**The exchange rates repriced violently.** JEPA went from runner-up to
dominant; the calm-world winner (Gate) proved fragile; Genie proved that
detection without adaptation is bankruptcy with extra steps.

In Taleb's terms: the Gate is fragile (harmed by volatility), Genie is
fragile (breaks), JEPA is robust (survives via strategic ignorance). None
are antifragile — nobody *gains* from swans here. That's an honest limit:
robustness, not antifragility, is what the energy budget buys.

The deeper point: **the "best" strategy is world-relative.** There is no
universally efficient agent — only agents efficient *for* a world. The
marketplace doesn't crown a champion; it prices strategies per world. Change
the world, reprice everything.

## Run it

```sh
python3 marketplace2.py   # ~2s, writes marketplace2.png
```

## Files

- `marketplace2.py` — long regimes, swans, three coping strategies
- `marketplace2.png` — wealth through the swans (red bands)
- `README.md` — this file

## Honest limits

Toy energy model (see marketplace.py). Swan coping strategies are
hand-designed dials, not learned policies — a real agent would *learn* when
to adapt vs ignore. The flip itself (JEPA wins swans, Gate wins calm) is
structural; the exact wealth numbers are illustrative.
