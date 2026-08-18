# ערכת כלי NLP לעברית

## הנחיות

### שלב 1: לזהות את משימת ה-NLP
| משימה | מודל מומלץ | מזהה HuggingFace | גודל | הערות |
|-------|-----------|------------------|------|-------|
| יצירת טקסט (איכות מרבית) | DictaLM 3.0 24B Base | `dicta-il/DictaLM-3.0-24B-Base` | 24B | המודל החזק ביותר בעברית, מבוסס על Mistral-Small-3.1-24B |
| יצירת טקסט (קל יותר) | DictaLM 3.0 Nemotron Instruct | `dicta-il/DictaLM-3.0-Nemotron-12B-Instruct` | 12B | מכוון להוראות, טביעת רגל קטנה יותר |
| היסק / שרשרת מחשבה | DictaLM 3.0 24B Thinking | `dicta-il/DictaLM-3.0-24B-Thinking` | 24B | מייצר בלוק חשיבה מפורש לפני התשובה |
| קצה / לפטופ | DictaLM 3.0 1.7B Thinking (GGUF) | `dicta-il/DictaLM-3.0-1.7B-Thinking-GGUF` | 1.7B | רץ על CPU דרך llama.cpp |
| מילוי מסכה (בסיס) | DictaBERT | `dicta-il/dictabert` | 184M | מודל בסיס מהיר; לסיווג יש לכוונן או להשתמש במודל ייעודי |
| זיהוי ישויות (NER) | DictaBERT NER | `dicta-il/dictabert-ner` | 184M | מזהה PER, GPE, TIMEX, TTL |
| ניתוח סנטימנט | DictaBERT Sentiment | `dicta-il/dictabert-sentiment` | 184M | סיווג סנטימנט בעברית |
| מורפולוגיה | DictaBERT Morph | `dicta-il/dictabert-morph` | 184M | פיצול תחיליות וחלקי דיבר |
| שאלות ותשובות | DictaBERT HeQ | `dicta-il/dictabert-heq` | 184M | QA חילוצי בעברית |
| הטמעות (מודרני) | NeoDictaBERT Bilingual Embed | `dicta-il/neodictabert-bilingual-embed` | 400M | הטמעות משפטים דו-לשוניות עברית-אנגלית |
| הטמעות (ישן יותר) | AlephBERT | `onlplab/alephbert-base` | 110M | בסיס ותיק יותר לדמיון |
| דיבור-לטקסט | ivrit.ai Whisper v3 | `ivrit-ai/whisper-large-v3` | 1.55B | כוונון עדין על קורפוס הדיבור העברי של ivrit.ai (מאגר של 22K+ שעות) |
| דיבור-לטקסט (מהיר) | ivrit.ai Whisper v3 Turbo CT2 | `ivrit-ai/whisper-large-v3-turbo-ct2` | 809M | מנוע CTranslate2, בערך פי 3 מהיר |

### שלב 2: התקנה וטעינת המודל

**DictaBERT (מודל בסיס, מילוי מסכה):**
```python
from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("dicta-il/dictabert")
model = AutoModelForMaskedLM.from_pretrained("dicta-il/dictabert")
```
`dicta-il/dictabert` הוא מודל בסיס מסוג masked-LM, ללא ראש סיווג. אל תטענו אותו עם `AutoModelForSequenceClassification` ותריצו חיזוי, זה יוצר ראש סיווג מאותחל אקראית ומחזיר תוצאות חסרות משמעות. לסיווג, או כווננו אותו על נתונים מתויגים תחילה, או השתמשו במודל ייעודי מוכן כמו `dicta-il/dictabert-sentiment` (סנטימנט) או `dicta-il/dictabert-ner` (NER).

**DictaLM 3.0 (יצירת טקסט, 12B Instruct):**
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("dicta-il/DictaLM-3.0-Nemotron-12B-Instruct")
model = AutoModelForCausalLM.from_pretrained("dicta-il/DictaLM-3.0-Nemotron-12B-Instruct")
```

לאיכות המרבית, תחליפו ל-`dicta-il/DictaLM-3.0-24B-Base`. למשימות היסק (מתמטיקה, לוגיקה רב-שלבית), תשתמשו ב-`dicta-il/DictaLM-3.0-24B-Thinking`, שכותב את שרשרת המחשבה בתוך בלוק thinking מפורש לפני התשובה הסופית.

**ivrit.ai Whisper (דיבור-לטקסט):**
```python
from transformers import pipeline
# מודל ASR עברי מכוונן עדין מ-ivrit.ai, מבוסס openai/whisper-large-v3
pipe = pipeline("automatic-speech-recognition", model="ivrit-ai/whisper-large-v3")
result = pipe("audio.wav", generate_kwargs={"language": "he"})
```
לזמן תגובה נמוך יותר, תשתמשו ב-`ivrit-ai/whisper-large-v3-turbo-ct2` דרך `faster-whisper` (מנוע CTranslate2, בערך פי 3 מהיר יותר על GPU).

### שלב 3: עיבוד מקדים של טקסט עברי
לפני שמעבירים טקסט למודלים:
1. **נרמול:** הסרת רווחים מיותרים, נרמול Unicode (NFC)
2. **טיפול בניקוד:** הסרת סימני ניקוד אלא אם הם באמת נחוצים
3. **טיפול באנגלית:** להחליט אם לשמור, לתרגם או לסמן טוקנים באנגלית
4. **טוקניזציה:** טוקנייזרים לעברית מטפלים בפיצול מורפולוגי

```python
import re
import unicodedata

def preprocess_hebrew(text):
    # Normalize Unicode
    text = unicodedata.normalize('NFC', text)
    # Remove niqqud (diacritics) - range U+0591 to U+05C7
    text = re.sub(r'[\u0591-\u05C7]', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

### שלב 4: שחזור ניקוד (דיאקריטיזציה)

העיבוד המקדים שלמעלה *מסיר* ניקוד. המשימה ההפוכה, *הוספת* ניקוד חזרה לטקסט לא מנוקד, נקראת דיאקריטיזציה והיא בעיה מרכזית בפני עצמה ב-NLP עברי (שימושית להמרת טקסט לדיבור, ללימוד שפה, לטקסטים ליטורגיים, ולפתרון דו-משמעות).

הנקדן של Dicta הוא הכלי הסטנדרטי. מודל ברמת התו מפורסם ב-HuggingFace:

```python
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('dicta-il/dictabert-large-char-menaked')
model = AutoModel.from_pretrained('dicta-il/dictabert-large-char-menaked', trust_remote_code=True)
model.eval()

# המודל חושף פונקציית עזר predict שמחזירה טקסט מנוקד
vocalized = model.predict(['שלום עולם'], tokenizer)
```

הערות:
- צריך `trust_remote_code=True` כי המודל כולל ראש `predict` מותאם. כדאי לעבור על כרטיס המודל לפני שמפעילים את זה.
- דיאקריטיזציה היא דו-משמעית: לאותו טקסט עיצורי יכולות להיות כמה נקודות תקינות לפי ההקשר. כדאי להתייחס לפלט כניחוש מיטבי, לא כאמת מוחלטת.
- לניקוד ברמת משפט שלם עם הקשר מורפולוגי, הנקדן המתארח של Dicta (ראו שלב 6) בדרך כלל טוב יותר ממודל תווים גולמי.

### שלב 5: שירותי REST מתארחים של Dicta

אם לא רוצים להריץ מודלים מקומית, Dicta חושפת את הכלים שלה (נקדן, מורפולוגיה ועוד) כשירותי ווב מתארחים. זה מתאים לשימוש בנפח נמוך, לאבות טיפוס, או לסביבות בלי GPU.

- נקדן (דיאקריטיזציה): https://nakdan.dicta.org.il/
- גישת מפתחים ופרטי API: https://dicta.org.il/developers

כדאי לאמת את מבנה ה-endpoint העדכני, פורמט הבקשה, מגבלות הקצב ותנאי השימוש בעמוד המפתחים לפני אינטגרציה, כי חוזי API מתארחים משתנים. אל תניחו כתובת endpoint או סכמת payload, תסתכלו בתיעוד המפתחים הרשמי.

### שלב 6: נקודות כניסה חלופיות ל-NLP

המחסניות `Dicta` ו-`ivrit.ai` הן העיקריות בעברית, אבל גם שני פריימוורקים כלליים של NLP כוללים צינורות לעברית:

- **HebSpacy** (https://github.com/8400TheHealthNetwork/HebSpacy): צינור spaCy לעברית עם טוקניזציה, POS, למטיזציה וזיהוי ישויות. מתאים כשכבר משתמשים ב-spaCy ורוצים API אחד.
- **Stanza** (https://stanfordnlp.github.io/stanza/): ערכת ה-NLP של סטנפורד כוללת מודל עברית עם טוקניזציה, מורפולוגיה, למטיזציה וניתוח תלות. מתאים לצינורות אקדמיים או רב-לשוניים.

לדיוק המרבי בעברית, מודלי Dicta עדיין מובילים. כדאי להשתמש בפריימוורקים האלה כשנוחות האינטגרציה חשובה יותר מאיכות גולמית.

### שלב 7: אתגרים ייחודיים לעברית
- **ניתוח מורפולוגי:** תשתמשו במנתח המורפולוגי של Dicta לפיצול מילים מדויק
- **אין אותיות גדולות:** בעברית אין הבחנה בין אותיות גדולות לקטנות, אז זיהוי ישויות מורכב יותר
- **ימין-לשמאל בקוד:** תוודאו שטיפול ב-bidi עובד כמו שצריך בפעולות מחרוזת
- **עירוב עברית-אנגלית:** נפוץ בטקסט טכנולוגי, לפעמים דורש עיבוד נפרד

## דוגמאות

### דוגמה 1: סיווג טקסט בעברית
המשתמש אומר: "אני צריך לסווג ביקורות לקוחות בעברית כחיוביות או שליליות"
תוצאה: מדריכים לשימוש ב-DictaBERT-Sentiment עם כוונון עדין על נתוני תחום.

### דוגמה 2: זיהוי ישויות בעברית
המשתמש אומר: "חלץ שמות חברות ואנשים ממאמרים בעברית"
תוצאה: משתמשים במודל DictaBERT-NER, מדגימים עם טקסט לדוגמה.

## משאבים מצורפים

### סקריפטים
- `scripts/preprocess_hebrew.py`: נרמול טקסט עברי לפני העברה למודלי NLP (DictaBERT, DictaLM, AlephBERT). מטפל בנרמול Unicode NFC, הסרת ניקוד, ניקוי רווחים, הסרת כתובות URL, נרמול סמל השקל, ופיצול טקסט מעורב עברית-אנגלית. הרצה: `python scripts/preprocess_hebrew.py --help`

### קובצי עזר
- `references/model-comparison.md`: השוואה מפורטת בין מודלי NLP בעברית (DictaLM 3.0, DictaBERT, AlephBERT, NeoDictaBERT, ivrit.ai Whisper) עם דרישות VRAM, מזהי HuggingFace, וטבלת מיפוי בין משימה למודל. תסתכלו בו כשבוחרים מודל מתאים למשימת NLP בעברית ספציפית.

## קישורי עזר

| מקור | כתובת | מה לבדוק |
|------|-------|----------|
| DICTA (HuggingFace) | https://huggingface.co/dicta-il | גרסאות עדכניות של DictaLM ו-DictaBERT, מזהים, הערות שחרור |
| ivrit.ai (HuggingFace) | https://huggingface.co/ivrit-ai | מודלי Whisper מכווננים לעברית, גרסאות דאטה |
| AlephBERT ב-HuggingFace | https://huggingface.co/onlplab/alephbert-base | כרטיס מודל ושימוש ב-AlephBERT |
| אתר ivrit.ai | https://www.ivrit.ai/en/ | גודל הדאטה, רישיון, מאמרים |
| NNLP-IL (קהילת NLP הישראלית) | https://github.com/NNLP-IL | רשימת משאבי NLP בעברית וכלי הערכה |
| דוח טכני DictaLM 3.0 (Dicta) | https://dicta.org.il/publications/DictaLM_3_0___Techincal_Report.pdf | ארכיטקטורה, שושלת מודל הבסיס, דאטה, תוצאות הערכה |
| נקדן Dicta (דיאקריטיזציה) | https://nakdan.dicta.org.il/ | כלי שחזור ניקוד מתארח |
| גישת מפתחים של Dicta | https://dicta.org.il/developers | פרטי API מתארח ותנאי שימוש |
| HebSpacy (spaCy לעברית) | https://github.com/8400TheHealthNetwork/HebSpacy | צינור spaCy לעברית, הוראות התקנה |
| Stanza (מודל עברית) | https://stanfordnlp.github.io/stanza/ | טוקניזציה, מורפולוגיה וניתוח לעברית |

## מלכודות נפוצות
- בעברית אין אותיות גדולות, אז סוכנים לא יכולים להשתמש בהיוריסטיקות NER שמבוססות על רישיות כמו באנגלית. זיהוי ישויות בעברית דורש ניתוח מורפולוגי או מודלים מאומנים.
- מילים בעברית יכולות לכלול כמה תחיליות (מילות יחס, וחיבור, ה' הידיעה) שנכתבות כחלק מהמילה. המחרוזת "ובבית" (ו-ב-בית) היא "וגם בבית" בטוקן אחד. סוכנים עלולים להתייחס אליה כמילה אחת.
- למערכת האותיות העברית יש חמש אותיות סופיות: כ"ף, מ"ם, נו"ן, פ"א, צד"י. סוכנים עלולים לנרמל אותן לצורות הלא-סופיות, וזה שובר התאמת מילים וחיפוש.
- ניקוד כמעט אף פעם לא מופיע בטקסט עברי מודרני. סוכנים שאומנו על טקסט מנוקד עלולים להיכשל על עברית רגילה בלי ניקוד. תמיד תתכננו על בסיס קלט בלי ניקוד.

## פתרון בעיות

### שגיאה: "הטוקניזציה מפיקה תוצאות לא צפויות"
סיבה: המורפולוגיה העברית מפצלת תחיליות (ב-, כ-, ל-, מ-, ש-, ו-)
פתרון: זו התנהגות תקינה. מילים בעברית כמו "בבית" מתפצלות למורפמות.

### שגיאה: "GPU out of memory"
סיבה: DictaLM 3.0 24B דורש בערך 48GB VRAM ב-BF16, וגרסת Nemotron-12B דורשת בערך 24GB.
פתרון: תרדו ל-`dicta-il/DictaLM-3.0-Nemotron-12B-Instruct` (12B), לגרסת 1.7B Thinking GGUF, או תשתמשו בצ'קפוינטים FP8 / W4A16 שפורסמו תחת אותו ארגון (`DictaLM-3.0-24B-Base-FP8` למשל). לחומרת לפטופ, תריצו את ה-1.7B GGUF דרך llama.cpp.
