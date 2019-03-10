#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dmenu_hotkeys` package."""

import unittest

from click.testing import CliRunner

from dmenu_hotkeys import __main__


class TestDmenuHotkeysMain(unittest.TestCase):
    """Tests for `dmenu_hotkeys` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    # def test_command_line_interface(self):
    #     """Test the CLI."""
    #     runner = CliRunner()
    #     result = runner.invoke(__main__.main)
    #     assert result.exit_code == 0
    #     assert 'dmenu_hotkeys.__main__.main' in result.output
    #     help_result = runner.invoke(__main__.main, ['--help'])
    #     assert help_result.exit_code == 0
    #     assert '--help  Show this message and exit.' in help_result.output
