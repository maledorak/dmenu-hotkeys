import os

from dmenu_hotkeys.constants import (
    USER_CONFIG_PATH, DMENU_HOTKEYS_CONFIG_PATH
)
from dmenu_hotkeys.utils import _Singleton

try:
    from configparser import ConfigParser
except ImportError:
    # noinspection PyUnresolvedReferences
    from ConfigParser import ConfigParser


class Config(_Singleton('SingletonMeta', (object,), {})):
    def __init__(self):
        cfg = ConfigParser()
        if os.path.exists(USER_CONFIG_PATH):
            cfg.read(USER_CONFIG_PATH)
        else:
            cfg.read(DMENU_HOTKEYS_CONFIG_PATH)
        self.cfg = cfg

    def get_config(self):
        return self.cfg


def get_config():
    return Config().get_config()
