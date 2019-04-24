import os

DMENU = "dmenu"
ROFI = "rofi"
SUPPORTED_MENUS = [DMENU, ROFI]

I3 = 'i3'
OPENBOX = 'openbox'
SUPPORTED_APPS = [I3, OPENBOX]

PARSERS = {
    I3: "I3ConfigParser",
    OPENBOX: "OpenBoxConfigParser"
}

DMENU_HOTKEYS_DIR = os.path.dirname(__file__)
SRC_CONF_PATH = os.path.join(DMENU_HOTKEYS_DIR, "config.cfg")
USER_CONF_PATH = os.path.expandvars("$HOME/.config/dmenu_hotkeys/config.cfg")
