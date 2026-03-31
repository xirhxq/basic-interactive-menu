# basic-interactive-menu Development Plan

## Context

`basic-interactive-menu` is a Python package for building interactive CLI menus with a fluent chainable API. Current state: functional but lacks type hints, docstrings, and comprehensive testing.

**Goal:** Transform basic-interactive-menu into a production-ready Python package.

---

## Phase 1: Code Quality Improvements ✅ COMPLETED

### Type Hints
- [x] Add complete type hints to `interactive_menu.py`
- [x] Use `from __future__ import annotations` for forward references
- [ ] Add type stub file if needed
- [ ] Run mypy in CI

### Docstrings
- [x] Add Google-style docstrings to `InteractiveMenu` class
- [x] Document all public methods with Args/Returns
- [x] Add module-level docstring
- [ ] Set up Sphinx documentation

### Testing
- [x] Achieve 90%+ test coverage (63 tests, all passing)
- [x] Add tests for edge cases (empty options, single option, etc.)
- [x] Add integration tests
- [ ] Run pytest-cov in CI

---

## Phase 2: New Features ✅ COMPLETED

### Keyboard Shortcuts ✅
- [x] Assign single-character shortcuts to options
- [x] Display shortcuts as `[A] Option A`
- [x] Support direct key input for selection
- [x] Handle shortcut conflicts

### History Memory ❌ SKIPPED
- Not necessary for simple CLI menu use cases

### Config File Support ✅
- [x] Create `config.py` with `MenuConfig` class
- [x] Support YAML menu definitions (optional, requires pyyaml)
- [x] Support JSON menu definitions
- [x] Add `from_file()` class method to `InteractiveMenu`

---

## Phase 3: Documentation & Release

### Documentation
- [ ] Update README.md with new features
- [ ] Add CHANGELOG.md
- [ ] Set up Sphinx docs (readthedocs)
- [ ] Add more examples

### PyPI Release
- [ ] Update setup.py with new dependencies
- [ ] Add GitHub Actions CI/CD
- [ ] Publish to PyPI
- [ ] Add version badges

---

## File Structure

```
basic_interactive_menu/
├── __init__.py           # Update exports
├── interactive_menu.py   # Type hints, docstrings, shortcuts
├── history.py            # New: HistoryManager
├── config.py             # New: MenuConfig
├── typing_utils.py       # New: Type aliases
└── version.py            # New: Version info

tests/
├── test_interactive_menu.py
├── test_history.py       # New
├── test_config.py        # New
├── test_shortcuts.py     # New
└── conftest.py           # Fixtures

docs/
├── conf.py               # Sphinx config
├── index.rst
└── api.rst
```

---

## Verification

After each phase:
1. `mypy basic_interactive_menu/` - type check passes
2. `pytest tests/ --cov` - 90%+ coverage
3. `python examples/*.py` - examples run correctly
4. `pip install -e .` - installs without errors

---

## Dependencies

```
Phase 1 → Phase 2 → Phase 3
```

**Current focus: Phase 1 (Code Quality)**
