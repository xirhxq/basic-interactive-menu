# Contributing Guide

Thank you for your interest in contributing to `basic-interactive-menu`! This guide will help you get started.

## Table of Contents

1. [Setting Up](#setting-up)
2. [Code Style](#code-style)
3. [Making Changes](#making-changes)
4. [Testing](#testing)
5. [Submitting Changes](#submitting-changes)

## Setting Up

### Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/basic-interactive-menu.git
cd basic-interactive-menu
```

### Create Development Environment

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install mypy pytest
```

### Verify Setup

```bash
# Run tests
python -m unittest discover tests

# Run type checking
mypy basic_interactive_menu/
```

All tests should pass!

## Code Style

### Python Version

We support Python 3.8+. Use modern Python features:

```python
# Use modern union syntax (PEP 604)
def func(x: str | None) -> str:  # Good
def func(x: Optional[str]) -> str:  # Also OK

# Use walrus operator where appropriate
if (n := len(items)) > 10:  # Good

# Use f-strings
print(f"Selected: {choice}")  # Good
```

### Type Hints

All public APIs must have type hints:

```python
from __future__ import annotations
from typing import List, Dict, Any

class InteractiveMenu:
    def add_option(
        self,
        name: str,
        shortcut: str | None = None
    ) -> InteractiveMenu:
        """Add an option to the menu.

        Args:
            name: The display name of the option.
            shortcut: Optional single-character shortcut.

        Returns:
            Self for method chaining.
        """
        ...
```

### Docstrings

Use Google-style docstrings:

```python
def search(self, query: str) -> List[int]:
    """Search for options matching the query.

    Args:
        query: Search string to match against options.

    Returns:
        List of indices matching the search query.

    Examples:
        >>> engine = SearchEngine(["Apple", "Banana"])
        >>> engine.search("app")
        [0]
    """
```

### Naming Conventions

```python
# Classes: PascalCase
class InteractiveMenu:
class SearchEngine:

# Functions/Methods: snake_case
def add_option():
def get_result():

# Constants: UPPER_SNAKE_CASE
MAX_OPTIONS = 100
DEFAULT_THEME = "default"

# Private methods: leading underscore
def _build_index():
def _validate_input():
```

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Edit the source files in `basic_interactive_menu/`
- Follow existing code style
- Add type hints to all new code
- Write docstrings for public APIs

### 3. Add Tests

All new features need tests:

```python
# tests/test_your_feature.py
import unittest
from basic_interactive_menu import YourFeature

class TestYourFeature(unittest.TestCase):
    def test_basic_functionality(self):
        """Test that basic functionality works."""
        feature = YourFeature()
        result = feature.do_something()
        self.assertEqual(result, expected_value)
```

### 4. Update Documentation

If your change affects user-facing behavior:
- Update README.md if needed
- Add examples to `examples/`
- Update relevant tutorials in `docs/tutorials/`

## Testing

### Run All Tests

```bash
python -m unittest discover tests
```

### Run Specific Test File

```bash
python -m unittest tests.test_search
```

### Run Specific Test

```bash
python -m unittest tests.test_search.TestSearchEngine.test_search_empty_query
```

### Test Coverage

We aim for >90% coverage. Check coverage:

```bash
pip install coverage
coverage run -m unittest discover tests
coverage report
```

### Type Checking

Run mypy before committing:

```bash
mypy basic_interactive_menu/
```

Fix any type errors!

## Committing

### Commit Message Format

```
type(scope): description

[Optional detailed explanation]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Build/config changes

**Examples:**

```
feat(search): add fuzzy search with character indexing

Implement SearchEngine class with O(1) character lookup
for efficient menu filtering.

fix(groups): handle empty groups gracefully

Raise ValueError when empty group is created instead of
crashing later.

docs(readme): add search feature example

Add usage example for enable_search() method.
```

### Pre-Commit Checklist

- [ ] All tests pass
- [ ] Type checking passes
- [ ] New features have tests
- [ ] Docstrings updated
- [ ] Documentation updated

## Submitting Changes

### Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### Create Pull Request

1. Go to the GitHub repository
2. Click "New Pull Request"
3. Select your branch
4. Fill in the PR template

### PR Title

Use the same format as commit messages:

```
feat(search): add fuzzy search with character indexing
```

### PR Description

Explain:
- **What** does this PR do?
- **Why** is this change needed?
- **How** does it work?
- **Any** breaking changes?

### Review Process

1. Automated tests run on your PR
2. Maintainer reviews your code
3. Address any feedback
4. Once approved, your PR is merged

## Development Workflow Example

Here's a complete example workflow:

```bash
# 1. Clone and setup
git clone https://github.com/YOUR_USERNAME/basic-interactive-menu.git
cd basic-interactive-menu
python -m venv venv
source venv/bin/activate
pip install -e .

# 2. Create branch
git checkout -b feat/add-sort-option

# 3. Make changes
# Edit files...

# 4. Test
python -m unittest discover tests
mypy basic_interactive_menu/

# 5. Commit
git add .
git commit -m "feat(menu): add option to sort menu items alphabetically"

# 6. Push
git push origin feat/add-sort-option

# 7. Create PR on GitHub
```

## Feature Ideas

Looking for something to work on? Here are some ideas:

### High Priority
- [ ] Multi-language support
- [ ] Accessibility improvements (screen reader mode)
- [ ] Performance optimizations for very large menus

### Medium Priority
- [ ] More built-in themes
- [ ] Option descriptions (shown on selection)
- [ ] Menu templates/presets

### Low Priority
- [ ] ASCII art borders
- [ ] Sound effects
- [ ] Animations

## Getting Help

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Existing Code**: Read through the source for examples

## Code of Conduct

Be respectful, inclusive, and constructive. We're all here to build something useful together.

---

Thank you for contributing! 🎉
