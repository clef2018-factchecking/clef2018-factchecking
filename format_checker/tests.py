from unittest import TestCase
from os.path import join, dirname

from format_checker import subtaskA, subtaskB

_ROOT_DIR = dirname(dirname(__file__))
_TEST_DATA_FOLDER = join(_ROOT_DIR, 'data/format_checker_tests/')


class FormatCheckerA(TestCase):
    _OK_FILES = ['subtaskA_OK.txt']
    _NOT_OK_FILES = ['subtaskA_NOTOK_0.txt', 'subtaskA_NOTOK_MISSING_ID.txt', 'subtaskA_NOTOK_DUP_LINE_NUM.txt']

    def test_ok(self):
        for _file in self._OK_FILES:
            self.assertTrue(subtaskA.check_format(join(_TEST_DATA_FOLDER, _file)))

    def test_not_ok(self):
        for _file in self._NOT_OK_FILES:
            self.assertFalse(subtaskA.check_format(join(_TEST_DATA_FOLDER, _file)))


class FormatCheckerB(TestCase):
    _OK_FILES = ['subtaskB_OK.txt','subtaskB_OK_LOWER.txt', 'subtaskB_WARN_MISSING_LABEL.txt']
    _NOT_OK_FILES = ['subtaskB_NOTOK_OTHER_LABELS.txt', 'subtaskB_NOTOK_MISSING_ID.txt', 'subtaskB_NOTOK_DUP_CLAIM_NUM.txt']

    def test_ok(self):
        for _file in self._OK_FILES:
            self.assertTrue(subtaskB.check_format(join(_TEST_DATA_FOLDER, _file)))

    def test_not_ok(self):
        for _file in self._NOT_OK_FILES:
            self.assertFalse(subtaskB.check_format(join(_TEST_DATA_FOLDER, _file)))
