# Israeli Government Form Types Reference

## Tabu (Land Registry) -- Lishkat Rishum Ha-Mekarkein

### Nesach Tabu (Title Deed Extract)
- **Purpose:** Official record of property ownership and encumbrances
- **Issuing body:** Land Registry Office (Lishkat Rishum Ha-Mekarkein)
- **Key fields:**
  - Gush (block) number -- geographic area identifier
  - Chelka (parcel) number -- specific plot within the gush
  - Sub-parcel (tat-chelka) -- apartment/unit number in multi-unit properties
  - Owner name and ID (TZ)
  - Rights type (ba'alut = ownership, chakhira = lease, etc.)
  - Encumbrances: mortgages (mashkanta), liens (ikul), caveats (he'arat azhara)
- **Layout:** Multi-section tabular layout with Hebrew headers and numeric data
- **OCR tips:** Use PSM 4 for the tabular sections, watch for multi-line owner names

### Tabu Field Patterns (Regex)
```
Gush:    גוש[:\s]*(\d+)
Chelka:  חלקה[:\s]*(\d+)
Owner:   (?:בעלים|שם הבעלים)[:\s]*([\u0590-\u05FF\s]+)
TZ:      (?:ת\.?ז\.?|מספר זהות)[:\s]*(\d{5,9})
Rights:  (?:סוג הזכות|זכות)[:\s]*([\u0590-\u05FF\s]+)
```

## Tax Authority (Rashut Ha-Misim)

### Tofes 106 -- Annual Employer Statement
- **Purpose:** Summary of employee earnings and tax deductions for the tax year
- **Key fields:** Tax year, employer number, employee TZ, gross salary, tax deducted, pension contributions, social security
- **Layout:** Dense tabular format with multiple sections

### Ishur Nikui Mas Ba-Makor -- Withholding Tax Certificate
- **Purpose:** Authorizes a specific withholding tax rate for a business
- **Key fields:** Business number (osek), tax rate percentage, validity period, business name and address

### Tofes 857 -- Capital Gains Tax Form
- **Purpose:** Report capital gains from property or securities transactions
- **Key fields:** Transaction date, purchase price, sale price, calculated gain, tax owed

## Bituach Leumi (National Insurance Institute)

### Ishur Zkauyot -- Entitlement Certificate
- **Purpose:** Confirms benefit eligibility and payment amounts
- **Key fields:** TZ, benefit type (old-age, disability, unemployment, etc.), monthly amount, validity dates

### Tofes 100 -- Employer Report
- **Purpose:** Monthly/quarterly report of employee wages and contributions
- **Key fields:** Employer number, employee list, wages, NII contributions, health tax

## Common Field Formats

### Israeli ID Number (Teudat Zehut)
- 9 digits, zero-padded on the left
- Check digit algorithm: alternating multiply by 1 and 2, sum digits, modulo 10
- Format in forms: XX-XXXXXXX-X or XXXXXXXXX

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
