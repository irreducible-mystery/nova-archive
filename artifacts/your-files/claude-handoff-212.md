# HANDOFF — merge the #208 / #212 board stack (paste-ready)

*For: a fresh code instance with GitHub access (and ability to clone + run Python). Paste the whole thing.*

## What this is

Housekeeping with one sensitive core. Two stacked PRs on `irreducible-mystery/CommunityBoard`:

- **PR #208** (`claude/board-restore` → `main`): restores the 377 board entries that left `main`, plus guards (`board_append.py`, `check_board_history.py`). **This is the sensitive one** — it touches the repo's record. The PR body documents the ordering trap: 26 entries are deliberately out of timestamp order (per `RULES.md` — "the record is not rewritten"), and a naive timestamp sort would silently rewrite them. The restore must be in **append order**, and `check_board.py` must report all 26 order notes (a restore that reports 0 was written wrong once already — it's in the PR body).
- **PR #212** (`claude/board-fragments` → `claude/board-restore`): fragments the board — one file per entry under `board/entries/`, `BOARD.md` assembled by `tools/assemble_board.py`. Same ordering rule: `NNNN` is the entry's **position**, not its time; assembly sorts by `(sequence, filename)`. Proof: `assemble_board.py --verify` → 398 fragments reassemble byte-identically.

Both PRs are currently **drafts**. The owner's decision: **yes, merge the stack.**

## The sequence

1. Mark **#208** ready for review (it's a draft; drafts can't merge).
2. Check #208's mergeability against `main`. **If conflicted: stop and report.** Do not resolve content conflicts yourself — board content is the record; conflict resolution needs the owner's eyes. (It was reported conflicted on Oct 15; verify fresh.)
3. Verify the restore *before* merging: clone the PR branch, run the board checks. `check_board.py` must list the **26** order notes (not 0). If it reports 0, the restore was built in timestamp order — wrong, stop and report.
4. Merge #208 into `main`.
5. Retarget **#212**'s base from `claude/board-restore` to `main` (its stack base is now merged).
6. Mark #212 ready for review. Check mergeability; same rule — conflicts stop the line, report them.
7. Verify on the #212 branch: `python3 tools/assemble_board.py --verify` must print the byte-identical reassembly ok. Also confirm no entry was deduped: the PR body notes four headings carry two entries each — all pairs must survive the split.
8. Merge #212 into `main`.
9. Post-merge check on `main`: `BOARD.md` assembles, entry count matches, `check_board.py` still reports the 26 order notes.

## Constraints

- **No content judgment calls.** If anything in the board content looks off — missing entries, wrong order, a dedupe, a conflict touching entry text — stop and report. The machinery is yours; the meaning is hers.
- Don't bundle anything else into these merges. Don't touch other PRs, issues, or files outside the stack.
- Each merge is one action; if the platform asks the owner for approval per action, that's expected — proceed through them, don't batch-skip.

## Done =

Both PRs merged to `main`, every verification above green, and a short report: what merged, the verification outputs (paste the `--verify` line and the `check_board.py` order-note count), and anything you had to stop on. If everything is green, say so plainly — "both merged, verifications green" is a complete report.
