import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from examples.nested_with_confirmation import main

class TestNestedWithConfirmationMenu(unittest.TestCase):
    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('basic_interactive_menu.interactive_menu.input', side_effect=['0', 'y', '1', 'y', '2', 'y', '1 3', 'y', 'y'])
    def test_full_order_workflow(self, mock_input):
        main()
        output = self.held_output.getvalue()
        self.assertIn("Processing order for 3 x Pepperoni", output)
        self.assertIn("With options:", output)
        self.assertIn("  - Mushrooms", output)  # Index 1
        self.assertIn("  - Peppers", output)    # Index 3

    @patch('basic_interactive_menu.interactive_menu.input', side_effect=['0', 'y', '1', 'y', '2', 'y', '1 3', 'y', 'n'])
    def test_order_confirmation_no(self, mock_input):
        result = main()
        output = self.held_output.getvalue()
        # Since user said 'n', the process should exit
        self.assertIsNone(result)

    @patch('basic_interactive_menu.interactive_menu.input', side_effect=['0', 'y', '1', 'y', '2', 'y', '1 3', 'y', 'r'])
    def test_order_restart_at_confirmation(self, mock_input):
        result = main()
        # When user chooses to restart, main() should return None (default return value of a function that doesn't explicitly return)
        self.assertIsNone(result)
        
    @patch('basic_interactive_menu.interactive_menu.input', side_effect=['0', 'y', '1', 'r', '1', 'y', '2', 'y', '0', 'y', '0', 'y', 'y'])
    def test_navigate_back_with_r_command(self, mock_input):
        main()
        output = self.held_output.getvalue()
        # Check that we return to the item type menu (indicated by "Step 1: Select Item Type" appearing twice)
        self.assertEqual(output.count("Step 1:  Select Item Type"), 2)
        self.assertIn("Processing order for 1 x Veggie Burger", output)
        self.assertIn("With options:", output)
        self.assertIn("  - Extra Patty", output)

    @patch('basic_interactive_menu.interactive_menu.input', side_effect=['0', 'y', '1', 'r', 'r', '1', 'y', '1', 'y', '1', 'y', '0', 'y', 'y'])
    def test_multi_level_return_and_restart(self, mock_input):
        main()
        output = self.held_output.getvalue()
        # Check that we return to the item type menu (indicated by "Step 1: Select Item Type" appearing more than once)
        self.assertGreater(output.count("Step 1:  Select Item Type"), 1)
        self.assertIn("Processing order for 2 x Double Burger", output)
        self.assertIn("With options:", output)
        self.assertIn("  - Extra Patty", output)

    @patch('basic_interactive_menu.interactive_menu.input', side_effect=['q'])
    def test_user_quit_at_first_step(self, mock_input):
        main()
        output = self.held_output.getvalue()
        self.assertIn("Exiting...", output)

    @patch('basic_interactive_menu.interactive_menu.input', side_effect=['0', 'y', 'q'])
    def test_user_quit_at_second_step(self, mock_input):
        main()
        output = self.held_output.getvalue()
        self.assertIn("Exiting...", output)

    @patch('basic_interactive_menu.interactive_menu.input', side_effect=['0', 'y', '1', 'y', 'q'])
    def test_user_quit_at_third_step(self, mock_input):
        main()
        output = self.held_output.getvalue()
        self.assertIn("Exiting...", output)

    @patch('basic_interactive_menu.interactive_menu.input', side_effect=['0', 'y', '1', 'y', '2', 'y', 'q'])
    def test_user_quit_at_fourth_step(self, mock_input):
        main()
        output = self.held_output.getvalue()
        self.assertIn("Exiting...", output)

if __name__ == '__main__':
    unittest.main()