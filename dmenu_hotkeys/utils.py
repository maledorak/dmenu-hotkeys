from distutils.spawn import find_executable


def is_menu_installed(app):
    return find_executable(app)
