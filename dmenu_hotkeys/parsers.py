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
