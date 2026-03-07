# יומן שבת עם GWS

## הוראות

### שלב 1: אימות הגדרת GWS CLI

לפני תזמון, יש לוודא שכלי Google Workspace CLI מותקן ומאומת.

```bash
# התקנת gws גלובלית (או שימוש ב-npx)
npm install -g @google/gws

# אימות מול חשבון Google
gws auth login

# אימות סטטוס ההתחברות
gws auth status
```

אם המשתמש לא אימת, יש להנחות אותו דרך `gws auth login` תחילה. להגדרה ברמת הפרויקט (חשבונות שירות, דומיין Workspace), יש להשתמש ב-`gws auth setup`.

### שלב 2: זיהוי הקשר התזמון

יש לזהות מה המשתמש צריך ואילו אילוצים רלוונטיים.

| הקשר | אילוצים עיקריים | פקודת GWS |
|-------|-----------------|-----------|
| יצירת אירוע בודד | בדיקת גבולות שבת, בדיקת חגים | `gws calendar insert` |
| צפייה ביומן שבועי | סינון שבוע עבודה ישראלי (א'-ה') | `gws calendar agenda` |
| חסימת זמן מיקוד | גבול ערב שבת (יום שישי 14:00) | `gws calendar insert` (חוזר) |
| מציאת חלונות פנויים | מניעת שבת + חגים | `gws calendar agenda` + ניתוח פערים |
| פגישות חוזרות | תבנית שבוע עבודה ישראלי (א'-ה') | `gws calendar insert --recurrence` |
| הזמנות מרובות | ריבוי משתתפים עם מודעות לאזורי זמן | מתכון batch-event-invites |
| תזמון מחדש | פתרון התנגשויות חגים | מתכון reschedule-meeting |
| חוצה אזורי זמן | חפיפת ישראל/ארה"ב עם שמירה על שבת | `gws calendar insert` + חישובי זמן |

### שלב 3: שליפת נתוני לוח שנה עברי

לפני יצירת או שינוי אירועים, יש לבדוק זמני שבת וחגים קרובים באמצעות HebCal API. ניתן להשתמש ב-`scripts/check_holidays.py` לשאילתות תכנותיות.

**זמני שבת לתאריך ספציפי:**
```bash
curl -s "https://www.hebcal.com/shabbat?cfg=json&geonameid=293397&M=on" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for item in data.get('items', []):
    cat = item.get('category', '')
    if cat in ('candles', 'havdalah'):
        print(f\"{cat}: {item['date']}\")
"
```

**בדיקת חגים לטווח תאריכים:**
```bash
# בדיקת חגים לחודש נתון (פורמט YYYY-MM)
python3 scripts/check_holidays.py --month 2026-09
```

**נתוני עיון מרכזיים (ראו `references/jewish-calendar-reference.md`):**

| חג | אנגלית | משך | השפעה על תזמון |
|----|--------|-----|----------------|
| שבת | Shabbat | שבועי (שקיעת שישי - שקיעת שבת) | ללא אירועים אחרי שישי 14:00 |
| ראש השנה | Rosh Hashana | יומיים (א'-ב' תשרי) | חסימה מלאה |
| יום כיפור | Yom Kippur | יום אחד (י' תשרי) | חסימה מלאה, ללא עבודה אחה"צ ערב יו"כ |
| סוכות | Sukkot | 7+1 ימים | ימים ראשון/אחרון חסימה מלאה, חול המועד חלקי |
| פסח | Pesach | 7 ימים | ימים ראשון/אחרון חסימה מלאה, חול המועד חלקי |
| שבועות | Shavuot | יום אחד | חסימה מלאה |
| יום הזיכרון | Yom HaZikaron | יום אחד | יום זיכרון לאומי, תזמון מצומצם |
| יום השואה | Yom HaShoah | יום אחד | יום זיכרון לאומי, תזמון מצומצם |

**מוסכמות עסקיות ישראליות:**
- שבוע עבודה: ראשון עד חמישי
- שישי: חצי יום, רוב המשרדים סוגרים עד 13:00-14:00
- ערב חג: משרדים סוגרים מוקדם, בדרך כלל עד 13:00
- אזור זמן: `Asia/Jerusalem` (UTC+2 חורף / UTC+3 קיץ, IST/IDT)

### שלב 4: יצירת אירועים עם בדיקת גבולות שבת

תמיד יש לאמת תזמון אירועים מול גבולות שבת וחגים לפני הוספה.

**יצירת אירוע בודד עם בדיקת גבולות:**
```bash
# שלב 1: בדיקה אם הזמן המבוקש מתנגש עם שבת
python3 scripts/check_holidays.py --date 2026-03-13

# שלב 2: אם ברור, יצירת האירוע
gws calendar insert \
  --summary "תכנון ספרינט" \
  --start "2026-03-11T10:00:00" \
  --end "2026-03-11T11:00:00" \
  --timezone "Asia/Jerusalem" \
  --description "פגישת תכנון ספרינט שבועית" \
  --attendees "team@company.co.il"
```

**אירוע ביום שישי עם אכיפת גבול זמן אוטומטית:**
```bash
# לאירועי שישי, אכיפת גבול 14:00
# חישוב: אם end_time > שישי 14:00 IST, דחייה או התאמה
gws calendar insert \
  --summary "סנכרון קצר" \
  --start "2026-03-13T11:00:00" \
  --end "2026-03-13T12:00:00" \
  --timezone "Asia/Jerusalem" \
  --description "סנכרון לפני סוף שבוע (מסתיים לפני ערב שבת)"
```

**מצב הרצת יבש לאימות:**
```bash
gws calendar insert \
  --summary "פגישת צוות" \
  --start "2026-03-11T14:00:00" \
  --end "2026-03-11T15:00:00" \
  --timezone "Asia/Jerusalem" \
  --dry-run
```

### שלב 5: צפייה ביומן שבוע עבודה ישראלי

סינון תצוגת היומן להצגת ימי עסקים ישראליים בלבד (ראשון עד חמישי).

**יומן שבועי לשבוע עבודה ישראלי:**
```bash
# קבלת יומן השבוע (א'-ה' בלבד)
gws calendar agenda \
  --from "2026-03-08" \
  --to "2026-03-12" \
  --timezone "Asia/Jerusalem"
```

**סינון ועיצוב עם הערות חגים:**
```bash
# קבלת יומן עם הערות חגים
gws calendar agenda \
  --from "2026-03-08" \
  --to "2026-03-14" \
  --timezone "Asia/Jerusalem" \
  --output json | python3 -c "
import json, sys
from datetime import datetime

events = json.load(sys.stdin)
for e in events:
    start = datetime.fromisoformat(e['start']['dateTime'])
    day = start.weekday()
    # סינון: 6=ראשון, 0=שני, 1=שלישי, 2=רביעי, 3=חמישי (שבוע עבודה ישראלי)
    if day in (6, 0, 1, 2, 3):
        print(f\"{start.strftime('%a %d/%m %H:%M')} - {e['summary']}\")
"
```

### שלב 6: חסימת זמן מיקוד עם מודעות לערב שבת

יצירת בלוקים חוזרים של זמן מיקוד שמכבדים את גבולות יום שישי.

**חסימת זמן מיקוד יומי (א'-ה', 09:00-12:00):**
```bash
gws calendar insert \
  --summary "זמן מיקוד (נא לא להפריע)" \
  --start "2026-03-08T09:00:00" \
  --end "2026-03-08T12:00:00" \
  --timezone "Asia/Jerusalem" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=SU,MO,TU,WE,TH" \
  --visibility private \
  --description "זמן עבודה עמוקה מוגן. תוזמן אוטומטית על ידי GWS Shabbat Calendar."
```

**בלוק מיקוד קצר ליום שישי (מסתיים לפני 13:00):**
```bash
gws calendar insert \
  --summary "מיקוד שישי (קצר)" \
  --start "2026-03-13T09:00:00" \
  --end "2026-03-13T12:00:00" \
  --timezone "Asia/Jerusalem" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=FR" \
  --visibility private \
  --description "בלוק מיקוד קצר ליום שישי, מסתיים לפני ערב שבת."
```

### שלב 7: מציאת חלונות פנויים ללא חגים

ניתוח פערים ביומן תוך סינון תקופות שבת וחגים.

```bash
# שלב 1: קבלת אירועים קיימים לשבוע
gws calendar agenda \
  --from "2026-03-08" \
  --to "2026-03-12" \
  --timezone "Asia/Jerusalem" \
  --output json > /tmp/week_events.json

# שלב 2: מציאת חלונות פנויים באמצעות סקריפט העזר
python3 scripts/find_free_slots.py \
  --events /tmp/week_events.json \
  --work-start 09:00 \
  --work-end 18:00 \
  --friday-end 14:00 \
  --duration 60 \
  --exclude-holidays
```

**מציאת חלונות פנויים חוצי אזורי זמן (ישראל + מזרח ארה"ב):**
```bash
python3 scripts/find_free_slots.py \
  --events /tmp/week_events.json \
  --work-start 09:00 \
  --work-end 18:00 \
  --friday-end 14:00 \
  --duration 60 \
  --overlap-tz "America/New_York" \
  --overlap-start 09:00 \
  --overlap-end 17:00 \
  --exclude-holidays
```

### שלב 8: ניהול אירועים חוזרים בתבנית ישראלית

הגדרת אירועים חוזרים שעוקבים אחרי שבוע העבודה הישראלי ומדלגים אוטומטית על חגים.

**סטנדאפ חוזר (א'-ה' בשעה 09:30):**
```bash
gws calendar insert \
  --summary "סטנדאפ יומי" \
  --start "2026-03-08T09:30:00" \
  --end "2026-03-08T09:45:00" \
  --timezone "Asia/Jerusalem" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=SU,MO,TU,WE,TH" \
  --attendees "dev-team@company.co.il" \
  --description "סטנדאפ יומי. לוח זמנים של שבוע עבודה ישראלי (א'-ה')."
```

**לטיפול בהתנגשויות חגים עם אירועים חוזרים:**
1. שליפת חגים קרובים: `python3 scripts/check_holidays.py --range 2026-03-01 2026-04-01`
2. זיהוי התנגשויות עם לוח הזמנים החוזר
3. שימוש במתכון reschedule-meeting להעברת מופעים מתנגשים:
```bash
# תזמון מחדש של מופע ספציפי שנופל על חג
gws calendar update \
  --event-id "EVENT_ID" \
  --start "2026-03-15T09:30:00" \
  --end "2026-03-15T09:45:00" \
  --timezone "Asia/Jerusalem"
```

### שלב 9: פעולות מרובות ומתכונים מתקדמים

**יצירת אירועים מרובים מקובץ לוח זמנים:**
```bash
# יצירת אירועים מרובים מלוח זמנים JSON
# ראו references/gws-calendar-recipes.md לפורמט המרובה
gws calendar insert --batch schedule.json --dry-run
```

**דוח לוח זמנים שבועי:**
```bash
# יצירת דוח שבועי מעוצב
gws calendar agenda \
  --from "$(date -v-sun +%Y-%m-%d)" \
  --to "$(date -v+thu +%Y-%m-%d)" \
  --timezone "Asia/Jerusalem" \
  --output json | python3 -c "
import json, sys
events = json.load(sys.stdin)
print(f'סה\"כ אירועים השבוע: {len(events)}')
for e in events:
    print(f\"  - {e.get('start',{}).get('dateTime','')[:16]} {e['summary']}\")
"
```

## דוגמאות

### דוגמה 1: תזמון פגישת צוות בהתחשב בשבת

המשתמש אומר: "קבע פגישת צוות של שעה ליום רביעי הבא ב-14:00 שעון ישראל עם צוות הבקאנד"

פעולות:
1. בדיקת תאריך יום רביעי מול לוח שנה יהודי: `python3 scripts/check_holidays.py --date 2026-03-11`
2. אישור שאין התנגשות חג (יום רביעי הוא יום עבודה רגיל בישראל)
3. יצירת האירוע:
```bash
gws calendar insert \
  --summary "פגישת צוות בקאנד" \
  --start "2026-03-11T14:00:00" \
  --end "2026-03-11T15:00:00" \
  --timezone "Asia/Jerusalem" \
  --attendees "backend-team@company.co.il" \
  --description "סנכרון שבועי בקאנד"
```
תוצאה: אירוע נוצר ביום רביעי 14:00 IST, ללא התנגשויות שבת או חגים.

### דוגמה 2: מציאת חלונות פגישה חוצי אזורי זמן ישראל/ארה"ב

המשתמש אומר: "מצא חלונות פנויים של 30 דקות השבוע לשיחה עם הצוות בניו יורק, בלי שבת וחגים"

פעולות:
1. שליפת יומן השבוע: `gws calendar agenda --from 2026-03-08 --to 2026-03-12 --timezone "Asia/Jerusalem" --output json > /tmp/week.json`
2. הפעלת מוצא חלונות חוצי אזורי זמן:
```bash
python3 scripts/find_free_slots.py \
  --events /tmp/week.json \
  --work-start 09:00 --work-end 18:00 --friday-end 14:00 \
  --duration 30 \
  --overlap-tz "America/New_York" --overlap-start 09:00 --overlap-end 17:00 \
  --exclude-holidays
```
3. הצגת חלונות חפיפה זמינים (בדרך כלל 16:00-18:00 IST / 09:00-11:00 EST בימים א'-ה')
תוצאה: רשימת חלונות פנויים בהם שני הצוותים בישראל ובניו יורק זמינים בשעות עבודה, עם מניעת שבת וחגים.

### דוגמה 3: הגדרת סטנדאפ חוזר א'-ה' עם בדיקת חגים אוטומטית

המשתמש אומר: "צור סטנדאפ יומי של 15 דקות בשעה 09:30 לצוות הפיתוח, ראשון עד חמישי, ובדוק אם יש חגים קרובים שמתנגשים"

פעולות:
1. יצירת האירוע החוזר:
```bash
gws calendar insert \
  --summary "סטנדאפ צוות פיתוח" \
  --start "2026-03-08T09:30:00" \
  --end "2026-03-08T09:45:00" \
  --timezone "Asia/Jerusalem" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=SU,MO,TU,WE,TH" \
  --attendees "dev-team@company.co.il"
```
2. בדיקת חגים קרובים ל-30 הימים הבאים: `python3 scripts/check_holidays.py --range 2026-03-08 2026-04-08`
3. דיווח על התנגשויות והצעה להוסיף חריגים לתאריכים אלו
תוצאה: סטנדאפ חוזר נוצר לימים א'-ה'. המשתמש מקבל מידע על תאריכי פסח הקרובים שידרשו ביטול או תזמון מחדש ידני.

## משאבים מצורפים

### סקריפטים
- `scripts/check_holidays.py` -- שאילתת HebCal API לזמני שבת וחגים יהודיים. הרצה: `python3 scripts/check_holidays.py --help`
- `scripts/find_free_slots.py` -- מציאת חלונות פגישה פנויים בניכוי שבת, חגים ואירועים קיימים. תומך בחפיפת אזורי זמן. הרצה: `python3 scripts/find_free_slots.py --help`

### מסמכי עיון
- `references/jewish-calendar-reference.md` -- מדריך מלא לחגים יהודיים, מוסכמות עסקיות ישראליות וכללי תזמון שבת. יש לעיין בו כשצריך לקבוע אילו תאריכים חסומים או בעלי שעות מצומצמות.
- `references/gws-calendar-recipes.md` -- מדריך פקודות יומן Google Workspace CLI ומתכונים מתקדמים. יש לעיין בו בעת בניית פקודות gws calendar, פעולות מרובות או כללי חזרה.

## פתרון בעיות

### שגיאה: "gws: command not found"
סיבה: Google Workspace CLI אינו מותקן או אינו ב-PATH.
פתרון: התקנה עם `npm install -g @google/gws` או שימוש ב-`npx @google/gws calendar ...` לפקודות חד-פעמיות. אימות עם `gws --version`.

### שגיאה: "Not authenticated" או "Token expired"
סיבה: טוקן ה-OAuth פג תוקף או שהמשתמש לא התחבר.
פתרון: הרצת `gws auth login` לאימות מחדש. לחשבונות שירות, הרצת `gws auth setup` וספקו את קובץ ה-JSON של האישורים.

### שגיאה: "Event conflicts with Shabbat boundary"
סיבה: הזמן המבוקש לאירוע נופל אחרי שישי 14:00 או במהלך שבת (שקיעת שישי עד שקיעת שבת).
פתרון: העברת האירוע ללפני שישי 14:00, או לימים א'-ה'. השתמשו ב-`python3 scripts/check_holidays.py --date YYYY-MM-DD` לאימות זמן הדלקת נרות המדויק לאותו שבוע.

### שגיאה: "Holiday data unavailable" או תפוגת זמן HebCal API
סיבה: בעיית רשת או ש-HebCal API לא זמין זמנית.
פתרון: סקריפט `scripts/check_holidays.py` שומר תוצאות בקאש מקומי. לשימוש ללא רשת, עיינו ב-`references/jewish-calendar-reference.md` לתאריכי חגים קבועים. שימו לב שתאריכים עבריים זזים בלוח הגרגוריאני כל שנה.

### שגיאה: "No overlapping slots found" בתזמון חוצה אזורי זמן
סיבה: חלון החפיפה בשעות העבודה ישראל/ארה"ב צר מדי (בדרך כלל 3-4 שעות) בשילוב עם אירועים קיימים.
פתרון: הרחיבו את טווח החיפוש למספר ימים. שקלו שעות התחלה מוקדמות יותר בארה"ב או שעות מאוחרות יותר בישראל. השתמשו בדגל `--duration` עם משך פגישה קצר יותר (למשל 15 או 20 דקות).
