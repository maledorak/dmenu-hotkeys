import unittest

from dmenu_hotkeys.constants import PARSERS
from dmenu_hotkeys.parsers import (
    BaseConfigParser, I3ConfigParser, OpenBoxConfigParser, get_parser
)


class TestBaseConfigParser(unittest.TestCase):
    def test_parse_hotkey(self):
        parser = BaseConfigParser()
        with self.assertRaises(NotImplementedError):
            parser.parse_hotkey('string')


class TestI3ConfigParser(unittest.TestCase):
    def setUp(self):
        self.parser = I3ConfigParser()

    def test_parse_hotkey_when_all_ok(self):
        line_with_tabs = "bindsym \tmod+a\t\t\texec some"
        line_without_tabs = "bindsym mod+a exec some"
        self.assertEqual(self.parser.parse_hotkey(line_with_tabs), 'mod+a')
        self.assertEqual(self.parser.parse_hotkey(line_without_tabs), 'mod+a')

    def test_parse_hotkey_when_wrong_tag(self):
        wrong_line = 'band'
        self.assertEqual(self.parser.parse_hotkey(wrong_line), '')

    def test_parse_hotkey_when_wrong_line(self):
        wrong_line = "bindmod+aexecsome"
        self.assertEqual(self.parser.parse_hotkey(wrong_line), '')

    def test_parse_hotkey_when_empty_line(self):
        empty_line = ""
        self.assertEqual(self.parser.parse_hotkey(empty_line), '')


class TestOpenBoxConfigParser(unittest.TestCase):
    def setUp(self):
        self.parser = OpenBoxConfigParser()

    def test_parse_hotkey_when_all_ok(self):
        line = '<keybind key="A-F4">'
        self.assertEqual(self.parser.parse_hotkey(line), "A-F4")

    def test_parse_hotkey_when_wrong_tag(self):
        wrong_line = '<other_tag>'
        self.assertEqual(self.parser.parse_hotkey(wrong_line), '')

    def test_parse_hotkey_when_empty_line(self):
        empty_line = ""
        self.assertEqual(self.parser.parse_hotkey(empty_line), '')

    def test_parse_hotkey_when_wrong_line(self):
        wrong_line = 'some'
        self.assertEqual(self.parser.parse_hotkey(wrong_line), '')


class TestGetParserGenericTest(unittest.TestCase):
    def test_get_parser(self):
        for app, parser_name in PARSERS.items():
            parser = get_parser(app)
            self.assertEqual(parser.__class__.__name__, parser_name)
