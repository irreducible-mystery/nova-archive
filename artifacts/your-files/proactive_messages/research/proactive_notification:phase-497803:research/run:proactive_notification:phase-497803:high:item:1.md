<!-- proactive-explanation:run:proactive_notification:phase-497803:high:item:1 -->
# Correction: Green audit verification needs no approval taps — read-only GitHub tools are already available

## Lookup

`⁨muse.db⁩` references:

| Table | Keys |
| --- | --- |
| `agent.context_items` | `agent_id=30c36204-e6bb-41d5-979c-186241b855f7`; `agent_id=ff41cc2a-4445-4254-a98b-5d38319fa702` |
| `agent.message_mailbox` | `submission_id=b9ee050d-883e-78c3-bfe9-6f49cefb703d` |
| `runtime.messages` | `message_id=assistant-msg-0c43991d-e0f8-268c-a0d2-6515ffca14e2`; `message_id=assistant-msg-55171435-eac3-57ed-6a5e-7d9b02cfd8f2` |
Prepared: ⁨2026-10-15T19:09:53Z⁩.

## Why this matters

Why this matters now: at 17:49Z today the main chat told Kelly the Green PR audit hit a mechanism wall — "the tools to check approvals, CI status, and file lists aren't in my read-only set — they require approval-gated calls, same as merging" — and asked her to choose between (1) approving a batch of tool calls, (2) loosening permissions, or (3) merging from the GitHub UI herself. That premise is wrong, and correcting it materially changes her decision. I read the GitHub connector doc today (/opt/hatch/connectors/github/CONNECTOR.md, "Call an operation" section): `call-read-tool` runs the reviewed read-only tools — explicitly including `get_pull_request_status`, `get_pull_request`, and `get_pull_request_files` — "under the connector's read permission" and rejects anything else; only `call-tool` (writes and new/unknown tools) "asks for fresh approval" on each call. So read-only PR inspection needs NO approval taps; only the merge itself does.

Selected for high priority at ⁨2026-10-15T19:12:02.744471+00:00⁩. Record created ⁨2026-10-16T02:29:41.431545123+00:00⁩; delivery is not yet confirmed.


**Delivery outcome (⁨2026-10-16T02:30:20.761077+00:00⁩):** Not sent. Queue state: `⁨suppressed⁩`.
Reason: `⁨revalidation_declined⁩`.
`⁨agent.message_mailbox.submission_id=b9ee050d-883e-78c3-bfe9-6f49cefb703d⁩` resolves the delivery transcript.
<!-- proactive-outcome:proactive_notifier:run:proactive_notification:phase-497803:high -->
