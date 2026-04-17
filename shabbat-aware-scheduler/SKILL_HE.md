# מתזמן מודע שבת

## הנחיות

### שלב 1: לזהות את הקשר התזמון
| הקשר | אילוצים עיקריים | דוגמאות |
|------|-----------------|---------|
| תזמון פגישות | שעות עבודה ישראליות (א'-ה'), שבת, חגים | "קבע פגישת צוות לשבוע הבא" |
| תכנון פריסה (deployment) | בלי פריסות בשבת, בחגים או בערבי חג | "מתי אפשר לפרוס את הגרסה?" |
| תכנון אירועים | מגבלות לוח שנה עברי, זמינות מקום | "תכנן אירוע השקת מוצר" |
| משימות cron/אוטומציה | לדלג על שבתות וחגים במשימות חוזרות | "הרץ משימה יומית חוץ משבת" |
| תזמון התראות | לא לשלוח בשבת או בשעות מאוחרות | "תזמן קמפיין התראות push" |

### שלב 2: קבלת זמני הלכה ונתוני חגים

תשתמשו ב-HebCal API כדי לשלוף זמני שבת ונתוני חגים.
תסתכלו על `scripts/check_shabbat.py` לכלי מוכן לשימוש.

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

### שלב 3: לוגיקת תזמון

**שעות עבודה בישראל:**

| יום | שעות | הערות |
|-----|------|-------|
| ראשון | 08:00-18:00 | יום ראשון בשבוע העבודה הישראלי |
| שני | 08:00-18:00 | יום עסקים רגיל |
| שלישי | 08:00-18:00 | יום עסקים רגיל |
| רביעי | 08:00-18:00 | יום עסקים רגיל |
| חמישי | 08:00-18:00 | יום עסקים רגיל |
| שישי | 08:00-13:00 | חצי יום - סגירה לפני שבת |
| שבת | סגור | שבת - אין פעילות עסקית |

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

| תקופה | תאריכים (בערך) | השפעה על התזמון |
|--------|------------------|---------------|
| ערב שבת (יום שישי) | כל שבוע | סגירה עד 13:00-15:00 לפי העונה |
| ערב ראש השנה | כספטמבר | העסקים סוגרים עד הצהריים |
| עונת ראש השנה + יום הכיפורים | א'-י' תשרי | 10 ימים של זמינות מופחתת |
| שבוע סוכות | ט"ו-כ"ב תשרי | הרבה אנשים בחופשה, חול המועד |
| שבוע טרום פסח | לפני ט"ו ניסן | עסוק מאוד, ניקיונות וקניות |
| שבוע פסח | ט"ו-כ"ב ניסן | הרבה אנשים בחופשה, חול המועד |
| קיץ (יולי-אוגוסט) | יולי-אוגוסט | חופשת קיץ, פעילות עסקית מופחתת |
| שבת חורפית | נובמבר-פברואר | שבת מוקדמת - יום שישי מסתיים מוקדם יותר |
| שבת קיצית | מאי-אוגוסט | שבת מאוחרת - יותר זמינות ביום שישי |

## דוגמאות

### דוגמה 1: קביעת פגישה
המשתמש אומר: "קבע פגישת צוות לשבוע הבא"
תוצאה: בודקים שעות עבודה ישראליות (א'-ה'), מאמתים שאין חגים, מציעים משבצות זמינות. נמנעים מיום שישי אלא אם בבוקר ומאשרים שזה לא ערב חג.

### דוגמה 2: חלון פריסה
המשתמש אומר: "מתי הזמן הבטוח ביותר לפרוס השבוע?"
תוצאה: מוצאים משבצת בשלישי או ברביעי (אמצע שבוע, הכי רחוק משבת), בשעות העבודה, לא לפני חג. ממליצים על פריסה בבוקר לזמן rollback מקסימלי לפני שבת.

### דוגמה 3: Cron מודע חגים
המשתמש אומר: "הגדר דו"ח יומי שמדלג על שבתות וחגים"
תוצאה: מגדירים cron עם בדיקת should_run_today(), מטמון חגים טעון מראש לשנה, עם לוגים לימים שדולגו.

## משאבים מצורפים

### סקריפטים
- `scripts/check_shabbat.py` - כלי עצמאי לשליפת זמני שבת, חגים ישראליים וסטטוס יום עסקים דרך HebCal API. תומך בבדיקה האם תאריך הוא שבת/יום טוב, הצגת כל החגים לשנה, ומציאת המשבצת העסקית הפנויה הבאה עם משך ומיקום שאפשר לכוונן. הרצה: `python scripts/check_shabbat.py --help`

### קובצי עזר
- `references/israeli-holiday-calendar.md` - לוח החגים הישראלי המלא עם תאריכים עבריים, קירובים גרגוריאניים, רמות השפעה על התזמון (גבוהה/בינונית/נמוכה), מגבלות תקופות אבל, זמני הדלקת נרות שבת עונתיים לפי חודש לירושלים, ומדריך endpoints של HebCal API. תסתכלו בו כשמתכננים סביב חגים, קובעים זמני סגירה עונתיים של יום שישי, או בודקים אם אירוע מתנגש עם תקופת אבל.

## מלכודות נפוצות
- זמני שבת משתנים לפי עיר בישראל. הדלקת נרות בירושלים היא 40 דקות לפני השקיעה, בעוד שברוב הערים האחרות משתמשים ב-20-30 דקות. סוכנים עלולים להשתמש בזמן אחיד לכל ישראל.
- לחגים ישראליים יש מגבלות עבודה שונות משבת. חלק מהחגים הם יום אחד בישראל אבל יומיים בחו"ל. סוכנים עלולים להשתמש בלוחות חגים של חו"ל לתזמון ישראלי.
- בלוח העברי יש שנים מעוברות עם חודש נוסף (אדר ב'), שמתרחשות 7 פעמים במחזור של 19 שנה. סוכנים עלולים לחשב תאריכים לפי הלוח הגרגוריאני ולפספס את החודש הזה לגמרי.
- שעות העבודה בישראל הן בד"כ ראשון-חמישי, כששישי הוא חצי יום (עד אחרי הצהריים מוקדם). סוכנים עלולים לתזמן פגישות בשישי אחרי הצהריים או דדליינים לשני בבוקר (שבת היא יום המנוחה השבועי, לא ראשון).

## פתרון בעיות

### שגיאה: "פגישה נקבעה בזמן שבת"
סיבה: אי-התאמה של אזור זמן - השרת ב-UTC, זמני שבת בשעון המקומי
פתרון: תמיד להמיר לאזור הזמן Asia/Jerusalem לפני הבדיקה. זמני שבת משתנים לפי העונה והמיקום.

### שגיאה: "חג לא זוהה"
סיבה: שימוש בלוח גרגוריאני בלבד בלי מיפוי של תאריכים עבריים
פתרון: תשתמשו ב-HebCal API שמטפל בהמרה עברי-גרגוריאני. תשמרו במטמון נתוני חגים שנתיים ותרעננו בראש השנה.

### שגיאה: "פגישת יום שישי מאוחרת מדי"
סיבה: זמן סיום קבוע של 17:00 ביום שישי בלי להתחשב בעונה
פתרון: בחורף, שבת יכולה להתחיל כבר ב-16:00. תמיד תבדקו את זמן הדלקת הנרות בפועל ליום שישי הספציפי.
