# Israeli Business Document Templates

## Tax Invoice (Heshbonit Mas / חשבונית מס)

### Required Fields (per Kol Zchut's summary of the VAT rules)

A tax invoice may be issued only by an עוסק מורשה. It must show:

| Field | Hebrew | Notes |
|-------|--------|-------|
| Business name and address | שם העוסק וכתובת העסק | As registered |
| The words "עוסק מורשה" and the osek number | המילים "עוסק מורשה" ומספר עוסק מורשה | The business's registration number with VAT |
| The words "חשבונית מס" | המילים "חשבונית מס" | As the document title |
| "מקור" | המילה "מקור" | On the original only; the copy the business keeps is marked "העתק" |
| Invoice number | מספר החשבונית | Serial |
| Date of issue | תאריך הוצאת החשבונית | DD/MM/YYYY |
| Transaction details | פירוט העסקה | Description, quantity, unit price |
| Delivery note number and date | מספר ותאריך תעודת משלוח | Only when a delivery note is required |
| Price without VAT, VAT, total | המחיר ללא המס, סכום המס בנפרד והמחיר הכולל | VAT currently 18% |
| Signature | חתימת העוסק או עורך החשבונית | |
| Allocation number | מספר הקצאה | Israel Invoices model: required from 1 June 2026 when the transaction exceeds 5,000 NIS before VAT (20,000 NIS in 2025, 10,000 NIS from 1 January 2026) and the customer, an עוסק מורשה, asks for one. Without it the customer cannot deduct input VAT. Time-sensitive. |

Kol Zchut's list for a tax invoice does not include the customer's details; a חשבונית עסקה lists "שם הלקוח וכתובתו". Business customers expect their name and osek number on a tax invoice in practice, so include them.

### Which document to issue

| Business | Payment status | Document |
|----------|----------------|----------|
| עוסק פטור | Paid | קבלה (never a חשבונית מס, never VAT) |
| עוסק מורשה | Not yet paid | חשבונית עסקה or חשבונית מס; a חשבון עסקה (free-form payment request) if only asking for payment |
| עוסק מורשה | Paid at the time of the transaction | חשבונית מס/קבלה |
| עוסק מורשה | Paid later | קבלה on payment (plus the invoice already issued) |

Tax invoices are printed from a pre-printed book or from authorized invoicing software, in an original and a copy. The bundled `scripts/generate_doc.py` output is a layout sample, not an issued invoice.

### VAT Rules
- Standard rate: 18% (since 1 January 2025)
- Some transactions are zero-rated (שיעור אפס) and some are exempt (עסקה פטורה); the two are treated differently on the invoice and for input VAT. Confirm the treatment with the Tax Authority or an accountant before issuing.
- The invoice must show the price without VAT and the VAT amount separately

## Contract (Hozeh / חוזה)

### Standard Sections

| Section | Hebrew | Content |
|---------|--------|---------|
| Preamble | מבוא | Date, parties, purpose |
| Definitions | הגדרות | Key terms used in the contract |
| Scope of work | היקף העבודה | Detailed description of deliverables |
| Payment terms | תנאי תשלום | Amounts, schedule, currency (NIS) |
| Duration | תקופת ההסכם | Start date, end date, renewal terms |
| Termination | ביטול ההסכם | Notice period, breach conditions |
| Confidentiality | סודיות | NDA clauses |
| IP rights | קניין רוחני | Ownership of deliverables |
| Liability | אחריות | Limitation of liability |
| Dispute resolution | יישוב סכסוכים | Jurisdiction (Israeli courts), arbitration |
| Signatures | חתימות | Both parties, date, witness if needed |

### Standard Hebrew Legal Phrases
- "הואיל ו..." (Whereas...)
- "הוסכם והותנה בין הצדדים כדלקמן:" (It was agreed between the parties as follows:)
- "מבלי לגרוע מכלליות האמור לעיל" (Without derogating from the generality of the above)
- "למען הסר ספק" (For the avoidance of doubt)

## Price Proposal (Hatza'at Mechir / הצעת מחיר)

### Customary Fields

| Field | Hebrew | Notes |
|-------|--------|-------|
| Business details | פרטי העסק | Name, address, Osek number |
| Proposal number | מספר הצעה | Sequential |
| Date | תאריך | DD/MM/YYYY |
| Recipient | נמען | Customer name and details |
| Item list | רשימת פריטים | Description, quantity, unit price |
| Subtotal | סכום ביניים | Before VAT |
| VAT | מע"מ | 18% |
| Total | סה"כ | Including VAT |
| Validity period | תוקף ההצעה | Typically 30 days |
| Payment terms | תנאי תשלום | Net 30, installments, etc. |
| Notes | הערות | Special conditions |

## Meeting Minutes (Protokol / פרוטוקול)

### Standard Structure

| Section | Hebrew | Content |
|---------|--------|---------|
| Header | כותרת | Meeting type, date, time, location |
| Attendees | משתתפים | Names and roles |
| Absent | נעדרים | Expected but absent members |
| Agenda | סדר יום | Numbered agenda items |
| Discussion | דיון | Summary of each agenda item |
| Decisions | החלטות | Numbered decisions made |
| Action items | משימות | Task, assignee, deadline |
| Next meeting | ישיבה הבאה | Date and preliminary agenda |
| Signatures | חתימות | Chair and secretary |

## Receipt (Kabala / קבלה)

### Customary Fields

| Field | Hebrew | Notes |
|-------|--------|-------|
| Business name | שם העסק | As registered |
| Osek number | מספר עוסק | עוסק מורשה or עוסק פטור number |
| Receipt number | מספר קבלה | Sequential |
| Date | תאריך | DD/MM/YYYY |
| Amount received | סכום שהתקבל | In NIS |
| Payment method | אמצעי תשלום | Cash, check, transfer, credit card |
| Payer name | שם המשלם | Individual or company |
| Reference | אסמכתא | Check number, transfer reference |
