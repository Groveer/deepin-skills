# Deepin Skills Collection

## Overview

This directory contains a collection of skills for deepin project development, covering various aspects of Qt/C++ development.

## Skills Directory

### Qt/C++ Unit Testing Skills

#### [qt-cpp-unittest-framework](qt-cpp-unittest-framework/)

**Purpose**: Generate complete Google Test framework with stub-ext mock tools and automated build/run scripts.

**When to use**: User requests setting up unit test infrastructure, generating autotest framework, or initializing Google Test framework for Qt/C++ CMake projects.

**Key features**:
- Intelligent project structure analysis
- Local stub-ext resources (bundled with skill)
- Adapted CMake configuration
- Automated test runner (5-step process)
- Coverage report generation

**Resources**:
- `SKILL.md` - Skill documentation
- `setup-autotest-framework.sh` - Framework generation script
- `resources/testutils/` - Local stub-ext source files

**Usage**:
```bash
~/.claude/skills/qt-cpp-unittest-framework/setup-autotest-framework.sh -p /path/to/project
cd autotests
./run-ut.sh
```

#### [qt-cpp-unittest-generation](qt-cpp-unittest-generation/)

**Purpose**: Generate comprehensive unit tests using LSP tools to analyze class structure and create precise stubs.

**When to use**: User requests generating unit tests for specific classes, writing test cases, or creating test files for Qt/C++ classes.

**Key features**:
- LSP-based class analysis (lsp_document_symbols, lsp_goto_definition)
- Business logic understanding from implementation files
- Precise stub generation with correct function signatures
- Virtual function stubbing (VADDR macro)
- Overloaded function stubbing (static_cast)
- UI method stubbing (QWidget::show, QDialog::exec)

**Resources**:
- `SKILL.md` - Skill documentation

**Usage**:
```bash
# AI automatically uses LSP tools:
lsp_document_symbols src/myclass.h
lsp_goto_definition src/myclass.cpp ClassName::methodName
lsp_find_references src/myclass.h ClassName
```

## Dependencies

### Framework Skill

**Script dependencies**:
- bash
- cmake
- Google Test (libgtest-dev, libgmock-dev)
- lcov, genhtml (for coverage reports)

**Stub-ext source**: Local `resources/testutils/` directory (bundled)

### Generation Skill

**LSP tools** (required):
- lsp_document_symbols
- lsp_goto_definition
- lsp_find_references

**Testing libraries**:
- Google Test (gtest/gmock)
- stub-ext (from framework skill)

## Testing Workflow

1. **Generate framework** (qt-cpp-unittest-framework):
   ```bash
   setup-autotest-framework.sh -p /path/to/project
   cd autotests
   ./run-ut.sh
   ```

2. **Generate tests for classes** (qt-cpp-unittest-generation):
   - User: "Generate tests for MyClass"
   - AI: Uses LSP tools → Analyzes class → Generates precise stubs → Creates test file

3. **Run tests**:
   ```bash
   cd autotests
   ./run-ut.sh
   ```

## File Structure

```
deepin-skills/
├── README.md                                  # This file
├── qt-cpp-unittest-framework/                   # Framework generation skill
│   ├── SKILL.md                               # Skill documentation (<500 words)
│   ├── setup-autotest-framework.sh             # Script (uses local resources)
│   └── resources/testutils/                   # Bundled stub-ext source
│       ├── cpp-stub/
│       │   ├── stub.h
│       │   ├── addr_any.h
│       │   ├── addr_pri.h
│       │   └── elfio.hpp
│       └── stub-ext/
│           ├── stubext.h
│           ├── stub-shadow.h
│           └── stub-shadow.cpp
└── qt-cpp-unittest-generation/                # Test generation skill
    └── SKILL.md                               # Skill documentation (<500 words)
```

## Adding New Skills

To add a new skill to this collection:

1. **Create skill directory**: `deepin-skills/skill-name/`
2. **Write SKILL.md**: Follow writing-skills guidelines
   - YAML frontmatter (name + description)
   - Description starts with "Use when..."
   - <500 words for frequently-loaded skills
   - Clear Iron Laws and Red Flags
3. **Add resources**: Any bundled resources in `resources/` subdirectory
4. **Update README**: Add skill entry to this document with:
   - Purpose
   - When to use
   - Key features
   - Resources
   - Usage example

## Design Principles

All skills in this collection follow writing-skills TDD methodology:

1. **RED Phase**: Identify pressure scenarios and baseline rationalizations
2. **GREEN Phase**: Write minimal skills addressing specific failures
3. **REFACTOR Phase**: Compress to <500 words, close all loopholes

Each skill includes:
- Clear Iron Laws (no exceptions)
- Red Flags (stop indicators)
- Rationalization tables (counters to common excuses)
- Quick Reference (efficient lookup)
- Common Mistakes (what goes wrong and fixes)

## Token Efficiency

- qt-cpp-unittest-framework: **414 words**
- qt-cpp-unittest-generation: **485 words**

All under 500-word limit for efficient context usage.

## Compatibility

**Tested with**:
- Qt5/Qt6 projects
- CMake 3.10+
- Google Test 1.8+
- C++14/17/20

**Supports**:
- Libraries (libs/)
- Plugins (plugins/)
- Services (services/)
- Standalone source files

## License

Part of dde-file-manager project (GPL-3.0-or-later).
