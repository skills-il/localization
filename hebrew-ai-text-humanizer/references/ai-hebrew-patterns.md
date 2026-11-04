# AI-Hebrew Pattern Catalogue

The named patterns the skill diagnoses. Each id matches the id printed by
`scripts/hebrew-ai-tells.py`. Three kinds of status:

- **Academy rule**: the Academy of the Hebrew Language rules the form non-standard or prescribes the mark. Say "the Academy rules" and cite it.
- **Style guidance**: legal Hebrew that reads as translated or templated. Say "reads as translated" or "reads as a template", never "incorrect Hebrew".
- **Check**: the script cannot decide. Read the sentence before changing anything. An Academy-rule pattern whose regex also matches correct Hebrew is printed as `check`, and is reported to the user as a rule only after you have read the sentence and confirmed it is the ruled form.

No pattern here is evidence that a text was written by AI. People write all of these. The catalogue explains why each one makes Hebrew sound translated or mass-produced, so the writer can decide.

Sources: Academy punctuation rules (https://hebrew-academy.org.il/topic/hahlatot/punctuation/), Academy usage decisions (https://hebrew-academy.org.il/topic/hahlatot/grammardecisions/terminology-ordinance/4-1-שימושי-לשון/), Academy answers linked per pattern, and W3C Internationalization for direction (https://www.w3.org/International/articles/inline-bidi-markup/).

---

## A. Calques and inflated connectors

### CAL01 עבור in the sense of "for"
- **Status**: style guidance. The Academy explicitly declines to rule on עבור meaning בשביל and calls it a question of style.
- **Why it reads as translated**: it maps one-to-one onto English "for", so machine text uses it for every "for", including where Hebrew uses ל־ or no preposition at all.
- **Bad**: הכנו עבורכם מדריך מיוחד עבור כל לקוח.
- **Fix**: הכנו לכם מדריך לכל לקוח.

### CAL02 ניתן ("it is possible")
- **Status**: style guidance (register).
- **Why**: office-form register. In a post, an email or a product page it puts a counter between writer and reader.
- **Bad**: ניתן להירשם באתר עד יום חמישי.
- **Fix**: אפשר להירשם באתר עד יום חמישי. / הירשמו באתר עד יום חמישי.
- **Careful**: ניתן is also the past tense "was given" (הפרס ניתן לה). Leave that alone.

### CAL03 במידה ו־
- **Status**: Academy rule. The Academy calls במידה ו־ non-standard (https://hebrew-academy.org.il/במידה-ש־/).
- **Why**: a classic inflated connector; the Academy page quotes Shoshana Bahat that writers swap the short אם for "respectable" phrases to sound important.
- **Bad**: במידה ותרצו לבטל, צרו קשר.
- **Fix**: אם תרצו לבטל, צרו קשר.

### CAL04 במידה ש־ in a plain condition
- **Status**: Academy rule, but needs a read (check). The Academy allows במידה ש־ only for real degree ("the more you learn, the more...").
- **Bad**: במידה שהטיול יבוטל, תקבלו החזר. (cancelling has no degree)
- **Fix**: אם הטיול יבוטל, תקבלו החזר.
- **Keep**: במידה שתתאמנו יותר, תתחזקו יותר. (real degree)

### CAL05 היה ו־ as a conditional opener
- **Status**: Academy rule once confirmed; the script prints it as `check`. Non-standard, like במידה ו־; the Academy says the best word to open a condition is אם (https://hebrew-academy.org.il/היה-ו־-היות-ש־-היות-ו־-וביטויים-קרובים/).
- **Not this**: היה ויכוח גדול על התקציב ("there was a big argument") is ordinary Hebrew. The script only fires when a comma follows in the same sentence and skips common vav-initial nouns, but read every hit.
- **Bad**: היה והלקוח יבקש החזר, נטפל בכך מיד.
- **Fix**: אם הלקוח יבקש החזר, נטפל בזה מיד.

### CAL06 היות ו־
- **Status**: Academy rule. Non-standard (same Academy page).
- **Bad**: היות והמשלוח התעכב, נעדכן אתכם.
- **Fix**: כיוון שהמשלוח התעכב, נעדכן אתכם. / המשלוח התעכב, אז נעדכן אתכם.

### CAL07 על מנת
- **Status**: style guidance, grounded in the Bahat quote on the Academy page: כדי ש is swapped for על מנת ש to sound weightier.
- **Bad**: על מנת להשלים את ההרשמה, יש למלא את הטופס.
- **Fix**: כדי להשלים את ההרשמה, מלאו את הטופס.

### CAL08 אשר where ש־ would do
- **Status**: style guidance (same Bahat quote: ש is swapped for אשר).
- **Bad**: המוצרים אשר הזמנתם יישלחו מחר.
- **Fix**: המוצרים שהזמנתם יישלחו מחר.
- **Careful**: the name אשר, and the verb אישר written without yod.

### CAL09 Importance preambles: חשוב לציין, יש לציין, ראוי לציין, חשוב להדגיש
- **Status**: style guidance.
- **Why**: announces that the next sentence matters instead of making it matter. A very common machine-text filler in Hebrew and in English ("it's important to note").
- **Bad**: חשוב לציין כי ההנחה תקפה עד סוף החודש.
- **Fix**: ההנחה תקפה עד סוף החודש.

### CAL10 Scene-setting openers: בעולם של היום, בעידן הדיגיטלי, בעולם המשתנה, בימינו אנו
- **Status**: style guidance.
- **Why**: "In today's world" carried over. Says nothing the reader did not know.
- **Bad**: בעולם של היום, כל עסק צריך נוכחות דיגיטלית.
- **Fix**: start with the claim, or with the reader's problem: לקוחות מחפשים אתכם בגוגל לפני שהם מתקשרים.

### CAL11 "It is not X, it is Y" and "not only X but also Y"
- **Status**: style guidance.
- **Why**: a rhetorical contrast against a claim nobody made. In machine text it appears once or twice per post.
- **What the script matches**: the same pronoun repeated after a comma or dash (זה לא X, זה Y), or אלא. A negated sentence with a later pronoun and no separator (היא לא הגיעה כי היא הייתה חולה) is not matched.
- **Bad**: זה לא על הטכנולוגיה, זה על האנשים.
- **Fix**: state the claim directly, at the same strength, without adding a new one: האנשים חשובים יותר מהטכנולוגיה.

### CAL12 להבטיח ש־ for "to ensure"
- **Status**: style guidance (editor's judgement, no source claimed).
- **Why**: להבטיח is also the everyday word for "to promise", so "להבטיח ש־" used for every English "ensure that" can read as translated. In ordinary copy כדי ש־, לוודא ש־, or just the verb often reads lighter. It is not wrong Hebrew.
- **Bad**: על מנת להבטיח שהמשלוח יגיע בזמן, נא לוודא את הכתובת.
- **Fix**: כדי שהמשלוח יגיע בזמן, בדקו שהכתובת נכונה.

### CAL13 English idioms carried over
- **Status**: style guidance.
- **List the script knows**: בסופו של יום (at the end of the day), משנה משחק / משנה את כללי המשחק (game changer), צעד קדימה (take it a step further), לצלול לעומק (deep dive), לעשות את ההבדל (make the difference), ליצור ערך / לייצר ערך (create value), מדברות בעד עצמן (speak for themselves).
- **Bad**: בסופו של יום, הכלי הזה הוא משנה משחק.
- **Fix**: say what changed: הכלי חסך לנו שעתיים ביום.
- Not every item is wrong everywhere, and none is incorrect Hebrew. In an editor's judgement (no source claimed), בסופו של דבר is the long-standing Hebrew phrase, while בסופו של יום mirrors English "at the end of the day" and reads as a cliché when it opens a closing line.

### CAL14 Stacked connectors at sentence start: בנוסף לכך, יתרה מזאת, כמו כן, מעבר לכך, לאור זאת
- **Status**: style guidance.
- **Why**: every sentence opens with a signpost, an essay-template habit.
- **Fix**: delete the connector; if the logic needs it, merge the two sentences with ו־ or כי.

### CAL15 באופן + adjective
- **Status**: style guidance.
- **Why**: mirrors English -ly adverbs (significantly, personally, immediately).
- **Bad**: הצוות שיפר באופן משמעותי את זמני התגובה.
- **Fix**: הצוות שיפר מאוד את זמני התגובה. / זמני התגובה התקצרו בחצי. (only if the fact is in the source)

### CAL16 Sentence that leads with an English noun
- **Status**: style guidance.
- **Why**: Hebrew readers parse the sentence frame first. Leading with the Latin token breaks the reading direction and the flow.
- **Bad**: CRM הוא כלי שכל עסק קטן צריך.
- **Fix**: מערכת CRM היא כלי שכל עסק קטן צריך.

---

## B. Register mismatch

### REG01 Office-form markers in a casual or professional text
- **Markers**: הננו, הריני, אנו, ברצוננו, בנוגע ל־, בהתאם ל־, לאור האמור, כמפורט להלן, impersonal directives (יש ל־ or נא ל־ before a directive infinitive such as לשים לב, לפנות, למלא, לשלוח; "יש לקוחות" is not a directive and is not flagged).
- **Status**: style guidance. All are correct Hebrew. They are wrong for a post, a WhatsApp message, or a warm customer email.
- **Bad**: הננו מודים לך על פנייתך. נא לפנות למוקד.
- **Fix (professional-warm)**: תודה שפניתם אלינו. אפשר להתקשר למוקד.

### REG02 Slang in a formal text
- **Markers**: סבבה, אחלה, וואלה, יאללה, תכלס, בקטנה, מגניב.
- **Status**: style guidance. Flagged only when the target register is formal.
- **Fix**: replace with the neutral word, or ask the user whether the formality is really wanted.

### Register targets the skill offers
| Target | Sounds like | Typical moves |
|---|---|---|
| dugri / casual | a smart friend on WhatsApp | short sentences, direct imperative, אנחנו, no preambles, at most one emoji |
| professional | a good Israeli business email or LinkedIn post | full sentences, אנחנו and plural address, no slang, no office-form markers |
| formal | a letter to an authority or a contract cover note | אנו allowed, impersonal directives allowed, but still no במידה ו־ or היות ו־ |

---

## C. Addressing and agreement

### ADR01 Slash gender forms: לקוח/ה, יקר/ה, כתוב/י
- **Status**: style guidance grounded in the Academy answer (https://hebrew-academy.org.il/פנייה-המיועדת-לגבר-וגם-לאישה/): slash notation is hard to recommend, cumbersome, and can produce impossible forms. The Academy grammar committee suggested plural address for a mixed audience.
- **Fix**: plural throughout (שלום, תודה שפניתם), or a gender-free construction.

### ADR02 Mixed address in one text
- **Status**: check. The script counts pronouns and second-person suffixes (שלך, אליך versus שלכם, אליכם) and slash forms. Two kinds in one text means the reader is addressed inconsistently.
- **Typical machine slip**: opens with לקוח/ה יקר/ה, continues with masculine singular (תרצה, אליך), closes with plural (נשמח לראותכם).
- **Fix**: pick one form and rewrite every verb, suffix and adjective to match. Plural is the Academy suggestion for a mixed audience; masculine singular is the unmarked default but reads as excluding in marketing.

### Agreement slips (manual check, no regex)
- Verb and adjective agreement with a feminine subject: המערכת החדשה מאפשרת (not מאפשר).
- Number agreement after collective nouns and after numbers: שתי אפשרויות, not שני אפשרויות.
- Construct-state plurals: בתי ספר, not בתי ספרים.
- The model must read for these; the script does not try.

---

## D. Structure tells

### STR01 List-itis
- **Status**: style guidance. Document level: four or more bullets and at least half of the non-blank lines are bullets.
- **Why**: reasoning chopped into fragments. Israeli business writing, especially email, is mostly prose.
- **Fix**: keep a list only for parallel items the reader will scan (dates, documents to bring). Turn reasoning back into sentences.

### STR02 Bold label lines (**יעילות:** ...)
- **Status**: style guidance. A template tell in posts and emails.
- **Fix**: write the sentence: קיצרנו את זמני החלוקה.

### STR03 Emoji bullets
- **Status**: style guidance. One emoji in a casual post is fine; a column of them is a template.

### STR04 Dash overuse and unspaced dashes
- **Status**: two parts.
  - The dash (קו מפריד) is a legitimate Hebrew mark. The Academy rules define it as a long line with a space on each side, used for extra separation, and say the choice between dash, parentheses and semicolon is the writer's. So "Hebrew does not use dashes" is false and the skill never says it.
  - **Academy rule**: a separating dash glued to words (English em dash style) is wrong; the dash takes spaces, and words that belong together take a maqaf, which joins, while the dash separates. The script reports a glued em dash between ordinary words as `rule`. A glued em dash between two month names, two day letters with geresh, or two numbers is reported as `check` instead: if it marks a range, the fix is an unspaced en dash, not added spaces.
  - **The range dash is the exception.** The Academy note on maqaf and dash exempts "a line marking a range" (להוציא קו לציון טווח), and its spacing guidance writes a range between numbers without spaces (עמ' 46 to 53 with an en dash, no spaces). So an unspaced en dash between letters or numbers may be a correct range (January to March, sections a to d). The script reports an unspaced en dash between letters as `check` (read it: a range stays as is), never as `rule`, ignores ranges between digits, and leaves ranges out of the density count, including day ranges with a geresh (א' to ה' with an en dash).
  - **Style guidance**: one separating dash every few lines is a machine tell. The script flags density at one dash per 60 words or more, ranges excluded.
- **Fix**: a comma, a period, parentheses, or nothing.

### STR05 Triads
- **Status**: style guidance. Three or more "X, Y and Z" series in a short text (הכנה, סבלנות ומחויבות).
- **Fix**: keep the real number of items; often one is enough.

### STR06 Every paragraph ends with a summary sentence
- **Status**: style guidance. Paragraphs closing on לסיכום, בסופו של דבר, השורה התחתונה, בקיצור, כך ש־.
- **Fix**: cut the closer and let the last fact land.

### STR07 Headings in a short text
- **Status**: style guidance. Markdown headings in an email or a post under about 250 words.

### STR08 Exclamation density
- **Status**: style guidance. Three or more, and at least one per 40 words.

### STR09 Rhetorical hook openers: דמיינו, תארו לעצמכם, האם ידעתם, רוצים לדעת
- **Status**: style guidance. Start with the news.

---

## E. Punctuation, mixed scripts and direction

### PUN01 Prefix glued to a number: ב2025, ל15
- **Status**: Academy rule. A maqaf goes in a sequence that mixes letters and digits; the Academy examples are הכנס ה־15 and המאה ה־12 (https://hebrew-academy.org.il/על-מקף-וקו-מפריד/).
- **Fix**: ב־2025. When the Hebrew maqaf (U+05BE) is not on the keyboard, a hyphen-minus is the common substitute: ב-2025.
- **Which character to output**: in social and marketing copy (LinkedIn, WhatsApp, Instagram, most websites) default to the keyboard hyphen (ב-2025); that is what Israeli readers see every day and the high maqaf can render oddly in some app fonts. Use the maqaf (U+05BE) in print, formal documents, or when the user's text already uses it. Ask if unsure, and keep one choice throughout.
- **Whole words are not prefixes**: מה, של, כל, כמה, למה and similar words made only of prefix letters are skipped (מה - 5 דברים שלמדתי is fine).

### PUN02 Prefix glued to a Latin-script word: בGoogle, ובExcel
- **Status**: Academy rule (same maqaf rule; the Academy example is פגיעה ב־DNA).
- **Fix**: ב־Google, וב־Excel.

### PUN03 Spaced dash where a maqaf belongs: ה plus a long dash plus 15, or ב - 2026
- **Status**: Academy rule. The Academy uses exactly this kind of heading as its example of failed maqaf and dash use.
- **Fix**: ה־15, ב־2026 (no spaces).

### PUN04 Abbreviations with periods: ת.ד., מס. 48213, צ.ה.ל.
- **Status**: Academy rule. No period after a shortened word; geresh for a shortened word (מס', עמ'), gershayim before the last letter of an acronym (צה"ל, ת"ד).
- **Fix**: מס' 48213, ת"ד, צה"ל.
- **Not this**: מס. at the end of a sentence is usually the word "tax" (שילמנו לא מעט מס.). The script flags מס. only when a number follows.
- **Typing note**: in typed text the keyboard double quote (U+0022) is an accepted stand-in for gershayim; the Academy's own spacing page writes תנ"ך and אחה"צ that way. The apostrophe likewise stands in for geresh.

### PUN06 Prefix separated from its number by a space: עלה ב 5 אחוז
- **Status**: check. It follows from the maqaf rule for a prefix and a number, but the Academy does not state the spaced case separately, and a lone letter before a number can be a label (סעיף ב 3), not a prefix. The script also flags a lone prefix before a Latin word (בחרו ב BrewMaster). Read it before changing it.
- **Fix**: עלה ב-5 אחוז (social copy) or ב־5 (print).

### PUN05 Space before punctuation: מה שלומך ?
- **Status**: Academy recommendation, not a ruling. The Academy strongly recommends ("מומלץ מאוד") not typing a real space before the heavy marks, and certainly not before a comma or a period; its example is "מה שלומך?" not "מה שלומך ?" (https://hebrew-academy.org.il/הרווח-כולו-שלכם-רווחים-בסביבת-סימני/). The same page notes that old Hebrew printing put a light space (smaller than a word space) before heavy marks, so a typographic light space is not an error. The script scores PUN05 as `style`; report it as "the Academy recommends", never as "non-standard".

### PUN07 Direction risks in mixed Hebrew, English and numbers
- **Status**: check. The Academy notes that punctuation problems arise in Hebrew text with Latin-script parts because of the opposite direction. W3C lists the cases that break without wrapping: an opposite-direction phrase that begins or ends with neutral characters, begins with a number, or is followed by a number.
- **What the script flags**: a Hebrew line that starts with a Latin word or a digit; and an English phrase followed by a SEPARATE number, detected as Latin text, a number, then a Hebrew counting word (קראתי את Harry Potter 3 פעמים). In the second case the number can visually attach to the English run.
- **Not this**: a number that belongs to the name (a product model or version number written right after the brand) displays correctly as one left-to-right run and needs nothing. The script does not flag it.
- **Fix order**: (1) rephrase so the separate number is not right after the English phrase (קראתי 3 פעמים את Harry Potter), or so the line starts with Hebrew; (2) in plain text where rephrasing is not possible, insert RLM (U+200F) right after the English phrase and before the separate number; (3) in HTML, wrap the phrase with the dir attribute or bdi as the W3C article describes.
- **Warning**: never insert RLM inside a name that contains its own number. RLM is a strong right-to-left character, so placing it between the brand and its number splits the run and can show the number before the name.

---

## F to I: LinkedIn tells, grammar-level translationese, vocabulary and spelling, the writer's gender

These sections (LNK01 to LNK08, GRM01 to GRM04, VOC01, SPL01, and the gender rules) are in `references/channel-grammar-gender.md`.

## How to report a pattern to the user

One line per change in the change log: `id | before | after | why (one short clause)`. Use "the Academy rules" only for rows whose status above is Academy rule. For style rows say "reads as translated", "template tell" or "register".
