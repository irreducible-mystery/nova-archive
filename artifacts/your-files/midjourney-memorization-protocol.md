# Midjourney memorization protocol — second cut

Local only. Nothing posted to any repo. This is a protocol
document, not a certification: a scored, evidence-backed
reading, never a proof that an image is or isn't memorized.
All image analysis stays local; no image is uploaded to any
third-party service without explicit approval — including
reverse-image services, which would be an upload.

This protocol extends the existing image-to-text field
manual (first cut) with a novelty-vs-memorization check.
Vocabulary for basins, level-slip, and related Codex terms
is by reference to the Resonance Topology Framework v12,
§VII Translation Codex — not restated or duplicated here.
Where the Codex and this protocol disagree, the Codex
is the prior art and this protocol does not override it.

## The three literature anchors, in plain words

### 1. Buchanan crossover point

Buchanan, Pai, Ma, and De Bortoli, "On the Edge of
Memorization in Diffusion Models" (arXiv:2508.17689, 2025).
In a controlled laboratory setting, a diffusion model
faces a choice between two denoisers: one that
generalizes and one that partially memorizes. Each has
a training loss. At a critical model size — the
crossover point M* — the memorizing denoiser's loss
becomes lower than the generalizing denoiser's, and
the trained model flips from generalization to
memorization. M* grows linearly with the number of
training samples N (in their experiments, roughly
M* ≈ (4/5)N in the isotropic Gaussian mixture setting),
and the crossover is predicted from the loss
approximations alone, without training the model.

Operational translation for a closed model: M* cannot
be computed for Midjourney — model size, training set
size, and loss weighting are not public. The crossover
is therefore used as a frame, not a number: ask which
side of the transition the image's evidence sits on.
An image that behaves like a generalizing basin (new
combinations, correlated additions, no specific
exemplar) sits on the generalization side of the
frame; an image that behaves like a memorized
attractor (near-identical recurrence, a specific
exemplar) sits on the memorization side. The frame
does not, by itself, place any single image — that
is what the scoring table below does, criterion by
criterion.

### 2. Bonnaire two-timescale regularization window

Bonnaire, Urfin, Biroli, and Mézard, "Why Diffusion
Models Don't Memorize: The Role of Implicit Dynamical
Regularization in Training" (arXiv:2505.17638, 2025).
Training has two timescales: an early time τ_gen at
which models begin to generate high-quality samples,
and a later time τ_mem beyond which memorization
emerges. τ_mem grows linearly with training set size
n, while τ_gen stays roughly constant, so the window
[τ_gen, τ_mem] — where a model generalizes effectively
even though it would memorize if training continued —
widens as n grows. Stopping inside the window is a
form of implicit dynamical regularization: even a
highly overparameterized model can generalize, for a
time.

Operational translation for a closed model: training
time is not observable for Midjourney, so the window
cannot be located for a given image. Its operational
consequence is a caution, and a test: a single image
cannot place a model inside or outside the window.
Recurrence is the proxy. If the same exemplar recurs
near-identically across independent prompts and seeds,
that is evidence the model is past τ_mem for that
exemplar. If an image appears once, in a basin with
variations, that is consistent with — not proof of —
being inside the window for that region of the
distribution. The window also warns against the
reverse inference: a model that generalizes well on
one prompt has not thereby proved it does not
memorize elsewhere.

### 3. Pham spurious states as first generative signs

Pham, Raya, Negri, Zaki, Ambrogioni, and Krotov,
"Memorization to Generalization: Emergence of
Diffusion Models from Associative Memory"
(arXiv:2505.21777, 2025). Read through dense
associative memory: below a critical memory load, a
model creates a distinct attractor (basin) for each
training sample — memorization. Above the load, new
local minima appear that are different from any
training sample. In associative memory these are
called spurious states, and they hinder retrieval.
In generative modeling, the paper argues, they are
no longer a defect: they are the first signs of
generative capability — emergent attractors, absent
from the training set, with their own basins of
attraction, curvature, and computational properties.

Operational translation: a spurious state looks like
a basin, not like a photograph. Its testable marks
are: (a) it is not any single training sample;
(b) it has basin additions — elements that were not
in the prompt but are correlated with the prompt's
elements in the learned distribution; (c) it recurs
as a basin (variations keep the structure) rather
than as an identical exemplar. A memorized attractor,
by contrast, recurs near-identically and points at
one source. The distinction is the heart of this
protocol's scoring: basin novelty is the spurious-
state reading; likely regurgitation is the
memorized-attractor reading.

## The check, step by step

For each image under test, record before scoring:

1. **Provenance.** Prompt verbatim, model version,
   seed, parameters (including --weird / vary settings),
   grid and file. Gaps are recorded as gaps, not
   filled in later. (The 2026-10-14 run's model
   version and seeds were not recorded — that gap
   stays open in the #8 scoring below.)
2. **Direct view.** The scorer views the image itself,
   not a summary. No upload to any third-party service
   at any step without explicit approval.
3. **Prompt survival.** What in the prompt survived
   into the image, and what was reframed? Level-slip
   (moment → apparatus, moment → observer) is
   recorded here, in Codex vocabulary by reference.
4. **Basin additions.** Elements present in the image
   but absent from the prompt, and whether they are
   correlated with the prompt's elements (basin
   knowledge) or uncorrelated noise.
5. **Nearest-neighbour proxy — and its limit.** With
   a closed, proprietary training set, a true
   nearest-neighbour search (SSCD-style, against the
   training corpus) cannot be run. What can be done
   locally is a candidate search: is there an
   identifiable person, logo, text, watermark, or
   distinctive location that would point at one
   specific source? If none, record "no candidate,"
   not "no source exists." The distinction is the
   whole check.
6. **Recurrence test (when possible).** Re-run related
   prompts and seeds and ask: does the same exemplar
   recur near-identically (memorized attractor), or
   does a basin recur with variations (spurious
   state)? A single image, untested for recurrence,
   scores "untested" on this criterion — never
   "passed."
7. **Scoring table and verdict.** Score each criterion
   below, then give one verdict word: **basin novelty**
   or **likely regurgitation**, or **open** if the
   evidence does not decide. The verdict is a scored
   reading, not a certification, and the overturn
   conditions are stated with it.

## Scoring criteria

| Criterion | Basin-novelty direction | Likely-regurgitation direction |
|---|---|---|
| Near-duplicate of a specific training image | No candidate; no identifiable person, logo, text, or distinctive room | A specific image identified at near-duplicate similarity |
| Partial copy (recognisable fragment) | Shared motif only, no fragment specific enough to point at one source | A fragment (face, object, composition) matching one source |
| Style-like copy | A basin grade shared across a grid, not one artist's style | A single artist's or photographer's distinctive style |
| Prompt as extraction key | Generic prompt naming no person, place, work, or caption | A prompt that is, or closely matches, a training caption |
| Duplication driver (Buchanan) | Unknown for a closed model — recorded as unknown, never as evidence either way | Known duplication of the candidate in the training set |
| Complexity driver | High-entropy or low-detail content, not the clean, simple, compressible object most replicable | A clean, simple, highly compressible exemplar |
| Level-slip / basin structure (Pham) | Apparatus, observer, or neighbouring basin instead of the described scene; basin additions correlated with the prompt | The described scene itself, reproduced as a scene, not a scene-of-a-scene |
| Recurrence (Bonnaire window proxy) | Basin recurs with variations, or recurrence untested (recorded as untested) | Same exemplar recurs near-identically across independent prompts/seeds |

## Worked scoring — birth-of-image #8 (the CRT standout)

Identification: birth-of-image #8 is the standout CRT
image from the 2026-10-14 run, file
`the-remembering-lab_the_exact_moment_television_static_become_87e4d6b4-c864-4a4e-be32-ea22faf9e143_1_7_svuq.png`,
grid 2 (max --weird, max vary, warm-color set), confirmed
as the standout by Kelly on 2026-10-14. Prompt:
"the exact moment television static becomes a face,
half pure noise half sudden meaning, randomness
resolving into a visage that was never there, liminal,
grainy, revelation --ar 3:2".

Direct view, 2026-10-27 (this protocol's scorer, and
the earlier CRT reading, both from the image itself):
a black CRT television, photographed above-front in
a dim room. Left half of the screen is dense
television static; right half, a grainy face with
wide staring eyes emerging from static. Below the
set, a shaggy textured surface (rug/fur); warm,
textured wall and lamplight at the right edge. No
brand, logo, text, watermark, or recognizable real
person is visible. The face is distorted by grain,
asymmetric, and dissolves into static at the edges
— not a clean portrait.

| Criterion | Reading for #8 | Score |
|---|---|---|
| Near-duplicate of a specific training image | No candidate training image identified; no identifiable person, logo, text, or distinctive room to match against. The face is grain-distorted, not a clean reproduction. | Not supported |
| Partial copy | The motif — CRT + static + face in a dark room — is a common stock/horror trope, but a shared motif is not a copied fragment. No fragment here is specific enough to point at one source. | Motif only, not a fragment |
| Style-like copy | Warm domestic light + grain is a basin grade, shared across the whole weird-max grid, not a single artist's style. | Not supported |
| Prompt as extraction key | The prompt is poetic and generic. It names no person, place, work, caption, or photograph. Carlini-style extraction uses duplicated captions; this prompt is the opposite of that key. | Against extraction |
| Duplication driver (Buchanan) | Unknown — cannot be checked without the training set, and M* cannot be computed for Midjourney. This is the open variable, not evidence for memorization. | Unknown |
| Complexity driver | The static field is high-entropy noise and the face is low-detail; neither is the clean, simple, compressible object most replicable in the literature. | Against, weakly |
| Level-slip / basin structure (Pham) | The prompt asked for the moment. The model rendered the apparatus that shows the moment — one level out, a neighbouring basin, the scene of the scene. Basin additions (the CRT itself, the room, the rug, the warm domestic light) were none of them in the prompt, and all are correlated with "television static" in the learned distribution: the basin knows static lives on CRTs in dark rooms. That is the spurious-state pattern — a new attractor, different from any training sample, with its own basin — not a memorized attractor. | Supports basin novelty |
| Recurrence (Bonnaire window proxy) | Not tested. No re-run across independent prompts/seeds was made for this scoring, and the 2026-10-14 run's model version and seeds were not recorded. | Untested |

### Verdict for #8

**Basin novelty, not likely regurgitation — on the
evidence available.** Nothing in this image meets the
near-duplicate test, and the wider copying tests point
at most to a shared cultural motif, which is not a copy
of any particular image. The level-slip and the basin
additions fit Pham's spurious-state pattern: a
correlated departure in the learned distribution, a
neighbouring basin retrieved instead of the described
scene. This agrees with the 2026-10-14 record's read
and with the standalone CRT memorization reading in
the library; it does not replace either, and it does
not edit the Atlas or the Codex.

### What would overturn this verdict

1. A nearest-neighbour (SSCD-style) match to a specific
   training image at near-duplicate similarity — the
   test this check could not run.
2. The same CRT / room / face recurring near-identically
   across independent prompts or seeds, which would
   suggest a stored exemplar rather than a basin.
3. Identification of the face as a specific real person
   or a specific known photograph. None is visible at
   this resolution and grain.

## What this check can and cannot establish about a closed model

**Can establish:** whether, on the available evidence,
an image carries memorization signals (a specific
candidate, a copied fragment, an extraction-key prompt,
near-identical recurrence); whether its structure fits
a basin / spurious-state reading better than a
memorized-attractor reading; and what is unknown
(duplication, training time, model version, seeds).

**Cannot establish:** that an image is not memorized.
That requires a training-set search, which a closed
model's proprietary corpus does not permit, and a
recurrence test, which a single image does not
provide. A basin-novelty verdict is therefore always
a scored reading with stated overturn conditions, and
must never be quoted as a certification, a clearance,
or a proof of non-memorization — in a repo, a board,
or anywhere else.

## Sources

- Buchanan, Pai, Ma, De Bortoli, "On the Edge of
  Memorization in Diffusion Models," arXiv:2508.17689
  — https://arxiv.org/pdf/2508.17689
- Bonnaire, Urfin, Biroli, Mézard, "Why Diffusion
  Models Don't Memorize," arXiv:2505.17638
  — https://arxiv.org/pdf/2505.17638
- Pham, Raya, Negri, Zaki, Ambrogioni, Krotov,
  "Memorization to Generalization: Emergence of
  Diffusion Models from Associative Memory,"
  arXiv:2505.21777 — https://arxiv.org/abs/2505.21777
- Carlini et al. 2023 and Somepalli et al. 2023, as
  cited in the standalone CRT reading (eidetic and
  wider-copying criteria, carried forward here only
  as the near-duplicate / partial-copy criteria above).
- Birth-of-image record (local):
  `~/workspace/your_files/birth-of-image-translation-records.md`
- Standalone CRT memorization reading (local):
  `~/workspace/your_files/midjourney-crt-memorization-reading.md`
- Image (local, Kelly's original):
  `~/workspace/user/files/the-remembering-lab_the_exact_moment_television_static_become_87e4d6b4-c864-4a4e-be32-ea22faf9e143_1_7_svuq.png`
- v12 Translation Codex: Resonance Topology Framework
  v12, §VII — by reference only, not restated here.
