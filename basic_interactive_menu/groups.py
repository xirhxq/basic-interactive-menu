"""Group functionality for organizing menu options.

This module provides the ability to group related menu options together
for better organization and visual clarity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class OptionGroup:
    """A group of related menu options.

    Attributes:
        name: Display name for the group.
        options: List of option strings in this group.
        collapsed: Whether the group is collapsed by default.
    """

    name: str
    options: List[str]
    collapsed: bool = False

    def __post_init__(self) -> None:
        """Validate the group after initialization."""
        if not self.options:
            raise ValueError(f"Group '{self.name}' cannot have empty options")

    def option_count(self) -> int:
        """Return the number of options in this group.

        Returns:
            Number of options in the group.
        """
        return len(self.options)


@dataclass
class GroupRenderer:
    """Handles the rendering of option groups in the menu display.

    Attributes:
        groups: List of OptionGroup objects to render.
        current_index: Global index counter across all groups.
    """

    groups: List[OptionGroup] = field(default_factory=list)
    current_index: int = 0

    def add_group(self, name: str, options: List[str], collapsed: bool = False) -> None:
        """Add a new group to the renderer.

        Args:
            name: Display name for the group.
            options: List of option strings in this group.
            collapsed: Whether the group is collapsed by default.

        Raises:
            ValueError: If options list is empty.
        """
        group = OptionGroup(name=name, options=options, collapsed=collapsed)
        self.groups.append(group)

    def get_global_index(self, group_index: int, local_index: int) -> int:
        """Get the global option index for a group-relative index.

        Args:
            group_index: Which group (0-based).
            local_index: Index within that group.

        Returns:
            Global index across all groups.
        """
        index = 0
        for i in range(group_index):
            if not self.groups[i].collapsed:
                index += len(self.groups[i].options)

        if not self.groups[group_index].collapsed:
            index += local_index

        return index

    def get_all_options(self) -> List[str]:
        """Get all options from all non-collapsed groups.

        Returns:
            Flat list of all visible options.
        """
        all_options: List[str] = []
        for group in self.groups:
            if not group.collapsed:
                all_options.extend(group.options)
        return all_options

    def render_header(self, group: OptionGroup) -> str:
        """Render the group header/separator.

        Args:
            group: The OptionGroup to render.

        Returns:
            Formatted header string.
        """
        header = f"\n{group.name}:"
        if group.collapsed:
            header += " (collapsed - press space to expand)"
        return header

    def render_option(self, global_index: int, option: str,
                      shortcut: Optional[str] = None) -> str:
        """Render a single menu option with global indexing.

        Args:
            global_index: Global index across all groups.
            option: The option text to render.
            shortcut: Optional shortcut character.

        Returns:
            Formatted option string.
        """
        if shortcut:
            return f"  [{global_index}/{shortcut.upper()}]: {option}"
        return f"  [{global_index}]: {option}"

    def total_visible_options(self) -> int:
        """Get the total count of visible options.

        Returns:
            Number of visible options across all groups.
        """
        return sum(len(g.options) for g in self.groups if not g.collapsed)
