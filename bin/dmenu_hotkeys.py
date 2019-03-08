#!/usr/bin/env python3

import sys

import os
from re import compile
from subprocess import run, Popen, PIPE

__author__ = "Mariusz 'Maledorak' Korzekwa"
__credits__ = ["Mariusz 'Maledorak' Korzekwa"]
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "maledorak@gmail.com"

I3 = 'i3'
OPENBOX = 'openbox'

SUPPORTED_APPS = (I3, OPENBOX)

CONFIG = {
    I3: {
        'name': I3,
        'path': (".config", "i3", "config"),
        'parser': 'I3ConfigParser'
    },
    OPENBOX: {
        'name': OPENBOX,
        'path': (".config", "openbox", "rc.xml"),
        'parser': 'OpenBoxConfigParser'
    }
}

DMENU_COMMAND = ["rofi", "-dmenu", "-i", "-p", "HotKeys", "-lines", "20", "-width", "35"]
START_LINE_SEARCHING_PATTERN = "%%hotkey:"
END_LINE_SEARCHING_PATTERN = "%%"
ADDITIONAL_DOTS = 10


class BaseConfigParser(object):
    def parse_hotkey(self, line):
        """
        Line parsing
        :param line: string
        :return: string
        """
        raise NotImplementedError


class I3ConfigParser(BaseConfigParser):
    def parse_hotkey(self, line):
        """
        Parsing hotkey from line like following:
        `bindsym $mod+Return exec $term`
        :param line: string
        :return: string
        """
        return line.split(None)[1]


class OpenBoxConfigParser(BaseConfigParser):
    def parse_hotkey(self, line):
        """
        Parsing hotkey from line like following:
        `<keybind key="my-key-combination">`
        :param line: string
        :return: string
        """
        return line.split("\"")[1]


class DmenuHotKeys(object):
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
        self.parser = self.get_parser(app)()
        self.content = self.get_config_file_content()
        self.entries = self.get_entries(self.content)
        self.output = self.format_entries(self.entries)

    def get_parser(self, app):
        app_parser_name = CONFIG[app]['parser']
        parser = [subcls for subcls in BaseConfigParser.__subclasses__() if subcls.__name__ == app_parser_name][0]
        return parser

    def get_config_file_content(self):
        """
        Getting content of app config file.
        :param path: string with path to your app config file
        :return: string
        """
        path = os.path.join(os.path.join(os.environ.get("HOME"), *CONFIG[self.app]['path']))
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
            start=START_LINE_SEARCHING_PATTERN, end=END_LINE_SEARCHING_PATTERN))
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
        dots_length = longest_hotkey + ADDITIONAL_DOTS
        output = list()
        for hotkey, info in entries:
            output.append("{hotkey} {dots} {info}".format(
                hotkey=hotkey,
                dots="." * (dots_length - len(hotkey)),
                info=info
            ))
        return "\n".join(output)


def main():
    app = sys.argv[1]
    if app not in SUPPORTED_APPS:
        print("This app \"{}\" is not supported, try these {}".format(app, SUPPORTED_APPS))
    else:
        hot_keys = DmenuHotKeys(app)
        # subprocess piping was created based on: https://stackoverflow.com/a/4846923
        echo = Popen(["echo", hot_keys.output], stdout=PIPE)
        run(DMENU_COMMAND, stdin=echo.stdout)
        echo.stdout.close()


if __name__ == "__main__":
    main()
