class InteractiveMenu:
    def __init__(self):
        self.options = []
        self.menu_title = "Choose an option"
        self.multiple_allowed = False
        self.parent = None
        self.selection = None

    def title(self, title_text):
        self.menu_title = title_text
        return self

    def add_option(self, name):
        self.options.append({'name': name})
        return self

    def add_options(self, items):
        for item in items:
            self.add_option(item)
        return self

    def allow_multiple(self):
        self.multiple_allowed = True
        return self

    def run(self):
        while True:
            print("\n" + "-" * 30)
            print(self.menu_title)
            print("-" * 30)

            for idx, option in enumerate(self.options):
                print(f"[{idx}]: {option['name']}")

            print("[q]: Quit")
            if self.parent is not None:
                print("[r]: Return to parent")
            if self.multiple_allowed:
                print("[*]: Enter indices (e.g., 0 1,2) to select multiple")

            choice = input("Choose an option: ").strip().lower()

            if choice == 'q':
                print("Exiting...")
                self.selection = None
                return self
            elif self.parent is not None and choice == 'r':
                print("\nReturning to parent menu...\n")
                return self.parent.run()
            elif self.multiple_allowed:
                selected_indices_input = choice
                try:
                    indices_str = selected_indices_input.replace(',', ' ').split()
                    selected_indices = [int(i) for i in indices_str]
                    results = [self.options[i]['name'] for i in selected_indices if 0 <= i < len(self.options)]

                    if not results:
                        print("Error: You must select at least one option.")
                        continue

                    self.selection = results
                except Exception as e:
                    print("Invalid input format. Please enter indices separated by space or comma.")
                    continue
                return self
            elif choice.isdigit() and 0 <= int(choice) < len(self.options):
                self.selection = self.options[int(choice)]['name']
                return self
            else:
                print("Invalid input. Please try again.")

    def result(self):
        return self.selection
