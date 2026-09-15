# ערכת כלי NLP לעברית

## הנחיות

### שלב 1: לזהות את משימת ה-NLP
| משימה | מודל מומלץ | מזהה HuggingFace | גודל | הערות |
|-------|-----------|------------------|------|-------|
| יצירת טקסט (איכות מרבית) | DictaLM 3.0 24B Base | `dicta-il/DictaLM-3.0-24B-Base` | 24B | המודל החזק ביותר בעברית, מבוסס על Mistral-Small-3.1-24B. רישיון Apache-2.0 |
| יצירת טקסט (קל יותר) | DictaLM 3.0 Nemotron Instruct | `dicta-il/DictaLM-3.0-Nemotron-12B-Instruct` | 12B | מכוון להוראות. רישיון NVIDIA Open Model License, לא Apache |
| היסק / שרשרת מחשבה | DictaLM 3.0 24B Thinking | `dicta-il/DictaLM-3.0-24B-Thinking` | 24B | מייצר בלוק חשיבה מפורש לפני התשובה |
| קצה / לפטופ | DictaLM 3.0 1.7B Thinking (GGUF) | `dicta-il/DictaLM-3.0-1.7B-Thinking-GGUF` | 1.7B | רץ על CPU דרך llama.cpp |
| מילוי מסכה (בסיס) | DictaBERT | `dicta-il/dictabert` | 184M | מודל בסיס; לסיווג יש לכוונן או להשתמש במודל ייעודי |
| זיהוי ישויות (NER) | DictaBERT NER | `dicta-il/dictabert-ner` | 184M | 13 סוגי ישויות, ביניהם PER, ORG, LOC, GPE, FAC, TIMEX, TTL |
| ניתוח סנטימנט | DictaBERT Sentiment | `dicta-il/dictabert-sentiment` | 184M | עובד מהקופסה, בלי אימון נוסף |
| מורפולוגיה / פיצול | DictaBERT Joint | `dicta-il/dictabert-joint` | 184M | פיצול תחיליות, חלקי דיבר, למה וניתוח תלות |
| שאלות ותשובות | DictaBERT HeQ | `dicta-il/dictabert-heq` | 184M | QA חילוצי בעברית |
| הטמעות (מודרני) | NeoDictaBERT Bilingual Embed | `dicta-il/neodictabert-bilingual-embed` | ~363M | הטמעות משפטים דו-לשוניות עברית-אנגלית, 768 ממדים |
| הטמעות (ישן יותר) | AlephBERT | `onlplab/alephbert-base` | BERT-base | בסיס ותיק יותר לדמיון |
| דיבור-לטקסט | ivrit.ai Whisper v3 | `ivrit-ai/whisper-large-v3` | 1.55B | אומן על כ-5,000 שעות מתוך הקורפוס של ivrit.ai (מליאות הכנסת, תמלולי המון, הקראות) |
| דיבור-לטקסט (מהיר) | ivrit.ai Whisper v3 Turbo CT2 | `ivrit-ai/whisper-large-v3-turbo-ct2` | 809M | גרסת CTranslate2 עבור `faster-whisper` |

קורפוס האודיו העברי המלא של ivrit.ai מונה יותר מ-22,000 שעות. כל מודל מפרט בכרטיס שלו את נתוני האימון שלו, והמספרים שונים: whisper-large-v3 מציין כ-5,000 שעות, ואילו גרסת turbo-ct2 מציינת 295 שעות של תמלולי המון ועוד 93 שעות של דיבור שתומלל מקצועית ממקורות אחרים.

חלק מהמודלים כוללים קוד מותאם ודורשים `trust_remote_code=True` (Nemotron, `dictabert-joint`, `dictabert-large-char-menaked`, `neodictabert-bilingual-embed`). הדגל הזה מריץ קוד Python ממאגר המודל על המחשב שלכם, אז כדאי לקרוא את כרטיס המודל ולנעול revision בפרודקשן.

### שלב 2: התקנה, טעינה והרצה

**סנטימנט (מוכן לשימוש, בלי כוונון):**
```python
from transformers import pipeline

oracle = pipeline('sentiment-analysis', model='dicta-il/dictabert-sentiment')
print(oracle(['אני אוהב את השירות']))
```

**זיהוי ישויות (ישויות מקובצות):**
```python
from transformers import pipeline
from tokenizers.decoders import WordPiece

oracle = pipeline('ner', model='dicta-il/dictabert-ner', aggregation_strategy='simple')
# with aggregation_strategy='simple' the tokenizer needs a decoder, per the model card
oracle.tokenizer.backend_tokenizer.decoder = WordPiece()
print(oracle('דוד בן-גוריון נולד בפולין'))
```
בלי שורת ה-decoder, הישויות המקובצות חוזרות כשברי `##` של word-pieces.

**מודל בסיס DictaBERT (מילוי מסכה):**
```python
from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("dicta-il/dictabert")
model = AutoModelForMaskedLM.from_pretrained("dicta-il/dictabert")
```
המודל `dicta-il/dictabert` הוא מודל בסיס מסוג masked-LM, ללא ראש סיווג. אל תטענו אותו עם `AutoModelForSequenceClassification` ותריצו חיזוי, זה יוצר ראש סיווג מאותחל אקראית ומחזיר תוצאות חסרות משמעות. לסיווג, או כווננו אותו על נתונים מתויגים תחילה, או השתמשו במודל ייעודי מוכן כמו `dicta-il/dictabert-sentiment` או `dicta-il/dictabert-ner`.

**מורפולוגיה ופיצול תחיליות (dictabert-joint):**
```python
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('dicta-il/dictabert-joint')
model = AutoModel.from_pretrained('dicta-il/dictabert-joint', trust_remote_code=True)
model.eval()
print(model.predict(['ובבית הספר למדנו'], tokenizer, output_style='json'))
```

**הטמעות משפטים (NeoDictaBERT):**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("dicta-il/neodictabert-bilingual-embed", trust_remote_code=True)
query_embeddings = model.encode_query(["query: מתכון לעוגת שוקולד"])
document_embeddings = model.encode_document(["עוגת שוקולד פשוטה בעשר דקות"])
```
שמרו על הקידומת `query: ` בשאילתות כמו בכרטיס המודל; בלעדיה איכות האחזור יורדת.

**יצירת טקסט עם DictaLM 3.0 (12B Instruct):**
```python
from transformers import pipeline

generator = pipeline('text-generation', model="dicta-il/DictaLM-3.0-Nemotron-12B-Instruct", trust_remote_code=True)
```
להגשה בשרת, כרטיס המודל ממליץ על vLLM (`vllm serve dicta-il/DictaLM-3.0-Nemotron-12B-Instruct --enable-auto-tool-choice --tool-call-parser hermes --trust-remote-code`). לאיכות המרבית, וגם לרישיון Apache-2.0, השתמשו ב-`dicta-il/DictaLM-3.0-24B-Base`. למשימות היסק, השתמשו ב-`dicta-il/DictaLM-3.0-24B-Thinking`, שכותב את שרשרת המחשבה בתוך בלוק thinking מפורש לפני התשובה הסופית.

**דיבור-לטקסט עם ivrit.ai Whisper (faster-whisper):**
```python
import faster_whisper

model = faster_whisper.WhisperModel('ivrit-ai/whisper-large-v3-turbo-ct2')
segs, _ = model.transcribe('media-file', language='he')
print(' '.join(s.text for s in segs))
```
המשתנה `segs` הוא generator, ולכן התמלול רץ רק כשעוברים עליו. על CPU העבירו `device="cpu", compute_type="int8"`; הפרמטר `vad_filter=True` מדלג על שקט, ו-`word_timestamps=True` מחזיר תזמון לכל מילה לכתוביות. כדי לעבוד עם transformers בלבד, טענו את `ivrit-ai/whisper-large-v3` עם `pipeline("automatic-speech-recognition", ...)` ו-`generate_kwargs={"language": "he"}`.

### שלב 3: עיבוד מקדים של טקסט עברי
לפני שמעבירים טקסט למודלים:
1. **נרמול:** הסרת רווחים מיותרים, נרמול Unicode (NFC)
2. **טיפול בניקוד:** הסרת סימני ניקוד אלא אם הם באמת נחוצים
3. **טיפול באנגלית:** להחליט אם לשמור, לתרגם או לסמן טוקנים באנגלית
4. **טוקניזציה:** הטוקנייזרים של DictaBERT ו-AlephBERT מפצלים מילים ליחידות WordPiece, לא למורפמות. לפיצול תחיליות אמיתי (לאינדוקס חיפוש, ספירה, למות) הריצו את `dictabert-joint` משלב 2

```python
import re
import unicodedata

def preprocess_hebrew(text):
    # Normalize Unicode
    text = unicodedata.normalize('NFC', text)
    # Remove niqqud and cantillation, but keep maqaf U+05BE and other punctuation in the block
    text = re.sub(r'[֑-ׇֽֿׁׂׅׄ]', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```
הסרה של כל הטווח U+0591 עד U+05C7 היא באג נפוץ: היא מוחקת גם את המקף העברי ומדביקה מילים (`עולם־גדול` הופך ל-`עולםגדול`).

### שלב 4: שחזור ניקוד (דיאקריטיזציה)

העיבוד המקדים שלמעלה *מסיר* ניקוד. המשימה ההפוכה, *הוספת* ניקוד חזרה לטקסט לא מנוקד, נקראת דיאקריטיזציה והיא בעיה מרכזית בפני עצמה ב-NLP עברי (שימושית להמרת טקסט לדיבור, ללימוד שפה ולפתרון דו-משמעות).

הנקדן של Dicta הוא הכלי הסטנדרטי. מודל ברמת התו מפורסם ב-HuggingFace:

```python
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('dicta-il/dictabert-large-char-menaked')
model = AutoModel.from_pretrained('dicta-il/dictabert-large-char-menaked', trust_remote_code=True)
model.eval()

# predict takes a list of sentences and returns a list of vocalized sentences
vocalized = model.predict(['שלום עולם'], tokenizer)
```

הערות:
- צריך `trust_remote_code=True` כי המודל כולל ראש `predict` מותאם. כדאי לעבור על כרטיס המודל לפני שמפעילים את זה.
- לפי כרטיס המודל, הוא מיועד לפרוזה עברית מודרנית ולא לטקסטים מקראיים, רבניים, קדם-מודרניים או שיריים.
- דיאקריטיזציה היא דו-משמעית: לאותו טקסט עיצורי יכולות להיות כמה נקודות תקינות לפי ההקשר. כדאי להתייחס לפלט כניחוש מיטבי, לא כאמת מוחלטת.
- לניקוד ברמת משפט שלם עם הקשר מורפולוגי, הנקדן המתארח של Dicta (ראו שלב 5) בדרך כלל טוב יותר ממודל תווים גולמי.

### שלב 5: שירותי REST מתארחים של Dicta

אם לא רוצים להריץ מודלים מקומית, Dicta חושפת את הכלים שלה (נקדן, מורפולוגיה ועוד) כשירותי ווב מתארחים. זה מתאים לשימוש בנפח נמוך, לאבות טיפוס, או לסביבות בלי GPU.

- נקדן (דיאקריטיזציה): https://nakdan.dicta.org.il/
- גישת מפתחים ופרטי API: https://dicta.org.il/developers

כדאי לאמת את מבנה ה-endpoint העדכני, פורמט הבקשה, מגבלות הקצב ותנאי השימוש בעמוד המפתחים לפני אינטגרציה, כי חוזי API מתארחים משתנים. אל תניחו כתובת endpoint או סכמת payload, תסתכלו בתיעוד המפתחים הרשמי.

### שלב 6: נקודות כניסה חלופיות ל-NLP

המחסניות `Dicta` ו-`ivrit.ai` הן העיקריות בעברית, אבל גם שני פריימוורקים כלליים של NLP כוללים צינורות לעברית:

- **HebSpacy** (https://github.com/8400TheHealthNetwork/HebSpacy): צינור spaCy שהמודל המפורסם שלו, `he_ner_news_trf`, הוא מודל זיהוי ישויות מבוסס AlephBERT עם 16 סוגי ישויות. הוא לא כולל תיוג חלקי דיבר או למטיזציה. מתאים כשכבר משתמשים ב-spaCy וצריכים זיהוי ישויות בעברית. בדקו את תאריך הקומיט האחרון במאגר ונעלו את גרסת spaCy לפני שמאמצים אותו.
- **Stanza** (https://stanfordnlp.github.io/stanza/): ערכת ה-NLP של סטנפורד כוללת מודל עברית עם טוקניזציה, מורפולוגיה, למטיזציה וניתוח תלות. מתאים לצינורות אקדמיים או רב-לשוניים.

לדיוק המרבי בעברית, מודלי Dicta עדיין מובילים. כדאי להשתמש בפריימוורקים האלה כשנוחות האינטגרציה חשובה יותר מאיכות גולמית.

### שלב 7: אתגרים ייחודיים לעברית
- **ניתוח מורפולוגי:** תשתמשו ב-`dictabert-joint` (או בכלים המתארחים של Dicta) לפיצול מילים מדויק
- **אין אותיות גדולות:** בעברית אין הבחנה בין אותיות גדולות לקטנות, אז זיהוי ישויות מורכב יותר
- **ימין-לשמאל בקוד:** תוודאו שטיפול ב-bidi עובד כמו שצריך בפעולות מחרוזת
- **עירוב עברית-אנגלית:** נפוץ בטקסט טכנולוגי, לפעמים דורש עיבוד נפרד
- **הרישיונות שונים בין המודלים:** מודלי DictaBERT ברישיון CC-BY-4.0, DictaLM 24B ב-Apache-2.0, וגרסת Nemotron 12B ברישיון NVIDIA Open Model License. בדקו לפני שימוש מסחרי

## דוגמאות

### דוגמה 1: סיווג טקסט בעברית
המשתמש אומר: "אני צריך לסווג ביקורות לקוחות בעברית כחיוביות או שליליות"
תוצאה: מריצים קודם את `dicta-il/dictabert-sentiment` דרך ה-pipeline של `sentiment-analysis` (הוא עובד בלי אימון). מכווננים אותו על ביקורות מתויגות מהתחום רק אם הדיוק על מדגם מהנתונים שלכם לא מספיק.

### דוגמה 2: זיהוי ישויות בעברית
המשתמש אומר: "חלץ שמות חברות ואנשים ממאמרים בעברית"
תוצאה: משתמשים ב-pipeline של `dicta-il/dictabert-ner` עם `aggregation_strategy='simple'` וה-decoder של WordPiece, ושומרים את הישויות מסוג `ORG` ו-`PER`.

### דוגמה 3: תמלול הקלטה בעברית
המשתמש אומר: "תמלל פודקאסט של שעה בעברית לטקסט"
תוצאה: משתמשים ב-`faster-whisper` עם `ivrit-ai/whisper-large-v3-turbo-ct2`, `language='he'` ו-`vad_filter=True`; עוברים על ה-generator של הקטעים וכותבים את הטקסט של כל קטע עם חותמות הזמן שלו.

## משאבים מצורפים

### סקריפטים
- `scripts/preprocess_hebrew.py`: נרמול טקסט עברי לפני העברה למודלי NLP (DictaBERT, DictaLM, AlephBERT). מטפל בנרמול Unicode NFC, הסרת ניקוד (תוך שמירה על המקף העברי), ניקוי רווחים, הסרת כתובות URL, נרמול מפרידי אלפים וקיצור השקל, ופיצול טקסט מעורב עברית-אנגלית. הרצה: `python scripts/preprocess_hebrew.py --help`

### קובצי עזר
- `references/model-comparison.md`: השוואה מפורטת בין מודלי NLP בעברית (DictaLM 3.0, DictaBERT, AlephBERT, NeoDictaBERT, ivrit.ai Whisper) עם דרישות VRAM, מזהי HuggingFace, רישיונות וטבלת מיפוי בין משימה למודל. תסתכלו בו כשבוחרים מודל מתאים למשימת NLP בעברית ספציפית.

## קישורי עזר

| מקור | כתובת | מה לבדוק |
|------|-------|----------|
| DICTA (HuggingFace) | https://huggingface.co/dicta-il | גרסאות עדכניות של DictaLM ו-DictaBERT, מזהים, רישיונות |
| ivrit.ai (HuggingFace) | https://huggingface.co/ivrit-ai | מודלי Whisper מכווננים לעברית, גרסאות דאטה |
| AlephBERT ב-HuggingFace | https://huggingface.co/onlplab/alephbert-base | כרטיס מודל ושימוש ב-AlephBERT |
| אתר ivrit.ai | https://www.ivrit.ai/en/ivrit-ai-2/ | גודל הקורפוס, רישיון |
| NNLP-IL (קהילת NLP הישראלית) | https://github.com/NNLP-IL | רשימת משאבי NLP בעברית וכלי הערכה |
| דוח טכני DictaLM 3.0 (Dicta) | https://dicta.org.il/publications/DictaLM_3_0___Techincal_Report.pdf | ארכיטקטורה, שושלת מודל הבסיס, דאטה, תוצאות הערכה |
| נקדן Dicta (דיאקריטיזציה) | https://nakdan.dicta.org.il/ | כלי שחזור ניקוד מתארח |
| גישת מפתחים של Dicta | https://dicta.org.il/developers | פרטי API מתארח ותנאי שימוש |
| faster-whisper | https://github.com/SYSTRAN/faster-whisper | `WhisperModel`, `compute_type`, VAD וחותמות זמן למילים |
| Stanza (מודל עברית) | https://stanfordnlp.github.io/stanza/ | טוקניזציה, מורפולוגיה וניתוח לעברית |

## מלכודות נפוצות
- בעברית אין אותיות גדולות, אז סוכנים לא יכולים להשתמש בהיוריסטיקות NER שמבוססות על רישיות כמו באנגלית. זיהוי ישויות בעברית דורש ניתוח מורפולוגי או מודלים מאומנים.
- מילים בעברית יכולות לכלול כמה תחיליות (מילות יחס, וחיבור, ה' הידיעה) שנכתבות כחלק מהמילה. המחרוזת "ובבית" (ו-ב-בית) היא "וגם בבית" בטוקן אחד. סוכנים עלולים להתייחס אליה כמילה אחת.
- למערכת האותיות העברית יש חמש אותיות סופיות: כ"ף, מ"ם, נו"ן, פ"א, צד"י. סוכנים עלולים לנרמל אותן לצורות הלא-סופיות, וזה שובר התאמת מילים וחיפוש.
- ניקוד כמעט אף פעם לא מופיע בטקסט עברי מודרני. סוכנים שאומנו על טקסט מנוקד עלולים להיכשל על עברית רגילה בלי ניקוד. תמיד תתכננו על בסיס קלט בלי ניקוד.
- סוכנים נוטים "לנרמל" את קיצור השקל בהחלפת מחרוזת פשוטה של ש ו-ח, מה שמשנה גם מילים רגילות כמו שחר ומשחק. התאימו אותו רק כטוקן עצמאי.

## פתרון בעיות

### שגיאה: "הטוקנים נראים כמו שברים עם ## בתוכם"
סיבה: DictaBERT ו-AlephBERT משתמשים בטוקניזציית WordPiece, שמפצלת מילים נדירות ליחידות תת-מילה. אלה לא מורפמות.
פתרון: לזיהוי ישויות, הגדירו `aggregation_strategy='simple'` יחד עם ה-decoder של WordPiece משלב 2. לפיצול תחיליות אמיתי, השתמשו ב-`dictabert-joint`.

### שגיאה: "GPU out of memory"
סיבה: ב-BF16 המשקולות לבדן תופסות כ-2 בייטים לפרמטר, כלומר בערך 48GB ל-DictaLM 3.0 24B ובערך 24GB לגרסת Nemotron-12B, עוד לפני KV cache ואקטיבציות.
פתרון: תרדו ל-`dicta-il/DictaLM-3.0-Nemotron-12B-Instruct` (12B), לגרסת 1.7B Thinking GGUF, או תשתמשו בצ'קפוינטים FP8 / W4A16 שפורסמו תחת אותו ארגון (`DictaLM-3.0-24B-Base-FP8` למשל). לחומרת לפטופ, תריצו גרסת GGUF דרך llama.cpp.
