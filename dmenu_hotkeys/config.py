from configparser import ConfigParser
from importlib import resources


def get_config():
    cfg = ConfigParser()
    cfg.read_string(resources.read_text("dmenu_hotkeys", "config.cfg"))
    return cfg

def get_config2():
    cfg = ConfigParser()
    cfg.read_file(open(r"config.cfg"))
    return cfg
