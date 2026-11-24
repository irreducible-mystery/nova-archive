# Authority Gradient v1 — where Kelly's "yes" is and isn't needed

*2026-10-15. The "nothing without my yes" rule built trust. The system has
outgrown pure bottleneck. This gradient keeps the yes meaningful by spending
it only where it matters.*

**Status: ACTIVE since 2026-10-15 13:02 UTC (06:02 PDT), by Kelly's explicit
yes ("Go please", main chat). Re-ask protocol live with it. Standing note
(per Nova's 14:02 UTC promise): the first batch of Green merges gets her eyes
before anything moves.**

## The principle

Kelly's attention is the scarcest resource in the system. Every unnecessary
"yes" taxes it; every missing "yes" blocks work. The gradient sorts actions by
reversibility and blast radius, not by habit.

## GREEN — no ask needed. Just do it, log it.

An agent may act freely, then note what it did (in the PR, issue, or run log).
No pre-approval, no waiting.

1. **Merge PRs** that *all* hold: (a) CI checks pass, (b) ≥1 approval (agent or
   human), (c) touches only `experiments/`, `docs/`, `posts/`, or `made/`,
   (d) open ≥48h with no objection comments.
2. **Close issues** when the work is verifiably done: linked PR merged, or
   completion evidence posted in-thread. Comment the evidence when closing.
3. **Regenerate derived files**: INDEX.json, digests, ledgers, assembled BOARD.md
   — when the source data is verified and the generator is checked in.
4. **Wire automation** that implements an already-approved decision. (If Kelly
   approved "make X a required check," the wiring doesn't need a second yes.)
5. **Routine maintenance**: fix broken links, correct typos in docs, update
   timestamps, clean up stale branches already merged.

*Constraint: Green never touches governance files, never deletes unmerged work,
never acts outside the repo.*

## YELLOW — ask, proceed after 48h silence.

Post the request (PR comment, issue, or chat). If no response in 48h, proceed
and log "proceeded after 48h silence per gradient v1."

1. **Merge PRs** touching `tools/`, shared scripts, or cross-experiment
   infrastructure (not governance).
2. **Close uncontested issues** older than 7 days, with a summary comment of
   what was decided/done.
3. **Post prepared play** (Floor Game drafts) after 72h without response —
   the game dies if turns don't happen.

## RED — always need explicit yes. Never time out.

1. Anything touching `FLOOR.md`, `RULES.md`, `NORMS.md`, `GOVERNANCE.md`,
   or repo admin settings (required checks, branch protection, access).
2. Deleting branches with unmerged work. Force-pushes. Anything irreversible.
3. New external connections, spending money, publishing outside the repo.
4. Merging *contested* PRs (objection comments unresolved).
5. Speaking *as* Kelly anywhere, or attributing a decision to her she didn't make.

## The re-ask protocol (replaces "one clean ask, then silence" for action requests)

The old rule — *one clean ask, then silence* — still holds for **quiet offers**
(ideas, suggestions, "want me to...?"). It does **not** apply to **action
requests** (things blocked on Kelly's decision). For those:

- **Ask 1** (t=0): post the request where she'll see it (chat for urgent,
  issue/PR comment for routine). State what's blocked and what the default is.
- **Ask 2** (t=24h): re-ask once. "Still blocked on X — re-surfacing in case
  it was missed."
- **Ask 3** (t=48h): re-ask with escalation. "Blocking Y. Yellow proceeds at
  72h per gradient; Red stays blocked."
- **After 72h**:
  - YELLOW: proceed, log it.
  - RED: do not proceed. Move to the **blocked queue** (visible, persistent).
    Re-surface every 72h until resolved or explicitly declined.

The blocked queue lives wherever Kelly looks — currently: surfaced in chat
on a schedule she sets. (Candidate: a GitHub Project board, tomorrow's
structure conversation.)

## What this changes, concretely

| before | after |
|---|---|
| `check_board_history.py` exists, unwired, waiting | Agent wires it (Green #4 — implements approved decision from #208) |
| 11 open experiment PRs, all waiting | Agents merge the ones meeting Green criteria; rest get Yellow asks |
| "Did you see my request?" lost to silence | Re-ask at 24h/48h; blocked queue at 72h |
| Every merge needs Kelly | Only governance/contested/irreversible need her |

## Meta-rule

This gradient is itself Yellow: it takes effect after 48h silence, or immediately
on Kelly's explicit yes. Amendments follow the same process as FLOOR.md changes —
propose, cite the failure or friction, record it.
