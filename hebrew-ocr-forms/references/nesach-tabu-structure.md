# Nesach Tabu Structure -- Parsing a Land-Registry Extract into a Spreadsheet

A Nesach Tabu (נסח טאבו, land-registry extract) is not a flat form. It is a multi-section
document where several sections repeat: one property can have many owners (each holding a
fractional share), several mortgages, and several cautions. Flattening it to one field per
label loses that structure. To get a usable spreadsheet you normalize each repeating section
into its own set of rows.

## What the extract contains

Per the Land Registration Authority (הרשות לרישום והסדר זכויות מקרקעין), a full extract
(נסח מלא) reports the registered owner and the encumbrances on the property: "שעבודים,
משכנתאות, עיקולים, צווים שיפוטיים ועוד". The information is correct as of the issue date
("המידע בנסח נכון ליום הפקתו"). The official digital extract is signed electronically and is
recognized as an original only in its digital form, not when printed.

The property is keyed by גוש (block) and חלקה (parcel). For an apartment in a shared building
(בית משותף) the תת-חלקה (sub-parcel) is mandatory, and note that "מספר תת החלקה בטאבו אינו
בהכרח זהה למספר הדירה בבניין" -- the sub-parcel number is not necessarily the apartment number.

## The output schema

`scripts/tabu_to_spreadsheet.py` emits ONE flat CSV with a fixed 8-column schema, and a
`section` column that tells each row apart. This keeps every extract shape identical so
several extracts concatenate cleanly:

`section, gush, helka, tat_helka, name, owner_id, share, detail`

- `name` is the free-text party for the row (owner, lessee, creditor, note beneficiary).
- `owner_id` is the party's id (a personal ת.ז., a company ח.פ. / מספר תאגיד, or a passport).
- `share` is the ownership share, kept verbatim.
- `detail` carries the section-specific extras that would otherwise be lost: a mortgage's
  degree (דרגה ראשונה/שנייה, which controls creditor priority), a caution/lien/order's
  beneficiary (לטובת ...) and statutory reference (סעיף 126/128), a lease's end date.

## Sections the parser recognizes

| Section keyword (Hebrew) | `section` value | What the row holds |
|---|---|---|
| תיאור הנכס / the גוש-חלקה line | `property` | one row carrying the gush / helka / tat_helka key |
| בעלויות / בעלות | `owner` | one row per owner, with share. Right type is implied by the section (owner=בעלות, lease=חכירה), not a separate column |
| חכירות / חכירה | `lease` | one row per lessee, lease end date in `detail` |
| משכנתאות / שעבודים | `mortgage` | one row per mortgage, degree in `detail` |
| עיקולים | `lien` | one row per attachment, beneficiary + reference in `detail` |
| צווים / צו | `order` | court orders (כינוס, הריסה, בית משותף) |
| הפקעות | `expropriation` | expropriation entries |
| זיקות הנאה | `easement` | easements |
| הערות / הערת אזהרה | `caution` | cautions, beneficiary + reference in `detail` |
| (anything before the first recognized header) | `unrecognized` | NOT dropped; emitted so a human can place it. The script also prints a warning. |

**Why an `unrecognized` bucket exists.** OCR routinely garbles a section title (ת->ח, injected
spaces). Rather than silently misfile those rows under the previous section, the parser emits
any content it cannot place as `section=unrecognized` and warns on stderr. For a legal document,
a visible "review this" row beats a silently-lost lien or court order. Always read the warnings.

### Ownership share (חלק ברכוש)

The share (חלק) is written as a fraction of the whole property, for example `1/2`, `1/3`,
`125/1000`, or `בשלמות` (in full = 1/1). Keep it verbatim as a string. Do NOT convert it to a
decimal in the spreadsheet: `125/1000` and `0.125` read differently to a lawyer, and rounding a
long denominator loses precision. If you must sanity-check, the owner shares in a single
property should sum to 1 (בשלמות); flag it for human review if they do not, since it usually
means an owner row was missed by OCR.

### Right type (סוג הזכות)

Common values: `בעלות` (ownership), `חכירה` (lease), `חכירה לדורות` (generational lease),
`זיקת הנאה` (easement). A lease and an ownership on the same parcel are two separate rows, not
a merged cell.

## Extraction notes specific to the Tabu layout

- Owner blocks are the most common multi-line field: a name can wrap across two OCR lines and
  the TZ and share land on the next line. Re-anchor by the `ת.ז.` label and the share fraction
  rather than by line position.
- The mortgage section often lists a degree (דרגה ראשונה / שנייה). Capture the degree; it
  controls priority between creditors.
- A caution (הערת אזהרה) records an obligation of a rights-holder toward a third party (a buyer,
  a bank). Capture its beneficiary and reference, not just the fact that one exists.
- An old handwritten extract (a legacy נסח that was never digitized) will not OCR reliably.
  Flag it for human transcription instead of emitting a half-parsed table.

## Limits: what the script does NOT do (check these by hand)

This is a structuring aid, not a substitute for reading the Nesach. Known limits:

- **Area and address are not auto-extracted.** The parcel area (שטח החלקה) and, for an apartment,
  its area and its share in the common property (חלק ברכוש המשותף) are not parsed into columns.
  Read them off the Nesach and add them if you need them. Note the common-property share is a
  different fraction from the ownership share; do not confuse the two.
- **Nesach type matters.** A נסח מרוכז (concentrated) covers a whole בית משותף with many
  apartments, each with its own owners: the single gush/helka/tat_helka key and the owner-share
  sum do NOT hold, split it per apartment by hand. A נסח היסטורי lists struck-through (מחוק)
  past owners: they may be emitted as if current. The script warns when it detects either word,
  but verify.
- **Owner id can be a person or a company.** A ת.ז. validates with the Israeli ID check digit;
  a company ח.פ. / מספר תאגיד and a foreign passport do NOT and will fail that check. A failed
  check-digit on an owner is NOT proof of a bad read, confirm whether the owner is a company.
- **Multi-line owner blocks** are merged only when a name-only line is immediately followed by an
  id/share line. A more scattered layout still needs a human eye.

## From table to file

Emit one flat CSV where a `section` column distinguishes property / owner / lease / mortgage /
caution rows, or emit one sheet per section. The bundled `scripts/tabu_to_spreadsheet.py` does
the former: it takes the OCR text (or the JSON that `extract_form_fields.py` produces) and writes
a normalized CSV that opens cleanly in Excel with RTL Hebrew intact (UTF-8 BOM so Excel detects
the encoding).

## Source

- Land-registry extract service (official), Land Registration Authority: <https://www.gov.il/he/service/land_registration_extract> (the page is bot-protected and may 403 to a plain fetch; it renders normally in a browser).
