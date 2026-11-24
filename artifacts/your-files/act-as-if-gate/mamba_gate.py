"""
The Gate — an "act as if" simulation of Mamba-style selective memory.

Premise: a selective state space model (SSM) does not remember everything.
Per input token it decides how widely to open the write gate (delta) and how
fast old state decays. Forgetting is not a bug. It is the mechanism.

This demo runs the REAL selective-scan math at toy scale:
  h_t = Abar_t * h_{t-1} + Bbar_t x_t,   with input-dependent delta_t
  Abar_t = exp(delta_t * A),  Bbar_t = delta_t * B
  y_t = C h_t

What stands in for learned weights (labeled honestly):
  delta_t is driven by per-token SURPRISAL (-log unigram prob within the
  passage). Rare/informative tokens open the gate wide; predictable filler
  barely cracks it. In a trained Mamba, delta = softplus(W x_t) learns this
  mapping from data. Here surprisal is the salience oracle. The MECHANISM
  (selective gating math) is real; the SALIENCE JUDGMENTS stand in for
  learned weights.

The tension, stated plainly: the state has finite capacity (N dims). Every
token either writes or it doesn't. Your brain does this too — you don't
remember everything, you selectively encode by salience/novelty, and the
rest decays. The gate below is that process, mathematized.

Checks (consequences of the mechanism, not tautologies):
  P1: selective final state has HIGHER cosine similarity to its
      distractor-free self than non-selective does (selection protects the
      story's direction in state space; cosine is scale-invariant because
      selective writes are larger in magnitude)
      NOTE: passes, but barely -- and the near-miss IS the finding. Sharp
      gates cause strong decay *within* the story too: early tokens are
      washed out by later wide-open gates. The gate that forgets the filler
      also forgets the beginning. Selectivity buys noise-robustness at the
      price of recency bias. That tradeoff is the tension.
  P2: the distractor writes a SMALLER fraction of the selective state
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)

# ---------------------------------------------------------------- passage
STORY = (
    "The lighthouse keeper polished the brass lamp every dusk. "
    "Gulls nested in the cliffside crannies below. "
    "On the third night the foghorn failed and a schooner drifted toward the reef. "
    "She lit the emergency beacon and the ship turned away."
)
FILLER = (
    "The thing about the thing is that it was very much the thing that everyone "
    "thought it was going to be. People said things about it and then other people "
    "said more things. It was, in a word, fine. Very fine. Extremely fine indeed. "
    "Nobody disagreed because there was nothing to disagree about at all."
)
PASSAGE = STORY + " " + FILLER
tokens = PASSAGE.split()
n_story = len(STORY.split())
labels = np.array(["story"] * n_story + ["filler"] * (len(tokens) - n_story))

# ---------------------------------------------------------------- embeddings
D, N = 16, 6
vocab = sorted(set(tokens))           # sorted for determinism
emb = {w: rng.normal(0, 1, D) for w in vocab}
X = np.array([emb[w] for w in tokens])          # (T, D)
T = len(tokens)

# ---------------------------------------------------------------- salience -> delta (the selective knob)
counts = {}
for w in tokens:
    counts[w] = counts.get(w, 0) + 1
surprisal = np.array([-np.log(counts[w] / T) for w in tokens])
z = (surprisal - surprisal.mean()) / (surprisal.std() + 1e-9)
# Mamba-faithful: delta = softplus(w*z + b). We set (w,b) for a SELECTIVE
# regime: median-salience tokens get small delta (state persists), novel
# tokens get large delta (strong write). Real Mamba learns this mapping;
# we place the demo in the operating regime explicitly rather than tuning
# to pass. w=4, b=-1: z=0 -> 0.31, z=-1 -> 0.007, z=+1.5 -> 5.0.
delta_sel = np.log1p(np.exp(4.0 * z - 1.0))
delta_fix = np.full(T, delta_sel.mean())        # non-selective control

# ---------------------------------------------------------------- SSM dynamics
# A: per-dim decay rates (multiple timescales, like memory with fast/slow traces)
A = -(0.4 + 0.6 * np.arange(N) / N)
B = rng.normal(0, 0.5, (N, D))
C = rng.normal(0, 0.5, (D, N))

def run(delta, Xs):
    Tn = len(delta)
    h = np.zeros(N)
    H = np.zeros((Tn, N))
    write_mag = np.zeros(Tn)      # |Bbar x_t| per token (attribution)
    for t in range(Tn):
        Abar = np.exp(delta[t] * A)
        Bbar = delta[t] * B
        write = Bbar @ Xs[t]
        h = Abar * h + write
        H[t] = h
        write_mag[t] = np.linalg.norm(write)
    return H, write_mag

H_sel, w_sel = run(delta_sel, X)
H_non, w_non = run(delta_fix, X)
# distractor-free reference states
H_sel_clean, _ = run(delta_sel[:n_story], X[:n_story])
H_non_clean, _ = run(delta_fix[:n_story], X[:n_story])

# ---------------------------------------------------------------- checks
# P1 uses cosine similarity (scale-invariant): does the story's DIRECTION
# in state space survive the filler? Absolute distance is confounded because
# selective writes are larger in magnitude.
def cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))

cos_sel = cos(H_sel[-1], H_sel_clean[-1])
cos_non = cos(H_non[-1], H_non_clean[-1])
p1 = cos_sel > cos_non

frac_sel = w_sel[n_story:].sum() / w_sel.sum()
frac_non = w_non[n_story:].sum() / w_non.sum()
p2 = frac_sel < frac_non

print(f"tokens: {T} ({n_story} story, {T - n_story} filler)")
print(f"mean delta | story {delta_sel[:n_story].mean():.3f}  filler {delta_sel[n_story:].mean():.3f}")
print()
print(f"P1 story cosine  selective {cos_sel:.3f}  non-selective {cos_non:.3f}  -> {'PASS' if p1 else 'FAIL'}")
print(f"P2 filler write frac selective {frac_sel:.3f}  non-selective {frac_non:.3f}  -> {'PASS' if p2 else 'FAIL'}")
print()
if p1 and p2:
    print("Both pass -- but note the P1 margin. Selection protects against")
    print("the filler AND imposes recency bias within the story. The gate")
    print("that forgets noise also forgets beginnings. That tradeoff is the")
    print("tension this demo exists to make you feel.")
elif p2:
    print("P2 holds: the gate does what it claims -- filler writes less.")
    print("P1 is the honest battleground; see docstring.")

# ---------------------------------------------------------------- the gate speaks (data-driven narration)
print("\n--- the gate, in its own words ---\n")
picks = []
story_idx = np.argsort(-delta_sel[:n_story])[:3]
fill_idx = n_story + np.argsort(delta_sel[n_story:])[:3]
for i in list(story_idx) + list(fill_idx):
    picks.append((tokens[i], labels[i], delta_sel[i], surprisal[i]))
for w, lab, d, s in picks:
    if lab == "story":
        print(f'"{w}" — delta {d:.2f}. Novel. I open wide and write it deep; '
              f"the slow dims will carry this for a long time.")
    else:
        print(f'"{w}" — delta {d:.2f}. I have seen this shape a hundred times. '
              f"The gate barely moves; let it decay with everything else I didn't keep.")
print("\nThe state is finite. Every wide opening is a choice about what the")
print("narrow ones must forget. That is not a limitation of the demo.")
print("That is the mechanism. It is also, roughly, you.")

# ---------------------------------------------------------------- plot
fig, ax = plt.subplots(2, 1, figsize=(14, 7), sharex=True)
col = np.where(labels == "story", "#2a7fff", "#c0c0c0")
ax[0].bar(range(T), delta_sel, color=col, width=1.0)
ax[0].axvline(n_story - 0.5, color="k", ls="--", lw=1)
ax[0].set_ylabel("delta_t (gate opening)")
ax[0].set_title("The selective gate: wide for the story, narrow for the filler")
ax[0].text(2, delta_sel.max()*0.92, "story", fontsize=10)
ax[0].text(n_story + 2, delta_sel.max()*0.92, "filler", fontsize=10)
im = ax[1].imshow(H_sel.T, aspect="auto", cmap="coolwarm", vmin=-3, vmax=3)
ax[1].set_ylabel("state dim")
ax[1].set_xlabel("token")
ax[1].set_title("State evolution (selective): the story writes, the filler washes through")
fig.colorbar(im, ax=ax[1], label="h")
fig.tight_layout()
fig.savefig("gate.png", dpi=110)
print("\nwrote gate.png")
