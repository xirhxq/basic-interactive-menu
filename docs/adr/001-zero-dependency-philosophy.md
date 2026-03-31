# ADR-001: Zero-Dependency Design Philosophy

**Status:** Accepted
**Date:** 2026-03-31
**Context:** basic-interactive-menu v0.3.0

## Context

When building `basic-interactive-menu`, we needed to decide whether to use external dependencies or maintain a pure Python implementation. CLI menu libraries commonly use dependencies like:
- `prompt_toolkit` for advanced terminal handling
- `click` or `typer` for CLI frameworks
- `rich` or `colorama` for colored output
- `fuzzysearch` for search functionality

## Decision

**We chose to implement a zero-dependency design.**

All functionality is built using only Python standard library:
- ANSI escape codes for colors and styling
- Character-based indexing for search
- Native string operations for parsing
- Standard `unittest` framework

## Rationale

### 1. Frictionless Installation
```bash
pip install basic-interactive-menu
# No dependency conflicts, no long dependency chains
```

Users can install the package without worrying about:
- Version conflicts with existing dependencies
- Security vulnerabilities in transitive dependencies
- Large download sizes
- Build failures on exotic platforms

### 2. Educational Value
As a teaching example, zero-dependency code:
- Is completely transparent - all logic is visible
- Demonstrates what's possible with stdlib alone
- Shows implementation details learners can adapt
- Reduces cognitive load for understanding the codebase

### 3. Long-term Stability
- Standard library changes slowly and predictably
- No risk of upstream dependencies becoming unmaintained
- No need to track and update transitive dependencies
- Python version compatibility is easier to maintain

### 4. Sufficient Functionality
For a CLI menu system, the standard library provides:
- ANSI color codes (terminal capabilities since 1980s)
- String manipulation for search
- Basic I/O for user interaction
- JSON/YAML parsing (via `json`, optional `yaml`)

## Trade-offs

### Drawbacks We Accept

| Feature | With Dependencies | Our Approach | Impact |
|---------|------------------|--------------|--------|
| Terminal detection | `blessed` detects capabilities | Assume ANSI support | Fails on very old terminals |
| Windows colors | `colorama` handles legacy consoles | Assume Windows 10+ | Win 7 users see escape codes |
| Advanced search | `fuzzywuzzy` with algorithms | Character indexing | Less sophisticated scoring |
| Input handling | `prompt_toolkit` multiline | Basic `input()` | No multiline editing |

### Mitigation Strategies

1. **Assumption:** ANSI support is universal on modern systems
2. **Documentation:** Clearly state requirements (Python 3.8+, modern terminal)
3. **Progressive enhancement:** Features work, may not be pretty on edge cases
4. **Optional dependencies:** Allow `pyyaml` for YAML configs (not required)

## Implementation Guidelines

When adding new features, follow this decision tree:

```
Can stdlib do it adequately?
├─ Yes → Use stdlib
└─ No → Can we simplify requirements?
    ├─ Yes → Simplify and use stdlib
    └─ No → Make it an optional dependency
```

### Examples

**Search implementation:**
- Could use `fuzzysearch` package
- Implemented character-based indexing instead
- Result: Good enough for typical menu sizes (< 100 options)

**Theme system:**
- Could use `rich` for styling
- Implemented ANSI codes directly
- Result: Full styling control, no dependency bloat

## Consequences

### Positive
- Installation is instant and reliable
- Code is portable across Python environments
- Easy to audit for security
- Smaller attack surface

### Negative
- Cannot leverage specialized library features
- Must implement some algorithms from scratch
- Testing requires more edge case coverage

### Neutral
- More code to maintain (we own the implementations)
- Slower initial development (building vs. using)
- Greater understanding of internals (educational benefit)

## Reconsideration

We should reconsider this decision if:
1. A standard library feature becomes deprecated
2. A compelling new capability requires external code
3. Performance becomes critical and optimized libraries exist

## Related Decisions
- [ADR-002: Fluent Chainable API Pattern](./002-fluent-api-pattern.md)
- [ADR-003: TDD Approach](./003-tdd-approach.md)
