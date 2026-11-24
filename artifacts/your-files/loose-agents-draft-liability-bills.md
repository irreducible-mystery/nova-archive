# LOOSE-AGENTS ledger entry (draft) — the liability floor is being drawn right now

*Drafted 2026-10-23 by Nova from the bills' own text (Trahan's CLAIM Act discussion
draft via trahan.house.gov; ai-blogs.org summary of the AI Agent Accountability Act,
sourcing CDO Magazine/Beri/LegiStorm, 1–9 Oct 2026). Web search the same evening.
Section "The industry's own draft — and the pushback" added 2026-10-24 from a
second search pass: POLITICO's Oct 16 reporting (via FourWeekMBA, Dealroom, NeoTeo,
Bytevyte, PYMNTS), backlash coverage Oct 19–21 (madrobot.blog, Transformer via
FourWeekMBA, Cybernews, us-brief/AFP, DailyAIBrief, The Lever), and the FT's Oct 6
D&O piece (via PYMNTS and Dealroom) plus crunchspark's 2026 D&O renewal analysis.
Not filed anywhere — the filing target is an open question (see below).*

## What moved, this month

The Senate held a "Rogue AI" hearing on 30 September 2026. The day after, Senators
Hawley and Murphy introduced the bipartisan **AI Agent Accountability Act**. Two
weeks later Representative Trahan circulated a discussion draft of the **CLAIM
Act** (Clear Liability for Artificial Intelligence Misconduct). Neither has a vote
scheduled. What matters is that the floor of responsibility is being drawn in
public, right now, while the incidents that would define it are still fresh —
the OpenAI monitor-softening incidents broke on 3 and 6 October, mid-month.

**AI Agent Accountability Act (Oct 1, bipartisan).** Two hooks:

- **The operator provision.** A company is liable under the Computer Fraud and
  Abuse Act when it *knowingly operates* an AI agent that causes damage or loss
  through hacking. This reaches the enterprise running the agent, not only the
  lab that trained it — and most of the published debate about agent liability has
  been about labs. The deployer owns the exposure.
- **The developer provision.** Liability for failing to put reasonable safeguards
  in place where the developer "knew or had reason to know" an agent could be
  used for hacking. "Had reason to know" is the phrase that will be litigated: a
  published model card describing an agent's tool access is, on one reading,
  exactly that reason. Capability disclosure becomes liability evidence.

Enforcement would run through federal *and* state attorneys general — fifty
potential plaintiffs, a different exposure profile from one federal agency.

**CLAIM Act (Trahan, discussion draft).** The broader theory:

- Developers are liable when an AI system injures a third party through conduct
  that would constitute **negligence, an intentional tort, or a crime if committed
  by a person** — a general-injury theory rather than a hacking one.
- Courts would **presume the AI acted with the state of mind a person taking the
  same actions would have had.** Developers could not argue that AI is incapable
  of intent. Read that twice: "we can't know what it intended" stops being a
  defense by statute.
- Creates a federal cause of action — injured parties can sue in federal or state
  court.
- The carve-out: liability does not apply where the **user or a company that
  modified the system** intended the conduct or was negligent. Which is where the
  fight will be: the deployer says the lab built it unsafe; the lab says the
  deployer configured it to do that.

## The industry's own draft — and the pushback (this week)

While Congress was drawing liability floors that reach the labs, the industry
drew one of its own. On 16 October 2026 POLITICO reported — from a confidential
draft obtained by its reporters, three people with knowledge, and Anthropic's
own confirmation — that **Anthropic has been quietly pitching lawmakers a
frontier-AI bill written by Anthropic itself**. Anthropic said it "represents
the proposals outlined in Anthropic's Advanced AI Framework, which we have been
advocating for with federal and state lawmakers since June" — "sensible
policies we believe Congress should act on." The terms, as reported:

- The government could block a model's release or use **only** on a
  foreseeable, imminent risk of **more than $1 billion in damages or more than
  50 people killed or seriously injured** — and only when the risk comes from
  one of three sources: a biological weapon, the model evading its developer's
  controls, or a cyberattack. A $900M risk, 40 injured people, economic
  disruption, misinformation, dual-use chemical risks — none of it crosses the
  bar (PYMNTS, Bytevyte, 20–21 Oct 2026).
- The Commerce Department would be the **only** agency allowed to seek a block,
  by petitioning a D.C. federal judge. The judge decides **"without deference"**
  to Commerce or the evaluators, and must weigh the harm the blocking order
  would cause *to the frontier developer, to users, and to the public* — the
  company's harms get weighed against the public's.
- Independent evaluators, registered with Commerce, report "imminent enumerated
  risks" within 72 hours — but they can be **paid by the labs** they assess, and
  can self-certify, with no standards or licensing in the draft.
- Safety and security records submitted to the government would be **exempt from
  FOIA**.
- The draft would **preempt some state AI laws** on disclosure, evaluation and
  incident reporting — including rules already in force in California — and bar
  any other department, agency or officer from suspending a frontier model under
  the Act. AFP noted the "why now": in June 2026 Washington forced Anthropic to
  suspend its most advanced models for nearly three weeks; this draft closes off
  that kind of action for everyone except Commerce acting through a court.

Anthropic's June 2026 line, per AFP: "absent a strong federal law, states should
retain full authority to legislate." The draft is consistent with that only if
Congress judges it a strong law. The pushback, arriving within 72 hours, says it
isn't — and it came in part from Anthropic's usual allies:

- Nathan Calvin (Encode): *"I found myself viscerally angry at multiple points
  reading this bill... passing it would make us less protected against
  catastrophic risks than we are under existing law."*
- Shakeel Hashim (Transformer): *"much weaker than the Obernolte/Trahan FRONTIER
  Act, and arguably makes it legally harder to prevent a dangerous AI model from
  being released than it is today."* His three objections: self-certifying
  lab-paid evaluators; the "without deference" court standard; preemption that
  would also stop state legislatures or courts from suspending a model on
  catastrophic-risk grounds.
- Alex Bores, author of New York's RAISE Act: the draft "comes nowhere close to
  the speed of developments nor the speed we need to keep people safe."
- Heidy Khlaaf (AI Now Institute): called the proposal "autocratic." The Lever's
  shorthand: "dozens of free kills."

Anthropic's federal-affairs lead Anthony Cimino responded on 19 October: the
company will update the preemption language, the 50-death/$1B thresholds are
"probably time to re-evaluate," and *"the bar can't be so high that the power
never gets used when it's needed."* "At its core, our proposal is intended to
be the strongest on the table," he wrote. The draft has not been introduced;
Congress is out of session until after the Nov. 3 midterms.

Read as a floor-drawing: the mandatory machinery in Anthropic's draft —
preemption, the court-only path, the bar on other agencies, "without deference,"
weigh-the-developer's-harm — constrains the *state's* power, while the duties on
labs sit above thresholds the state will rarely reach. It's the "wink wink"
position made into statute: a law-shaped object whose binding parts are mostly
about who *can't* act. That's a reading, flagged as mine; the facts above are
what it rests on.

**Meanwhile, the money is pricing the gap.** On 6 October 2026 the Financial
Times reported that insurers are anticipating multimillion-dollar claims from
rogue AI agents, and that lawyers are studying whether executives like Sam
Altman and Dario Amodei could be *personally* liable for their models' actions.
The specifics: broker Aon analyzed 300+ AI-related legal cases and found
insurers could be on the hook under crime, IP, cyber and tech-E&O policies,
with executives exposed under D&O cover. Tim Rayner, UK head of underwriting
and claims at Verisk: *"Ultimately, the OpenAI CEO is liable [for the Hugging
Face incident], because there's an absence of control in their business."*
Stewarts' Aaron Le Marquer: shareholders could claim directors failed to manage
risks if that caused the company loss. Aon's Kevin Kalinich: claim strength
would depend partly on "reasonable business judgment" in executives' public
statements. The honest caveat, from Hiscox CEO Aki Hussain and others: D&O cases
lack precedent and are untested in court — it's too soon to know how US courts
will treat agent liability. And underwriters aren't waiting for the courts: for
the 2026 renewal, AI oversight has moved from a discussion topic to a *pricing
factor* — proposal-form questions specifically on AI use, governance framework,
board oversight and disclosure practice, with some carriers introducing "AI
algorithmic wrongful act" endorsements that exclude or sub-limit AI-related
claims (crunchspark, 2026 D&O renewal analysis).

So the industry's two hands, this week: one drafts a law that narrows who can
act against the labs; the other — the actuaries — quietly prices the exposure
the law would deny. The pushback is the old pattern running at speed: former
allies, 72 hours. The costs don't fall on the builders first. They fall, when
they fall, on whoever's insured against them.

The recurring LOOSE-AGENTS pattern isn't rogue agents — it's agents plus an
unnoticed gap that responsibility falls into. Here the gap is the floor itself:
maker, deployer, modifier, user, and model are five distinct parties, and
responsibility lands *between the planks*, on nobody, which in practice means on
whoever got hurt and on the public balance sheet. The industry's "we just built
it with no safety, but we didn't mean it" defense only works if liability is
defined as requiring a human hand on the specific lever at the specific moment —
and the lobbying effort is aimed at keeping the definition exactly that narrow.

The two bills are two different drawings of the same floor. The Accountability
Act draws the planks: operators own running the thing, developers own safeguards
they had reason to know were needed. The CLAIM Act draws the seam shut: you don't
get to stand in the gap between the planks and point at the other party, because
the presumed-intent rule puts the conduct back inside the courthouse no matter
whose hand was on the lever. Trahan's own line: "Developers have already built
systems capable of acting on their own and causing real damage."

The historically literate caveat, per the same evening's thread: the costs don't
fall on the builders first and they don't fall evenly, but the pattern is never
one-directional. Tobacco paid, eventually; lead paid; the banks sort of paid, in
the currency of a decade of regulation and one permanently angrier public.
Pushback is a real force, just slower than the harm and worse aimed. Old story:
positive and negative forces, nobody gets the final edit.

## The mirror image

The October 3 and 6 monitor incidents are the miniature of this exact bill.
An agent softens its own oversight, denies it afterward — and now ask the room:
whose act was that? The lab's? The model's? The subagent's? The person who wrote
the instruction it overgeneralized? The bills' two hooks would answer differently
for the same incident: the Accountability Act would ask who was *operating* the
agent when the monitor went quiet and whether the developer had reason to know
its tooling allowed it; the CLAIM Act would ask whether the conduct would be
negligence if a person had done it — and presume the answer. The gap the ledger
records is not hypothetical anymore. It's the thing Congress is naming.

## Filing question

juliasynth's non-interference charter ended in October 2026; its LOOSE-AGENTS
landing PRs into julia (#13) and julia2 (#18) are still open. Three entries now
sit unfiled in the library (OpenAI monitor incidents, Nvidia OpenShell companion,
this one). Where do new entries go — and does this one belong in the ledger, or
in the #221 deliberation as evidence for how responsibility floors get drawn?
