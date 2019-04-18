import unittest

from dmenu_hotkeys.parsers import BaseConfigParser, I3ConfigParser, OpenBoxConfigParser


class TestBaseConfigParser(unittest.TestCase):
    def test_parse_hotkey(self):
        parser = BaseConfigParser()
        with self.assertRaises(NotImplementedError):
            parser.parse_hotkey('string')


class TestI3ConfigParser(unittest.TestCase):
    def setUp(self):
        self.line_with_tabs = "bind \tmod+a\t\t\texec some"
        self.line_without_tabs = "bind mod+a exec some"

    def test_parse_hotkey(self):
        parser = I3ConfigParser()
        self.assertEqual(parser.parse_hotkey(self.line_with_tabs), 'mod+a')
        self.assertEqual(parser.parse_hotkey(self.line_without_tabs), 'mod+a')


class TestOpenBoxConfigParser(unittest.TestCase):
    def setUp(self):
        self.line = '<keybind key="A-F4">'

    def test_parse_hotkey(self):
        parser = OpenBoxConfigParser()
        self.assertEqual(parser.parse_hotkey(self.line), "A-F4")
