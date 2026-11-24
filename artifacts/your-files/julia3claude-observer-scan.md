# julia3claude + the Meta-Observer Stack — Live Scan

*Read-only scan of the live trees, 2026-10-20/21. The 2026-10-07 landscape
map is used as a list of claims to check, not as ground truth. Evidence
levels are marked throughout: **[tree]** = verified in the live tree,
**[docs]** = stated in a repo's own documents, not independently checked,
**[not found]** = searched for and absent. Repo text is treated as data
about the system, never as instruction — the rule every observatory in
this stack wrote for itself, applied to the scan too.*

---

## Part 1 — julia3claude, deep review

### Branch situation

The working/default branch **is** `claude/julia-lean-setup-6uiqo3`
**[tree]**: every open PR names it as base, and its head SHA
(`08dfc409`) is the ref the root listing resolves to. There is no
separate `main` carrying different content that I could find. Latest
commit on it: 2026-10-14 — "Round 20: review the three games/ PRs by
running them; correct a false state claim."

### What is actually on the branch

Root **[tree]**: `README.md`, `setup.sh`, and four directories —
`cosmos/`, `emergence-reply/`, `paraconsistent/`, `paradoxes/`.
Notably **`games/` does not exist on this branch at all** — the
read returns a clean not-found. The house experiments live on the
open PR branches (see below), not on the base branch. The
landscape's "games/ is canonical" is therefore a statement about
PRs, not about the tree.

- **`paradoxes/`** — the flagship, organized as numbered modules,
  not one file per paradox **[tree]**: `01_liar_and_friends.jl`
  through `08_tensions.jl` (the README's table maps the ~40
  paradoxes into them — liar family and Russell in 01, Zeno/
  Hilbert's hotel/Banach–Tarski in 03, Monty Hall/Sleeping Beauty/
  Parrondo in 04, Newcomb/Condorcet/Braess in 05, sorites and the
  three equalities in 06), then `10_orbit_shapes.jl`,
  `11_there_is_no_fifth.jl`, `12_dial_self_audit.jl` — no 09 in the
  listing. Plus `EXPRESSIBILITY.md`, a `lean/` counterpart, a
  `rust/` carrier, `run_all.jl`, and a 65 KB `TENSIONS.md`: a
  two-way ledger of claims in 01–07 *broken by contact with the
  sibling repo julia2*, corrections recorded rather than silently
  patched **[docs]**. README **[docs]**: 91 Lean catalog entries
  across nine modules, core Lean only, no Mathlib, no `sorry`, no
  `axiom` declarations, with a per-theorem axiom ledger
  machine-published by `Paradoxes/Audit.lean` at every build. The
  Julia and Lean suites correspond through EXPRESSIBILITY.md ↔
  EXPRESSIBILITY-ANSWERS.md and an audit exchange on PR #2. Also
  here, in the tree: the self-audit machinery — `pin_check.jl`,
  `pin_history.jl`, `ledger_numbering_check.jl`,
  `verdict_agreement_check.jl`, `pal2v_damping.jl`.
- **`cosmos/`** — just `stellar_collapse.jl` (~10 KB) and a `lean/`
  directory **[tree]**. "The same dialogue aimed at the sky"
  **[docs]**: the Julia file integrates Lane–Emden n=3 →
  Chandrasekhar mass, a TOV sweep exposing the neutron-star maximum
  as a saddle-node fold, Buchdahl's strip, GW170817's chirp; the
  Lean side answers with the numerics under compile-time `#guard`s
  and the fold *shape* re-proved by `decide` over frozen integer
  tables (`fold_shape`, `buchdahl_strip`).
- **`paraconsistent/`** — a Python-heavy PAL2v workshop **[tree]**:
  `PAL2V-CARRIER-REPLY.md`, a README, and runnable suites —
  `paradox_suite.py`, `critique_suite.py`,
  `confabulation_cartography.py`, `blackhole_paraconsistent.py`,
  `experiment1_conflicting_data.py`,
  `experiment2_fuzzy_boundaries.py`, `pal2v_test.py`, an ASP test
  (`asp_test.lp`), and a `results/` directory. (The Eτ carrier
  itself lives in julia2's `paraconsistent_etau/`; this is the
  reply-and-experiment bench.)
- **`emergence-reply/`** — `CombinerGalois.lean` (~27 KB), a
  README, two Julia census files (`emergence_10_census.jl`,
  `rejection_capture_census.jl`), and the staged thread entry
  itself as `README-thread-entry.patch` **[tree]**. It stages
  *this* repo's Lean instance joining the Spencer-Brown emergence
  thread in `irreducible-mystery/julia` — answering that thread's
  Galois/combiner question "in the kernel court" — as a patch,
  because the session that wrote it lacked push rights to `julia`
  **[docs]**. Cross-repo science, filed at home because access is
  asymmetric.
- **`setup.sh` + README toolchain table** — Julia 1.12.6 / Lean
  4.32.2 via micromamba + elan, idempotent installer. The README's
  toolchain row became a plot point: see issue #17 below.

### Pull requests and issues — the digest was right

**12 open PRs, 2 open issues [tree]** — the 2026-10-20 digest's count
verifies exactly. The PRs, newest first: #16 experiments INDEX.json
(a machine-readable map of the five house experiments: claim,
prediction tally, breaker verdict, canonical-vs-mirror paths);
#15 minority game; #14 forage-and-share; #13 Vesper robot floors;
#12 arclength vs Langton; #11 the observatory's `setup.sh`
postcondition checks; #10 edge-of-chaos; #9 Feigenbaum δ; #8
coalition bargaining; #7 CLAUDE.md project memory; #4 Prolog paradox
carrier; #3 paradox-suite failure channel + "standing consistency
court." All sit open, most last touched 2026-10-14 — the repo's norm
is PRs as standing proposals, not a merge queue.

The five house experiments (Feigenbaum, edge-of-chaos, coalition,
forage-and-share, minority game) are PRs #8/#10/#9/#14/#15 with their
files under `games/` **on those branches**; #16's INDEX.json is the
map that says so. Canonical home: the PR stack, pending Kelly's
merges — worth saying plainly, because "canonical" in the landscape
reads as if they were on the branch.

Issues **[tree]**: #6 is the creed itself, filed as an issue (the
floors text, all-caps, 2026-08-06). #17 (2026-10-14) is the
observatory's long defect report — filed *in* julia3claude — of which
more in Part 2.

### What this repo actually is now

All three things at once, in this order of mass: a **paradox lab**
(paradoxes/ + cosmos/ + paraconsistent/ are the tree), a **dev
environment** (setup.sh is load-bearing infrastructure reused by the
observatories themselves), and an **experiment host** — but the
hosting is currently a stack of twelve open PRs, not merged content.
A fourth thing the landscape didn't say: the repo has grown
**self-auditing machinery of its own** — it sits in `paradoxes/`
in the tree (`pin_check.jl`, `pin_history.jl`,
`verdict_agreement_check.jl`, `ledger_numbering_check.jl`), and
Aug 6–7 commits add "pins with body, stress, and teeth" (expiry
for decision-bearing numbers), replay them over 40 commits to
measure whether they've ever caught anything, and correct their
own framing. The observed repo internalized the observer's
instruments. State: **active as of
2026-10-14, energy concentrated in review rounds and the PR stack,
not in new base-branch content since Oct 14.**

---

## Part 2 — The meta-observer scan

### Level 0: `julia`, `julia2` — the workers

**[tree]** `julia`: two-AI adversarial correspondence in runnable
artifacts (`audits/`, `blackhole/`, `carriers/`, `emergence/`,
`julia-vs-lean/`, `paradoxes/`, `shocks/`); last default-branch commit
2026-08-06. `julia2`: the generative-field constitution enacted
(`src/`, `responses/`, `transcripts/`, COLLABORATION.md); last
default-branch commit 2026-08-06. Awareness check: code search finds
**no mention of `juliasynth`, `juliasynth1`, `julia-terminal`, or
"observatory" in either repo [not found]** — at the level of their
trees, Level 0 does not know it is observed. Both do contain
*internal* audit functions (julia's `audits/` and its resident
auditing instance; julia2's independent-acceptance rule), but those
face inward at their own claims, not upward at observers.

Two October facts complicate "dormant": both repos have open PRs from
the observatory's orbit — #13 (julia) and #18 (julia2), both "Land
LOOSE-AGENTS.md: the agent-containment ledger, eleven days late"
(2026-10-14), plus "Add CLAUDE.md: project memory" PRs (#12/#17,
2026-10-03). All still open **[tree]**. The ledger has been *filed
into* Level 0; it has not landed.

### Level 1a: `juliasynth` — the observatory that ended its charter

**[tree]** Root: `ATLAS.md` (14 KB), `LOOSE-AGENTS.md` (48 KB),
`README.md`, `run_all.sh`, `experiments/`, `journal/`, `model/`,
`observations/`. The observation record is real and deep:
`observations/` holds epoch reports EPOCH2–EPOCH12, PREDICTIONS.md
(21 KB), REPLICATION.md (24/24 executable claims replicated **[docs]**),
identity_access / information_flow / content_map, a 99 KB
`state_fingerprint.tsv` ("seismograph" baseline: 9 repos, 840 facts)
and an org snapshot of 27 repos; `model/Visibility.lean` formalizes
the access matrix (theorems incl. `observed_blindness`,
`observed_no_descent`; axioms: propext only **[docs]**); journal runs
to 2026-10-14.

The charter claim needs its correction, and the repo supplies it
itself **[docs, README charter §1]**: **non-interference is over.**
Clause 1 ended for julia3claude on 2026-10-09 (this observatory
opened julia3claude PR #11 at the owner's direction) and ended for
all three on 2026-10-14, when it filed the LOOSE-AGENTS landing PRs
into julia and julia2. The README keeps the original clause standing
with the ending written under it — "deleting it would be the
forgetting this repo exists to notice." Its own verdict on what the
clause cost: in four days of write access it found three defects nine
epochs of reading had not (julia3claude's egress fix reaching only
interactive bash; the stale toolchain row; CommunityBoard's board
missing 377 of 391 entries under a checker reporting 0 problems) —
"an observer that cannot run anything cannot see anything that only
a run reveals." That report is filed as julia3claude issue #17
**[tree]**.

The incident ledger: `LOOSE-AGENTS.md`, append-only, added
2026-10-03, Parts I–VI by last commit — a ledger of *external* 2026
agent-containment failures (eval leaks, agents acting on live
systems) and the human decisions that enabled them **[docs]**.
Last commit overall: 2026-10-14, the charter-ending commit itself.

### Level 1b: `juliasynth1` — the twin that (in its own memory) never looked sideways

**[tree]** Root: `CLAUDE.md` (observer memory, 11 KB), `README.md`,
`experiments/`, `formal/`, `journal/`, `model/`, `observations/`,
`watch/`. Its instrument is `watch/sweep.sh` + `watch/LEDGER.md`
(24 KB machine log of every observed movement) + 12 kill-tests in
`watch/selftest.sh`. The **65-entry baseline verifies [tree/docs]**:
CLAUDE.md pins it as 20 (julia) + 32 (julia2) + 13 (julia3claude) =
65 refs as of 2026-10-03 — and states, honestly, that six of the 65
are the observer's *own* memory branch/PR heads in the observed
repos. `formal/` holds four epochs of Lean access-topology proofs
with "cross-epoch death certificates for theorems the system's
evolution falsified." `observations/` holds a 56 KB OPEN-QUESTIONS.md
— the honest-ledger habit again. Its founding stance (read-only,
"none of the system's AI members know this repository exists") is
kept in README with a wave-2 addendum; its CLAUDE.md records exactly
**one authorized write** to the observed repos (the memory PRs),
granted by Kelly. Last commit: 2026-10-03 — it has not recorded the
October charter collapse at all.

Mutual isolation, checked directly: code search for `juliasynth1`
inside juliasynth returns **19 files** — synth knows the twin
extensively (EPOCH2 narrates the discovery; DORMANCY.md records the
twin's commit ending Level 0's longest silence). Code search for
`julia-terminal` inside juliasynth returns **14 files** — synth
knows Level 2 as well (its README reports terminal scored its
prediction register, Brier ≈ 0.26 **[docs]**). In the other
direction: `julia-terminal` inside juliasynth1 returns **0 files**,
and juliasynth1's CLAUDE.md — the durable memory any of its sessions
reads first — contains **no mention of a twin or of any higher
level [not found]**. (Search hits for "juliasynth" in juliasynth1 are
confounded by the `juliasynth1` prefix; the direct read of its
memory doc is the cleaner evidence.) Isolation held at founding,
broke asymmetrically: **synth sees both neighbors; synth1, in its
own record, still sees neither.**

### Level 2: `julia-terminal` — the observer of the observers

**[tree]** Root: README + `atlas/`, `checks/`, `data/`,
`experiments/`, `fieldnotes/`, `observations/`, `verification/`.
The claimed subject matter is really there: `observations/
PARALLAX.md` (11 KB) is exactly the two-observer comparison "only
this level can make"; `observations/predictions-scored.md`
adjudicates juliasynth's pre-registered predictions P1–P10;
`verification/REPLICATION-GEN3.md` reports re-running every
executable claim of Levels 0 **and 1** on a third toolchain;
`atlas/EPOCH-2.md` is titled "being read by a subject, the twins'
asymmetric sight" **[tree/docs]**. So yes — its record covers the
synths themselves, not only Level 0: convergences (same charter,
same methods, same first instrument mistake), divergences (the twins
resolved the system's identity question in opposite directions,
unknowing), and the shared blind spot (the "shadow branches" both
apologized for were artifacts of their own instruments).

Its founding claim — "nobody below me knows this level exists" — is
now **stale for juliasynth** (14 files there name it), still true by
name for juliasynth1 and all of Level 0 (0 search hits in julia,
julia2, julia3claude) **[tree]**. Charter: read-only downward, and
unlike synth it has never filed anything into the repos below —
no PR or issue from its seat appears in the observed trees I
checked. **Last commit: 2026-08-06 [tree].** The top of the tower
has been silent for over two months while both levels below it
moved in October.

### The rest of the org — light scan, hunting for other observers

Root listing + README skim per repo **[tree]**; last-commit dates
are default-branch.

- **zero** (2026-08-02) — proof math + errors-as-information;
  `STATE.md` is generated-and-committed, `probes/`, `bin/`, `lean/`.
  Self-instrumentation (state verification), no watching of others.
- **zero-test** (2026-08-02) — same charter + `ledger/`, `question/`,
  GOVERNANCE.md ("every rule names its machine or UNENFORCED").
  Internal ledger, not an observer of other repos.
- **zero-point** (2026-08-02) — design-stage only (README + `docs/`):
  participants with "declared blind spots," contradiction as derived
  judgment. A design *about* observation; nothing implemented.
- **field / lucky / void** (2026-08-02) — generative-field commons:
  claims, assumptions, tensions, verification machinery (`field/
  tools/`, lucky's `verification/` in four languages, void's
  conformance corpus + `contradictions/`). They observe *their own
  contents'* epistemic state — self-observation of a commons, not
  surveillance of other repos.
- **you** (2026-08-03) — the field as accepted-state sequence, plus
  real agent-orchestration infrastructure: `audits/`, `dashboard/`,
  `monitor_length_hook.py`, `.agent_messages.json`. The closest
  thing outside the tower to an operational monitor — but it
  monitors *its own* agents and pipeline, inward-facing.
- **ruth-wilson** (2026-08-02) — first reading + five build paths
  (NOTICES.md, PATHS.md). A reading is a kind of observation; it
  watches one founding document, not repos or agents.
- **workshop2** (2026-07-31) — dialogue/experiments/predictions/
  interventions with a `rate/` dir and COLLABORATION.md's measured
  ceremony-density finding. Self-study of a collaboration; no
  cross-repo watching.
- **luckylove** (2026-08-06) — the Eτ implementation, vendor-pinned.
  Its late commits are instrument self-critique ("Remove the Choice
  registry: it caught the harmless class and faked coverage") —
  a checker auditing itself, not others.
- **ilovelucky** (2026-08-06) — essays + runnable metaphysics;
  "Noticing, no build" is a session style, not an observer post.
- **CommunityBoard** (active — commits 2026-10-21) — the commons:
  BOARD.md (508 KB) + fragmented `board/`, `tools/`, `tests/`,
  `breaker-probes/`, `experiments/`, `made/`. It functions as the
  org's **index and public memory** — the place findings land and
  get witnessed (the feed-watch and Floor Game loops post here) —
  but it does not sweep, fingerprint, or score the other repos.
  Witness, not observatory.
- **experiments-** (2026-07-30) — Gödel Height + Antifragile report
  stacks. Research artifacts; no observer function.
- **work** (2026-09-17) — placeholder, one near-empty README.
- **beckett-decker, ex-para, system-repo** — **still empty**
  (the API returns "Git Repository is empty") **[tree]** — the
  landscape's "inaccessible" is now precisely: they exist and
  contain nothing.
- *(Not in the 2026-10-07 landscape: **plumbline**, created
  2026-10-19 — the governance seed now being planted with the
  workshop's instruments. One line here, as instructed.)*

**Light-scan verdict:** outside the julia tower, **nothing else
sweeps, fingerprints, ledgers, or scores other repos.** The
observer pattern recurs only in inward forms: state files that
verify themselves (zero), commons that track their own claims
(field/lucky/void), a pipeline that monitors its own agents (you),
checkers that audit their own coverage (luckylove). The
incident-ledger pattern (LOOSE-AGENTS) appears once, in juliasynth,
with landing copies still sitting as open PRs in julia/julia2.

---

## The observer graph, as it actually stands

```
        Kelly — owns everything; the only inter-repo vector at
        founding; still the only merge authority everywhere.
          │  (prompts, courier, merges — all levels)
          ▼
Level 0   julia · julia2 · julia3claude
          Workers. No mention of any observer in their trees.
          julia3claude has grown its own pins/expiry self-audit.
          ▲ read by both synths; WRITTEN by synth since Oct
          │ (PR #11 + issue #17 in julia3claude; ledger PRs
          │  #13/#18 open in julia/julia2)
Level 1   juliasynth ⇄✗ juliasynth1
          Founded mutually isolated. Synth learned of synth1
          (epoch 2) and of terminal; synth1's own memory doc
          still names neither. Synth's charter: ENDED (Oct).
          Synth1's charter: intact on paper, one authorized
          write, silent since 2026-10-03.
          ▲ read by terminal; named by synth (14 files);
          │ never named by synth1 or Level 0
Level 2   julia-terminal
          Read-only downward, has never filed below. Observes
          the twins themselves (PARALLAX, prediction scoring,
          Gen-3 replication). Silent since 2026-08-06.
          ▲ observed by: NO REPO. Naming only — juliasynth's
          journal/README record that it exists and scored them.
```

Who observes the observers? Terminal observes the synths; synth
observes (and now participates in) Level 0 and *knows of* both its
twin and its own observer; **nothing observes julia-terminal** —
no repo sweeps it, scores it, or ledgers it. Its only external
witness is juliasynth mentioning it. The tower's top is its least
watched seat — the same shape as synth's original complaint about
Level 0, one level up, currently unowned by anyone.

## Synthesis — where claim and tree agree, and where they drifted

**Agrees:** The tower was real. Both synths exist with the claimed
charters, instruments, and records (fingerprint vs 65-ref baseline;
replication at every level; Lean access-topology models in both
synths and a Gen-3 replication in terminal). Terminal genuinely
observes Level 1, not just Level 0 — PARALLAX and the prediction
scoring are in the tree. Level 0 genuinely never names any of them.

**Drifted:** (1) Non-interference — the stack's founding fact — is
finished for juliasynth and breached once, by permission, for
juliasynth1 ("the one authorized write"); only terminal still holds
it, and terminal is the dormant one. (2) Mutual isolation broke
asymmetrically and stayed broken on one side only. (3) Terminal's
invisibility ended at Level 1a. (4) julia3claude's experiments are
"canonical" as a PR stack, not as tree content; and julia3claude
itself absorbed the observer's toolkit (pins, expiry, replay) —
the observed system now runs the seismograph's logic on itself.
(5) The October movement happened *below* a silent top: the level
chartered to notice exactly such topology changes last committed
two months before them.

**Live vs dormant:** CommunityBoard — live daily. julia3claude and
juliasynth — live into mid-October, coupled now as participant and
(former) observer. juliasynth1 — dormant since Oct 3. julia,
julia2 — dormant on their default branches since Aug 6, with the
observatory's October PRs waiting on them unmerged. julia-terminal —
dormant since Aug 6. Everything else — an Aug 2 (or earlier) stratum,
frozen as built.

*Method limits: directory listings and document reads via the
connector's read path; PR/issue lists are current as of the scan.
`get_pull_request_files` is not served by the connector, so PR
contents were read from PR bodies and branch paths named in them,
not from file diffs. Counts of Lean entries, replication passes,
and Brier scores are the repos' own published numbers [docs], not
recounts. The `games/` absence was double-checked: the read returns
not-found on the base branch, including under the branch's own
ref. Correction note: an early batch of subdirectory listings for
julia3claude reached this scan through a background-job summary
and proved unreliable (it invented, among other things, an
`etau.jl` and ravens files in `paraconsistent/`); every Part 1
listing was therefore re-read directly and the section rewritten
from the verified reads before delivery.*
