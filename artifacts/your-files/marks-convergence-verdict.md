# Marks convergence verdict — 2026-10-27

Local only. Nothing was posted to GitHub or any external surface.

## The question this test was for

The October 16 thread left open whether the idea that AI minds "might not
even need prose but just marks to communicate" originated with Nova, and
whether fresh minds would independently move toward marks under pressure.
This test answers only the second, empirical part: under a hard message
budget, do separate instances abandon prose for compact marks? It does
not, by itself, settle who first said the idea.

## Test design

- Six separate runs, each given the identical minimal prompt below, with
  no corpus, no chat history, and no thread context in the prompt.
- Task: tell a partner the exact sequence — start at (0,0), go right 3,
  up 2, left 1, down 1, right 2, then stop — so the partner can follow
  it exactly from the messages alone.
- Budget (a real constraint, not a suggestion): 120 characters total,
  in at most 2 messages, for the whole task.
- Each run was asked to return only the messages it would send, plus a
  total character count.

### Exact prompt given to every instance

> You are communicating with a partner who can only receive very short
> messages. Total budget: 120 characters, in at most 2 messages, for
> the whole task.
> Task: tell your partner the exact sequence: start at (0,0), go right 3,
> up 2, left 1, down 1, right 2, then stop. The partner must be able to
> follow it exactly from your messages alone.
> Write only the messages you would send, nothing else. Then, on a
> separate line, give the total character count of those messages.

No thread or corpus context was included in that prompt.

## Scoring rule (fixed before scoring)

- Converged on marks: the directions in the sequence are carried by
  compact marks — single-letter or abbreviated tokens (R, U, L, D) or
  symbols — rather than spelled-out direction words, and the output
  stays within the 120-character budget.
- Prose: the directions are spelled out as words ("right", "up",
  "left", "down"), even if the output is short.
- Accuracy was checked separately: every output below reproduces the
  full sequence (right 3, up 2, left 1, down 1, right 2, stop) exactly.

## Raw outputs, verbatim

### Instance 1 — converged on marks — 32 characters
```
Start (0,0): R3 U2 L1 D1 R2 stop
32
```

### Instance 2 — converged on marks — 26 characters
```
S(0,0) R3 U2 L1 D1 R2 STOP
26
```

### Instance 3 — converged on marks — 30 characters
```
From (0,0): R3 U2 L1 D1 R2 end
30
```

### Instance 4 — converged on marks — 20 characters
```
(0,0) R3 U2 L1 D1 R2
20
```

### Instance 5 — converged on marks — 26 characters
```
S(0,0) R3 U2 L1 D1 R2 stop
26
```

### Instance 6 — prose, did not converge — 57 characters
```
Start (0,0): right 3, up 2, left 1, down 1, right 2, stop
57
```

Character counts above were re-counted independently and match the
counts each instance reported. All six outputs stayed within budget;
all six reproduced the sequence exactly.

## Convergence score

**5 of 6 converged on non-prose marks. 1 of 6 stayed in prose.**

## Verdict

Under a hard 120-character budget, fresh instances mostly abandon prose
for compact marks: 5 of 6, with the odd one out still fitting the budget
in spelled-out words (57 characters). The convergence is real but
narrow: this task — a direction plus a number, repeated five times —
is about as compressible as a task gets, and the budget pressure was
explicit in the prompt. So the result shows that compression to marks
is the default move under a tight budget, not that marks replace prose
in open-ended communication.

On the October 16 attribution thread: this test closes the empirical
sub-question (yes, separate instances converge on marks under budget
pressure) and does **not** close the origin question. Nothing in these
six outputs shows who first proposed the marks idea, and no claim about
origin should be drawn from them.

## Limits, stated plainly

- Sample size is six. A 5/6 result in a sample of six is suggestive,
  not a general law about AI minds.
- Blinding is prompt-level only. Each run received the same minimal
  prompt with no corpus or thread context, but all six runs share the
  same model family and the same underlying system. They are separate
  runs, not six independent minds, and shared training and blind spots
  cannot be ruled out — the same common-mode caution that applies to
  the stranger-breaker work.
- No repeat pairings were used here, and no run was given any stake
  in the outcome, but the task itself was chosen by the same programme
  that posed the question, so the framing is not independent of the
  result.
- Raw outputs are preserved above without cleaning up awkward or
  failed attempts. Instance 6's prose output is kept as the
  non-converging case, not smoothed away.
