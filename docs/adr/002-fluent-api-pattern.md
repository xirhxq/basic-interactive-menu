# ADR-002: Fluent Chainable API Pattern

**Status:** Accepted
**Date:** 2026-03-31
**Context:** basic-interactive-menu v0.3.0

## Context

When designing the API for `InteractiveMenu`, we had several options:

```python
# Option A: Constructor-based
menu = InteractiveMenu(title="Select", options=["A", "B"], key="choice")
result = menu.ask()

# Option B: Property-based
menu = InteractiveMenu()
menu.title = "Select"
menu.options = ["A", "B"]
menu.key = "choice"
result = menu.ask()

# Option C: Fluent chainable (our choice)
result = (InteractiveMenu()
    .set_title("Select")
    .add_option("A")
    .add_option("B")
    .set_key("choice")
    .ask())
```

## Decision

**We chose the fluent chainable API pattern (Option C).**

All configuration methods return `self`, enabling method chaining.

## Rationale

### 1. Readability Matches Mental Model

Building a menu is a sequential process:
```python
result = (InteractiveMenu()
    .set_title("Select Action")           # First, set the context
    .set_key("action")                    # Name the result
    .add_option("Create")                 # Add options
    .add_option("Update")
    .add_option("Delete")
    .ask())                               # Finally, execute
```

This reads like a sentence: "Create menu, set title, add options, ask."

### 2. Composability

Fluent APIs compose naturally:

```python
# Reusable menu fragment
def add_standard_actions(menu):
    return (menu
        .add_option("Create", shortcut='c')
        .add_option("Update", shortcut='u')
        .add_option("Delete", shortcut='d'))

# Use it
result = (add_standard_actions(InteractiveMenu())
    .set_title("Manage Resources")
    .ask())
```

### 3. IDE-Friendly

Type hints and IDE autocomplete work well:
```python
menu = (InteractiveMenu()
    .set_title("Test")     # Returns InteractiveMenu
    # IDE knows available methods here
    .set_key("choice"))     # Still InteractiveMenu
```

### 4. Reduced Intermediate Variables

Without fluent API:
```python
menu = InteractiveMenu()
menu.set_title("Select")
menu.add_option("A")
menu.add_option("B")
menu.set_key("choice")
result = menu.ask()
```

With fluent API:
```python
result = (InteractiveMenu()
    .set_title("Select")
    .add_option("A")
    .add_option("B")
    .set_key("choice")
    .ask())
```

### 5. Natural Extension Point

Adding new features doesn't break existing code:
```python
# v0.1.0 API
menu.set_title("Test").ask()

# v0.2.0 added shortcuts - still works
menu.set_title("Test").add_option("Exit", shortcut='x').ask()

# v0.3.0 added themes - still works
menu.set_title("Test").set_theme("hacker").ask()
```

## Implementation Pattern

```python
class InteractiveMenu:
    def set_title(self, title: str) -> "InteractiveMenu":
        """Set menu title and return self for chaining."""
        self.title = title
        return self

    def add_option(self, name: str, shortcut: str | None = None) -> "InteractiveMenu":
        """Add option and return self for chaining."""
        self.options.append(Option(name=name, shortcut=shortcut))
        return self

    # All configuration methods follow this pattern
```

### Key Principles

1. **Return `self`**: All configuration methods return `self`
2. **Void methods for execution**: Methods that produce values (like `ask()`) don't return `self`
3. **Logical ordering**: Methods are named to encourage sensible sequences
4. **No required parameters**: Most methods have sensible defaults

## Trade-offs

### Drawbacks

1. **Debugging chained failures**: Harder to identify which method failed
   - Mitigation: Good error messages with context

2. **Longer lines**: Chaining can create wide lines
   - Mitigation: Python's implicit line continuation with parentheses

3. **State mutation**: Each method mutates the object
   - Mitigation: Clear documentation, immutable configs where possible

### Advantages Gained

1. **Expressiveness**: Code reads like intent
2. **Discoverability**: IDE autocomplete guides users
3. **Conciseness**: Less boilerplate
4. **Composition**: Easy to build reusable fragments

## Examples in the Wild

This pattern is used successfully by:

- **jQuery**: `$('#id').addClass('active').fadeIn()`
- **Pandas**: `df.groupby('col').filter(lambda x: x.sum() > 0)`
- **StringBuilder** (Java): `sb.append("a").append("b").toString()`

## Anti-patterns to Avoid

```python
# DON'T: Mixing concerns in one chain
menu.set_title("Test").ask().add_option("A")  # Error!

# DON'T: Chaining after execution
result = menu.ask().set_title("New")  # Returns result, not menu

# DON'T: State-dependent chains
menu.set_theme(theme).ask()  # If theme can be None, this breaks
```

## Reconsideration

We should reconsider if:
1. Users consistently struggle with the pattern
2. We need to support non-mutating operations
3. A different pattern becomes standard in Python CLI tools

## Related Decisions
- [ADR-001: Zero-Dependency Philosophy](./001-zero-dependency-philosophy.md)
- [ADR-004: Type-First Development](./004-type-first-development.md)
