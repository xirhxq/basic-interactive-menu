"""Integration tests for InteractiveMenu.

This module contains integration tests that verify the complete functionality
of the menu system, including end-to-end workflows.
"""

import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basic_interactive_menu.interactive_menu import InteractiveMenu


class TestBasicWorkflows(unittest.TestCase):
    """Test basic menu workflows."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_simple_single_selection_workflow(self, mock_input):
        """Test a simple single selection menu workflow."""
        menu = InteractiveMenu()
        result = (menu
                  .set_title("Choose an option")
                  .set_key("choice")
                  .add_option("Option A")
                  .add_option("Option B")
                  .add_option("Option C")
                  .ask()
                  .get_all_results())

        self.assertEqual(result, {"choice": "Option A"})

    @patch('builtins.input', side_effect=['1', 'y'])
    def test_select_middle_option(self, mock_input):
        """Test selecting an option in the middle of the list."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("choice")
                  .add_options(["A", "B", "C", "D", "E"])
                  .ask()
                  .get_all_results())

        self.assertEqual(result, {"choice": "B"})

    @patch('builtins.input', side_effect=['4', 'y'])
    def test_select_last_option(self, mock_input):
        """Test selecting the last option."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("choice")
                  .add_options(["A", "B", "C", "D", "E"])
                  .ask()
                  .get_all_results())

        self.assertEqual(result, {"choice": "E"})


class TestMultipleSelectionWorkflows(unittest.TestCase):
    """Test multiple selection workflows."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['0 1 2', 'y'])
    def test_select_all_options(self, mock_input):
        """Test selecting all available options."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("choices")
                  .add_options(["A", "B", "C"])
                  .allow_multiple()
                  .ask()
                  .get_all_results())

        self.assertEqual(result, {"choices": ["A", "B", "C"]})

    @patch('builtins.input', side_effect=['0,2', 'y'])
    def test_select_with_commas(self, mock_input):
        """Test selecting options using comma-separated indices."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("choices")
                  .add_options(["A", "B", "C", "D"])
                  .allow_multiple()
                  .ask()
                  .get_all_results())

        self.assertEqual(result, {"choices": ["A", "C"]})

    @patch('builtins.input', side_effect=['0 1,2 3', 'y'])
    def test_select_mixed_separators(self, mock_input):
        """Test selecting options using mixed separators."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("choices")
                  .add_options(["A", "B", "C", "D"])
                  .allow_multiple()
                  .ask()
                  .get_all_results())

        self.assertEqual(result, {"choices": ["A", "B", "C", "D"]})


class TestNestedMenuWorkflows(unittest.TestCase):
    """Test nested menu workflows."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['0', '1', 'y'])
    def test_two_level_nesting(self, mock_input):
        """Test a two-level nested menu."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("level1")
                  .set_title("Level 1")
                  .add_option("A1")
                  .add_option("A2")
                  .ask()
                  .set_key("level2")
                  .set_title("Level 2")
                  .add_option("B1")
                  .add_option("B2")
                  .ask()
                  .get_all_results())

        self.assertEqual(result, {"level1": "A1", "level2": "B2"})

    @patch('builtins.input', side_effect=['0', '0', '0', 'y'])
    def test_three_level_nesting(self, mock_input):
        """Test a three-level nested menu."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("level1").add_option("A1").add_option("A2").ask()
                  .set_key("level2").add_option("B1").add_option("B2").ask()
                  .set_key("level3").add_option("C1").add_option("C2").ask()
                  .get_all_results())

        self.assertEqual(result, {"level1": "A1", "level2": "B1", "level3": "C1"})

    @patch('builtins.input', side_effect=['0', 'r', '1', '0', 'y'])
    def test_return_to_parent_and_continue(self, mock_input):
        """Test returning to parent menu and making a different selection."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("level1").add_option("A1").add_option("A2").ask()
                  .set_key("level2").add_option("B1").add_option("B2").ask()
                  .get_all_results())

        self.assertEqual(result, {"level1": "A2", "level2": "B1"})


class TestConfirmationWorkflows(unittest.TestCase):
    """Test confirmation and cancellation workflows."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_confirm_selection(self, mock_input):
        """Test confirming a selection returns the result."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("A").ask().get_all_results()
        self.assertEqual(result, {"choice": "A"})

    @patch('builtins.input', side_effect=['0', 'n'])
    def test_cancel_selection(self, mock_input):
        """Test cancelling a selection returns None."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("A").ask().get_all_results()
        self.assertIsNone(result)

    @patch('builtins.input', side_effect=['0', 'r', '1', 'y'])
    def test_restart_workflow(self, mock_input):
        """Test restarting the menu workflow.

        When restart is chosen, get_all_results() returns the menu object
        itself, allowing the workflow to be restarted.
        """
        menu = InteractiveMenu()
        result = (menu
                  .set_key("choice")
                  .add_option("A")
                  .add_option("B")
                  .ask()
                  .get_all_results())

        # After restart, get_all_results returns self (the menu object)
        self.assertIsInstance(result, InteractiveMenu)

    @patch('builtins.input', side_effect=['0', 'n', '1', 'y'])
    def test_cancel_and_restart(self, mock_input):
        """Test cancelling and then making a new selection."""
        menu = InteractiveMenu()
        first_result = menu.set_key("choice").add_option("A").add_option("B").ask().get_all_results()

        # Cancelling returns None
        self.assertIsNone(first_result)

        # Create a new menu and make a different selection
        menu2 = InteractiveMenu()
        second_result = menu2.set_key("choice").add_option("A").add_option("B").ask().get_all_results()
        self.assertEqual(second_result, {"choice": "B"})


class TestQuitWorkflows(unittest.TestCase):
    """Test quit scenarios."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['q'])
    def test_quit_at_first_menu(self, mock_input):
        """Test quitting at the first menu."""
        menu = InteractiveMenu()
        result = menu.add_option("A").ask().get_all_results()
        self.assertIsNone(result)

    @patch('builtins.input', side_effect=['0', 'q'])
    def test_quit_at_second_menu(self, mock_input):
        """Test quitting at the second menu level."""
        menu = InteractiveMenu()
        result = (menu
                  .set_key("level1").add_option("A").ask()
                  .set_key("level2").add_option("B").ask()
                  .get_all_results())
        self.assertIsNone(result)


class TestMethodChaining(unittest.TestCase):
    """Test that method chaining works correctly."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['0', 'y'])
    def test_full_chain(self, mock_input):
        """Test a complete method chain."""
        menu = InteractiveMenu()
        result = (menu
                  .set_title("Test Menu")
                  .set_key("test_key")
                  .add_option("First")
                  .add_options(["Second", "Third"])
                  .ask()
                  .get_all_results())

        self.assertIsInstance(result, dict)
        self.assertIn("test_key", result)
        self.assertEqual(result["test_key"], "First")


class TestComplexScenarios(unittest.TestCase):
    """Test complex real-world scenarios."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['0', '0', '0 1 2', 'y'])
    def test_configuration_builder_workflow(self, mock_input):
        """Test a configuration builder workflow with multiple levels."""
        menu = InteractiveMenu()

        # Level 1: Choose environment
        result = (menu
                  .set_title("Select Environment")
                  .set_key("environment")
                  .add_options(["Development", "Staging", "Production"])
                  .ask()

                  # Level 2: Choose region
                  .set_title("Select Region")
                  .set_key("region")
                  .add_options(["US-East", "US-West", "EU-West", "AP-Southeast"])
                  .ask()

                  # Level 3: Choose features (multiple)
                  .set_title("Select Features")
                  .set_key("features")
                  .allow_multiple()
                  .add_options(["Feature A", "Feature B", "Feature C"])
                  .ask()
                  .get_all_results())

        self.assertEqual(result["environment"], "Development")
        self.assertEqual(result["region"], "US-East")
        self.assertEqual(result["features"], ["Feature A", "Feature B", "Feature C"])

    @patch('builtins.input', side_effect=['2', '0', '1', 'y'])
    def test_ordering_system_workflow(self, mock_input):
        """Test an ordering system workflow."""
        menu = InteractiveMenu()

        result = (menu
                  .set_title("Select Product Category")
                  .set_key("category")
                  .add_options(["Electronics", "Clothing", "Books"])
                  .ask()

                  .set_title("Select Price Range")
                  .set_key("price_range")
                  .add_options(["Under $25", "$25-$50", "$50-$100", "Over $100"])
                  .ask()

                  .set_title("Select Shipping")
                  .set_key("shipping")
                  .add_options(["Standard", "Express", "Overnight"])
                  .ask()
                  .get_all_results())

        self.assertEqual(result["category"], "Books")
        self.assertEqual(result["price_range"], "Under $25")
        self.assertEqual(result["shipping"], "Express")


class TestErrorHandling(unittest.TestCase):
    """Test error handling in various scenarios."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['invalid', '0', 'y'])
    def test_invalid_then_valid_input(self, mock_input):
        """Test that invalid input is handled and user can try again."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("A").ask().get_all_results()
        output = self.held_output.getvalue()

        self.assertIn("Invalid input", output)
        self.assertEqual(result, {"choice": "A"})

    @patch('builtins.input', side_effect=['999', '0', 'y'])
    def test_out_of_range_then_valid_input(self, mock_input):
        """Test that out of range input is handled."""
        menu = InteractiveMenu()
        result = menu.set_key("choice").add_option("A").ask().get_all_results()
        output = self.held_output.getvalue()

        self.assertIn("Invalid input", output)
        self.assertEqual(result, {"choice": "A"})


if __name__ == '__main__':
    unittest.main()
