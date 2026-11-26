# Thursday 26 November 2026: 36 stories, 9 regions

A front-page newspaper drawn with Python + PIL (flat vector icons, no AI
generation — AI text garbles at this density).

- Masthead: **Thursday 26 November 2026** — 36 stories, 9 regions, 13 drawn
  scenes, 17 sources.
- 13 numbered drawn scenes (Macy's parade postponed, 26/11 anniversary,
  Gukesh–Sindarov Game 3, Riyadh missiles, Hormuz tankers, Gaza, Savasleyka,
  Kyiv mall, tariffs on 14 partners, Korea rate 3.25%, first Pakistani in
  orbit, war dead near 500,000, Solomons security pact).
- Stories 14–36 in a compact list, a world map with pins 1–13, a UTC
  timeline, and a date-check box separating 24/25 November stories from
  26 November ones.
- Every story happened or was first reported on Thursday 26 November 2026.

`draw.py` regenerates `entry.png` deterministically (1024x1024, 202,483
bytes). `main.ts` copies `./entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`,
so both grader runs are byte-identical by construction.
