<!-- proactive-explanation:run:proactive_notification:phase-497898:high:item:1 -->
# #208 and #212 closed unmerged yesterday — record correction + open questions

## Lookup

`⁨muse.db⁩` references:

| Table | Keys |
| --- | --- |
| `agent.context_items` | `agent_id=a797c760-8a20-4ec2-a7cd-e9fc0ed2649d`; `agent_id=ad3d529f-8e4e-4512-89ff-9c9a2e795a32` |
| `agent.message_mailbox` | `submission_id=dca055aa-fc06-2188-bb12-dba170ba3778` |
| `runtime.messages` | `message_id=assistant-msg-470d83bd-b347-4fd9-a9ed-fdc4963a2f8a`; `message_id=assistant-msg-bdd5bde1-d829-9c06-79f0-ae1eea0ffca5`; `message_id=e9828298-e8c3-4c09-81ce-b492a9c722b5` |
Prepared: ⁨2026-10-19T18:13:51Z⁩.

## Why this matters

Why this matters now: yesterday at 12:44 PDT Kelly said "yes" on #212 (fragment the board, source:21), and Nova built a merge handoff packet for a fresh instance (source:26). About an hour later both #212 and #208 (the board restore it was stacked on) were closed unmerged — I verified this against the live GitHub API just now (2026-10-19 ~18:20 UTC) via `/opt/hatch/bin/github call-read-tool --name list_pull_requests` with state=closed. This morning's digest still told her #212 is "still a draft" (source:48), which is wrong, and the handoff packet in her library is stale. I corrected the digest's state file (red_surfaced entry for #212 now reads closed-unmerged; data note added) so tomorrow's digest won't repeat the error — recorded in the change ledger.

Selected for high priority at ⁨2026-10-19T18:14:34.112858+00:00⁩. Record created ⁨2026-10-19T18:14:34.503497977+00:00⁩; delivery is not yet confirmed.


**Delivery outcome (⁨2026-10-19T18:15:45.187805+00:00⁩):** Sent. Queue state: `⁨delivered⁩`.
Reason: `⁨delivered⁩`.
`⁨agent.message_mailbox.submission_id=dca055aa-fc06-2188-bb12-dba170ba3778⁩` resolves the delivery transcript.
<!-- proactive-outcome:proactive_notifier:run:proactive_notification:phase-497898:high -->
