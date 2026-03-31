# Writing Tests

This tutorial covers testing practices for `basic-interactive-menu`. Well-written tests ensure code quality, prevent regressions, and serve as documentation.

## Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Test Structure](#test-structure)
3. [Writing Good Tests](#writing-good-tests)
4. [Common Patterns](#common-patterns)
5. [Running Tests](#running-tests)

## Testing Philosophy

We follow **Test-Driven Development (TDD)** principles:

1. **Red**: Write a failing test first
2. **Green**: Write minimal code to make it pass
3. **Refactor**: Improve the code while tests stay green

### Why Write Tests First?

- **Design by example**: Tests define how the API should work
- **Living documentation**: Tests show actual usage
- **Refactoring confidence**: Change code without fear
- **Regression prevention**: Bugs are caught immediately

## Test Structure

### File Organization

```
tests/
├── __init__.py
├── test_one_layer.py         # Basic functionality
├── test_three_layers.py      # Nested menus
├── test_search.py            # Search feature
├── test_groups.py            # Group feature
├── test_themes.py            # Theme feature
├── test_config.py            # Config loading
├── test_integration.py       # Feature interactions
└── test_edge_cases.py        # Boundary conditions
```

### Basic Test Template

```python
"""Tests for [feature name]."""

import unittest
from basic_interactive_menu import [ClassBeingTested]


class Test[FeatureName](unittest.TestCase):
    """Test [FeatureName] functionality."""

    def test_[specific_behavior](self):
        """Test that [expected behavior] occurs."""
        # Arrange
        input_value = "test"
        expected = "result"

        # Act
        result = function_being_tested(input_value)

        # Assert
        self.assertEqual(result, expected)
```

### Example: Search Tests

```python
"""Tests for search functionality."""

import unittest
from basic_interactive_menu.search import SearchEngine


class TestSearchEngine(unittest.TestCase):
    """Test SearchEngine functionality."""

    def test_search_empty_query(self):
        """Test that empty query returns all indices."""
        engine = SearchEngine(["Apple", "Banana", "Cherry"])
        result = engine.search("")

        # Should return all indices
        self.assertEqual(result, [0, 1, 2])

    def test_search_exact_match(self):
        """Test exact substring matching."""
        engine = SearchEngine(["Apple", "Banana", "Cherry"])
        result = engine.search("app")

        # Only Apple contains "app"
        self.assertEqual(result, [0])

    def test_search_case_insensitive(self):
        """Test case-insensitive search."""
        engine = SearchEngine(["Apple", "BANANA", "Cherry"])
        result = engine.search("banana")

        # Should match BANANA
        self.assertEqual(result, [1])
```

## Writing Good Tests

### 1. Descriptive Names

Test names should describe what is being tested:

```python
# Good: Descriptive
def test_search_returns_empty_list_for_no_matches(self):
    ...

def test_search_is_case_insensitive(self):
    ...

# Bad: Vague
def test_search(self):
    ...

def test_it_works(self):
    ...
```

### 2. Test One Thing

Each test should verify a single behavior:

```python
# Good: One assertion per test
def test_search_returns_correct_indices(self):
    engine = SearchEngine(["Apple", "Banana"])
    result = engine.search("app")
    self.assertEqual(result, [0])

# Bad: Multiple assertions testing different things
def test_search(self):
    engine = SearchEngine(["Apple", "Banana"])
    result = engine.search("app")
    self.assertEqual(result, [0])
    self.assertTrue(len(result) >= 0)  # Unrelated assertion
```

### 3. Use Arrange-Act-Assert

Structure tests clearly:

```python
def test_add_option_increases_count(self):
    """Test that adding options increases the option count."""
    # Arrange
    menu = InteractiveMenu()
    initial_count = len(menu.options)

    # Act
    menu.add_option("New Option")

    # Assert
    self.assertEqual(len(menu.options), initial_count + 1)
```

### 4. Test Edge Cases

Don't forget boundary conditions:

```python
class TestSearchEngine(unittest.TestCase):
    # ... normal cases ...

    def test_search_empty_options_list(self):
        """Test search with empty options list."""
        engine = SearchEngine([])
        result = engine.search("anything")
        self.assertEqual(result, [])

    def test_search_special_characters(self):
        """Test search with special characters."""
        engine = SearchEngine(["C++", "C#", "F#"])
        result = engine.search("c")
        self.assertEqual(result, [0, 1])

    def test_search_unicode(self):
        """Test search with unicode characters."""
        engine = SearchEngine(["Café", "Naïve"])
        result = engine.search("é")
        self.assertEqual(result, [0])
```

## Common Patterns

### Testing Menu Interactions

Use `unittest.mock.patch` to simulate user input:

```python
from unittest.mock import patch

class TestMenuInteraction(unittest.TestCase):
    @patch('builtins.input', return_value='0')
    def test_select_first_option(self, mock_input):
        """Test selecting the first option."""
        result = (
            InteractiveMenu()
            .set_key("choice")
            .add_option("A")
            .add_option("B")
            .ask()
            .get_result("choice")
        )
        self.assertEqual(result, "A")

    @patch('builtins.input', return_value='q')
    def test_quit_returns_none(self, mock_input):
        """Test that quitting returns None."""
        result = (
            InteractiveMenu()
            .set_key("choice")
            .add_option("A")
            .ask()
            .get_result("choice")
        )
        self.assertIsNone(result)
```

### Testing Multiple Selections

```python
@patch('builtins.input', return_value='0,2')
def test_multiple_selection(self, mock_input):
    """Test selecting multiple options."""
    result = (
        InteractiveMenu()
        .set_key("choices")
        .allow_multiple()
        .add_option("A")
        .add_option("B")
        .add_option("C")
        .ask()
        .get_result("choices")
    )
    self.assertEqual(result, ["A", "C"])
```

### Testing Config Loading

```python
import tempfile
import json

class TestConfigLoading(unittest.TestCase):
    def test_load_from_json_file(self):
        """Test loading menu from JSON file."""
        config = {
            "title": "Test Menu",
            "key": "choice",
            "options": ["A", "B", "C"]
        }

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False
        ) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            menu = InteractiveMenu.from_file(temp_path)
            self.assertEqual(menu.title, "Test Menu")
            self.assertEqual(len(menu.options), 3)
        finally:
            os.unlink(temp_path)
```

### Testing Theme Application

```python
class TestThemeApplication(unittest.TestCase):
    def test_theme_applies_to_border(self):
        """Test that theme colors are applied to borders."""
        theme = MenuTheme(border_color=Colors.CYAN)
        result = theme.apply_border("----")

        # Should contain the color code
        self.assertIn(Colors.CYAN, result)
        # Should contain the border
        self.assertIn("----", result)
```

## Testing Anti-Patterns

### Don't Test Implementation Details

```python
# Bad: Tests internal implementation
def test_index_is_dict(self):
    engine = SearchEngine(["A", "B"])
    self.assertIsInstance(engine._index, dict)

# Good: Tests behavior
def test_search_finds_matches(self):
    engine = SearchEngine(["A", "B"])
    result = engine.search("a")
    self.assertEqual(result, [0])
```

### Don't Test Trivial Code

```python
# Unnecessary: Testing a simple getter
def test_get_title(self):
    menu = InteractiveMenu()
    menu.set_title("Test")
    self.assertEqual(menu.title, "Test")

# Better: Test actual behavior
def test_menu_displays_title(self):
    # Test that title actually appears in output
    ...
```

### Don't Write Fragile Tests

```python
# Fragile: Depends on exact timing
def test_search_performance(self):
    start = time.time()
    engine.search("query")
    self.assertLess(time.time() - start, 0.001)  # Flaky!

# Better: Use complexity analysis or benchmarks
def test_search_scales_linearly(self):
    # Test that larger inputs don't cause exponential slowdown
    ...
```

## Running Tests

### Run All Tests

```bash
python -m unittest discover tests
```

### Run Specific Test File

```bash
python -m unittest tests.test_search
```

### Run Specific Test Class

```bash
python -m unittest tests.test_search.TestSearchEngine
```

### Run Specific Test Method

```bash
python -m unittest tests.test_search.TestSearchEngine.test_search_empty_query
```

### Run with Verbose Output

```bash
python -m unittest discover tests -v
```

### Run with Coverage

```bash
pip install coverage
coverage run -m unittest discover tests
coverage report
coverage html  # Generate HTML report
```

## Test Checklist

Before submitting, ensure:

- [ ] All tests pass
- [ ] New features have corresponding tests
- [ ] Edge cases are covered
- [ ] Test names are descriptive
- [ ] Tests are independent (no shared state)
- [ ] No tests are commented out
- [ ] Coverage hasn't decreased

## Example: Complete Test Suite

Here's a complete example for a simple feature:

```python
"""Tests for option shortcuts."""

import unittest
from basic_interactive_menu import InteractiveMenu


class TestShortcuts(unittest.TestCase):
    """Test keyboard shortcut functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.menu = InteractiveMenu()

    def test_explicit_shortcut_assigned(self):
        """Test that explicit shortcuts are assigned."""
        self.menu.add_option("Exit", shortcut='x')
        self.assertEqual(self.menu.options[0].shortcut, 'x')

    def test_auto_generated_shortcut(self):
        """Test that shortcuts are auto-generated from first letter."""
        self.menu.add_option("Create")
        self.assertEqual(self.menu.options[0].shortcut, 'C')

    def test_shortcut_conflict_detection(self):
        """Test that conflicting shortcuts are detected."""
        self.menu.add_option("Create", shortcut='c')
        self.menu.add_option("Cancel", shortcut='c')
        # Should handle conflict (skip, warn, or modify)
        self.assertIn('c', [o.shortcut for o in self.menu.options])

    def test_shortcut_case_insensitive(self):
        """Test that shortcuts are case-insensitive."""
        self.menu.add_option("Option", shortcut='a')
        self.menu.add_option("Other", shortcut='A')
        # Both 'a' and 'A' should be treated as same
        ...


if __name__ == '__main__':
    unittest.main()
```

## What's Next?

- [Tutorial 4: Contributing Guide](./04-contributing-guide.md) - How to contribute
- [ADR-003: TDD Approach](../adr/003-tdd-approach.md) - Our testing philosophy

Happy testing! 🧪
