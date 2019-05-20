from unittest import TestCase

from dmenu_hotkeys.config import get_config
from dmenu_hotkeys.constants import I3
from dmenu_hotkeys.feeders import Feeder


class TestFeeder(TestCase):
    def test_format_entries_when_no_entries(self):
        test_entries = []
        feeder = Feeder(I3)
        self.assertEqual(feeder.format_entries(test_entries), "")

    def test_format_entries_check_lines_with_dots(self):
        test_entries = [
            ('ctrl+a', "Run amarok"),
            ('ctrl+t', "Run translator")
        ]
        feeder = Feeder(I3)
        feeder.is_dots = True
        feed = feeder.format_entries(test_entries)
        config = get_config()
        additional_dots = int(config.get("OTHERS", "additional_dots"))
        dots = "." * additional_dots
        for index, feed_line in enumerate(feed.splitlines()):
            entry = test_entries[index]
            self.assertEqual("{} {} {}".format(entry[0], dots, entry[1]),
                             feed_line)

    def test_format_entries_check_lines_without_dots(self):
        test_entries = [
            ('ctrl+a', "Run amarok"),
            ('ctrl+t', "Run translator")
        ]
        feeder = Feeder(I3)
        feeder.is_dots = False
        feed = feeder.format_entries(test_entries)
        for index, feed_line in enumerate(feed.splitlines()):
            entry = test_entries[index]
            self.assertEqual("{}: {}".format(*entry), feed_line)
