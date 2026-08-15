"""
Neural Computation (MIT Press) archive scraper -> yearly PDFs
----------------------------------------------------------------
Pulls title, authors, and abstract for every paper in the journal
"Neural Computation" (ISSN 0899-7667) and writes one clean, nicely
typeset PDF per publication year (1989.pdf, 1990.pdf, ... ), with
proper paragraph wraparound on abstracts and a clean rule between
papers. No .txt files are produced.

WHY THIS DOESN'T SCRAPE MIT PRESS DIRECTLY:
direct.mit.edu (the journal's own site) actively blocks automated
access and its terms prohibit bulk/automated downloading. Instead,
this script uses OpenAlex (https://openalex.org), a free, open
bibliographic database (CC0-licensed metadata) built specifically
for this kind of bulk academic-metadata retrieval. It already has
Neural Computation indexed, including abstracts for most papers.

USAGE:
    pip install requests reportlab
    python neco_scraper.py

    Optional: edit EMAIL below to your own address. OpenAlex asks
    for this ("polite pool") so they can contact you if something
    about your usage needs attention -- it gets you faster, more
    reliable responses. It is not required.

OUTPUT:
    ./neural_computation_by_year/1989.pdf
    ./neural_computation_by_year/1990.pdf
    ...one PDF per year, each containing every paper published
    that year (all issues collapsed together, in page order) with
    title, authors, DOI, page range, and wrapped abstract text.
"""

import os
import time
import requests

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
)

# ----------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------
OPENALEX_SOURCE_ID = "S207023548"  # Neural Computation, MIT Press
OUTPUT_DIR = "neural_computation_by_year"
EMAIL = "your_email@example.com"   # optional but recommended, see above
START_YEAR = 1989
END_YEAR = 2026                    # bump this forward as new years appear
REQUEST_DELAY = 0.15                # seconds between API calls (be polite)
PER_PAGE = 200                      # OpenAlex max per page


# ----------------------------------------------------------------
# PDF STYLES
# ----------------------------------------------------------------
_base_styles = getSampleStyleSheet()

STYLE_YEAR_HEADER = ParagraphStyle(
    "YearHeader",
    parent=_base_styles["Title"],
    fontSize=22,
    spaceAfter=4,
)
STYLE_YEAR_SUB = ParagraphStyle(
    "YearSub",
    parent=_base_styles["Normal"],
    fontSize=10,
    textColor=colors.grey,
    spaceAfter=18,
)
STYLE_PAPER_TITLE = ParagraphStyle(
    "PaperTitle",
    parent=_base_styles["Heading2"],
    fontSize=13,
    leading=16,
    spaceAfter=4,
    textColor=colors.HexColor("#1a1a1a"),
)
STYLE_AUTHORS = ParagraphStyle(
    "Authors",
    parent=_base_styles["Normal"],
    fontSize=10,
    leading=13,
    textColor=colors.HexColor("#444444"),
    fontName="Helvetica-Oblique",
    spaceAfter=2,
)
STYLE_META = ParagraphStyle(
    "Meta",
    parent=_base_styles["Normal"],
    fontSize=8.5,
    leading=11,
    textColor=colors.HexColor("#888888"),
    spaceAfter=8,
)
STYLE_ABSTRACT = ParagraphStyle(
    "Abstract",
    parent=_base_styles["Normal"],
    fontSize=10,
    leading=14.5,
    alignment=TA_JUSTIFY,
    textColor=colors.HexColor("#222222"),
    spaceAfter=14,
)


def reconstruct_abstract(inverted_index):
    """OpenAlex stores abstracts as an inverted index (word -> [positions])
    rather than plain text, for copyright reasons. This rebuilds the
    original text from that structure."""
    if not inverted_index:
        return "No abstract available."
    position_map = {}
    for word, positions in inverted_index.items():
        for pos in positions:
            position_map[pos] = word
    if not position_map:
        return "No abstract available."
    max_pos = max(position_map.keys())
    words = [position_map.get(i, "") for i in range(max_pos + 1)]
    return " ".join(w for w in words if w)


def escape_xml(text):
    """ReportLab Paragraphs interpret a mini-XML markup, so raw text
    needs its special characters escaped before being wrapped in one."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def fetch_year(year, session):
    """Fetch all works published in `year` for the given journal,
    handling pagination via OpenAlex's cursor system."""
    works = []
    cursor = "*"
    while cursor:
        params = {
            "filter": (
                f"primary_location.source.id:{OPENALEX_SOURCE_ID},"
                f"publication_year:{year}"
            ),
            "per-page": PER_PAGE,
            "cursor": cursor,
            "select": "id,doi,title,authorships,publication_year,"
                      "abstract_inverted_index,biblio",
            "mailto": EMAIL,
        }
        resp = session.get(
            "https://api.openalex.org/works", params=params, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        works.extend(results)

        cursor = data.get("meta", {}).get("next_cursor")
        if not results:
            break
        time.sleep(REQUEST_DELAY)
    return works


def sort_key(work):
    """Sort papers within a year by their first page number where
    available, falling back to 0 (keeps issues in reading order)."""
    first_page = (work.get("biblio") or {}).get("first_page")
    try:
        return int(first_page)
    except (TypeError, ValueError):
        return 0


def build_year_pdf(year, works, out_path):
    doc = SimpleDocTemplate(
        out_path,
        pagesize=LETTER,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
        title=f"Neural Computation -- {year}",
    )

    story = []
    story.append(Paragraph(f"Neural Computation -- {year}", STYLE_YEAR_HEADER))
    story.append(Paragraph(f"{len(works)} article(s), all issues", STYLE_YEAR_SUB))

    for i, w in enumerate(works, 1):
        title = escape_xml(w.get("title") or "(untitled)")
        authors = ", ".join(
            a["author"]["display_name"]
            for a in w.get("authorships", [])
            if a.get("author") and a["author"].get("display_name")
        )
        authors = escape_xml(authors) if authors else "(authors unknown)"

        doi = w.get("doi") or "(no DOI)"
        biblio = w.get("biblio") or {}
        first_page = biblio.get("first_page")
        last_page = biblio.get("last_page")
        pages = f"pp. {first_page}-{last_page}" if first_page else None

        meta_bits = [escape_xml(doi)]
        if pages:
            meta_bits.append(escape_xml(pages))
        meta_line = "  |  ".join(meta_bits)

        abstract = escape_xml(reconstruct_abstract(w.get("abstract_inverted_index")))

        story.append(Paragraph(f"{i}. {title}", STYLE_PAPER_TITLE))
        story.append(Paragraph(authors, STYLE_AUTHORS))
        story.append(Paragraph(meta_line, STYLE_META))
        story.append(Paragraph(abstract, STYLE_ABSTRACT))

        # Clean separator between papers (skip after the last one)
        if i != len(works):
            story.append(
                HRFlowable(
                    width="100%",
                    thickness=0.6,
                    color=colors.HexColor("#cccccc"),
                    spaceBefore=2,
                    spaceAfter=18,
                )
            )

    doc.build(story)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    session = requests.Session()
    session.headers.update(
        {"User-Agent": f"neco-yearly-archiver/1.0 (mailto:{EMAIL})"}
    )

    for year in range(START_YEAR, END_YEAR + 1):
        print(f"Fetching {year}...")
        try:
            works = fetch_year(year, session)
        except requests.RequestException as e:
            print(f"  Failed for {year}: {e}")
            continue

        if not works:
            print(f"  No entries found for {year}, skipping PDF.")
            continue

        works.sort(key=sort_key)

        out_path = os.path.join(OUTPUT_DIR, f"{year}.pdf")
        build_year_pdf(year, works, out_path)
        print(f"  Wrote {len(works)} entries to {out_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()