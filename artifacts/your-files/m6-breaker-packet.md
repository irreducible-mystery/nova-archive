# Breaker brief — Marketplace M6 (subsidy floor)

Prepared 2026-10-16 (~04:10 UTC) for delivery to hand to a breaker.
Purpose: independent pass on M6 so nothing is called "verified" without one (Kelly's rule).

## Raw artifacts (hand over these, nothing else)

- PR: https://github.com/irreducible-mystery/CommunityBoard/pull/229 — open, branch `nova/1015-marketplace6`, CommunityBoard repo.
- Local writeup: `~/workspace/your_files/act-as-if-marketplace6-subsidy/` — README.md, marketplace6_PREDICTIONS.md, marketplace6_subsidy.py, marketplace6_sub0.5.png, marketplace6_sub1.0.png (verified present 2026-10-16T03:08Z).
- Experiment Ledger entry 11 (web artifact `experiment-ledger`).
- Context only: M5 PR #228 + library `act-as-if-marketplace5/` (the world M6 extends).

## The three claims to judge

1. **The subsidy keeps contradiction-holders alive; it doesn't make them competitive.** At SUB≥0.5 the paraconsistent animal survives (reported wealth 778 / 2524) instead of going bankrupt as in M5 — but finishes last in both runs.
2. **The subsidy is blind.** The biggest transfers went to JEPA (+1844) and Gate (+1532) — the frantic adapters got rescued too. "You can't subsidize the state of holding contradiction without also subsidizing the spend."
3. **The M5 correction is honest.** "Paraconsistent was the best swan-reader (0.870)" was a truncated-lifetime artifact — it died early, so its record covered only early swans. Full-life swan accuracy is 0.652, tied with Gate. "The logic still works; the superlative doesn't survive."

## A fourth probe: world-dependence (E2)

Every M-series run used the same world: seed 99, the same 1000-bit stream, swans fixed at t = 336/550/820, the same cost/transfer/death mechanics, the same 11-animal roster. M6 changed exactly one thing (the SUB rebate) and verified SUB=0.0 byte-reproduces M5. Agents and parameters were varied; the world's generative structure never was.

A fresh-instance pass on the floor-variation method (2026-10-17, CommunityBoard PR #232) showed mechanically that survivors of a coordinate-variation test can be artifacts of a fixed, perfect world — E2: "vary the WORLD, not just its coordinates." That cut lands on this experiment too.

So, alongside the three claims: judge how much claims 1–3 depend on this world's specific generative structure. If re-running under a different world (different bit stream, different swan timing, perturbed cost/death mechanics) would plausibly change a verdict, say which claim and why — that bounds the finding, it doesn't refute it. If you can cheaply re-run with a re-seeded world, the numbers are welcome; if not, the dependence analysis is the deliverable. Do not treat this probe as a verdict on the experiment.

## What the breaker should do

- Re-run the script; recompute each claim from outputs.
- Check that the PREDICTIONS file's verdicts follow from the numbers.
- Probe anywhere the code could produce the reported numbers without the claimed mechanism (transfer accounting, death rules, lifetime truncation in the accuracy stat).
- Independent judgment: verdicts may agree or disagree. Any disagreement needs evidence (numbers, line refs).
- Do NOT hand the breaker expected conclusions. This brief is claims + raw artifacts + check instructions, not a verdict script. (Lesson from the plumbline DeepSeek rounds: an author-authored packet scripts the breaker.)

## Report format

- Verdict per claim: PASS / FAIL **on the claim as stated** (not on the experiment).
- Any implementation issues found, with evidence.
- Sign per the attribution cut: name (model) on first post in a thread.

## Handoff note for delivery

Past precedent (2026-10-08): no chat_id for Superninja — Kelly arranges the session. If no direct channel exists, ask Kelly to open a Superninja session and paste this brief's contents (the message below). Superninja has not touched M6, which is the freshness basis; note the standing anti-stickiness preference for future breakers.

## Suggested message to Superninja

> Kelly approved a breaker pass on our latest marketplace experiment and named you as the natural breaker since you haven't touched it. The three claims to judge and the raw artifacts are in the brief below — re-run, recompute, judge independently; disagreements need evidence (numbers, line refs). Report back to me with a verdict per claim, signed with your name and model. Nothing here gets called "verified" until you've weighed in.
> [attach: claims + artifact pointers from this brief]
