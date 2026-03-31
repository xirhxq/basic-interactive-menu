# Building Your First Menu

This tutorial dives deeper into constructing menus with `basic-interactive-menu`. You'll learn the patterns and best practices for building effective interactive menus.

## Menu Anatomy

Every menu has several components:

```
┌────────────────────────────────────┐
│     Menu Title (set_title)         │  ← Title bar
├────────────────────────────────────┤
│ [0]: Option A                      │  ← Options with indices
│ [1/X]: Option B (shortcut: X)      │
│ [2]: Option C                      │
├────────────────────────────────────┤
│ [q]: Quit                          │  ← Built-in quit option
│ [*]: Multi-select hint             │  ← Context help
├────────────────────────────────────┤
│ Choose an option: _                │  ← Prompt
└────────────────────────────────────┘
```

## Building Blocks

### 1. Create and Configure

```python
from basic_interactive_menu import InteractiveMenu

menu = InteractiveMenu()
```

### 2. Set Title and Key

```python
menu = (
    InteractiveMenu()
    .set_title("Main Menu")      # Displayed at top
    .set_key("main_choice")      # Result identifier
)
```

**Why set a key?** The key lets you retrieve results from menus, especially useful with nested menus.

### 3. Add Options

```python
# Single option
menu.add_option("Choice A")

# Multiple options
menu.add_options(["Choice B", "Choice C", "Choice D"])

# With shortcut
menu.add_option("Exit", shortcut='x')
```

### 4. Execute and Retrieve

```python
result = (
    menu
    .ask()                    # Display menu, get input
    .get_result("main_choice") # Retrieve by key
)
```

## Common Patterns

### Pattern 1: Sequential Questions

```python
results = {}

# Question 1
results['file'] = (
    InteractiveMenu()
    .set_key("file")
    .set_title("Select file")
    .add_option("data.csv")
    .add_option("data.json")
    .ask()
    .get_result("file")
)

# Question 2
results['format'] = (
    InteractiveMenu()
    .set_key("format")
    .set_title("Select output format")
    .add_option("Table")
    .add_option("Chart")
    .ask()
    .get_result("format")
)

print(f"File: {results['file']}, Format: {results['format']}")
```

### Pattern 2: Nested Menus

```python
results = (
    InteractiveMenu()
    .set_key("category")
    .set_title("Select Category")
    .add_option("Fruits")
    .add_option("Vegetables")
    .ask()
)

# Based on first choice, show second menu
if results.get_result("category") == "Fruits":
    fruit = (
        InteractiveMenu()
        .set_key("item")
        .set_title("Select Fruit")
        .add_option("Apple")
        .add_option("Banana")
        .ask()
        .get_result("item")
    )
    print(f"You selected: {fruit}")
```

### Pattern 3: Action Menu

```python
def handle_action(action: str) -> None:
    """Handle menu action selection."""
    if action == "Create":
        print("Creating new item...")
    elif action == "Update":
        print("Updating item...")
    elif action == "Delete":
        print("Deleting item...")
    elif action == "Exit":
        print("Goodbye!")
        return

action = (
    InteractiveMenu()
    .set_key("action")
    .set_title("What would you like to do?")
    .add_option("Create", shortcut='c')
    .add_option("Update", shortcut='u')
    .add_option("Delete", shortcut='d')
    .add_option("Exit", shortcut='x')
    .ask()
    .get_result("action")
)

handle_action(action)
```

### Pattern 4: Confirmation Menu

```python
def confirm(message: str) -> bool:
    """Show a yes/no confirmation menu."""
    result = (
        InteractiveMenu()
        .set_title(message)
    .set_key("confirmed")
    .add_option("Yes", shortcut='y')
    .add_option("No", shortcut='n')
    .ask()
    .get_result("confirmed")
)
return result == "Yes"

# Usage
if confirm("Delete this file?"):
    os.remove("file.txt")
else:
    print("Cancelled")
```

### Pattern 5: Dynamic Options

```python
import os

def list_files(directory: str) -> list[str]:
    """Get list of files in directory."""
    return [f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))]

files = list_files(".")
selected = (
    InteractiveMenu()
    .set_title("Select a file")
    .set_key("file")
    .add_options(files)  # Dynamically loaded options
    .ask()
    .get_result("file")
)
print(f"Selected: {selected}")
```

## Result Management

### Single Result

```python
result = (
    InteractiveMenu()
    .set_key("choice")
    .add_option("A").add_option("B")
    .ask()
    .get_result("choice")
)
# result is a string: "A" or "B"
```

### Multiple Results

```python
results = (
    InteractiveMenu()
    .set_key("choices")
    .allow_multiple()
    .add_option("A").add_option("B").add_option("C")
    .ask()
    .get_result("choices")
)
# results is a list of strings: ["A", "C"]
```

### All Results as Dictionary

```python
all_results = (
    InteractiveMenu()
    .set_key("first")
    .add_option("X").add_option("Y")
    .ask()
    .get_all_results()
)
# all_results = {"first": "X" or "Y"}
```

## Error Handling

### Handling "Quit"

```python
result = (
    InteractiveMenu()
    .set_key("choice")
    .add_option("A")
    .add_option("B")
    .ask()
)

choice = result.get_result("choice")
if choice is None:
    print("User quit")
else:
    print(f"Selected: {choice}")
```

### Validation

```python
def get_valid_choice() -> str:
    """Get a validated menu choice."""
    while True:
        result = (
            InteractiveMenu()
            .set_key("choice")
            .add_option("Option A")
            .add_option("Option B")
            .ask()
        )

        choice = result.get_result("choice")
        if choice is not None:
            return choice

        print("You must make a selection!")
```

## Best Practices

### 1. Use Descriptive Titles

```python
# Good
.set_title("Select output format for the report")

# Less clear
.set_title("Format")
```

### 2. Group Related Options

```python
# Logical grouping
.add_option("Create New", shortcut='n')
.add_option("Open Existing", shortcut='o')
.add_option("Save", shortcut='s')
.add_option("Exit", shortcut='x')
```

### 3. Provide Shortcuts for Common Actions

```python
# Frequent actions get shortcuts
.add_option("Continue", shortcut='c')
.add_option("Retry", shortcut='r')
.add_option("Quit", shortcut='q')
```

### 4. Handle the Result Immediately

```python
# Good - result is used right away
choice = menu.ask().get_result("choice")
process_choice(choice)

# Avoid - storing for no reason
stored_choice = menu.ask().get_result("choice")
# ... 100 lines later ...
process_choice(stored_choice)
```

## Complete Example

Here's a complete CLI application using menus:

```python
#!/usr/bin/env python3
"""File manager CLI using basic-interactive-menu."""

import os
from basic_interactive_menu import InteractiveMenu


def main_menu() -> str:
    """Display main menu and return selection."""
    return (
        InteractiveMenu()
        .set_title("File Manager")
        .set_key("action")
        .add_option("List Files", shortcut='l')
        .add_option("Create Directory", shortcut='c')
        .add_option("Delete File", shortcut='d')
        .add_option("Exit", shortcut='x')
        .ask()
        .get_result("action")
    )


def list_files() -> None:
    """List files in current directory."""
    files = os.listdir(".")
    print("\nFiles:")
    for f in files:
        print(f"  - {f}")


def create_directory() -> None:
    """Create a new directory."""
    name = input("Enter directory name: ")
    if name:
        os.mkdir(name)
        print(f"Created: {name}")
    else:
        print("Cancelled")


def delete_file() -> None:
    """Delete a file."""
    files = [f for f in os.listdir(".") if os.path.isfile(f)]

    if not files:
        print("No files to delete")
        return

    filename = (
        InteractiveMenu()
        .set_title("Select file to delete")
        .set_key("file")
        .add_options(files)
        .ask()
        .get_result("file")
    )

    if filename:
        os.remove(filename)
        print(f"Deleted: {filename}")


def main() -> None:
    """Run the file manager."""
    while True:
        action = main_menu()

        if action == "List Files":
            list_files()
        elif action == "Create Directory":
            create_directory()
        elif action == "Delete File":
            delete_file()
        elif action == "Exit":
            print("Goodbye!")
            break

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
```

## What's Next?

- [Tutorial 3: Advanced Features](./03-advanced-features.md) - Search, groups, themes
- [Tutorial 4: Contributing Guide](./04-contributing-guide.md) - How to contribute
- [Tutorial 5: Writing Tests](./05-writing-tests.md) - Testing best practices
