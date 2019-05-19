import os

try:
    from configparser import ConfigParser
except ImportError:
    # noinspection PyUnresolvedReferences
    from ConfigParser import ConfigParser

from dmenu_hotkeys.config import Config, get_config, init_config
from dmenu_hotkeys.constants import DMENU_HOTKEYS_CONFIG_PATH, TEST_CONFIG_PATH
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
        with mock.patch("dmenu_hotkeys.config.USER_CONFIG_PATH",
                        self.user_conf_path):
            config1 = Config()
            config2 = Config()
        self.assertEqual(config1, config2)

    def test_init_config_when_config_path_was_passed(self):
        tested_config = Config(config_path=TEST_CONFIG_PATH).get_config()
        cfg = ConfigParser()
        cfg.read(TEST_CONFIG_PATH)
        expected_arg_path_conf = cfg._sections
        self.assertDictEqual(tested_config._sections, expected_arg_path_conf)

    def test_set_config_with_cli_kwargs(self):
        conf_without_cli_kwargs = Config(config_path=TEST_CONFIG_PATH).get_config()
        self.assertEqual(conf_without_cli_kwargs.getboolean('OTHERS', 'dots'), False)
        self.assertEqual(conf_without_cli_kwargs.getint('OTHERS', 'additional_dots'), 10)
        Config._clean_singleton()  # clean singleton

        conf_with_cli_kwargs = Config(
            config_path=TEST_CONFIG_PATH,
            dots=True,
            additional_dots=5).get_config()
        unnecessary_args = 2
        self.assertEqual(
            Config.set_config.__code__.co_argcount - unnecessary_args, 2,
            msg="Added more kwargs to Config.set_config, correct this test!")
        self.assertEqual(conf_with_cli_kwargs.getboolean('OTHERS', 'dots'), True)
        self.assertEqual(conf_with_cli_kwargs.getint('OTHERS', 'additional_dots'), 5)


    def test_get_config_when_user_home_config_not_exists(self):
        self.assertFalse(os.path.exists(self.user_conf_path))
        # override user configuration path, to file which don't exist
        with mock.patch("dmenu_hotkeys.config.USER_CONFIG_PATH",
                        self.user_conf_path):
            tested_config_from_src = Config().get_config()._sections
        cfg = ConfigParser()
        cfg.read(DMENU_HOTKEYS_CONFIG_PATH)
        expected_config_from_src = cfg._sections
        self.assertDictEqual(tested_config_from_src, expected_config_from_src)

    def test_get_config_when_user_home_config_exists(self):
        self.assertFalse(os.path.exists(self.user_conf_path))
        cfg = ConfigParser()
        cfg.read(DMENU_HOTKEYS_CONFIG_PATH)
        cfg.remove_section('OTHERS')
        with open(self.user_conf_path, 'w') as configfile:
            cfg.write(configfile)
        self.assertTrue(os.path.exists(self.user_conf_path))

        # override user configuration path, to file which already exists
        with mock.patch("dmenu_hotkeys.config.USER_CONFIG_PATH",
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
        with mock.patch("dmenu_hotkeys.config.USER_CONFIG_PATH",
                        self.user_conf_path):
            config1 = Config().get_config()
            config2 = get_config()
        self.assertEqual(config1, config2)


class TestInitConfig(TempDirTestCase):
    def setUp(self):
        super(TestInitConfig, self).setUp()
        self.user_conf_path = os.path.join(self.TEMP_DIR, "config.cfg")

    def tearDown(self):
        super(TestInitConfig, self).tearDown()
        Config._clean_singleton()  # clean singleton after every test

    def test_init_config_should_be_singleton(self):
        # override user configuration path, to path which don't exist
        with mock.patch("dmenu_hotkeys.config.USER_CONFIG_PATH",
                        self.user_conf_path):
            config1 = Config().get_config()
            config2 = init_config()
        self.assertEqual(config1, config2)
