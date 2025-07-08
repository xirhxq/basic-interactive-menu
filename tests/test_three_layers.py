import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from examples.three_layers import main

class TestThreeLayersMenu(unittest.TestCase):
    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('interactive_menu.input', side_effect=['0', 'r', '1', 'r', '2', '0', '1, 2 3', 'y'])
    def test_navigate_back_with_r_command(self, mock_input):
        main()
        output = self.held_output.getvalue()
        self.assertIn("Returning to parent menu...", output)
        self.assertIn("You selected: data3.txt", output)

    @patch('interactive_menu.input', side_effect=['0', '0', 'r', 'r', '1', '1', '0', 'y'])
    def test_multi_level_return_and_restart(self, mock_input):
        main()
        output = self.held_output.getvalue()
        self.assertIn("Returning to parent menu...", output)
        self.assertIn("You selected: data2.json", output)

    @patch('interactive_menu.input', side_effect=['0', '0', 'r', '1', '1', 'r', '2', '2', '1, 2', 'y'])
    def test_selection_persistence_and_return(self, mock_input):
        main()
        output = self.held_output.getvalue()
        self.assertIn("You selected: data3.txt", output)

    @patch('interactive_menu.input', side_effect=['0', '0', '1, 2  3', 'l', 'r', 'r', 'q'])
    def test_escape_all_levels(self, mock_input):
        main()
        output = self.held_output.getvalue()
        self.assertIn("Exiting...", output)

    @patch('interactive_menu.input', side_effect=['0', '0', 'r', 'r', 'r', 'r', 'q'])
    def test_excessive_r_commands(self, mock_input):
        main()
        output = self.held_output.getvalue()
        self.assertIn("Invalid input. Please try again.", output)
        self.assertIn("Exiting...", output)

    @patch('interactive_menu.input', side_effect=['0', '0', '2, 3', 'r', '1', '1', '1, 3 4', 'y'])
    def test_restart_workflow(self, mock_input):
        main()
        output = self.held_output.getvalue()
        self.assertIn("Current selections:", output)
        self.assertIn("You selected: data2.json", output)