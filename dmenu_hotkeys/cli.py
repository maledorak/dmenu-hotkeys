import sys
from subprocess import Popen, run, PIPE

import click

from dmenu_hotkeys import constans as const
from dmenu_hotkeys.config import get_config
from dmenu_hotkeys.hotkeys import HotKeys
from dmenu_hotkeys.utils import is_installed


def install_validation(ctx, param, value):
    try:
        is_installed(value)
        return value
    except SystemError as error:
        support_map = {
            "menu": const.SUPPORTED_MENUS,
            "app": const.SUPPORTED_APPS
        }
        error = "{}\nInstall one of supported: {}".format(error, support_map[param.name])
        raise click.UsageError(error)


@click.command(help="Run hotkeys in menu.")
@click.argument("menu", callback=install_validation, required=True, type=click.Choice(const.SUPPORTED_MENUS))
@click.argument("app", callback=install_validation, required=True, type=click.Choice(const.SUPPORTED_APPS))
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
