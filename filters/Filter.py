import re
import unittest

def is_line_separate_record(line):
    return re.match("\A=\d\d\.\d\d", line)

class Filter:
    settings = None

    def __init__(self, settings=None):
        """
        Base constructor
        @param settings: there are could be some additional settings for filters
        @return:
        """
        self.settings = settings

    def apply(self, source):
        """
        Perform filtration logic
        @param source: iterable of strings, that represents content for filtration
        @return: iterable of strings, result of applying logic of filtration
        """
        return source


class Settings:
    pass


class FilterTest(unittest.TestCase):
    def test_correct_template_line(self):
        self.assertTrue(is_line_separate_record("=27.02.2014 18:31:13.384 [DEBUG]"), "this line starts is separate log entry")

    def test_incorrect_template_line(self):
        self.assertFalse(is_line_separate_record("random string without any sense"), "this is random meaningless line is not and extra entry of log")

if __name__ == "__main__":
    print("self-testing for Filter.py")
    unittest.main()