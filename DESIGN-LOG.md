# DESIGN-LOG: Thomas Sowell appreciation site (redesign)

**Run.** DADA, Adaptive mode, Full run type (a redesign of a five-page site that had no design to preserve), **bounded to one panel round** at the owner's request ("lightish"). Look: the new design pack `study-ledger` (SolutionsAsService/dada-changes, `skills/dada/designpacks/`). Pages are generated from `data/works.json` and `data/quotes.json` by `scripts/build.py`; every number printed on a page is read from those files.

## R0. The inherited site, measured and read
A fixed footer covering the content; a contact form that posted nowhere; 18 quotations all presented as his with no source; 5 of them doubtful or misattributed on their face (one is the well-known Twain-type saying, one is Paul Farmer's); the same 3 quotes repeated on home and quotes; the works list a bare `<ul>`; 60% of the viewport taken by header at 390px; Arial throughout. Findings became the Frontier: (1) honesty about sources, (2) one memorable picture, (3) the Mobile Floor, (4) a real way to report errors.

## Decisions
**D1 Source is the subject.** The site's difference from every fan page: each quotation carries a mark for how well its source is known, as a rule style plus a word (solid, dashed, dotted, double), never colour alone. D2 **The shelf.** One book per work, one column per year, one shelf; the three "start here" books are red. The drawing and the text are generated from the same data. D3 **Paper, ink, one accent.** System serif, a heavy rule over each page, hard offset shadows, no blur. D4 **The contact form is replaced by Corrections**, which links to GitHub issues; `contact.html` redirects. D5 **Honest footer:** not affiliated; photographs' source and licence unrecorded; the MIT licence does not cover them or the quoted words.

## Panel R1 (3 seats, one agent per reference; verdicts in `panel/R1/`)
Krug (usability), Debord (claims check, no web access, judged from knowledge with stated confidence), Cairo (measurement). Not seated, for the bound: an inclusion seat (Mace/Holmes); named under Open.

| Seat(s): finding | Resolution |
|---|---|
| Cairo: deep links dead with JS on (`replaceState` stripped the hash; `works.html#w-15` landed at scroll 0) | ADAPT: script never rewrites a hash it does not own; verified at 1280 and 390, all three "Where to start" links land on their target |
| Cairo: chip group visible with JS off (`display:flex` beat `[hidden]`) | ADAPT: `.chips[hidden]{display:none}`; verified no-JS shows 28 works and no dead chips |
| Cairo: 301 KB hero image shown at 420px; 112 KB cover shown at 120px | ADAPT: 840px (64 KB) and 240px (9 KB) derivatives; originals kept |
| Cairo: unknown / capitalised hash handled badly | ADAPT: lower-cased and validated; unknown falls back to All |
| Krug: shelf unreadable on a phone (cropped in its own scroller, tiny, no cue) | ADAPT: scroller removed, whole shelf fits; a one-line key under it; link to the works page. Still small on a phone: see Open |
| Krug: three spine colours with no meaning (colour alone) | ADAPT: one colour; red now means the three "start here" books, said in the caption |
| Krug: quotes page puts the first quote ~950px down; legend and chips say the same four things | ADAPT: legend and filter are one control (the legend rows become the filter with JS); legend text shortened; first quote now sits about 520px down on a phone |
| Krug: "Widely attributed" does not say whether to use it | ADAPT: every tier now reads as an action ("Say attributed to him, not he said"; "Do not quote it as his"; "Do not attribute it to him") |
| Krug: lede hides the site's point; "2 of 20" leaves out 16 | ADAPT: lede now says every quotation is marked; caption says only 2 even name a book and none is checked |
| Krug: cards link only on title text; bare dot for repeated years; footer has no nav | ADAPT: whole card is the target; repeated years show in a lighter tone; footer nav added |
| Krug: quotes cannot be linked individually | DEFERRED: needs a permalink affordance; logged |
| Debord: honesty apparatus overclaims ("could not place it" implies a search that never happened; "quote him without quoting someone else" promises too much) | ADAPT: "No source known; not yet searched for"; lede says treat every mark as a lead, not a licence to quote |
| Debord: top tier is unverified but looks like an evidence hierarchy | ADAPT: tier 1 renamed "Book named, unchecked"; "Probably not his" renamed "Credited to someone else" (only for sayings on record as someone else's) |
| Debord: "same rules ... a racist today" and "Freedom has cost too much blood" over-ranked | ADAPT: both moved to "No source known" (counts now 2 / 8 / 8 / 2) |
| Debord: Twain-type and Farmer notes name no one; "Probably not his" overstated | ADAPT: notes name Josh Billings and Kidder's Mountains Beyond Mountains with "not checked" |
| Debord: corrections page promotes by wrong rule | ADAPT: any tier becomes "Book named" only with a book, edition and page or a dated original |
| Debord: "question under all of it" crowns one unchecked line | ADAPT: "One line that gets quoted often", still marked unchecked |
| Debord: lede phrase "and then what happens?" set like a quotation | ADAPT: removed |
| Debord: bio details (Cornell mostly 1960s, Amherst visiting, Howard omitted, "book most readers meet first", "engineered away") | ADAPT: all five reworded as proposed |
| Debord: photo alt asserts identity and date | PARTLY ADAPTED: alt now says "captioned as Thomas Sowell; date and source unknown"; photographs kept pending the owner's source (the remove-them option is the owner's call) |
| Debord: MIT licence does not cover photographs or quoted words | ADAPT: footer says so |
| Debord: "28 books" reads as a census | ADAPT: "A shelf of 28 books", "28 of his books", "a selection" in the title block |
| Debord: the "Corrections" nav item and exact counts perform an audit not done | OVERRULE: the page now says plainly that nothing has been checked against a page; the nav label is how a reader finds the way to help, and the counts are of marks, not of verified facts |

## Measured
Mobile Floor 12 of 12 at 360, 390 and 430px on all 5 pages, re-run after every change set. Contrast preset n:0 on all pages; Cairo's own contrast walk found no pair under 4.5:1 in light or dark (lowest 5.04:1 light, 6.66:1 dark). Page-level horizontal overflow 0 at 360, 390, 430 and 1280. All 9 printed figures equal the data; the shelf has exactly 28 book rects and per-year stack heights equal the data. Behaviour verified in a real browser: filters, deep links, hash fallbacks, no-JS.

## Stop test
S1 not met (no R2). S2 not met (round 1's ADAPTs were applied after the last round and judged only by measurement, not by the panel). S4 not run. **Reported as incomplete under the one-round bound.**

## Open
- Every quotation is unchecked against a printed page; no wording has been verified. The biography and the 28 years and titles are from general knowledge (Debord judged them high-confidence except the points fixed above).
- The shelf is small on a 390px phone (blocks about 10px wide); it reads as a picture, not as data, and the text beside it carries the numbers. A phone-specific layout (two rows of years) was not tried.
- Not shown on a real phone; one-handed reach and the shelf on a 667px device are unverified.
- No inclusion seat (Mace or Holmes) was seated; no keyboard-only walkthrough by a person.
- Photograph source and licence unknown (owner to supply).
- Quotes have no permalinks.

## Grade of round 1: B+ (recorded by the owner, 2026-11-09)
The site is added to the studio portfolio (guides group). The look is now the adopted dada design pack `study-ledger` 1.0.0 (grade B+). The previous version of the site is kept on the branch `legacy/pre-redesign` (commit 4c32af5). What stands between B+ and A is the Open list above, chiefly that no quotation has been checked against a printed page and that the shelf is small on a phone.
