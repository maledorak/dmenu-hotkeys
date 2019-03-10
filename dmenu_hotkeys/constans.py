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
