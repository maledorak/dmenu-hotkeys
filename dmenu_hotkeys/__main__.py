# -*- coding: utf-8 -*-

import sys

import click
from subprocess import Popen, run, PIPE

from dmenu_hotkeys import constans as const
from dmenu_hotkeys.config import get_config
from dmenu_hotkeys.hotkeys import HotKeys


@click.command()
@click.option("--menu", default=const.DMENU, required=True, type=click.Choice([*const.SUPPORTED_MENUS]))
@click.option("--app", required=True, type=click.Choice([*const.SUPPORTED_APPS]))
def main(menu, app):
    cfg = get_config()
    hot_keys = HotKeys(app)

    # subprocess piping was created based on: https://stackoverflow.com/a/4846923
    echo = Popen(["echo", hot_keys.output], stdout=PIPE)
    menu_command = cfg.get("MENU_COMMAND", menu).split()
    run(menu_command, stdin=echo.stdout)
    echo.stdout.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
