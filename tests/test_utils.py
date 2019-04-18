import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from dmenu_hotkeys.utils import is_installed


class TestIsInstalled(unittest.TestCase):
    @mock.patch("dmenu_hotkeys.utils.find_executable", mock.Mock(return_value=True))
    def test_is_installed_when_return_true(self):
        self.assertTrue(is_installed(app='some-app'))

    @mock.patch("dmenu_hotkeys.utils.find_executable", mock.Mock(return_value=False))
    def test_is_installed_when_return_false(self):
        expected_msg = "\"some-app\" is not installed in your system or don't exists in PATH"
        with self.assertRaises(SystemError) as cm:
            is_installed(app='some-app')
        self.assertEqual(str(cm.exception), expected_msg)
