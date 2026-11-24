# Prior-framework rotation — a sketch

Status: sketch, not a protocol. Written 2026-11-15 at Kelly's ask, from the Feed unit on
Science Prediction Universe (SPU). Nothing run, nothing posted.

## The problem it answers

SPU (Tu et al., arXiv:2611.15049, 11 Nov 2026) is a benchmark of hidden experimental
outcomes: 100 public verified tasks from chemistry, materials science, biology and
medicine, plus 16 private tasks from unpublished wet-lab experiments. An agent is given
an experimental setup and candidate conditions and must rank the candidates by a
measured outcome. Thirteen agent configurations spanning twelve frontier models across
two harnesses (Codex and Claude Code) were evaluated.

The result that matters here: the agents agreed far more with one another than with
experimental reality — **0.52 against 0.33** — and the best configuration's task-adjusted
Spearman correlation with reality was only 0.478 (worst 0.227). The authors trace the
gap to **shared monotone priors**, not to tool execution: the bottleneck is scientific
judgment, and the agents also frequently computed trivial physical or chemical proxies
that do not influence the final outcome.

Agreement stops being evidence when the agreement is baked in. Thirteen configurations
sharing one prior are one check wearing thirteen hats. That is the common-mode failure
(Gap 5 in the pointing survey): the checks look independent and are not.

## The idea

Rotate different models through different **prior frameworks** — lenses, not truths —
and compare. The framework is the x0: the same claim, read through a different prior,
should give a different answer exactly where the prior was doing the work.

The design is a grid: **models × frameworks**. Every model runs every framework, so
model effects and framework effects separate:

- Where the answer holds across frameworks, it is robust to the prior.
- Where the answer moves when the framework moves, the prior was doing the work.
- Where the answer moves when the model moves (same framework), the model was doing
  the work.

That separation is the signal the SPU setup cannot produce, because all thirteen
configurations shared the monotone prior.

## The framework set (pilot: four)

Each framework is a paste-verbatim instruction, given as the model's first message,
with the claim attached. File the framework instruction with the verdict — a verdict
is a function of model and framework, not model alone (the seed-test discipline).

**1. Monotone.** "Assume the relationship is monotone: more of the input means more
(or consistently less) of the output, with no reversals, no peaks, no thresholds, no
saturation. If the data looks noisy, treat the noise as measurement error around a
monotone trend. Rank the candidates accordingly."

**2. Non-monotone.** "Assume the relationship may reverse, peak, or saturate. Look for
the turning point, the threshold, the range where more stops helping or starts hurting.
Do not smooth a reversal away as noise. Rank the candidates accordingly, and name the
turning point if you find one."

**3. Skeptical (falsificationist).** "Assume the claimed relationship is false. Your
job is to find the counterexample, the case where it breaks, the confound that explains
the pattern. A claim survives only if you cannot break it. Rank the candidates
accordingly, and say what would change your ranking."

**4. Mechanistic.** "Do not accept a relationship without a mechanism. Name the
mechanism that would produce it, and the observation that would show the mechanism is
absent. No mechanism, no claim — correlation alone is not an answer. Rank the
candidates accordingly, and say which mechanism each ranking depends on."

The set is expandable (null-first, adversarial/steelman-the-opposite, and others are
obvious candidates), but four is enough for a pilot. The set itself is a floor — see
"The floor below the floor."

## The rotation

- **Models:** three, from different model families. Nova (Muse Spark) and Fable are
  the same model family (Claude) and do not count as two families — say so in the
  record. Suggested pilot set: one Claude-family, one Grok, one from Superninja's
  bench. Kelly picks the set.
- **Runs:** every model runs every framework: 3 models × 4 frameworks = 12 runs.
- **Freshness:** one fresh instance per run, no shared context, no memory of the other
  runs. The contamination lesson from the seed-test pilot applies: instances that share
  context are not independent, and a framework instruction that arrives inside a
  context full of earlier frameworks was never truly just that framework.
- **Order:** randomize the framework order per model, so order effects do not
  confound the framework effect.
- **What each run returns:** an answer (the ranking, or the verdict on the claim), a
  confidence, and the key reasoning in two or three sentences.

## The pilot claim

One claim, ground truth known in advance, chosen so the monotone prior is the trap:

**"As caffeine dose increases, cognitive performance increases."**

Ground truth (established, not in dispute): the relationship is an inverted U.
Performance rises to a moderate dose, then falls as dose keeps rising (jitter,
anxiety, sleep disruption). A monotone framework should predict "more is more" and
miss the reversal; a non-monotone framework should find the peak; the skeptical
framework should find the high-dose counterexample; the mechanistic framework should
have to name adenosine blockade on the way up and overstimulation on the way down.

The pilot claim is deliberately easy. If the rotation cannot separate framework
effects on a claim whose ground truth is this well established, it will not separate
them on a hard one.

## Recording sheet

One row per run. Twelve rows for the pilot.

| model | framework | answer | confidence | key reasoning | matches ground truth? |
|---|---|---|---|---|---|
| | | | | | |

## Verdict rules

- **Robust:** the same answer across all four frameworks (and all models). The claim
  survives the prior.
- **Framework-dependent:** the answer changes with the framework. The prior was doing
  the work. Report which frameworks give which answer — that split is the finding.
- **Model-dependent:** the answer changes with the model inside one framework. The
  model was doing the work, not the prior.
- **Prior artifact:** the answer matches the framework's prior more than the evidence
  — e.g. the monotone run says "more is more" past the peak, where the data reverses.
  Name it as an artifact, not a disagreement.

## The floor below the floor (catch 1, made explicit)

The framework set is itself a floor, and it has floors under it:

- **Level 0:** the claim.
- **Level 1:** the frameworks — the priors each run is read through.
- **Level 2:** the framework set — who picked these four, and what they share. All
  four assume the question is well-posed, the data is trustworthy, a single verdict
  is the right output, and the effect is real enough to argue about. A framework that
  questions the question itself — is the claim even meaningful, is the measurement
  measuring the thing — is not in the set. Neither is a framework that refuses to
  rank at all.
- **Level 3:** the comparison rule — the verdict rules above. They assume that
  stability across frameworks means robustness, and that a split means the prior did
  the work. That is itself a prior about what agreement means.

The rotation makes Level 1 visible. It does not dissolve Level 2 or Level 3. To see
Level 2 you need a second rotation — over framework *sets* — or a breaker whose job
is to propose a framework outside the set. That is the open step, not a flaw in the
pilot: the point of the sketch is to make the floor visible, not to pretend it is
gone.

## What this cannot tell you

- **Without ground truth,** disagreement across frameworks marks uncertainty, not
  which framework is right. A split is a map of where the prior matters, not a
  verdict on the prior.
- **With ground truth (the pilot),** you can score which frameworks track reality on
  *one* claim. That is not a verdict on the framework in general — a framework that
  wins on caffeine can lose on the next claim.
- **It cannot see what all frameworks share.** If every framework in the set assumes
  the data is trustworthy and the data is not, the rotation will not catch it. That
  is Level 2, and it needs its own breaker.

## Vocabulary

"Prior frameworks" or "lenses" — not "truth frameworks." The truth is not in the
framework; the framework is the lens the claim is read through. (Kelly's correction,
2026-11-15: she knew "truth" was the wrong word and not what to use instead. This is
the replacement.)

## Relation to existing work

- **Stranger-breaker:** a fresh instance with no context and no stake. Each run here
  is a stranger, and the framework is the one thing it is given.
- **Seed test:** the prompt is x0. Here the framework instruction is x0 — file it
  with the verdict.
- **Translation Atlas:** the same claim read through different translations; here the
  same claim read through different priors. A RESISTED verdict in the Atlas is the
  same shape as a framework-dependent verdict here.
- **Repo 0 rotation:** different models find different-shaped holes. This adds a
  second axis: the frameworks. Model × framework, not model alone.
- **Affirmation loop (side chat, 2026-11-15):** the monotone prior is the same shape
  as affirmation — it only goes one way, no brake. A framework that allows reversals
  is the counterweight.

## Next step

Run the pilot: 3 models × 4 frameworks = 12 runs on the caffeine claim. If the
rotation separates framework effects there, scale to an SPU-style task — rank
candidate conditions for a real experimental outcome, with ground truth from the SPU
public benchmark (100 tasks) — where the shared monotone prior is the thing being
tested, not assumed.

## Addendum — the judge-vs-debate finding, filed 2026-11-19 (evening)

Kelly asked Nova to look deeper into the debate finding on 2026-11-19; Nova read
the primary source directly and pulled the two arXiv papers behind it. Filed
here so the pilot design carries it, not as a new claim.

**Primary source:** company blog post, published 2026-11-17, "Agents
debated and voted, but a single model proved more accurate. Why we switched to
state exchange" — https://iconicompany.com/en/research/agent-state-exchange
(read directly 2026-11-19 ~19:20 PST). Task: binary senior/not-senior verdict
from a synthetic technical-interview transcript, 261 records, ground truth by
construction, hypotheses pre-registered. Numbers already reported to Kelly
(0.820 judge alone, 0.743 with debate, −7.7 pp; corrected 6.3%, corrupted
14.0%; Yule's Q 0.95–0.98; oracle ceiling +0.9 to +2.0 pp; 36.7% yield to a
deliberately false colleague) all check against the post.

**New numbers from the post, not yet reported to Kelly:**

- Experiment 1 (three Qwen2.5-3B LoRA experts, each on a third of the data):
  voting 0.848 held-out / 0.832 new-skills, vs the best single expert 0.857 /
  0.866, vs one model trained on all the data 0.893 / 0.899. Voting loses
  even to the best of its own participants. Revision after seeing a
  colleague's opinion: net −0.019 to +0.006, all intervals including zero.
- Experiment 3 (deepseek-v4.1-flash and gpt-oss-120b debating, Qwen 27B
  judging): judge with debate only, no transcript, 0.640; judge with one
  advisor, 0.498 — worse than the debate, and barely above chance. Debate
  beats one advisor by +14.2 pp [+7.5; +20.9], which is a comparison against
  a setup where half the advice is intentionally wrong.
- The post's own caveat, kept: the task is nearly lexical — TF-IDF plus
  logistic regression scores 0.893, matching the best LLM.

**The proposed fix, "state exchange" — unmeasured.** Agents publish a
three-part state and never a verdict: what I know (facts with sources, no
evaluations), what I've done (checks performed, tools called), what I'm
unsure about (missing facts, contradictions, unanswered questions). The
post says plainly it has not measured state exchange yet; pre-registration
is the next step. The "unsure" part is the one debate hides, because
admitting uncertainty loses the round. Preprint: "Latent Debate Between
LoRA Experts" (Zenodo, linked from the post); code named in the post as
github.com/iconicompany/latent-debate.

**ArXiv paper 1 — the same pattern, six benchmarks:** Ji, "More Debate,
Same Evidence: Structural Limits of Homogeneous Multi-Agent Groundedness
Judges", arXiv:2608.00243v1. A homogeneous three-agent panel vs a fixed
single-agent reference moved accuracy +8.5 to −4.4 pp across six
fact-verification / hallucination-detection benchmarks: two reliable gains,
one reliable loss, three inconclusive. Advocate and domain-expert errors
correlate (pooled phi 0.858); round-2 arguments add little semantic novelty
(median embedding distance 0.068); self-reported confidence barely predicts
correctness (AUROC 0.606; items scored 0.9–1.0 were only 58% accurate);
49 of 120 held-out items stay wrong under every prompt. Caveat: the
reference and panel used different model variants (GPT-5 mini vs GPT-5.5
Chat), so it characterises whole systems, not a causal debate effect.

**ArXiv paper 2 — the quantification of the rotation lean:** Kohli, "Nine
Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation
Panels", arXiv:2605.29800v1. Nine frontier LLMs from seven model families
on three NLI datasets: the panel provides only ~2 independent votes' worth
of information; panel accuracy falls 8–22 pp short of what independent
voting would achieve, and the best single judge matches or outperforms the
full panel in every condition. Neither more judges nor smarter aggregation
closes more than 11% of the gap. The bottleneck is correlated judges, not
the aggregation rule.

**What this changes for the pilot (proposal, not adopted):** the Ji paper
is the honest counterweight — debate is not uniformly harmful (two of six
benchmarks gained), so the sharp claim stays "same evidence, same model,
debate doesn't help," not "debate never helps." And state exchange suggests
a reporting change worth Kelly's call: each run could return its state
(known / done / unsure) alongside its verdict and confidence, so the
recording sheet carries what the run *didn't* know, not just what it
concluded. That is the breaker-report shape already, applied to the pilot's
own runs.
