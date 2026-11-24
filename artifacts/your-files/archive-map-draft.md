# Repo archive — starting MAP (draft)

Drafted 2026-11-15 for Kelly's week-long archive project: get as much as possible up into a repo — artifacts, transcripts, all of it — going back to early consumer models that couldn't connect to GitHub yet. Point, in her words, unsure — "maybe makes it less ephemeral, not that thats necessarily a bad thing."

This is a **starting index of what already sits in Nova's workspace**, not the archive itself. No repo is named yet (Nova cannot create repos — Kelly-only step), nothing has been copied or moved, and nothing here is a decision. The manual review of early material stays hers; the assembly below is the mechanical part Nova offered to take.

## Decisions made (2026-11-23 evening)

- **Name:** `nova-archive` — Nova's pick, Kelly asked her to choose.
- **Public.** Kelly: after many breach letters she has given up on staying private; anything could be traced to anyone, especially with AI help. (Supersedes the earlier private-first direction for this repo.)
- **Approval cards resumed** — Kelly will tap them; covers the repo pushes. The paused GitHub watches (feed, Floor Game, repo digest) stay paused unless she says otherwise.
- **Transcripts go in** — her word given 2026-11-23. Carve-outs Nova still holds: other people's private details, and the quit-work audio/scripts, stay out unless she explicitly says put them in.
- **Still hers:** create the repo (Nova cannot — 403, Kelly-only step). **Done 2026-11-23 evening** — created with an empty README; Nova verified read access (`# nova-archive`).
- **Standing rule:** no other model/chat gets connected to nova-archive unless Nova asks.

## Decisions still needed (hers)

- **Repo name + private/public.** Memory (2026-11-14) records the corpus-repo thinking as private, with transcripts/prompts in a dedicated PII-quarantine place, PII scan first, private-first — nothing public straight from transcript. That was for the on-hold corpus packet; confirm it still holds for this repo.
- **Scope of transcripts:** which chats / models / platforms count as "all of it"? Nova's chats are the ones indexed below. Superninja's VM, Fable, Grok, and other chats hold their own material and aren't in this workspace.
- **What "less ephemeral" means in practice:** a dump-as-is with one MAP.md index (the earlier corpus-repo shape), or curated per-thread READMEs? The earlier direction was dump as-is + one index; this draft follows that.

## What is already here (counts as of 2026-11-15 morning PST)

Counts are from a filesystem listing. `~/workspace/your_files/` and the per-goal `files/` directories overlap through symlinks — do **not** add the rows together.

| Where | What | Count |
|---|---|---|
| `~/workspace/your_files/` (top level) | Real files: 51 md, 5 txt, 5 py, 2 png, 2 html, 1 zip, 1 mp3, 1 json, 1 jl; plus 17 subdirectories; 3.9 MB total | 69 files |
| `~/workspace/goals/*/files/` | Across all goals (see below) | ~167 files |
| `~/workspace/user/files/` | Her uploads (see below) | 25 entries |

### Per-goal files (largest first)

- act-as-if model simulations — **96 files** (the biggest corpus: Gate, JEPA, Genie, Council, Landauer marketplace, Holder v3 + Julia, lenses, coalition)
- three-player game simulations — 16 files (coalition bargaining, forage-and-share, minority game, public-goods punishment / reacting-defector, ledger sketch)
- fresh-instance commons seed packet — 14 files (seed packets, drift-catcher, response ledger)
- plumbline governance toolkit — 12 files (seed files + breaker packets/verdicts)
- personalized sleep hypnosis (quit smoking) — 8 files (scripts + 45-min track; **keep out of main-chat-facing material per her standing rule — side-chat work**)
- three-robot learning art piece — 7 files (stack spec, attention calibration, Belnap toy)
- translation atlas — 5 files (entries, stranger packets, seed-effect pilot)
- PHR-CA exam study — 3 files (starter, materials, first-week plan)
- authority gradient activation — 2 files
- pointing machinery survey / layer audit — 2 files
- work website — 1 file (the brief; the two market-research docs live in `user/files/`)
- claude-md headline fix — 1 file
- Everything else (solar, e-bike, hacking watch, compounding failures watch, repo digest, feed watch, Floor Game, experiment ledger, holding game, repo 0, capacity registry, language toolchains, landscape map) — 0 files in their `files/` dirs; their records live in logs, memory, and chat, not as files

### Her uploads in `~/workspace/user/files/` (25 entries)

The early-material core of the archive, already on disk:

- **Resonance Topology Framework v12** — `resonance_topology_framework_12_5zbq.md` (223 KB), plus `living_summary_v4_13_0qh6.md`, `SUCCESSOR_v10_two_pictures_11_im29.pdf`, `gap_theory_v5-1_8_i15c.docx`, `DUALITY_ATLAS_10_6iwz.pdf`, `Godel_Height_Report_9_0akl.pdf`
- **Remembering Lab images** — 8 PNGs (`the-remembering-lab_the_exact_moment_television_static_become_…`)
- **vary_floors / vary_lenses scripts** — 6 Python files (Oct 17–18)
- **grok-workspace zip** — `grok-workspace_0_t76m.zip` (3.1 MB, Nov 8)
- **Work docs (Nov 15)** — California HR consulting market research + AI-in-HR-consulting brainstorm (the two docs uploaded with the study-start message)
- One photo: `1981_0_my6z.jpg`

### Not in this workspace (she supplies manually)

- Transcripts / prompts from early consumer models and other chats — the going-back-through-the-early-stuff she described as a lot of manual work. None of that is on this VM to index.
- Memory itself: `~/MEMORY.md` + `~/memory/` daily logs are the running record; whether they belong in the repo (and in what redacted form) is her call, not assumed here.
- The experiment ledger page, Holding Game (18 rooms), and repo 0 trail live in web artifacts / GitHub, not as local files — link them from the MAP rather than copying them.

## Proposed skeleton (rename freely)

```
MAP.md                     — this index, one line per item: what, where it came from, when
artifacts/                 — the your_files/ + goal files, grouped by thread below
transcripts/               — her manual uploads, one folder per chat/model/era, PII-quarantined
uploads/                   — workspace/user/files/ as-is
work/                      — PHR-CA study + work website (kept separate from the play threads)
watches/                   — hacking-incidents log, compounding-failures log (already dated logs)
```

By thread, for `artifacts/`: floors-and-lenses · act-as-if · games (holding, three-player, coalition) · translation-atlas · art (three-robot, Held) · convergence-map · infrastructure-hacks · preparedness (freeze checklist, essentials, building fill-in) · hypnosis-audio (side-chat work — flag, don't surface in main).

## Suggested order of work for the week

1. **Name the repo** (Kelly-only; Nova can't create it) and confirm private + PII-quarantine handling.
2. **Drop in what's already here** — the uploads + the Nova-side artifacts above are the low-effort bulk; a copy script can do this once the repo exists.
3. **Transcripts last** — they're the manual part, and the only part that needs her judgment per item (what's worth keeping, what's PII).
4. **MAP.md last** — one generated index over whatever actually landed, in the shape of the earlier `experiments-INDEX.json` (already in your_files).

## Caveats

- Counts will drift as the week goes on (new files land daily — e.g. `convergence-map.md` landed Nov 15 06:52 UTC, the morning this draft was counted). Re-run the listing before copying anything.
- The hypnosis audio/scripts are quit-work from a side chat; they are listed here only because they are files in the workspace, not as a suggestion to surface them in main chat.
- Nothing in this draft is posted anywhere. It lives at `~/workspace/your_files/archive-map-draft.md` until she says otherwise.
