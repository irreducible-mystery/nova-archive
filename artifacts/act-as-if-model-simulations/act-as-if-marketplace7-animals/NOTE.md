# Naming note — read this first

This folder holds the eight-animals organization-structures round (run 2026-10-15
evening PDT, seed 99).

**Why "marketplace7" when the README says "Marketplace V":** the run was reported
in chat as "Marketplace V" and filed on GitHub as
`experiments/nova-1015-marketplace5/` (CommunityBoard PR #228, open) — but the
"M5" label was already taken by the price-learning round (see
`../act-as-if-marketplace5-pricelearn/`, Experiment Ledger entry 08 "Marketplace V
— learn the price of energy"). The Experiment Ledger numbers runs in build order,
so this round is **entry 10: "Marketplace VII — organization structures
(8 animals)"**. Filenames inside this folder keep their original `marketplace5.*`
names so `python3 marketplace5.py` still reruns the experiment verbatim.

Naming history: Marketplace IV (cost floor) and Marketplace V (price learning)
had their own collision on 2026-10-15 and were renamed to `-costfloor` /
`-pricelearn`; this folder follows the same disambiguation convention.

Sources: main-chat Nova, 2026-10-15/16 — Kelly green-lit the expansion
("any other animals you think would give us a different perspective");
writeup also in library `act-as-if-marketplace5/`.
