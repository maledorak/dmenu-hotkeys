from dmenu_hotkeys.apps import App
from dmenu_hotkeys.constants import I3, SUPPORTED_APPS, OPENBOX, PARSERS, BSPWM
from tests.utils import TestConfigTestCase


class TestApp(TestConfigTestCase):
    def test_get_app_config_generic_test(self):
        for app_name in SUPPORTED_APPS:
            app = App(app_name)
            app_conf = app.get_app_config()
            self.assertEqual(app.name, app_name)
            self.assertIn(PARSERS[app_name], app.parser.__class__.__name__)
            self.assertIn(
                "{} config".format(app_name), app_conf,
                msg="Add 'app_name config' comment to the config fixture")

    def test_get_entries_from_configs_generic_test(self):
        expected_data_from_config_files = {
            I3: {
                "entries_length": 4,
                "first_entry": ('$mod+q', 'Add todoist task')
            },
            BSPWM: {
                "entries_length": 3,
                "first_entry": ('super + alt + Escape', 'Exit bspwm')
            },
            OPENBOX: {
                "entries_length": 2,
                "first_entry": ('A-F4', 'Close container')
            }
        }

        self.assertEqual(
            len(expected_data_from_config_files), len(SUPPORTED_APPS),
            msg="Update 'expected_data_from_config_files' to new supported apps")

        for app_name in SUPPORTED_APPS:
            app = App(app_name)
            app_conf = app.get_app_config()
            entries = app.get_entries(app_conf)
            expected = expected_data_from_config_files[app_name]
            self.assertEqual(len(entries), expected["entries_length"])
            self.assertEqual(entries[0], expected["first_entry"])

    def test_get_entries_when_hotkeys_line_is_empty(self):
        lines = {
            I3: "# %%hotkey: Open %%\n\nbindsym $mod+w xec --no-startup-id rofi -show window",
            BSPWM: "# %%hotkey: Close %%\n\nalt + F4",
            OPENBOX: "<!-- %%hotkey: Open %% -->\n\n<keybind key=\"A-F4\">"
        }
        self.assertEqual(
            len(lines), len(SUPPORTED_APPS),
            msg="Update 'lines' to new supported apps")
        for app_name in SUPPORTED_APPS:
            app = App(app_name)
            entries = app.get_entries(lines[app_name])
            self.assertEqual(len(entries), 0)

    def test_get_entries_when_hotkeys_line_is_end_of_file(self):
        hotkey_tag_lines = {
            I3: "# %%hotkey: Open %%",
            BSPWM: "# %%hotkey: Close %%",
            OPENBOX: "<!-- %%hotkey: Open %% -->"
        }
        self.assertEqual(
            len(hotkey_tag_lines), len(SUPPORTED_APPS),
            msg="Update 'hotkey_tag_lines' to new supported apps")
        for app_name in SUPPORTED_APPS:
            app = App(app_name)
            entries = app.get_entries(hotkey_tag_lines[app_name])
            self.assertEqual(len(entries), 0)

    def test_get_entries_when_hotkeys_line_is_not_redable_by_parser(self):
        lines = {
            I3: "# %%hotkey: Open %%\nsome bad line",
            BSPWM: "# %%hotkey: Close %%\n",  # in bspwm only empty line is wrong
            OPENBOX: "<!-- %%hotkey: Open %% -->\nsome bad line"
        }
        self.assertEqual(
            len(lines), len(SUPPORTED_APPS),
            msg="Update 'lines' to new supported apps")
        for app_name in SUPPORTED_APPS:
            app = App(app_name)
            entries = app.get_entries(lines[app_name])
            self.assertEqual(len(entries), 0)
