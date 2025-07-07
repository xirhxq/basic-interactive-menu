# Basic Interactive Menu

A simple Python-based interactive menu system for building command-line applications with nested menus and selection workflows.

## Overview

This project provides a lightweight framework for creating interactive command-line interfaces with:
- Multi-level menu navigation
- Single and multiple selection support
- Parent-child menu relationships
- Dynamic class instantiation
- Clean, chainable API

The example implementation demonstrates selecting a data file, processing class, and visualization types to generate charts.

## File Structure

```plain
.
 ├── README.md
 ├── interactive_menu.py # Core menu system implementation
 ├── main.py # Application entry point
 └── classes/ # Data processing classes 
  ├── A.py # Class A implementation
  ├── B.py # Class B implementation 
  ├── C.py # Class C implementation 
  └── classes.py # Class module exports
```

### Key Files

1. **`interactive_menu.py`** - Menu core:
   - `InteractiveMenu` class with chainable methods
   - Menu navigation and selection handling
   - Single/multiple selection support
   - Parent-child menu relationships

2. **`main.py`** - Application entry:
   - Three-level menu implementation
   - File → Class → Chart type selection
   - Dynamic class instantiation
   - Process restart handling

3. **`classes/`** - Data processors:
   - Modular class implementations
   - Dynamic loading via `getattr()`
   - Example classes A, B, C

## Example Usage

```bash
python main.py
```

### Sample Workflow

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

Selected chart types: Line Chart, Scatter Plot

Instantiating class...
Class B with {'file': 'data1.csv', 'types': ['Line Chart', 'Scatter Plot']}

Successfully created instance: <classes.B.B object at 0x7f9a5c0b7d60>

Would you like to start over? (y/n): n

Exiting application. Goodbye!
```

## Customization

1. **Add new processors**:
   - Create new class files in `classes/`
   - Implement with [__init__(self, **kwargs)](file:///Users/xirhxq/PycharmProjects/basic-interactive-menu/interactive_menu.py#L1-L6)
   - Import in [classes/classes.py](file:///Users/xirhxq/PycharmProjects/basic-interactive-menu/classes/classes.py)

2. **Modify menu options**:
   - Edit options in [main.py](file:///Users/xirhxq/PycharmProjects/basic-interactive-menu/main.py):
   
    ```python
    .add_option("New Option")
    .add_options(["Option 1", "Option 2"])
    ```

3. **Extend workflow**:
   - Add new menu levels in [main.py](file:///Users/xirhxq/PycharmProjects/basic-interactive-menu/main.py)
   - Adjust parent-child relationships
   - Modify result handling logic

The framework provides a flexible foundation for various command-line selection workflows beyond the example implementation.
