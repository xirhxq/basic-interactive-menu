from ultralytics.utils import DEFAULT_CFG


class InteractiveMenu:
    DEFAULT_TITLE = "Choose an option"
    DEFAULT_MULTIPLE_ALLOWED = False
    DEBUG = False
    def __init__(self, multiple_allowed=False, debug=False):
        self.current_index = 0
        self.options = [[]]
        self.menu_title = [self.DEFAULT_TITLE]
        self.DEFAULT_MULTIPLE_ALLOWED = multiple_allowed
        self.multiple_allowed = [self.DEFAULT_MULTIPLE_ALLOWED]
        self.DEBUG = debug
        self.keys = [None]
        self.results = [None]
        self.quit = False
        self.end = False

    def has_quit(self):
        return self.quit

    def has_ended(self):
        if self.DEBUG:
            print("Has ended" if self.end else "Not ended")
        return self.end

    def set_key(self, key):
        if self.quit:
            return self
        self.keys[self.current_index] = key
        return self

    def set_title(self, title_text):
        if self.quit:
            return self
        self.menu_title[self.current_index] = title_text
        return self

    def add_option(self, name):
        if self.quit:
            return self
        self.options[self.current_index].append({'name': name})
        if self.DEBUG:
            print(f"Added option: {name}")
        return self

    def add_options(self, items):
        if self.quit:
            return self
        for item in items:
            self.add_option(item)
        if self.DEBUG:
            print(f"Added options: {items}")
        return self

    def allow_multiple(self):
        if self.quit:
            return self
        self.multiple_allowed[self.current_index] = True
        if self.DEBUG:
            print(f"Allow multiple: {self.multiple_allowed[self.current_index]}")
        return self

    def _has_parent(self):
        if self.DEBUG:
            print(f"Current index: {self.current_index}")
        return self.current_index > 0

    def _to_parent(self):
        if self.DEBUG:
            print(f"Index from {self.current_index} to", end=" ")
        self.current_index -= 1
        if self.DEBUG:
            print(f"{self.current_index}")
        self._check_index_validity()

    def _is_new(self):
        return len(self.options[self.current_index]) == 0

    def _need_new(self):
        return self.current_index >= len(self.options)

    def _is_last(self):
        if self.DEBUG:
            print(f"Is last: {self.current_index} == {len(self.options) - 1}")
        return self.current_index == len(self.options) - 1

    def _to_next(self):
        self.current_index += 1
        if self._need_new():
            self.options.append([])
            self.menu_title.append(self.DEFAULT_TITLE)
            self.multiple_allowed.append(self.DEFAULT_MULTIPLE_ALLOWED)
            self.keys.append(None)
            self.results.append(None)
        self._check_index_validity()

    def _remove_last(self):
        self.options.pop()
        self.menu_title.pop()
        self.multiple_allowed.pop()
        self.keys.pop()
        self.results.pop()
        self.current_index -= 1
        self._check_index_validity()

    def _check_index_validity(self):
        if self.DEBUG:
            print(f"Checking index validity: {self.current_index} in range (0, {len(self.options)})")
        assert 0 <= self.current_index < len(self.options), "Invalid index, something went wrong"

    def _is_multiple_allowed(self):
        return self.multiple_allowed[self.current_index]

    def _print_history(self):
        if not self._has_parent():
            return
        print("History:", end=" ")
        for i in range(self.current_index):
            if i > 0:
                print("->", end=" ")
            print(f"{self.keys[i]}=", end="")
            if isinstance(self.results[i], list):
                print("[" + ", ".join(self.results[i]) + "]", end=" ")
            else:
                print(self.results[i], end=" ")
        print()

    def _save_result_once(self, value):
        self.results[self.current_index] = value
        if self.DEBUG:
            print(f"Saved result: {self.keys[self.current_index]} = {value}")
            print(f"Now results: {self.results}")
        self._to_next()

    def ask(self, title=None, key=None):
        if self.quit:
            return self
        if key is not None:
            self.set_key(key)
        if title is not None:
            self.set_title(title)
        while True:
            print("\n" + "-" * 30)
            print(f"Step {self.current_index + 1}: ", self.menu_title[self.current_index])
            print("-" * 30)
            self._print_history()
            for idx, option in enumerate(self.options[self.current_index]):
                print(f"[{idx}]: {option['name']}")

            print("[q]: Quit")
            if self._has_parent():
                print("[r]: Return to parent")
            if self._is_multiple_allowed():
                print("[*]: Enter indices (e.g., 0 1,2) to select multiple")

            choice = input("Choose an option: ").strip().lower()

            if choice == 'q':
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
                        return self.get_all_results() if self.has_ended() else self
                    continue
                except Exception as e:
                    print("Invalid input format. Please enter indices separated by space or comma.")
                    continue
            elif choice.isdigit() and 0 <= int(choice) < len(self.options[self.current_index]):
                self._save_result_once(self.options[self.current_index][int(choice)]['name'])
                if self._is_new():
                    return self.get_all_results() if self.has_ended() else self
                continue
            else:
                print("Invalid input. Please try again.")

    def _reset(self):
        self.current_index = 0

    def get_all_results(self):
        self.end = True
        if self.DEBUG:
            print(f"End Selection")
        if self.quit:
            return None
        self._remove_last()
        results = dict(zip(self.keys, self.results))
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
                return self.ask()
            elif confirm == 'l':
                return self.ask()
            else:
                print("Invalid input. Please enter y/n/r")

