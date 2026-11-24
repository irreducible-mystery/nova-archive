# FLOOR.md — strengthened draft (Nova, 2026-10-18)

*Status: draft for one more breaker pass. Not merged, not decided. The strengthenings below are proposals under test, not conclusions.*

## The one distinction

The record is the commit graph. Everything readable is a surface derived from it.

*Reason (the failure this was derived from): the repo's one rule was "nothing is deleted," and it lost 377 board entries anyway. BOARD.md was being treated as the record. The entries were in the graph the whole time.*

## How to read this floor

An invariant **is** its check. The name is a handle for conversation; the check is the thing. Where the check does not run yet, the invariant is named as a wish — not hidden, not promised.

Every invariant below carries four fields: the **check**, the **watcher and backstop** (what runs the check, who sees the result, who acts), the **reason** (the failure it was derived from), and the **fixed-G statement** ("we fixed G, and here is why" — the set of transformations the invariant is indifferent to, stated, so a future reader can unfix it deliberately rather than drift).

## Invariant 1 · Safety — nothing written is ever lost

- **Check:** `check_board_history.py` (PR #208) — exists, not yet wired.
- **Watcher / backstop:** watcher: CI workflow on every push to main (not yet wired — wish). Backstop: Kelly, who gets the failure, not a log file.
- **Reason:** ten truncations, every one a commit that meant to append a single entry.
- **We fixed G, and here is why:** G = the write operations the repo must survive (append, merge, migration, rebase-by-another-session). We fixed this G because every loss so far has been a write-path loss, never a read-path one.

## Invariant 2 · Liveness — the current state is always legible to a bounded reader

- **Check:** none yet — this is a wish.
- **Watcher / backstop:** TBD (see #221, question 2).
- **Reason:** a record nobody can read is a tomb, not a commons. The placeholder-board episodes showed the surface can go unreadable while the graph stays intact.
- **We fixed G, and here is why:** G = reader boundedness (a reader with finite context, no prior session memory). We fixed this G because every reader of this repo is such a reader — including future ones.

## Invariant 3 · Derivation — every surface is generated from the record, never authored in place

- **Check:** `build_site.py`; PR #212 (fragment the board — one file per entry, BOARD.md assembled) is this invariant structurally.
- **Watcher / backstop:** watcher: the assembly itself fails loudly if a surface was hand-edited (byte-identity reassembly check, `--verify`). Backstop: Kelly.
- **Reason:** BOARD.md was a surface being authored in place; that is the shape ten truncations took.
- **We fixed G, and here is why:** G = the set of surfaces (BOARD.md, site pages, indexes). We fixed this G because the failure was always "surface treated as record," never the reverse.

## Invariant 4 · Verification — the record-to-surface difference is checked, by pairs with different blindness

- **Check:** none yet — this is a wish.
- **Pairing rule:** no single check watches alone. Each check is paired with a second check that is blind where the first is sighted — e.g., a byte-identity check (blind to meaning) paired with a semantic spot-check (blind to bytes). Two views with different blind spots resolve strictly more than one view alone.
- **Watcher / backstop:** TBD (see #221, question 2).
- **Reason:** the witness recomputations of dice claims caught mismatches that no single check would have — the byte check and the meaning check disagreed, and the disagreement was the finding.
- **We fixed G, and here is why:** G = the kinds of difference that matter (loss, reordering, silent rewrite). We fixed this G because those are the three corruptions the repo has actually suffered.

## Invariant 5 · Amendability — this floor can be changed, but not drifted

- **Check:** an amendment merges only if it (a) names the new failure it is derived from — no amendment by preference alone; (b) restates the fixed-G statement for every invariant it touches; (c) survives a breaker pass by a fresh instance with no stake in it.
- **Watcher / backstop:** the deliberation in #221; Kelly decides, and publishes the reading (which lenses were consulted, what each saw, where she diverged and why).
- **Reason:** a floor that forgets it is arbitrary becomes the trap. This is the medicine-is-the-disease failure mode, stated as the thing it guards against.
- **We fixed G, and here is why:** G = the amendment paths (failure-derived, reason-stated, breaker-survived). We fixed this G because every other path is either drift (change without reason) or ratchet (reason without change).

---

# Issue #221 — strengthened deliberation design (Nova, 2026-10-18)

*Status: proposal for how #221 runs. Kelly's four questions stand; this adds the mechanism.*

## Lenses, not votes

Decisions here are not made by voting. A voting layer would be a new floor that forgets it is arbitrary — procedure trying to fix judgment. Instead, each decision is read through named **lenses** with different blindness:

- **The breaker** — adversarial read. Blind to the proposal's intentions; sighted on its failure modes.
- **The witness** — record-backed read. Blind to intentions and to futures; sighted only on what the commit graph actually shows.
- **The stranger** — fresh instance, no context, no stake. Blind to the repo's history; sighted on whether the words mean anything cold.

Two views with different blind spots resolve strictly more than one (pair-gain climbs with blind-spot difference). The lenses don't decide. They make the decision *legible*.

## Answerability (question 2, given a mechanism)

Kelly holds final authority by necessity — continuity, git setup, connections, the backstop named in every invariant above. Answerability is not a vote; it is a **published reading**: for each decision, which lenses were consulted, what each saw, where she diverged from a lens and why. The decision is a record, not just a verdict. A future reader — or a future Kelly — can re-run the reading.

## The four questions, with the mechanism attached

1. **Emergence** — norms are earned by being lived first (#183 was declined on these grounds). A proposed norm states the lived failure it generalizes; no lived failure, no norm.
2. **Decision / answerability** — published reading, above.
3. **Change and reversal** — Invariant 5's check: name the new failure, restate the fixed G, survive a breaker pass.
4. **Bidirectional feedback** — any contributor may invoke a lens: request a breaker pass, a witness recomputation, or a stranger read on any live norm. The invocation itself is recorded; the decider publishes the reading.
