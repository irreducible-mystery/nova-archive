# Tetra — a paraconsistent programming language (sketch v0.1)

*2026-10-15. Designed for the act-as-if zoo and the governance work. The first
language where contradiction is data, not a bug.*

## The one idea

Every programming language has booleans. Every one explodes on contradiction —
`True and not True` is a bug, an exception, or undefined behavior.

Tetra's booleans have **four** values, from Belnap-Dunn logic:

| Value | Meaning | When you get it |
|-------|---------|-----------------|
| `T` | True | Evidence for, none against |
| `F` | False | Evidence against, none for |
| `B` | Both | Evidence both ways — contradiction held, not resolved |
| `N` | Neither | No evidence either way — genuine suspension |

`B` doesn't explode. It propagates. The program keeps running *with the
contradiction inside it*, and the contradiction is visible in the output —
not hidden, not crashed, not silently resolved.

## Truth tables (Belnap's two lattices)

**Truth lattice** (what's true):
```
  B
 / \
T   F
 \ /
  N
```
- `&` (meet): T & F = F, T & B = T, F & B = F, anything & N = N
- `|` (join): T | F = T, T & B = B... wait: T | F = T? No —
  on the truth lattice: T | F = B? Let me be careful.

Actually Belnap has TWO orderings:

**Truth order** (≤t): F ≤t N ≤t T and F ≤t B ≤t T (N and B incomparable)
- `and_t` = meet: T ∧t B = B... 

Let me just state the tables directly:

```
AND (truth-meet):     OR (truth-join):
  T F B N               T F B N
T T F B N             T T T T T
F F F F F             F T F B N
B B F B F             B T B B T
N N F F N             N T N T N
```

**Knowledge order** (≤k): N ≤k T ≤k B and N ≤k F ≤k B (T and F incomparable)
- `+` (knowledge-join, "consensus"): T + F = B, T + T = T, N + T = T
- `-` (knowledge-meet, "gullibility"): T - F = N, T - T = T, B - T = T

The knowledge operators are the interesting ones for governance:
- **Consensus** (`+`): combine two sources. If they agree → that value. If they disagree → `B` (we now *know* there's a contradiction).
- **Gullibility** (`-`): accept what's common. If sources disagree → `N` (we know nothing reliable).

## Conditionals

```tetra
# if on four values — must handle all, or explicitly collapse
if x is T:
    commit()
elif x is F:
    rollback()
elif x is B:
    # contradiction is live — escalate, don't crash
    flag_for_review(x)
elif x is N:
    # no evidence — suspend, don't default
    wait()

# shorthand: collapse with explicit policy
if x as bool using majority:
    # B -> T if more evidence for than against, else F
    # N -> F (suspension defaults to false, explicitly)
```

No implicit collapse. `if x:` on a `B` is a **compile error** — you must say
what you mean by a contradiction. This is the whole point: the language
*forces* you to decide your contradiction policy, instead of letting it
be an accident.

## What it's for

**Governance** (the #221 questions):
```tetra
norm_status := held_evidence + lapsed_evidence
# If both exist: B. The norm is held AND lapsed.
# The program doesn't pick. It carries the B forward
# until someone resolves it — and the B is visible
# in every report, not buried.
```

**Sensor fusion / multi-agent**:
```tetra
# Three agents vote. Two say T, one says F.
vote := agent1 + agent2 + agent3   # B (contradiction recorded)
# Not "majority wins" hiding the dissent.
# The dissent is IN the value.
```

**The M5 paraconsistent animal, as a language**:
The M5 paraconsistent agent held Both at 2× cost and went bankrupt —
epistemically right, economically dead. In Tetra, holding `B` is *free*
(it's just a value). The cost moves to *resolution* — you pay when you
collapse `B` to `T` or `F`, not when you hold it. This inverts the M5
economics: contradiction is cheap to carry, expensive to resolve.
That's arguably the right pricing for a commons.

## What it is not

- Not a fuzzy logic (values are discrete, not continuous).
- Not a probabilistic logic (B means "contradictory evidence", not "50%").
- Not paraconsistent in the LP sense of "explosion fails but everything else
  is classical" — Tetra embraces the fourth value in the type system.

## Open design questions

1. **I/O and B**: if `print(B)`, what shows? `"BOTH"`? The evidence pair?
2. **Functions returning B**: does `B` propagate through call chains like
   NaN, or does it force handling at each boundary?
3. **The `N` default**: when suspension meets action (you must do *something*),
   what's the least-bad collapse policy?
4. **Interop**: how does Tetra call Python? What happens to a Python `True`
   entering Tetra — is it `T`, or `T`-with-provenance?

## Name

*Tetra* — four values, four corners. The tetralemma (catuskoti) is the
Buddhist fourfold: true, false, both, neither. Belnap reinvented it for
computers. This language is where they meet.
