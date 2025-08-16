from typing import List, Dict, Any, Optional, Union

class InteractiveMenu:
    DEFAULT_TITLE: str = "Choose an option"
    DEFAULT_MULTIPLE_ALLOWED: bool = False
    DEBUG: bool = False
    
    def __init__(self, multiple_allowed: bool = False, debug: bool = False) -> None:
        self.current_index: int = 0
        self.options: List[List[Dict[str, str]]] = [[]]
        self.menu_title: List[str] = [self.DEFAULT_TITLE]
        self.multiple_allowed: List[bool] = [multiple_allowed]
        self.DEBUG: bool = debug
        self.keys: List[Optional[str]] = [None]
        self.results: List[Optional[Union[str, List[str]]]] = [None]
        self.quit: bool = False
        self.end: bool = False

    def has_quit(self) -> bool:
        return self.quit

    def has_ended(self) -> bool:
        if self.DEBUG:
            print("Has ended" if self.end else "Not ended")
        return self.end

    def set_key(self, key: str) -> 'InteractiveMenu':
        if self.quit:
            return self
        self.keys[self.current_index] = key
        return self

    def set_title(self, title_text: str) -> 'InteractiveMenu':
        if self.quit:
            return self
        self.menu_title[self.current_index] = title_text
        return self

    def add_option(self, name: str) -> 'InteractiveMenu':
        if self.quit:
            return self
        self.options[self.current_index].append({'name': name})
        if self.DEBUG:
            print(f"Added option: {name}")
        return self

    def add_options(self, items: List[str]) -> 'InteractiveMenu':
        if self.quit:
            return self
        for item in items:
            self.add_option(item)
        if self.DEBUG:
            print(f"Added options: {items}")
        return self

    def allow_multiple(self) -> 'InteractiveMenu':
        if self.quit:
            return self
        self.multiple_allowed[self.current_index] = True
        if self.DEBUG:
            print(f"Allow multiple: {self.multiple_allowed[self.current_index]}")
        return self

    def _has_parent(self) -> bool:
        if self.DEBUG:
            print(f"Current index: {self.current_index}")
        return self.current_index > 0

    def _to_parent(self) -> None:
        if self.DEBUG:
            print(f"Index from {self.current_index} to", end=" ")
        self.current_index -= 1
        if self.DEBUG:
            print(f"{self.current_index}")
        self._check_index_validity()

    def _is_new(self) -> bool:
        return len(self.options[self.current_index]) == 0

    def _need_new(self) -> bool:
        return self.current_index >= len(self.options)

    def _is_last(self) -> bool:
        if self.DEBUG:
            print(f"Is last: {self.current_index} == {len(self.options) - 1}")
        return self.current_index == len(self.options) - 1

    def _to_next(self) -> None:
        self.current_index += 1
        if self._need_new():
            self.options.append([])
            self.menu_title.append(self.DEFAULT_TITLE)
            self.multiple_allowed.append(self.DEFAULT_MULTIPLE_ALLOWED)
            self.keys.append(None)
            self.results.append(None)
        self._check_index_validity()

    def _remove_last(self) -> None:
        self.options.pop()
        self.menu_title.pop()
        self.multiple_allowed.pop()
        self.keys.pop()
        self.results.pop()
        self.current_index -= 1
        self._check_index_validity()

    def _check_index_validity(self) -> None:
        if self.DEBUG:
            print(f"Checking index validity: {self.current_index} in range (0, {len(self.options)})")
        assert 0 <= self.current_index < len(self.options), "Invalid index, something went wrong"

    def _is_multiple_allowed(self) -> bool:
        return self.multiple_allowed[self.current_index]

    def _print_history(self) -> None:
        if not self._has_parent():
            return
        print("History:", end=" ")
        for i in range(self.current_index):
            if i > 0:
                print("->", end=" ")
            key = self.keys[i]
            result = self.results[i]
            if key is not None:
                print(f"{key}=", end="")
            if isinstance(result, list):
                print("[" + ", ".join(result) + "]", end=" ")
            elif result is not None:
                print(result, end=" ")
        print()

    def _save_result_once(self, value: Union[str, List[str]]) -> None:
        self.results[self.current_index] = value
        if self.DEBUG:
            print(f"Saved result: {self.keys[self.current_index]} = {value}")
            print(f"Now results: {self.results}")
        self._to_next()

    def ask(self, title: Optional[str] = None, key: Optional[str] = None) -> 'InteractiveMenu':
        # If this is a restart, we need to reset the state
        if self.end and self.current_index == 0 and len(self.options[0]) == 0:
            # This is a restart, reset everything
            self.end = False
            
        if self.DEBUG:
            print(f"Asking with ended {self.end} and quit {self.quit}")
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
                        return self
                    continue
                except Exception as e:
                    print("Invalid input format. Please enter indices separated by space or comma.")
                    continue
            elif choice.isdigit() and 0 <= int(choice) < len(self.options[self.current_index]):
                self._save_result_once(self.options[self.current_index][int(choice)]['name'])
                if self._is_new():
                    return self
                continue
            else:
                print("Invalid input. Please try again.")

    def _reset(self) -> None:
        self.current_index = 0

    def get_all_results(self) -> Optional[Union[Dict[str, Any], 'InteractiveMenu']]:
        if self.DEBUG:
            print(f"Get all results")
        if self.quit:
            if self.DEBUG:
                print("Quit")
            return None
        if not self.end:
            self.end = True
            # Only remove last if we have more than one level and it's empty
            if len(self.options) > 1 and len(self.options[-1]) == 0:
                self._remove_last()
            # Filter out None keys and create a clean dictionary
            results: Dict[str, Any] = {}
            # Use all levels that have keys and results
            for i in range(len(self.keys)):
                key = self.keys[i]
                result = self.results[i]
                if key is not None and result is not None:
                    results[key] = result
            
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
                    # For restart, we return self to allow building a new menu
                    return self
                elif confirm == 'l':
                    # For last, we also return self to allow building a new menu
                    return self
                else:
                    print("Invalid input. Please enter y/n/r")
        else:
            # This is a restart or last option, so we need to ask again
            # Return self to allow continuing the chain
            return self

