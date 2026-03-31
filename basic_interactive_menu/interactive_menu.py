"""Interactive menu system for building command-line applications.

This module provides a fluent chainable API for creating interactive CLI menus
with support for nested menus, selection workflows, and parent-child navigation.

Example:
    >>> results = (
    ...     InteractiveMenu()
    ...     .set_title("Select a Fruit")
    ...     .set_key("fruit")
    ...     .add_option("Apple")
    ...     .add_option("Banana")
    ...     .add_options(["Orange", "Grapes"])
    ...     .ask()
    ...     .get_all_results()
    ... )
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any, Optional, Union


class InteractiveMenu:
    """A fluent chainable API for creating interactive CLI menus.

    This class provides a simple and intuitive way to build command-line
    interfaces with nested menus, selection persistence, and parent-child
    navigation.

    Attributes:
        DEFAULT_TITLE: The default title displayed when no title is set.
        DEFAULT_MULTIPLE_ALLOWED: Default setting for multiple selection mode.
        DEBUG: Global debug flag for verbose output.

    Example:
        >>> menu = InteractiveMenu()
        >>> results = (menu
        ...            .set_title("Choose an option")
        ...            .set_key("choice")
        ...            .add_option("Option A")
        ...            .add_option("Option B")
        ...            .ask()
        ...            .get_all_results())
    """

    DEFAULT_TITLE: str = "Choose an option"
    DEFAULT_MULTIPLE_ALLOWED: bool = False
    DEBUG: bool = False

    def __init__(self, multiple_allowed: bool = False, debug: bool = False) -> None:
        """Initialize an InteractiveMenu instance.

        Args:
            multiple_allowed: Whether multiple selections are allowed by default.
                Defaults to False.
            debug: Enable debug output for troubleshooting. Defaults to False.
        """
        self.current_index: int = 0
        self.options: List[List[Dict[str, str]]] = [[]]
        self.menu_title: List[str] = [self.DEFAULT_TITLE]
        self.multiple_allowed: List[bool] = [multiple_allowed]
        self.DEBUG: bool = debug
        self.keys: List[Optional[str]] = [None]
        self.results: List[Optional[Union[str, List[str]]]] = [None]
        self.shortcuts: List[Dict[str, int]] = [{}]
        self.quit: bool = False
        self.end: bool = False

        # v0.3 features
        self.search_enabled: List[bool] = [False]
        self.groups: List[List] = [[]]  # List of group renderers per level
        self.theme: Any = None  # Will be set by set_theme()

    def has_quit(self) -> bool:
        return self.quit

    def has_ended(self) -> bool:
        if self.DEBUG:
            print("Has ended" if self.end else "Not ended")
        return self.end

    def set_key(self, key: str) -> 'InteractiveMenu':
        """Set the result key name for the current menu level.

        Args:
            key: The key name to use for storing the selection result.

        Returns:
            Self, for method chaining.
        """
        if self.quit:
            return self
        self.keys[self.current_index] = key
        return self

    def set_title(self, title_text: str) -> 'InteractiveMenu':
        """Set the menu title for the current menu level.

        Args:
            title_text: The title text to display for this menu.

        Returns:
            Self, for method chaining.
        """
        if self.quit:
            return self
        self.menu_title[self.current_index] = title_text
        return self

    def add_option(self, name: str, shortcut: Optional[str] = None) -> 'InteractiveMenu':
        """Add a single option to the current menu.

        Args:
            name: The display name of the option.
            shortcut: Optional single-character shortcut key. If None, auto-generated
                from the first alphabetic character of the name.

        Returns:
            Self, for method chaining.
        """
        if self.quit:
            return self
        option_index = len(self.options[self.current_index])
        self.options[self.current_index].append({'name': name})

        if shortcut is not None:
            shortcut = shortcut.lower()
            if shortcut in self.shortcuts[self.current_index]:
                existing_idx = self.shortcuts[self.current_index][shortcut]
                raise ValueError(f"Shortcut '{shortcut}' conflicts with option at index {existing_idx}")
            self.shortcuts[self.current_index][shortcut] = option_index

        if self.DEBUG:
            print(f"Added option: {name} (shortcut: {shortcut})")
        return self

    def add_options(self, items: List[str]) -> 'InteractiveMenu':
        """Add multiple options to the current menu.

        Args:
            items: A list of option display names to add.

        Returns:
            Self, for method chaining.
        """
        if self.quit:
            return self
        for item in items:
            self.add_option(item)
        if self.DEBUG:
            print(f"Added options: {items}")
        return self

    def allow_multiple(self) -> 'InteractiveMenu':
        """Enable multiple selection mode for the current menu.

        When enabled, users can select multiple options by entering
        indices separated by spaces or commas (e.g., "0 1,2").

        Returns:
            Self, for method chaining.
        """
        if self.quit:
            return self
        self.multiple_allowed[self.current_index] = True
        if self.DEBUG:
            print(f"Allow multiple: {self.multiple_allowed[self.current_index]}")
        return self

    def enable_search(self) -> 'InteractiveMenu':
        """Enable search functionality for the current menu.

        When enabled, users can press '/' to enter search mode and
        filter options by typing a query string.

        Returns:
            Self, for method chaining.
        """
        self.search_enabled[self.current_index] = True
        return self

    def add_group(self, name: str, options: List[str]) -> 'InteractiveMenu':
        """Add a group of related options to the current menu.

        Groups are visually separated in the menu display and help
        organize related options together.

        Args:
            name: Display name for the group.
            options: List of option strings in this group.

        Returns:
            Self, for method chaining.

        Raises:
            ValueError: If options list is empty.
        """
        if not options:
            raise ValueError(f"Group '{name}' cannot have empty options")

        from basic_interactive_menu.groups import OptionGroup
        self.groups[self.current_index].append(OptionGroup(name=name, options=options))

        for option in options:
            self.add_option(option)
        return self

    def set_theme(self, theme: Union[str, Any]) -> 'InteractiveMenu':
        """Set the visual theme for menu display.

        Args:
            theme: Either a theme name (str) like 'minimal', 'bold', 'colorful',
                or a MenuTheme object for custom theming.

        Returns:
            Self, for method chaining.
        """
        from basic_interactive_menu.themes import get_theme

        if isinstance(theme, str):
            self.theme = get_theme(theme)
        else:
            self.theme = theme
        return self

    @classmethod
    def from_file(cls, file_path: Union[str, Path]) -> 'InteractiveMenu':
        """Create an InteractiveMenu from a configuration file.

        Supports JSON and YAML (if pyyaml is installed) file formats.

        Args:
            file_path: Path to the configuration file.

        Returns:
            A new InteractiveMenu instance configured from the file.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If the file type is unsupported or content is invalid.

        Example:
            >>> menu = InteractiveMenu.from_file("menu_config.json")
            >>> results = menu.ask().get_all_results()
        """
        from basic_interactive_menu.config import MenuConfig

        config = MenuConfig.from_file(file_path)
        MenuConfig.validate_config(config)

        menu = cls(
            multiple_allowed=config.get("multiple", False),
            debug=config.get("debug", False)
        )

        title = config.get("title")
        if title:
            menu.set_title(title)

        key = config.get("key")
        if key:
            menu.set_key(key)

        options = config.get("options", [])
        for option in options:
            if isinstance(option, str):
                menu.add_option(option)
            elif isinstance(option, dict):
                name = option.get("name")
                shortcut = option.get("shortcut")
                if name:
                    menu.add_option(name, shortcut=shortcut)

        return menu

    def _auto_generate_shortcuts(self) -> None:
        """Auto-generate shortcuts for options without explicit shortcuts.

        Uses the first unique alphabetic character from each option name.
        """
        current_shortcuts = self.shortcuts[self.current_index].copy()
        used_chars = set(current_shortcuts.keys())

        for idx, option in enumerate(self.options[self.current_index]):
            if idx in current_shortcuts.values():
                continue

            name = option['name']
            for char in name.lower():
                if char.isalpha() and char not in used_chars:
                    self.shortcuts[self.current_index][char] = idx
                    used_chars.add(char)
                    break

    def _get_option_shortcut(self, index: int) -> Optional[str]:
        """Get the shortcut character for an option by index.

        Args:
            index: The option index.

        Returns:
            The shortcut character or None if no shortcut is assigned.
        """
        for shortcut, idx in self.shortcuts[self.current_index].items():
            if idx == index:
                return shortcut
        return None

    def _has_parent(self) -> bool:
        if self.DEBUG:
            print(f"Current index: {self.current_index}")
        return self.current_index > 0

    def _to_parent(self) -> None:
        if self.DEBUG:
            print(f"Index from {self.current_index} to", end=" ")
        self.current_index -= 1
        if self.DEBUG:
            print(f"{self.current_index}")
        self._check_index_validity()

    def _is_new(self) -> bool:
        return len(self.options[self.current_index]) == 0

    def _need_new(self) -> bool:
        return self.current_index >= len(self.options)

    def _is_last(self) -> bool:
        if self.DEBUG:
            print(f"Is last: {self.current_index} == {len(self.options) - 1}")
        return self.current_index == len(self.options) - 1

    def _to_next(self) -> None:
        self.current_index += 1
        if self._need_new():
            self.options.append([])
            self.menu_title.append(self.DEFAULT_TITLE)
            self.multiple_allowed.append(self.DEFAULT_MULTIPLE_ALLOWED)
            self.keys.append(None)
            self.results.append(None)
            self.shortcuts.append({})
            self.search_enabled.append(False)
            self.groups.append([])
        self._check_index_validity()

    def _remove_last(self) -> None:
        self.options.pop()
        self.menu_title.pop()
        self.multiple_allowed.pop()
        self.keys.pop()
        self.results.pop()
        self.shortcuts.pop()
        self.search_enabled.pop()
        self.groups.pop()
        self.current_index -= 1
        self._check_index_validity()

    def _check_index_validity(self) -> None:
        if self.DEBUG:
            print(f"Checking index validity: {self.current_index} in range (0, {len(self.options)})")
        assert 0 <= self.current_index < len(self.options), "Invalid index, something went wrong"

    def _is_multiple_allowed(self) -> bool:
        return self.multiple_allowed[self.current_index]

    def _print_history(self) -> None:
        if not self._has_parent():
            return
        print("History:", end=" ")
        for i in range(self.current_index):
            if i > 0:
                print("->", end=" ")
            key = self.keys[i]
            result = self.results[i]
            if key is not None:
                print(f"{key}=", end="")
            if isinstance(result, list):
                print("[" + ", ".join(result) + "]", end=" ")
            elif result is not None:
                print(result, end=" ")
        print()

    def _save_result_once(self, value: Union[str, List[str]]) -> None:
        self.results[self.current_index] = value
        if self.DEBUG:
            print(f"Saved result: {self.keys[self.current_index]} = {value}")
            print(f"Now results: {self.results}")
        self._to_next()

    def _handle_search_mode(self) -> None:
        """Handle interactive search mode for filtering options.

        Users can type a query string and see matching options.
        Press Enter to select from filtered results, '/' again or Esc to exit search.
        """
        from basic_interactive_menu.search import SearchEngine

        option_names = [opt['name'] for opt in self.options[self.current_index]]
        engine = SearchEngine(option_names)

        while True:
            prompt = "Filter: "
            if self.theme:
                prompt = self.theme.apply_prompt("Filter: ")
            query = input(prompt).strip().lower()

            # Exit search mode with '/' again or empty input
            if query == '/' or query == '':
                print("Exited search mode")
                return

            matches = engine.search(query)

            if not matches:
                print("No matches found. Try again or '/' to exit.")
                continue

            # Display filtered results
            print(f"\n{engine.get_matches_summary(query)}")
            print("-" * 30)
            for idx in matches:
                shortcut = self._get_option_shortcut(idx)
                if shortcut:
                    print(f"[{idx}/{shortcut.upper()}]: {option_names[idx]}")
                else:
                    print(f"[{idx}]: {option_names[idx]}")

            # Get selection from filtered results
            prompt = "Select (or '/' to search again): "
            if self.theme:
                prompt = self.theme.apply_prompt("Select (or '/' to search again): ")
            select = input(prompt).strip().lower()

            if select == '/':
                continue  # Search again
            elif select.isdigit() and int(select) in matches:
                selected_index = int(select)
                if self._is_multiple_allowed():
                    self._save_result_once([self.options[self.current_index][selected_index]['name']])
                else:
                    self._save_result_once(self.options[self.current_index][selected_index]['name'])
                return
            else:
                print("Invalid selection. Try again.")

    def _print_groups(self) -> None:
        """Print options organized by groups.

        For menus with groups, displays headers and options with
        proper global indexing.
        """
        from basic_interactive_menu.groups import GroupRenderer

        renderer = GroupRenderer()

        # Build groups from options
        option_names = [opt['name'] for opt in self.options[self.current_index]]
        for group in self.groups[self.current_index]:
            renderer.add_group(group.name, group.options)

        global_index = 0
        for group_idx, group in enumerate(renderer.groups):
            print(renderer.render_header(group))
            for option in group.options:
                # Find the actual index of this option
                actual_index = option_names.index(option)
                shortcut = self._get_option_shortcut(actual_index)
                if shortcut:
                    print(renderer.render_option(global_index, option, shortcut))
                else:
                    print(renderer.render_option(global_index, option))
                global_index += 1

    def ask(self, title: Optional[str] = None, key: Optional[str] = None) -> 'InteractiveMenu':
        """Display the menu and prompt for user input.

        This method renders the current menu with all options and waits
        for user input. Special commands include:
        - 'q': Quit the entire menu workflow
        - 'r': Return to the parent menu (only available in nested menus)
        - Multiple indices (when multiple selection is enabled): e.g., "0 1,2"

        Args:
            title: Optional title to override the current menu title.
                If None, uses the title set by set_title().
            key: Optional key name for storing the result.
                If None, uses the key set by set_key().

        Returns:
            Self, for method chaining.
        """
        # If this is a restart, we need to reset the state
        if self.end and self.current_index == 0 and len(self.options[0]) == 0:
            # This is a restart, reset everything
            self.end = False
            
        if self.DEBUG:
            print(f"Asking with ended {self.end} and quit {self.quit}")
        if self.quit:
            return self
        if key is not None:
            self.set_key(key)
        if title is not None:
            self.set_title(title)

        # Auto-generate shortcuts for options without explicit shortcuts
        self._auto_generate_shortcuts()

        while True:
            print("\n" + "-" * 30)
            print(f"Step {self.current_index + 1}: ", self.menu_title[self.current_index])
            print("-" * 30)
            self._print_history()

            # Apply theme if set
            if self.theme:
                print(self.theme.apply_border("-" * 30))

            # Display groups or regular options
            if self.groups[self.current_index]:
                self._print_groups()
            else:
                for idx, option in enumerate(self.options[self.current_index]):
                    shortcut = self._get_option_shortcut(idx)
                    if self.theme:
                        if shortcut:
                            print(f"[{idx}/{self.theme.apply_shortcut(shortcut.upper())}]: {self.theme.apply_option(option['name'])}")
                        else:
                            print(f"[{idx}]: {self.theme.apply_option(option['name'])}")
                    else:
                        if shortcut:
                            print(f"[{idx}/{shortcut.upper()}]: {option['name']}")
                        else:
                            print(f"[{idx}]: {option['name']}")

            print("[q]: Quit")
            if self._has_parent():
                print("[r]: Return to parent")
            if self._is_multiple_allowed():
                print("[*]: Enter indices (e.g., 0 1,2) to select multiple")
            if self.search_enabled[self.current_index]:
                print("[/]: Search")

            prompt = "Choose an option: "
            if self.theme:
                prompt = self.theme.apply_prompt("Choose an option: ")
            choice = input(prompt).strip().lower()

            # Search mode
            if self.search_enabled[self.current_index] and choice == '/':
                self._handle_search_mode()
                continue

            # Check for single-character shortcut
            if len(choice) == 1 and choice.isalpha() and choice in self.shortcuts[self.current_index]:
                selected_index = self.shortcuts[self.current_index][choice]
                if self._is_multiple_allowed():
                    self._save_result_once([self.options[self.current_index][selected_index]['name']])
                else:
                    self._save_result_once(self.options[self.current_index][selected_index]['name'])
                if self._is_new():
                    return self
                continue
            elif choice == 'q':
                print("Exiting...")
                self.quit = True
                return self
            elif self._has_parent() and choice == 'r':
                print("\nReturning to parent menu...\n")
                self._to_parent()
                continue
            elif self._is_multiple_allowed():
                selected_indices_input = choice
                try:
                    indices_str = selected_indices_input.replace(',', ' ').split()
                    selected_indices = [int(i) for i in indices_str]
                    results = [self.options[self.current_index][i]['name'] for i in selected_indices if 0 <= i < len(self.options[self.current_index])]

                    if not results:
                        print("Error: You must select at least one option.")
                        continue

                    self._save_result_once(results)
                    if self._is_new():
                        return self
                    continue
                except Exception as e:
                    print("Invalid input format. Please enter indices separated by space or comma.")
                    continue
            elif choice.isdigit() and 0 <= int(choice) < len(self.options[self.current_index]):
                self._save_result_once(self.options[self.current_index][int(choice)]['name'])
                if self._is_new():
                    return self
                continue
            else:
                print("Invalid input. Please try again.")

    def _reset(self) -> None:
        self.current_index = 0

    def get_all_results(self) -> Optional[Union[Dict[str, Any], 'InteractiveMenu']]:
        """Get all collected results with user confirmation.

        This method displays all selections made across all menu levels
        and prompts for confirmation. The user can:
        - 'y': Confirm and return the results dictionary
        - 'n': Cancel and return None
        - 'r': Restart the menu workflow
        - 'l': Continue to add more options (last option)

        Returns:
            A dictionary mapping keys to selected values if confirmed,
            None if cancelled, or self if restarting/continuing.
            For multiple selections, values are lists of strings.
            For single selections, values are strings.
        """
        if self.DEBUG:
            print(f"Get all results")
        if self.quit:
            if self.DEBUG:
                print("Quit")
            return None
        if not self.end:
            self.end = True
            # Only remove last if we have more than one level and it's empty
            if len(self.options) > 1 and len(self.options[-1]) == 0:
                self._remove_last()
            # Filter out None keys and create a clean dictionary
            results: Dict[str, Any] = {}
            # Use all levels that have keys and results
            for i in range(len(self.keys)):
                key = self.keys[i]
                result = self.results[i]
                if key is not None and result is not None:
                    results[key] = result
            
            print("\nCurrent selections:")
            for k, v in results.items():
                print(f"{k}: {v}")

            while True:
                confirm = input("\nConfirm selection? (y/n/r=restart/l=last): ").strip().lower()
                if confirm == 'y':
                    return results
                elif confirm == 'n':
                    return None
                elif confirm == 'r':
                    self._reset()
                    # For restart, we return self to allow building a new menu
                    return self
                elif confirm == 'l':
                    # For last, we also return self to allow building a new menu
                    return self
                else:
                    print("Invalid input. Please enter y/n/r")
        else:
            # This is a restart or last option, so we need to ask again
            # Return self to allow continuing the chain
            return self

