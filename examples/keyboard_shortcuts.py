"""Example demonstrating keyboard shortcuts feature."""

from basic_interactive_menu import InteractiveMenu


def main():
    """Run menu with keyboard shortcuts example."""
    menu = InteractiveMenu()

    result = (
        menu
        .set_title("Select Action")
        .set_key("action")
        # Explicit shortcuts
        .add_option("Exit", shortcut='x')
        .add_option("Continue", shortcut='c')
        # Auto-generated shortcuts
        .add_option("Help")
        .add_option("Settings")
        .ask()
        .get_all_results()
    )

    if result:
        print(f"\nYou selected: {result['action']}")


if __name__ == "__main__":
    main()
