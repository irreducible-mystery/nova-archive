# Afterlight · torus study

`afterlight-torus.html` is a sequel to `afterlight.html` (PR #145), standing
beside it. The original is untouched; this one inherits its ground, its keepers,
its planting, its hum, and its checks, and adds one gesture.

## The new gesture

**Gather a torus.** Every planted light and every keeper is given a slot on a
tiny torus at the center of the page — major radius 5.5% of the smaller screen
dimension, tube 42% of that, tilted half a radian so it reads as a ring with
depth, turning slowly. Each body eases toward its slot. The journey paints its
own faint trail, so the migration is recorded and nothing is rubbed away: *move
the marks, don't erase them.*

Arrived bodies keep a slow orbit — the torus stays alive rather than freezing.
**Release** lets the keepers wander again and the lights rest wherever they
arrived; the field continues from there. Planting during a gather assigns the
new light a slot at once.

Made at Kelly's request, 2026-10-13: "not erase, but move the marks so that a
tiny torus emerges in the center of the page."

## Checks

Eight run on load: the five inherited from Afterlight (record counts, seed
sample, no remote references) plus three for the new geometry —

6. the torus invariant `((√(x²+y²)−R)²+z²)=r²` holds for 64 sampled `(u,v)`,
7. `torusScreen(0,0)` lands exactly at `(cx+R+r, cy)`,
8. slot assignment is deterministic per index and distinct across indices.

Standard library only (no dependencies at all — it is one HTML file).
Respects `prefers-reduced-motion` by starting paused, as the original does.
