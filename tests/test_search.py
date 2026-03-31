"""Tests for search functionality."""

import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basic_interactive_menu.search import SearchEngine
from basic_interactive_menu.interactive_menu import InteractiveMenu


class TestSearchEngine(unittest.TestCase):
    """Test SearchEngine functionality."""

    def test_search_empty_query(self):
        """Test that empty query returns all indices."""
        engine = SearchEngine(["Apple", "Banana", "Cherry"])
        result = engine.search("")
        self.assertEqual(result, [0, 1, 2])

    def test_search_exact_match(self):
        """Test exact substring matching."""
        engine = SearchEngine(["Apple", "Banana", "Cherry"])
        result = engine.search("app")
        self.assertEqual(result, [0])

    def test_search_case_insensitive(self):
        """Test case-insensitive search."""
        engine = SearchEngine(["Apple", "BANANA", "Cherry"])
        result = engine.search("banana")
        self.assertEqual(result, [1])

    def test_search_multiple_matches(self):
        """Test multiple matches."""
        engine = SearchEngine(["Python", "Cython", "PyPy", "Pyjama", "Java"])
        result = engine.search("py")
        # Python, PyPy, Pyjama contain "py" substring
        self.assertEqual(set(result), {0, 2, 3})

    def test_search_no_matches(self):
        """Test search with no matches."""
        engine = SearchEngine(["Apple", "Banana", "Orange"])
        result = engine.search("xyz")
        self.assertEqual(result, [])

    def test_get_matches_summary(self):
        """Test match summary generation."""
        engine = SearchEngine(["Apple", "Banana", "Cherry"])
        summary = engine.get_matches_summary("app")
        self.assertIn("1 match", summary)
        self.assertIn("Apple", summary)


class TestSearchInMenu(unittest.TestCase):
    """Test search functionality within InteractiveMenu."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', side_effect=['q'])
    def test_search_shown_in_menu(self, mock_input):
        """Test that search indicator appears when enabled."""
        menu = InteractiveMenu()
        menu.set_title("Test").enable_search().add_option("Apple").ask()
        output = self.held_output.getvalue()
        self.assertIn("[/]: Search", output)


if __name__ == '__main__':
    unittest.main()
