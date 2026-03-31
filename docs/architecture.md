# basic-interactive-menu Architecture

**Version:** 0.3.0
**Last Updated:** 2026-03-31

## System Overview

`basic-interactive-menu` is a zero-dependency Python library for building interactive CLI menus. The architecture follows a modular design with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                      User Application                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    InteractiveMenu (Facade)                 │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────┐ │
│  │ Search  │ │ Groups  │ │ Themes  │ │ Config  │ │History│ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └──────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Terminal I/O                            │
│                     (stdin/stdout)                           │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### InteractiveMenu (Main Facade)

The primary interface for users. Orchestrates all other components.

**Responsibilities:**
- Menu configuration (title, options, key)
- User input handling
- Result storage and retrieval
- Component coordination

**Key Methods:**
```python
set_title(title: str) -> InteractiveMenu
add_option(name: str, shortcut: str | None = None) -> InteractiveMenu
add_group(name: str, options: List[str]) -> InteractiveMenu
set_theme(theme: str | MenuTheme) -> InteractiveMenu
enable_search() -> InteractiveMenu
ask() -> InteractiveMenu
get_result(key: str) -> Any
get_all_results() -> Dict[str, Any]
```

### SearchEngine

Provides fuzzy search capabilities for filtering menu options.

**Architecture:**
```
┌──────────────┐     build      ┌────────────────┐
│   Options    │ ──────────────► │ Character Index│
│   ["A","B"]  │                │  char → [idx]  │
└──────────────┘                 └────────────────┘
                                         │
                                         ▼
┌──────────────┐     search     ┌────────────────┐
│    Query     │ ──────────────► │ Filtered Indices│
│    "py"      │                │    [0, 2]      │
└──────────────┘                 └────────────────┘
```

**Data Flow:**
1. `__init__`: Build character index from options
2. `search(query)`: Use index to find candidates, validate with substring match
3. `get_matches_summary`: Generate human-readable result summary

### GroupRenderer

Manages option grouping for visual organization.

**Architecture:**
```
┌─────────────────────────────────────┐
│          GroupRenderer              │
│  ┌─────────────────────────────┐   │
│  │ OptionGroup[]                │   │
│  │  ┌─────────────────────┐    │   │
│  │  │ name: "Languages"   │    │   │
│  │  │ options: ["Py", "Go"]│    │   │
│  │  │ collapsed: False     │    │   │
│  │  └─────────────────────┘    │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Key Methods:**
```python
add_group(name: str, options: List[str], collapsed: bool = False)
get_all_options() -> List[str]
get_global_index(group_idx: int, option_idx: int) -> int
render_header(group: OptionGroup) -> str
render_option(global_idx: int, option: str, shortcut: str | None) -> str
```

### MenuTheme

Handles visual styling with ANSI color codes.

**Theme Structure:**
```
MenuTheme
├── name: str
├── border_style: str ("-", "=", "*")
├── border_color: Colors
├── title_color: Colors
├── option_color: Colors
├── shortcut_color: Colors
├── selected_color: Colors
└── prompt_color: Colors
```

**Built-in Themes:**
- `default` - Standard styling
- `minimal` - No borders, basic colors
- `bold` - Bold text throughout
- `dim` - Dimmed text for subtle look
- `colorful` - Full rainbow colors
- `hacker` - Green on black (Matrix style)

### MenuConfig

Loads menu definitions from JSON/YAML files.

**Config Structure:**
```json
{
  "title": "Menu Title",
  "key": "result_key",
  "multiple": false,
  "theme": "default",
  "options": [
    {"name": "Option A", "shortcut": "a"},
    "Option B"
  ],
  "groups": [
    {"name": "Group 1", "options": ["A", "B"]}
  ]
}
```

## Data Flow Diagrams

### Menu Creation Flow

```
┌─────────┐   set_title()   ┌──────────────┐
│  User   │ ──────────────► │ InteractiveMenu│
└─────────┘                └──────────────┘
     │                              │
     │ add_option("A")              │
     ├─────────────────────────────► │
     │                              │ Options.append()
     │ add_option("B")              │
     ├─────────────────────────────► │
     │                              │
     │ enable_search()              │ SearchEngine()
     ├─────────────────────────────► │
     │                              │
     │ ask()                        │
     ├─────────────────────────────► │
     │                              ▼
     │                      ┌─────────────┐
     │                      │  Display    │
     │                      │   Menu      │
     │                      └─────────────┘
     │                              │
     │              user input       │
     │◄─────────────────────────────┤
     │                              │
     │                      ┌─────────────┐
     │                      │   Store     │
     │                      │   Result    │
     │                      └─────────────┘
```

### Search Flow

```
┌─────────┐   press "/"     ┌──────────────┐
│  User   │ ──────────────► │ Search Mode  │
└─────────┘                └──────────────┘
     │                              │
     │ type query                   │
     ├─────────────────────────────► │
     │                              │
     │                      ┌──────────────┐
     │                      │ SearchEngine │
     │                      │  .search()   │
     │                      └──────────────┘
     │                              │
     │                              ▼
     │                      ┌──────────────┐
     │                      │ Filtered     │
     │                      │ Options      │
     │                      └──────────────┘
     │                              │
     │              display filtered   │
     │◄─────────────────────────────┘
```

### Config Loading Flow

```
┌──────────┐   from_file()   ┌──────────────┐
│   User   │ ──────────────► │ InteractiveMenu│
└──────────┘                 └──────────────┘
                                    │
                                    ▼
                           ┌──────────────┐
                           │ MenuConfig   │
                           │ .from_file() │
                           └──────────────┘
                                    │
                           ┌────────┴────────┐
                           ▼                 ▼
                    ┌──────────┐    ┌──────────┐
                    │  JSON    │    │  YAML    │
                    │  Parser  │    │  Parser  │
                    └──────────┘    └──────────┘
                           │                 │
                           └────────┬────────┘
                                    ▼
                           ┌──────────────┐
                           │  Validated   │
                           │  Config Dict │
                           └──────────────┘
                                    │
                                    ▼
                           ┌──────────────┐
                           │   Configure  │
                           │   Menu       │
                           └──────────────┘
```

## Module Dependencies

```
┌────────────────────────────────────────────────────┐
│              basic_interactive_menu                │
├────────────────────────────────────────────────────┤
│                                                    │
│  ┌────────────────┐    ┌─────────────────┐       │
│  │interactive_menu│◄───┤   __init__.py   │       │
│  └───────┬────────┘    └─────────────────┘       │
│          │                                        │
│    ┌─────┼─────┬─────┬─────┬─────┐              │
│    ▼     ▼     ▼     ▼     ▼     ▼              │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌────┐          │
│  │sea│ │gro│ │the│ │con│ │his│ │ver││          │
│  │rch│ │ups│ │mes│ │fig│ │tory│ │sion│          │
│  └───┘ └───┘ └───┘ └───┘ └───┘ └────┘          │
│                                                    │
│  All modules use only Python standard library      │
└────────────────────────────────────────────────────┘
```

## Design Principles

### 1. Zero External Dependencies

All functionality uses Python standard library only.

### 2. Fluent Chainable API

All configuration methods return `self` for method chaining.

### 3. Separation of Concerns

Each module has a single, well-defined responsibility.

### 4. Type Safety

Complete type hints enable IDE support and early error detection.

### 5. Testability

Components are designed for easy unit testing.

## Extension Points

### Adding New Features

1. **New menu property**:
   - Add to `InteractiveMenu.__init__`
   - Add setter method returning `self`
   - Add tests

2. **New renderer**:
   - Implement renderer protocol
   - Add configuration option
   - Add usage example

3. **New input handler**:
   - Extend `InteractiveMenu._get_selection()`
   - Add command handling logic
   - Add tests

### Custom Themes

```python
from basic_interactive_menu.themes import MenuTheme, Colors

custom = MenuTheme(
    name="my_theme",
    border_style="~",
    border_color=Colors.CYAN,
    title_color=Colors.BOLD,
    option_color=Colors.BRIGHT_YELLOW
)
```

## Performance Characteristics

| Component | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| SearchEngine.search() | O(n × m) | O(n) |
| SearchEngine.__init__() | O(n × k) | O(n × k) |
| GroupRenderer.get_all_options() | O(n) | O(n) |
| MenuConfig.from_file() | O(n) | O(n) |

Where:
- n = number of options
- m = query length
- k = average option length

## Security Considerations

1. **Input sanitization**: All user input is validated
2. **No code execution**: Config files define data only
3. **No file system access**: Except explicitly requested config files
4. **No network operations**: Zero external dependencies

## Future Architecture Considerations

1. **Plugin system**: Allow custom renderers/handlers
2. **Async support**: For async application integration
3. **Internationalization**: Multi-language support
4. **Accessibility**: Screen reader compatibility
