from unittest import TestCase

from dmenu_hotkeys.config import get_config
from dmenu_hotkeys.constants import I3
from dmenu_hotkeys.feeders import Feeder


class TestFeeder(TestCase):
    def test_format_entries_when_no_entries(self):
        test_entries = []
        feeder = Feeder(I3)
        self.assertEqual(feeder.format_entries(test_entries), "")

    def test_format_entries_check_lines(self):
        test_entries = [
            ('ctrl+a', "Run amarok"),
            ('ctrl+t', "Run translator")
        ]
        feeder = Feeder(I3)
        feed = feeder.format_entries(test_entries)
        config = get_config()
        dots = "." * int(config.get("OTHERS", "additional_dots"))
        for feed_line in feed.splitlines():
            self.assertIn(dots, feed_line)
