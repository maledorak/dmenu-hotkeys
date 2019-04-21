import sys
from subprocess import Popen, PIPE, call

import click

from dmenu_hotkeys import constans as const
from dmenu_hotkeys.config import get_config
from dmenu_hotkeys.hotkeys import HotKeys
from dmenu_hotkeys.utils import is_installed


@click.group()
def main():
    pass


def install_validation(ctx, param, value):
    try:
        is_installed(value)
        return value
    except SystemError as error:
        support_map = {
            "menu": const.SUPPORTED_MENUS,
            "app": const.SUPPORTED_APPS
        }
        error = "{}\nInstall one of supported: {}".format(
            error, support_map[param.name])
        raise click.UsageError(error)


@click.command(help="Run dmenu_hotkeys.")
@click.option("-m", "--menu", callback=install_validation,
              required=True, type=click.Choice(const.SUPPORTED_MENUS))
@click.option("-a", "--app", callback=install_validation,
              required=True, type=click.Choice(const.SUPPORTED_APPS))
def run(menu, app):
    cfg = get_config()
    hot_keys = HotKeys(app)

    # subprocess piping was created based on:
    # https://stackoverflow.com/a/4846923
    echo = Popen(["echo", hot_keys.output], stdout=PIPE)
    menu_command = cfg.get("MENU_COMMAND", menu).split()
    call(menu_command, stdin=echo.stdout)
    echo.stdout.close()
    return 0


main.add_command(run)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
