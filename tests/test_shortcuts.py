"""Tests for keyboard shortcuts feature."""

import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basic_interactive_menu.interactive_menu import InteractiveMenu


class TestShortcutBasics(unittest.TestCase):
    """Test basic shortcut functionality."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['a', 'y'])
    def test_shortcut_selection(self, mock_input):
        """Test selecting an option using its shortcut."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("Apple").ask().get_all_results()
        self.assertEqual(result, {"choice": "Apple"})

    @patch('builtins.input', side_effect=['b', 'y'])
    def test_shortcut_selection_second_option(self, mock_input):
        """Test selecting the second option using its shortcut."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("choice")
                  .add_option("Apple")
                  .add_option("Banana")
                  .ask()
                  .get_all_results())
        self.assertEqual(result, {"choice": "Banana"})

    @patch('builtins.input', side_effect=['c', 'y'])
    def test_shortcut_selection_third_option(self, mock_input):
        """Test selecting the third option using its shortcut."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("choice")
                  .add_option("Apple")
                  .add_option("Banana")
                  .add_option("Cherry")
                  .ask()
                  .get_all_results())
        self.assertEqual(result, {"choice": "Cherry"})


class TestExplicitShortcuts(unittest.TestCase):
    """Test explicit shortcut assignment."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['x', 'y'])
    def test_explicit_shortcut(self, mock_input):
        """Test using an explicitly assigned shortcut."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("choice")
                  .add_option("Exit", shortcut='x')
                  .ask()
                  .get_all_results())
        self.assertEqual(result, {"choice": "Exit"})

    @patch('builtins.input', side_effect=['a', 'y'])
    def test_explicit_shortcut_overrides_auto(self, mock_input):
        """Test that explicit shortcuts override auto-generated ones."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("choice")
                  .add_option("Apple", shortcut='a')
                  .add_option("Apricot")
                  .ask()
                  .get_all_results())
        self.assertEqual(result, {"choice": "Apple"})


class TestShortcutConflicts(unittest.TestCase):
    """Test shortcut conflict handling."""

    def test_duplicate_shortcut_raises_error(self):
        """Test that assigning a duplicate shortcut raises ValueError."""
        menu = InteractiveMenu()
        menu.add_option("First", shortcut='a')
        with self.assertRaises(ValueError) as context:
            menu.add_option("Another", shortcut='a')
        self.assertIn("conflicts", str(context.exception).lower())


class TestShortcutDisplay(unittest.TestCase):
    """Test shortcut display in menu output."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['q'])
    def test_shortcut_display_format(self, mock_input):
        """Test that shortcuts are displayed in the correct format."""
        menu = InteractiveMenu()
        menu.add_option("Apple").add_option("Banana").ask()
        output = self.held_output.getvalue()
        self.assertIn("[0/A]: Apple", output)
        self.assertIn("[1/B]: Banana", output)


class TestMultipleSelectionWithShortcuts(unittest.TestCase):
    """Test shortcuts in multiple selection mode."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['a', 'y'])
    def test_shortcut_in_multiple_mode(self, mock_input):
        """Test that shortcuts work in multiple selection mode."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("choices")
                  .add_option("Apple")
                  .add_option("Banana")
                  .allow_multiple()
                  .ask()
                  .get_all_results())
        self.assertEqual(result, {"choices": ["Apple"]})


class TestNestedMenusWithShortcuts(unittest.TestCase):
    """Test shortcuts across nested menu levels."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['a', 'x', 'y'])
    def test_shortcuts_in_nested_menus(self, mock_input):
        """Test that shortcuts work correctly in nested menus."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("level1")
                  .add_option("Apple")
                  .add_option("Banana")
                  .ask()
                  .set_key("level2")
                  .add_option("Small", shortcut='s')
                  .add_option("XLarge", shortcut='x')
                  .ask()
                  .get_all_results())
        self.assertEqual(result, {"level1": "Apple", "level2": "XLarge"})


class TestAutoGeneration(unittest.TestCase):
    """Test automatic shortcut generation."""

    def test_auto_generate_from_option_names(self):
        """Test that shortcuts are auto-generated from option names."""
        menu = InteractiveMenu()
        menu.add_option("Apple").add_option("Banana").add_option("Cherry")
        menu._auto_generate_shortcuts()
        self.assertEqual(menu.shortcuts[0]['a'], 0)
        self.assertEqual(menu.shortcuts[0]['b'], 1)
        self.assertEqual(menu.shortcuts[0]['c'], 2)

    def test_auto_generate_avoids_duplicates(self):
        """Test that auto-generation avoids duplicate characters."""
        menu = InteractiveMenu()
        menu.add_option("Apple").add_option("Apricot").add_option("Avocado")
        menu._auto_generate_shortcuts()
        # Only first should get 'a', others should get different letters
        self.assertEqual(menu.shortcuts[0]['a'], 0)
        # Second option should get 'p' (from Apricot) or 'r'
        # Third option should get remaining letters
        total_shortcuts = len(menu.shortcuts[0])
        self.assertEqual(total_shortcuts, 3)


class TestShortcutsWithSpecialCharacters(unittest.TestCase):
    """Test shortcuts with special characters in option names."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['o', 'y'])
    def test_shortcut_with_numbers_in_name(self, mock_input):
        """Test shortcut selection when option name contains numbers."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("Option 1").ask().get_all_results()
        self.assertEqual(result, {"choice": "Option 1"})

    @patch('builtins.input', side_effect=['q', 'y'])
    def test_shortcut_with_special_chars_in_name(self, mock_input):
        """Test shortcut selection when option name contains special characters."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("Quit (A)").ask().get_all_results()
        output = self.held_output.getvalue()
        # Should display with shortcut [0/Q]: Quit (A)
        self.assertIn("[0/Q]:", output)
        self.assertEqual(result, {"choice": "Quit (A)"})


class TestCaseInsensitiveShortcuts(unittest.TestCase):
    """Test that shortcuts are case-insensitive."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['A', 'y'])
    def test_uppercase_shortcut_input(self, mock_input):
        """Test that uppercase shortcut input works."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("Apple").ask().get_all_results()
        self.assertEqual(result, {"choice": "Apple"})


if __name__ == '__main__':
    unittest.main()
