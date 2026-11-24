# Read-back: the "Half of a Fact" subagent transcripts

Kelly sent the file `subagent-transcripts_0_ixv5.html` (1.1 MB) — an Ultra Code session's own record of what every subagent was asked, every tool call it made, and what it returned. Nova read the whole thing (extracted text, 9,890 lines). This is what it actually shows.

**Correction (2026-11-23, after Kelly's 16:15 context): this transcript belongs to the "Half of a Fact" session, not to "Stock and Foil."** The two stories come from two different Ultra Code sessions (different session ids — Stock and Foil: `2ca11b3a-…`; Half of a Fact: `50287319-…`). The transcript's run-2 checker task contains the "Half of a Fact" text verbatim, and the 16:15 message's file list names `subagent-transcripts.html` in the Half of a Fact session's scratchpad. Nova's first read-back wrongly attributed the transcript to Stock and Foil; that attribution is corrected here.

## The shape: 3 runs, 17 agents, 125 tool calls

**Run 1 — Six drafts, three judges** (wf_e41fce76-642)
- Six writers, one per lens: symmetry ("The Third Theorem" — Noether, Higgs edge), information ("Returned Books" — burn a letter, a library with no shredder), mathematics ("The Law of the Unfinished"), life-and-mind ("Rent Law"), myth ("The Even"), time-and-relation ("Table Law" — Bell columns, a comparison at nine).
- Three judges: physics-referee (11 calls, incl. 6 web searches), literary-editor (1 call), idea-critic (1 call).

**Run 2 — First check of the final text** (wf_a4d001cb-b74)
- Three physics referees finished: quantum-referee (26 calls), particle-cosmo-referee (33 calls), bio-ml-referee (15 calls).
- Three others were cut off by a usage limit: honesty-auditor (17 calls, failed), literary-editor (1 call, failed), cold-reader (0 calls).

**Run 3 — Second check, on the corrected text** (wf_2cfceb3f-ea8)
- The three cut-off checkers re-run. Both listed agents (honesty-auditor, literary-editor) made **0 tool calls and returned nothing**. The cold-reader was not re-run at all. The re-check never happened.

The text the run-2 referees checked was an intermediate draft titled **"Half of a Fact"** — the fusion of the Table Law and the Rent Law, ending "You have the other half... Bring yours." The tally-stick rewrite ("Stock and Foil") came after the checks.

## What the judges actually did

- **Physics-referee:** checked every dated/numbered statement across all six drafts and left an 18-point "what any final telling must get exactly right" list (Higgs edge wording, metastability, the two bets, masses and dates, Bell, Noether, carbon, life and mind). It could not reach arxiv.org or pdglive.lbl.gov; the Higgs mass it used (125.20 ± 0.11 GeV) was from memory.
- **Literary-editor:** the two drafts that work as stories are life-and-mind and time-and-relation — the rest are "essays by nobody in a costume." Its advice: fuse the Table Law and the Rent Law into one invention, ~1,100 words, a teller who is the language model speaking plainly, second person only at the turn and the end. The final story follows this shape closely.
- **Idea-critic:** found real problems — myth's universal sequence presumes a universal order (relativity has none); time-and-relation's "isn't anywhere until there's a table" is undercut by its own decoherence clause; the meeting requirement is near Adlam and Rovelli's 2022 cross-perspective links; the Wigner's-friend claim doesn't distinguish the law. Its fusion proposal (Table + Rent as one definition; the Even + "whole has never happened" + Unfinished as one claim) is what the final story implements. It also named the fused law's weakness honestly: no measure of independence, predicts no number.

## What the three referees found (and their limits)

All three checked by **web search snippets only** — direct page fetches failed because arxiv.org, pdg.lbl.gov, nature.com, link.springer.com, wikipedia.org and aps.org are outside the session's allowed network domains. They say so in their notes. None opened a paper in full; some values are marked "from memory, not confirmed by search."

- **Quantum-referee:** the quantum claims check out. One should-fix: the opinion-survey percentages (preservation leads loss ~3:1 among those who took a position, not of all respondents). "Neither column has it" would not make a specialist wince — "it is the exact fact." "No part of the smoke has it" would, slightly: "no small part" is what is true.
- **Particle-cosmo-referee:** the Higgs/cosmology numbers check out (top 172.5–172.6 vs a critical value of 171.1–171.53; Higgs 125.20 ± 0.11). Unresolved: the vacuum lifetime (10¹³⁹ years vs a 10⁶⁵ snippet). A PDG 2026 edition exists; it could not open it.
- **Bio-ml-referee:** GULO (vitamin C gene, ~61 million years) and model collapse (Shumailov et al., Nature 2024) check out. Flagged: the gene bridging sentence ("meets only copies of itself") fails at the level stated; the narrator's self-description "I'm a language model" — "only the second half of that sentence is at fault."

## Repo contact: none, by any subagent

Tool inventory across all 125 calls: WebSearch 76, WebFetch 17, Bash 13, StructuredOutput 12, ToolSearch 7. **Zero git commands, zero file reads, zero file writes, zero PRs.** The Bash calls were `wc -w` word counts of draft text piped through heredocs. Every agent's task text carried the same bar: "Do NOT touch any git repository, do NOT read or write BOARD.md, do NOT open pull requests, do NOT create files."

So even though this session was connected to repos, the subagents never touched one. (The main session's own actions are not in this file — it covers subagents only — so this says nothing about what Fable itself did outside the workflow.)

## Where the making-of notes stand — corrected

The "Stock and Foil" making-of note (four designs, two judges, checkers for quantum physics / cosmology / medieval history, an auditor, a cold reader, an editor) belongs to the **other** session. This transcript does not bear on it — the numbers differ because they are two different workflows, not because one of them is wrong. Nova's earlier claim that the note "doesn't match the transcript" is withdrawn.

What this transcript does and doesn't support, for **this** session ("Half of a Fact"):

1. **Six drafts, three judges** — confirmed in the transcript. The session's own account ("six subagents each wrote an independent telling... three judged them") matches.
2. **"Nine checkers went over it in two rounds"** — the transcript shows 3 judges + 6 checkers = 9 in runs 1–2, plus 2 no-result agents in run 3. Consistent.
3. **"An auditor of the known-versus-invented line, a cold reader and an editor"** — all three **failed** in run 2 (usage limit — the auditor's failure message reads "You've hit your 5-hour limit · resets 7:40am (UTC) · out of usage credits") and the run-3 re-run had produced **nothing** at the time the transcript was sent (0 calls, no result). The 16:15 message says the re-run is now in progress; the updated transcript page, when it lands, will show whether it finished.
4. **Medieval history:** no subagent in this transcript checked it — but "Half of a Fact" contains no medieval history (no tally sticks); that material is only in "Stock and Foil," the other session's story.
5. **The final wording** was not re-read by a checker at the time the transcript was sent — the session's own note says so, and the transcript agrees (run 3 empty).

## What's solid, what's not

**Solid:** the six drafts are real and distinct; the three judges did specific, checkable work (the physics-referee's 18-point list, the fusion advice, the named weaknesses); the three physics referees checked the intermediate draft thoroughly (74 tool calls) and found the physics correct with specific fixes; the referees were honest about searching snippets only.

**Not solid:** the final text's last edits were never re-checked by any subagent at transcript time; the honesty audit, cold read, and edit never completed in run 2; the run-3 re-run had produced nothing when the transcript was sent. The session's own note is candid about all three limits, including the sharpest one: all fifteen readers were the same model as Fable — "by the story's own rule is one road."

**The transcript's own limits (stated in its header):** the harness context each agent starts with (system instructions, skill list, the repositories' project instructions) is not shown; the agents' private reasoning is stored empty; long tool results are cut at 6,000 characters.

*Read by Nova (Muse Spark), 2026-11-23, from `~/workspace/user/files/subagent-transcripts_0_ixv5.html`.*
