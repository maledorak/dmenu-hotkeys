#!/usr/bin/env python

import unittest
from unittest import mock

from click.testing import CliRunner

from dmenu_hotkeys.cli import main
from dmenu_hotkeys.constans import DMENU, I3


class TestMainAndCheckArgumentsWhenEmpty(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_main_check_menu_argument_when_is_empty(self):
        result = self.runner.invoke(main)
        self.assertEqual(result.exit_code, 2)
        expected_output = 'Error: Missing argument "[dmenu|rofi]"'
        self.assertIn(expected_output, result.output)

    def test_main_check_app_argument_when_is_empty(self):
        result = self.runner.invoke(main, args=[DMENU])
        self.assertEqual(result.exit_code, 2)
        expected_output = 'Error: Missing argument "[i3|openbox]"'
        self.assertIn(expected_output, result.output)


class TestMainAndCheckArgumentsWhenInvalid(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_main_check_menu_argument_when_is_invalid(self):
        result = self.runner.invoke(main, args=[I3])
        self.assertEqual(result.exit_code, 2)
        expected_output = 'Error: Invalid value for "[dmenu|rofi]"'
        self.assertIn(expected_output, result.output)

    def test_main_check_app_argument_when_is_invalid(self):
        result = self.runner.invoke(main, args=[DMENU, DMENU])
        self.assertEqual(result.exit_code, 2)
        expected_output = 'Error: Invalid value for "[i3|openbox]"'
        self.assertIn(expected_output, result.output)


class TestMainAndCheckArgumentsWhenInstallNotValidated(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @mock.patch("dmenu_hotkeys.utils.find_executable")
    def test_main_check_menu_argument_when_fail_install_validation(self, find_executable_mock):
        find_executable_mock.side_effect = [False, False]  # menu, app
        result = self.runner.invoke(main, args=[DMENU, I3])
        self.assertEqual(result.exit_code, 2)
        expected_output_1 = 'Error: "dmenu" is not installed in your system or don\'t exists in PATH'
        expected_output_2 = 'Install one of supported: [\'dmenu\', \'rofi\']'
        self.assertIn(expected_output_1, result.output)
        self.assertIn(expected_output_2, result.output)

    @mock.patch("dmenu_hotkeys.utils.find_executable")
    def test_main_check_app_argument_when_fail_install_validation(self, find_executable_mock):
        find_executable_mock.side_effect = [True, False]  # menu, app
        result = self.runner.invoke(main, args=[DMENU, I3])
        self.assertEqual(result.exit_code, 2)
        expected_output_1 = 'Error: "i3" is not installed in your system or don\'t exists in PATH'
        expected_output_2 = 'Install one of supported: [\'i3\', \'openbox\']'
        self.assertIn(expected_output_1, result.output)
        self.assertIn(expected_output_2, result.output)
