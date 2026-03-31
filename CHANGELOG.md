# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-03-31

### Added
- **Architecture Decision Records (ADR)**: 4 comprehensive ADRs documenting key design decisions
  - ADR-001: Zero-dependency design philosophy
  - ADR-002: Fluent chainable API pattern
  - ADR-003: Test-driven development approach
  - ADR-004: Type-first development strategy
- **Architecture Documentation**: Complete system overview with diagrams
  - Component interaction diagrams
  - Data flow diagrams
  - Design principles and trade-offs
- **Tutorial Series**: 5 step-by-step guides for users and contributors
  - 01-getting-started: Installation and first menu
  - 02-building-your-first-menu: Deep dive into menu construction
  - 03-advanced-features: Search, groups, themes
  - 04-contributing-guide: How to contribute
  - 05-writing-tests: Testing best practices
- **README documentation section**: Quick links to all documentation

### Changed
- Enhanced README with documentation links
- Improved project positioning as both tool library and teaching example
- Better onboarding for new contributors

### Documentation
- Added 9 comprehensive documents (~3,500 lines)
- ADRs provide rationale for major design decisions
- Tutorials cover beginner to advanced topics
- Architecture docs explain system design

## [0.3.0] - 2026-03-31

### Added
- **Search Functionality**: Real-time search to filter menu options
  - Press `/` to enter search mode
  - Character-based indexing for efficient substring matching
  - Case-insensitive search
  - `SearchEngine` class with zero-dependency implementation
  - `enable_search()` method on InteractiveMenu
  - Match summary display
- **Option Groups**: Organize options into collapsible groups
  - `OptionGroup` dataclass for group definitions
  - `GroupRenderer` class for group rendering
  - `add_group()` method on InteractiveMenu
  - Collapsed state support for hierarchical organization
- **Theme System**: Built-in themes and custom styling
  - 5 built-in themes: default, minimal, bold, dim, colorful, hacker
  - `MenuTheme` dataclass for theme configuration
  - `Colors` class with ANSI color codes
  - `set_theme()` method on InteractiveMenu
  - `get_theme()` and `list_themes()` helper functions
- **Demo examples**: Added search_demo.py, groups_demo.py, themes_demo.py

### Changed
- Improved test coverage to 127 tests
- Enhanced README with new features and examples
- Better code organization with dedicated modules for search, groups, and themes

### Tests
- Added `test_search.py` (7 tests)
- Added `test_groups.py` (18 tests)
- Added `test_themes.py` (13 tests)

## [0.2.0] - 2026-03-31

### Added
- **Keyboard Shortcuts**: Single-character shortcuts for menu options
  - Auto-generate shortcuts from option names
  - Explicit shortcut assignment via `add_option(name, shortcut='x')`
  - Display format: `[0/A]: Option A`
  - Direct key input for selection
  - Shortcut conflict detection
- **Config File Support**: Load menu definitions from files
  - JSON configuration support
  - YAML configuration support (optional, requires pyyaml)
  - `InteractiveMenu.from_file()` class method
  - `MenuConfig` class for configuration validation
- **Module documentation**: Added comprehensive module and method docstrings
- **Type hints**: Complete type annotations with `from __future__ import annotations`

### Changed
- Improved test coverage to 92 tests
- Enhanced README with new features and examples

### Tests
- Added `test_shortcuts.py` (14 tests)
- Added `test_config.py` (15 tests)
- Added `test_edge_cases.py` (23 tests)
- Added `test_integration.py` (20 tests)

## [0.1.0] - Initial Release

### Added
- Fluent chainable API for menu creation
- Single and multiple selection modes
- Nested menu support with parent navigation (`r` command)
- Selection confirmation and restart workflow
- Zero external dependencies

[0.2.0]: https://github.com/xirhxq/basic-interactive-menu/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/xirhxq/basic-interactive-menu/releases/tag/v0.1.0
