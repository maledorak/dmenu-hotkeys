import os
import shutil
import sys
from subprocess import Popen, PIPE, call

import click

from dmenu_hotkeys.config import get_config
from dmenu_hotkeys.constans import (
    SUPPORTED_MENUS, SUPPORTED_APPS, SRC_CONF_PATH, USER_CONF_PATH
)
from dmenu_hotkeys.hotkeys import HotKeys
from dmenu_hotkeys.utils import is_installed

if sys.version_info < (3, 5):
    # noinspection PyUnresolvedReferences
    # python <= 3.4 backport (mkdir exist_ok param is from py35)
    from pathlib2 import Path
else:
    from pathlib import Path


@click.group()
def main():
    pass


def install_validation(ctx, param, value):
    try:
        is_installed(value)
        return value
    except SystemError as error:
        support_map = {
            "menu": SUPPORTED_MENUS,
            "app": SUPPORTED_APPS
        }
        error = "{}\nInstall one of supported: {}".format(
            error, support_map[param.name])
        raise click.UsageError(error)


@click.command(help="Run dmenu_hotkeys.")
@click.option("-m", "--menu", callback=install_validation,
              required=True, type=click.Choice(SUPPORTED_MENUS))
@click.option("-a", "--app", callback=install_validation,
              required=True, type=click.Choice(SUPPORTED_APPS))
def run(menu, app):
    config = get_config()
    hot_keys = HotKeys(app)

    # subprocess piping was created based on:
    # https://stackoverflow.com/a/4846923
    echo = Popen(["echo", hot_keys.output], stdout=PIPE)
    menu_command = config.get("MENU_COMMAND", menu).split()
    call(menu_command, stdin=echo.stdout)
    echo.stdout.close()
    return 0


@click.command(help="Copy dmenu_hotkeys config to ~/.config")
@click.option("-d", "--dest", required=False, type=click.Path())
def copy_config(dest=None):
    src = SRC_CONF_PATH
    dest = dest or USER_CONF_PATH
    dest_dir = os.path.dirname(dest)
    if os.path.exists(dest):
        raise click.UsageError("Config already exists in {}".format(dest))
    else:
        if not os.path.exists(dest_dir):
            click.echo("Create config directory in {}".format(dest_dir))
            Path(dest_dir).mkdir(parents=True, exist_ok=True)
        click.echo("Creating config in {}".format(dest))
        shutil.copy(src, dest)


main.add_command(copy_config)
main.add_command(run)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
