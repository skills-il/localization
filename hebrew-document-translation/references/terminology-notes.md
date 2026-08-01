# Hebrew professional-translation conventions

Domain-agnostic conventions observed across real published Hebrew professional documents,
regardless of field - useful defaults when no reference document dictates otherwise. These rules
apply the same way whether the source is a software manual, a legal contract, a medical report, a
financial statement, marketing copy, or an exam - the *specific* terms will differ by field, but
the *approach* below doesn't.

## Keep in English (don't translate or transliterate)

- Acronyms, initialisms, and codes that are specific to the source document's own field - whatever
  those happen to be. A software document might have API, UI, CI/CD, OWASP; a legal contract might
  have UCC, NDA, or clause/section codes; a financial report might have IFRS, EBITDA, ISO codes; a
  medical document might have lab-test abbreviations or drug names. The rule is the same regardless
  of field: don't force-translate or transliterate a term the source itself left as an acronym or
  code, just because the surrounding sentence is Hebrew.
- Product/brand/organization names, and any vendor or standard-body names.
- Standard document boilerplate that itself contains a registered trademark or org name - keep the
  `®`/`©` and the org name in English even when the surrounding sentence is Hebrew.
- On first use of a term that *does* have a common Hebrew equivalent, give the Hebrew phrase
  followed by the English term in parentheses (e.g. `מיקור חוץ (outsourcing)`); after that, the
  shorter form is fine.

## Style rules (apply to any field)

- **Consistency beats "correctness"**: once you've picked a Hebrew rendering for a recurring term
  in a document, reuse the exact same phrase everywhere - don't vary it for style. If a reference
  document already translated a term a certain way, match it exactly rather than improving on it.
- **Gender-neutral phrasing**: Hebrew professional documents commonly use slash-forms for gender
  neutrality in role/person references - e.g. `המועמד/ת`, `הלקוח/ה`, `העובד/ת`, `יכול/ה`. Apply
  this to any noun/verb referring to an unspecified person, in whatever role the document is
  about (customers, employees, applicants, patients, etc.), not just obviously gendered nouns.
- **Numbers, codes, dates**: keep numerals, reference/clause/requirement codes (e.g. `STE-4.3.1`,
  `§12.4`), and version numbers exactly as in the source - don't convert digit style or reformat
  dates unless the reference template does so.
- **Lettered/numbered lists**: keep the same lettering/numbering scheme as the source (a, b, c…)
  rather than switching to Hebrew letters (א, ב, ג…), unless the reference document you're matching
  does the latter - then match it exactly.
- **Formal register**: when the source is a formal document, prefer the more official/formal Hebrew
  synonym over a casual one for recurring role or concept terms - but which word that is depends
  entirely on the document's own field and house style. If a reference document is available, copy
  its choice rather than picking your own.

## Worked examples (illustrative only - don't apply one field's glossary to a different field)

These are just two small samples of what a field-specific glossary looks like in practice. Build a
similar (informal, ad hoc) glossary for whatever field the current document actually belongs to -
don't assume either of these applies outside its own field.

### Example: software / QA testing documents (e.g. ISTQB-style material)
| English | Preferred Hebrew | Notes |
|---|---|---|
| Exam / Sample Exam | בחינה / בחינה לדוגמה | More formal/official register than מבחן |
| Framework | מסגרת | e.g. מסגרת אוטומציית בדיקות (TAF) |
| Shift left/right | shift-left (הסטה שמאלה) / shift right (הסטה ימינה) | Keep the English term; Hebrew gloss in parentheses |
| Legacy (software) | תוכנת legacy / תוכנת מורשת | `legacy` in Latin script is common in Israeli tech writing |
| Sprint | ספרינט | Fully Hebraized/transliterated, not translated |

### Example: contracts / legal documents
| English | Preferred Hebrew | Notes |
|---|---|---|
| Whereas | הואיל ו- | Standard formal contract-opening phrasing |
| Party of the first part | הצד הראשון / הצד הא' | Match whichever convention the reference template uses |
| Governing law | הדין החל | Keep jurisdiction names (states, countries) in their normal Hebrew form |
| Indemnify | לשפות | Standard legal-Hebrew rendering |
| For educational/non-commercial use only | לשימוש לימודי / לא מסחרי בלבד | Standard disclaimer line for translated official materials, useful across fields |
