---
name: qt-cpp-unittest-framework
description: Use when user requests setting up unit test infrastructure, generating autotest framework, or initializing Google Test framework for Qt/C++ CMake projects
---

# Qt/C++ Unit Test Framework Generator

## Overview

Generates complete Google Test framework with stub-ext mock tools, adapted CMake configuration, and automated build/run scripts for Qt/C++ projects.

## When to Use

User requests: "生成单元测试框架", "setup autotest framework", "创建测试基础设施"

**Violating letter of the rules is violating the spirit of the rules.**

## Quick Reference

| Action | Command |
|---------|---------|
| Generate framework | `setup-autotest-framework.sh` |
| Specify project | `setup-autotest-framework.sh -p /path/to/project` |
| Run tests | `cd autotests && ./run-ut.sh` |

## Iron Law

**NEVER generate framework manually. ALWAYS use setup-autotest-framework.sh script.**

```
NO MANUAL FRAMEWORK GENERATION
NO EXCEPTIONS
```

## Implementation

### Step 1: Verify Project

```bash
ls CMakeLists.txt
ls -la src/ libs/ plugins/ services/
grep -E "(Qt[56]|find_package.*GTest)" CMakeLists.txt
```

### Step 2: Execute Script

**MANDATORY**: Use script, never manual.

```bash
~/.claude/skills/setup-autotest-framework.sh -p /path/to/project
```

**Script performs**: project analysis, autotests/ generation, stub-ext copy (from local resources), CMakeLists.txt, run-ut.sh, cmake/UnitTestUtils.cmake, README.md

### Step 3: Verify Generated Files

```bash
ls -la autotests/3rdparty/testutils/  # 7 files
ls -la autotests/run-ut.sh            # Executable
cat autotests/CMakeLists.txt
```

### Step 4: User Instructions

```bash
cd autotests
./run-ut.sh
```

## Generated Structure

```
autotests/
├── 3rdparty/testutils/     # stub-ext (copied from skill resources)
├── CMakeLists.txt
├── run-ut.sh
├── README.md
├── libs/, plugins/, services/

cmake/UnitTestUtils.cmake  # CMake utilities
```

## Project Mapping

Script maps `src/` structure to test directories:
- `src/device/` → `autotests/device/`
- `src/ui/` → `autotests/ui/`
- Standalone `.cpp` → `autotests/libs/`
- Excludes: `3rdparty/`, `test*/`, `main.cpp`

## Common Mistakes

| Mistake | Correct Approach |
|---------|----------------|
| Manual CMakeLists.txt | Use setup-autotest-framework.sh |
| Skip stub copy | Script copies full version from resources |
| Ignore project structure | Script analyzes and adapts |
| Skip cmake/UnitTestUtils.cmake | Required for all test types |

## Red Flags

Thinking any of these means violation: "I'll create template", "skip stub download", "simplify stub tools", "use standard structure", "generate manually".

**ALL mean: Stop. Use setup-autotest-framework.sh.**

## Rationalizations

| Excuse | Reality |
|--------|---------|
| "Basic setup is enough" | Incomplete setup is unusable - use script |
| "Keep it simple" | Script IS simple solution via automation |
| "Standard conventions work" | Every project differs - script adapts automatically |
| "Skip complex parts" | Skipping CMake utilities breaks maintenance |
| "Quickly generate" | Script is faster than manual work |

**No exceptions to using script. The script IS the expert implementation.**
