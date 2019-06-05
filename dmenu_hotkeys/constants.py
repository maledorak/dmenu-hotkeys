import os

DMENU = "dmenu"
ROFI = "rofi"
SUPPORTED_MENUS = [DMENU, ROFI]

AWESOME = 'awesome'
BSPWM = 'bspwm'
I3 = 'i3'
OPENBOX = 'openbox'
SUPPORTED_APPS = [
    AWESOME,
    BSPWM,
    I3,
    OPENBOX
]

PARSERS = {
    AWESOME: "AwesomeConfigParser",
    BSPWM: "BspwmConfigParser",
    I3: "I3ConfigParser",
    OPENBOX: "OpenBoxConfigParser"
}

DMENU_HOTKEYS_DIR = os.path.dirname(__file__)
DMENU_HOTKEYS_CONFIG_PATH = os.path.join(DMENU_HOTKEYS_DIR, "config.cfg")
XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", os.path.join(
    os.environ.get("HOME"), ".config"))
USER_CONFIG_PATH = os.path.join(XDG_CONFIG_HOME, "dmenu_hotkeys", "config.cfg")
TEST_CONFIG_PATH = os.path.join(os.path.dirname((DMENU_HOTKEYS_DIR)),
                                "tests", "fixtures", "config.cfg")
