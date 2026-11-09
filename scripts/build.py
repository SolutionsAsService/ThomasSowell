#!/usr/bin/env python3
"""Generate the site from data/*.json. Standard library only.

    python3 scripts/build.py           write index/about/works/quotes/corrections.html and the favicon
    python3 scripts/build.py --check   exit 1 if any generated file is stale

Every figure on a page (the number of books, the years, the count in each quote tier) is read from the data files,
so the drawing and the text cannot disagree.
"""
import html
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
e = lambda s: html.escape(str(s), quote=True)
W = json.loads((ROOT / "data" / "works.json").read_text(encoding="utf-8"))
Q = json.loads((ROOT / "data" / "quotes.json").read_text(encoding="utf-8"))
works, subjects = W["works"], {s["id"]: s for s in W["subjects"]}
quotes, tiers = Q["quotes"], {t["id"]: t for t in Q["tiers"]}
Y0, Y1 = min(w["year"] for w in works), max(w["year"] for w in works)
NB = len(works)
by_tier = Counter(q["tier"] for q in quotes)
START = set()
REPO = "https://github.com/SolutionsAsService/ThomasSowell"

NAV = [("index.html", "Home"), ("about.html", "About"), ("works.html", "Works"), ("quotes.html", "Quotes"), ("corrections.html", "Corrections")]

SHAPES = {
    "square": '<rect x="2" y="2" width="12" height="12"/>',
    "circle": '<circle cx="8" cy="8" r="6.5"/>',
    "diamond": '<path d="M8 1 15 8 8 15 1 8z"/>',
    "triangle": '<path d="M8 1.5 15 14.5H1z"/>',
    "bar": '<rect x="1" y="5.5" width="14" height="5"/>',
}


def glyph(shape):
    return f'<svg class="glyph" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true" focusable="false">{SHAPES[shape]}</svg>'


def shelf():
    """Books per year as stacks of flat books on one shelf: the bibliography as a picture, one book per work."""
    per = Counter(w["year"] for w in works)
    span = Y1 - Y0
    W_, H_, pad = 1000, 142, 14
    step = (W_ - 2 * pad - 40) / span
    bw, bh, gap = step * 0.86, 32, 5
    out = [f'<svg class="shelf" viewBox="0 0 {W_} {H_}" aria-hidden="true" focusable="false" preserveAspectRatio="xMidYMax meet">']
    base = H_ - 20
    out.append(f'<line x1="0" y1="{base + 8}" x2="{W_}" y2="{base + 8}" class="plank"/>')
    out.append(f'<rect x="0" y="{base + 10}" width="{W_}" height="6" class="plank-edge"/>')
    starters = Counter(w["year"] for w in works if w.get("blurb"))
    for y in sorted(per):
        cx = pad + 20 + (y - Y0) * step
        for i in range(per[y]):
            yy = base - (i + 1) * (bh + gap) + gap
            shade = "b" if i < starters.get(y, 0) else "a"
            out.append(f'<rect x="{cx - bw / 2:.1f}" y="{yy:.1f}" width="{bw:.1f}" height="{bh}" rx="2" class="bk bk-{shade}"/>')
            out.append(f'<path d="M{cx - bw / 2 + 3:.1f} {yy + 8:.1f}H{cx + bw / 2 - 3:.1f}M{cx - bw / 2 + 3:.1f} {yy + bh - 8:.1f}H{cx + bw / 2 - 3:.1f}" class="bk-l"/>')
    out.append("</svg>")
    return "".join(out)


def head(title, desc, page):
    nav = "".join(f'<a href="{h}"' + (' aria-current="page"' if h == page else "") + f">{t}</a>" for h, t in NAV)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
<header class="mast">
  <a class="wordmark" href="index.html">Thomas Sowell<span> an appreciation</span></a>
  <nav aria-label="Pages">{nav}</nav>
</header>
<main id="main">
'''


def foot(script=False):
    return f'''</main>
<footer class="foot">
  <p><strong>A fan-made appreciation site.</strong> It is not affiliated with Thomas Sowell or the Hoover Institution. Every quotation is marked with how well its source is known; if one is wrong, <a href="corrections.html">tell us</a>.</p>
  <nav class="footnav" aria-label="Pages">{"".join(f'<a href="{h}">{t}</a>' for h, t in NAV)}</nav>
  <p class="small">Photographs are the ones the original repository carried; their source and licence were not recorded. If you hold the rights and want one changed or removed, open an <a href="{REPO}/issues">issue</a>. The site\'s code and text are MIT-licensed; the photographs and the quoted words are not covered by that licence. Site by SolutionsAsService.</p>
</footer>
{'<script src="script.js"></script>' if script else ''}
</body>
</html>
'''


def quote_block(q):
    t = tiers[q["tier"]]
    src = f'<span class="src">{e(q["source"])}</span>' if q.get("source") else ""
    note = f'<p class="qnote">{e(q["note"])}</p>' if q.get("note") else ""
    return (f'<li class="q tier-{q["tier"]}" data-tier="{q["tier"]}"><blockquote><p>{e(q["text"])}</p></blockquote>'
            f'<p class="qmeta"><span class="tier-tag tier-{q["tier"]}"><i aria-hidden="true"></i>{e(t["name"])}</span>{src}</p>{note}</li>')


def index():
    cards = "".join(
        f'<li class="card"><p class="yr">{w["year"]}</p><h3><a href="works.html#w-{i}">{e(w["title"])}</a></h3><p>{e(w["blurb"])}</p>'
        f'<p class="tag">{glyph(subjects[w["subject"]]["shape"])}{e(subjects[w["subject"]]["name"])}</p></li>'
        for i, w in enumerate(works) if w.get("blurb"))
    pull = quotes[0]
    decades = "".join(f"<span>{d}s</span>" for d in range((Y0 // 10) * 10, Y1 + 1, 10))
    return head("Thomas Sowell: an appreciation", "Economist, historian and writer. His books, his ideas and the sayings attributed to him, each marked with how well it is sourced.", "index.html") + f'''
<section class="hero" aria-labelledby="h1">
  <div class="hero-copy">
    <p class="kicker">Economist · historian · writer</p>
    <h1 id="h1">Thomas Sowell</h1>
    <p class="lede">A reader's guide to his books, his ideas and the sayings attributed to him, with every quotation marked for how far its source can be trusted.</p>
    <p class="cta"><a class="btn" href="works.html">Browse the books</a><a class="btn ghost" href="quotes.html">Read the quotes</a></p>
  </div>
  <figure class="portrait"><img src="images/Thomas-Sowell-840.jpg" width="840" height="525" alt="Photograph captioned as Thomas Sowell, in a tweed jacket and striped tie; date and source unknown" fetchpriority="high"></figure>
</section>

<section class="shelfband" aria-labelledby="h-shelf">
  <h2 id="h-shelf" class="label">A shelf of {NB} books, {Y0} to {Y1}</h2>
  {shelf()}<div class="axis" aria-hidden="true">{decades}</div>
  <p class="small">Each block is one book and each column is a year. The three red blocks are the books in “Where to start” below. A selection, not a complete bibliography.</p>
  <p><a class="more" href="works.html">See all {NB} on the works page</a></p>
</section>

<section class="pull" aria-labelledby="h-pull">
  <h2 id="h-pull" class="label">One line that gets quoted often</h2>
  <blockquote><p>{e(pull["text"])}</p></blockquote>
  <p class="qmeta"><span class="tier-tag tier-sourced"><i aria-hidden="true"></i>{e(tiers["sourced"]["name"])}</span><span class="src">{e(pull["source"])}</span></p>
  <p class="small">Only {by_tier["sourced"]} of the {len(quotes)} sayings on this site even name a book, and none has been checked against a page yet. <a class="more" href="quotes.html">See how each one is marked</a></p>
</section>

<section aria-labelledby="h-start">
  <h2 id="h-start" class="sech">Where to start</h2>
  <ul class="cards">{cards}</ul>
</section>

<section class="two" aria-labelledby="h-who">
  <div><h2 id="h-who" class="sech">Who he is</h2>
  <p>Born in North Carolina in 1930 and raised in Harlem, he left school at 17, served in the Marine Corps, and went on to a Harvard degree in economics and a doctorate from the University of Chicago. He taught at several universities, then spent decades as a senior fellow at the Hoover Institution.</p>
  <p><a class="more" href="about.html">The short biography and the ideas he returns to</a></p></div>
  <figure class="young"><img src="images/thomas-sowell-young.jpg" width="300" height="250" alt="A younger man at a television panel, captioned as Thomas Sowell; date and source unknown" loading="lazy"></figure>
</section>
''' + foot()


def about():
    life = [("1930", "Born in Gastonia, North Carolina; grows up in Harlem, New York."),
            ("1950s", "Leaves school at 17, serves in the U.S. Marine Corps, studies at Howard, then at Harvard (A.B. 1958) and Columbia (A.M. 1959)."),
            ("1968", "Ph.D. in economics, University of Chicago."),
            ("1960s–70s", "Teaches at Cornell, Brandeis, UCLA and, as a visitor, Amherst, among other posts; publishes Say's Law (1972) and Race and Economics (1975)."),
            ("1980", "Joins the Hoover Institution, Stanford University, as a senior fellow."),
            ("2000", "Basic Economics, a book written for the general reader."),
            ("2002", "Awarded the National Humanities Medal.")]
    li = "".join(f'<li><p class="yr">{y}</p><p>{e(t)}</p></li>' for y, t in life)
    ideas = [("There are no solutions, only trade-offs.", "Everything costs something. A good question about any policy is what it costs, who pays, and what else that money or time could have done."),
             ("Incentives, not intentions.", "He judges a policy by what people actually do under it, not by what its authors hoped they would do."),
             ("Two visions.", "In A Conflict of Visions he argues that many political fights come from two different pictures of human nature, one that treats human limits as lasting and works through trade-offs and accumulated social processes, and one that holds that wise design can overcome them."),
             ("Look at the evidence across places and times.", "His books on race, culture and migration compare many countries and centuries before they draw a conclusion.")]
    ids = "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in ideas)
    return head("About Thomas Sowell", "A short biography of Thomas Sowell and the four ideas he returns to most.", "about.html") + f'''
<section class="page-head"><p class="kicker">About</p><h1>A short life, a long shelf</h1>
<p class="lede">The facts below are written from general knowledge and have not yet been checked line by line against sources. See <a href="corrections.html">Corrections</a>.</p></section>
<section class="two" aria-labelledby="h-life">
  <div><h2 id="h-life" class="sech">Life</h2><ol class="timeline">{li}</ol></div>
  <figure class="young"><img src="images/thomas-sowell-young.jpg" width="300" height="250" alt="A younger man at a television panel, captioned as Thomas Sowell; date and source unknown" loading="lazy"></figure>
</section>
<section aria-labelledby="h-ideas"><h2 id="h-ideas" class="sech">Four ideas he returns to</h2><ul class="ideas">{ids}</ul>
<p class="small">These are summaries in our words, not quotations. Where a line is his, it is on the <a href="quotes.html">quotes page</a> with its sourcing.</p></section>
''' + foot()


def works_page():
    chips = '<button type="button" class="chip on" data-subject="">All</button>' + "".join(
        f'<button type="button" class="chip" data-subject="{s["id"]}">{glyph(s["shape"])}{e(s["name"])}</button>' for s in W["subjects"])
    rows = []
    last = None
    for i, w in enumerate(works):
        s = subjects[w["subject"]]
        yr = f'<p class="yr{" same" if w["year"] == last else ""}">{w["year"]}</p>'
        last = w["year"]
        blurb = f'<p class="blurb">{e(w["blurb"])}</p>' if w.get("blurb") else ""
        cover = '<img class="cover" src="images/basic-economics-240.jpg" width="120" height="120" alt="Cover of Basic Economics" loading="lazy">' if w["title"] == "Basic Economics" else ""
        rows.append(f'<li class="work" id="w-{i}" data-subject="{w["subject"]}">{yr}<div class="wb"><h3>{e(w["title"])}</h3>{blurb}<p class="tag">{glyph(s["shape"])}{e(s["name"])}</p></div>{cover}</li>')
    return head("Works by Thomas Sowell", f"{NB} of Thomas Sowell's books by year and subject.", "works.html") + f'''
<section class="page-head"><p class="kicker">Works</p><h1>{NB} of his books, {Y0} to {Y1}</h1>
<p class="lede">{e(W["note"])} Listed by year; filter by subject.</p></section>
<section aria-labelledby="h-list">
  <h2 id="h-list" class="sr">The list</h2>
  <div class="chips" role="group" aria-label="Filter by subject" id="subject-chips" hidden>{chips}</div>
  <p class="count" id="count" role="status" aria-live="polite"></p>
  <ol class="works">{"".join(rows)}</ol>
</section>
''' + foot(True)


def quotes_page():
    legend = "".join(f'<li class="tier-{t["id"]}" data-tier="{t["id"]}"><span class="tier-tag tier-{t["id"]}"><i aria-hidden="true"></i>{e(t["name"])} <b class="n">({by_tier[t["id"]]})</b></span><span class="act">{e(t["blurb"])}</span></li>' for t in Q["tiers"])
    items = "".join(quote_block(q) for q in sorted(quotes, key=lambda q: list(tiers).index(q["tier"])))
    return head("Quotes attributed to Thomas Sowell", f"{len(quotes)} sayings attributed to Thomas Sowell, each marked with how well its source is known.", "quotes.html") + f'''
<section class="page-head"><p class="kicker">Quotes</p><h1>{len(quotes)} sayings attributed to him</h1>
<p class="lede">Each carries a mark for how well its source is known. None has yet been checked against a printed page, so treat every mark as a lead, not a licence to quote. Listed best-sourced first.</p></section>
<section aria-labelledby="h-legend" class="tiers"><h2 id="h-legend" class="sech">The four marks</h2>
<ul class="legend" id="tier-legend">{legend}</ul>
<p class="count" id="count" role="status" aria-live="polite"></p></section>
<section aria-labelledby="h-q">
  <h2 id="h-q" class="sr">The quotes</h2>
  <ul class="quotes">{items}</ul>
</section>
''' + foot(True)


def corrections():
    return head("Corrections", "How to report a mistake or add a source on this appreciation site of Thomas Sowell.", "corrections.html") + f'''
<section class="page-head"><p class="kicker">Corrections</p><h1>Found a mistake? Add a source?</h1>
<p class="lede">This is a fan site and it will have errors. The most useful thing you can send is a citation.</p></section>
<section class="two">
  <div>
    <h2 class="sech">What helps most</h2>
    <ul class="plain">
      <li><strong>A quotation:</strong> the book, edition and page, or a dated column or interview with a link.</li>
      <li><strong>A misattribution:</strong> where the saying really comes from.</li>
      <li><strong>A fact or a date:</strong> the source that shows the right one.</li>
      <li><strong>A photograph:</strong> its source and licence, or a request to remove it.</li>
    </ul>
    <p><a class="btn" href="{REPO}/issues/new">Open an issue on GitHub</a></p>
    <p class="small">There is no form on this page because there is nowhere for it to post. GitHub issues are public and answered in the open.</p>
  </div>
  <div>
    <h2 class="sech">How a quote moves up</h2>
    <ol class="plain">
      <li>Any quote becomes <strong>Book named</strong> only when a book, edition and page, or a dated original, shows the words. At present none has been checked.</li>
      <li><strong>Widely attributed</strong> means popular, not checked. We never promote a quote because it is popular.</li>
      <li><strong>Credited to someone else</strong> stays until a source in his own words is shown.</li>
    </ol>
  </div>
</section>
''' + foot()


FAV = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#1c1915"/><rect x="6" y="19" width="20" height="5" rx="1" fill="#f5efe2"/><rect x="8" y="13" width="17" height="5" rx="1" fill="#c9674c"/><rect x="7" y="7" width="18" height="5" rx="1" fill="#f5efe2"/></svg>'
OUT = {"index.html": index(), "about.html": about(), "works.html": works_page(), "quotes.html": quotes_page(),
       "corrections.html": corrections(), "favicon.svg": FAV,
       "contact.html": '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=corrections.html"><link rel="canonical" href="corrections.html"><title>Moved</title><p>The contact page is now <a href="corrections.html">Corrections</a>.</p>\n'}


def main():
    check = "--check" in sys.argv
    stale = []
    for name, text in OUT.items():
        p = ROOT / name
        if not p.exists() or p.read_text(encoding="utf-8") != text:
            stale.append(name)
            if not check:
                p.write_text(text, encoding="utf-8")
    if check and stale:
        print("stale:", ", ".join(stale))
        sys.exit(1)
    print("ok" if check else f"written {len(OUT)} files; {NB} books {Y0}-{Y1}; quotes by tier {dict(by_tier)}")


main()
