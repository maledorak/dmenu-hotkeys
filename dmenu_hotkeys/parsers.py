from dmenu_hotkeys.constants import PARSERS


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
        if "bindsym" not in line:
            return ""
        try:
            return line.split(None)[1]
        except IndexError:  # empty or wrong line
            return ""


class OpenBoxConfigParser(BaseConfigParser):
    def parse_hotkey(self, line):
        """
        Parsing hotkey from line like following:
        `<keybind key="my-key-combination">`
        :param line: string
        :return: string
        """
        if "keybind" not in line:
            return ""
        try:
            return line.split("\"")[1]  # todo add xml parser
        except IndexError:  # empty or wrong line
            return ""


def get_parser(app_name):
    """
    Return parser based on app name.
    :param app_name: String
    :return: parser object
    """
    app_parser_name = PARSERS[app_name]
    parser = [subcls for subcls in BaseConfigParser.__subclasses__() if
              subcls.__name__ == app_parser_name][0]
    return parser()  # return parser object instead of class
