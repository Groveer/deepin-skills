# Qt Unittest Make Skill

为 Qt 项目自动生成单元测试代码的技能。

## 功能特性

- **100% 函数覆盖率**: 自动为每个 public/protected 函数生成测试用例
- **智能 LSP 分析**: 使用 `lsp_document_symbols`, `lsp_goto_definition`, `lsp_find_references` 精确分析类结构
- **Stub 智能生成**: 基于 UNIT_TEST_GUIDE.md 自动生成 UI、信号、虚函数、重载函数的 Stub
- **智能 CMake 合并**: 根据项目具体情况优化 CMake 配置，确保通用性
- **支持增量更新**: 对比现有测试，补全未覆盖的函数
- **必须验证构建**: 生成后自动验证 cmake 编译，确保测试可运行

## 与 qt-unittest-build 的关系

```
qt-unittest-build (构建框架)
    ↓ 生成测试框架（CMake、目录结构、stub工具）

qt-unittest-make (生成测试代码)
    ↓ 生成测试用例（100% 函数覆盖率）
```

**协作流程**:
1. 首次使用：运行 `qt-unittest-build` 生成测试框架
2. 生成测试：运行 `qt-unittest-make` 生成测试代码
3. 增量更新：代码变更后，再次运行 `qt-unittest-make` 补全测试

## 使用方法

### 场景 1: 为模块批量生成测试

**触发方式**:
```
为 src/lib/ui 模块创建单元测试
```

**执行流程**:
1. 扫描模块所有类（glob 查找 `.h/.hpp` 文件）
2. 使用 LSP 分析每个类结构
3. 为每个类生成测试文件（`test_myclass.cpp`）
4. 生成测试用例（100% 函数覆盖率）
5. 生成 Stub 插桩（UI、信号、虚函数等）
6. 智能合并 CMake 配置
7. 验证构建（cmake 编译）

**输出**:
```
autotests/
├── CMakeLists.txt (已更新)
└── ui/
    ├── CMakeLists.txt (新建)
    ├── test_myclass.cpp
    ├── test_anotherclass.cpp
    └── ...
```

### 场景 2: 为单个类创建/补全测试

**触发方式**:
```
为 src/test/myclass.cpp 创建单元测试
```

或

```
为 MyClass 补全测试
```

**执行流程**:
1. 检查现有测试文件
2. 如果存在：对比已测试 vs 未测试函数
3. 如果不存在：完整生成测试
4. 补全或生成测试用例
5. 更新 CMake 配置（如需要）
6. 验证构建

**增量更新示例**:
```
现有测试：test_myclass.cpp
已测试函数：10/15
未测试函数：5

结果：
- 追加 5 个测试用例
- 覆盖率：100%
```

## 技术规范

### 测试框架

**仅支持 Google Test**:
```cpp
#include <gtest/gtest.h>

class MyClassTest : public ::testing::Test {
    // 测试类
};

TEST_F(MyClassTest, Method_Scenario_Result) {
    // 测试用例
}
```

### 命名规范

**文件命名**: `test_myclass.cpp`（小写）

**测试类命名**: `MyClassTest`（PascalCase）

**测试用例命名**: `{Feature}_{Scenario}_{ExpectedResult}`

**示例**:
- `Calculate_TwoNumbers_ReturnsSum` - 基本功能
- `Process_NullInput_HandlesGracefully` - 错误处理
- `SetValue_MaximumValue_ClampsCorrectly` - 边界条件

### LSP 工具使用

```bash
# 提取类结构
lsp_document_symbols "src/lib/ui/myclass.h"

# 读取函数实现
lsp_goto_definition "src/lib/ui/myclass.cpp" "MyClass::calculate"

# 查找依赖
lsp_find_references "src/lib/ui/myclass.h" "MyClass"
```

### Stub 插桩模式

**UI 显示/隐藏**:
```cpp
stub.set_lamda(&QWidget::show, [](QWidget *) {
    __DBG_STUB_INVOKE__
});

stub.set_lamda(&QWidget::hide, [](QWidget *) {
    __DBG_STUB_INVOKE__
});
```

**对话框执行**:
```cpp
stub.set_lamda(VADDR(QDialog, exec), [] {
    __DBG_STUB_INVOKE__
    return QDialog::Accepted;
});
```

**信号监听**:
```cpp
QSignalSpy spy(obj, &MyClass::signalChanged);
EXPECT_EQ(spy.count(), 1);
EXPECT_EQ(spy.at(0).at(0).toInt(), expected);
```

**虚函数**:
```cpp
stub.set_lamda(VADDR(MyClass, virtualMethod), []() {
    __DBG_STUB_INVOKE__
});
```

**重载函数**:
```cpp
stub.set_lamda(
    static_cast<int (MyClass::*)(int, int)>(&MyClass::overloadedMethod),
    [](MyClass *self, int a, int b) -> int {
        __DBG_STUB_INVOKE__
        return a + b;
    }
);
```

### CMake 智能合并

**策略**: 根据 CMake 具体情况优化合并，确保通用性

**分析项目**:
```bash
# 根目录 CMakeLists.txt
- 项目名称: project(...)
- Qt 版本: find_package(Qt5/Qt6 ...)
- 依赖库: find_package(...)
```

**生成通用 CMakeLists.txt**:
```cmake
cmake_minimum_required(VERSION 3.16)

# 使用变量而非硬编码
set(QT_VERSION "6")  # 从项目推断
set(PROJECT_LIBRARIES "")

file(GLOB TEST_SOURCES "test_*.cpp")

add_executable(test_{module_name} ${TEST_SOURCES})

target_link_libraries(test_{module_name}
    PRIVATE
    GTest::gtest
    GTest::gtest_main
    Qt${QT_VERSION}::Test
)

target_include_directories(test_{module_name}
    PRIVATE
    ${{CMAKE_SOURCE_DIR}}/autotests/3rdparty/stub
    ${{CMAKE_SOURCE_DIR}}/{source_module_path}
)

gtest_discover_tests(test_{module_name})
```

## 测试用例设计

### AAA 模式

每个测试用例遵循 Arrange-Act-Assert 模式：

```cpp
TEST_F(MyClassTest, Method_Scenario_Result) {
    // Arrange: 准备测试数据
    obj->setInput(42);

    // Act: 执行被测试的操作
    int result = obj->calculate();

    // Assert: 验证结果
    EXPECT_EQ(result, 84);
}
```

### 测试用例分类

#### 1. 基本功能测试
```cpp
TEST_F(MyClassTest, Calculate_TwoNumbers_ReturnsSum) {
    EXPECT_EQ(obj->calculate(2, 3), 5);
}
```

#### 2. 边界条件测试
```cpp
TEST_F(MyClassTest, Calculate_MaximumValue_ClampsCorrectly) {
    EXPECT_EQ(obj->calculate(INT_MAX, 1), INT_MAX);
}

TEST_F(MyClassTest, Process_EmptyInput_ReturnsDefault) {
    EXPECT_EQ(obj->process(""), "default");
}
```

#### 3. 错误处理测试
```cpp
TEST_F(MyClassTest, Process_NullInput_HandlesGracefully) {
    EXPECT_NO_THROW(obj->process(nullptr));
}

TEST_F(MyClassTest, Process_InvalidInput_ThrowsException) {
    EXPECT_THROW(obj->process("invalid"), std::runtime_error);
}
```

#### 4. 特殊场景测试
```cpp
TEST_F(MyClassTest, Process_SpecialCharacters_HandlesCorrectly) {
    QString input = "test & % $";
    EXPECT_NO_THROW(obj->process(input));
}
```

## 验证构建

**自动验证**:
```bash
cd build-autotests
cmake .. -DCMAKE_BUILD_TYPE=Debug -DBUILD_TESTS=ON
cmake --build . -j$(nproc)
```

**预期输出**:
- `Configuring done`
- `Generating done`
- `Built target test_{module_name}`
- 无错误

## 常见问题

### Q: 为什么只支持 Google Test？

A: 为了简化技能设计，确保测试质量。Google Test 提供了丰富的断言宏和测试发现功能，适合 Qt 项目。

### Q: 如何处理复杂的依赖关系？

A: 使用 `lsp_find_references` 分析依赖关系，自动生成对应的 Stub 插桩。

### Q: CMake 合并策略是什么？

A: 智能 CMake 合并根据项目具体情况优化：
1. 分析现有 CMakeLists.txt
2. 提取 Qt 版本、依赖库、包含目录模式
3. 生成通用 CMakeLists.txt（使用变量）
4. 保持项目现有风格

### Q: 如何保证 100% 函数覆盖率？

A:
1. 使用 `lsp_document_symbols` 提取所有 public/protected 函数
2. 为每个函数至少生成一个测试用例
3. 考虑边界条件、错误处理、特殊场景

### Q: 增量更新如何工作？

A:
1. 对比现有测试文件中的已测试函数
2. 提取所有函数（LSP）
3. 计算未覆盖函数
4. 为未覆盖函数追加测试用例

## 与其他技能的对比

| 特性 | qt-unittest-build | qt-unittest-make | qt-cpp-unittest-generation |
|------|------------------|------------------|----------------------------|
| **功能** | 生成测试框架 | 生成测试代码 | 生成测试代码 |
| **测试框架** | GTest/Qt Test | 仅 GTest | GTest/Qt Test |
| **LSP 工具** | 无 | 必需 | 必需 |
| **CMake** | 自动生成 | 智能合并 | 无 |
| **覆盖率要求** | 无 | 100% | 无 |
| **增量更新** | 不支持 | 支持 | 不支持 |
| **构建验证** | 可选 | 必须 | 无 |

## 依赖要求

- Google Test (libgtest-dev, libgmock-dev)
- LSP 工具 (OpenCode 内置)
- Qt 项目结构（CMake）
- 测试框架（由 qt-unittest-build 生成）

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关资源

- **Google Test 文档**: https://google.github.io/googletest/
- **Qt Test 文档**: https://doc.qt.io/qt-6/qtest-overview.html
- **Stub-Ext 源码**: https://github.com/manfredlohw/cpp-stub
