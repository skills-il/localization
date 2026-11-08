# Print-shop handoff

Every figure below belongs to the shop that published it. The user's own shop spec always wins.

## Questions to ask the shop before the final export

1. Trim size, and whether they print the size you chose without a surcharge.
2. Bleed for the interior (only if something reaches the edge) and for the cover.
3. Minimum inner (spine) margin for the page count and binding.
4. Whether the page count must divide by a fixed number for their production method.
5. Interior paper type and weight, and its thickness per leaf (caliper) for the spine.
6. Whether they require PDF/X, CMYK images, or a specific image resolution.
7. Their cover template or layout (פריסה), especially for hardcover.
8. A proof copy before the full run.

## Published figures, per shop

| Topic | Figure | Source |
|---|---|---|
| Most common size | A5, 14.8 x 21 cm | PrintaBook, https://printabook.co.il/size/ |
| Standard sizes | A4, A5, 17 x 24 cm ("חצי שמינית") | Dfus Eichut, https://dfus.co.il/page-size-and-layout/ |
| Margins | 2 cm all round; with a running head 2.8 cm top, 2.2 cm bottom | Dfus Eichut, same page |
| Margins | at least 1.5 cm | PrintaBook, https://printabook.co.il/blog/book-formatting-guide/ |
| Bleed | 3 mm on each side, 300 DPI, interior and cover as two PDFs | Armon Rama, https://www.armonrama.co.il/מוצרים/הדפסת-ספרים-בכמויות-קטנות/ |
| Separate files | interior pages in one PDF, cover in another | Dfus Seder Tzalam, https://sdar.co.il/books-printing/ |
| Never Word | the shop receives a PDF, never a Word file | Dfus Eichut, https://dfus.co.il/products-pages/books-printing/ |
| Spine | leaves times sheet thickness; a leaf is 2 pages; 80 g uncoated paper is listed at 0.1 mm | Meiri, https://www.meiri-pr.com/blank-rbnaz |

Bleed and safety margin are different things. Bleed extends BEYOND the trim edge so a photo
that runs to the edge has no white strip after cutting. The safety margin is INSIDE the trim,
and text must stay inside it. Some shop FAQs blur the two; use the shop's spec line.

## Spine worked example

A 300-page A5 book on 80 g uncoated paper at 0.1 mm per leaf:
300 pages / 2 = 150 leaves, 150 x 0.1 mm = 15 mm. Run `scripts/cover_size.py` with the shop's
actual caliper, and measure the spine on the proof copy before the full run.

## PDF standards

Typst exports PDF 1.4 to 2.0, PDF/A and PDF/UA. It does not export PDF/X. If the shop requires
PDF/X, the shop's preflight or a PDF tool converts the file; say this to the shop rather than
labelling the file PDF/X.
