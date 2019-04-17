try:
    from configparser import ConfigParser
except ImportError:
    # noinspection PyUnresolvedReferences
    from ConfigParser import ConfigParser

try:
    from importlib import resources
except ImportError:  # for python lower than 3.7
    import importlib_resources as resources


def get_config():
    cfg = ConfigParser()
    cfg.read_string(resources.read_text("dmenu_hotkeys", "config.cfg"))
    return cfg
