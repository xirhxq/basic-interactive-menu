# ADR-003: Test-Driven Development Approach

**Status:** Accepted
**Date:** 2026-03-31
**Context:** basic-interactive-menu v0.3.0

## Context

When developing `basic-interactive-menu`, we needed to decide how to ensure code quality and prevent regressions. Options included:

1. Write tests after implementation (traditional)
2. Write tests alongside implementation
3. Test-Driven Development (TDD) - write tests first

## Decision

**We adopted a Test-Driven Development approach.**

All features are developed with tests written before or alongside implementation.

## Rationale

### 1. Living Documentation

Tests serve as executable documentation:

```python
def test_add_option_with_shortcut(self):
    """Test that options with shortcuts are displayed correctly."""
    engine = SearchEngine(["Python", "JavaScript"])
    result = engine.search("py")
    self.assertEqual(result, [0])
```

This test documents:
- Expected behavior: search returns matching indices
- Input format: list of strings
- Return type: list of integers

### 2. Refactoring Confidence

With comprehensive tests, we can refactor fearlessly:

```python
# v0.2.0 implementation
def search(self, query: str) -> List[int]:
    results = []
    for i, option in enumerate(self.options):
        if query.lower() in option.lower():
            results.append(i)
    return results

# v0.3.0: Refactored with indexing for performance
def search(self, query: str) -> List[int]:
    # Uses character index for O(1) lookup
    # Tests verify same behavior
```

The 127 tests ensure refactoring doesn't break existing functionality.

### 3. Design by Example

Writing tests first forces us to design the API from usage perspective:

```python
# Test-first approach: How do we WANT it to work?
def test_fluent_api_chaining(self):
    result = (InteractiveMenu()
        .set_title("Test")
        .add_option("A")
        .ask()
        .get_result())
    self.assertIsNotNone(result)

# Then implement to make this work
```

### 4. Regression Prevention

Bugs are caught immediately:

```python
# v0.3.0 bug: Search returned wrong indices
def test_search_exact_match(self):
    engine = SearchEngine(["Apple", "Banana", "Cherry"])
    result = engine.search("app")
    self.assertEqual(result, [0])  # Failed! Returned [0, 1]
```

This test caught a bug in the character indexing logic before release.

### 5. Educational Value

For a teaching project, tests show:
- How to use the library
- Edge cases to consider
- Proper error handling
- Testing best practices

## Our TDD Workflow

```
1. Write failing test (Red)
   └─ Defines the desired behavior

2. Write minimal implementation (Green)
   └─ Make the test pass

3. Refactor and improve (Refactor)
   └─ Clean up while tests stay green

4. Repeat for next feature
```

### Example: Search Feature

**Step 1 - Write test:**
```python
def test_search_empty_query(self):
    engine = SearchEngine(["Apple", "Banana"])
    result = engine.search("")
    self.assertEqual(result, [0, 1])
```

**Step 2 - Implement:**
```python
def search(self, query: str) -> List[int]:
    if not query:
        return list(range(len(self.options)))
    # TODO: implement actual search
```

**Step 3 - Add more tests:**
```python
def test_search_exact_match(self):
    engine = SearchEngine(["Apple", "Banana"])
    result = engine.search("app")
    self.assertEqual(result, [0])

def test_search_case_insensitive(self):
    engine = SearchEngine(["Apple", "BANANA"])
    result = engine.search("banana")
    self.assertEqual(result, [1])
```

**Step 4 - Complete implementation:**
```python
def search(self, query: str) -> List[int]:
    if not query:
        return list(range(len(self.options)))
    # Full implementation with indexing
```

## Test Organization

```
tests/
├── test_one_layer.py           # Basic functionality
├── test_three_layers.py        # Nested menus
├── test_shortcuts.py           # Keyboard shortcuts
├── test_search.py              # Search feature (7 tests)
├── test_groups.py              # Group feature (18 tests)
├── test_themes.py              # Theme feature (13 tests)
├── test_config.py              # Config file loading
├── test_integration.py         # Integration tests (20 tests)
└── test_edge_cases.py          # Edge cases (23 tests)
```

### Coverage Categories

1. **Unit tests**: Individual methods and functions
2. **Integration tests**: Feature interactions
3. **Edge case tests**: Boundary conditions, error cases
4. **Regression tests**: Known bugs with guarding tests

## Trade-offs

### Drawbacks

1. **Slower initial development**: Writing tests takes time upfront
2. **More code to maintain**: Test code can exceed implementation code
3. **False confidence**: Tests only cover what you test

### Mitigation

1. **Focus on high-value tests**: Test complex logic, not getters/setters
2. **Keep tests simple**: Avoid test code complexity
3. **Review test coverage**: Ensure critical paths are covered

### Benefits Outweigh Drawbacks

For a library project:
- Users trust tested code
- Refactoring is safe
- Documentation is always accurate
- Bugs are caught early

## Metrics

| Version | Tests | Coverage | Lines of Test Code |
|---------|-------|----------|-------------------|
| v0.1.0  | 36    | ~85%     | ~400              |
| v0.2.0  | 92    | ~90%     | ~1,200            |
| v0.3.0  | 127   | ~95%     | ~1,800            |

## Guidelines for Contributors

1. **All features must have tests**
2. **Write tests before or with implementation**
3. **Tests should be readable** (they're documentation)
4. **Use descriptive test names**: `test_search_returns_empty_list_for_no_matches`
5. **One assertion per test** (when reasonable)

## Related Decisions
- [ADR-001: Zero-Dependency Philosophy](./001-zero-dependency-philosophy.md)
- [ADR-004: Type-First Development](./004-type-first-development.md)
