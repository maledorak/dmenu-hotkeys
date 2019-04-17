from distutils.spawn import find_executable


def is_installed(app):
    if not find_executable(app):
        raise SystemError("\"{}\" is not installed in your system or don't exists in PATH".format(app))
    return True
