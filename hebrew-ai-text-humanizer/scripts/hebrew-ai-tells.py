#!/usr/bin/env python3
"""
hebrew-ai-tells.py: scan Hebrew text for the patterns that make it read as
machine-written or translated from English, and (optionally) check that a
rewrite kept every fact of the original.

Stdlib only, no network. Works offline and inside sandboxes.

Modes
-----
1. Scan (default): print every flagged span with line, column, pattern id and a
   fix hint, then document-level findings and a density figure.

       python3 hebrew-ai-tells.py post.txt
       python3 hebrew-ai-tells.py post.txt --register professional --channel linkedin
       cat email.txt | python3 hebrew-ai-tells.py -
       python3 hebrew-ai-tells.py post.txt --format json

2. Compare: check that a rewrite kept the machine-checkable facts of the
   original: digits, Latin-script tokens (brand names, codes), URLs, e-mails,
   @handles, Hebrew weekdays and number words, negation phrases (each negation word
   plus the word after it; a negation moved to a sentence with the same following
   word is NOT detected), and
   any names or phrases passed with --keep.

       python3 hebrew-ai-tells.py original.txt --compare rewrite.txt --keep "Dana Cohen"

   Exit 0: everything checkable is present. Exit 1: something to review.
   Exit 3: nothing in the original was machine-checkable; this is never a pass.
   Hebrew names (without --keep), dates in words and meaning are NOT checked.

3. List the pattern catalogue:

       python3 hebrew-ai-tells.py --list-patterns

4. Regression tests: python3 test_hebrew_ai_tells.py

Severity levels
---------------
  rule   The Academy of the Hebrew Language rules this form non-standard, and the
         regex is precise enough to report it as such.
  style  Style guidance: legal Hebrew, but a typical translated or AI tell.
  check  The script cannot decide (including Academy-rule patterns whose regex
         also matches correct Hebrew); a human or the model must read it.

The density figure is flags (rule + style) per 100 words. It is an editing
workload heuristic for this catalogue only. It is NOT an AI-detector score and
says nothing about who wrote the text or how any detector would classify it.
"""

import argparse
import json
import re
import sys
from collections import Counter

H = 'א-ת'            # Hebrew letters
HL = '[' + H + ']'             # one Hebrew letter
NOT_H_BEFORE = '(?<![' + H + '])'
NOT_H_AFTER = '(?![' + H + '])'
MAQAF = '\u05be'
EM = '\u2014'
EN = '\u2013'
PREFIX = '[ובכלמהש]{1,3}'   # vav, bet, kaf, lamed, mem, he, shin
# A run of 1-3 prefix letters can also be a whole word (מה, של, כל, כמה). Never treat those as a prefix.
PREFIX_WORDS = 'מה|של|כל|כמה|למה|ממה|במה|שמה|בכל|וכל|לכל|שכל|מכל|ככה|כמו|הכל|מהם|שלה|ולה|לה|בה'
PREFIX_START = NOT_H_BEFORE + '(?!(?:' + PREFIX_WORDS + ')(?![' + H + ']))'
EMOJI = ('[\U0001F300-\U0001FAFF☀-➿⭐⬆⬇⤴⤵'
         '‼⁉™ℹ↔-↙↩↪⌚⌛⌨'
         '⏏⏩-⏳⏸-⏺Ⓜ▪▫▶◀◻-◾]')


MONTHS = ('ינואר|פברואר|מרץ|מרס|אפריל|מאי|יוני|יולי|אוגוסט|ספטמבר|אוקטובר|נובמבר|דצמבר|'
          'תשרי|חשוון|חשון|כסלו|טבת|שבט|אדר|ניסן|אייר|סיוון|סיון|תמוז|אב|אלול')
# one side of a range: a month name, a day letter with geresh (א' to ש'), or a number
RANGE_SIDE_BEFORE = '(?:(?<![' + H + '])[ובמל]?(?:' + MONTHS + ')|(?<![' + H + '])[א-ש][\'\u05f3]|\\d)'
RANGE_SIDE_AFTER = '(?:(?:' + MONTHS + ')(?![' + H + '])|[א-ש][\'\u05f3]|\\d)'
EM_RANGE_RX = RANGE_SIDE_BEFORE + '(' + EM + ')(?=' + RANGE_SIDE_AFTER + ')'


def w(body, prefixes='[וש]?'):
    """Wrap a Hebrew phrase so it matches as a whole word, allowing vav/shin prefixes."""
    return NOT_H_BEFORE + prefixes + '(?:' + body + ')' + NOT_H_AFTER


# ---------------------------------------------------------------------------
# Pattern catalogue (inline patterns). Keep ids in sync with
# references/ai-hebrew-patterns.md.
# ---------------------------------------------------------------------------
PATTERNS = [
    # --- Calques and inflated connectors -----------------------------------
    dict(id='CAL01', sev='style', group='calque',
         rx=w('עבור(?:ך|כם|כן|ו|ה|ם|ן|נו|י)?', '[ו]?'),
         hint='"avur" for "for": the Academy calls it a style question. Prefer l-/bishvil when it reads lighter.'),
    dict(id='CAL02', sev='style', group='calque',
         rx=w('ניתן'),
         hint='"nitan" register. Usually "efshar" or a direct imperative. Check it is not the past tense "was given".'),
    dict(id='CAL03', sev='rule', group='calque',
         rx=NOT_H_BEFORE + '[ו]?במידה\\s+ו(?=[' + MAQAF + '\\-]?' + HL + ')',
         hint='Academy: the vav form of bemida is non-standard. In a condition write "im".'),
    dict(id='CAL04', sev='check', group='calque',
         rx=NOT_H_BEFORE + '[ו]?במידה\\s+ש(?=[' + MAQAF + '\\-]?' + HL + ')',
         hint='Academy: bemida-she only for real degree ("the more..."). In a plain condition use "im".'),
    # CAL05 cannot be decided by regex: "היה ויכוח" (there was an argument) is
    # ordinary Hebrew. Only flag it when a clause break follows (the conditional
    # shape "היה ו<verb> ..., <result>"), skip common vav-initial nouns, and keep
    # it at check severity so it is never reported as an Academy ruling unread.
    dict(id='CAL05', sev='check', group='calque',
         rx='(?:^|(?<=[.!?:]\\s))היה\\s+ו(?!יכוח|ויכוח|ותיק|וודאי|ודאי|ויטמין|וילון|ועד|ועידה|ורד|ולד|וידאו|ויזה|ויסות)' + HL + '+[^.!?\\n]{0,80},',
         hint='Possible conditional "haya ve-" (the Academy rules it non-standard; use "im"). Read it: if it means "there was", leave it.'),
    dict(id='CAL06', sev='rule', group='calque',
         rx=NOT_H_BEFORE + '[ו]?היות\\s+ו(?=' + HL + ')',
         hint='Academy: heyot-ve is non-standard. Use "ki", "mipnei she-", "keivan she-".'),
    dict(id='CAL07', sev='style', group='calque',
         rx=w('על\\s+מנת'),
         hint='"al menat" inflates "kdei". In ordinary prose write "kdei".'),
    dict(id='CAL08', sev='style', group='calque',
         rx=w('אשר'),
         hint='"asher" where "she-" would do raises the register. Check it is not the name Asher or the verb ishar.'),
    dict(id='CAL09', sev='style', group='preamble',
         rx=w('(?:חשוב|יש|ראוי|כדאי)(?:\\s+לנו)?\\s+(?:לציין|להדגיש|לזכור)'),
         hint='Announcing that something is important. Delete the preamble and say the thing.'),
    dict(id='CAL10', sev='style', group='opener',
         rx=w('בעולם\\s+של\\s+היום|בעולם\\s+המודרני|בעולם\\s+המשתנה|בעידן\\s+(?:הנוכחי|הדיגיטלי|המודרני|של\\s+היום)|בימינו\\s+אנו'),
         hint='Scene-setting opener ("in today\'s world"). Start with the actual point.'),
    dict(id='CAL11', sev='style', group='frame',
         # same pronoun repeated (or אלא) right after a comma or a dash: "זה לא X, זה Y".
         # "היא לא הגיעה כי היא חולה" has no separator before the second pronoun and is not matched.
         rx=NOT_H_BEFORE + '(זה|זו|הוא|היא)\\s+לא\\s+(?:רק\\s+)?[^.!?\\n,]{1,40}?(?:,|\\s[' + EM + EN + '-])\\s*(?:\\1|אלא)' + NOT_H_AFTER,
         hint='"It is not X, it is Y" frame. State Y directly unless someone really claimed X.'),
    dict(id='CAL11', sev='style', group='frame',
         rx=NOT_H_BEFORE + 'לא\\s+רק\\s+[^.!?\\n]{1,60}?\\s+אלא\\s+גם' + NOT_H_AFTER,
         hint='"Not only X but also Y". Usually a plain "and" is enough.'),
    dict(id='CAL12', sev='style', group='calque',
         rx=w('להבטיח(?=\\s+(?:ש|את))', '[וכ]?(?:די\\s+)?'),
         hint='"lehavtiach" for "to ensure". Use "kdei she-", "levadeh she-", or just the verb.'),
    dict(id='CAL13', sev='style', group='idiom',
         rx=w('בסופו\\s+של\\s+יום|משנה(?:ת|י)?\\s+(?:את\\s+כללי\\s+)?(?:ה)?משחק|צעד\\s+(?:אחד\\s+)?קדימה|לצלול\\s+(?:לעומק|פנימה)|לעשות\\s+את\\s+ההבדל|ליצור\\s+ערך|לייצר\\s+ערך|מדבר(?:ות|ים)?\\s+בעד\\s+עצמ(?:ן|ם|ו|ה)'),
         hint='English idiom carried over word for word (end of the day, game changer, deep dive, speak for themselves).'),
    dict(id='CAL14', sev='style', group='connector',
         rx='(?:^|(?<=[.!?]\\s))(?:בנוסף(?:\\s+לכך)?|יתרה\\s+מזאת|יתרה\\s+מכך|כמו\\s+כן|מעבר\\s+לכך|לאור\\s+זאת|לאור\\s+האמור)' + NOT_H_AFTER,
         hint='Sentence opens with a stacked connector. Drop it or merge the sentences.'),
    dict(id='CAL15', sev='style', group='calque',
         rx=w('באופן\\s+(?:משמעותי|אישי|מלא|ישיר|מיידי|יעיל|מקצועי|אופטימלי|שוטף|עקבי)'),
         hint='"be-ofen + adjective" mirrors English -ly adverbs. Often the adverb can go, or use a real Hebrew adverb.'),
    dict(id='CAL16', sev='style', group='calque',
         rx='(?:^|(?<=[.!?]\\s))[A-Za-z][A-Za-z0-9]+(?=\\s+' + HL + ')',
         hint='Hebrew sentence that leads with an English noun. Lead with the Hebrew framing, then the term.'),
    # --- LinkedIn and announcement tells (style guidance) ------------------
    dict(id='LNK01', sev='style', group='linkedin',
         rx=w('(?:אני\\s+|אנחנו\\s+)?(?:נרגש|נרגשת|נרגשים|נרגשות|גאה|גאים|גאות|שמח|שמחה|שמחים|שמחות)\\s+(?:מאוד\\s+)?(?:לשתף|להכריז|לבשר|להודיע|להציג|להצטרף|לראות|לספר|לחגוג)'),
         hint='"Excited to share" / "proud to announce" opener. Start with the news itself.'),
    dict(id='LNK02', sev='style', group='linkedin',
         rx=w('(?:ה|מה|ב|ל)?מסע(?:\\s+(?:הזה|שלי|שלנו|המאתגר|מאתגר|מרגש|מדהים|מטורף))?', '[ו]?(?:חלק\\s+)?'),
         hint='"Journey" for a project, a job or a process. Name the thing: the project, the year, the move.'),
    dict(id='LNK03', sev='style', group='linkedin',
         rx=w('ממלא(?:ת|ים|ות)?\\s+אותי\\s+ב' + HL + '+'),
         hint='"Fills me with pride/excitement". Say what happened; the reader infers the pride.'),
    dict(id='LNK04', sev='style', group='linkedin',
         rx='\\d+\\s+(?:שנים|שנות|חודשים|שבועות)\\s+(?:מדהימות|מדהימים|מטורפות|מטורפים|מופלאות|מופלאים|מרגשות|מרגשים)' + NOT_H_AFTER,
         hint='"4 amazing years". Drop the adjective or replace it with one concrete thing that happened.'),
    dict(id='LNK05', sev='style', group='linkedin',
         rx=w('תודה(?:\\s+רבה)?\\s+לכל\\s+מי\\s+ש(?:היה|הייתה|היו)\\s+חלק'),
         hint='Blanket thank-you to "everyone who was part of it". Thank named people, or cut it.'),
    dict(id='LNK06', sev='style', group='linkedin',
         rx=w('לרתום|להעצים|מעצים|מעצימה|פורץ(?:ת)?\\s+דרך|פורצי\\s+דרך|חדשני|חדשנית|חדשניים|חדשניות|סינרגיה|אקוסיסטם|ערך\\s+מוסף|משנה\\s+חיים|ברמה\\s+הבאה'),
         hint='Buzzword. Replace with the concrete claim behind it, or cut it.'),
    # --- Grammar-level translationese (style guidance) ---------------------
    dict(id='GRM01', sev='style', group='grammar',
         rx=NOT_H_BEFORE + '[ו]?אני\\s+(?!(?:אמיתי|איכותי|תרבותי|חברתי|אותנטי|בריאותי|עצמאי)' + NOT_H_AFTER + ')(?=' + HL + '{2,}תי' + NOT_H_AFTER + ')' + '|' + NOT_H_BEFORE + '[ו]?אנחנו\\s+(?!כולנו|שנינו|עצמנו|לבדנו|כאן)(?=' + HL + '{2,}נו' + NOT_H_AFTER + ')',
         hint='Subject pronoun before a past-tense verb that already carries the person ("ani hovalti"). Drop the pronoun unless it marks contrast.'),
    dict(id='GRM02', sev='style', group='grammar',
         rx=w('(?:לבצע|ביצע|ביצעה|ביצענו|ביצעתי|ביצעו|מבצעים|מבצעת|נבצע|לקבל|קיבלנו|קיבלתי|קיבלו|נקבל|לערוך|ערכנו|ערכתי|לעשות|עשינו|עשיתי)\\s+(?:את\\s+)?(?:ה)?(?:הטמעה|הטמעת|בדיקה|בדיקות|בדיקת|החלטה|החלטות|ניתוח|שינוי|שינויים|שיפור|הערכה|אופטימיזציה|התאמה|התאמות|הגדרה|העברה|סקירה|בחינה|שימוש)'),
         hint='Light verb + action noun ("bitzanu hatmaa shel"). A plain verb usually reads lighter: hitmanu, bodkim, hechlatnu.'),
    dict(id='GRM03', sev='style', group='register-notformal',
         rx='(?:^|(?<=[.!?]\\s))(?:ו)?האם\\s+[^.!?\\n]*\\?',
         hint='Yes/no question opened with "haim". In casual and professional Hebrew it is usually dropped: "atem yod\'im ...?"'),
    dict(id='GRM04', sev='style', group='grammar',
         rx=w('על\\s+ידי'),
         hint='"al yedei" passive or means phrase. Make the agent the subject, or use "b-".'),
    # --- Vocabulary: over-Hebraised words (gated to casual/professional) ----
    dict(id='VOC01', sev='style', group='register-formal',
         rx=w('משוב|דוא"ל|דואר\\s+אלקטרוני|יישומון|יישומונים|מרשתת|במרשתת|מקוון|מקוונת', '[וב]?'),
         hint='Academy coinage or high-register word that many Israeli business readers do not use (feedback, mail, app, internet, online). Keep the loanword the audience says, unless the brand prefers the Hebrew.'),
    # --- Register markers (gated by --register) ----------------------------
    dict(id='REG01', sev='style', group='register-formal',
         rx=w('הנני|הריני|הננו|לאור\\s+האמור|בהתאם(?=\\s+ל)|כמפורט\\s+להלן|ברצוננו|בנוגע(?=\\s+ל)|על\\s+אודות|אנו(?=\\s)'),
         hint='Office-form register. Fine in a formal letter, stiff in a post, a WhatsApp message or a warm customer email.'),
    dict(id='REG01', sev='style', group='register-formal',
         # only before a known directive infinitive, so "יש לקוחות" (there are customers) is not matched
         rx=NOT_H_BEFORE + '(?:יש|נא)\\s+(?:לשים\\s+לב|לפנות|למלא|להגיש|לשלוח|לוודא|להקפיד|לצרף|לבדוק|להירשם|להתקשר|לעדכן|להציג|לשמור|להימנע|לקרוא|לאשר|להשתמש|להעביר|לבצע|להתחיל|לאסוף|להביא|לחתום|לשלם|להמתין)' + NOT_H_AFTER,
         hint='Impersonal directive ("yesh le-", "na le-"). In casual or professional text address the reader directly.'),
    dict(id='REG02', sev='style', group='register-casual',
         rx=w('סבבה|אחלה|וואלה|יאללה|תכלס|בקטנה|מגניב|חבר\'ה', ''),
         hint='Slang. Out of place when the target register is formal.'),
    # --- Addressing --------------------------------------------------------
    dict(id='ADR01', sev='style', group='addressing',
         rx=HL + '+/(?:ה|ת|י|ות|ים|ן)' + NOT_H_AFTER,
         hint='Slash gender forms. The Academy finds them hard to recommend and suggests plural address instead.'),
    # --- Structure ---------------------------------------------------------
    dict(id='STR02', sev='style', group='structure',
         rx='^\\s*(?:[-*•]\\s*)?(?:' + EMOJI + '\\s*)?\\*\\*[^*\\n]{1,40}\\*\\*',
         hint='Bold label at the start of a line. In prose, write the sentence; keep labels for real reference lists.'),
    dict(id='STR03', sev='style', group='structure',
         rx='^\\s*(?:[-*•]\\s*)?' + EMOJI,
         hint='Emoji used as a bullet. Fine in a casual post once or twice; a column of them is a template tell.'),
    # STR04: the Academy separating dash takes a space on each side, EXCEPT the range
    # dash ("to"), which the Academy writes unspaced (punctuation rules, maqaf note,
    # footnote: "except a line marking a range"). So an unspaced EN dash between letters
    # (ינואר-מרץ with an en dash, א-ד) may be a correct range: check, never rule.
    # Ranges between digits are not matched at all.
    dict(id='STR04', sev='rule', group='punctuation',
         rx='(?<=[' + H + 'A-Za-z])' + EM + '(?=[' + H + 'A-Za-z])',
         hint='Em dash glued to words (English style). The Academy dash takes a space on both sides; between words that belong together use a maqaf.'),
    dict(id='STR04', sev='check', group='punctuation',
         rx=EM_RANGE_RX,
         hint='Em dash between two months, day letters or numbers. If this marks a range, the Academy writes it as an unspaced en dash; do not add spaces.'),
    dict(id='STR04', sev='check', group='punctuation',
         rx='(?<=[' + H + 'A-Za-z])' + EN + '(?=[' + H + 'A-Za-z])',
         hint='Unspaced en dash between words. Correct if it marks a range (ינואר to מרץ, א to ד), which the Academy writes without spaces; otherwise space it as a dash or use a maqaf.'),
    dict(id='STR09', sev='style', group='structure',
         rx='^\\s*(?:דמיינו|תארו\\s+לעצמכם|האם\\s+ידעת(?:ם)?|רוצים\\s+לדעת|מה\\s+אם)' + NOT_H_AFTER,
         hint='Rhetorical hook opener. Start with the fact or the news instead.'),
    # --- Punctuation and mixed scripts ------------------------------------
    dict(id='PUN01', sev='rule', group='punctuation',
         rx=PREFIX_START + PREFIX + '(?=\\d)',
         hint='Prefix letter glued to a number. The Academy puts a maqaf between letters and digits (in social copy the keyboard hyphen is the usual substitute: b-2026).'),
    dict(id='PUN02', sev='rule', group='punctuation',
         rx=PREFIX_START + PREFIX + '(?=[A-Za-z])',
         hint='Prefix letter glued to a Latin-script word. Add a maqaf (or the keyboard hyphen) between them.'),
    dict(id='PUN03', sev='rule', group='punctuation',
         rx=PREFIX_START + PREFIX + '(?:\\s*[' + EM + EN + ']\\s*|\\s+-\\s*)(?=[\\dA-Za-z])',
         hint='A dash with spaces used where a maqaf belongs. Write prefix, maqaf (or hyphen), number with no spaces.'),
    dict(id='PUN04', sev='rule', group='punctuation',
         # dotted acronyms (ת.ד., צ.ה.ל.) and abbreviations that cannot be a whole word.
         # Bare "מס." is skipped: at a sentence end it is usually the word "tax".
         rx=NOT_H_BEFORE + '(?:' + PREFIX + ')?(?:' + HL + '\\.){2,}' + '|' + NOT_H_BEFORE + '(?:' + PREFIX + ')?(?:עמ|וכו|רח)\\.(?=\\s|$)' + '|' + NOT_H_BEFORE + '(?:' + PREFIX + ')?מס\\.(?=\\s*\\d)',
         hint='Abbreviation marked with periods. Hebrew uses geresh for a shortened word (mispar: mem-samekh-geresh) and gershayim for an acronym.'),
    # PUN05 is an Academy RECOMMENDATION ("mumlatz meod"), not a ruling; old Hebrew
    # printing used a light space before heavy marks. Scored as style.
    dict(id='PUN05', sev='style', group='punctuation',
         rx='(?<=[' + H + 'A-Za-z0-9"\'\\)])[ \\t]+[?!:;,.](?=\\s|$)',
         hint='Full space before a punctuation mark. The Academy strongly recommends attaching the mark to the word before it (a recommendation, not a ruling).'),
    # PUN06 is a check, not a rule: the Academy does not state it separately, and a
    # lone letter before a number can be a label ("סעיף ב 3"), not a prefix.
    dict(id='PUN06', sev='check', group='punctuation',
         # a lone prefix letter (or vav/shin + one prefix) detached from a number or Latin word: "עלה ב 5"
         rx=NOT_H_BEFORE + '(?!של' + NOT_H_AFTER + ')(?:[ובכלמהש]|[וש][בכלמה])' + NOT_H_AFTER + '(?=[ \\t]+[\\dA-Za-z])',
         hint='Possible prefix letter separated from its number or Latin word by a space ("ala b 5"). If it is a prefix, join it with a hyphen or maqaf; if it is a label (section b 3), leave it.'),
    # PUN07 (W3C case): an English phrase followed by a SEPARATE number, detected as
    # Latin run + number + a Hebrew counting word ("Harry Potter 3 פעמים"). A number
    # that is part of the name (a model or version number) renders fine and is not matched.
    dict(id='PUN07', sev='check', group='bidi',
         rx='(?<=[A-Za-z])[ \\t]+\\d[\\d.,]*(?=[ \\t]+[ובל]?(?:פעמים|פעם|שנים|שנה|חודשים|ימים|שעות|דקות|אחוז|אחוזים|שקלים|ש"ח|משתמשים|לקוחות|עובדים|אנשים|מקומות|כוכבים)' + NOT_H_AFTER + ')',
         hint='English phrase followed by a separate number: in RTL text the number can attach to the English run. Rephrase (put the number first) or add RLM (U+200F) right after the English phrase. Never insert RLM inside a name that contains its own number.'),
]

EM_RANGE = re.compile(EM_RANGE_RX)
FORMAL_TARGETS = {'formal'}
CASUAL_TARGETS = {'casual', 'professional'}

SUMMARY_CLOSERS = re.compile(
    '^(?:לסיכום|בסופו\\s+של\\s+דבר|'
    'בסופו\\s+של\\s+יום|בשורה\\s+התחתונה|'
    'השורה\\s+התחתונה|בקיצור|כך\\s+ש|'
    'ולכן|אז|בסוף)' + NOT_H_AFTER)
BULLET = re.compile('^\\s*(?:[-*•]|\\d+[.)]|' + EMOJI + ')\\s*')
HEADING = re.compile('^\\s*#{1,6}\\s')
TRIAD = re.compile(NOT_H_BEFORE + HL + '+,\\s+' + HL + '+(?:\\s+' + HL + '+)?\\s+ו' + HL + '+')
WORD = re.compile('[' + H + 'A-Za-z0-9]+')
HEB_WORD = re.compile(HL)
HASHTAG = re.compile(r'(?<![\w#])#[\w]+')
HASHTAG_LINE = re.compile(r'^\s*(?:#[\w]+\s*)+$')
SPELLING_PAIRS = [('תכנית', 'תוכנית'), ('אמא', 'אימא'), ('מיד', 'מייד'), ('לעתים', 'לעיתים'),
                  ('דוגמא', 'דוגמה')]

PRONOUNS = {
    'singular_m': re.compile(NOT_H_BEFORE + '[ו]?אתה' + NOT_H_AFTER),
    'plural': re.compile(NOT_H_BEFORE + '[ו]?את(?:ם|ן)' + NOT_H_AFTER),
    'singular_suffix': re.compile(NOT_H_BEFORE + '[וש]?(?:לך|שלך|אליך|אותך|עבורך|בשבילך|ממך|עליך|איתך|אתך)' + NOT_H_AFTER),
    'plural_suffix': re.compile(NOT_H_BEFORE + '[וש]?(?:לכם|שלכם|אליכם|אתכם|אותכם|עבורכם|בשבילכם|מכם|עליכם|איתכם)' + NOT_H_AFTER),
    'slash': re.compile(HL + '+/(?:ה|ת|י|ות|ים|ן)' + NOT_H_AFTER),
}

WEEKDAYS = ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת']
NUMBER_WORDS = ['אחד', 'אחת', 'שניים', 'שתיים', 'שתי', 'שלוש', 'שלושה', 'ארבע', 'ארבעה', 'חמש', 'חמישה',
                'שש', 'שישה', 'שבע', 'שבעה', 'שמונה', 'תשע', 'תשעה', 'עשר', 'עשרה', 'עשרים', 'שלושים',
                'ארבעים', 'חמישים', 'מאה', 'מאות', 'אלף', 'אלפים', 'מיליון', 'חצי', 'רבע', 'פעמיים',
                'שנתיים', 'יומיים', 'חודשיים', 'שבועיים', 'שעתיים']
# Closed list, whole words, only ו/ש prefixes allowed (so מלא, שאל and ללא-as-ל+לא never count).
NEGATIONS = ['לא', 'אין', 'אינו', 'אינה', 'אינם', 'אינן', 'איננו', 'אינני', 'בלי', 'ללא']
NEG_RX = re.compile(NOT_H_BEFORE + '[וש]?(' + '|'.join(sorted(NEGATIONS, key=len, reverse=True)) + ')' + NOT_H_AFTER
                    + r'(?:\s+(' + HL + '+))?')

FACT_TOKENS = [
    ('url', re.compile(r'https?://\S+')),
    ('email', re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')),
    ('handle', re.compile(r'(?<![\w@])@[A-Za-z0-9_]+')),
    ('latin', re.compile(r'[A-Za-z][A-Za-z0-9_+#.-]*[A-Za-z0-9]|[A-Za-z]')),
    ('number', re.compile(r'\d+(?:[.,:/]\d+)*')),
]


def compile_patterns():
    out = []
    for p in PATTERNS:
        q = dict(p)
        q['re'] = re.compile(p['rx'], re.MULTILINE)
        out.append(q)
    return out


def active(p, register):
    if p['group'] == 'register-formal':
        return register in CASUAL_TARGETS
    if p['group'] == 'register-casual':
        return register in FORMAL_TARGETS
    if p['group'] == 'register-notformal':
        return register not in FORMAL_TARGETS
    return True


def scan(text, register, channel=None):
    pats = compile_patterns()
    lines = text.split('\n')
    hits = []
    for ln, line in enumerate(lines, 1):
        range_dashes = {m.start(1) for m in EM_RANGE.finditer(line)}
        for p in pats:
            if not active(p, register):
                continue
            for m in p['re'].finditer(line):
                # a glued em dash that looks like a range is reported by the STR04 range check below
                if p['id'] == 'STR04' and p['sev'] == 'rule' and m.start() in range_dashes:
                    continue
                span = m.group(0).strip() or m.group(0)
                hits.append(dict(line=ln, col=m.start() + 1, id=p['id'], severity=p['sev'],
                                 match=span, hint=p['hint']))
    hits.sort(key=lambda h: (h['line'], h['col']))

    doc = []
    nonblank = [l for l in lines if l.strip()]
    words = WORD.findall(text)
    n_words = len(words)

    # STR01 list-itis
    bullets = [l for l in nonblank if BULLET.match(l)]
    if len(bullets) >= 4 and len(bullets) * 2 >= len(nonblank):
        doc.append(dict(id='STR01', severity='style',
                        detail='{} of {} non-blank lines are bullets'.format(len(bullets), len(nonblank)),
                        hint='List-itis. Turn the bullets that carry reasoning back into sentences.'))
    # STR04 dash density
    # range dashes (an unspaced en dash between two letters or digits) are not counted
    ranges = len(re.findall('[' + H + 'A-Za-z0-9][\'\u05f3]?' + EN + '(?=[' + H + 'A-Za-z0-9])', text))
    dashes = text.count(EM) + text.count(EN) - ranges
    if dashes >= 2 and n_words and dashes * 60 >= n_words:
        doc.append(dict(id='STR04', severity='style',
                        detail='{} long dashes in {} words'.format(dashes, n_words),
                        hint='The dash is a legitimate Hebrew mark, but one every few lines is a tell. Use commas, a period or parentheses.'))
    # STR05 triads
    triads = TRIAD.findall(text)
    if len(triads) >= 3:
        doc.append(dict(id='STR05', severity='style',
                        detail='{} three-item series'.format(len(triads)),
                        hint='Repeated triads. Keep the strongest item or the real number of items.'))
    # STR06 summary closers
    paras = [p for p in re.split(r'\n\s*\n', text) if p.strip()]
    closers = 0
    for para in paras:
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', para.strip()) if s.strip()]
        if len(sentences) >= 2 and SUMMARY_CLOSERS.match(sentences[-1]):
            closers += 1
    if closers >= 2:
        doc.append(dict(id='STR06', severity='style',
                        detail='{} paragraphs end with a summarising sentence'.format(closers),
                        hint='Every paragraph closes on a moral. Cut the closers; let the last fact land.'))
    # STR07 headings in a short text
    headings = [l for l in nonblank if HEADING.match(l)]
    if headings and n_words < 250:
        doc.append(dict(id='STR07', severity='style',
                        detail='{} markdown headings in a {}-word text'.format(len(headings), n_words),
                        hint='Headings in a post or an email. Remove them unless the text is a document.'))
    # STR08 exclamation density
    bangs = text.count('!')
    if bangs >= 3 and n_words and bangs * 40 >= n_words:
        doc.append(dict(id='STR08', severity='style',
                        detail='{} exclamation marks in {} words'.format(bangs, n_words),
                        hint='Enthusiasm by punctuation. Keep one at most.'))
    # LNK07 hashtags
    tags = HASHTAG.findall(text)
    if len(tags) > 3:
        doc.append(dict(id='LNK07', severity='style',
                        detail='{} hashtags'.format(len(tags)),
                        hint='Hashtag pile. On LinkedIn keep about three at the end; join a multi-word Hebrew tag with an underscore.'))
    elif tags:
        body_lines = [l for l in nonblank if not HASHTAG_LINE.match(l)]
        if any(HASHTAG.search(l) for l in body_lines):
            doc.append(dict(id='LNK07', severity='style', detail='hashtags inside the body text',
                            hint='Hashtags mid-sentence read as a template. Move them to the end.'))
    # LNK08 channel fit (only with --channel linkedin)
    if channel == 'linkedin' and nonblank:
        first = len(WORD.findall(nonblank[0]))
        if first > 25:
            doc.append(dict(id='LNK08', severity='style',
                            detail='first line is {} words'.format(first),
                            hint='The hook sits before the "see more" fold. Open with one short line that carries the news.'))
        long_paras = [l for l in nonblank if len(WORD.findall(l)) > 60]
        if long_paras:
            doc.append(dict(id='LNK08', severity='style',
                            detail='{} paragraph(s) over 60 words'.format(len(long_paras)),
                            hint='LinkedIn reads as short paragraphs, one idea each. Split them.'))
    # SPL01 spelling consistency
    for pair in SPELLING_PAIRS:
        seen = [v for v in pair if re.search(NOT_H_BEFORE + '[ובלמהש]?' + v + NOT_H_AFTER, text)]
        if len(seen) > 1:
            doc.append(dict(id='SPL01', severity='check',
                            detail='both spellings used: ' + ' / '.join(seen),
                            hint='Mixed spelling of one word. Pick one and keep it throughout the text.'))
    # ADR02 addressing mix
    counts = {k: len(r.findall(text)) for k, r in PRONOUNS.items()}
    kinds = [k for k, v in counts.items() if v]
    if len(kinds) >= 2:
        doc.append(dict(id='ADR02', severity='check',
                        detail='mixed address forms: ' + ', '.join('{}={}'.format(k, counts[k]) for k in kinds),
                        hint='The reader is addressed in more than one way. Pick one (plural is the Academy suggestion for a mixed audience) and fix every verb and suffix to match.'))
    # PUN07 RTL line that opens with Latin or a digit
    for ln, line in enumerate(lines, 1):
        s = line.strip()
        if s and re.match(r'[A-Za-z0-9]', s) and HEB_WORD.search(s):
            hits.append(dict(line=ln, col=line.find(s[0]) + 1, id='PUN07', severity='check',
                             match=s[:20], hint='Hebrew line that starts with a Latin word or a number. Check paragraph direction; start with Hebrew if you can.'))
    hits.sort(key=lambda h: (h['line'], h['col']))

    scored = [h for h in hits if h['severity'] in ('rule', 'style')] + \
             [d for d in doc if d['severity'] in ('rule', 'style')]
    density = round(len(scored) * 100.0 / n_words, 1) if n_words else 0.0
    return dict(words=n_words, hits=hits, document=doc,
                counts=dict(Counter(h['id'] for h in hits)),
                flags_scored=len(scored), density_per_100_words=density)


def band(density):
    # Bands are an editing-workload label, not a verdict on who wrote the text.
    if density < 3:
        return 'light edit'
    if density < 8:
        return 'moderate edit'
    return 'heavy edit'


def fact_tokens(text):
    found = Counter()
    rest = text
    for kind, rx in FACT_TOKENS:
        for m in rx.finditer(rest):
            found[(kind, m.group(0).rstrip('.,;:)'))] += 1
        rest = rx.sub(' ', rest)
    return found


def negation_phrases(text):
    """Each negation word with the word right after it ("לא כוללת", "לא רק"), as a
    multiset. Comparing phrases, not counts, catches a negation dropped in one place and
    added in another (the count stays equal), but only when the following word differs:
    a negation moved to a sentence with the same next word ("לא כולל") is not detected."""
    return Counter((m.group(1) + (' ' + m.group(2) if m.group(2) else '')) for m in NEG_RX.finditer(text))


def word_counts(text, words):
    out = Counter()
    for wd in words:
        n = len(re.findall(NOT_H_BEFORE + '[ובלמהש]{0,2}' + wd + NOT_H_AFTER, text))
        if n:
            out[wd] = n
    return out


def compare(original, rewrite, keep=()):
    """Machine-checkable fact preservation. Returns missing / reduced / added tokens,
    Hebrew weekday and number-word changes, negation phrases that disappeared, --keep strings."""
    a, b = fact_tokens(original), fact_tokens(rewrite)
    missing = sorted(k for k in a if k not in b)
    reduced = sorted(k for k in a if k in b and b[k] < a[k])
    added = sorted(k for k in b if k not in a)
    wa, wb = word_counts(original, WEEKDAYS + NUMBER_WORDS), word_counts(rewrite, WEEKDAYS + NUMBER_WORDS)
    # a weekday or number word that disappears, or one that appears new, is a possible
    # value change; the same word merely repeated more often is not.
    hebrew_changed = sorted(wd for wd in set(wa) | set(wb)
                            if wb.get(wd, 0) < wa.get(wd, 0) or (wa.get(wd, 0) == 0 and wb.get(wd, 0) > 0))
    pa, pb = negation_phrases(original), negation_phrases(rewrite)
    na, nb = sum(pa.values()), sum(pb.values())
    neg_missing = sorted(k for k in pa if pb.get(k, 0) < pa[k])
    neg_new = sorted(k for k in pb if pa.get(k, 0) < pb[k])
    keep_missing = [k for k in keep if k and k in original and k not in rewrite]
    keep_absent_in_original = [k for k in keep if k and k not in original]
    checked = sum(a.values()) + sum(wa.values()) + len([k for k in keep if k in original])
    return dict(checked=checked,
                missing=[dict(kind=k, token=t) for k, t in missing],
                reduced=[dict(kind=k, token=t, before=a[(k, t)], after=b[(k, t)]) for k, t in reduced],
                added=[dict(kind=k, token=t) for k, t in added],
                hebrew_words_changed=[dict(word=wd, before=wa.get(wd, 0), after=wb.get(wd, 0)) for wd in hebrew_changed],
                negations=dict(before=na, after=nb, missing=neg_missing, new=neg_new),
                keep_missing=keep_missing,
                keep_not_in_original=keep_absent_in_original)


NOT_CHECKED = ('NOT checked by this script: Hebrew names and places unless passed with --keep, '
               'dates or amounts written in words beyond the number-word list, and whether the meaning '
               'of each sentence survived. Do the Step 4 manual inventory for those.')


def read_input(path):
    if path == '-':
        return sys.stdin.read()
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def main():
    ap = argparse.ArgumentParser(
        description='Flag AI and translated-English tells in Hebrew text, or check that a rewrite kept every fact.',
        epilog='Examples: hebrew-ai-tells.py post.txt --register casual ; '
               'hebrew-ai-tells.py original.txt --compare rewrite.txt ; hebrew-ai-tells.py --list-patterns')
    ap.add_argument('file', nargs='?', help='text file to scan, or - for stdin')
    ap.add_argument('--register', choices=['casual', 'professional', 'formal'],
                    help='target register; enables the matching register-mismatch flags (REG01 / REG02)')
    ap.add_argument('--format', choices=['text', 'json'], default='text')
    ap.add_argument('--compare', metavar='REWRITE',
                    help='rewrite file: report numbers, Latin tokens, URLs, e-mails, handles, Hebrew weekdays and number words '
                         'missing or changed, negation phrases (negation + next word) that disappeared, and --keep strings. Exit 0 all present, '
                         '1 something to review, 3 nothing in the original was machine-checkable (never a pass)')
    ap.add_argument('--list-patterns', action='store_true', help='print the pattern catalogue and exit')
    ap.add_argument('--channel', choices=['linkedin', 'email', 'whatsapp', 'web', 'report'],
                    help='channel of the text; linkedin enables the hook and paragraph-length checks (LNK08)')
    ap.add_argument('--keep', metavar='LIST',
                    help='with --compare: comma-separated names or phrases that must survive verbatim (e.g. "Dana Cohen,Nativ Logistics")')
    args = ap.parse_args()

    if args.list_patterns:
        seen = set()
        for p in PATTERNS:
            key = (p['id'], p['hint'])
            if key in seen:
                continue
            seen.add(key)
            print('{:6} {:6} {:16} {}'.format(p['id'], p['sev'], p['group'], p['hint']))
        for pid, hint in [('STR01', 'List-itis (document level)'), ('STR04', 'Dash density (document level)'),
                          ('STR05', 'Repeated triads (document level)'), ('STR06', 'Summary closers (document level)'),
                          ('STR07', 'Headings in a short text (document level)'),
                          ('STR08', 'Exclamation density (document level)'), ('ADR02', 'Mixed address forms (document level)'),
                          ('LNK07', 'Hashtag pile or hashtags in the body (document level)'),
                          ('LNK08', 'LinkedIn hook and paragraph length, with --channel linkedin (document level)'),
                          ('SPL01', 'Mixed spelling of the same word (document level)')]:
            print('{:6} {:6} {:16} {}'.format(pid, '', 'document', hint))
        return 0

    if not args.file:
        ap.error('give a file path or - for stdin (or use --list-patterns)')
    try:
        text = read_input(args.file)
    except (OSError, UnicodeDecodeError) as e:
        print('ERROR: cannot read {}: {}'.format(args.file, e), file=sys.stderr)
        return 2
    if not HEB_WORD.search(text):
        print('ERROR: no Hebrew letters found in the input.', file=sys.stderr)
        return 2

    if args.compare:
        try:
            rewrite = read_input(args.compare)
        except (OSError, UnicodeDecodeError) as e:
            print('ERROR: cannot read {}: {}'.format(args.compare, e), file=sys.stderr)
            return 2
        keep = [k.strip() for k in (args.keep or '').split(',') if k.strip()]
        res = compare(text, rewrite, keep)
        needs_review = bool(res['missing'] or res['hebrew_words_changed'] or res['keep_missing']
                            or res['negations']['missing'])
        if res['checked'] == 0:
            code = 3
        else:
            code = 1 if needs_review else 0
        res['exit_code'] = code
        res['not_checked'] = NOT_CHECKED
        if args.format == 'json':
            print(json.dumps(res, ensure_ascii=False, indent=2))
            return code
        print('Machine-checkable items in original: {}'.format(res['checked']))
        if res['checked'] == 0:
            print('WARNING: nothing in the original could be checked automatically (no digits, Latin tokens, '
                  'URLs, e-mails, handles, weekdays or number words, and no --keep strings). '
                  'This is NOT a pass. Check names, dates and claims by hand, or rerun with --keep "name1,name2".')
        for m in res['missing']:
            print('MISSING  [{}] {}'.format(m['kind'], m['token']))
        for k in res['keep_missing']:
            print('MISSING  [keep] {}'.format(k))
        for k in res['keep_not_in_original']:
            print('NOTE     [keep] "{}" is not in the original, so it was not checked'.format(k))
        for m in res['hebrew_words_changed']:
            print('CHANGED  [hebrew] {}: {} in original, {} in rewrite (weekday or number word; confirm the value)'.format(
                m['word'], m['before'], m['after']))
        neg = res['negations']
        if neg['missing']:
            note = ' (count unchanged, but the negation phrases differ)' if neg['after'] == neg['before'] else ''
            print('CHECK    [negation] {} negation words in original, {} in rewrite{}: confirm no statement flipped'.format(
                neg['before'], neg['after'], note))
            for ph in neg['missing']:
                print('  gone: "{}"'.format(ph))
            for ph in neg['new']:
                print('  new:  "{}"'.format(ph))
        for m in res['reduced']:
            print('FEWER    [{}] {}: {} -> {} occurrences (fine if a repeat was merged)'.format(
                m['kind'], m['token'], m['before'], m['after']))
        for m in res['added']:
            print('NEW      [{}] {} (make sure nothing was invented)'.format(m['kind'], m['token']))
        if code == 0:
            print('All machine-checkable items are still present.')
        print(NOT_CHECKED)
        return code

    res = scan(text, args.register, args.channel)
    if args.format == 'json':
        res['band'] = band(res['density_per_100_words'])
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    for h in res['hits']:
        print('L{}:C{}  {}  [{}]  "{}"  {}'.format(h['line'], h['col'], h['id'], h['severity'], h['match'], h['hint']))
    if res['document']:
        print('\nDocument level:')
        for d in res['document']:
            print('  {}  [{}]  {}. {}'.format(d['id'], d['severity'], d['detail'], d['hint']))
    print('\nWords: {}  Scored flags: {}  Density: {} per 100 words ({})'.format(
        res['words'], res['flags_scored'], res['density_per_100_words'], band(res['density_per_100_words'])))
    print('Density is an editing-workload heuristic for this catalogue, not an AI-detector score.')
    if not args.register:
        print('Tip: pass --register casual|professional|formal to add register-mismatch flags.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
