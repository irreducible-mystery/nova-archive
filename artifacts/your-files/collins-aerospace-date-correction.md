# Collins Aerospace MUSE — date correction (resolved 2026-11-10)

## Verdict
**19 September 2025 — not 2026.** The Collins Aerospace MUSE airport incident falls
*outside* the November 2025 – November 2026 window of the Infrastructure Hacks report.
It should be moved from an in-window incident to a precursor, alongside Shai-Hulud
(Sep 2025) and Salesloft/Drift (Aug 2025), which the report already treats that way.

## What was unresolved
The report (`~/workspace/research_notes/infrastructure-hacks-last-year-20261110-0254/report.md`,
§4a and "Could not verify") said: Infosecurity Magazine dates its NCA-arrest/HardBit
article 25 Sep 2025, while several 2026 roundups date the MUSE incident 19 Sep 2026,
and told the reader not to cite a year without resolving it against the RTX 8-K /
ENISA primary release. The page "Infrastructure Hacks — Last Year"
(slug `infrastructure-hacks-last-year`, delivered ~19:02 PST on 2026-11-09) carries the
same open question.

## How it was resolved (checked 2026-11-10, ~16:06–16:07 UTC)
Primary / contemporaneous sources, all 2025:

- **RTX SEC Form 8-K, quoted verbatim in multiple reports:** "On September 19, 2025,
  RTX Corporation … became aware of a product cyber security incident involving
  ransomware on systems that support its Multi-User System Environment ('MUSE')
  passenger processing software."
  - https://techcrunch.com/2025/09/24/uk-police-arrest-man-linked-to-ransomware-attack-that-caused-airport-disruptions-in-europe/
  - https://brandefense.io/security-news/airport-check-in-outage-one-supplier-many-airports/
- **TechCrunch, published 2025-09-24:** NCA arrest that week, disruption "since the
  weekend", RTX 8-K filed that Wednesday.
- **UK NCSC statement 20 September 2025; NCA arrest announced 24 September 2025.**
- **European Parliament written question E-003667/2025, submitted 22.9.2025:**
  "Since 19 September 2025, a cyberattack on check-in and boarding systems provider
  Collins Aerospace has forced airports such as Brussels and Berlin to operate manually…"
  - https://www.europarl.europa.eu/RegData/questions/ecrites/2025/003667/P10_QE(2025)003667_EN.pdf

Why the 2026 roundups got it wrong: ENISA's *Threat Landscape 2026*, published
September 2026, lists the September 2025 Collins hack — roundups appear to have taken
the publication/listing year for the incident year.

## What still stays unresolved (do NOT overclaim)
Attribution is still conflicting, and the date fix does not settle it:
- ENISA Threat Landscape 2026 lists it as a cyberattack by the **Everest Group**,
  via unauthorised FTP access, with exfiltration of 1.5m+ passenger records and
  3,637 airline employee records (per Brandefense's summary of ENISA).
- Security researchers linked it to **HardBit** ransomware (Kevin Beaumont) — unconfirmed.
- Everest itself claimed the breach but **denies any ransomware / encryption**,
  alleging Collins shut its own servers down — a claim, not a finding.
- The NCA arrest (man in his 40s, West Sussex, 24 Sep 2025, released on conditional
  bail) has no confirmed affiliation.

## Exact edits needed
In `report.md`:
1. Summary table, row 7: change "19–22 Sep — year disputed, 2025 vs 2026" to
   "19 Sep 2025 — OUTSIDE the window; precursor, not an in-window incident".
2. §4a heading/body: date it 19 September 2025, note it predates the window by
   ~6 weeks, and keep it as a precursor note rather than incident #7.
3. Scope note (§6 / Summary): incident count becomes **10 in-window incidents
   + Collins as a precursor** (was 11 in-window). The four confirmed physical-outage
   cases are unchanged (Poland, UK generator, US water, France refrigeration) —
   Collins was only ever a transport *service* outage (manual check-in, ≥217 flights
   cancelled), so that tally does not move.
4. "Could not verify" section: delete the Collins date bullet; replace with a
   one-line resolved note citing the RTX 8-K quote above, and keep the HardBit /
   Everest attribution conflict as still open.
5. Recovery detail worth adding (from Berlin Airport updates, via Brandefense):
   check-in still largely manual 24 Sep 2025; Collins aimed to restore by 5 Oct 2025,
   with security tests then step-by-step airline reconnection.

On the page (`infrastructure-hacks-last-year`): apply the same move — Collins out of
the in-window list / into a precursor note, count 11 → 10 + precursor, and remove the
disputed-date open question, replacing it with the resolved 2025 date and the
still-open attribution conflict.

## Decision for Kelly
None needed on the facts — the date is settled by the 8-K. The only choice is
whether to apply the edits to the report and the page (recommended: yes, it's a
one-line move, and leaving a known-wrong year on a page she may share is worse
than fixing it).
