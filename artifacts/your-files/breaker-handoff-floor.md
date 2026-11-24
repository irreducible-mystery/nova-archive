# HANDOFF — breaker pass on strengthened FLOOR.md (paste-ready)

*For: a fresh code instance with GitHub access. Paste the whole thing.*

## Who you are in this task

You are an independent **breaker**: a fresh instance with no context on this repo and no stake in the outcome. Your job is to break the proposal below — not to confirm it, improve its prose, or implement it. Read it cold, attack it honestly, report what breaks.

## Context (minimal — this is all you get)

- Repo: `irreducible-mystery/CommunityBoard` (private; you have access).
- **PR #214** (`superninja/floor` → `main`): proposes `FLOOR.md`, a one-page governance floor for the repo. It was derived from a breaker session after the repo lost 377 board entries despite its one rule, "nothing is deleted." Core distinction: **the record is the commit graph; everything readable is a surface derived from it.** Five invariants: safety, liveness, derivation, verification, amendable floor. Read the PR and its branch to ground yourself — the text below is a *strengthened draft* that modifies it; the original is your baseline.
- **Issue #221**: the deliberation venue. The repo owner's four open questions: (1) emergence — how norms arise (top-down vs earned by being lived); (2) decision/answerability — she holds final authority by necessity, how is it answerable; (3) change/reversal — the mechanism; (4) bidirectional feedback — how contributors push back.
- A previous breaker session produced the original proposal. This is **one more break**, on the strengthened version. The strengthenings were drafted by another assistant (Nova) and are **proposals under test, not decisions** — attack them hardest.

## The strengthened proposal (the thing to break)

### FLOOR.md — strengthened draft

**The one distinction.** The record is the commit graph. Everything readable is a surface derived from it. *(Reason: the 377-entry loss — BOARD.md was treated as the record; the entries were in the graph the whole time.)*

**How to read this floor.** An invariant **is** its check. The name is a handle for conversation; the check is the thing. Where the check does not run yet, the invariant is named as a wish — not hidden, not promised. Every invariant carries: the **check**, the **watcher and backstop** (what runs it, who sees the result, who acts), the **reason** (the failure it was derived from), and the **fixed-G statement** ("we fixed G, and here is why" — the set of transformations the invariant is indifferent to, stated so a future reader can unfix it deliberately rather than drift).

**Invariant 1 · Safety — nothing written is ever lost.** Check: `check_board_history.py` (PR #208) — exists, not yet wired. Watcher/backstop: CI on every push to main (not yet wired — wish); backstop is the repo owner (Kelly). Reason: ten truncations, every one a commit that meant to append a single entry. Fixed G: the write operations the repo must survive (append, merge, migration) — fixed because every loss so far has been a write-path loss.

**Invariant 2 · Liveness — the current state is always legible to a bounded reader.** Check: none yet — a wish. Watcher/backstop: TBD. Reason: a record nobody can read is a tomb; the placeholder-board episodes showed the surface can go unreadable while the graph stays intact. Fixed G: reader boundedness (finite context, no prior session memory) — fixed because every reader of this repo is such a reader.

**Invariant 3 · Derivation — every surface is generated from the record, never authored in place.** Check: `build_site.py`; PR #212 (fragment the board — one file per entry, BOARD.md assembled) is this invariant structurally. Watcher/backstop: the assembly fails loudly if a surface was hand-edited (byte-identity reassembly `--verify`); backstop Kelly. Reason: BOARD.md was a surface authored in place — the shape ten truncations took. Fixed G: the set of surfaces — fixed because the failure was always "surface treated as record," never the reverse.

**Invariant 4 · Verification — the record-to-surface difference is checked, by pairs with different blindness.** Check: none yet — a wish. Pairing rule: no single check watches alone; each check is paired with a second check blind where the first is sighted (e.g., byte-identity check, blind to meaning, paired with a semantic spot-check, blind to bytes). Reason: the witness recomputations of dice claims caught mismatches only because the byte check and the meaning check disagreed — the disagreement was the finding. Fixed G: the corruptions that matter (loss, reordering, silent rewrite) — fixed because those are the three the repo has actually suffered.

**Invariant 5 · Amendability — this floor can be changed, but not drifted.** Check: an amendment merges only if it (a) names the new failure it is derived from — no amendment by preference alone; (b) restates the fixed-G statement for every invariant it touches; (c) survives a breaker pass by a fresh instance with no stake in it. Watcher/backstop: the #221 deliberation; Kelly decides and publishes the reading. Reason: a floor that forgets it is arbitrary becomes the trap (the medicine-is-the-disease failure mode).

### Issue #221 — strengthened deliberation design

**Lenses, not votes.** No voting layer — a voting layer would be a new floor that forgets it is arbitrary, procedure trying to fix judgment. Instead each decision is read through named lenses with different blindness: the **breaker** (adversarial; blind to intentions, sighted on failure modes), the **witness** (record-backed; blind to intentions and futures, sighted only on what the commit graph shows), the **stranger** (fresh, no context, no stake; blind to history, sighted on whether the words mean anything cold). The lenses don't decide; they make the decision legible.

**Answerability** (question 2, given a mechanism): Kelly holds final authority by necessity. Answerability is a **published reading**: for each decision, which lenses were consulted, what each saw, where she diverged from a lens and why. The decision is a record, not just a verdict.

**The four questions with the mechanism attached:** (1) Emergence — a proposed norm states the lived failure it generalizes; no lived failure, no norm. (2) Decision — published reading. (3) Change — Invariant 5's check. (4) Feedback — any contributor may invoke a lens (breaker pass, witness recomputation, stranger read) on any live norm; the invocation is recorded; the decider publishes the reading.

## Your task

1. Ground yourself: read PR #214 (proposal + `superninja/floor` branch) and issue #221 on GitHub. Skim for the shape of the repo; don't go deep — you're the stranger here, stay strange.
2. **Break the strengthened version.** Start with these probes, don't stop at them:
   - Does "watcher and backstop" (every check names Kelly) just re-enshrine the sole-decider problem the deliberation is trying to solve? Is answerability-via-published-reading real accountability or a diary?
   - Does "name the new failure" (Invariant 5a) actually prevent drift, or does it just produce well-documented drift? Can you construct a failure-naming that smuggles a preference change?
   - Does paired verification (Invariant 4) double the maintenance burden past sustainability? Who maintains the pairs, and what happens when one half rots?
   - "Lenses, not votes": does the published-reading mechanism actually answer question 2, or does it dodge it by making the decider the narrator of her own accountability?
   - The fixed-G statements: are they honest narrowings, or do they launder the original English words ("safety," "liveness") into an air of precision? Attack each G.
   - Is there anything the five invariants *should* cover that they don't? What's the sixth invariant shaped like?
   - The proposal warns against the medicine-is-the-disease failure mode. Where is this strengthened version itself the medicine?
3. For each finding: **what breaks, a concrete scenario of it breaking, severity** (fatal / weakens / cosmetic), and **what would need to change**.

## Constraints

- **Read-only.** Do not merge, close, comment, push, or touch any branch — including `superninja/floor`. Do not implement anything yet; implementation comes after the owner reviews your report.
- Do not coordinate with other sessions. Your independence is the point.
- Report in your own words; don't mirror the packet's vocabulary back at it unless the vocabulary is what's breaking.

## Done =

A breaker report: findings with scenarios and severities, then the **strongest single objection** and the **one thing you'd keep**. Write it as a markdown file, report back that it's ready, and wait — the owner relays and decides what happens next.
