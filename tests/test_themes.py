"""Tests for theme functionality."""

import unittest
from basic_interactive_menu.themes import MenuTheme, Colors, get_theme, list_themes, BUILT_IN_THEMES


class TestMenuTheme(unittest.TestCase):
    """Test MenuTheme dataclass."""

    def test_default_theme(self):
        """Test default theme creation."""
        theme = MenuTheme()
        self.assertEqual(theme.name, "default")
        self.assertEqual(theme.border_style, "-")
        self.assertEqual(theme.border_color, Colors.RESET)

    def test_custom_theme(self):
        """Test custom theme configuration."""
        theme = MenuTheme(
            name="custom",
            border_style="=",
            border_color=Colors.CYAN,
        )
        self.assertEqual(theme.name, "custom")
        self.assertEqual(theme.border_style, "=")

    def test_apply_border(self):
        """Test applying border styling."""
        theme = MenuTheme(border_color=Colors.CYAN)
        result = theme.apply_border("----")
        self.assertIn(Colors.CYAN, result)
        self.assertIn("----", result)

    def test_apply_title(self):
        """Test applying title styling."""
        theme = MenuTheme(title_color=Colors.BOLD)
        result = theme.apply_title("Test Title")
        self.assertIn(Colors.BOLD, result)
        self.assertIn("Test Title", result)

    def test_apply_option(self):
        """Test applying option styling."""
        theme = MenuTheme(option_color=Colors.DIM)
        result = theme.apply_option("Option")
        self.assertIn(Colors.DIM, result)
        self.assertIn("Option", result)

    def test_apply_shortcut(self):
        """Test applying shortcut styling."""
        theme = MenuTheme(shortcut_color=Colors.BRIGHT_YELLOW)
        result = theme.apply_shortcut("X")
        self.assertIn(Colors.BRIGHT_YELLOW, result)
        self.assertIn("X", result)

    def test_apply_selected(self):
        """Test applying selected styling."""
        theme = MenuTheme(selected_color=Colors.BRIGHT_GREEN)
        result = theme.apply_selected("Selected")
        self.assertIn(Colors.BRIGHT_GREEN, result)
        self.assertIn("Selected", result)

    def test_apply_prompt(self):
        """Test applying prompt styling."""
        theme = MenuTheme(prompt_color=Colors.RESET)
        result = theme.apply_prompt("Choose: ")
        self.assertIn("Choose: ", result)


class TestBuiltinThemes(unittest.TestCase):
    """Test built-in theme presets."""

    def test_all_themes_have_required_attributes(self):
        """Test that all built-in themes have required attributes."""
        for name, theme in BUILT_IN_THEMES.items():
            self.assertIsNotNone(theme.border_style)
            self.assertIsNotNone(theme.title_color)
            self.assertIsNotNone(theme.option_color)

    def test_list_themes(self):
        """Test listing all available themes."""
        themes = list_themes()
        self.assertIn("default", themes)
        self.assertIn("minimal", themes)
        self.assertIn("bold", themes)
        self.assertIn("colorful", themes)
        self.assertIn("hacker", themes)


class TestGetTheme(unittest.TestCase):
    """Test get_theme function."""

    def test_get_default_theme(self):
        """Test getting default theme."""
        theme = get_theme("default")
        self.assertEqual(theme.name, "default")

    def test_get_builtin_theme(self):
        """Test getting built-in theme."""
        theme = get_theme("minimal")
        self.assertEqual(theme.name, "minimal")

    def test_get_unknown_theme_returns_default(self):
        """Test that unknown theme name returns default."""
        theme = get_theme("unknown")
        self.assertEqual(theme.name, "default")

    def test_get_theme_is_case_insensitive(self):
        """Test that theme lookup is case-insensitive."""
        theme1 = get_theme("COLORFUL")
        theme2 = get_theme("colorful")
        self.assertEqual(theme1.name, theme2.name)


if __name__ == '__main__':
    unittest.main()
