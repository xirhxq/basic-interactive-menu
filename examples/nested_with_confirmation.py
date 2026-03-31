from basic_interactive_menu import InteractiveMenu

def process_order(item, quantity, options):
    print(f"Processing order for {quantity} x {item}")
    if options:
        print("With options:")
        for option in options:
            print(f"  - {option}")
    else:
        print("No additional options selected.")

def main():
    while True:
        # First level: Select item type
        menu = (
            InteractiveMenu()
            .add_option("Pizza")
            .add_option("Burger")
            .add_option("Salad")
            .ask("Select Item Type", "item_type")
        )
        
        item_type_result = menu.get_all_results()
        
        # Handle restart/last options
        if isinstance(item_type_result, InteractiveMenu):
            # User chose to restart or go back, continue the loop
            continue
        
        if item_type_result is None:
            print("\nExiting...")
            return
            
        item_type = item_type_result['item_type']
        
        # Second level: Select specific item
        if item_type == "Pizza":
            menu = (
                InteractiveMenu()
                .add_option("Margherita")
                .add_option("Pepperoni")
                .add_option("Vegetarian")
                .ask("Select Pizza Type", "item")
            )
        elif item_type == "Burger":
            menu = (
                InteractiveMenu()
                .add_option("Cheeseburger")
                .add_option("Double Burger")
                .add_option("Veggie Burger")
                .ask("Select Burger Type", "item")
            )
        else:  # Salad
            menu = (
                InteractiveMenu()
                .add_option("Caesar Salad")
                .add_option("Greek Salad")
                .add_option("Fruit Salad")
                .ask("Select Salad Type", "item")
            )
            
        item_result = menu.get_all_results()
        
        # Handle restart/last options
        if isinstance(item_result, InteractiveMenu):
            # User chose to restart or go back, continue the loop
            continue
            
        if item_result is None:
            print("\nExiting...")
            return
            
        item = item_result['item']
        
        # Third level: Select quantity
        menu = (
            InteractiveMenu()
            .add_option("1")
            .add_option("2")
            .add_option("3")
            .add_option("4")
            .add_option("5")
            .ask("Select Quantity", "quantity")
        )
        
        quantity_result = menu.get_all_results()
        
        # Handle restart/last options
        if isinstance(quantity_result, InteractiveMenu):
            # User chose to restart or go back, continue the loop
            continue
            
        if quantity_result is None:
            print("\nExiting...")
            return
            
        quantity = quantity_result['quantity']
        
        # Fourth level: Select options (multiple selection)
        if item_type == "Pizza":
            menu = (
                InteractiveMenu()
                .add_option("Extra Cheese")
                .add_option("Mushrooms")
                .add_option("Olives")
                .add_option("Peppers")
                .allow_multiple()
                .ask("Select Extra Options", "options")
            )
        elif item_type == "Burger":
            menu = (
                InteractiveMenu()
                .add_option("Extra Patty")
                .add_option("Bacon")
                .add_option("Avocado")
                .add_option("Lettuce")
                .allow_multiple()
                .ask("Select Extra Options", "options")
            )
        else:  # Salad
            menu = (
                InteractiveMenu()
                .add_option("Extra Dressing")
                .add_option("Croutons")
                .add_option("Nuts")
                .add_option("Fruit")
                .allow_multiple()
                .ask("Select Extra Options", "options")
            )
            
        options_result = menu.get_all_results()
        
        # Handle restart/last options
        if isinstance(options_result, InteractiveMenu):
            # User chose to restart or go back, continue the loop
            continue
            
        if options_result is None:
            print("\nExiting...")
            return
            
        options = options_result['options'] if options_result['options'] else []
        
        # Process the order
        process_order(item, quantity, options)
        break

if __name__ == "__main__":
    main()