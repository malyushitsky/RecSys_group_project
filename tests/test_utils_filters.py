

import unittest
import sys
sys.path.append('..')
from Telegram_bot.utils.filters import check_query  # Assume your function is in your_module.py

class TestCheckQuery(unittest.TestCase):

    def test_valid_queries(self):
        self.assertTrue(check_query("Hello, world"))
        self.assertTrue(check_query("123,good day."))
        self.assertTrue(check_query("This is a test; it should work."))

    def test_invalid_characters(self):
        self.assertFalse(check_query("Hello@world"))
        self.assertFalse(check_query("Test#1"))
        self.assertFalse(check_query("Why?"))

    def test_regex_match_failure(self):
        self.assertFalse(check_query("----"))
        self.assertFalse(check_query("...."))
        self.assertFalse(check_query(";;;;"))
        self.assertFalse(check_query(""))

    def test_consecutive_characters(self):
        self.assertFalse(check_query("Heeeeello"))
        self.assertFalse(check_query("Nooooooo"))
        self.assertFalse(check_query("4444"))

    def test_bad_characters_ratio(self):
        self.assertFalse(check_query("1234,"))
        self.assertFalse(check_query("1234, abc"))
        self.assertFalse(check_query("-.,-"))

    def test_length_constraints(self):
        self.assertFalse(check_query("Hi"))  # Too short
        text_101 = "a" * 101  # Too long
        self.assertFalse(check_query(text_101))

# check_query("123, good day.")

if __name__ == "__main__":
    print('---$#^$#---')
    print(check_query("Hello, world"))
    unittest.main()

