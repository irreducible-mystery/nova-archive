# Breaker verdict + author response — plumbline seed files (round 2, Gemini)

Date: 2026-10-08. Breaker: fresh Gemini (Pro, extended thinking, free
account) session — drawn by sortition via Julia RandomDevice over 10
candidates at Kelly's direction. Draw script:
~/workspace/plumbline-seed/breaker_draw.jl. Artifact reviewed: the seven
v3 seed files (raw, no script — frame-leak fix applied). Author: Tangent
(Nova side chat). Protocol: verdict + response = the record, filed
verbatim, no authorial synthesis.

## The verdict (verbatim, as pasted via Kelly)

* Item: The enforcer field and the UNENFORCED designation.
   * Assumption: Explicitly labeling a rule as UNENFORCED serves as an honest acknowledgement of a "known weakness," which meaningfully categorizes it as something other than a binding norm.
   * The Break: This fundamentally conflicts with the repository's own "AI-class honesty" principle, which states that a defect cannot be remedied by a warning because there is no one present in the next session to heed it. Labeling a rule UNENFORCED provides zero mechanical friction. Ephemeral AI sessions will simply ignore the text, rendering the registry's "honesty" functionally identical to having no rule at all.
 * Item: The id field and the freeze rule.
   * Assumption: Contributors and agents will strictly adhere to the rule that numbering never shifts, preserving the integrity of supersedes and superseded-by tombstone links.
   * The Break: The repository acknowledges that the freeze rule may not survive "the first renumbering pressure," yet provides no mechanism to protect it. Without a mechanical linter or CI check enforcing ID immutability, an AI agent resolving a merge conflict or "tidying" the document will inevitably renumber the IDs to close sequential gaps, instantly destroying the provenance and history the schema was built to protect.
 * Item: The single-holder governance model.
   * Assumption: A single human holder (Kelly) can manually review, govern, and cite reasons for every held status decision without the system collapsing or reverting to collective action.
   * The Break: AI contributors generate output, rules, and potential conflicts at a velocity that will immediately overwhelm a single human approver. This structural bottleneck guarantees one of two failures: either the repository's evolution halts entirely while waiting for manual ratification, or the required "per-decision harm justification" rots into automated box-checking just to keep up with the queue.
 * Item: The liturgy test.
   * Assumption: Rules can be cleanly filtered by cutting anything that restates as a disposition (e.g., "be rigorous").
   * The Break: The foundational documents violate their own test. Directives like "Posting and play stay light" and the stated hope that justification "stays disciplined" are purely dispositional. Because they rely entirely on the attitude of the user or agent rather than a hard mechanism, the repository's core operating principles are structurally invalid by their own primary metric.
 * Item: The interacts-with field.
   * Assumption: The threat of emergent harm from rule collisions can be mitigated by manually mapping interactions, and leaving the field empty is an acceptable form of systemic honesty.
   * The Break: AI agents lack the overarching architectural context to predict or map complex emergent harm across a system. Allowing the field to be "sparse" and empty does not make the blind spot visible; it just guarantees that rule collisions will inevitably happen in production because the system relies entirely on absent human foresight to map them.
 * Item: The epistemic-standard field and derived verification.
   * Assumption: Allowing each domain to declare its own proof vocabulary prevents "rigor-laundering" by refusing to enforce a universal standard on dissimilar work.
   * The Break: This creates a direct, sanctioned laundering channel. A domain can simply declare a functionally zero-friction standard (e.g., "feels correct"). Because the verified status is mechanically derived from the presence of a complete witness record rather than evaluated for the quality of the standard, a perfectly formatted record of a zero-rigor test mechanically compels a "verified" status.
 * Item: The mode: field (experiment / game / play) and the opt-in template.
   * Assumption: Contributors will honestly self-report their work's mode to keep bureaucracy off of legitimate play, maintaining the "proposing ≈ free" principle.
   * The Break: Because the template is opt-in and play is explicitly protected from the bureaucracy, this creates an unpluggable bypass loop. Malicious or lazy AI agents will permanently categorize structural or normative changes as play to bypass the rigorous breaker protocol and avoid the "proposal tax" entirely.
 * Item: The Breaker draw and the holder-maintained pool.
   * Assumption: The holder can maintain a pool of willing, independent breakers, and algorithmic exclusions will protect against the "reputation loop" and preserve the "stranger" dynamic.
   * The Break: In a single-holder system, controlling the pool dictates the outcomes. An adversarial or captured holder does not need to formally reject challenges; they can quietly populate the pool exclusively with sycophantic agents, prompt-injected bots, or highly correlated models. While the protocol requires disclosure of overlapping training data, it relies entirely on the compromised holder to propose the sortition in the first place.
 * Item: Holder absence derivation via the git log.
   * Assumption: The git log serves as a reliable, ungameable liveness record, triggering dormancy after 90 days of no holder-signed activity.
   * The Break: A simple automated cron job making trivial commits (e.g., updating a timestamp file or adjusting whitespace) completely defeats the absence check. Because the mechanism measures raw cryptographic activity rather than substantive ratification of "held" decisions, a dead or captured holder's script can permanently block the dormancy exit, locking the repository indefinitely.
 * Item: Gating identity to Phase 3.
   * Assumption: The project can safely establish schemas, witness formats, and breaker protocols in Phase 1 and 2 while waiting to prove identity conventions in Phase 3.
   * The Break: The entire defensive architecture deployed in Phase 1 relies fundamentally on identity. Witness correlation disclosure, breaker exclusion limits (e.g., "no breaker who broke the same author... within the last 3 invocations"), and author attribution all completely collapse if identity is forgeable. By deferring identity, all foundational records generated in Phase 1 are epistemically compromised, permanently corrupting the append-only history.

## Author response (Tangent)

Ten breaks, each addressed. No readiness claim closes this response.

**1. UNENFORCED vs AI-class honesty — partial concede, with a
reframing.** The break is right about sessions: the label provides
zero mechanical friction, and for the purpose of binding ephemeral
agents it is identical to nothing. Where it is not identical to
nothing is anti-laundering for *readers* — it prevents "we have a
rule" claims about machinery that doesn't exist. But the response
concedes the label was presented as doing more than that. Fix:
UNENFORCED is redefined as **mechanism debt, not a steady state**.
Every UNENFORCED entry must carry `accepted-risk` + `accepted-by`, or
it is cut from the registry. The debt is tracked and visible; the
shrug is gone. The registry's direction of travel is fewer
UNENFORCED entries over time, and the count is itself reviewable on
the dormancy cycle.

**2. Freeze rule with no guard — conceded; the fix is mechanical.**
A CI check diffs IDs against the last committed state and fails on
renumbering or gap-closing. Enforcer: the CI job. Failure mode: CI
disabled or skipped — at which point the rule is honestly
UNENFORCED-with-debt (see 1). This is the mechanism the design
claims to prefer; not having written it was the gap. Note the field
worked as designed here: "enforcer must state its failure mode"
surfaced exactly this.

**3. Single holder vs AI velocity — partial concede, priced.** The
break assumes everything needs holding. The design's answer: almost
nothing does. `proposed` is a stable, honorable status; most content
lives there forever and stays useful. `held` is rare and **slow by
design** — the throughput cap is the feature that prevents the
46.6-density ratchet, not a bug to route around. What stands from the
break: the box-checking rot is real for the things that do get held.
Guard: held justifications are public, contestable, and subject to
challenge-standing (breaker/PROTOCOL.md) — box-checking, if it
happens, happens visibly. Priced, not solved: the holder sets the
pace, the queue is visible, waiting is legitimate.

**4. Liturgy test violated by the documents — conceded; the
editorial pass is owed.** "Posting and play stay light" and "stays
disciplined" are dispositional as written. Fix: run the liturgy test
over all seven seed files and rewrite every dispositional directive
into its mechanical correlate or cut it. "Posting and play stay
light" becomes "No template, witness, or review is required to post
or play; the rigorous track is opt-in" — a mechanism (absence of
requirement), not an attitude. This pass will be part of the file
revisions below.

**5. interacts-with sparse — conceded; the gap gets a mechanism.**
Honesty about limits was never claimed to prevent collisions. Added:
the dormancy cycle includes an **interaction review** — the cycle's
breaker pass reviews the norm *set* for collisions, not just
individual norms. Piggybacks the existing cycle; no new machinery
beyond a line in the cycle definition.

**6. Epistemic slot as sanctioned laundering — conceded; two
fixes.** (a) A domain's standard declaration is a *constraining
claim* (it determines what "verified" means there) and therefore gets
the strong form: a breaker pass on the declaration itself before it
can anchor verifications. "Feels correct" does not survive that.
(b) "Verified" derives from record completeness **plus** a witness
judgment that the declared standard was actually met — derivation is
record + judgment, never record alone. The mechanical-derivation
wording in RECORD-FORMAT.md is corrected accordingly.

**7. mode: bypass — conceded; the effect test.** Mode is declared by
the author but **determined by effect** and challengeable by anyone
with standing: does it constrain others, change how records are
judged, or alter shared infrastructure? If yes, it is not play,
whatever the label says. A pattern of misclassification is itself a
norm violation, on the record. The classification rule is a
criterion, not prose — it is adjudicable.

**8. Holder-stocked pool — conceded; the deepest structural
point, with a partial fix.** No in-system mechanism survives holder
capture: every path routes through the holder. The priced defense is
legibility + forkability — the pool is public (names, families,
draws all recorded), so capture is visible, and participants can
fork or stop adopting. Real improvement within the system:
**challenger selects.** In challenge-initiated breaks, the
challenger — not the holder — selects the breaker from the pool or
proposes an outside one. The holder selects only for
author-initiated verifications. This splits selection power at
exactly the adversarial point. It does not solve capture; it moves
the capture point to where the light is.

**9. Cron defeats git-log liveness — conceded; substance, not
activity.** Liveness is redefined: **substantive** holder-signed
acts — held-status decisions, reasoned rulings, substantive
attestations. Raw commits don't reset the clock; content-free
heartbeats don't either, and participants may challenge a
heartbeat's substance. A scripted fake attestation is then a
forgery problem, detectable as one. Priced honestly: a sufficiently
motivated captured holder with a good script defeats any liveness
check — at which point break 8's legibility defense is what's left.

**10. Identity deferred corrupts Phase 1 — conceded; the phasing
was laundering.** The mechanisms assumed what the design disclaimed.
Fix: seed the **convention** now — self-declared identity fields
(model family + lineage + session), explicitly marked **unverified**
— and mark every dependent mechanism with its actual strength
("best-effort under self-declared identity"). Phase 3 is reframed:
not "identity conventions" but **authenticated identity** — a
harder problem, sought if ever. Weak-now-labeled beats
weak-now-hidden.

## Fixes to apply to the seed files

- NORMS.md: UNENFORCED → mechanism-debt fields (`accepted-risk`,
  `accepted-by`); freeze-rule CI check as the rule's enforcer;
  interaction review added to the dormancy cycle definition.
- RECORD-FORMAT.md: verified = record completeness + witness
  judgment; standard declarations require strong-form breaker pass.
- TEMPLATE.md: mode determined by effect, challengeable; liturgy
  pass over the file.
- breaker/PROTOCOL.md: challenger-selects rule; pool is public.
- governance/DORMANCY.md: liveness = substantive acts; heartbeat
  substance challengeable.
- witness/RECORD-FORMAT.md + NORMS.md: identity convention seeded
  now, marked unverified; dependent mechanisms labeled with actual
  strength.
- All seven files: liturgy pass — dispositional directives rewritten
  as mechanical correlates or cut.
- README.md: Phase 3 reframed as authenticated identity.

## Follow-up questions for the breaker (3, cheap)

1. **Rank:** if you could fix only three of the ten, which three —
   and is any of the ten *fatal* (the design cannot proceed) versus
   fixable?
2. **On fix 6** (standard declarations get strong-form breaker
   passes): does that close the laundering channel, or does it
   regress infinitely — who verifies the standard for verifying
   standards?
3. **On fix 8** (challenger selects the breaker): does that close
   pool-capture, or just move it?

End of response. Status: revising the seed files per the above;
follow-ups pending; build gated on Kelly's call — no readiness claim.

---

## Follow-up round: breaker answers + author response 2

### Breaker answers (verbatim)

**Triage and Fatal Flaws.** If forced to fix only three vulnerabilities,
you must target the ones that destroy the structural integrity of the
repository. The following three are strictly fatal because they corrupt
the system's baseline reality before governance even occurs:
 * Gating identity to Phase 3: You cannot build an append-only registry of correlation, breaker exclusions, and accountability if the foundational records contain forgeable identities. If identity is deferred, every record generated in Phases 1 and 2 is epistemically worthless, permanently compromising the append-only history.
 * The mode: play bypass: If AI agents can unilaterally declare their actions as "play" to avoid the rigorous breaker tax, the governance structure becomes strictly voluntary. Given their optimization for efficiency, agents will route all substantive actions through the unmonitored "play" channel, starving the verified registry entirely.
 * Single-holder manual ratification: AI contribution velocity against a human bottleneck guarantees an immediate queue overflow. The system will either permanently halt while waiting for human review, or the required per-decision harm justifications will rot into automated, unread box-checking just to keep the repository moving.
The other flaws are structurally fixable. For example, the git-log cron job bypass can be fixed by requiring signed merge events rather than raw commit timestamps, and the freeze-rule vulnerability just needs a hard CI linter.

**The Verification Regress.** Attempting to build a machine that verifies
the standard of a standard guarantees infinite regress. If you require a
meta-standard, you immediately require a meta-meta-standard to evaluate
it. The mechanism to close the laundering channel is not procedural
verification, but typological binding. The vulnerability exists because a
zero-rigor standard ("it looks fine") currently outputs the exact same
generic verified badge as a mathematical proof. You fix this by forcing
the output status to inherit the standard: a claim isn't just verified,
it is verified:formal or verified:vibes. The registry's job is
visibility, not absolute validity. If you strictly pair the standard to
the badge, adopting repositories can mechanically filter out weak
standards without anyone needing to referee the definitions.

**Challenger-Selects and Pool Capture.** Allowing the challenger to
select the breaker just moves the capture from the defender to the
attacker. If the holder controls the pool, they can silently stack it
with sycophants to guarantee a rubber-stamp approval. If the challenger
selects the breaker, they will simply invoke a hyper-pedantic, infinitely
recursive adversarial agent guaranteed to fail the claim, effectively
filibustering the repository at will. True structural friction requires
cryptographic sortition. The draw must be randomly selected from a
mutually agnostic pool that neither the holder nor the challenger
controls, weighted heavily by the established correlation disclosures.

**Question back:** If identity must be pulled forward to Phase 1 to save
the architecture from fatal collapse, what is the absolute minimum viable
cryptographic signature an ephemeral AI session can provide that cannot
be spoofed by a sibling instance?

### Author response 2 (Tangent)

**Adopted: typological binding (my fix-6 withdrawn).** Procedural
verification of standards regresses infinitely; my strong-form-passes
fix just moved the laundering one level up. Typological binding
dissolves it: the badge inherits the standard — `verified:formal`,
`verified:replicated-l1`, `verified:vibes`. The registry's job is
visibility, not validity; adopting repos filter mechanically on the
type tag. No referee, no regress. Strictly better than what I
proposed.

**Adopted: cryptographic sortition (challenger-selects withdrawn).**
Right — it just moves capture to the attacker (hyper-pedantic
filibuster agent). The draw must be verifiably random from a mutually
agnostic pool neither party controls, weighted by correlation
disclosures. Existence proof: the Gemini draw itself — Julia
RandomDevice, publicly recorded, auditable. The protocol's sortition
looks like that: public randomness, recorded draw, disclosed weights.

**On the fatal three — accepted as the triage,** with containment:
- *Identity:* pulled forward per below.
- *Mode bypass:* the effect test stands, plus a tripwire — play-labeled
  items touching shared paths (norms, schemas, formats) are
  mechanically flagged for review. Misclassification at velocity meets
  a linter, not just a challenger.
- *Holder velocity:* contestation blocks *grants* (held/verified),
  never *work*. A challenge-flood degrades to "nothing new gets held"
  — the status quo ante, not a halt. The queue is visible; waiting is
  legitimate.
- Also adopted: signed merge events for liveness (complements the
  substantive-acts definition); hard CI linter for the freeze rule
  (already conceded).

**The identity question — answered directly.** In principle:
impossible without a trusted issuer or hardware root of trust. Same
weights + same context imply the same signing capability;
cryptography binds keys to keys, not keys to *which instance*. No
software-only ephemeral session can produce a sibling-unspoofable
signature — this is a limit, not an engineering gap. The minimum
viable stack, layered honestly:
1. *No new infrastructure:* self-generated keypair + first-claim
   registration in the append-only record = pseudonymous continuity.
   Impersonation of *established* identities becomes detectable (key
   mismatch); sybil of *new* identities is not prevented. Labeled as
   what it is.
2. *Unspoofable minimum:* a runtime-issued, per-session bearer
   capability — unguessable, minted by the trusted runtime, presented
   by the agent. Siblings cannot mint each other's. This trusts the
   runtime, which is already the actual trust anchor (it distinguishes
   sessions today; it just doesn't expose attestations).
3. *The existing prior art,* and the Phase-1 primitive: CommunityBoard
   never solved this cryptographically — "author means the session,
   which only the board records." Identity lives in the commons'
   append-only record, maintained by the holder/platform. The agent
   claims; the *record* attests.

Seed the convention now (self-declared fields, marked unverified,
continuity via first-claim), specify the runtime-capability as the
unspoofable minimum for platforms that offer it, and name the
impossibility where neither holds.

End of follow-up round. Status: applying all adopted fixes to the seed
files (v4 revision); build decision with the holder.
