# Critic: Usability (Krug), round 1

Anchor: Don't Make Me Think (Steve Krug): the five-second test, "it doesn't matter how many times I have to click as long as each click is mindless", and "get rid of half the words". Evidence: the screenshots in shots/ and index.html, quotes.html, works.html, corrections.html, styles.css, script.js. I changed no site file.

## Verdict

OBJECT, mildly. The home page passes my five-second test better than most fan sites. On the phone first screen you can read "Thomas Sowell", a lede saying "a reader's guide to the books, the ideas and the sayings, with the sourcing shown", and two big buttons you can actually tap. The quotes page earns its keep: the tier mark is a rule plus a word, the legend sits above the list, and the list is sorted best-sourced first. Two things stop it from passing outright. First, the shelf, the page's signature drawing, is the one piece that makes me decode. On a phone it is half off-screen, about 22px tall per book, with three book colours and no key, and nothing tells me it scrolls or what it is for. Second, the quotes page makes a reader who only wants the safe ones scroll past a full screen of explanation, then reach a "trustworthy" tier of two quotes, each still marked "Edition and page not yet checked". There are no BLOCKERs. I disagree with the brief on one point: "drawn as a rule style plus a word, never colour alone" is honoured on the quotes but quietly broken on the shelf (finding 2).

## Findings

1. **MAJOR. The shelf drawing is not self-explaining on a phone, and half of it is out of sight.**
   - Evidence: index.html, phone (390px). `.shelfscroll .shelf { min-width: 680px }` sits inside a box about 342px wide, so the drawing is cropped. The screenshot shows the axis ending at "1990s", and the 2000s to 2020s books (about 12 of 28) are off-screen. Books render about 11 x 22px with no titles, and the SVG is `aria-hidden`. The only explanation is a 13px uppercase label, "28 books, 1972 to 2023: one book per work, stacked by year". The label itself starts at about y=850 on a 390x~844 first screen, so the drawing is below the fold. There is no arrow, fade or peek to say it scrolls, and a reader who does swipe will take it for a rigged carousel.
   - Change: (a) Fit the whole shelf into 342px, with fewer and fatter books if needed, or split it into two rows (1972-1996, 1997-2023). Do not hide half of it behind a swipe. (b) Put one plain sentence above it, such as "Each spine is one book; taller stacks are the same year." (c) Add a visible cue to what is clickable: either make each spine a link to its row on works.html (`#w-N`, which already exist) or say outright that it is only a picture. Right now it looks tappable and is not.

2. **MAJOR. The shelf uses three spine colours (ink, oxblood, grey) with no legend, which is colour alone doing a job.**
   - Evidence: `bk-a`, `bk-b` and `bk-c` fills in styles.css, and the three hues in the shelf in both screenshots. The page's own rule is "never colour alone". A reader assumes the colours mean something (subject?) and goes looking for a key that is not there.
   - Change: If the colours encode subject, add a four-glyph key that reuses the subject glyphs already on the cards (diamond, square, circle, triangle, bar), and draw those glyphs on the spines. If they encode nothing, make all spines one colour and let the accent highlight only the three "Where to start" books, which gives the shelf a purpose.

3. **MAJOR. The quotes page puts the explanation before the thing the reader came for, on one column.**
   - Evidence: quotes.html, phone. The first quote starts at roughly y=950 (kicker, h1, 3-line lede, "How to read the marks" with four rows, then three rows of filter chips, then "Showing 20 of 20"). It is the same 4-row legend plus filter chips again, each carrying the same four tier names. On desktop the same stack puts the first quote at about 860px. The chips repeat the legend's four words but sit below it, so a reader meets each tier name twice before reading any quote.
   - Change: Merge the legend and the chips into one control: each chip carries its one-line meaning, or the legend rows become the filter buttons. Put the first quote on the first phone screen, with the legend one tap away or below the lede in two lines. Cut the lede to one sentence ("Each saying is marked for how well its source is known.").

4. **MAJOR. "Can I trust this?" is answered only by a label I must interpret.**
   - Evidence: quotes.html. The legend says "Widely attributed" means "Printed everywhere as his; we have not yet checked the primary source." That covers 10 of 20 quotes, the biggest tier. A hurried reader cannot tell whether it is safe to quote. The top tier has two quotes, each footnoted "Edition and page not yet checked". So the page's best answer to "which quotes can I use?" is "two, with a caveat". Also nothing says the list runs best-sourced to least, so the order carries meaning the reader has to infer.
   - Change: (a) Add a line under the h1: "Listed from best sourced to least." (b) In the legend, say what to do with each tier in the reader's terms: "Safe to cite with the book named", "Quote it as 'attributed to'", "Don't quote", "Don't attribute". (c) Merge the "Source named" footnote into the legend once, rather than printing the same note under each of the two quotes.

5. **MINOR. The home page's "who is this for / what's special" is half there.**
   - Evidence: index.html, phone and desktop first screens. The lede says what the site is. The differentiator (the tier marks) only appears below the shelf, at about y=1750 (phone). The first button is "Browse the 28 books" and the second is "Read the quotes", but the quotes page is the distinctive product and the books button is the lead. That is a defensible choice for a first-time visitor who has not heard of the tier system, so I won't make this a MAJOR. But the 5-second test would give a visitor "a Sowell site" rather than "a Sowell site that tells me which quotes are real".
   - Change: Tighten the lede to "A reader's guide to Thomas Sowell's books, ideas and sayings, with every quotation marked for how well its source is known." Then put the sourced pull-quote and its tag directly under the buttons on phone, ahead of the shelf, since that is the page's real proof.

6. **MINOR. The home pull-quote caption makes me do arithmetic.**
   - Evidence: index.html: "2 of the 20 quotes on this site name a book; 2 circulate under his name and are probably not his." The other 16 are unaccounted for.
   - Change: Replace it with the full split in one line: "Of 20 sayings: 2 name a book, 10 are widely attributed, 6 doubtful, 2 probably not his." Or drop the sentence and keep the link.

7. **MINOR. Small tap targets and one-handed reach on the home page.**
   - Evidence: index.html, phone. The nav is at the top (the hardest place for a thumb) and wraps to five 44px-high links, which is acceptable. The "Where to start" cards link only on the title text (`h3 a`), about 24px high, though the whole card looks like a button. The footer links ("tell us", "issue") sit in 15px body text.
   - Change: Make the whole card the link target (stretched `::after` on the title link). Keep the primary buttons where they are: the two stacked buttons at roughly y=390-450 are in the comfortable thumb zone.

8. **MINOR. The works page's dot where the year should be.**
   - Evidence: works.html, phone. Three rows (Compassion Versus Guilt, A Personal Odyssey, Dismantling America) show a tiny dot in the year column. It is a ditto for "same year as the row above", but a reader meeting it cold takes it for a missing year. This also matters for the shelf's "stacked by year" claim, which depends on the same-year pairs. In index.html the home page says "the full list, by subject, is on the works page", but the works page is ordered by year with a subject filter.
   - Change: Print the year on every row (it is only four characters). Reword the home line to "the full list, by year, with a subject filter".

9. **MINOR. Navigation and dead ends.**
   - Evidence: all pages have the same five-link top nav and the footer repeats the disclaimer, but the footer has no nav links. On quotes.html phone (5100px tall) you end at the footer with nothing but the "tell us" link, no back-to-top and no way on. corrections.html ends in a single GitHub button, and corrections.html says "There is no form on this page because there is nowhere for it to post", which is honest but means a fan with no GitHub account cannot report anything. contact.html is a meta-refresh redirect, which is fine. Individual quotes have no link of their own, so I cannot send someone "this one is doubtful".
   - Change: Add the five nav links to the footer, or a "Back to top" link at least. Give each quote an `id` and a visible "link" affordance so the Doubtful ones can be pointed at. On corrections, offer a second route (a `mailto:` link) next to GitHub.

10. **MINOR (premise, not defect). "Corrections" as a top-level nav item.**
    - Evidence: five nav items on a 390px phone, with the fifth ("Corrections") ending about 30px from the edge on the works page, one font-size change from wrapping.
    - Change: Keep it (it is part of the site's honesty promise) but be ready to wrap or shorten it to "Fix a quote" if the nav breaks on a 360px phone.

## What needs a real phone

- Whether the shelf swipe works at all, and whether it fights vertical page scroll (`overscroll-behavior-x: contain` plus `overflow-x: auto` on a 342px strip). Screenshots cannot show scroll-chaining or whether iOS shows a scroll hint.
- Whether the 11 x 22px spines are legible and distinguishable (the three colours, the two lines on each spine) in sunlight and on a small screen. The screenshot is a downscaled capture.
- Actual first-screen height: I assumed about 844px (iPhone 14); a 667px device cuts the second button and the portrait.
- Thumb reach: the nav at the top, the quote filter chips mid-page (y about 840 on phone), and the card tap targets.
- Whether the tier rules (a 3-4px solid, dashed, dotted or double line at the left of each quote) are distinguishable at arm's length. At screenshot scale the dashed and dotted rules are readable, but I cannot judge them at real size.
- The `fetchpriority="high"` 1280x800 hero JPEG over a cellular connection, since I could not time it.
- The filter chips: whether they wrap to three rows on a narrow phone (visible in the screenshot) and whether the hash state (`#tier=doubtful`) survives back and forward navigation.
