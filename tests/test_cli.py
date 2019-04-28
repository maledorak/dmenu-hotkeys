import filecmp
import os
import shutil
import sys
import unittest

from click.testing import CliRunner

from dmenu_hotkeys.cli import run, copy_config
from dmenu_hotkeys.constants import (
    DMENU, I3, DMENU_HOTKEYS_CONFIG_PATH
)
from tests.utils import TempDirTestCase

try:
    from unittest import mock
except ImportError:
    import mock

if sys.version_info < (3, 5):
    # noinspection PyUnresolvedReferences
    # python <= 3.4 backport (mkdir exist_ok param is from py35)
    from pathlib2 import Path
else:
    from pathlib import Path


@mock.patch("dmenu_hotkeys.utils.find_executable", mock.Mock(return_value=True))
class TestRunAndCheckRequiredOptionWhenEmpty(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_run_command_and_check_menu_argument_when_is_empty(self):
        result = self.runner.invoke(run)
        self.assertEqual(result.exit_code, 2)
        expected_output = 'Error: Missing option "-m" / "--menu"'
        self.assertIn(expected_output, result.output)

    def test_run_command_and_check_app_argument_when_is_empty(self):
        result = self.runner.invoke(run, args=["--menu", DMENU])
        self.assertEqual(result.exit_code, 2)
        expected_output = 'Error: Missing option "-a" / "--app"'
        self.assertIn(expected_output, result.output)


@mock.patch("dmenu_hotkeys.utils.find_executable", mock.Mock(return_value=True))
class TestRunAndCheckRequiredOptionWhenInvalid(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_run_command_and_check_menu_argument_when_is_invalid(self):
        result = self.runner.invoke(run, args=["--menu", I3, "--app", I3])
        self.assertEqual(result.exit_code, 2)
        expected_output = 'Error: Invalid value for "-m" / "--menu"'
        self.assertIn(expected_output, result.output)

    def test_run_command_and_check_app_argument_when_is_invalid(self):
        result = self.runner.invoke(run, args=["--menu", DMENU, "--app", DMENU])
        self.assertEqual(result.exit_code, 2)
        expected_output = 'Error: Invalid value for "-a" / "--app"'
        self.assertIn(expected_output, result.output)


@mock.patch("dmenu_hotkeys.utils.find_executable", mock.Mock(return_value=True))
class TestRunAndCheckConfigPathOption(TempDirTestCase):
    def setUp(self):
        super(TestRunAndCheckConfigPathOption, self).setUp()
        self.runner = CliRunner()

    def test_run_command_and_check_config_option_when_dir(self):
        path = self.TEMP_DIR
        result = self.runner.invoke(
            run, args=["--menu", DMENU, "--app", I3, '--config-path', path])
        self.assertEqual(result.exit_code, 2)
        expected_output_1 = 'Error: Invalid value for "-cp" / "--config-path"'
        expected_output_2 = 'is a directory.'
        self.assertIn(expected_output_1, result.output)
        self.assertIn(expected_output_2, result.output)

    def test_run_command_and_check_config_option_when_file_exists(self):
        path = os.path.join(self.TEMP_DIR, 'some_config.cfg')
        Path(path).touch()
        result = self.runner.invoke(
            run, args=["--menu", DMENU, "--app", I3, '--config-path', path])
        self.assertEqual(result.exit_code, 0)

    def test_run_command_and_check_config_option_when_file_not_exists(self):
        path = os.path.join(self.TEMP_DIR, 'some_config.cfg')
        result = self.runner.invoke(
            run, args=["--menu", DMENU, "--app", I3, '--config-path', path])
        self.assertEqual(result.exit_code, 2)
        expected_output_1 = 'Error: Invalid value for "-cp" / "--config-path"'
        expected_output_2 = 'does not exist'
        self.assertIn(expected_output_1, result.output)
        self.assertIn(expected_output_2, result.output)


@mock.patch("dmenu_hotkeys.utils.find_executable")
class TestRunAndCheckRequiredOptionWhenInstallNotValidated(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_run_command_and_check_menu_argument_when_fail_install_validation(
        self, find_executable_mock):
        find_executable_mock.side_effect = [False, False]  # menu, app
        result = self.runner.invoke(run, args=["--menu", DMENU, "-app", I3])
        self.assertEqual(result.exit_code, 2)
        expected_output_1 = 'Error: "dmenu" is not installed in your system or don\'t exists in PATH'
        expected_output_2 = 'Install one of supported: [\'dmenu\', \'rofi\']'
        self.assertIn(expected_output_1, result.output)
        self.assertIn(expected_output_2, result.output)

    def test_run_command_and_check_app_argument_when_fail_install_validation(
        self, find_executable_mock):
        find_executable_mock.side_effect = [True, False]  # menu, app
        result = self.runner.invoke(run, args=["--menu", DMENU, "--app", I3])
        self.assertEqual(result.exit_code, 2)
        expected_output_1 = 'Error: "i3" is not installed in your system or don\'t exists in PATH'
        expected_output_2 = 'Install one of supported: [\'i3\', \'openbox\']'
        self.assertIn(expected_output_1, result.output)
        self.assertIn(expected_output_2, result.output)


class TestCopyConfig(TempDirTestCase):
    def setUp(self):
        super(TestCopyConfig, self).setUp()
        self.runner = CliRunner()
        self.dest = os.path.join(self.TEMP_DIR, "config.cfg")

    def test_copy_config_when_there_is_no_destination_dir_and_file(self):
        shutil.rmtree(self.TEMP_DIR, ignore_errors=True)
        result = self.runner.invoke(copy_config, args=["--dest", self.dest])
        expected_output_1 = 'Create config directory in {}'.format(
            self.TEMP_DIR)
        expected_output_2 = 'Creating config in {}'.format(self.dest)
        self.assertIn(expected_output_1, result.output)
        self.assertIn(expected_output_2, result.output)
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(filecmp.cmp(DMENU_HOTKEYS_CONFIG_PATH, self.dest))

    def test_copy_config_when_there_is_no_destination_file(self):
        result = self.runner.invoke(copy_config, args=["--dest", self.dest])
        expected_output_1 = 'Create config directory in {}'.format(
            self.TEMP_DIR)
        expected_output_2 = 'Creating config in {}'.format(self.dest)
        self.assertNotIn(expected_output_1, result.output)
        self.assertIn(expected_output_2, result.output)
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(filecmp.cmp(DMENU_HOTKEYS_CONFIG_PATH, self.dest))

    def test_copy_config_when_there_is_destination_file(self):
        shutil.copy(DMENU_HOTKEYS_CONFIG_PATH, self.dest)
        result = self.runner.invoke(copy_config, args=["--dest", self.dest])
        self.assertEqual(result.exit_code, 2)
        expected_output = 'Config already exists in {}'.format(self.dest)
        self.assertIn(expected_output, result.output)
