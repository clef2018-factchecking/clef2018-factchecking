from unittest import TestCase
from os.path import join

from format_checker import subtaskA, subtaskB

_EXAMPLES_FOLDER = 'examples/'


class FormatCheckerA(TestCase):
    _OK_FILES = ['subtaskA_OK.txt', 'subtaskA_WARN_MISSING_ID.txt', 'subtaskA_WARN_UNORDERED.txt']
    _NOT_OK_FILES = ['subtaskA_NOTOK_ALPHA.txt', 'subtaskA_NOTOK_LEADING0.txt', 'subtaskA_NOTOK_0.txt', 'subtaskA_NOTOK_SEP.txt']

    def test_ok(self):
        for _file in self._OK_FILES:
            self.assertTrue(subtaskA.check_format(join(_EXAMPLES_FOLDER, _file)))

    def test_not_ok(self):
        for _file in self._NOT_OK_FILES:
            self.assertFalse(subtaskB.check_format(join(_EXAMPLES_FOLDER, _file)))


class FormatCheckerB(TestCase):
    _OK_FILES = ['subtaskB_OK.txt','subtaskB_OK_LOWER.txt', 'subtaskB_WARN_MISSING_LABEL.txt']
    _NOT_OK_FILES = ['subtaskB_NOTOK_OTHER_LABELS.txt', 'subtaskB_NOTOK_MISSING_ID.txt']

    def test_ok(self):
        for _file in self._OK_FILES:
            self.assertTrue(subtaskB.check_format(join(_EXAMPLES_FOLDER, _file)))

    def test_not_ok(self):
        for _file in self._NOT_OK_FILES:
            self.assertFalse(subtaskB.check_format(join(_EXAMPLES_FOLDER, _file)))
