import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from examples.one_layer import simple_fruit_menu

class TestOneLayerMenu(unittest.TestCase):
    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('interactive_menu.input', side_effect=['0', 'y'])
    def test_user_selection(self, mock_input):
        simple_fruit_menu()
        output = self.held_output.getvalue()
        self.assertIn("You selected: Apple", output)
        
    @patch('interactive_menu.input', side_effect=['q'])
    def test_user_quit(self, mock_input):
        simple_fruit_menu()
        output = self.held_output.getvalue()
        self.assertIn("Exiting...", output)
        
    @patch('interactive_menu.input', side_effect=['5', 'q'])
    def test_invalid_input(self, mock_input):
        result = simple_fruit_menu()
        output = self.held_output.getvalue()
        self.assertIn("Invalid input. Please try again.", output)
        self.assertIn("Exiting...", output)
        self.assertIsNone(result)
        
    @patch('interactive_menu.input', side_effect=['q'])
    def test_user_quit_returns_none(self, mock_input):
        result = simple_fruit_menu()
        output = self.held_output.getvalue()
        self.assertIn("Exiting...", output)
        self.assertIsNone(result)
        
    @patch('interactive_menu.input', side_effect=['5', '5', 'q'])
    def test_multiple_invalid_inputs_return_none(self, mock_input):
        result = simple_fruit_menu()
        output = self.held_output.getvalue()
        self.assertIn("Invalid input. Please try again.", output)
        self.assertIn("Exiting...", output)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()