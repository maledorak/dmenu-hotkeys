from dmenu_hotkeys.apps import get_app_entries
from dmenu_hotkeys.config import get_config


class Feeder(object):
    """
    Feeding class for dmenu
    """

    def __init__(self, app_name):
        self.app_name = app_name
        self.config = get_config()
        self.is_dots = bool(self.config.getboolean("OTHERS", "dots"))
        self.additional_dots = int(self.config.get(
            "OTHERS", "additional_dots"))

    def format_entries(self, entries):
        """
        Adding nice looking dots between "hotkey" and "info"
        and return entries in string.
        :param entries: list of tuples, eg. [(hotkey, info), (hotkey, info)]
        :return: string
        """
        if not entries:
            return ""

        output = list()
        if not self.is_dots:
            for hotkey, info in entries:
                output.append("{hotkey}: {info}".format(
                    hotkey=hotkey,
                    info=info
                ))
            return "\n".join(output)

        longest_hotkey = max(set(len(entry[0]) for entry in entries))
        dots_length = longest_hotkey + self.additional_dots
        for hotkey, info in entries:
            output.append("{hotkey} {dots} {info}".format(
                hotkey=hotkey,
                dots="." * (dots_length - len(hotkey)),
                info=info
            ))
        return "\n".join(output)

    def run(self):
        entries = get_app_entries(self.app_name)
        return self.format_entries(entries)
