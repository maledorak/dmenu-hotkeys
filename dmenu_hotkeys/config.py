import os

from dmenu_hotkeys.constans import USER_CONF_PATH, SRC_CONF_PATH

try:
    from configparser import ConfigParser
except ImportError:
    # noinspection PyUnresolvedReferences
    from ConfigParser import ConfigParser


def get_config():
    cfg = ConfigParser()
    if os.path.exists(USER_CONF_PATH):
        cfg.read(USER_CONF_PATH)
    else:
        cfg.read(SRC_CONF_PATH)
    return cfg
