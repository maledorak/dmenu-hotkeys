import filecmp
import os
import shutil
import unittest

from tests.utils import TempDirTestCase

try:
    from unittest import mock
except ImportError:
    import mock

from click.testing import CliRunner

from dmenu_hotkeys.cli import run, copy_config
from dmenu_hotkeys.constans import DMENU, I3, SRC_CONF_PATH


@mock.patch("dmenu_hotkeys.utils.find_executable", mock.Mock(return_value=True))
class TestRunAndCheckOptionWhenEmpty(unittest.TestCase):
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
class TestRunAndCheckOptionWhenInvalid(unittest.TestCase):
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


@mock.patch("dmenu_hotkeys.utils.find_executable")
class TestRunAndCheckArgumentsWhenInstallNotValidated(unittest.TestCase):
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
        self.assertTrue(filecmp.cmp(SRC_CONF_PATH, self.dest))

    def test_copy_config_when_there_is_no_destination_file(self):
        result = self.runner.invoke(copy_config, args=["--dest", self.dest])
        expected_output_1 = 'Create config directory in {}'.format(self.TEMP_DIR)
        expected_output_2 = 'Creating config in {}'.format(self.dest)
        self.assertNotIn(expected_output_1, result.output)
        self.assertIn(expected_output_2, result.output)
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(filecmp.cmp(SRC_CONF_PATH, self.dest))

    def test_copy_config_when_there_is_destination_file(self):
        shutil.copy(SRC_CONF_PATH, self.dest)
        result = self.runner.invoke(copy_config, args=["--dest", self.dest])
        self.assertEqual(result.exit_code, 2)
        expected_output = 'Config already exists in {}'.format(self.dest)
        self.assertIn(expected_output, result.output)
