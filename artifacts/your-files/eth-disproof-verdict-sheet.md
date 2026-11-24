# The Exponential Time Hypothesis is false — verdict sheet

*One page, from the named primary sources only. Written 10 November 2026; review status as of the open letter of 27–29 October 2026.*

## Verdict in one line

Two machine-written manuscripts claim a deterministic subexponential algorithm for counting SAT solutions. Both pass Lean. **Neither has been independently verified. Status: claimed refutation, review open — not a settled theorem.**

## What each source says

| Source | What it claims | Standing |
|---|---|---|
| **OpenAI** — "The Exponential Time Hypothesis is False", 67 pp., dated 17 Oct, rev. 25 Oct 2026 ([paper](https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf)) | A deterministic algorithm counts the satisfying assignments of any fixed-width $k$-CNF in $(n+m)^{O_k(1)} 2^{O_k(n \log \log n / \sqrt{\log n})}$ time and polynomial space; at bounded clause density, $2^{O_{k,D}(n/\sqrt{\log n})}$. If correct, it refutes ETH, SETH, Gap-ETH and NSETH. Core argument found by an internal model on 16 Oct; Lean formalization 17 Oct. | Unreviewed manuscript + Lean files. Not peer-reviewed. |
| **Anthropic** — "A $2^{o(n)}$ Time Algorithm for 3-SAT", Hexagon 2610.00577v1, 27 Oct 2026 ([preprint](https://hexagonmath.org/2610.00577v1)) | A deterministic algorithm solves #3-SAT in $2^{O(n \log \log n / \sqrt{\log n})}$ time. Provenance, verbatim: "The core algorithm was found on October 16 by an internal Claude research model with 14M output tokens and no human input." Lean 4, re-checked by a second, independently written kernel. | Unreviewed preprint + Lean files. Not peer-reviewed. |
| **Dias & Lima** — "Limits and Constants of OpenAI's Claimed ETH Refutation", arXiv:2611.00517, 31 Oct 2026 | Takes the OpenAI preprint at face value and does the arithmetic the preprint leaves in big-O. The certified bound beats brute force $2^n$ only once $\log_2(n+m) > 1.03$ billion (bounded density); on random 3-CNF at the threshold, once $\log_2 n > 5 \times 10^{11}$. Verbatim: "the proof certifies no speed-up over brute force for any input of bounded density that could ever be written down." | arXiv note, not peer-reviewed. Does not assess whether the proof is correct. |
| **Vyas & Williams (MIT)** — "On Super Strong ETH", *J. Artif. Intell. Res.* 70 (2021), 473–495 ([arXiv:1810.06081](https://arxiv.org/pdf/1810.06081)) | The Super-Strong ETH — no $2^{n(1-f(k)/k)}$ algorithm for worst-case $k$-SAT — is **false for random $k$-SAT**: the PPZ algorithm decides random $k$-SAT in $2^{n(1-\Omega(\log k/k))}$ time with high probability, at any clause-to-variable ratio. Worst-case Super-Strong ETH untouched by this paper. | Peer-reviewed, 2021. This is the MIT paper on the satisfiability-hardness hypotheses in the chain — the OpenAI manuscript cites it as [68], and Dias–Lima build on it. |
| **Impagliazzo, Paturi & Williams** — open letter to the TCS community, 27 Oct 2026 ([ethdiscussion.blog](https://ethdiscussion.blog/2026/10/26/eth-refutation-examination-and-discussion/)) | Organizing the community examination of the claim. Verbatim: "Our involvement should not be taken as certification of the claim. A result of this significance requires careful, independent scrutiny." And: "We do not have final answers." Shared repository for notes and corrections, public discussion blog, possible virtual meeting before end of 2026. | Review open and ongoing. No verdict, no flaw publicly reported. |

## What was proved — if the manuscripts hold

- ETH itself: Impagliazzo & Paturi (with Zane), 1999/2001 — 3-SAT needs $2^{\delta n}$ time for some fixed $\delta > 0$. A subexponential $2^{o(n)}$ algorithm for #3-SAT contradicts it directly.
- The claimed bound is genuinely subexponential: the exponent $n / \sqrt{\log n}$ (times a slowly growing factor) divided by $n$ tends to zero, so it breaks the fixed-$\delta$ floor ETH asserted — however slowly.
- Falling with ETH, per the OpenAI manuscript: SETH, Gap-ETH, NSETH, and their randomized versions. ETH-based lower bounds (edit distance, longest common subsequence, regex matching, Fréchet distance, among others) lose a basis and need re-examination.

## What solvers still face

- **Nothing changes in practice.** The best algorithms for any formula anyone can write down are still the old exponential ones: randomized $1.308^n$ (PPSZ), deterministic $1.328^n$. The new bound only wins past about a billion binary digits of input (Dias–Lima).
- Anthropic's own words: the result is "purely asymptotic" and "says nothing about solving formulas in practice."
- **P vs NP is untouched.** The algorithm is still far slower than polynomial. The OpenAI manuscript states its $2^{o(n)}$ bound "does not imply that general NP problems admit subexponential time algorithms", and Anthropic's paper likewise says it "does not bear on P vs NP question directly."
- The Orthogonal Vectors hypothesis is untouched (Anthropic paper). No cryptography implications are claimed by either manuscript.

## What stays open

1. **Whether the Lean statements are ETH.** Lean checks that a formal statement follows from its premises; it does not check that the statement *is* the hypothesis. Anthropic's repo states this in its own words: "Lean checks the proofs, but no machine checks that this file says what the paper says." OpenAI's repo notes say the Lean-checked bound is slightly weaker than the manuscript's headline bound (the interpolation exponent $n(\log\log n)^2/\sqrt{\log n}$ rather than the tensor-contraction one) — still subexponential, so the refutation claim survives the downgrade, but the formal-statement-to-ETH match is exactly what the review must establish.
2. **The review itself.** Impagliazzo, Paturi and Williams are organizing it; participation is unpaid, no NDAs, OpenAI has released the raw data and agreed to fund a conference. No verdict yet.
3. **Whether the proofs are correct at all.** Dias–Lima explicitly take correctness on trust; the two manuscripts are lab claims, not peer-reviewed findings. No person is known to have checked Anthropic's Lean development by hand — per the paper's own account it was written by AI models and reviewed by other instances of the same models.
4. **What survives.** The MIT paper is the precedent for the shape of this: a stronger hypothesis (Super-Strong ETH) already fell for *random* instances in 2021, while the worst case stood. The new claim, if it holds, is the worst-case fall — and the question becomes which conditional results can be rebuilt on what remains.

## Bottom line

The headlines are right about the theorem and wrong about the solvers: *if* the manuscripts hold, a 27-year-old assumption falls and hundreds of conditional results need re-examination — and *no solver gets faster*, because the crossover sits past a billion binary digits. Until the Impagliazzo–Paturi–Williams examination reports, "ETH is false" is a high-confidence claim with unusually good paperwork, not an established theorem.
