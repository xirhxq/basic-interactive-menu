"""Theme system for InteractiveMenu.

This module provides theming support using ANSI color codes,
allowing customization of menu appearance without external dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


# ANSI color codes
class Colors:
    """ANSI escape codes for terminal colors."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


@dataclass
class MenuTheme:
    """Theme configuration for menu appearance.

    Attributes:
        name: Theme name.
        border_style: Character(s) used for border lines.
        border_color: ANSI color code for borders.
        title_color: ANSI color code for title text.
        option_color: ANSI color code for option text.
        shortcut_color: ANSI color code for shortcut display.
        selected_color: ANSI color code for selected/highlighted text.
        prompt_color: ANSI color code for input prompt.
    """

    name: str = "default"
    border_style: str = "-"
    border_color: str = Colors.RESET
    title_color: str = Colors.RESET
    option_color: str = Colors.RESET
    shortcut_color: str = Colors.BRIGHT_CYAN
    selected_color: str = Colors.BRIGHT_GREEN
    prompt_color: str = Colors.RESET

    def apply_border(self, text: str) -> str:
        """Apply border styling to text.

        Args:
            text: The border text to style.

        Returns:
            Styled border text.
        """
        return f"{self.border_color}{self.border_style * 30}{Colors.RESET}"

    def apply_title(self, text: str) -> str:
        """Apply title styling to text.

        Args:
            text: The title text to style.

        Returns:
            Styled title text.
        """
        return f"{self.title_color}{text}{Colors.RESET}"

    def apply_option(self, text: str) -> str:
        """Apply option styling to text.

        Args:
            text: The option text to style.

        Returns:
            Styled option text.
        """
        return f"{self.option_color}{text}{Colors.RESET}"

    def apply_shortcut(self, text: str) -> str:
        """Apply shortcut styling to text.

        Args:
            text: The shortcut text to style.

        Returns:
            Styled shortcut text.
        """
        return f"{self.shortcut_color}{text}{Colors.RESET}"

    def apply_selected(self, text: str) -> str:
        """Apply selected/highlight styling to text.

        Args:
            text: The text to highlight.

        Returns:
            Styled text.
        """
        return f"{self.selected_color}{text}{Colors.RESET}"

    def apply_prompt(self, text: str) -> str:
        """Apply prompt styling to text.

        Args:
            text: The prompt text to style.

        Returns:
            Styled prompt text.
        """
        return f"{self.prompt_color}{text}{Colors.RESET}"


# Built-in theme presets
BUILT_IN_THEMES: Dict[str, MenuTheme] = {
    "default": MenuTheme(name="default"),
    "minimal": MenuTheme(
        name="minimal",
        border_style=" ",
    ),
    "bold": MenuTheme(
        name="bold",
        option_color=Colors.BOLD,
        shortcut_color=Colors.BOLD,
    ),
    "dim": MenuTheme(
        name="dim",
        option_color=Colors.DIM,
        prompt_color=Colors.DIM,
    ),
    "colorful": MenuTheme(
        name="colorful",
        border_color=Colors.CYAN,
        title_color=Colors.BOLD,
        option_color=Colors.RESET,
        shortcut_color=Colors.BRIGHT_YELLOW,
        selected_color=Colors.BRIGHT_GREEN,
    ),
    "hacker": MenuTheme(
        name="hacker",
        border_color=Colors.GREEN,
        title_color=Colors.BRIGHT_GREEN,
        option_color=Colors.GREEN,
        shortcut_color=Colors.BRIGHT_GREEN,
        selected_color=Colors.BRIGHT_GREEN,
    ),
}


def get_theme(name: str) -> MenuTheme:
    """Get a theme by name.

    Args:
        name: Theme name. Can be a built-in theme name or 'default'.

    Returns:
        The requested MenuTheme instance.

    Raises:
        KeyError: If the theme name is not found.
    """
    return BUILT_IN_THEMES.get(name.lower(), BUILT_IN_THEMES["default"])


def list_themes() -> list[str]:
    """List all available built-in theme names.

    Returns:
        List of theme names.
    """
    return list(BUILT_IN_THEMES.keys())
