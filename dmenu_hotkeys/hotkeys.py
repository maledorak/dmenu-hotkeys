# import dmenu_hotkeys.config as config
import os
from re import compile

from dmenu_hotkeys import constans as const
from dmenu_hotkeys.config import get_config
from dmenu_hotkeys.parsers import BaseConfigParser


class HotKeys(object):
    """
    Getting hotkeys info from your app config file.
    If you want use this script you should:
    1. Add the following comment line before your hotkey line which you want to use in your app config
    eg:
    `i3 line: # %%hotkey: Some description of the following hotkey %%`
    `openbox line: <--%%hotkey: Some description of the following hotkey %%-->`
    2. Run this script with your app arg (i3 or openbox)
    `./dmenu_hotkeys.py i3`
    `./dmenu_hotkeys.py openbox`
    """

    def __init__(self, app):
        self.app = app
        self.cfg = get_config()
        self.parser = self.get_parser(app)()
        self.content = self.get_config_file_content()
        self.entries = self.get_entries(self.content)
        self.output = self.format_entries(self.entries)

    def get_parser(self, app):
        app_parser_name = const.PARSERS[app]
        parser = [subcls for subcls in BaseConfigParser.__subclasses__() if subcls.__name__ == app_parser_name][0]
        return parser

    def get_config_file_content(self):
        """
        Getting content of app config file.
        :param path: string with path to your app config file
        :return: string
        """
        path = os.path.join(os.path.join(os.environ.get("HOME"), self.cfg.get("APP_CONF_PATHS", self.app)))
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
            start=self.cfg.get("OTHERS", "start_pattern"), end=self.cfg.get("OTHERS", "end_pattern")))
        content_lines = content.splitlines()
        entries = list()
        for index, line in enumerate(content_lines):
            match = regex_search.match(line)
            if match:
                info = match.group(1).strip()
                hotkey_line = content_lines[index + 1]
                hotkey = self.parser.parse_hotkey(hotkey_line)
                entries.append((hotkey, info))
        return entries

    def format_entries(self, entries):
        """
        Adding nice looking dots between "hotkey" and "info" and return entries in string.
        :param entries: list of tuples, eg. [(hotkey, info), (hotkey, info)]
        :return: string
        """
        if not entries:
            return ""

        longest_hotkey = max(set(len(entry[0]) for entry in entries))
        dots_length = longest_hotkey + int(self.cfg.get("OTHERS", "additional_dots"))
        output = list()
        for hotkey, info in entries:
            output.append("{hotkey} {dots} {info}".format(
                hotkey=hotkey,
                dots="." * (dots_length - len(hotkey)),
                info=info
            ))
        return "\n".join(output)
