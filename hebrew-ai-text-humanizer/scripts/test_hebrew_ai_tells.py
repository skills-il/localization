#!/usr/bin/env python3
"""Regression tests for hebrew-ai-tells.py (stdlib unittest, no network).

Run: python3 scripts/test_hebrew_ai_tells.py

fixtures/expert-linkedin.txt and fixtures/punctuation-stress.txt are built from the
lines quoted in the 2026-11-02 independent expert review: real AI tells the first
version missed, and correct Hebrew it wrongly flagged as an Academy rule.
"""
import importlib.util
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('tells', os.path.join(HERE, 'hebrew-ai-tells.py'))
tells = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tells)


def ids(text, register=None, channel=None):
    res = tells.scan(text, register, channel)
    return [h['id'] for h in res['hits']] + [d['id'] for d in res['document']], res


def fixture(name):
    with open(os.path.join(HERE, 'fixtures', name), encoding='utf-8') as fh:
        return fh.read()


class ExpertLinkedIn(unittest.TestCase):
    def setUp(self):
        self.found, self.res = ids(fixture('expert-linkedin.txt'), 'professional', 'linkedin')

    def test_catches_linkedin_and_grammar_tells(self):
        for pid in ('LNK01', 'LNK02', 'LNK03', 'LNK04', 'LNK05', 'LNK07', 'GRM01', 'GRM02', 'GRM03'):
            self.assertIn(pid, self.found, pid)

    def test_no_false_rule_flags(self):
        # "היה ויכוח", "מס." (tax), "יש לקוחות", "היא לא הגיעה ... כי היא" are correct Hebrew
        for pid in ('CAL05', 'PUN04', 'REG01', 'CAL11'):
            self.assertNotIn(pid, self.found, pid)
        self.assertEqual([h for h in self.res['hits'] if h['severity'] == 'rule'], [])


class PunctuationStress(unittest.TestCase):
    def setUp(self):
        self.found, self.res = ids(fixture('punctuation-stress.txt'), 'casual')

    def test_true_positives(self):
        for pid in ('PUN01', 'PUN02', 'PUN04', 'PUN06', 'CAL05'):
            self.assertIn(pid, self.found, pid)

    def test_whole_word_is_not_a_prefix(self):
        line1 = [h for h in self.res['hits'] if h['line'] == 1]
        self.assertEqual(line1, [], 'מה - 5 must not be read as a prefix plus dash')

    def test_conditional_haya_ve_is_check_not_rule(self):
        cal05 = [h for h in self.res['hits'] if h['id'] == 'CAL05']
        self.assertTrue(cal05 and all(h['severity'] == 'check' for h in cal05))

    def test_bare_mas_tax_not_flagged_but_mas_number_is(self):
        self.assertNotIn('PUN04', ids('שילמנו על זה לא מעט מס.')[0])
        self.assertIn('PUN04', ids('הזמנה מס. 48213 יצאה.')[0])


EN_DASH = chr(0x2013)   # built from an escape so the skill folder stays free of the character
EM_DASH = chr(0x2014)


class JudgeFindings(unittest.TestCase):
    """Round-2 independent judge: range dash, RLM advice, PUN05 status."""

    def test_range_dash_is_never_a_rule(self):
        text = 'בחודשים ינואר' + EN_DASH + 'מרץ, ראו סעיפים א' + EN_DASH + 'ד ועמודים 46' + EN_DASH + '53.'
        found, res = ids(text)
        self.assertEqual([h for h in res['hits'] if h['severity'] == 'rule'], [])
        self.assertNotIn('STR04', [d['id'] for d in res['document']])

    def test_glued_em_dash_still_a_rule(self):
        found, res = ids('המערכת' + EM_DASH + 'החדשה עובדת.')
        self.assertIn(('STR04', 'rule'), [(h['id'], h['severity']) for h in res['hits']])

    def test_number_inside_a_name_is_not_a_bidi_flag(self):
        for t in ('ראינו ש-iPhone 15 נמכר היטב.', 'Version 3 שוחררה השבוע.'):
            hits = [h for h in tells.scan(t, None)['hits'] if h['id'] == 'PUN07' and h['match'][:1].isdigit()]
            self.assertEqual(hits, [], t)

    def test_separate_number_after_english_phrase_is_flagged(self):
        self.assertIn('PUN07', ids('קראתי את Harry Potter 3 פעמים.')[0])

    def test_space_before_punctuation_is_style_not_rule(self):
        res = tells.scan('מה שלומך ?', None)
        self.assertEqual([h['severity'] for h in res['hits'] if h['id'] == 'PUN05'], ['style'])


class Round3(unittest.TestCase):
    """Second expert review and second judge."""

    def test_negation_counter_closed_list(self):
        # מלא (full), שאל (asked), אל, and ללא counted once, not as ל+לא
        p = tells.negation_phrases('המשלוח מלא. הוא שאל אל המנהל. משלוח ללא עלות.')
        self.assertEqual(sum(p.values()), 1)
        self.assertEqual(list(p), ['ללא עלות'])

    def test_negation_swap_with_equal_count_is_reported(self):
        res = tells.compare('המחיר לא כולל משלוח. המוצר מלא.', 'המחיר כולל משלוח. זה לא מסובך.')
        self.assertEqual(res['negations']['before'], res['negations']['after'])
        self.assertEqual(res['negations']['missing'], ['לא כולל'])

    def test_geresh_day_range_not_counted_as_dash(self):
        text = 'פתוח א\'' + EN_DASH + 'ה\' 9:00' + EN_DASH + '18:00, ו\' 9:00' + EN_DASH + '13:00, ושבת סגור. ' + 'מילה ' * 20
        res = tells.scan(text, None)
        self.assertNotIn('STR04', [d['id'] for d in res['document']])
        self.assertEqual([h for h in res['hits'] if h['id'] == 'STR04'], [])

    def test_pun06_is_check_and_section_label_not_rule(self):
        res = tells.scan('ראו סעיף ב 3 בחוזה.', None)
        self.assertEqual([h for h in res['hits'] if h['severity'] == 'rule'], [])
        self.assertEqual({h['severity'] for h in res['hits'] if h['id'] == 'PUN06'}, {'check'})

    def test_grm01_skips_adjective(self):
        self.assertNotIn('GRM01', ids('אני אמיתי עם עצמי.')[0])
        self.assertIn('GRM01', ids('אני הובלתי את הפרויקט.')[0])

    def test_glued_em_dash_range_is_check_not_rule(self):
        cases = ['פתוח בחודשים ינואר' + EM_DASH + 'מרץ.',
                 'שעות פעילות א\'' + EM_DASH + 'ה\' בבוקר.',
                 'בשעות 9' + EM_DASH + '13 בלבד.']
        for t in cases:
            res = tells.scan(t, None)
            str04 = [h for h in res['hits'] if h['id'] == 'STR04']
            self.assertTrue(str04, t)
            self.assertEqual({h['severity'] for h in str04}, {'check'}, t)
            self.assertIn('unspaced en dash', str04[0]['hint'])
        # a glued em dash between ordinary words is still a rule
        res = tells.scan('המערכת' + EM_DASH + 'החדשה עובדת.', None)
        self.assertEqual([h['severity'] for h in res['hits'] if h['id'] == 'STR04'], ['rule'])

    def test_new_coverage(self):
        self.assertIn('LNK01', ids('אני נרגשת לראות לאן נגיע.')[0])
        self.assertIn('REG01', ids('יש לשים לב למועד.', 'professional')[0])


class Compare(unittest.TestCase):
    def test_zero_tokens_is_not_a_pass(self):
        res = tells.compare('שלום לכולם, נתראה בקרוב.', 'היי לכולם, נתראה.')
        self.assertEqual(res['checked'], 0)

    def test_expert_meaning_changes_are_reported(self):
        orig = 'דנה כהן תגיע ביום חמישי. ההזמנה לא כוללת משלוח. יש שלושה פריטים.'
        new = 'דנה לוי תגיע ביום שישי. ההזמנה כוללת משלוח. יש חמישה פריטים.'
        res = tells.compare(orig, new, keep=['דנה כהן'])
        changed = {m['word'] for m in res['hebrew_words_changed']}
        self.assertTrue({'חמישי', 'שישי', 'שלושה', 'חמישה'} <= changed)
        self.assertEqual(res['keep_missing'], ['דנה כהן'])
        self.assertLess(res['negations']['after'], res['negations']['before'])

    def test_code_change_detected(self):
        res = tells.compare('קוד הנחה SORRY15 להזמנה 48213.', 'קוד הנחה SORRY16 להזמנה 48213.')
        self.assertEqual([m['token'] for m in res['missing']], ['SORRY15'])

    def test_repeated_token_reduction_reported(self):
        res = tells.compare('הזמנה 48213 ועוד 48213.', 'הזמנה 48213.')
        self.assertEqual(res['reduced'][0]['token'], '48213')


if __name__ == '__main__':
    unittest.main(verbosity=1)
