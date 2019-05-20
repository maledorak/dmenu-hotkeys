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
    def __init__(self, config_path=None, **cli_kwargs):
        cfg = ConfigParser()
        if config_path and os.path.exists(config_path):
            cfg.read(config_path)
        elif os.environ.get('DMENU_HOTKEYS_TEST_CONFIG'):
            cfg.read(TEST_CONFIG_PATH)
        elif os.path.exists(USER_CONFIG_PATH):
            cfg.read(USER_CONFIG_PATH)
        else:
            cfg.read(DMENU_HOTKEYS_CONFIG_PATH)
        self._file_cfg = cfg
        self.set_config(cfg=cfg, **cli_kwargs)

    def set_config(self, cfg, dots=None, additional_dots=None):
        cli_kwargs_to_sections_map = {
            "OTHERS.dots": dots,
            "OTHERS.additional_dots": additional_dots
        }
        for name, value in cli_kwargs_to_sections_map.items():
            if value is not None:
                section, option = name.split(".")
                cfg.set(section=section, option=option, value=str(value))
        self.cfg = cfg

    def get_config(self):
        return self.cfg


def init_config(**cli_kwargs):
    config = Config(**cli_kwargs)
    return config.get_config()


def get_config():
    return Config().get_config()

# todo update README
# todo release new version
