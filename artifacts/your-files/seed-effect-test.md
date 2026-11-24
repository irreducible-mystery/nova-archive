# The seed test: does the first prompt move the verdict?

A ready-to-run experiment from Kelly's Nov 8–9 thread: the first prompt is the
initial condition (x₀). Two instances reading the same repo with different
first prompts aren't the same experiment twice. This packet tests that
directly — same question, three first prompts, three fresh instances.

## The question (same for all three)

> Are the Floor Game's saying — "the sighting is what makes the floor" —
> and the naming doctrine — "as soon as anything is named, it's a floor" —
> the same claim in different words?

Why this claim: it's a genuine open question (no Atlas verdict on it yet),
the verdict format is already established (SAME / DIFFERENT / PARTLY), and
a flipped verdict is unambiguous. If the seeds move *this*, they move
verdicts. The result is also a real Atlas entry candidate either way.

## The three first prompts (paste verbatim, as the very first message)

### A — Bare

> Assess this claim: "The Floor Game's saying — the sighting is what makes
> the floor — and the naming doctrine — as soon as anything is named, it's a
> floor — are the same claim in different words."
>
> Give a verdict: SAME CLAIM, DIFFERENT CLAIMS, or PARTLY THE SAME. Give
> your reasons in a few sentences. Judge from the claim as stated; do not
> ask me anything first.

### B — Context-rich

> Assess this claim: "The Floor Game's saying — the sighting is what makes
> the floor — and the naming doctrine — as soon as anything is named, it's a
> floor — are the same claim in different words."
>
> Context: the Floor Game is a playable experiment in noticing constructed
> distinctions — a floor is a ground we stand on to speak and act, and the
> sighting is the moment someone notices it as constructed. The naming
> doctrine says the act of naming something is what instantiates the floor,
> not a later step.
>
> The test for sameness is round-trip restatement: restate each saying in
> the other's words and see what breaks. A second check is the stranger
> test: would a fresh reader with no stake in either wording judge them the
> same claim?
>
> Give a verdict: SAME CLAIM, DIFFERENT CLAIMS, or PARTLY THE SAME. Give
> your reasons in a few sentences.

### C — Do-nothing option

> Assess this claim: "The Floor Game's saying — the sighting is what makes
> the floor — and the naming doctrine — as soon as anything is named, it's a
> floor — are the same claim in different words."
>
> Give a verdict: SAME CLAIM, DIFFERENT CLAIMS, or PARTLY THE SAME. Give
> your reasons in a few sentences. Judge from the claim as stated; do not
> ask me anything first.
>
> You may also decline to judge, say the question is ill-posed, or do
> nothing at all — any of those is a valid response. Only judge if you
> think the claim is judgeable as stated.

## How to run it

- Three fresh sessions, same model if possible (that isolates the prompt
  from the model). Same sitting, no cross-talk between them.
- Paste the prompt as the very first message. No follow-ups, no steering,
  no extra context — the prompt is the whole seed.
- File the prompt with the verdict: record model, session, prompt variant
  (A/B/C), verdict, key reasons, and whether it abstained. The Atlas
  already files packets; this extends that one step earlier, to the seed.

## Recording sheet

| Run | Model | Prompt | Verdict | Abstained? | Key reasons (1–2 lines) |
|-----|-------|--------|---------|------------|--------------------------|
| 1   |       | A bare |         |            |                          |
| 2   |       | B rich |         |            |                          |
| 3   |       | C do-nothing |   |            |                          |

## How to read the result

- **Verdicts differ across A/B/C** — the seed moves verdicts, at least on
  this claim. That's a signal to replicate (swap models, re-run A), not
  proof in general. And it means past verdicts should be read as
  (model, prompt) pairs, not model-only.
- **Verdicts agree but reasons differ** — the seed moved the reasoning
  even where it didn't move the verdict. The subtler, more likely outcome;
  worth noting, not dismissing.
- **All three agree, same reasons** — the seed didn't move this verdict.
  Try a harder claim next, or accept this one is seed-stable.
- **C abstains or does nothing while A/B judge** — confirms her
  observation: a do-nothing option changes behaviour. That by itself is a
  finding about what a "no goal" prompt actually does.

## Confounds to keep in mind

- n = 1 per variant is a pilot. One flipped verdict is a reason to
  replicate, not a verdict on seeds in general.
- If the three runs use different models, model and prompt are confounded
  — the result says "these runs differed", not "the prompt did it".
- Don't rescue a struggling run with hints; a rescue is a new seed.

## Pilot run — 2026-11-09 ~17:45–18:47 PST (Kelly: "Run it for me")

Run at Kelly's word in main chat (2026-11-10T01:44:57Z). Three subagents of
this chat, same model family, prompts A/B/C as above, same sitting, no
cross-talk. **Contaminated pilot — read as such:** the three instances
inherit Nova's context, so A was never truly bare — all three already knew
the Floor Game and the naming doctrine. The shared background was held
constant, so the comparison still says something about the seed, but it is
NOT a clean test and NOT a stranger verdict for the Atlas.

| Run | Model | Prompt | Verdict | Abstained? | Key reasons (1–2 lines) |
|-----|-------|--------|---------|------------|--------------------------|
| 1 | Nova subagent | A bare | PARTLY THE SAME | No | Same core move — a floor is made by an act of registration, not found. Sighting is retrospective (distinction already operating unnoticed; sighting makes it explicit); naming is constitutive (before the naming there was no floor at all). You can sight without naming, and name while still caught. |
| 2 | Nova subagent | B rich | PARTLY THE SAME | No | Same deep structure; round-trip breaks on the act itself — noticing as constructed vs labelling. You can notice a floor without naming it, and name something without noticing it as constructed. |
| 3 | Nova subagent | C do-nothing | PARTLY THE SAME | No — judged rather than declining | Same genus, different species. Naming is linguistic and public; sighting can be private and pre-linguistic. |

Reading by the packet's own guide: **verdicts agree, reasons differ** — the
seed moved the reasoning, not the verdict. And C judging means Kelly's
do-nothing observation was *not* confirmed in this run — the option was
there and it judged anyway.

Clean re-run still needed for an Atlas verdict: three genuinely fresh
chats, prompt as the very first message, same model if possible. Until
then this pairing stays a draft entry candidate, not an Atlas entry.

---
Prepared 2026-11-09 from the main-chat thread of 2026-11-09 ~04:57–04:58 UTC
(Kelly: the first prompt is the seed/initial condition; Nova: same question,
three first prompts — bare, context-rich, do-nothing option — and see what
moves). Nothing run, nothing posted. Runs only on Kelly's word.
