# ערכת כלי NLP לעברית

## הנחיות

### שלב 1: זיהוי משימת ה-NLP
| משימה | מודל מומלץ | מזהה HuggingFace | גודל | הערות |
|-------|-----------|------------------|------|-------|
| יצירת טקסט (איכות מרבית) | DictaLM 3.0 24B Base | `dicta-il/DictaLM-3.0-24B-Base` | 24B | המודל החזק ביותר בעברית, מבוסס Mistral-Small-3.1-24B |
| יצירת טקסט (קל יותר) | DictaLM 3.0 Nemotron Instruct | `dicta-il/DictaLM-3.0-Nemotron-12B-Instruct` | 12B | מכוון להוראות, טביעת רגל קטנה יותר |
| היסק / שרשרת מחשבה | DictaLM 3.0 24B Thinking | `dicta-il/DictaLM-3.0-24B-Thinking` | 24B | מייצר בלוק חשיבה מפורש לפני התשובה |
| קצה / לפטופ | DictaLM 3.0 1.7B Thinking (GGUF) | `dicta-il/DictaLM-3.0-1.7B-Thinking-GGUF` | 1.7B | רץ על CPU דרך llama.cpp |
| סיווג / מילוי מסכה | DictaBERT | `dicta-il/dictabert` | 184M | מהיר, דיוק טוב |
| זיהוי ישויות (NER) | DictaBERT NER | `dicta-il/dictabert-ner` | 184M | מזהה PER, GPE, TIMEX, TTL |
| ניתוח סנטימנט | DictaBERT Sentiment | `dicta-il/dictabert-sentiment` | 184M | סיווג סנטימנט בעברית |
| מורפולוגיה | DictaBERT Morph | `dicta-il/dictabert-morph` | 184M | פיצול תחיליות וחלקי דיבר |
| שאלות ותשובות | DictaBERT HeQ | `dicta-il/dictabert-heq` | 184M | QA חילוצי בעברית |
| הטמעות (מודרני) | NeoDictaBERT Bilingual Embed | `dicta-il/neodictabert-bilingual-embed` | 400M | הטמעות משפטים דו-לשוניות עברית-אנגלית |
| הטמעות (מדור קודם) | AlephBERT | `onlplab/alephbert-base` | 110M | בסיס ותיק יותר לדמיון |
| דיבור-לטקסט | ivrit.ai Whisper v3 | `ivrit-ai/whisper-large-v3` | 1.55B | כוונון עדין על 22K+ שעות של אודיו בעברית |
| דיבור-לטקסט (מהיר) | ivrit.ai Whisper v3 Turbo CT2 | `ivrit-ai/whisper-large-v3-turbo-ct2` | 809M | מנוע CTranslate2, פי 3 מהיר בערך |

### שלב 2: התקנה וטעינת מודל

**DictaBERT (משימות סיווג):**
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("dicta-il/dictabert")
model = AutoModelForSequenceClassification.from_pretrained("dicta-il/dictabert")
```

**DictaLM 3.0 (יצירת טקסט, 12B Instruct):**
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("dicta-il/DictaLM-3.0-Nemotron-12B-Instruct")
model = AutoModelForCausalLM.from_pretrained("dicta-il/DictaLM-3.0-Nemotron-12B-Instruct")
```

לאיכות מרבית, החלף ל-`dicta-il/DictaLM-3.0-24B-Base`. למשימות היסק (מתמטיקה, לוגיקה רב-שלבית), השתמש ב-`dicta-il/DictaLM-3.0-24B-Thinking`, שכותב את שרשרת המחשבה בתוך בלוק thinking מפורש לפני התשובה הסופית.

**ivrit.ai Whisper (דיבור-לטקסט):**
```python
from transformers import pipeline
# מודל ASR עברי מכוונן עדין מ-ivrit.ai, מבוסס openai/whisper-large-v3
pipe = pipeline("automatic-speech-recognition", model="ivrit-ai/whisper-large-v3")
result = pipe("audio.wav", generate_kwargs={"language": "he"})
```
לזמן תגובה נמוך יותר, השתמש ב-`ivrit-ai/whisper-large-v3-turbo-ct2` דרך `faster-whisper` (מנוע CTranslate2, כפי 3 מהיר יותר ב-GPU).

### שלב 3: עיבוד מקדים של טקסט עברי
לפני הזנת טקסט למודלים:
1. **נרמול:** הסרת רווחים מיותרים, נרמול Unicode (NFC)
2. **טיפול בניקוד:** הסרת סימני ניקוד אלא אם נדרשים במפורש
3. **טיפול באנגלית:** החלטה אם לשמור, לתרגם או לסמן טוקנים באנגלית
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

### שלב 4: התמודדות עם אתגרים ייחודיים לעברית
- **ניתוח מורפולוגי:** שימוש במנתח המורפולוגי של Dicta לפיצול מילים מדויק
- **ללא אותיות גדולות:** בעברית אין הבחנה בין אותיות גדולות לקטנות, כך שזיהוי ישויות מורכב יותר
- **ימין-לשמאל בקוד:** יש להבטיח טיפול תקין ב-bidi בפעולות מחרוזת
- **עירוב עברית-אנגלית:** נפוץ בטקסט טכנולוגי, עשוי לדרוש עיבוד נפרד

## דוגמאות

### דוגמה 1: סיווג טקסט עברי
המשתמש אומר: "אני צריך לסווג ביקורות לקוחות בעברית כחיוביות או שליליות"
תוצאה: הדרכה לשימוש ב-DictaBERT-Sentiment עם כוונון עדין על נתוני תחום.

### דוגמה 2: זיהוי ישויות בעברית
המשתמש אומר: "חלץ שמות חברות ואנשים ממאמרים בעברית"
תוצאה: שימוש במודל DictaBERT-NER, הדגמה עם טקסט לדוגמה.

## משאבים מצורפים

### סקריפטים
- `scripts/preprocess_hebrew.py`: נרמול טקסט עברי לפני הזנה למודלי NLP (DictaBERT, DictaLM, AlephBERT). מטפל בנרמול Unicode NFC, הסרת ניקוד, ניקוי רווחים, הסרת כתובות URL, נרמול סמל השקל, ופיצול טקסט מעורב עברית-אנגלית. הרצה: `python scripts/preprocess_hebrew.py --help`

### קובצי עזר
- `references/model-comparison.md`: השוואה מפורטת בין מודלי NLP לעברית (DictaLM 3.0, DictaBERT, AlephBERT, NeoDictaBERT, ivrit.ai Whisper) עם דרישות VRAM, מזהי HuggingFace, וטבלת מיפוי משימה-למודל. יש לעיין בו בעת בחירת מודל מתאים למשימת NLP בעברית ספציפית.

## קישורי עזר

| מקור | כתובת | מה לבדוק |
|------|-------|----------|
| DICTA (HuggingFace) | https://huggingface.co/dicta-il | גרסאות עדכניות של DictaLM ו-DictaBERT, מזהים, הערות שחרור |
| ivrit.ai (HuggingFace) | https://huggingface.co/ivrit-ai | מודלי Whisper מכווננים לעברית, גרסאות דאטה |
| AlephBERT ב-HuggingFace | https://huggingface.co/onlplab/alephbert-base | כרטיס מודל ושימוש ב-AlephBERT |
| אתר ivrit.ai | https://www.ivrit.ai/en/ | גודל הדאטה, רישיון, מאמרים |
| NNLP-IL (קהילת NLP ישראלית) | https://github.com/NNLP-IL | רשימת משאבי NLP לעברית וכלי הערכה |
| מאמר DictaLM 3.0 | https://arxiv.org/pdf/2309.14568 | ארכיטקטורה, דאטה, תוצאות הערכה |

## מלכודות נפוצות
- בעברית אין אותיות גדולות, כך שסוכנים לא יכולים להשתמש בהיוריסטיקות NER מבוססות רישיות שעובדות באנגלית. זיהוי ישויות בעברית דורש ניתוח מורפולוגי או מודלים מאומנים.
- מילים בעברית יכולות לכלול מספר תחיליות (מילות יחס, מילות חיבור, ה' הידיעה) שנכתבות כחלק מהמילה. המחרוזת "ובבית" (ו-ב-בית) היא "וגם בבית" כטוקן אחד. סוכנים עלולים להתייחס אליו כמילה אחת.
- למערכת האותיות העברית חמש צורות סופיות (סופיות): כ"ף, מ"ם, נו"ן, פ"א, צד"י. סוכנים עלולים לנרמל אותן לצורות הלא-סופיות, מה ששובר התאמת מילים וחיפוש.
- ניקוד כמעט לעולם לא מופיע בטקסט עברי מודרני. סוכנים שאומנו על טקסט מנוקד עלולים להיכשל על עברית רגילה ללא ניקוד. תמיד יש לתכנן לקלט ללא ניקוד.

## פתרון בעיות

### שגיאה: "טוקניזציה מפיקה תוצאות בלתי צפויות"
סיבה: המורפולוגיה העברית מפצלת תחיליות (ב-, כ-, ל-, מ-, ש-, ו-)
פתרון: זו התנהגות תקינה. מילים בעברית כמו "בבית" (in the house) מפוצלות למורפמות.

### שגיאה: "GPU out of memory"
סיבה: DictaLM 3.0 24B דורש כ-48GB VRAM ב-BF16, וגרסת Nemotron-12B דורשת כ-24GB.
פתרון: ירד ל-`dicta-il/DictaLM-3.0-Nemotron-12B-Instruct` (12B), לגרסת 1.7B Thinking GGUF, או השתמש בצ׳קפוינטים FP8 / W4A16 שפורסמו תחת אותו ארגון (למשל `DictaLM-3.0-24B-Base-FP8`). לחומרת לפטופ, הרץ את ה-1.7B GGUF דרך llama.cpp.
