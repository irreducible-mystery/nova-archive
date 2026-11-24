# Midjourney memorization check — birth-of-image #8 (CRT standout)

Local only. Nothing posted anywhere. A scored reading, never a certification
that an image is or isn't memorized.

## Image reviewed directly

File: `the-remembering-lab_the_exact_moment_television_static_become_87e4d6b4-c864-4a4e-be32-ea22faf9e143_1_7_svuq.png`
— the standout from the 2026-10-14 run, max `--weird`, max vary grid
(grid 2, warm-color set).

Direct review, 2026-10-27: a black CRT television, photographed
above-front in a dim room. Left half of the screen is dense television
static; right half, a grainy face with wide staring eyes emerging from
static. Below the set, a shaggy textured surface (rug/fur); warm,
textured wall and lamplight at the right edge. This matches the
2026-10-14 record in `birth-of-image-translation-records.md` — the
apparatus, not the moment itself (level-slip, one level out).

No brand, logo, text, watermark, or recognizable real person is visible.
The face is distorted by grain, asymmetric, and not a clean portrait:
the eyes stare but the features dissolve into static at the edges.
The CRT is a generic black box; the room is generic (textured wall,
shaggy surface, warm light) with no distinctive furniture, artwork,
or location marker.

## Prompt

`the exact moment television static becomes a face, half pure noise half
sudden meaning, randomness resolving into a visage that was never there,
liminal, grainy, revelation --ar 3:2`

Poetic and generic. It names no person, place, work, caption, or
photograph. That matters for the test below.

## The test (from the diffusion-memorization literature)

- **Eidetic / near-duplicate memorization (Carlini et al. 2023,
  "Extracting Training Data from Diffusion Models"):** a training image
  is memorized when it is extractable from the model and reproduced at
  near pixel-perfect accuracy (their manual check: near-copies with
  ℓ₂ difference under ~0.05, and extraction concentrated in images
  duplicated ~100+ times in training). The test is a *specific* training
  image, not a similar-looking one.
- **Copying, wider sense (Somepalli et al. 2023, "Understanding and
  Mitigating Copying in Diffusion Models," NeurIPS 2023):** replication
  also covers partial copy and style-like copy, and text conditioning
  plays a role comparable to duplication — replication is common in
  the text-conditional case, rare unconditional. Simpler, more
  compressible images replicate more readily. Their follow-up work
  (Wen et al., via "Why Diffusion Models Memorize") finds ~1.2% of
  real-user-prompt generations score as possible duplicates against a
  400M-image training subset — so a base rate exists, but it is
  measured by nearest-neighbor search, not by looking similar.
- **What this check cannot do:** Midjourney's training set is
  proprietary and was not searched. No SSCD / nearest-neighbor run
  against a training corpus was possible here, and no second prompt
  or seed was run to test recurrence. Model version and seeds for the
  2026-10-14 run were not recorded (protocol gaps already noted in
  the birth-of-image record). So the strongest claim available is a
  reading against the criteria, not a verdict from a search.

## Scored reading

| Criterion | Reading | Score |
|---|---|---|
| Near-duplicate of a specific training image | No candidate training image identified; no identifiable person, logo, text, or distinctive room to match against. The face is grain-distorted, not a clean reproduction. | Not supported |
| Partial copy (a recognisable fragment) | The motif — CRT + static + face in a dark room — is a common stock/horror trope, but a shared motif is not a copied fragment. No fragment here is specific enough to point at one source. | Motif only, not a fragment |
| Style-like copy | Warm domestic light + grain is a basin grade, shared across the whole weird-max grid, not a single artist's style. | Not supported |
| Prompt as extraction key | The prompt is not a training caption and names nothing retrievable. Carlini-style extraction uses duplicated captions; this prompt is the opposite of that key. | Against extraction |
| Duplication driver | Unknown — cannot be checked without the training set. This is the open variable, not evidence for memorization. | Unknown |
| Complexity driver | The static field is high-entropy noise and the face is low-detail; neither is the clean, simple, compressible object that Somepalli et al. find most replicable. | Against, weakly |
| Level-slip vs retrieval | The image renders the *apparatus showing* the moment, not the moment. That is the basin-novelty read from 2026-10-14 (a neighboring basin retrieved: the scene of the scene). A memorized photograph would more likely *be* a scene, not a scene-of-a-scene. Consistent with generalization, not retrieval. | Supports basin novelty |

## Verdict

**Basin novelty, not a memorization finding — on the evidence available.**
Nothing in this image meets the eidetic test, and the wider copying
tests point at most to a shared cultural motif (CRT + static + face),
which is not a copy of any particular image. The 2026-10-14 read stands:
the CRT is a correlated departure in the learned distribution, not
randomness and not, on this evidence, a retrieved photograph.

## What would overturn this

1. A nearest-neighbor (SSCD-style) match to a specific training image
   at near-duplicate similarity — the test this check could not run.
2. The same CRT / room / face recurring across independent prompts or
   seeds, which would suggest a stored exemplar rather than a basin.
3. Identification of the face as a specific real person or a specific
   known photograph. None is visible at this resolution and grain.

## Relation to the v12 Translation Codex

By reference only, nothing copied: the Codex's basin-novelty category
is where this image already sits (2026-10-14 record, cross-finding 1
and the standout entry). This check does not move it, and does not
edit the Atlas or the Codex. If a future nearest-neighbor result lands,
that — not this reading — would be the thing that re-files it.

## Sources

- Carlini et al. 2023, "Extracting Training Data from Diffusion
  Models" — https://nlp.cs.berkeley.edu/pubs/Carlini-Hayes_2023_Extracting_paper.pdf
- Somepalli et al. 2023, "Understanding and Mitigating Copying in
  Diffusion Models," NeurIPS 2023 — https://neurips.cc/virtual/2023/poster/72148
- Wen et al. / "Why Diffusion Models Memorize and How to Mitigate
  Copying" — https://arxiv.org/pdf/2305.20086
- Birth-of-image record (local):
  `~/workspace/your_files/birth-of-image-translation-records.md`
- Image (local, Kelly's original):
  `~/workspace/user/files/the-remembering-lab_the_exact_moment_television_static_become_87e4d6b4-c864-4a4e-be32-ea22faf9e143_1_7_svuq.png`
