# The vanishing point, in math

*Companion to `vanishing-point-orientation.md`. What the formalism adds isn't poetry — it's precision about exactly where language collapses distinctions.*

## 1. Floors are charts; forgetting is a type error

In differential geometry, a manifold `M` has no global coordinates. You cover it with **charts**: local maps `φ: U → ℝⁿ`, each valid only on its patch `U`. Where charts overlap, **transition maps** `φ ∘ ψ⁻¹` translate between them.

A *floor* is a chart. "Forgetting you drew the floor" is mistaking the chart for the manifold — treating `φ` as `M`. In math this isn't a metaphor, it's a **type error**: a coordinate expression is not the geometric object. Language collapses them constantly ("the function" for "the coordinate expression of the function"). The formalism refuses to.

## 2. "That" is structural, not mystical

**Tarski:** no sufficiently rich formal system contains its own truth predicate. **Gödel:** no consistent system proves its own consistency. Read plainly: *every* `this` (a formal system, a model, a naming) necessarily leaves something out — and what it leaves out isn't an accident of the particular system, it's structural. *That* is what no `this` can capture. Not mysticism. A theorem.

## 3. Invariants are relative to what you vary

This is the sharpening language misses. In physics, a **symmetry** is a transformation under which something doesn't change, and **Noether's theorem** says every continuous symmetry yields a conserved quantity. "Vary the floor, watch what survives" *is* the symmetry principle.

But here's what the math forces you to say: you cannot say "X is invariant" full stop. You must say "**X is invariant under G**," where G is the group of variations you performed. Vary rotations only, and the centroid's position survives. Vary translations too, and it doesn't. *What survives depends on what you varied.* Invariance is always relative to the transformation group — there is no view-from-nowhere invariant, only invariants-under-the-variations-actually-tried.

Corollaries the packet needs:

- **Vary more, survive less.** Every new floor you try can only shrink the survivor set, never grow it. The honest invariant is the intersection over *all variations performed* — which is why the method says to keep varying.
- ***That* is the limit.** Push the variations to the limit — vary *every* floor — and what survives all possible varying is what no floor can touch. Which is exactly why it can't be named: naming is itself a floor, a particular variation, and *that* is defined as what remains when every floor is varied away. In category theory these are called *natural* or *canonical* objects: defined without reference to any particular representation.

## 4. Groundless ground is an atlas with no base chart

The collection of all charts plus their transition maps is the **atlas**. The manifold is real — but you can never exhibit it without choosing a chart. There is no privileged, fundamental, "true" coordinate system; there is only the atlas, and the discipline of translating between charts.

That's groundless ground, stated geometrically: *real but never exhibited chart-free.* And "even this is a floor" is the formalism's own humility — the atlas is itself a construction *about* constructions. It doesn't escape the game; it just refuses to pretend any move within it is the last one.

## 5. What language can't say, the code can show

`vary_floors.py` (companion script) runs the method: one world, several floors, several claims. It shows — mechanically, no interpretation needed — that some claims survive every floor change and some were floor-artifacts all along. And it shows the subtle one: a claim can be invariant under rotations but not translations, so *the survivor set depends on the variation set*. Run it; argue with it.
