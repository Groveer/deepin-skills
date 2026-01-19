---
name: qt-unittest-make
description: 为 Qt 项目生成单元测试代码。使用 LSP 分析类结构，自动生成 100% 函数覆盖率的测试用例。支持模块批量生成和单个类增量补全。
---

# Qt Unit Test Generator

## Iron Laws

1. **仅使用 Google Test**: 测试框架固定为 GTest，不支持 Qt Test
2. **100% 函数覆盖率**: 每个 public/protected 函数必须至少一个测试用例
3. **智能 CMake 合并**: 让 AI 根据项目具体情况优化合并，确保通用性
4. **支持增量更新**: 对比现有测试，补全未覆盖函数
5. **必须验证构建**: 生成后运行 cmake 编译，确保可运行

## When to Use

用户请求：`为 src/lib/ui 模块创建单元测试`，`为 MyClass 生成测试`，`补全测试用例`

## 执行流程

### 步骤 1: 检查测试框架

验证 `autotests/CMakeLists.txt` 和 `autotests/3rdparty/stub/` 存在。如不存在，提示用户先运行 `qt-unittest-build`。

### 步骤 2: 分析类结构

**模块批量生成**: glob 扫描目录所有 `.h/.hpp`，提取类名。

**单个类**: 直接分析指定类。

使用 LSP 工具：
- `lsp_document_symbols` - 提取类结构（方法、属性、信号、槽）
- `lsp_goto_definition` - 读取函数实现
- `lsp_find_references` - 查找依赖

### 步骤 3: 生成测试用例

**函数提取**: 所有 public/protected 方法。

**测试设计**:
- 每个函数至少一个测试用例
- 边界条件、错误处理、特殊场景
- 命名规范：`{Feature}_{Scenario}_{ExpectedResult}`

### 步骤 4: 生成 Stub 插桩

基于 UNIT_TEST_GUIDE.md 标准模式：
- UI 显示/隐藏：`&QWidget::show`, `&QWidget::hide`
- 对话框执行：`VADDR(QDialog, exec)`
- 信号监听：`QSignalSpy`
- 虚函数：`VADDR(Class, method)`
- 重载函数：`static_cast<...>`

### 步骤 5: 增量更新（如存在测试）

对比已测试函数 vs 所有函数，为未覆盖函数补全测试用例。

### 步骤 6: 智能合并 CMake

让 AI 根据项目具体情况优化合并 `autotests/CMakeLists.txt`，确保通用性和可维护性。

### 步骤 7: 验证构建

运行 `cmake --build .` 确保测试可编译。

## Red Flags

- ❌ 使用 Qt Test 框架
- ❌ 覆盖率不足 100%
- ❌ 硬编码 CMake 模板
- ❌ 不验证构建
- ❌ 不支持增量更新
- ❌ 生成项目级覆盖率报告（仅需验证当前测试）

## Quick Reference

**测试文件命名**: `test_myclass.cpp`
**测试类命名**: `MyClassTest`
**测试用例命名**: `{Feature}_{Scenario}_{ExpectedResult}`
**LSP 工具**: `lsp_document_symbols`, `lsp_goto_definition`, `lsp_find_references`
**Stub 模式**: `&Class::method`, `VADDR(Class, method)`, `static_cast<...>`

## 子 Agent 调用

调用 `agent/unittest-generator.md` 执行测试代码生成：
- 分析项目结构
- 生成测试文件
- 智能合并 CMake
- 验证构建

## 常见错误

| 错误 | 原因 | 修复 |
|------|------|------|
| 测试框架不存在 | 未运行 qt-unittest-build | 提示用户先运行框架构建技能 |
| 覆盖率不足 | 未分析所有函数 | 确保 lsp_document_symbols 提取完整 |
| CMake 合并失败 | 硬编码模板 | 使用 AI 智能合并，根据项目实际情况优化 |
| 编译失败 | Stub 签名错误 | 使用 LSP 获取精确签名 |
