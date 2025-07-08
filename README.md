# Basic Interactive Menu

![Example, Three Layers](example_three_layers.gif)

A simple Python-based interactive menu system for building command-line applications with nested menus and selection workflows.

**Unique Features Highlight**:
- 🚀 **Fluent Chainable API** - Build complex menus with intuitive method chaining
- 🔄 **Seamless Parent Menu Navigation** - Built-in `r` command for hierarchical menu traversal
- 📦 **Zero-Dependency Design** - Pure Python implementation with no external libraries
- ✅ **Selection Confirmation & Restart Workflow** - Built-in confirmation and restart capabilities
- 🧪 **Development Package Support** - Easily installable with `setup.py` for development

## Overview

This project provides a lightweight framework for creating interactive command-line interfaces with:
- Chainable API for intuitive menu building
- Parent-child navigation with single-key return (`r` command)
- Pure Python implementation requiring no third-party dependencies
- Multi-level menu navigation with selection persistence across sessions
- Single and multiple selection support

The core implementation resides in a single file: [interactive_menu.py](interactive_menu.py)

## Requirements

- **Python 3.6 or higher** (due to use of f-strings syntax)
- **Zero external dependencies** - uses only Python standard libraries

We recommend using [conda](https://docs.conda.io/en/latest/) to create a clean Python environment:

```bash
conda create -n basic-interactive-menu python=3.6+
conda activate basic-interactive-menu
```

## Getting Started

### Installation

For development, we recommend installing the package in editable mode:

```bash
# Install the package in development mode
pip install -e .
```

To uninstall:

```bash
pip uninstall basic-interactive-menu
 ```

This allows you to use standard Python imports in all project files.

### File Structure

```plain
.
├── README.md
├── setup.py              # Development package configuration
├── interactive_menu.py        # Core menu system implementation
├── examples/
│   ├── one_layer.py           # Single-layer menu example
│   └── three_layers.py        # Three-level menu example
└── tests/
    ├── test_one_layer.py      # Unit tests for one-layer menu
    └── test_three_layers.py   # Unit tests for three-layer menu
```

### Example Usage

```bash
# Run single-layer example
python examples/one_layer.py

# Run three-layer example
python examples/three_layers.py

# Run tests
python -m unittest tests.test_one_layer.py
python -m unittest tests.test_three_layers.py

# Run all tests
python -m unittest discover tests
```

### Sample Output

```plain
------------------------------
Step 1: Select a Data File
------------------------------
[0]: data1.csv
[1]: data2.json
[2]: data3.txt
[q]: Quit
Choose an option: 0

Selected file: data1.csv

------------------------------
Step 2: Select a Class
------------------------------
[0]: A
[1]: B
[2]: C
[q]: Quit
[r]: Return to parent
Choose an option: 1

Selected class: B

------------------------------
Step 3: Select Chart Types
------------------------------
[0]: Line Chart
[1]: Bar Chart
[2]: Scatter Plot
[3]: Pie Chart
[q]: Quit
[r]: Return to parent
[*]: Enter indices (e.g., 0 1,2) to select multiple
Choose an option: 0,2

Current selections:
file: data1.csv
class_name: B
chart_type_list: ['Line Chart', 'Scatter Plot']

Confirm selection? (y/n/r=restart): y
```

## API Documentation

### `InteractiveMenu` Class

#### Initialization
```python
def __init__(self, multiple_allowed=False, debug=False):
    """Initialize an InteractiveMenu instance."""
```
- `multiple_allowed`: Whether multiple selections are allowed (default: False)
- `debug`: Enable debug output (default: False)

#### Core Methods

1. **`set_key(key)`** - Sets the result key name
2. **`set_title(title_text)`** - Sets the menu title
3. **`add_option(name)`** - Adds a single option
4. **`add_options(items)`** - Adds multiple options
5. **`allow_multiple()`** - Enables multiple selection mode
6. **`ask(title=None, key=None)`** - Displays menu and gets user input
7. **`get_all_results()`** - Gets all results with confirmation

## Customization Guide

### Integrating into Your Project

1. **Install the package in development mode**:
```bash
pip install -e .
```

2. **Import the module**:
```python
from basic_interactive_menu import InteractiveMenu
```

3. **Create your menu workflow**:
```python
results = (
    InteractiveMenu()
    .add_option("Apple")
    .add_option("Banana")
    .add_options(["Orange", "Grapes"])
    .ask("Select a Fruit", "selection")
    .get_all_results()
)
```

4. **Implement your classes**:
Ensure classes implement the `__init__(self, **kwargs)` interface:

```python
class MyCustomClass:
    def __init__(self, **kwargs):
        print(f'Class initialized with {kwargs}')
```

### Extending Functionality

- Add custom validation in menu methods
- Extend the `InteractiveMenu` class for specialized behavior
- Implement your own result processing logic

## Contributing

We welcome contributions to improve this project! Please consider:

1. **Testing** - Run the examples and tests, and report any bugs or unexpected behavior
2. **Enhancements** - Suggest or implement improvements to the core functionality
3. **Documentation** - Help improve the clarity and completeness of documentation
4. **Examples** - Add new example implementations demonstrating different use cases
5. **Packaging** - Improve the development package configuration in setup.py

To contribute:
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Submit a pull request with detailed explanation

When contributing, please ensure:
- Your changes maintain backward compatibility
- New functionality includes corresponding test cases
- Documentation is updated to reflect changes
- Code follows existing style guidelines

Your contributions help make this library better for everyone!

## License

MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

We would like to express our gratitude to the following AI tools and models that contributed to this project:

- **Tongyi Lingma**: For generating code & commit messages, designing architecture, and improving development efficiency
- **Qwen3**: For creating clear documentation and enhancing code readability
- **DeepSeek-R1**: For optimizing implementation logic and providing technical guidance

These AI assistants have significantly accelerated the development process and helped maintain high code quality standards.
