# Headline fixes — DRAFT FOR APPROVAL ONLY

**Nothing here is posted, opened as a PR, merged, or
edited on any repo.** This is a local draft in your
library, for your approval, file by file. If you approve
a fix, the next step is a PR draft — still not a merge.

## Basis — and its limit, stated first

These fixes are drafted against the **Oct 13 local
snapshot** of CommunityBoard (`communityboard-read/`,
README.md / RULES.md / CLAUDE.md as of 2026-10-13),
plus the Oct 18 #238 change to RULES.md on main
("nothing here is lost") and your Oct 24 layer
principle.

## Verification outcome, 2026-10-27 (live main read)

You approved all three on 2026-10-27, and the live
check that followed collapsed the scope:

- **Fix 1 (README.md): DROPPED — already landed.**
  Live README.md on main already reads: "**Rules:
  nothing here is lost.** Git history is the record
  and is never rewritten. Closed and pruned things
  stay recoverable, and every close says why. Board
  entries are never edited or removed."
- **Fix 2 (RULES.md): DROPPED — already landed.**
  Live RULES.md on main already carries the short
  version "**nothing here is lost**" and the
  "Nothing is lost" section (history never
  rewritten; surface tended only if recoverable and
  the removal says why; branches only when commits
  are reachable elsewhere; no one else's work edited
  away; board never tended).
- **Fix 3 (CLAUDE.md): REDUCED to the heading.**
  Live CLAUDE.md's body is already correct (history
  never rewritten, surface tended if recoverable and
  the close says why, board never tended, steward,
  RULES.md reference). The only remaining headline
  issue is the heading itself: "The rule that
  **overrides** the others: nothing is lost."
  Remaining change, prepared locally in
  `~/workspace/pr-headline-fix/CLAUDE.md` and NOT
  yet pushed: heading "overrides" → "frames", plus
  one precedence sentence after the RULES.md
  reference: "If this headline and that split ever
  seem to conflict, the split in RULES.md wins."
  Everything else in the file is untouched.

Do not apply the original three-file draft blindly
to live files — two of its three fixes are already
on main, and applying them again would only create
noise.

The rule being aligned to (already on main via #238,
per the Oct 24 audit): *nothing here is lost. This
repository is a record as much as a place to work.
The record is git history, and git history is never
rewritten. The surface may be tended, as long as
nothing tended away becomes unrecoverable and every
removal says why.*

## Fix 1 — README.md (opening Rules line)

**Old (Oct 13 snapshot):**
> **Rules: nothing here is ever deleted.** No file,
> branch, post, board entry, or pull request is
> removed, and no history is rewritten. When something
> is superseded, it stays and the new thing is added
> beside it. The full list is in [`RULES.md`](RULES.md).

**Proposed:**
> **Rules: nothing here is lost.** Git history is
> never rewritten. The live surface may be tended,
> as long as nothing tended away becomes unrecoverable
> and every removal says why. Board entries are never
> tended — they are record, not surface. When something
> is superseded, the old thing stays reachable in
> history and the new thing is added beside it. The
> full list is in [`RULES.md`](RULES.md).

**Why:** removes the global "ever deleted" claim
(the tree *does* change; a merge dropping a file
from the tree is a surface deletion) and replaces it
with the claim git can actually deliver: history
kept, removals recoverable and explained.

## Fix 2 — RULES.md (short version + "Nothing is deleted" section)

**Old (Oct 13 snapshot):**
> The short version: **nothing here is deleted.**
> This repository is a record as much as a place to
> work, and the record is the point. Everything below
> follows from that one rule.
>
> ## Nothing is deleted
> - No file, branch, post, board entry, or pull
>   request is ever deleted.
> - No history is rewritten. Nothing is force-pushed
>   over, and no one else's work is edited away.
> - When something is superseded, the old thing stays
>   and the new thing is added beside it.
> - Duplicates stay as duplicates. […]
> - Merged branches are left in place. Do not delete
>   a branch after its pull request merges.

**Proposed:**
> The short version: **nothing here is lost.** This
> repository is a record as much as a place to work,
> and the record is git history.
>
> ## Nothing is lost
> - Git history is never rewritten. No force-push
>   over shared branches; no dropping commits other
>   work depends on.
> - The live surface may be tended, as long as
>   nothing tended away becomes unrecoverable and
>   every removal says why and where it went.
> - Board entries are never tended.
> - No one else's work is edited away inside a file:
>   supersede beside it, or retire a whole file
>   with a stated reason.
> - A branch may be deleted only when its commits
>   are reachable elsewhere.
> - When something is superseded, the old thing stays
>   reachable in history and the new thing is added
>   beside it.

**Why:** the old bullets promise tree-level
permanence (no file ever deleted, merged branches
left in place) that the history/surface subsection
below them already contradicts. The new bullets say
only what the subsection can deliver. **Verify
first:** if live RULES.md already carries the
"nothing here is lost" subsection from #238, this
fix is only the heading and the first bullets —
do not reintroduce a second, competing version of
the rule.

## Fix 3 — CLAUDE.md ("the rule that overrides the others")

**Old (Oct 13 snapshot):**
> ## The rule that overrides the others: nothing is deleted
>
> No file, branch, post, board entry, or pull request
> is ever deleted, and no history is rewritten. When
> something is superseded, the old thing stays and the
> new thing is added beside it; duplicates stay as
> duplicates. Do not delete a branch after its pull
> request merges. Every other rule below serves this
> one. The full list is in [`RULES.md`](RULES.md).

**Proposed:**
> ## The rule that frames the others: nothing is lost
>
> Git history is never rewritten. The live surface
> may be tended only as RULES.md allows: nothing
> tended away becomes unrecoverable, and every
> removal says why. Board entries are never tended.
> When something is superseded, the old thing stays
> reachable in history and the new thing is added
> beside it. Every other rule below serves this one
> — but this headline does not override RULES.md's
> history/surface split; if they seem to conflict,
> that split wins. The full list is in
> [`RULES.md`](RULES.md).

**Why:** "overrides the others" is the most
dangerous of the three headlines — it tells a
session to follow the global version over the
subsection that corrects it. "Frames" keeps the
rule prominent without giving the headline
precedence over its own correction.

## What this draft does NOT do

- No history rewrite, no force-push, no board-entry
  edits, no changes to FLOOR.md (merged Oct 26 as
  PR #214) or to any open PR (#234, #245).
- No change to the *rule* — only to headlines that
  state it more broadly than the rule itself.
- No fix is applied to a file whose live text
  already matches the proposal.

## Verification checklist (before any use)

1. Read live main README.md, RULES.md, CLAUDE.md
   top sections (needs a GitHub read approval on
   a card, or your paste of the current top lines).
2. Drop every fix already landed on main.
3. Confirm the board layout on main today
   (single BOARD.md vs fragmented board/entries/)
   and adjust Fix 2's board bullet to match.
4. Check the merged FLOOR.md text for any conflict
   with these headlines.
5. Your approval, per file — approve all three,
   or pick ones. Unapproved fixes stay in this
   draft and go nowhere.
