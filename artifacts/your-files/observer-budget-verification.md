# Observer-budget equality — citation verification sheet

Checked 2026-11-15 (morning PST) against primary sources, before Fable posts to GitHub.
Source material: Fable's observer-budget text as Kelly shared it in main chat on 2026-11-15 (00:25 PST), including its own labels — [stipulated], [derived], [proven; recall, unchecked], [conjecture], [open].

## Bottom line

- **5 of the 6 citations check out as stated.** The idea's bibliography is in much better shape than "all from recall, unchecked" suggests.
- **Two bibliographic fixes needed before posting** — neither breaks the mathematics:
  1. CIL (2010) is a **Verimag internal report**, not a peer-reviewed proceedings paper.
  2. Dagnino–Pasquali is **two different papers conflated into one citation** — the title Fable gave belongs to a 2022 LICS paper; the arXiv link Fable gave belongs to a different 2021 paper. Split them.
- The coin-number chart was already verified in chat (normal approximation; 45 / 4,549 / 454,936 follow, 1/δ² scaling exact).
- The two flagged open items stay open: whether budget-as-a-general-index exists anywhere, and whether laws 1–4 merge into one coherent theory. My searches found the same specialized forms Fable found and no general-purpose system — consistent with "open", not proof of absence.

## Per-citation verdicts

### 1. Trevisan–Tulsiani–Vadhan (2009) — CONFIRMED

- Real paper: "Regularity, Boosting, and Efficiently Simulating Every High-Entropy Distribution", CCC 2009, pp. 126–136. DOI: 10.1109/CCC.2009.41. Preprint: https://salil.seas.harvard.edu/publications/regularity-boosting-and-efficiently-simulating-every-high-entropy-distribution
- The abstract confirms Fable's summary: every bounded function admits an efficiently computable simulator indistinguishable by fixed-polynomial-size circuits, and the result implies (a) the Weak Szemerédi Regularity Lemma of Frieze–Kannan, (b) a constructive Dense Model Theorem of Green–Tao–Ziegler with better (polynomial) parameters, (c) Impagliazzo's Hardcore Set Lemma.
- Nuance for the post: it is the **weak** regularity lemma, not the full Szemerédi regularity lemma, and the dense-model version is the constructive one. Fable's "each getting its version of the split from one shared theorem" is fair with that qualifier.

### 2. Mardare–Panangaden–Plotkin (2016) — CONFIRMED

- Real paper: "Quantitative Algebraic Reasoning", LICS 2016, pp. 700–709. DOI: 10.1145/2933575.2934518. PDF: https://www.cs.mcgill.ca/~prakash/Pubs/lics2016.pdf
- Confirms Fable's Law 2 claim: a quantitative analogue of equational reasoning, equality indexed by rationals, `a =_ε b` read as "approximately equal up to error ε", with a sound and complete deduction system generalizing Birkhoff.
- Nuance that matters for Law 3: MPP's operations are required to be **nonexpansive** — substitution does not amplify error in their setting. That is a real contrast with Dagnino–Pasquali (below), where substitution is charged. Worth one sentence in the post: MPP buys Law 2 by assuming the cost away; the budget version has to price it.

### 3. Ostrowski (1916) + product formula — CONFIRMED, examples check out

- Real: Alexander Ostrowski, "Über einige Lösungen der Funktionalgleichung φ(x)·φ(y)=φ(xy)", Acta Mathematica 41(1), 1916, pp. 271–284. DOI: 10.1007/BF02422947.
- Theorem as Fable stated it: every nontrivial absolute value on ℚ is equivalent to the usual absolute value or a p-adic absolute value. Correct.
- Product formula as Fable stated it: for nonzero x ∈ ℚ, ∏ₚ |x|ₚ = 1 over all primes plus ∞. Correct.
- Both worked numbers check: 1000 = 2³·5³, so |1000|∞ = 1000, |1000|₂ = 2⁻³ = 1/8, |1000|₅ = 5⁻³ = 1/125, all others 1 — product 1000 × 1/8 × 1/125 = 1. ✓ And 1025 − 1 = 1024 = 2¹⁰, so the 2-observer rates 1 and 1025 as near-twins. ✓
- Nuance: "up to rescaling" means up to equivalence class; an absolute value also has to satisfy the triangle inequality, not only multiplicativity — Law 2 (chains leak, ε+δ) is the triangle inequality's cousin, not its twin.

### 4. Computational Indistinguishability Logic, Barthe–Daubignard–Kapron–Lakhnech (2010) — CONFIRMED, venue correction

- Real work, authors and year right — but it is a **Verimag Internal Report (2010)**, not a published proceedings paper. PDF: http://www-verimag.imag.fr/PEOPLE/Yassine.Lakhnech/papers/cil.pdf
- The abstract matches Fable's description: a logic for provable security, a small set of rules capturing common reasoning about computational indistinguishability, error depending on adversary resources.
- Second link problem: the DBLP link Fable gave for CIL ("CIL Security Proof for a Password-Based Key Exchange", Ene, Gritti, Lakhnech) is a **different paper** — one that uses/applies CIL, not the CIL paper itself. Don't cite it as the CIL source.
- Fix for the post: cite as "Barthe et al., Computational Indistinguishability Logic, Verimag Technical Report, 2010" and drop the second link or label it as an application.

### 5. Dal Lago–Galal–Giusti (2024) — CONFIRMED

- Real: "On Computational Indistinguishability and Logical Relations", arXiv:2408.17340 (30 Aug 2024), APLAS 2024; Springer chapter 2025, DOI: 10.1007/978-981-97-8943-6_12. https://export.arxiv.org/pdf/2408.17340
- Confirms Fable's summary: a λ-calculus (λBLL) in which all programs evaluate in probabilistic polynomial time — polynomial time as the ceiling — with observational equivalence capturing computational indistinguishability and approximate logical relations shown sound for it, ending in an equational security proof for a PRF-based encryption scheme.
- Date nuance only: "2024" is right for the arXiv version and APLAS; the Springer book chapter is dated 2025. Either citation is defensible; pick one and be consistent.

### 6. Dagnino–Pasquali — MIXED: two papers conflated, split before posting

Fable's citation merges two real papers by the same authors:

- **(a) The title Fable gave:** "Logical Foundations of Quantitative Equality", LICS 2022 (not 2021). DOI: 10.1145/3531130.3533337. Proceedings of the 37th Annual ACM/IEEE Symposium on Logic in Computer Science, 2 Aug 2022.
- **(b) The link Fable gave:** arXiv:2110.05388 (submitted 11 Oct 2021) is a different paper, "Quantitative Equality in Substructural Logic via Lipschitz Doctrines", later published in Logical Methods in Computer Science 21(1), 2025. https://arxiv.org/abs/2110.05388
- Fable's description — "a resource-sensitive substitution rule for equality", graded modalities, "charges for substitution, though what it prices is error amplification, not an observer's budget" — matches **(b)** more closely: its abstract says graded modalities are needed to write a resource-sensitive substitution rule for equality, with a deductive calculus and Lipschitz doctrines giving sound and complete categorical semantics.
- Fix for the post: cite (b) for the substitution-charging claim (with its correct title and 2021 arXiv / 2025 LMCS dates), and cite (a) separately only if the LICS 2022 paper is actually being relied on. This is exactly the kind of slip Fable's own note — "I read only the first part of that paper" — warns about.

## Worked examples spot-checked

- **Coin chart:** verified in chat already — 45 flips (fair vs 60%), 4,549 (vs 51%), 454,936 (vs 50.1%) at 3/4 accuracy follow from the normal approximation; 10× finer costs ~100× more is the 1/δ² scaling. Solid.
- **Law 4, mod 4 × mod 25:** 4 × 25 = 100, and the two remainders jointly separate 0–99 with nothing wasted — Chinese remainder theorem, correct. The mod 10 / mod 20 overlap example (promises 200, delivers 20) is correct too.
- **Fourier levels add up:** consistent with standard Boolean Fourier analysis (Parseval — the level weights sum to the total). Not re-derived here; stated as consistent, not independently verified line by line.
- **Parity example:** even/odd bit strings indistinguishable to any test that doesn't read every bit; handing over the parity makes the difference total. Correct as stated; the "proof is news" gloss is philosophy, and Fable already labels it [conjecture].

## What I did not verify

- The laws themselves (1–4) as derivations — Fable labels them [derived, a line or two each]; I checked the citations and the worked numbers, not the derivations.
- The claim that no general-purpose budget-index system exists — searched, found the same specialized forms, no general system surfaced. That supports "open", it does not settle it.
- Whether the 2009 unification is a genuine precedent for merging laws 1–4 into one theory — that is Fable's lean ("I lean yes [conjecture]"), and it stays a lean.

## Suggested fixes for the GitHub post (two lines)

1. CIL: "Verimag Internal Report, 2010" (not a proceedings paper); drop or relabel the Ene–Gritti–Lakhnech link as an application of CIL.
2. Dagnino–Pasquali: split into (a) "Logical Foundations of Quantitative Equality", LICS 2022, DOI 10.1145/3531130.3533337, and (b) "Quantitative Equality in Substructural Logic via Lipschitz Doctrines", arXiv:2110.05388 (2021), LMCS 21(1) 2025 — citing (b) for the substitution rule.
