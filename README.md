# Basic Interactive Menu

A simple Python-based interactive menu system for building command-line applications with nested menus and selection workflows.

**Unique Features Highlight**:
- 🚀 **Fluent Chainable API** - Build complex menus with intuitive method chaining
- 🔄 **Seamless Parent Menu Navigation** - Built-in `r` command for hierarchical menu traversal
- 📦 **Zero-Dependency Design** - Pure Python implementation with no external libraries
- ✅ **Selection Confirmation & Restart Workflow** - Built-in confirmation and restart capabilities

## Overview

This project provides a lightweight framework for creating interactive command-line interfaces with:
- **Chainable API** for intuitive menu building
- **Parent-child navigation** with single-key return (`r` command)
- **Pure Python implementation** requiring no third-party dependencies
- Multi-level menu navigation with selection persistence across sessions
- Single and multiple selection support

The example implementation demonstrates selecting a data file, processing class, and visualization types to generate charts.

## Usage

This is a single-file (and single-class) library. You only need the `interactive_menu.py` file to use this framework in your projects. Simply copy the file to your project directory and import it:

```python
from interactive_menu import InteractiveMenu
```

## Requirements

- **Python 3.6 or higher** (due to use of f-strings syntax)
- **Zero external dependencies** - uses only Python standard libraries

We recommend using [conda](https://docs.conda.io/en/latest/) to create a clean Python environment:

```bash
conda create -n basic-interactive-menu python=3.6
conda activate basic-interactive-menu
```

## File Structure

```plain
.
├── README.md
├── interactive_menu.py        # Core menu system implementation
├── examples/
│   ├── one_layer.py           # Single-layer menu example
│   └── three_layers.py        # Three-level menu example with dynamic class instantiation
```

### Key Files

1. **`interactive_menu.py`** - Menu core:
   - `InteractiveMenu` class with chainable methods
   - Menu navigation and selection handling
   - Single/multiple selection support
   - Parent-child menu relationships
   - Selection confirmation and restart workflow

2. **`examples/one_layer.py`** - Single-layer menu example:
   - Demonstrates basic menu creation
   - Shows simple selection workflow
   - Illustrates single option selection

3. **`examples/three_layers.py`** - Three-level menu example:
   - Demonstrates multi-level menu navigation
   - Shows dynamic class instantiation
   - Illustrates parent-child menu relationships
   - Implements complete selection workflow

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

1. **`set_key(key)`**
   Sets the result key name for this menu level
   - `key`: The key name to identify this menu's result

2. **`set_title(title_text)`**
   Sets the title for the current menu level
   - `title_text`: The title text to display

3. **`add_option(name)`**
   Adds a single option to the current menu level
   - `name`: The text to display for this option

4. **`add_options(items)`**
   Adds multiple options to the current menu level
   - `items`: A list of strings representing the options

5. **`allow_multiple()`**
   Enables multiple selection mode for the current menu level

6. **`ask(title=None, key=None)`**
   Displays the menu and gets user input
   - `title`: Optional title to override the set title
   - `key`: Optional key name to override the set key
   Returns: self for chainability

7. **`get_all_results()`**
   Gets all results from completed menu flow
   Returns: Dictionary of results if confirmed, None otherwise

8. **`has_quit()`**
   Checks if the user has quit the menu
   Returns: Boolean indicating if user quit

9. **`has_ended()`**
   Checks if the menu flow has ended
   Returns: Boolean indicating if menu flow has ended

These methods are designed to be used in a chainable fashion, allowing for fluent API style programming:

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

## Example Usage

```bash
# Run single-layer example
python examples/one_layer.py

# Run three-layer example
python examples/three_layers.py
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

Confirm selection? (y/n/r=restart/l=last): y
```

## Customization

1. **Add new processors**:
   - Create new class files in `classes/`
   - Implement with `__init__(self, **kwargs)`
   - Import in `classes/classes.py`

2. **Modify menu options**:
   - Edit options in your code:
   
    ```python
    # Create a new menu instance
    menu = InteractiveMenu()
    
    # Add a single option
    menu.add_option("New Option")
    
    # Add multiple options
    menu.add_options(["Option 1", "Option 2"])
    ```

3. **Extend workflow**:
   - Add new menu levels by calling `.ask()` multiple times
   - Adjust parent-child relationships through index management
   - Modify result handling logic in your application code

The framework provides a flexible foundation for various command-line selection workflows beyond the example implementation.