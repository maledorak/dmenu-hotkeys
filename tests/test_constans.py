import os

from dmenu_hotkeys import constants
from tests.utils import TempDirTestCase

try:
    from importlib import reload
except ImportError:
    from imp import reload


class TestConstants(TempDirTestCase):
    def test_supported_menus(self):
        self.assertEqual(len(constants.SUPPORTED_MENUS), 2)

    def test_supported_apps(self):
        self.assertEqual(len(constants.SUPPORTED_APPS), 2)

    def test_supported_parsers(self):
        self.assertEqual(len(constants.PARSERS), 2)

    def test_check_path_DMENU_HOTKEYS_DIR(self):
        expected = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'dmenu_hotkeys')
        self.assertEqual(constants.DMENU_HOTKEYS_DIR, expected)

    def test_check_path_DMENU_HOTKEYS_CONFIG_PATH(self):
        expected = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'dmenu_hotkeys', 'config.cfg')
        self.assertEqual(constants.DMENU_HOTKEYS_CONFIG_PATH, expected)

    def test_check_path_XDG_CONFIG_HOME_when_XDG_exist(self):
        expected = os.path.join(self.TEMP_DIR, "test_config")
        os.environ["XDG_CONFIG_HOME"] = expected
        reload(constants)
        self.assertEqual(constants.XDG_CONFIG_HOME, expected)

    def test_check_path_XDG_CONFIG_HOME_when_XDG_env_dont_exist(self):
        os.environ["XDG_CONFIG_HOME"] = 'some'
        self.assertEqual(os.environ["XDG_CONFIG_HOME"], 'some')
        del os.environ["XDG_CONFIG_HOME"]
        self.assertIsNone(os.environ.get("XDG_CONFIG_HOME"))

        home = os.path.join(self.TEMP_DIR, "test_home")
        os.environ["HOME"] = home
        reload(constants)
        expected = os.path.join(home, ".config")
        self.assertEqual(constants.XDG_CONFIG_HOME, expected)

    def test_check_path_USER_CONFIG_PATH(self):
        config_home = os.path.join(self.TEMP_DIR, "test_config")
        os.environ["XDG_CONFIG_HOME"] = config_home
        expected = os.path.join(config_home, 'dmenu_hotkeys', 'config.cfg')
        reload(constants)
        self.assertEqual(constants.USER_CONFIG_PATH, expected)
