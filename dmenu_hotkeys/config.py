import os

from dmenu_hotkeys.constants import (
    USER_CONFIG_PATH, DMENU_HOTKEYS_CONFIG_PATH, TEST_CONFIG_PATH
)
from dmenu_hotkeys.utils import _Singleton

try:
    from configparser import ConfigParser
except ImportError:
    # noinspection PyUnresolvedReferences
    from ConfigParser import ConfigParser


class Config(_Singleton('SingletonMeta', (object,), {})):
    def __init__(self, arg_path=None):
        cfg = ConfigParser()
        if arg_path and os.path.exists(arg_path):
            cfg.read(arg_path)
        elif os.environ.get('DMENU_HOTKEYS_TEST_CONFIG'):
            cfg.read(TEST_CONFIG_PATH)
        elif os.path.exists(USER_CONFIG_PATH):
            cfg.read(USER_CONFIG_PATH)
        else:
            cfg.read(DMENU_HOTKEYS_CONFIG_PATH)
        self.cfg = cfg

    def get_config(self):
        return self.cfg


def init_config(arg_path=None):
    config = Config(arg_path=arg_path)
    return config.get_config()


def get_config():
    return Config().get_config()
