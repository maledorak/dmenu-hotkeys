import os

try:
    from configparser import ConfigParser
except ImportError:
    # noinspection PyUnresolvedReferences
    from ConfigParser import ConfigParser

from dmenu_hotkeys.config import Config, get_config
from dmenu_hotkeys.constans import SRC_CONF_PATH
from tests.utils import TempDirTestCase

try:
    from unittest import mock
except ImportError:
    import mock


class TestConfig(TempDirTestCase):
    def setUp(self):
        super(TestConfig, self).setUp()
        self.user_conf_path = os.path.join(self.TEMP_DIR, "config.cfg")

    def tearDown(self):
        super(TestConfig, self).tearDown()
        Config._clean_singleton()  # clean singleton after every test

    def test_config_should_be_singleton(self):
        # override user configuration path, to path which don't exist
        with mock.patch("dmenu_hotkeys.config.USER_CONF_PATH",
                        self.user_conf_path):
            config1 = Config()
            config2 = Config()
        self.assertEqual(config1, config2)

    def test_get_config_when(self):
        self.assertFalse(os.path.exists(self.user_conf_path))
        # override user configuration path, to file which don't exist
        with mock.patch("dmenu_hotkeys.config.USER_CONF_PATH",
                        self.user_conf_path):
            tested_config_from_src = Config().get_config()._sections
        cfg = ConfigParser()
        cfg.read(SRC_CONF_PATH)
        expected_config_from_src = cfg._sections
        self.assertDictEqual(tested_config_from_src, expected_config_from_src)

    def test_get_config_when_user_config_exists(self):
        self.assertFalse(os.path.exists(self.user_conf_path))
        cfg = ConfigParser()
        cfg.read(SRC_CONF_PATH)
        cfg.remove_section('OTHERS')
        with open(self.user_conf_path, 'w') as configfile:
            cfg.write(configfile)
        self.assertTrue(os.path.exists(self.user_conf_path))

        # override user configuration path, to file which already exists
        with mock.patch("dmenu_hotkeys.config.USER_CONF_PATH",
                        self.user_conf_path):
            tested_config_from_user = Config().get_config()._sections
        expected_config_from_user = cfg._sections
        self.assertDictEqual(tested_config_from_user, expected_config_from_user)


class TestGetConfig(TempDirTestCase):
    def setUp(self):
        super(TestGetConfig, self).setUp()
        self.user_conf_path = os.path.join(self.TEMP_DIR, "config.cfg")

    def tearDown(self):
        super(TestGetConfig, self).tearDown()
        Config._clean_singleton()  # clean singleton after every test

    def test_get_config_should_be_singleton(self):
        # override user configuration path, to path which don't exist
        with mock.patch("dmenu_hotkeys.config.USER_CONF_PATH",
                        self.user_conf_path):
            config1 = Config().get_config()
            config2 = get_config()
        self.assertEqual(config1, config2)
