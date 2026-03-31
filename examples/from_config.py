"""Example demonstrating loading menu from configuration file."""

from basic_interactive_menu import InteractiveMenu


def main():
    """Run menu from configuration file example."""
    # Load menu from JSON config file
    menu = InteractiveMenu.from_file("examples/config_example.json")

    result = menu.ask().get_all_results()

    if result:
        print(f"\nYou selected: {result['language']}")


if __name__ == "__main__":
    main()
