#!/usr/bin/env python

import unittest
from unittest import mock

from dmenu_hotkeys.constans import DMENU, ROFI
from dmenu_hotkeys.utils import is_menu_installed


@mock.patch("dmenu_hotkeys.utils.find_executable", mock.Mock(return_value=True))
class IsMenuInstalledWhenReturnTrue(unittest.TestCase):
    def test_is_menu_installed_with_dmenu(self):
        self.assertTrue(is_menu_installed(app=DMENU))

    def test_is_menu_installed_with_rofi(self):
        self.assertTrue(is_menu_installed(app=ROFI))


@mock.patch("dmenu_hotkeys.utils.find_executable", mock.Mock(return_value=False))
class IsMenuInstalledWhenReturnFalse(unittest.TestCase):
    def test_is_menu_installed_with_dmenu(self):
        self.assertFalse(is_menu_installed(app=DMENU))

    def test_is_menu_installed_with_rofi(self):
        self.assertFalse(is_menu_installed(app=ROFI))
