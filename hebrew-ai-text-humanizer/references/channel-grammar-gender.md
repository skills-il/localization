# Channel, Grammar, Vocabulary and Gender Patterns

Part two of the catalogue (part one is `ai-hebrew-patterns.md`, sections A to E). Same ids as `scripts/hebrew-ai-tells.py`. Everything in this file is **style guidance** or a **manual check**: none of it is an Academy ruling, and no source is claimed. Report these as "reads as translated", "template tell" or "register", never as "incorrect Hebrew".

## F. LinkedIn and announcement tells (style guidance)

No source is claimed for these; they are an editor's catalogue of what makes a Hebrew LinkedIn post read as a translated template.

### LNK01 "Excited to share" openers: אני נרגש/ת לשתף, נרגשת לראות, גאה להכריז, שמח/ה לבשר
- **Bad**: אני נרגשת לשתף שהתחלתי תפקיד חדש!
- **Fix**: התחלתי השבוע תפקיד חדש: [the role] ב[company]. (The news first; the feeling is implied.)

### LNK02 "Journey": המסע, מסע מאתגר, חלק מהמסע
- **Fix**: name the thing: הפרויקט, השנה הזאת, המעבר, ארבע השנים בחברה.
- **Keep**: a real trip (המסע לנפאל).

### LNK03 "Fills me with pride": ממלא אותי בגאווה / בהתרגשות
- **Fix**: say what happened and let the reader infer the pride: הצוות סגר את הפרויקט שבוע לפני הזמן.

### LNK04 "4 amazing years": 4 שנים מדהימות / מטורפות
- **Fix**: drop the adjective, or replace it with one concrete thing from the source.

### LNK05 Blanket thanks: תודה לכל מי שהיה חלק
- **Fix**: thank named people (if the source names them), or cut it.

### LNK06 Buzzwords: לרתום, להעצים, פורץ דרך, חדשני, סינרגיה, אקוסיסטם, ערך מוסף, ברמה הבאה
- **Fix**: the concrete claim behind the word, or nothing. Never invent the concrete claim.

### LNK07 Hashtags (document level)
- More than about three, or hashtags in the middle of sentences, read as a template.
- Convention: at the end, on their own line; a multi-word Hebrew tag joined with an underscore (#ניהול_מוצר).

### LNK08 Hook and paragraphing (document level, with `--channel linkedin`)
- LinkedIn shows only the first lines before "see more". The first line should carry the news in one short sentence, not a scene-setting opener (CAL10) or a hook question (STR09, GRM03).
- One idea per short paragraph; a line over about 60 words is split.

## G. Grammar-level translationese (style guidance)

### GRM01 Redundant subject pronoun: אני הובלתי, אנחנו ביצענו
- **Why**: in the past tense (and future) the verb already carries the person. English needs "I"; Hebrew does not.
- **Fix**: הובלתי, ביצענו. **Keep** the pronoun for contrast (אני הובלתי, והם ביצעו).

### GRM02 Light verb + action noun: ביצענו הטמעה של, קיבלנו החלטות, לעשות שימוש ב
- **Fix**: הטמענו, החלטנו, להשתמש ב. "לקבל החלטה" is idiomatic Hebrew too; change it when a plain verb is lighter, not by reflex.

### GRM03 האם opening a yes/no question (casual and professional only)
- **Bad**: האם אתם יודעים כמה קשה לעזוב צוות?
- **Fix**: אתם יודעים כמה קשה לעזוב צוות? (Formal letters may keep האם.)

### GRM04 על ידי
- **Why**: English "by" passives and "by means of". Machine Hebrew stacks them.
- **Bad**: הבקשה תטופל על ידי הצוות. / ניתן לבטל על ידי מענה למייל.
- **Fix**: הצוות יטפל בבקשה. / אפשר לבטל בתשובה למייל.

### Manual read (no regex)
- Present-tense or participle chains that mirror English "-ing": "אני עובד על פיתוח של" for "פיתחתי" or "אני מפתח".
- Possessive "של" chains where a construct form is natural (ההחלטה של ההנהלה is fine; three של in a row is not).

## H. Vocabulary and spelling

### VOC01 Over-Hebraised words (casual and professional only)
- **Words**: משוב, דוא"ל, דואר אלקטרוני, יישומון, מרשתת, מקוון.
- **Why**: correct Hebrew, often Academy coinages, but Israeli business readers usually say פידבק, מייל, אפליקציה, אינטרנט, אונליין. Machine text pushed towards "pure" Hebrew sounds stiffer, not more native.
- **Rule of thumb**: keep the loanword the audience actually uses; keep the Hebrew word when the brand, the sector (government, academia) or the user's own text uses it. Leading a sentence with an English noun (CAL16) is still a tell: the fix is Hebrew framing around the loanword (מערכת ה-CRM שלנו), not replacing the loanword.

### SPL01 Mixed spelling of one word (document level)
- **Pairs the script knows**: תכנית / תוכנית, אמא / אימא, מיד / מייד, לעתים / לעיתים, דוגמא / דוגמה.
- **Fix**: pick one spelling and keep it throughout. Do not "correct" the writer's consistent choice. (Full ktiv maleh rules: hebrew-content-writer.)

## I. The writer's gender (manual, always)

- Hebrew first person is ungendered in the past and future (הובלתי, אשמח) but gendered in the present, in participles and in adjectives (אני נרגש / נרגשת, שמח / שמחה, גאה is the same for both, מתחיל / מתחילה in "הייתי מתחיל").
- Never introduce a gendered first-person form that is not already in the source. If the source has one, keep its gender. If the writer's gender is unknown, use forms that are the same for both: past or future verbs (התחלתי, אשמח), "כדאי" + infinitive, or the plural "אנחנו".
- Every change that adds, removes or switches a gendered form goes under Judgement calls in the output.

