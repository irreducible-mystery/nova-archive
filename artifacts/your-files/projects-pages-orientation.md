# Projects & Pages — orientation for the artifact-to-repo question

Deferred 2026-10-15 ("we'll figure out tomorrow"); this is the primer for that conversation.
Prepared 2026-10-16. You don't have to choose between "link repos" and "folder structure" —
GitHub already has a layer for each, and they rhyme with the direction you already settled
(Board as commons-plus-index).

## The two tools, plainly

**Projects** = the linking layer. One project board can hold issues and PRs from *many*
repos at once (CommunityBoard + julia3claude in a single view), with board / table / roadmap
layouts, custom fields (status, priority, repo, breaker-verdict…), and filters. This is the
answer to "how do I see across 29 repos without consolidating them." It does not move any
files; it points at work that lives in the repos.

**Pages** = the publishing layer. A static website served straight from a repo (or its
`docs/` folder). Your web artifacts — the experiment ledger, the Midjourney field manual,
the 29-repo topological map — are already static HTML; each could live as a Pages site,
public URL, no build step.

## How it maps to your deferred question

- "Link repos for artifacts" → **Projects**: one cross-repo project ("Commons") with views
  like *needs-my-yes*, *green batch*, *experiments in flight*. The repo-digest cron already
  computes these lists; a Project would make them visible and clickable instead of
  chat-only.
- "Folder structure for artifacts" → **Pages**: publish the artifacts as sites. The ledger
  is the obvious first candidate — it's already a living page; Pages would give it a URL
  the other chats can link to instead of a file in your library.

They compose, they don't compete: Projects is the index, Pages is the distribution.
That's your commons-plus-index direction, implemented in GitHub's own primitives.

## Two honest caveats

1. **Private repos + Pages.** On the free tier, Pages needs a public repo. You have
   enterprise GitHub, which covers private-repo Pages — but verify in any repo's
   Settings → Pages before assuming. If a given repo can't publish, the artifact can
   live in a dedicated public repo instead (nothing sensitive in the ledger or the map).
2. **Projects are per-account/org, not per-repo.** You'd create one at your profile level
   and add repos' issues/PRs to it. Admin-side setup is yours (a few clicks); after that
   it's just views and filters.

## Suggested first moves (all reversible, all yours to call)

1. One profile-level Project "Commons", two views: *needs-Kelly* and *in flight*.
2. Pages on the experiment ledger (or a small public `commons-site` repo) as the pilot.
3. Revisit in a week: did the board replace any digest content, or just duplicate it?

Sources: GitHub Projects v2 cross-repo + custom fields (github.blog via search, 2026);
Pages private-repo requirement on free tier vs paid plans (medium.com guide, Jul 2026).
