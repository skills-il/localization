# ערכת כלי NLP לעברית

## הנחיות

### שלב 1: זיהוי משימת ה-NLP
| משימה | מודל מומלץ | גודל | הערות |
|-------|-----------|------|-------|
| יצירת טקסט | DictaLM 3.0 (14B) | 14B | הטוב ביותר ליצירת טקסט בעברית |
| סיווג | DictaBERT | 110M | מהיר, דיוק טוב |
| זיהוי ישויות (NER) | DictaBERT-NER | 110M | אומן על מאגר NER בעברית |
| ניתוח סנטימנט | DictaBERT-Sentiment | 110M | סיווג סנטימנט בעברית |
| הטמעה/חיפוש | AlephBERT | 110M | מתאים למשימות דמיון |
| דיבור-לטקסט | ivrit.ai Whisper | משתנה | 22K+ שעות נתוני אימון |
| תרגום | DictaLM 3.0 (7B) | 7B | עברית מ/אל אנגלית |
| קריאת כלים | DictaLM 3.0 Chat | 7B/14B | תומך בקריאת פונקציות |

### שלב 2: התקנה וטעינת מודל

**DictaBERT (משימות סיווג):**
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("dicta-il/dictabert")
model = AutoModelForSequenceClassification.from_pretrained("dicta-il/dictabert")
```

**DictaLM 3.0 (יצירת טקסט):**
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("dicta-il/dictalm-3.0-7b-chat")
model = AutoModelForCausalLM.from_pretrained("dicta-il/dictalm-3.0-7b-chat")
```

**ivrit.ai Whisper (דיבור-לטקסט):**
```python
import whisper
# Use ivrit.ai fine-tuned model
model = whisper.load_model("ivrit-ai/whisper-large-v3-he")
```

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
- **ללא אותיות גדולות:** בעברית אין הבחנה בין אותיות גדולות לקטנות — זיהוי ישויות מורכב יותר
- **ימין-לשמאל בקוד:** יש להבטיח טיפול תקין ב-bidi בפעולות מחרוזת
- **עירוב עברית-אנגלית:** נפוץ בטקסט טכנולוגי, עשוי לדרוש עיבוד נפרד

## משאבים
- מודלים של Dicta: `https://huggingface.co/dicta-il`
- ivrit.ai: `https://huggingface.co/ivrit-ai`
- AlephBERT: `https://huggingface.co/onlplab/alephbert-base`
- משאבי NNLP-IL: משאבי קהילת NLP עברית

## דוגמאות

### דוגמה 1: סיווג טקסט עברי
המשתמש אומר: "אני צריך לסווג ביקורות לקוחות בעברית כחיוביות או שליליות"
תוצאה: הדרכה לשימוש ב-DictaBERT-Sentiment עם כוונון עדין על נתוני תחום.

### דוגמה 2: זיהוי ישויות בעברית
המשתמש אומר: "חלץ שמות חברות ואנשים ממאמרים בעברית"
תוצאה: שימוש במודל DictaBERT-NER, הדגמה עם טקסט לדוגמה.

## משאבים מצורפים

### סקריפטים
- `scripts/preprocess_hebrew.py` — נרמול טקסט עברי לפני הזנה למודלי NLP (DictaBERT, DictaLM, AlephBERT). מטפל בנרמול Unicode NFC, הסרת ניקוד, ניקוי רווחים, הסרת כתובות URL, נרמול סמל השקל, ופיצול טקסט מעורב עברית-אנגלית. הרצה: `python scripts/preprocess_hebrew.py --help`

### קובצי עזר
- `references/model-comparison.md` — השוואה מפורטת בין מודלי NLP לעברית (DictaLM 3.0, DictaBERT, AlephBERT, ivrit.ai Whisper, Hebrew-Gemma) עם דרישות VRAM, מזהי HuggingFace, וטבלת מיפוי משימה-למודל. יש לעיין בו בעת בחירת מודל מתאים למשימת NLP בעברית ספציפית.

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
סיבה: DictaLM 14B דורש כ-28GB VRAM
פתרון: שימוש בגרסת 7B או 1.7B, או קוונטיזציה עם bitsandbytes (4-bit).
