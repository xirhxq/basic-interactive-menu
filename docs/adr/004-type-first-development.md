# ADR-004: Type-First Development Strategy

**Status:** Accepted
**Date:** 2026-03-31
**Context:** basic-interactive-menu v0.3.0

## Context

Python is dynamically typed, but type hints (PEP 484) have become standard. We had to decide:

1. **No type hints**: Traditional Python, duck typing
2. **Minimal type hints**: Only on public APIs
3. **Full type hints**: Complete type coverage (our choice)

## Decision

**We adopted a type-first development strategy.**

All functions, methods, and classes have complete type hints using Python's `typing` module and `from __future__ import annotations`.

## Rationale

### 1. IDE Support and Autocomplete

Type hints enable powerful IDE features:

```python
from basic_interactive_menu import InteractiveMenu

menu = InteractiveMenu()
menu.set_t  # IDE suggests: set_title, set_theme, set_key
```

Without types, IDEs can't provide accurate suggestions.

### 2. Early Error Detection

Type checkers catch errors before runtime:

```python
# mypy catches this error
result: str = menu.ask()  # Error: ask() returns MenuResult, not str
```

Our CI runs `mypy` on every push.

### 3. Self-Documenting Code

Types serve as inline documentation:

```python
def add_option(
    self,
    name: str,
    shortcut: str | None = None
) -> InteractiveMenu:
    """Add an option to the menu."""
```

Users can see:
- `name` must be a string
- `shortcut` is optional
- Method returns `InteractiveMenu` for chaining

### 4. Refactoring Safety

With types, refactoring is safer:

```python
# Before refactoring
def search(self, query: str) -> List[int]:
    ...

# After refactoring - types catch breaking changes
def search(self, query: str, threshold: float = 0.5) -> List[int]:
    ...

# Old code still works (default value)
# New code can use threshold
```

### 5. Educational Value

For a teaching project, type hints:
- Show expected data structures explicitly
- Teach modern Python best practices
- Help readers understand code flow

## Implementation

### Type Annotation Style

We use `from __future__ import annotations`:

```python
from __future__ import annotations
from typing import List, Dict, Optional, Union

class InteractiveMenu:
    def add_option(
        self,
        name: str,
        shortcut: str | None = None
    ) -> InteractiveMenu:
        ...

def get_all_results(self) -> Dict[str, Any]:
    ...
```

Benefits:
- Use modern union syntax (`str | None` instead of `Optional[str]`)
- Forward references work without strings (`MenuResult` not `"MenuResult"`)

### Type Definitions

```python
# basic_interactive_menu/types.py (if needed)
from typing import TypedDict, Union

class MenuResult(TypedDict):
    """Type for menu result dictionary."""
    key: str
    value: Union[str, List[str]]
    timestamp: float

OptionOrString = Union[str, Option]
```

### Complex Types

```python
from typing import Callable, Protocol

class MenuRenderer(Protocol):
    """Protocol for menu renderers."""
    def render(self, options: List[str]) -> str: ...

def use_renderer(renderer: MenuRenderer) -> None:
    ...
```

## Coverage Strategy

### What We Type

1. **All public APIs**: Every user-facing method
2. **All function signatures**: Parameters and return types
3. **Class attributes**: Where applicable
4. **Callback signatures**: For user-provided functions

### What We Don't Type

1. **Private methods**: Still typed for consistency
2. **Lambdas**: Usually inferred
3. **Literal values**: Redundant

### Example

```python
class SearchEngine:
    """Zero-dependency fuzzy search engine for menu options."""

    def __init__(self, options: List[str]) -> None:
        """Initialize the search engine with menu options."""
        self.options: List[str] = options
        self._index: Dict[str, List[int]] = self._build_index()

    def _build_index(self) -> Dict[str, List[int]]:
        """Build a character-to-indices mapping for fast lookup."""
        index: Dict[str, List[int]] = {}
        for i, option in enumerate(self.options):
            for char in option.lower():
                if char.isalnum():
                    if char not in index:
                        index[char] = []
                    if i not in index[char]:
                        index[char].append(i)
        return index

    def search(self, query: str) -> List[int]:
        """Search for options matching the query."""
        if not query:
            return list(range(len(self.options)))

        query = query.lower()
        matches: set[int] = set()

        for char in query:
            if char.isalnum() and char in self._index:
                matches.update(self._index[char])

        for i, option in enumerate(self.options):
            if query in option.lower():
                matches.add(i)

        return sorted(matches)
```

## Type Checking in CI

```yaml
# .github/workflows/ci.yml
- name: Run type checks
  run: |
    mypy basic_interactive_menu/
```

Configuration:

```ini
# setup.cfg
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

## Trade-offs

### Benefits

1. **Better IDE experience**: Autocomplete, inline errors
2. **Fewer runtime bugs**: Type checker catches mismatched types
3. **Easier refactoring**: Types show impact of changes
4. **Self-documenting**: Types are always accurate documentation

### Drawbacks

1. **More verbose**: Type hints add ~20% to code size
2. **Learning curve**: New contributors need typing knowledge
3. **Flexibility**: Some dynamic patterns are harder to express

### Mitigation

1. **Use modern syntax**: `str | None` vs `Optional[str]`
2. **Type aliases**: Simplify complex types
3. **Protocol classes**: For duck typing with types

## Guidelines

1. **Type all public APIs** (non-negotiable)
2. **Type private methods** (for consistency)
3. **Use `Any` sparingly** (prefer specific types)
4. **Add type stubs** for external libraries if needed
5. **Run mypy in CI** (enforces type correctness)

## Examples: Before and After

```python
# Without types
def add_option(self, name, shortcut=None):
    self.options.append(name)
    return self

# With types
def add_option(
    self,
    name: str,
    shortcut: str | None = None
) -> InteractiveMenu:
    """Add an option to the menu."""
    self.options.append(name)
    return self
```

The typed version is:
- More explicit about expected inputs
- Clearer about return type for chaining
- Self-documenting

## Reconsideration

We should reconsider if:
1. Type hints significantly slow down development
2. Contributors struggle with typing concepts
3. Type checking becomes a bottleneck

## Related Decisions
- [ADR-001: Zero-Dependency Philosophy](./001-zero-dependency-philosophy.md)
- [ADR-002: Fluent API Pattern](./002-fluent-api-pattern.md)
- [ADR-003: TDD Approach](./003-tdd-approach.md)
