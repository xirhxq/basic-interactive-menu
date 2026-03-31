"""Tests for configuration file support."""

import unittest
import json
import tempfile
from pathlib import Path
from io import StringIO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basic_interactive_menu.interactive_menu import InteractiveMenu
from basic_interactive_menu.config import MenuConfig


class TestMenuConfig(unittest.TestCase):
    """Test MenuConfig functionality."""

    def test_from_json_basic(self):
        """Test loading a basic JSON config."""
        config = {
            "title": "Test Menu",
            "key": "test",
            "multiple": False,
            "options": ["A", "B", "C"]
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            loaded = MenuConfig.from_json(temp_path)
            self.assertEqual(loaded["title"], "Test Menu")
            self.assertEqual(loaded["key"], "test")
            self.assertEqual(loaded["options"], ["A", "B", "C"])
        finally:
            os.unlink(temp_path)

    def test_from_json_missing_file(self):
        """Test that missing file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            MenuConfig.from_json("/nonexistent/file.json")

    def test_from_json_invalid_json(self):
        """Test that invalid JSON raises ValueError."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{invalid json")
            temp_path = f.name

        try:
            with self.assertRaises(ValueError):
                MenuConfig.from_json(temp_path)
        finally:
            os.unlink(temp_path)

    def test_from_file_json(self):
        """Test from_file with JSON extension."""
        config = {
            "title": "Test",
            "options": ["A", "B"]
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            loaded = MenuConfig.from_file(temp_path)
            self.assertEqual(loaded["title"], "Test")
        finally:
            os.unlink(temp_path)

    def test_from_file_unsupported_type(self):
        """Test that unsupported file types raise ValueError."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("test")
            temp_path = f.name

        try:
            with self.assertRaises(ValueError) as context:
                MenuConfig.from_file(temp_path)
            self.assertIn("Unsupported", str(context.exception))
        finally:
            os.unlink(temp_path)

    def test_validate_config_valid(self):
        """Test validation of a valid config."""
        config = {
            "title": "Test",
            "options": ["A", "B", "C"]
        }
        # Should not raise
        MenuConfig.validate_config(config)

    def test_validate_config_missing_options(self):
        """Test that missing options field raises ValueError."""
        config = {"title": "Test"}
        with self.assertRaises(ValueError) as context:
            MenuConfig.validate_config(config)
        self.assertIn("options", str(context.exception))

    def test_validate_config_empty_options(self):
        """Test that empty options list raises ValueError."""
        config = {"options": []}
        with self.assertRaises(ValueError) as context:
            MenuConfig.validate_config(config)
        self.assertIn("empty", str(context.exception).lower())

    def test_validate_config_invalid_option_type(self):
        """Test that non-string options raise ValueError."""
        config = {"options": ["A", 123, "C"]}
        with self.assertRaises(ValueError) as context:
            MenuConfig.validate_config(config)
        self.assertIn("string", str(context.exception))

    def test_validate_config_invalid_multiple_type(self):
        """Test that non-boolean multiple raises ValueError."""
        config = {
            "options": ["A", "B"],
            "multiple": "yes"
        }
        with self.assertRaises(ValueError) as context:
            MenuConfig.validate_config(config)
        self.assertIn("boolean", str(context.exception))


class TestInteractiveMenuFromFile(unittest.TestCase):
    """Test InteractiveMenu.from_file() method."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_from_file_basic_json(self):
        """Test creating menu from basic JSON config."""
        config = {
            "title": "Select Fruit",
            "key": "fruit",
            "options": ["Apple", "Banana", "Cherry"]
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            menu = InteractiveMenu.from_file(temp_path)
            self.assertEqual(menu.menu_title[0], "Select Fruit")
            self.assertEqual(menu.keys[0], "fruit")
            self.assertEqual(len(menu.options[0]), 3)
            self.assertEqual(menu.options[0][0]["name"], "Apple")
        finally:
            os.unlink(temp_path)

    def test_from_file_with_multiple(self):
        """Test creating menu with multiple selection enabled."""
        config = {
            "title": "Select Items",
            "key": "items",
            "multiple": True,
            "options": ["A", "B", "C"]
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            menu = InteractiveMenu.from_file(temp_path)
            self.assertTrue(menu.multiple_allowed[0])
        finally:
            os.unlink(temp_path)

    def test_from_file_with_shortcuts(self):
        """Test creating menu with explicit shortcuts."""
        config = {
            "options": [
                {"name": "Exit", "shortcut": "x"},
                {"name": "Continue", "shortcut": "c"}
            ]
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            menu = InteractiveMenu.from_file(temp_path)
            self.assertEqual(menu.shortcuts[0]["x"], 0)
            self.assertEqual(menu.shortcuts[0]["c"], 1)
        finally:
            os.unlink(temp_path)

    def test_from_file_with_debug(self):
        """Test creating menu with debug mode enabled."""
        config = {
            "debug": True,
            "options": ["A", "B"]
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            menu = InteractiveMenu.from_file(temp_path)
            self.assertTrue(menu.DEBUG)
        finally:
            os.unlink(temp_path)


class TestYAMLSupport(unittest.TestCase):
    """Test optional YAML support."""

    def test_from_yaml_without_pyyaml(self):
        """Test that YAML without pyyaml raises appropriate error."""
        # Create a temporary YAML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("title: Test\noptions:\n  - A\n  - B")
            temp_path = f.name

        try:
            # Try to import yaml to check if it's available
            try:
                import yaml
                has_yaml = True
            except ImportError:
                has_yaml = False

            if has_yaml:
                # If yaml is available, this should work
                config = MenuConfig.from_yaml(temp_path)
                self.assertEqual(config["title"], "Test")
            else:
                # If yaml is not available, should raise ValueError
                with self.assertRaises(ValueError) as context:
                    MenuConfig.from_yaml(temp_path)
                self.assertIn("PyYAML", str(context.exception))
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
