"""Example demonstrating search functionality."""

from basic_interactive_menu import InteractiveMenu


def main():
    """Run menu with search enabled."""
    menu = InteractiveMenu()

    result = (
        menu
        .set_title("Select Programming Language")
        .set_key("language")
        .enable_search()  # Enable search with "/" key
        .add_options([
            "Python",
            "JavaScript",
            "TypeScript",
            "Go",
            "Rust",
            "Java",
            "C++",
            "Ruby",
            "PHP",
            "Swift",
            "Kotlin",
            "Scala",
            "Haskell",
            "Lua",
            "Perl",
            "R",
        ])
        .ask()
        .get_all_results()
    )

    if result:
        print(f"\nYou selected: {result['language']}")


if __name__ == "__main__":
    main()
