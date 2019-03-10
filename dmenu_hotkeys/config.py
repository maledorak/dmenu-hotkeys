from configparser import ConfigParser
from importlib import resources


def get_config():
    cfg = ConfigParser()
    cfg.read_string(resources.read_text("dmenu_hotkeys", "config.cfg"))
    return cfg
