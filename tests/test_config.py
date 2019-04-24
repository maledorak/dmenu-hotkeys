import os

try:
    from configparser import ConfigParser
except ImportError:
    # noinspection PyUnresolvedReferences
    from ConfigParser import ConfigParser

from dmenu_hotkeys.config import get_config
from dmenu_hotkeys.constans import SRC_CONF_PATH
from tests.utils import TempDirTestCase

try:
    from unittest import mock
except ImportError:
    import mock


class TestGetConfig(TempDirTestCase):
    def setUp(self):
        super(TestGetConfig, self).setUp()
        self.user_conf_path = os.path.join(self.TEMP_DIR, "config.cfg")

    def test_get_config_when_no_user_config(self):
        self.assertFalse(os.path.exists(self.user_conf_path))
        with mock.patch("dmenu_hotkeys.config.USER_CONF_PATH",
                        self.user_conf_path):
            tested_config = get_config()._sections
        cfg = ConfigParser()
        cfg.read(SRC_CONF_PATH)
        expected_config = cfg._sections
        self.assertDictEqual(tested_config, expected_config)

    def test_get_config_when_user_config_exists(self):
        self.assertFalse(os.path.exists(self.user_conf_path))
        cfg = ConfigParser()
        cfg.read(SRC_CONF_PATH)
        cfg.remove_section('OTHERS')
        with open(self.user_conf_path, 'w') as configfile:
            cfg.write(configfile)
        self.assertTrue(os.path.exists(self.user_conf_path))

        with mock.patch("dmenu_hotkeys.config.USER_CONF_PATH",
                        self.user_conf_path):
            tested_config = get_config()._sections
        self.assertDictEqual(tested_config, cfg._sections)
