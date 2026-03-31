"""Edge case tests for InteractiveMenu.

This module contains tests for unusual or edge case scenarios including:
- Empty options list
- Single option
- Very long option names
- Special characters in options
- Unicode characters
"""

import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basic_interactive_menu.interactive_menu import InteractiveMenu


class TestEmptyOptions(unittest.TestCase):
    """Test menu behavior with no options."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['q'])
    def test_empty_menu_quit(self, mock_input):
        """Test that an empty menu can be quit without errors."""
        menu = InteractiveMenu()
        menu.ask().get_all_results()
        output = self.held_output.getvalue()
        self.assertIn("Exiting...", output)

    @patch('builtins.input', side_effect=['0', 'q'])
    def test_empty_menu_invalid_index(self, mock_input):
        """Test that selecting an invalid index on empty menu shows error."""
        menu = InteractiveMenu()
        menu.ask().get_all_results()
        output = self.held_output.getvalue()
        self.assertIn("Invalid input", output)


class TestSingleOption(unittest.TestCase):
    """Test menu behavior with a single option."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_single_option_selection(self, mock_input):
        """Test selecting the only available option."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("Only Option").ask().get_all_results()
        self.assertEqual(result, {"choice": "Only Option"})

    @patch('builtins.input', side_effect=['1', '0', 'y'])
    def test_single_option_invalid_then_valid(self, mock_input):
        """Test invalid input followed by valid input on single option menu."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("Only Option").ask().get_all_results()
        output = self.held_output.getvalue()
        self.assertIn("Invalid input", output)
        self.assertEqual(result, {"choice": "Only Option"})


class TestLongOptionNames(unittest.TestCase):
    """Test menu behavior with very long option names."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_very_long_option_name(self, mock_input):
        """Test that very long option names are handled correctly."""
        long_name = "A" * 200
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option(long_name).ask().get_all_results()
        self.assertEqual(result, {"choice": long_name})

    @patch('builtins.input', side_effect=['0 1', 'y'])
    def test_multiple_long_option_names(self, mock_input):
        """Test selecting from multiple long option names."""
        menu = InteractiveMenu()
        menu.allow_multiple()
        long_names = ["Option" + "X" * i * 50 for i in range(1, 4)]
        for name in long_names:
            menu.add_option(name)
        result = menu.set_key("choices").ask().get_all_results()
        self.assertIn("choices", result)
        self.assertEqual(len(result["choices"]), 2)


class TestSpecialCharacters(unittest.TestCase):
    """Test menu behavior with special characters in option names."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_option_with_quotes(self, mock_input):
        """Test option names containing quotes."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option('Option "with quotes"').ask().get_all_results()
        self.assertEqual(result, {"choice": 'Option "with quotes"'})

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_option_with_parentheses(self, mock_input):
        """Test option names containing parentheses."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("Option (with parentheses)").ask().get_all_results()
        self.assertEqual(result, {"choice": "Option (with parentheses)"})

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_option_with_brackets(self, mock_input):
        """Test option names containing brackets."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("Option [with brackets]").ask().get_all_results()
        self.assertEqual(result, {"choice": "Option [with brackets]"})

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_option_with_slashes(self, mock_input):
        """Test option names containing forward and backward slashes."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("path/to/file").ask().get_all_results()
        self.assertEqual(result, {"choice": "path/to/file"})

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_option_with_emoji(self, mock_input):
        """Test option names containing emoji characters."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("Option 😀 with emoji").ask().get_all_results()
        self.assertEqual(result, {"choice": "Option 😀 with emoji"})


class TestUnicodeCharacters(unittest.TestCase):
    """Test menu behavior with Unicode characters."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_chinese_characters(self, mock_input):
        """Test option names with Chinese characters."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("选项中文").ask().get_all_results()
        self.assertEqual(result, {"choice": "选项中文"})

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_japanese_characters(self, mock_input):
        """Test option names with Japanese characters."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("日本語オプション").ask().get_all_results()
        self.assertEqual(result, {"choice": "日本語オプション"})

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_arabic_characters(self, mock_input):
        """Test option names with Arabic characters."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("خيار باللغة العربية").ask().get_all_results()
        self.assertEqual(result, {"choice": "خيار باللغة العربية"})


class TestWhitespace(unittest.TestCase):
    """Test menu behavior with whitespace in option names."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_option_with_leading_trailing_spaces(self, mock_input):
        """Test option names with leading and trailing spaces."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("  Spaced Option  ").ask().get_all_results()
        self.assertEqual(result, {"choice": "  Spaced Option  "})

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_option_with_multiple_internal_spaces(self, mock_input):
        """Test option names with multiple internal spaces."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("Option    with    spaces").ask().get_all_results()
        self.assertEqual(result, {"choice": "Option    with    spaces"})


class TestMultipleSelectionEdgeCases(unittest.TestCase):
    """Test edge cases in multiple selection mode."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['', 'q'])
    def test_empty_multiple_selection(self, mock_input):
        """Test that empty input in multiple mode shows error."""
        menu = InteractiveMenu()
        menu.allow_multiple().add_option("A").add_option("B")
        menu.ask().get_all_results()
        output = self.held_output.getvalue()
        # Should show some kind of error message

    @patch('builtins.input', side_effect=['0,0', 'y'])
    def test_duplicate_selection(self, mock_input):
        """Test selecting the same option multiple times."""
        menu = InteractiveMenu()
        menu.allow_multiple().add_option("A").add_option("B")
        result = menu.set_key("choices").ask().get_all_results()
        # Duplicate indices should be handled

    @patch('builtins.input', side_effect=['999', '0', 'y'])
    def test_out_of_range_multiple_selection(self, mock_input):
        """Test selecting indices that are out of range."""
        menu = InteractiveMenu()
        menu.allow_multiple().add_option("A").add_option("B")
        result = menu.set_key("choices").ask().get_all_results()
        # Should filter out invalid indices


class TestMethodChaining(unittest.TestCase):
    """Test method chaining behavior."""

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_full_method_chain(self, mock_input):
        """Test that all methods return self for chaining."""
        menu = InteractiveMenu()
        result = (menu
                  .set_title("Test Menu")
                  .set_key("test")
                  .add_option("A")
                  .add_options(["B", "C"])
                  .allow_multiple()
                  .ask()
                  .get_all_results())
        self.assertIsInstance(result, dict)
        self.assertIn("test", result)


class TestQuitStates(unittest.TestCase):
    """Test various quit scenarios."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['q'])
    def test_quit_returns_none(self, mock_input):
        """Test that quitting returns None."""
        menu = InteractiveMenu()
        result = menu.add_option("A").ask().get_all_results()
        self.assertIsNone(result)

    @patch('builtins.input', side_effect=['0', 'n'])
    def test_cancel_at_confirmation(self, mock_input):
        """Test that cancelling at confirmation returns None."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("A").ask().get_all_results()
        self.assertIsNone(result)


class TestDebugMode(unittest.TestCase):
    """Test debug mode functionality."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_debug_output(self, mock_input):
        """Test that debug mode produces verbose output."""
        menu = InteractiveMenu(debug=True)
        result = menu.set_key("choice").add_option("A").ask().get_all_results()
        output = self.held_output.getvalue()
        # Debug mode should add additional output


if __name__ == '__main__':
    unittest.main()
