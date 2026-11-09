# Critic: Evidence (Cairo), round 1 (measurement seat)

Anchor: How Charts Lie (Cairo): every printed figure must be reproducible from its source; a drawing's marks must equal the data. I edited no site file. Instruments: check_floor.py, tools/measure.py --preset contrast, and node playwright scripts (Chromium 1243). Scratch scripts are in the session scratchpad, not in the site.

## Measurements

| # | Measurement | Result | Pass/Fail |
|---|---|---|---|
| 1 | Mobile Floor, 5 pages (360/390/430) | index, about, works, quotes, corrections: 12/12 hold at all three widths, PASS x5 | PASS |
| 2 | measure.py --preset contrast, 390 and 1280, 5 pages | n:0 on all 10 runs | PASS |
| 3 | Own contrast walk, light, index / quotes | 26 / 20 distinct pairs, min 5.04 / 5.57, 0 under threshold | PASS |
| 4 | Own contrast walk, dark, index / quotes | 26 / 20 distinct pairs, min 6.66 / 7.04, 0 under threshold | PASS |
| 5 | "28 books" (index.html:26, :32) vs works.json | 28 works | PASS |
| 6 | "1972 to 2023" (index.html:32) | min year 1972, max 2023 | PASS |
| 7 | "20 quotes" / "2 of the 20" | 20 quotes; 2 tier=sourced (index.html:41) | PASS |
| 8 | "2 circulate ... probably not his" | 2 tier=misattributed | PASS |
| 9 | Tier counts printed on chips (quotes.html:26) 2/10/6/2 | data: sourced 2, attributed 10, doubtful 6, misattributed 2 | PASS |
| 10 | Shelf: `rect.bk` count in svg.shelf | 28 = works; 25 columns = 25 distinct years; stack sizes (22x1, 3x2) are identical to the per-year counts from the data (1987, 2000, 2010 = 2) | PASS |
| 11 | Shelf: total `<rect>` in svg | 29 = 28 books + 1 plank-edge (not a book) | PASS (note) |
| 12 | Subject counts via chips: eco 6, race 9, theory 7, essays 5, edu 1 | page shows 6/9/7/5/1, data 6/9/7/5/1 | PASS |
| 13 | Quote chips shown vs data | 20 / 2 / 10 / 6 / 2, all equal data, "Showing n of N" text equals too | PASS |
| 14 | `lang`, one h1, `main`, skip link | en, 1, 1, present on 5/5 | PASS |
| 15 | Heading order | index 1,2,2,2,3,3,3,2; about 1,2,2,3x4; works 1,2,3x28; quotes 1,2,2; corrections 1,2,2; no level skipped | PASS |
| 16 | Alt text | 4 of 4 img have non-empty alt | PASS |
| 17 | Page weight incl. images (bytes) | index 336,284; works 138,188; about 29,348; quotes 25,049; corrections 15,586 | see F5 |
| 18 | Hero image: Thomas-Sowell.jpg | 301,441 B, 1280x800 natural, displayed 420x525 at 1280 vw (0.33x of natural width, 0.66x of it at 2x DPR) | FAIL (F5) |
| 19 | basic-economics.jpg | 111,769 B, 1536x1536 natural, displayed 120x120 (12.8x linear oversize, 6.4x at 2x DPR); 111 KB is 80% of works.html's 138 KB | FAIL (F5) |
| 20 | Keyboard, JS on: tab order | skip, brand, nav x5, chips in DOM order, then content links; outline solid 3px on every stop | PASS |
| 21 | Chips with Enter / Space | Enter on chip 3 gave "Showing 9 of 28"; Space on chip 2 gave "Showing 6 of 28"; :focus-visible true | PASS |
| 22 | JS disabled: all items visible | works 28/28, quotes 20/20 | PASS |
| 23 | JS disabled: chip group hidden | `hidden` attribute is set but computed `display:flex` and height 200px at 390 wide on both pages; the buttons are visible and do nothing; `#count` is empty | FAIL (F2) |
| 24 | Hash `#subject=race`, `#tier=doubtful` (fresh load) | 9 of 28 shown, "Race, culture and history" pressed; 6 of 20 shown, "Doubtful (6)" pressed | PASS |
| 25 | Hash with unknown value (`#subject=bogus`, `#tier=bogus`) | "Showing 0 of 28 books" / "0 of 20 quotes", no chip pressed, no way to see why | FAIL (F3) |
| 26 | Deep link works.html#w-15 / #w-27, JS on | hash is stripped to "" and scrollY 0 on every fresh load; target sits at top=2060 / 3460 px (1280 wide), 2340 / 3837 (390 wide) | FAIL (F1) |
| 27 | Same deep link, JS off | hash kept, scrollY 2041 at 1280 (target top 16), 2321 at 390 | PASS (so the JS causes it) |
| 28 | Page-level horizontal overflow, 360/390/430/1280, 5 pages | documentElement.scrollWidth = clientWidth in all 20 cases | PASS |
| 29 | `.shelfscroll` inner scroller | 325/355/395 px client vs 680 px scroll width at 360/390/430; 1045 = 1045 at 1280. It scrolls inside itself and adds 0 px to the page | PASS |

## Findings

1. **BLOCKER. Deep links from index to the works list are dead with JS on.** script.js ends with `apply(m ? m[1] : "")`; for an empty value `apply` runs `history.replaceState(null,"",location.pathname)`, which deletes `#w-15`. The browser's fragment scroll then does not happen. Measured on fresh loads of `works.html#w-15` and `#w-27`: hash "" and scrollY 0 at 1280 and 390 wide (target 2,060 to 3,837 px below the fold). index.html links `works.html#w-6`, `#w-15` and `#w-18` (the "Where to start" cards), so all three land at the top of a 28-item list. With JS off, the same links scroll correctly (scrollY 2041). Fix: call `replaceState` only when the user clicks a chip (or when the value differs from the current hash), and leave the hash alone when it is not a `subject=`/`tier=` key. If there is a non-filter hash on load, call `document.getElementById(id).scrollIntoView()` after `apply`.
2. **MAJOR. With JS off, the "hidden" filter group is rendered and inert.** `.chips{display:flex}` (styles.css:89) overrides the UA `[hidden]{display:none}`. Computed display is `flex`, height 200 px at 390 px wide on both pages, and the five or six buttons do nothing; `#count` is empty. The page's own premise, "the lists work without JS", is false for the chrome above them. It also means the `chips.hidden = false` line in script.js changes nothing on screen. Fix: add `.chips[hidden]{display:none}` (or set `hidden` only through CSS class `.js .chips`), and put `<html class="no-js">` swapped by a one-line head script.
3. **MINOR. An unknown or mistyped filter hash yields an empty list with no explanation.** `#subject=bogus` gives "Showing 0 of 28 books" and 0 items, with no chip pressed. `#subject=Race` (capital) is rejected by the `[a-z]+` pattern and silently shows all 28 and rewrites the URL. Fix: validate the value against the chip `data-*` values and fall back to All; no empty state is then reachable except by a real filter.
4. **MINOR. Hash-only chip state is not exposed to assistive tech before interaction.** The "All" chip is `class="on"` in the markup but gets `aria-pressed` only when JS runs; pressed state is correct after apply (verified), so this is only a markup-consistency note. Fix: none needed unless F2 is fixed by moving the chips into the no-JS markup; then render `aria-pressed="true"` statically.
5. **MAJOR (weight). Two images are 6x to 13x larger than displayed.** images/Thomas-Sowell.jpg is 301,441 B (90% of index.html's 336,284 B payload) at 1280x800 for a 420 px wide display; images/basic-economics.jpg is 111,769 B at 1536x1536 for 120 px (80% of works.html's 138,188 B), and it is the only image on that page, for one of 28 books. Fix: export the hero at 840 px wide (about 1/3 of the pixels; expect roughly 80 to 110 KB) with width/height kept for layout, and the cover at 240x240 (expect under 15 KB); or drop the cover. Index would fall from about 336 KB to about 140 KB; works from about 138 KB to about 40 KB.
6. **MINOR. The shelf's one non-book rect.** svg.shelf holds 29 `<rect>`: 28 books plus the plank edge. The ratio is correct (28 books for 28 works, per-year stack heights equal data), but a reader who counts rects gets 29. Fix: give the plank edge a `<line>`/`<path>` or a class that the print note names, so rect count equals 28 for anyone who inspects it.

Figures printed vs data: 9 of 9 reproduce exactly. Floor: 5 of 5 pages hold 12/12 at 3 widths. Contrast: 0 failing pairs in 4 mode-by-page runs and 10 preset runs. The failures are behavioural (F1, F2) and weight (F5).

Verdict: OBJECT (F1 is a BLOCKER: 3 of the page's 3 deep links are dead).
