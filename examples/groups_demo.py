"""Example demonstrating group functionality."""

from basic_interactive_menu import InteractiveMenu


def main():
    """Run menu with grouped options."""
    menu = InteractiveMenu()

    result = (
        menu
        .set_title("Select Database Option")
        .set_key("selection")
        # Add groups of related options
        .add_group("Databases", [
            "PostgreSQL",
            "MySQL",
            "MongoDB",
            "Redis",
        ])
        .add_group("Client Libraries", [
            "psycopg2",
            "pymongo",
            "redis-py",
        ])
        .add_group("Tools", [
            "pgAdmin",
            "DBeaver",
            "Redis Commander",
        ])
        .ask()
        .get_all_results()
    )

    if result:
        print(f"\nYou selected: {result['selection']}")


if __name__ == "__main__":
    main()
