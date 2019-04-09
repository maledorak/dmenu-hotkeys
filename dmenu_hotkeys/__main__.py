# -*- coding: utf-8 -*-

import sys

import click
from subprocess import Popen, run, PIPE

from dmenu_hotkeys import constans as const
from dmenu_hotkeys.config import Config
from dmenu_hotkeys.hotkeys import HotKeys
from dmenu_hotkeys.utils import is_menu_installed


@click.command()
@click.option("--menu", default=const.DMENU, required=True, type=click.Choice(const.SUPPORTED_MENUS))
@click.option("--app", required=True, type=click.Choice(const.SUPPORTED_APPS))
@click.option("--dots", default=True, type=click.BOOL)
def main(menu, app, dots):
    is_menu_installed(app) #todo rzuć throwem i ustaw w teście następnie zacommituj
    cfg = Config(dots=dots)
    hot_keys = HotKeys(app=app, cfg=cfg.config)

    # subprocess piping was created based on: https://stackoverflow.com/a/4846923
    echo = Popen(["echo", hot_keys.output], stdout=PIPE)
    menu_command = cfg.config.get("MENU_COMMAND", menu).split()
    run(menu_command, stdin=echo.stdout)
    echo.stdout.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
