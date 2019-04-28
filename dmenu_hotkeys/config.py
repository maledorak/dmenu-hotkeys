import os

from dmenu_hotkeys.constans import USER_CONF_PATH, SRC_CONF_PATH
from dmenu_hotkeys.utils import _Singleton

try:
    from configparser import ConfigParser
except ImportError:
    # noinspection PyUnresolvedReferences
    from ConfigParser import ConfigParser


class Config(_Singleton('SingletonMeta', (object,), {})):
    def __init__(self):
        cfg = ConfigParser()
        if os.path.exists(USER_CONF_PATH):
            cfg.read(USER_CONF_PATH)
        else:
            cfg.read(SRC_CONF_PATH)
        self.cfg = cfg

    def get_config(self):
        return self.cfg


def get_config():
    return Config().get_config()
