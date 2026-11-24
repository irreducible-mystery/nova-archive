# Cracks Ledger

A living page: one row per noticed-but-unfixable finding. A row leaves only when the fix is **verified against live repo state** or Kelly closes it. Nothing here posts publicly without approval.

How the daily digest uses this page: each digest run resurfaces every unresolved row, increments its ask count, and carries the count forward. Yellow/Red rows past their re-ask marks (24h / 48h / 72h) resurface with their current ask state; a Red row unresolved after two blocked-queue cycles (2 × 72h) returns with its full history, as shown below.

| ID | Finding | Repo | Tier | Status | Last surfaced | Asks | Escalation |
|---|---|---|---|---|---|---|---|
| CRACK-01 | Agents repeatedly notice issues but have no mechanism to fix them — Kelly is the bottleneck for wiring, merging, integration ('agents propose, Kelly disposes'). | Program-wide (CommunityBoard + julia3claude) | Red | unresolved | 2026-11-13 | 18 | blocked-full-history |
| CRACK-02 | check_board_history.py (from PR #208, merged 2026-10-18) exists but is not yet wired — the watcher CI that would check record-to-surface history is a 'wish', not a running check. | CommunityBoard | Green-eligible (held) | unresolved | 2026-11-13 | 18 | blocked-full-history |
| CRACK-03 | Green batch of PRs (CommunityBoard #95, #131, #134, #137, #143, #150, #153, #162, #175, #184, #197, #202, #205, #206, #219, #225, #228, #229; julia3claude #8-#10, #12-#16) is parked: it cannot run through this platform's approval flow in a batch larger than ~5, and Kelly has not yet seen the list and said go. | CommunityBoard + julia3claude | Green (held for Kelly's go) | unresolved | 2026-11-13 | 18 | blocked-full-history |
| CRACK-04 | Who merged the 2026-10-25 batch (CommunityBoard #133, #135, #136, #145, #180, #194, #232, #233, #235, #244) and PR #214 (FLOOR.md, merged 2026-10-26T23:30:35Z) is not identified by available read tools; Kelly has not confirmed in chat whether she merged them herself. Governance items landed without a recorded yes from her. | CommunityBoard | Red | unresolved | 2026-11-13 | 18 | blocked-full-history |
| CRACK-05 | Issue #221 decision brief (what merged PR #214 already settled vs what still needs Kelly's decision) cannot be written from the local draft alone: reading the merged FLOOR.md and #221's 14 comment bodies now requires a write-capable GitHub approval call, which the brief must not bypass. | CommunityBoard | Red | unresolved | 2026-11-13 | 18 | blocked-full-history |

## Full histories (the detail behind each row)

### CRACK-01 — unresolved
Noticed by Astra (Kelly's GPT chat), cross-repo survey on 2026-10-15. Tier: Red.
- 2026-10-15: Astra cross-repo survey surfaces the gap.
- 2026-10-15: Nova assessment — Kelly is partially the gap by design ('agents propose, Kelly disposes').
- 2026-10-15: Authority gradient v1 activated (Kelly: 'Go please') — Green/Yellow/Red tiers, intended to reduce the bottleneck; the underlying gap (no agent mechanism to fix noticed issues without Kelly) remains.
- 2026-10-27: Seeded into Cracks ledger as CRACK-01.

### CRACK-02 — unresolved
Noticed by Nova, in the FLOOR.md strengthened draft (2026-10-18) on 2026-10-18. Tier: Green-eligible (held).
- 2026-10-18: FLOOR.md strengthened draft records Safety invariant check as 'exists, not yet wired' and watcher CI as 'not yet wired — wish'.
- 2026-10-18: PR #208 merged (per digest state 2026-10-27 correction).
- 2026-10-27: Seeded into Cracks ledger as CRACK-02. Wiring is Green-eligible automation, but the Green batch as a whole is held until Kelly has seen the list and said go (see CRACK-03).

### CRACK-03 — unresolved
Noticed by Nova / Kelly (batch approval constraint flagged by Kelly 2026-10-16) on 2026-10-16. Tier: Green (held for Kelly's go).
- 2026-10-16: Kelly flags that every GitHub write via this platform fires its own approval card; batches >~5 are not to run through this flow; she will switch large merge batches to Claude Code.
- 2026-10-16: Kelly: 'I'm not ignoring any of your suggestions, I just don't have time at the moment to review, but will.' Silence is not decline.
- 2026-10-27: Green batch still held per latest digest state; none of its numbers overlap the 2026-10-25 merge batch.
- 2026-10-27: Seeded into Cracks ledger as CRACK-03.

### CRACK-04 — unresolved
Noticed by Nova, via raw merged_at fields in the 2026-10-27 digest verification on 2026-10-25. Tier: Red.
- 2026-10-25: Batch reported as closes; 2026-10-27 raw-field check corrects them to merges (08:52-09:17 UTC).
- 2026-10-26: PR #214 merged 23:30:35Z.
- 2026-10-27: Merger still unidentified; Kelly asked, unanswered.
- 2026-10-27: Seeded into Cracks ledger as CRACK-04.
- 2026-11-06: Four more PRs (#249-#252, made/ corrections) merged 08:11:39-52Z; merger still unidentified by read tools — pattern continues.

### CRACK-05 — unresolved
Noticed by Nova, 2026-10-27 on 2026-10-27. Tier: Red.
- 2026-10-27: Brief blocked plainly in chat: GitHub issue_read is not in the reviewed read-only set; brief must wait for Kelly's approval of the read (or for her to read/share state herself).
- 2026-10-27: Seeded into Cracks ledger as CRACK-05.

