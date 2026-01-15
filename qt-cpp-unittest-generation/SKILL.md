---
name: qt-cpp-unittest-generation
description: Use when user requests generating unit tests for specific classes, writing test cases, or creating test files for Qt/C++ classes
---

# Qt/C++ Unit Test Generation

## Overview

Generates comprehensive unit tests using LSP tools to analyze class structure, understand business logic, identify dependencies, and create precise stubs with correct function signatures.

## When to Use

User requests: "为 MyClass 生成单元测试", "智能生成测试用例", "为这个类写测试"

**Violating the letter of the rules is violating the spirit of the rules.**

## Quick Reference

`lsp_document_symbols` - Read class
`lsp_goto_definition` - Read implementation
`lsp_find_references` - Find dependencies
Stub: `&Class::method`, `VADDR(Class, method)`, `static_cast<Ret(Class::*)(Args)>(&Class::method)`

## Iron Law

**NEVER use grep. ALWAYS use LSP tools. ALWAYS read implementation.**

```
NO GREP FOR CLASS ANALYSIS
NO EXCEPTIONS
NO TEMPLATE GENERATION
NO SIGNATURE GUESSING
```

## Implementation

### Step 1: Analyze with LSP

**MANDATORY**: LSP tools only.

```bash
lsp_document_symbols src/myclass.h
lsp_goto_definition src/myclass.cpp ClassName::methodName
lsp_find_references src/myclass.h ClassName
```

Extract: inheritance, methods, properties, signals, slots.

### Step 2: Read Implementations

**MANDATORY**: Read `.cpp` to understand logic.

```bash
lsp_goto_definition src/myclass.cpp MyClass::calculate
```

Identify: branches, boundary checks, error handling, edge cases.

### Step 3: Stub Dependencies

**MANDATORY**: Stub ALL external dependencies (QFile, QDialog, QWidget, etc.).

### Step 4: Design Targeted Scenarios

Based on logic, not templates: normal, boundary (min/max, empty, null), error handling, special cases.

### Step 5: Precise Stubs

**Match signatures EXACTLY** (const, &, *, virtual).

```cpp
// Virtual: VADDR macro
stub.set_lamda(VADDR(MyClass, virtualMethod), []() { });

// Overloaded: static_cast
stub.set_lamda(static_cast<Ret(Class::*)(Args)>(&Class::method), []() { });

// Regular: direct address
stub.set_lamda(&Class::method, []() { });
```

### Step 6: Test File Output

```cpp
class UT_MyClass : public ::testing::Test {
    stub_ext::StubExt stub;
    MyClass *obj = nullptr;
    void SetUp() override { stub.clear(); obj = new MyClass(); }
    void TearDown() override { delete obj; stub.clear(); }
};
TEST_F(UT_MyClass, Method_Scenario_Result) { /* Arrange, Act, Assert */ }
```

## UI Stubbing

`stub.set_lamda(VADDR(QDialog, exec), [] { return QDialog::Accepted; });`
`stub.set_lamda(&QWidget::show, [](QWidget *) { });`

## Naming Convention

- Test class: `UT_MyClass`
- Test case: `<Feature>_<Scenario>_<Result>`
- File: `test_myclass.cpp`

```cpp
TEST_F(UT_MyClass, Calculate_ValidInput_ReturnsCorrect)
TEST_F(UT_MyClass, Calculate_EmptyInput_ThrowsException)
```

## Common Mistakes

Using grep → Use LSP tools
Not reading .cpp → lsp_goto_definition
Generic templates → Read implementation, target scenarios
Wrong stub signature → Match exactly (const, &, *, virtual)
Letting QDialog::exec execute → Stub with VADDR(QDialog, exec)
Letting QWidget::show display → Stub &QWidget::show

## Red Flags

Thinking: "I'll grep", "use template", "skip UI stub", "let dialog show", "don't worry about signature".

**ALL mean: Delete code. Use LSP tools and read implementation.**

## Rationalizations

"Basic tests enough" → Missing edge cases, LSP mandatory
"Don't worry about dependencies" → Unstubbed fail, stub ALL
"All getters same" → Logic varies, read each
"Just mock somehow" → Wrong signatures fail, match exactly
"Skip complex stubs" → UI blocks CI/CD, UI MUST be stubbed
"grep is faster" → Grep misses too much, LSP REQUIRED
"Just read header" → Headers don't show logic, read .cpp

**No exceptions. LSP tools are mandatory for class analysis.**
