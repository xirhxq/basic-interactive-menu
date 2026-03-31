# Getting Started with basic-interactive-menu

Welcome to `basic-interactive-menu`! This tutorial will help you get started with building interactive command-line menus in Python.

## What is basic-interactive-menu?

A zero-dependency Python library for creating beautiful, interactive terminal menus with a clean chainable API.

**Key Features:**
- 🚀 Fluent chainable API
- ⌨️ Keyboard shortcuts
- 🔍 Built-in search
- 📂 Option groups
- 🎨 Themes
- 📦 Zero dependencies

## Installation

```bash
pip install basic-interactive-menu
```

That's it! No external dependencies required.

## Your First Menu

Let's create a simple menu:

```python
from basic_interactive_menu import InteractiveMenu

result = (
    InteractiveMenu()
    .set_title("What's your favorite fruit?")
    .set_key("fruit")
    .add_option("Apple")
    .add_option("Banana")
    .add_option("Orange")
    .ask()
    .get_result("fruit")
)

print(f"You selected: {result}")
```

**Output:**
```
------------------------------
What's your favorite fruit?
------------------------------
[0]: Apple
[1]: Banana
[2]: Orange
[q]: Quit

Choose an option: 0
You selected: Apple
```

## Understanding the API

The fluent API chains methods together:

1. `InteractiveMenu()` - Create a new menu
2. `.set_title("...")` - Set the display title
3. `.set_key("fruit")` - Name for storing the result
4. `.add_option("...")` - Add menu options
5. `.ask()` - Display menu and get user input
6. `.get_result("fruit")` - Retrieve the result by key

## Multiple Selection

Enable multiple selections:

```python
results = (
    InteractiveMenu()
    .set_title("Select your toppings")
    .set_key("toppings")
    .allow_multiple()  # Enable multiple selection
    .add_option("Cheese")
    .add_option("Pepperoni")
    .add_option("Mushrooms")
    .ask()
    .get_result("toppings")
)

print(f"You selected: {', '.join(results)}")
```

**Output:**
```
------------------------------
Select your toppings
------------------------------
[0]: Cheese
[1]: Pepperoni
[2]: Mushrooms
[q]: Quit
[*]: Enter indices (e.g., 0 1,2) to select multiple

Choose an option: 0,2
You selected: Cheese, Mushrooms
```

## Keyboard Shortcuts

Add single-character shortcuts for quick selection:

```python
result = (
    InteractiveMenu()
    .set_title("Select Action")
    .set_key("action")
    .add_option("Exit", shortcut='x')
    .add_option("Continue", shortcut='c')
    .add_option("Help")
    .add_option("Settings")
    .ask()
    .get_result("action")
)
```

**Output:**
```
------------------------------
Select Action
------------------------------
[0/X]: Exit
[1/C]: Continue
[2/H]: Help
[3/S]: Settings
[q]: Quit

Choose an option: x
```

Shortcuts are auto-generated from option names if not specified.

## Loading from Config File

Define your menu in JSON:

**menu.json:**
```json
{
  "title": "Select Programming Language",
  "key": "language",
  "options": [
    {"name": "Python", "shortcut": "p"},
    {"name": "JavaScript", "shortcut": "j"},
    "TypeScript",
    "Go"
  ]
}
```

**Python:**
```python
from basic_interactive_menu import InteractiveMenu

menu = InteractiveMenu.from_file("menu.json")
result = menu.ask().get_result("language")
print(f"You chose: {result}")
```

## What's Next?

- [Tutorial 2: Building Your First Menu](./02-building-your-first-menu.md) - Deep dive into menu construction
- [Tutorial 3: Advanced Features](./03-advanced-features.md) - Search, groups, themes
- [Tutorial 4: Contributing Guide](./04-contributing-guide.md) - How to contribute
- [Tutorial 5: Writing Tests](./05-writing-tests.md) - Testing best practices

## Quick Reference

| Method | Description |
|--------|-------------|
| `set_title(title)` | Set menu title |
| `set_key(key)` | Set result key name |
| `add_option(name, shortcut)` | Add a single option |
| `add_options(list)` | Add multiple options |
| `allow_multiple()` | Enable multiple selection |
| `enable_search()` | Enable search mode |
| `add_group(name, options)` | Add option group |
| `set_theme(theme)` | Set visual theme |
| `ask()` | Display menu and get input |
| `get_result(key)` | Get result by key |
| `get_all_results()` | Get all results as dict |

## Getting Help

- GitHub: [xirhxq/basic-interactive-menu](https://github.com/xirhxq/basic-interactive-menu)
- Issues: Report bugs and request features
- Documentation: See `/docs` folder

Happy coding! 🎉
