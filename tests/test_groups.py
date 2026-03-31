"""Tests for group functionality."""

import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basic_interactive_menu.groups import OptionGroup, GroupRenderer
from basic_interactive_menu.interactive_menu import InteractiveMenu


class TestOptionGroup(unittest.TestCase):
    """Test OptionGroup dataclass."""

    def test_create_group(self):
        """Test creating a valid group."""
        group = OptionGroup(name="Test", options=["A", "B"])
        self.assertEqual(group.name, "Test")
        self.assertEqual(group.options, ["A", "B"])
        self.assertFalse(group.collapsed)

    def test_empty_group_raises_error(self):
        """Test that empty group raises ValueError."""
        with self.assertRaises(ValueError):
            OptionGroup(name="Empty", options=[])

    def test_collapsed_group(self):
        """Test creating a collapsed group."""
        group = OptionGroup(name="Test", options=["A"], collapsed=True)
        self.assertTrue(group.collapsed)

    def test_option_count(self):
        """Test option count method."""
        group = OptionGroup(name="Test", options=["A", "B", "C"])
        self.assertEqual(group.option_count(), 3)


class TestGroupRenderer(unittest.TestCase):
    """Test GroupRenderer functionality."""

    def test_add_group(self):
        """Test adding groups to renderer."""
        renderer = GroupRenderer()
        renderer.add_group("Group1", ["A", "B"])
        renderer.add_group("Group2", ["C", "D"])
        self.assertEqual(len(renderer.groups), 2)

    def test_get_all_options(self):
        """Test getting all visible options."""
        renderer = GroupRenderer()
        renderer.add_group("Group1", ["A", "B"])
        renderer.add_group("Group2", ["C", "D"])
        all_options = renderer.get_all_options()
        self.assertEqual(all_options, ["A", "B", "C", "D"])

    def test_get_all_options_with_collapsed(self):
        """Test that collapsed groups are excluded."""
        renderer = GroupRenderer()
        renderer.add_group("Group1", ["A", "B"])
        renderer.add_group("Group2", ["C", "D"], collapsed=True)
        all_options = renderer.get_all_options()
        self.assertEqual(all_options, ["A", "B"])

    def test_total_visible_options(self):
        """Test counting visible options."""
        renderer = GroupRenderer()
        renderer.add_group("Group1", ["A", "B", "C"])
        renderer.add_group("Group2", ["D"])
        self.assertEqual(renderer.total_visible_options(), 4)

    def test_render_header(self):
        """Test rendering group header."""
        group = OptionGroup(name="TestGroup", options=["A"])
        renderer = GroupRenderer()
        header = renderer.render_header(group)
        self.assertIn("TestGroup:", header)

    def test_render_option(self):
        """Test rendering option with global index."""
        renderer = GroupRenderer()
        rendered = renderer.render_option(5, "TestOption", "t")
        self.assertIn("5", rendered)
        self.assertIn("TestOption", rendered)

    def test_render_option_with_shortcut(self):
        """Test rendering option with shortcut."""
        renderer = GroupRenderer()
        rendered = renderer.render_option(5, "TestOption", "x")
        self.assertIn("5", rendered)
        self.assertIn("X", rendered.upper())

    def test_get_global_index(self):
        """Test global index calculation."""
        renderer = GroupRenderer()
        renderer.add_group("G1", ["A", "B"])
        renderer.add_group("G2", ["C"])
        self.assertEqual(renderer.get_global_index(0, 0), 0)
        self.assertEqual(renderer.get_global_index(0, 1), 1)
        self.assertEqual(renderer.get_global_index(1, 0), 2)


class TestGroupsInMenu(unittest.TestCase):
    """Test group functionality within InteractiveMenu."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['q'])
    def test_add_group_to_menu(self, mock_input):
        """Test adding groups to menu."""
        menu = InteractiveMenu()
        menu.add_group("Test", ["A", "B"])
        self.assertEqual(len(menu.groups[0]), 1)

    def test_empty_group_raises_error(self):
        """Test that empty group raises error."""
        menu = InteractiveMenu()
        with self.assertRaises(ValueError):
            menu.add_group("Empty", [])


if __name__ == '__main__':
    unittest.main()
