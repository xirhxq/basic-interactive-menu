"""Example demonstrating theme functionality."""

from basic_interactive_menu import InteractiveMenu


def main():
    """Run menu with custom theme."""
    menu = InteractiveMenu()

    # Try different built-in themes
    print("Available themes: default, minimal, bold, dim, colorful, hacker")
    print("Using 'hacker' theme...\n")

    result = (
        menu
        .set_title("Hacker Theme Menu")
        .set_key("choice")
        .set_theme("hacker")
        .add_option("Initiate Hack")
        .add_option("Scan Network")
        .add_option("Exploit Vulnerability")
        .add_option("Cover Tracks")
        .ask()
        .get_all_results()
    )

    if result:
        print(f"\nYou selected: {result['choice']}")


if __name__ == "__main__":
    main()
