# מתזמן מודע שבת

## הנחיות

### שלב 1: קביעת הקשר התזמון
| הקשר | אילוצים עיקריים | דוגמאות |
|------|-----------------|---------|
| תזמון פגישות | שעות עסקים ישראליות (א'-ה'), שבת, חגים | "קבע פגישת צוות לשבוע הבא" |
| תכנון פריסה (deployment) | ללא פריסות בשבת, חגים או ערבי חג | "מתי אפשר לפרוס את הגרסה?" |
| תכנון אירועים | מגבלות לוח שנה עברי, זמינות מקום | "תכנן אירוע השקת מוצר" |
| משימות cron/אוטומציה | דילוג על שבתות וחגים במשימות חוזרות | "הרץ משימה יומית מלבד שבת" |
| תזמון התראות | אין לשלוח בשבת או בשעות מאוחרות | "תזמן קמפיין התראות push" |

### שלב 2: קבלת זמני הלכה ונתוני חגים

שימוש ב-HebCal API לשליפת זמני שבת ונתוני חגים.
ראו `scripts/check_shabbat.py` לכלי מוכן לשימוש.

**שאילתת HebCal API לזמני שבת:**
```python
import requests
from datetime import datetime, timedelta

def get_shabbat_times(date=None, latitude=31.7683, longitude=35.2137, tzid="Asia/Jerusalem"):
    """Get Shabbat candle lighting and havdalah times.
    Default location: Jerusalem.
    """
    if date is None:
        date = datetime.now()

    # Find next Friday
    days_until_friday = (4 - date.weekday()) % 7
    friday = date + timedelta(days=days_until_friday)

    response = requests.get("https://www.hebcal.com/shabbat", params={
        "cfg": "json",
        "gy": friday.year,
        "gm": friday.month,
        "gd": friday.day,
        "latitude": latitude,
        "longitude": longitude,
        "tzid": tzid,
        "b": 18,  # Candle lighting minutes before sunset (18 for Israel)
        "M": "on"  # Include havdalah
    })

    data = response.json()
    times = {}
    for item in data.get("items", []):
        if item["category"] == "candles":
            times["candle_lighting"] = item["date"]
        elif item["category"] == "havdalah":
            times["havdalah"] = item["date"]

    return times
```

**קבלת כל החגים הישראליים לשנה:**
```python
def get_holidays(year):
    """Get all Israeli holidays for a given year."""
    response = requests.get("https://www.hebcal.com/hebcal", params={
        "v": 1,
        "cfg": "json",
        "year": year,
        "month": "x",  # All months
        "maj": "on",   # Major holidays
        "min": "on",   # Minor holidays
        "mod": "on",   # Modern holidays
        "i": "on",     # Israeli holidays (1-day yom tov)
        "nx": "off",
        "ss": "off"
    })

    data = response.json()
    holidays = []
    for item in data.get("items", []):
        if item["category"] in ["holiday", "roshchodesh"]:
            holidays.append({
                "title": item["title"],
                "date": item["date"],
                "category": item.get("subcat", item["category"]),
                "yomtov": item.get("yomtov", False),
                "memo": item.get("memo", "")
            })

    return holidays
```

### שלב 3: מימוש לוגיקת תזמון

**שעות עסקים ישראליות:**

| יום | שעות | הערות |
|-----|------|-------|
| ראשון | 08:00-18:00 | יום ראשון בשבוע העבודה הישראלי |
| שני | 08:00-18:00 | יום עסקים רגיל |
| שלישי | 08:00-18:00 | יום עסקים רגיל |
| רביעי | 08:00-18:00 | יום עסקים רגיל |
| חמישי | 08:00-18:00 | יום עסקים רגיל |
| שישי | 08:00-13:00 | חצי יום — סגירה לפני שבת |
| שבת | סגור | שבת — ללא פעילות עסקית |

**פונקציית תזמון מרכזית:**
```python
from datetime import datetime, timedelta, time
import pytz

IL_TZ = pytz.timezone("Asia/Jerusalem")

BUSINESS_HOURS = {
    6: (time(8, 0), time(18, 0)),  # Sunday
    0: (time(8, 0), time(18, 0)),  # Monday
    1: (time(8, 0), time(18, 0)),  # Tuesday
    2: (time(8, 0), time(18, 0)),  # Wednesday
    3: (time(8, 0), time(18, 0)),  # Thursday
    4: (time(8, 0), time(13, 0)),  # Friday (half day)
    5: None,                        # Saturday (Shabbat)
}

def is_business_day(date, holidays_cache=None):
    """Check if a date is a valid Israeli business day."""
    if date.weekday() == 5:  # Saturday
        return False
    if holidays_cache:
        date_str = date.strftime("%Y-%m-%d")
        for h in holidays_cache:
            if h["date"].startswith(date_str) and h["yomtov"]:
                return False
    return True
```

### שלב 4: משימות cron מודעות חגים

```python
def should_run_today(holidays_cache=None, skip_friday=False, skip_erev_chag=False):
    """Determine if a scheduled job should run today."""
    today = datetime.now(IL_TZ).date()

    # Never run on Shabbat
    if today.weekday() == 5:
        return False, "Shabbat"

    # Check holidays
    if holidays_cache:
        date_str = today.strftime("%Y-%m-%d")
        for h in holidays_cache:
            if h["date"].startswith(date_str):
                if h["yomtov"]:
                    return False, f"Yom Tov: {h['title']}"

        # Check if tomorrow is Yom Tov (today is Erev Chag)
        if skip_erev_chag:
            tomorrow = today + timedelta(days=1)
            tomorrow_str = tomorrow.strftime("%Y-%m-%d")
            for h in holidays_cache:
                if h["date"].startswith(tomorrow_str) and h["yomtov"]:
                    return False, f"Erev Chag: {h['title']} tomorrow"

    if skip_friday and today.weekday() == 4:
        return False, "Friday (half day)"

    return True, "Business day"
```

### שלב 5: מודעות לתקופות טרום-חג ועונתיות

| תקופה | תאריכים (בקירוב) | השפעה על תזמון |
|--------|------------------|---------------|
| ערב שבת (יום שישי) | כל שבוע | סגירה עד 13:00-15:00 בהתאם לעונה |
| ערב ראש השנה | ~ספטמבר | עסקים סוגרים עד הצהריים |
| עונת ראש השנה + יום הכיפורים | א'-י' תשרי | 10 ימים של זמינות מופחתת |
| שבוע סוכות | ט"ו-כ"ב תשרי | רבים בחופשה, חול המועד |
| שבוע טרום פסח | לפני ט"ו ניסן | עסוק מאוד, ניקיונות וקניות |
| שבוע פסח | ט"ו-כ"ב ניסן | רבים בחופשה, חול המועד |
| קיץ (יולי-אוגוסט) | יולי-אוגוסט | חופשת קיץ, פעילות עסקית מופחתת |
| שבת חורפית | נובמבר-פברואר | שבת מוקדמת — יום שישי מסתיים מוקדם יותר |
| שבת קיצית | מאי-אוגוסט | שבת מאוחרת — יותר זמינות ביום שישי |

## דוגמאות

### דוגמה 1: קביעת פגישה
המשתמש אומר: "קבע פגישת צוות לשבוע הבא"
תוצאה: בדיקת שעות עסקים ישראליות (א'-ה'), אימות שאין חגים, הצעת משבצות זמינות. הימנעות מיום שישי אלא אם בבוקר ואישור שזה לא ערב חג.

### דוגמה 2: חלון פריסה
המשתמש אומר: "מתי הזמן הבטוח ביותר לפרוס השבוע?"
תוצאה: מציאת משבצת ביום שלישי או רביעי (אמצע שבוע, מרחק מקסימלי משבת), בשעות עסקים, לא לפני חג. המלצה על פריסה בבוקר לזמן rollback מקסימלי לפני שבת.

### דוגמה 3: Cron מודע חגים
המשתמש אומר: "הגדר דו"ח יומי שמדלג על שבתות וחגים"
תוצאה: הגדרת cron עם בדיקת should_run_today(), מטמון חגים טעון מראש לשנה, עם לוגים לימים שדולגו.

## משאבים מצורפים

### סקריפטים
- `scripts/check_shabbat.py` — כלי עצמאי לשאילתת זמני שבת, חגים ישראליים וסטטוס יום עסקים דרך HebCal API. תומך בבדיקה האם תאריך הוא שבת/יום טוב, הצגת כל החגים לשנה, ומציאת המשבצת העסקית הזמינה הבאה עם משך ומיקום מתכווננים. הרצה: `python scripts/check_shabbat.py --help`

### קובצי עזר
- `references/israeli-holiday-calendar.md` — לוח חגים ישראלי מלא עם תאריכים עבריים, קירובים גרגוריאניים, רמות השפעה על תזמון (גבוהה/בינונית/נמוכה), מגבלות תקופות אבל, זמני הדלקת נרות שבת עונתיים לפי חודש לירושלים, ומדריך endpoints של HebCal API. יש לעיין בו בעת תכנון סביב חגים, קביעת זמני סגירה עונתיים של יום שישי, או בדיקה אם אירוע מתנגש עם תקופת אבל.

## מלכודות נפוצות
- זמני שבת משתנים לפי עיר בישראל. הדלקת נרות בירושלים 40 דקות לפני השקיעה, בעוד רוב הערים האחרות משתמשות ב-20-30 דקות. סוכנים עלולים להשתמש בזמן אחיד לכל ישראל.
- חגים ישראליים יש להם מגבלות עבודה שונות משבת. חלק מהחגים הם יום אחד בישראל אבל יומיים בגולה. סוכנים עלולים להשתמש בלוחות חגים של הגולה לתזמון ישראלי.
- ללוח העברי יש שנים מעוברות עם חודש נוסף (אדר ב'), המתרחשות 7 פעמים במחזור של 19 שנה. סוכנים עלולים לחשב תאריכים לפי הלוח הגרגוריאני ולפספס את החודש הזה לגמרי.
- שעות עבודה בישראל הן בדרך כלל ראשון-חמישי, כאשר שישי הוא חצי יום (עד אחרי הצהריים מוקדם). סוכנים עלולים לתזמן פגישות בשישי אחרי הצהריים או דדליינים ליום שני בבוקר (שבת הוא יום המנוחה השבועי, לא ראשון).

## פתרון בעיות

### שגיאה: "פגישה תוזמנה בזמן שבת"
סיבה: אי-התאמת אזור זמן — השרת ב-UTC, זמני שבת בשעון מקומי
פתרון: תמיד להמיר לאזור הזמן Asia/Jerusalem לפני הבדיקה. זמני שבת משתנים לפי עונה ומיקום.

### שגיאה: "חג לא זוהה"
סיבה: שימוש בלוח גרגוריאני בלבד ללא מיפוי תאריכים עבריים
פתרון: שימוש ב-HebCal API שמטפל בהמרה עברי-גרגוריאני. שמירת נתוני חגים במטמון שנתי ורענון בראש השנה.

### שגיאה: "פגישת יום שישי מאוחרת מדי"
סיבה: זמן סיום קבוע של 17:00 ביום שישי ללא התחשבות בעונה
פתרון: בחורף, שבת יכולה להתחיל כבר ב-16:00. תמיד לבדוק את זמן הדלקת הנרות בפועל ליום שישי הספציפי.
