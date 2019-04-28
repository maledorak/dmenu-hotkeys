import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from dmenu_hotkeys.utils import is_installed, _Singleton


class TestIsInstalled(unittest.TestCase):
    @mock.patch("dmenu_hotkeys.utils.find_executable",
                mock.Mock(return_value=True))
    def test_is_installed_when_return_true(self):
        self.assertTrue(is_installed(app='some-app'))

    @mock.patch("dmenu_hotkeys.utils.find_executable",
                mock.Mock(return_value=False))
    def test_is_installed_when_return_false(self):
        expected_msg = "\"some-app\" is not installed in your system or don't exists in PATH"
        with self.assertRaises(SystemError) as cm:
            is_installed(app='some-app')
        self.assertEqual(str(cm.exception), expected_msg)


class TestSingleton(unittest.TestCase):
    def setUp(self):
        class SomeClass(_Singleton('SingletonMeta', (object,), {})):
            pass

        self.SomeClass = SomeClass

    def tearDown(self):
        self.SomeClass._clean_singleton()

    def test_singleton_objects_should_be_exact(self):
        some1 = self.SomeClass()
        some2 = self.SomeClass()
        self.assertEqual(some1, some2)

    def test_singleton_objects_should_not_be_exact_after_cleaning_between(self):
        some1 = self.SomeClass()
        some2 = self.SomeClass()
        self.assertEqual(some1, some2)
        self.SomeClass._clean_singleton()
        some3 = self.SomeClass()
        self.assertNotEqual(some1, some3)
