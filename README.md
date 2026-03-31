# Basic Interactive Menu

![Version](https://img.shields.io/badge/version-0.3.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Tests](https://img.shields.io/badge/tests-127%20passing-brightgreen)

A simple Python-based interactive menu system for building command-line applications with nested menus and selection workflows.

## Features

- 🚀 **Fluent Chainable API** - Build complex menus with intuitive method chaining
- ⌨️ **Keyboard Shortcuts** - Single-character shortcuts for quick selection
- 🔍 **Built-in Search** - Real-time search to filter menu options
- 📂 **Option Groups** - Organize options into collapsible groups
- 🎨 **Theme System** - Built-in themes and custom styling support
- 📁 **Config File Support** - Define menus from JSON or YAML files
- 🔄 **Seamless Parent Menu Navigation** - Built-in `r` command for hierarchical menu traversal
- 📦 **Zero-Dependency Design** - Pure Python implementation with no external libraries
- ✅ **Selection Confirmation & Restart Workflow** - Built-in confirmation and restart capabilities
- 🧪 **Comprehensive Testing** - 127 tests with full coverage
- 📝 **Full Type Hints** - Complete type annotations for IDE support

## Installation

```bash
pip install basic-interactive-menu
```

Or for development:

```bash
git clone https://github.com/xirhxq/basic-interactive-menu.git
cd basic-interactive-menu
pip install -e .
```

## Quick Start

### Basic Usage

```python
from basic_interactive_menu import InteractiveMenu

results = (
    InteractiveMenu()
    .set_title("Select a Fruit")
    .set_key("fruit")
    .add_option("Apple")
    .add_option("Banana")
    .add_options(["Orange", "Grapes"])
    .ask()
    .get_all_results()
)

print(f"You selected: {results['fruit']}")
```

### Keyboard Shortcuts

```python
from basic_interactive_menu import InteractiveMenu

menu = InteractiveMenu()

result = (
    menu
    .set_title("Select Action")
    .set_key("action")
    # Explicit shortcuts
    .add_option("Exit", shortcut='x')
    .add_option("Continue", shortcut='c')
    # Auto-generated shortcuts
    .add_option("Help")
    .add_option("Settings")
    .ask()
    .get_all_results()
)
```

Menu displays shortcuts as:
```
------------------------------
Step 1:  Select Action
------------------------------
[0/X]: Exit
[1/C]: Continue
[2/H]: Help
[3/S]: Settings
[q]: Quit
Choose an option: x
```

### Config File Support

Create a `menu.json`:

```json
{
  "title": "Select Programming Language",
  "key": "language",
  "multiple": true,
  "options": [
    {"name": "Python", "shortcut": "p"},
    {"name": "JavaScript", "shortcut": "j"},
    {"name": "Go", "shortcut": "g"},
    "TypeScript",
    "Java"
  ]
}
```

Then load it:

```python
from basic_interactive_menu import InteractiveMenu

menu = InteractiveMenu.from_file("menu.json")
results = menu.ask().get_all_results()
```

### Search

Enable search to filter options in real-time:

```python
from basic_interactive_menu import InteractiveMenu

results = (
    InteractiveMenu()
    .set_title("Select Programming Language")
    .set_key("language")
    .enable_search()  # Enable search functionality
    .add_option("Python")
    .add_option("JavaScript")
    .add_option("TypeScript")
    .add_option("Go")
    .add_option("Rust")
    .ask()
    .get_all_results()
)
```

Press `/` to enter search mode, then type to filter options.

### Option Groups

Organize options into collapsible groups:

```python
from basic_interactive_menu import InteractiveMenu

results = (
    InteractiveMenu()
    .set_title("Select Tool")
    .set_key("tool")
    # Add a group
    .add_group("Languages", ["Python", "JavaScript", "Go"])
    # Add another group (collapsed by default)
    .add_group("Databases", ["PostgreSQL", "MongoDB", "Redis"], collapsed=True)
    # Add individual options
    .add_option("Other")
    .ask()
    .get_all_results()
)
```

### Themes

Customize the visual appearance with built-in themes:

```python
from basic_interactive_menu import InteractiveMenu

results = (
    InteractiveMenu()
    .set_title("Hacker Menu")
    .set_theme("hacker")  # Built-in themes: default, minimal, bold, dim, colorful, hacker
    .add_option("Initiate Hack")
    .add_option("Scan Network")
    .add_option("Cover Tracks")
    .ask()
    .get_all_results()
)
```

Or create a custom theme:

```python
from basic_interactive_menu import InteractiveMenu, MenuTheme
from basic_interactive_menu.themes import Colors

custom_theme = MenuTheme(
    name="custom",
    border_style="=",
    border_color=Colors.CYAN,
    title_color=Colors.BOLD,
    option_color=Colors.BRIGHT_GREEN,
)

results = (
    InteractiveMenu()
    .set_title("Custom Themed Menu")
    .set_theme(custom_theme)
    .add_option("Option A")
    .add_option("Option B")
    .ask()
    .get_all_results()
)
```

### Multiple Selection

```python
results = (
    InteractiveMenu()
    .set_title("Select Features")
    .set_key("features")
    .add_option("Feature A")
    .add_option("Feature B")
    .add_option("Feature C")
    .allow_multiple()  # Enable multiple selection
    .ask()
    .get_all_results()
)
```

### Nested Menus

```python
results = (
    InteractiveMenu()
    .set_key("file").add_option("data1.csv").add_option("data2.json").ask()
    .set_key("class").add_option("A").add_option("B").add_option("C").ask()
    .set_key("charts").allow_multiple()
        .add_option("Line Chart")
        .add_option("Bar Chart")
        .add_option("Scatter Plot")
        .ask()
    .get_all_results()
)
```

## API Documentation

### `InteractiveMenu` Class

#### Initialization
```python
InteractiveMenu(multiple_allowed=False, debug=False)
```
- `multiple_allowed`: Whether multiple selections are allowed by default
- `debug`: Enable debug output

#### Core Methods

| Method | Description |
|--------|-------------|
| `set_key(key)` | Set the result key name |
| `set_title(title)` | Set the menu title |
| `add_option(name, shortcut=None)` | Add a single option with optional shortcut |
| `add_options(items)` | Add multiple options |
| `allow_multiple()` | Enable multiple selection mode |
| `ask(title=None, key=None)` | Display menu and get user input |
| `get_all_results()` | Get all results with confirmation |

#### Class Methods

| Method | Description |
|--------|-------------|
| `InteractiveMenu.from_file(path)` | Create menu from JSON/YAML config file |

### `MenuConfig` Class

Configuration loader for menu definitions from files.

```python
from basic_interactive_menu import MenuConfig

# Load and validate config
config = MenuConfig.from_file("menu.json")
MenuConfig.validate_config(config)
```

## Examples

```bash
# Run examples
python examples/one_layer.py
python examples/three_layers.py
python examples/nested_with_confirmation.py
python examples/keyboard_shortcuts.py
python examples/from_config.py
python examples/search_demo.py
python examples/groups_demo.py
python examples/themes_demo.py

# Run tests
python -m unittest discover tests
```

## Configuration File Format

### JSON Format

```json
{
  "title": "Menu Title",
  "key": "result_key",
  "multiple": false,
  "debug": false,
  "options": [
    {"name": "Option A", "shortcut": "a"},
    {"name": "Option B", "shortcut": "b"},
    "Option C"
  ]
}
```

### YAML Format (optional, requires pyyaml)

```yaml
title: Menu Title
key: result_key
multiple: false
debug: false
options:
  - name: Option A
    shortcut: a
  - name: Option B
    shortcut: b
  - Option C
```

## Requirements

- **Python 3.8 or higher**
- **Zero external dependencies** for core functionality
- **PyYAML** (optional, for YAML config support)

```bash
# Optional: Install PyYAML for config file support
pip install pyyaml
```

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

Please ensure:
- All tests pass
- New features include tests
- Documentation is updated
- Code follows existing style

## License

MIT License - see the [LICENSE](LICENSE) file for details

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.
