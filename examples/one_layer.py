from interactive_menu import InteractiveMenu


def simple_fruit_menu():
    menu = (
        InteractiveMenu()
        .add_option("Apple") # add an option
        .add_option("Banana")
        .add_options(["Orange", "Grapes"]) # add multiple options
        .ask("Select a Fruit", "selection") # ask the user to select, passing hint and key args
    )

    selection = menu.get_all_results() # get the selection
    print(f"\nYou selected: {selection['selection']}")


if __name__ == "__main__":
    simple_fruit_menu()