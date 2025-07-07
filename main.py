from interactive_menu import InteractiveMenu
import classes.classes as classes


def main():
    file_menu = (
        InteractiveMenu()
        .title("Step 1: Select a Data File")
        .add_option("data1.csv")
        .add_option("data2.json")
        .add_option("data3.txt")
    )

    class_menu = (
        InteractiveMenu()
        .title("Step 2: Select a Class")
        .add_option("A")
        .add_option("B")
        .add_option("C")
    )

    type_menu = (
        InteractiveMenu()
        .title("Step 3: Select Chart Types")
        .add_options(["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart"])
        .allow_multiple()
    )

    file_menu.parent = None
    class_menu.parent = file_menu
    type_menu.parent = class_menu

    current_menu = file_menu

    while True:
        current_menu = current_menu.run()

        if current_menu.result() is None:
            print("Operation canceled.")
            break

        if current_menu == file_menu:
            print(f"\nSelected file: {current_menu.result()}")
            current_menu = class_menu
        elif current_menu == class_menu:
            print(f"\nSelected class: {current_menu.result()}")
            current_menu = type_menu
        else:
            selected_types = current_menu.result()
            print(f"\nSelected chart types: {', '.join(selected_types)}")

            print("\nInstantiating class...")

            class_name = class_menu.result()

            try:
                cls = getattr(classes, class_name)
                instance = cls(file=file_menu.result(), types=selected_types)
                print(f"\nSuccessfully created instance: {instance}")
            except AttributeError:
                print(f"\nError: Unknown class '{class_name}'")

            restart = input("\nWould you like to start over? (y/n): ").strip().lower()
            if restart == 'y':
                file_menu.selection = None
                class_menu.selection = None
                type_menu.selection = None
                current_menu = file_menu
                print("\nRestarting process...\n")
            else:
                print("\nExiting application. Goodbye!")
                break


if __name__ == "__main__":
    main()
