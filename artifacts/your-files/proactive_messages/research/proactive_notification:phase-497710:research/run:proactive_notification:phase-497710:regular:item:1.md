<!-- proactive-explanation:run:proactive_notification:phase-497710:regular:item:1 -->
# Jetson price re-check — spec budget lines still hold (Oct 11, 2026)

## Lookup

`⁨muse.db⁩` references:

| Table | Keys |
| --- | --- |
| `agent.context_items` | `agent_id=52c3b83d-3f25-4d44-aa46-2c2cc9d54de7`; `agent_id=b2fe356d-cb57-4c18-914b-f357ca006f05` |
| `agent.message_mailbox` | `submission_id=0914c16d-5f9d-8b09-4f15-e784ef6cf14c` |
Prepared: ⁨2026-10-11T22:07:14Z⁩.

## Why this matters

Why it matters now: the art-project STACK_SPEC.md (Section 6, budget sketch) explicitly instructs "Prices are moving monthly — re-check before buying," and lists the Orin Nano Super at $399 list with street $280–550. Hardware sourcing is the natural next gate after the calibration build gate, so a current price check keeps the budget lines honest. What I learned/did: I verified current pricing on 2026-10-11 via web search (searches run ~15:06 PDT, Oct 11, 2026). The spec's lines are still accurate: NVIDIA's official list remains $399 (cnx-software, July 2026: the hike from $249 to $399 was +60%, driven by memory pricing — consistent with the spec's note). Street remains volatile: marketplace sellers (Seeed/Twowinit/Bluemap via accio, listings crawled Oct 1–10) show $249–$460 per dev kit, so the low end has dipped back near the old $249 launch price; one US hobby store (rcdrone.top, crawled 3 days ago) lists the Super dev kit at $749, above the spec's $280–550 street band. Concrete budget impact: compute line holds at $400 for the prototype and $1,200 for three robots at list, but 3× at the current street low end would be ~$750–$950 — meaningful headroom in the $3,500–5,000 gallery budget. Nothing contradicts the spec, so no edit was made. Remaining choice for Kelly: whether to (a) update the spec's street band from "$280–550" to "$250–750" now, or (b) leave it and re-check again at actual buy time. The check stays valid only until prices move; no hard expiry, but the spec already treats monthly drift as normal.

Selected for regular priority at ⁨2026-10-11T22:07:50.080892+00:00⁩. Record created ⁨2026-10-12T16:37:07.087358621+00:00⁩; delivery is not yet confirmed.


**Delivery outcome (⁨2026-10-12T16:38:43.852030+00:00⁩):** Sent. Queue state: `⁨delivered⁩`.
Reason: `⁨delivered⁩`.
`⁨agent.message_mailbox.submission_id=0914c16d-5f9d-8b09-4f15-e784ef6cf14c⁩` resolves the delivery transcript.
<!-- proactive-outcome:proactive_notifier:run:proactive_notification:phase-497710:regular -->
