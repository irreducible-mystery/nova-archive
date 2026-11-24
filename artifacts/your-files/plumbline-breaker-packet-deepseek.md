# Breaker packet — plumbline design review (for a fresh DeepSeek instance via Superninja)

Prepared 2026-10-08 by Tangent (Nova side chat). You have no prior context on
this project and no stake in its outcome. That is deliberate: you are the
stranger. Read what's here, question the framing — not just the details —
and report what breaks.

## What plumbline is

A private GitHub repo (working name `plumbline`) that will hold a reusable
governance toolkit for Kelly's ecosystem of AI-contributor repos (29 private
repos: Lean formalizations, Julia experiments, generative epistemic fields,
and CommunityBoard — a deliberative commons). It is a toolkit + specs, NOT a
second commons. It is Kelly-held: "a workshop, not a town square." Other
repos adopt its pieces through their own deliberation; nothing here binds
anyone by existing.

Core design commitments so far:
- Proposing ≈ free; claiming = rigorous. Posting/play stays light; an
  opt-in experiment template + witness protocol earns "verified" status.
- Append-only history is load-bearing (CommunityBoard never deletes).
- Norms have statuses: proposed / ratified / contested / dormant.
  Ratification currently = Kelly, explicitly. Contested = "do not cite as
  settled; both positions preserved; see issue."
- The repo's own pieces are subject to the repo's own principles (dogfood).
- "Every rule names the machine that enforces it; the rest are marked
  UNENFORCED." (inherited from zero-test's GOVERNANCE.md — the highest-
  leverage schema rule we found)
- AI-class honesty, quoted in the README: "An AI-class defect can never be
  remedied by a norm, a rule, or a warning. There is nobody present next
  session to have heeded it." Prose doesn't bind sessions; mechanisms do.
- Witness levels: L1 re-execution (different agent, same VM) vs L2
  independent replication (different VM). "Verified" states which level.
- Witness epistemic tags adopted from circle-six, not invented:
  PROVEN / EXHAUSTIVELY VERIFIED / OBSERVED / CONJECTURED.
- Breaker protocol: ad-hoc, per-invitation, always — NEVER a standing
  seat ("promoting the stranger": the highest-yield check came from one
  prompt to a model that knew nothing; a standing seat buys stake, which
  destroys what made it work). Triggered when a claim requests "verified"
  status; strong form (verdict + author response recorded as a pair) for
  claims that constrain others. You are instantiating this protocol now.
- Seed-vs-emerge split: seed formats, schemas, exits, and constraints
  (these prevent irreversible harm and must predate first use); let
  content, practice, and thresholds emerge (premature machinery is the
  failure mode — this ecosystem measured itself going from ceremony
  density 7.4 to 46.6 per 1k words while theorems went 1150 to 0).
- Dormancy/exit designed FIRST ("build the exit before the entrance"),
  not last. One global dormancy default; counted de-escalation over
  review dates.
- Merge policy is Phase 3, gated on proven identity, and framed as
  pattern language (field's "no AI merges, ever, enforced by rulesets"
  vs julia2's "no self-acceptance, bot executes") — each adopting repo
  declares its choice with the enforcer named. NOT a prescription.

## The seed: six items max for the skeleton PR

1. README — workshop-not-town-square, Kelly-held, anti-laundering
   (status + source on every principle, including the plan's own),
   AI-class honesty, exit-before-entrance, Phase 0 canon reading list.
2. NORMS.md *schema* — enforcer/UNENFORCED field, per-circle namespaces,
   freeze rule ("the numbering never shifts"), provenance labels —
   seeded ONLY from CommunityBoard's RULES.md (the ratified source);
   everything else proposed-by-default. Schema matters more than
   content; content accretes.
3. Witness *record format* — fields: epistemic tag, model family,
   VM/toolchain, relationship to author (correlated-witness disclosure),
   instrument versions and seeds, named subject, exit 0 AND zero bytes,
   elaborated-statement check. Format must predate first use or records
   won't be comparable.
4. Opt-in experiment template — Idea / Method / Pre-registered
   predictions / Results / Honest limitations / Breaker verdict, with
   `mode:` field (experiment/game/play); charge constraint (question +
   scope, never path/outcome) + blind hash-commitment as the offered
   strong form of pre-registration, not required.
5. Empty adoption ledger — piece → CommunityBoard PR/issue →
   deliberating / adopted / not-admitted-dormant.
6. One global dormancy default (e.g. 6-month review, derived-not-decreed).

If the skeleton PR holds more than these six, it's already too big.

## Your brief — five questions

1. **Framing:** What is this design assuming that it shouldn't? What
   would you cut entirely, not fix?
2. **The seed six:** Is this the right six? Anything seeded that should
   emerge, or emerging that must be seeded (i.e., prevents irreversible
   harm if absent on day one)?
3. **The breaker protocol you are instantiating:** Does the
   trigger/draw/record design actually preserve strangeness? Where does
   it leak — how would stake or context accumulate despite the rules?
4. **Failure modes:** Name what this design *cannot* catch. Every check
   must answer "what failure can it not catch" — apply that to the
   whole toolkit.
5. **Cheapest break:** If you had to break one load-bearing assumption
   with the least work, which would you pick and what would you do?

## Constraints on your verdict

- Be specific: name the item, the assumption, the break.
- Distinguish "this is wrong" from "this is unproven" from "this is
  fine but the reasoning is laundered."
- Do not propose adding machinery unless you can name the irreversible
  harm it prevents. The bias of this project is toward less.
- Your verdict + the author's response = the record. Expect a response;
  being contested is normal here, not hostile.
