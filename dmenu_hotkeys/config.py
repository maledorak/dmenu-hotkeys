from configparser import ConfigParser
from importlib import resources


class Config(object):
    def __init__(self, **kwargs):
        self.parsed_cfg = self.get_config_content()
        self.kwargs_cfg = kwargs
        self.config = self.get_config(self.parsed_cfg, self.kwargs_cfg)

    def get_config_content(self):
        cfg = ConfigParser()
        cfg.read_string(resources.read_text("dmenu_hotkeys", "config.cfg"))
        return cfg

    def get_config(self, parsed_cfg, kwargs_cfg):
        import bpdb;bpdb.set_trace();
        return parsed_cfg
