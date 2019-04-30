import os
from re import compile

from dmenu_hotkeys.config import get_config
from dmenu_hotkeys.parsers import get_parser


class App(object):
    def __init__(self, name):
        self.name = name
        self.parser = get_parser(app_name=name)
        self.config = get_config()

    def get_app_config(self):
        """
        Getting content of supported application config file.
        :return: string
        """
        path = os.path.expandvars(self.config.get("APP_CONF_PATHS", self.name))
        with open(path, "r") as file_:
            content = file_.read()
        return content

    def get_entries(self, content):
        """
        Geting entries of hotkey "info" and hotkey itself.
        :param content: string with app config content
        :return: list of tuples, eg. [(hotkey, info), (hotkey, info)]
        """
        regex_search = compile(r"^.*{start}([^%]+){end}.*$".format(
            start=self.config.get("OTHERS", "start_pattern"),
            end=self.config.get("OTHERS", "end_pattern")
        ))
        content_lines = content.splitlines()
        entries = list()
        for index, line in enumerate(content_lines):
            info_match = regex_search.match(line)
            if info_match:
                try:
                    hotkey_line = content_lines[index + 1]
                except IndexError:
                    break
                info = info_match.group(1).strip()
                hotkey = self.parser.parse_hotkey(hotkey_line)
                # todo add bad lines report, maybe logger or click.echo
                if info and hotkey:
                    entries.append((hotkey, info))
        return entries

    def run(self):
        config_content = self.get_app_config()
        return self.get_entries(config_content)


def get_app_entries(app_name):
    return App(app_name).run()
