# Israeli Government Form Types Reference

## Tabu (Land Registry) -- Lishkat Rishum Ha-Mekarkein

### Nesach Tabu (Title Deed Extract)
- **Purpose:** Official record of property ownership and encumbrances
- **Issuing body:** Land Registry Office (Lishkat Rishum Ha-Mekarkein)
- **Key fields:**
  - Gush (block) number -- geographic area identifier
  - Chelka (parcel) number -- specific plot within the gush
  - Sub-parcel (tat-chelka) -- the unit identifier for an apartment in a shared building; NOT necessarily the same as the apartment number
  - Owner name and ID (TZ)
  - Rights type (ba'alut = ownership, chakhira = lease, etc.)
  - Encumbrances: mortgages (mashkanta), liens (ikul), caveats (he'arat azhara)
- **Layout:** Multi-section tabular layout with Hebrew headers and numeric data
- **OCR tips:** Use PSM 4 for the tabular sections, watch for multi-line owner names

### Tabu Field Patterns (Regex)
```
Gush:    גוש[:\s]*(\d+)
Chelka:  חלקה[:\s]*(\d+)
TZ:      (?:ת[.'"׳״]?ז[.'"׳״]?|מספר זהות)[:\s]*(\d{8}-\d|\d{8,9})(?![\d-])
Share:   (?<![\d/])\d{1,7}\s*/\s*\d{1,7}(?![\d/])|בשלמות
Deed:    (?<![\d/])\d{1,7}/\d{4}/\d{1,4}(?![\d/])
```

Owners are a table (section header "בעלויות", then one row per owner), not a
"label: value" pair, so a single-line owner regex returns only the first owner and
can run across line breaks. Use `scripts/tabu_to_spreadsheet.py` for owners,
mortgages and cautions. Keep the share regex's look-arounds: without them a deed
number such as 12345/2015/1 is read as the share 12345/2015.

## Tax Authority (Rashut Ha-Misim)

### Form 106 -- "אישור על משכורת וניכוי מס"
- **Purpose:** The employer's annual certificate to the employee of salary paid and tax withheld in the tax year
- **Printed labels:** "שם מלא של המעסיק", "מספר תיק ניכויים" (the employer's withholding file), "שם מלא של העובד", "מספר זהות העובד", "שנת מס"
- **Amount rows carry annual-return field codes:** salary row "משכורת" = field 158/172; "ניכיתי ושילמתי מס הכנסה" = field 042; other rows include 218/219 (keren hishtalmut salary), 244/245 (pension salary), 248/249 (pension deposits)
- **OCR tip:** the code and the amount sit side by side and OCR often glues them ("04221,340"); split the code off before parsing, and never return the code as the amount
- **Layout:** Dense tabular format with multiple sections

### Ishur Nikui Mas Ba-Makor -- Withholding Tax Certificate
- **Purpose:** States the withholding-at-source rate the assessing officer (פקיד שומה) set for a business. Payers ask for it together with the bookkeeping certificate, as "אישור ניהול ספרים וניכוי מס במקור"
- **Key fields:** File number (income-tax file / osek murshe / partnership), withholding rate, validity period, business name and address
- **Before relying on it:** an OCR'd rate or validity date can be misread or out of date; confirm both in the Tax Authority's online lookup by file number (the service also prints the current certificate)

### Form 806/857 -- Annual Withholding Certificate on Payments
- **Title:** "אישור שנתי על ניכוי מס הכנסה מתשלומים המחייבים ניכוי מס במקור" (the form header prints "0806/0857")
- **Purpose:** Given by a payer to a supplier or service provider, listing the year's payments and the tax withheld. It is NOT a capital-gains form; capital-gains sales are reported on Form 1399
- **Key fields:** Payer's withholding file number, payee ID / file, type of payment, gross payment, tax withheld, tax year

## Bituach Leumi (National Insurance Institute)

### Benefit certificates (אישורים)
- **Names on BTL's certificates page:** "אישור זכאות לגמלאות שנתי", "אישור תשלומים שנתי", "אישור על תשלומים", "אישור שנתי למס הכנסה", "אישור על תקופות ביטוח". Detect by the header "המוסד לביטוח לאומי": titles like "אישור זכאות" alone also appear on housing and utility documents
- **Key fields:** TZ, benefit type (old-age, disability, unemployment, etc.), period, amount
- **Extraction:** the bundled extractor detects these and lists their ids, dates and amounts unlabelled; map them to fields from the raw text

### Form 102 -- "דין וחשבון על העסקת עובדים"
- **Purpose:** The employer's monthly report and payment of insurance contributions to Bituach Leumi
- **Key fields:** Employer, employees, wages, contributions

Do not key on "טופס 100": the PDF BTL publishes under that number is a claimant's refusal form, and "קובץ 100" is an online per-employee file, never a scanned document.

## Common Field Formats

### Israeli ID Number (Teudat Zehut)
- 9 digits, zero-padded on the left
- Check digit algorithm: alternating multiply by 1 and 2, sum digits, modulo 10
- Format in forms: usually XXXXXXXXX; an id printed as 8 digits (leading zero dropped) is left-padded to 9 and flagged. Never pad a shorter read: a fragment can pass the check digit by chance

### Date Formats in Israeli Forms
- DD/MM/YYYY (most common)
- DD.MM.YYYY (some forms)
- Hebrew calendar dates (rare in government forms, more common in religious documents)

### Currency
- Symbol: ₪ (New Israeli Shekel, NIS)
- Format: ₪1,234.56 or 1,234.56 ₪
- Agorot (cents): 100 agorot = 1 shekel

### Phone Numbers
- Landline: 0X-XXXXXXX (e.g., 02-1234567 for Jerusalem)
- Mobile: 05X-XXXXXXX (e.g., 054-1234567)
- Always LTR in forms, even within RTL context
