# Advanced Features

This tutorial covers the advanced features of `basic-interactive-menu`: search, option groups, and themes.

## Search

Enable search to help users find options quickly in large menus.

### Basic Search

```python
from basic_interactive_menu import InteractiveMenu

result = (
    InteractiveMenu()
    .set_title("Select Programming Language")
    .set_key("language")
    .enable_search()  # Enable search functionality
    .add_option("Python")
    .add_option("JavaScript")
    .add_option("TypeScript")
    .add_option("Go")
    .add_option("Rust")
    .add_option("Java")
    .add_option("C++")
    .add_option("Ruby")
    .add_option("PHP")
    .ask()
    .get_result("language")
)
```

**Usage:**
1. Press `/` to enter search mode
2. Type your query (e.g., "py" to find Python)
3. Matching options are filtered
4. Press `/` again or `Esc` to exit search

### Search Algorithm

The search uses:
- **Character indexing** for fast lookups (O(1) per character)
- **Case-insensitive** matching
- **Substring** matching

```python
# Searching for "py" matches:
- "Python"      ✓ (contains "py")
- "TypeScript"  ✓ (contains "py")
- "Ruby"        ✗ (no "py")
```

### When to Use Search

**Good for menus with 10+ options:**

```python
# Large menu - search helps!
languages = [
    "Python", "JavaScript", "TypeScript", "Go", "Rust",
    "Java", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin",
    "Scala", "Haskell", "Lua", "R", "Julia"
]

result = (
    InteractiveMenu()
    .set_title("Select Language")
    .enable_search()
    .add_options(languages)
    .ask()
    .get_result("language")
)
```

**Not needed for small menus:**

```python
# Small menu - search is overkill
result = (
    InteractiveMenu()
    .set_title("Select Format")
    .add_option("JSON")
    .add_option("XML")
    .add_option("CSV")
    .ask()
    .get_result("format")
)
```

## Option Groups

Organize related options into visual groups.

### Basic Groups

```python
from basic_interactive_menu import InteractiveMenu

result = (
    InteractiveMenu()
    .set_title("Select Tool")
    .set_key("tool")
    .add_group("Programming Languages", [
        "Python",
        "JavaScript",
        "Go"
    ])
    .add_group("Databases", [
        "PostgreSQL",
        "MongoDB",
        "Redis"
    ])
    .add_option("Other")
    .ask()
    .get_result("tool")
)
```

**Output:**
```
------------------------------
Select Tool
------------------------------
Programming Languages:
  [0]: Python
  [1]: JavaScript
  [2]: Go

Databases:
  [3]: PostgreSQL
  [4]: MongoDB
  [5]: Redis

Other:
  [6]: Other

[q]: Quit
```

### Collapsed Groups

Hide options until the user wants to see them:

```python
result = (
    InteractiveMenu()
    .set_title("Select Configuration")
    .set_key("config")
    .add_group("Common", [
        "Debug",
        "Release"
    ])
    .add_group("Advanced", [
        "Profiling",
        "Memory Tracking",
        "Custom Allocator"
    ], collapsed=True)  # Hidden by default
    .ask()
    .get_result("config")
)
```

**When to use collapsed groups:**
- Advanced/rarely-used options
- Options that might overwhelm users
- Optional or experimental features

### Mixing Groups and Individual Options

```python
result = (
    InteractiveMenu()
    .set_title("Git Action")
    .set_key("action")
    .add_group("Common", [
        "Commit",
        "Push",
        "Pull"
    ])
    .add_group("Branching", [
        "Create Branch",
        "Switch Branch",
        "Merge Branch"
    ], collapsed=True)
    .add_option("Help")  # Individual option
    .ask()
    .get_result("action")
)
```

## Themes

Customize the visual appearance of your menus.

### Built-in Themes

```python
from basic_interactive_menu import InteractiveMenu

# Available themes: default, minimal, bold, dim, colorful, hacker

result = (
    InteractiveMenu()
    .set_title("Hacker Menu")
    .set_theme("hacker")  # Matrix-style green on black
    .add_option("Initiate Hack")
    .add_option("Scan Network")
    .add_option("Cover Tracks")
    .ask()
    .get_result("action")
)
```

**Theme Preview:**

| Theme | Description |
|-------|-------------|
| `default` | Standard styling with hyphens |
| `minimal` | No borders, basic colors |
| `bold` | Bold text throughout |
| `dim` | Dimmed, subtle appearance |
| `colorful` | Full rainbow colors |
| `hacker` | Green on black (Matrix) |

### Custom Themes

Create your own theme:

```python
from basic_interactive_menu import InteractiveMenu
from basic_interactive_menu.themes import MenuTheme, Colors

custom_theme = MenuTheme(
    name="my_theme",
    border_style="=",           # Use equals for border
    border_color=Colors.CYAN,   # Cyan borders
    title_color=Colors.BOLD,    # Bold title
    option_color=Colors.BRIGHT_GREEN,  # Bright green options
    shortcut_color=Colors.BRIGHT_YELLOW,  # Yellow shortcuts
    selected_color=Colors.BRIGHT_BLUE,   # Blue when selected
    prompt_color=Colors.RESET   # Reset for prompt
)

result = (
    InteractiveMenu()
    .set_title("Custom Themed Menu")
    .set_theme(custom_theme)
    .add_option("Option A")
    .add_option("Option B")
    .ask()
    .get_result("choice")
)
```

### Available Colors

```python
from basic_interactive_menu.themes import Colors

# Basic colors
Colors.BLACK
Colors.RED
Colors.GREEN
Colors.YELLOW
Colors.BLUE
Colors.MAGENTA
Colors.CYAN
Colors.WHITE

# Bright variants
Colors.BRIGHT_RED
Colors.BRIGHT_GREEN
Colors.BRIGHT_YELLOW
Colors.BRIGHT_BLUE
Colors.BRIGHT_MAGENTA
Colors.BRIGHT_CYAN
Colors.BRIGHT_WHITE

# Styles
Colors.BOLD
Colors.DIM
Colors.UNDERLINE
Colors.RESET
```

## Combining Features

### Search + Groups

```python
result = (
    InteractiveMenu()
    .set_title("Select Package")
    .set_key("package")
    .enable_search()
    .add_group("Web Frameworks", [
        "Django",
        "Flask",
        "FastAPI"
    ])
    .add_group("Data Science", [
        "NumPy",
        "Pandas",
        "Matplotlib"
    ])
    .add_group("DevOps", [
        "Docker",
        "Kubernetes",
        "Terraform"
    ])
    .ask()
    .get_result("package")
)
```

### Search + Groups + Theme

```python
result = (
    InteractiveMenu()
    .set_title("CLI Tool Selector")
    .set_key("tool")
    .set_theme("colorful")
    .enable_search()
    .add_group("Version Control", [
        "Git",
        "Mercurial",
        "SVN"
    ])
    .add_group("Build Tools", [
        "Make",
        "CMake",
        "Gradle"
    ], collapsed=True)
    .ask()
    .get_result("tool")
)
```

## Real-World Example

Here's a complete example using all advanced features:

```python
#!/usr/bin/env python3
"""DevOps CLI tool launcher."""

from basic_interactive_menu import InteractiveMenu


def main():
    """Launch DevOps tools with advanced menu."""
    result = (
        InteractiveMenu()
        .set_title("DevOps Tool Launcher")
        .set_key("tool")
        .set_theme("hacker")
        .enable_search()

        # Common actions
        .add_group("Common Actions", [
            "Deploy to Production",
            "View Logs",
            "Restart Service",
            "Run Health Check"
        ])

        # Infrastructure (collapsed)
        .add_group("Infrastructure", [
            "Provision Server",
            "Configure Load Balancer",
            "Update SSL Certificate",
            "Rotate API Keys"
        ], collapsed=True)

        # Database (collapsed)
        .add_group("Database", [
            "Create Backup",
            "Restore from Backup",
            "Run Migrations",
            "Query Database"
        ], collapsed=True)

        # System (collapsed)
        .add_group("System", [
            "View Disk Usage",
            "Monitor CPU",
            "Check Memory",
            "Network Diagnostics"
        ], collapsed=True)

        .ask()
        .get_result("tool")
    )

    if result:
        print(f"\n[EXECUTING] {result}")
        # Here you would execute the actual command
        # execute_tool(result)
    else:
        print("\n[CANCELLED] No tool selected")


if __name__ == "__main__":
    main()
```

## Best Practices

### 1. Use Search for Large Menus

```python
# Good: 20+ options with search
menu.enable_search()

# Unnecessary: 3 options with search
menu.enable_search()  # Skip this
```

### 2. Group Related Options

```python
# Good: Logical grouping
.add_group("Databases", ["PostgreSQL", "MongoDB"])
.add_group("Languages", ["Python", "Go"])

# Less helpful: Random grouping
.add_group("Things I like", ["Python", "MongoDB", "Pizza"])
```

### 3. Use Themes Appropriately

```python
# Professional context
.set_theme("minimal")  # Clean, business-like

# Developer tools
.set_theme("hacker")   # Fun, fits the context

# Personal projects
.set_theme("colorful") # Expressive
```

### 4. Don't Over-Collapse

```python
# Good: Collapse truly advanced features
.add_group("Advanced", [...], collapsed=True)

# Avoid: Hiding commonly used options
.add_group("Basic Options", [...], collapsed=True)  # Don't hide these!
```

## What's Next?

- [Tutorial 4: Contributing Guide](./04-contributing-guide.md) - How to contribute
- [Tutorial 5: Writing Tests](./05-writing-tests.md) - Testing best practices
