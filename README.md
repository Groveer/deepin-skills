# Deepin Skills Collection

## Overview

This directory contains a collection of skills for deepin project development, covering various aspects of Qt/C++ development.

## Skills Directory

### Qt/C++ Unit Testing Skills

#### [qt-unittest-build](qt-unittest-build/) ⭐ **推荐**

**Purpose**: 为 Qt 项目自动生成单元测试框架，采用"固定脚本 + 动态AI"架构。

**When to use**: 用户请求为 Qt 项目设置单元测试框架，或需要自动化生成 CMake 配置和测试文件时。

**Key features**:
- **全自动流程**: 1句话即可完成，无需手动步骤
- **扁平化架构**: Skill 路由 + 子 Agent 全栈执行，无中间层
- **内置模板**: CMakeLists.txt、测试文件、stub-ext 工具、运行脚本全部内置
- **智能分析**: 自动识别项目结构、Qt 版本、第三方依赖
- **多框架支持**: Qt Test、Google Test、Catch2 任选

**Resources**:
- `SKILL.md` - 技能文档（任务路由器）
- `.opencode/agent/qt-unit-test-executor.md` - 子 Agent（全栈执行者）
- `README.md` - 详细使用文档

**Usage**:
```bash
# 在 OpenCode 中直接输入
请为当前项目生成单元测试框架

# 或显式调用
使用 qt-unittest-build 技能
```

**执行流程**:
1. Skill 触发 → 子 Agent 自动调用
2. 项目分析 → CMakeLists.txt、依赖、Qt 版本
3. 文件生成 → tests/ 目录、CMake 配置、测试文件
4. 用户确认 → write 工具询问确认
5. 完成 → 提供构建和运行命令

**与 qt-cpp-unittest-framework 对比**:
- ✅ 1句话 vs 5-6步手动流程
- ✅ 扁平化 vs 多脚本 + 占位符
- ✅ 内置模板 vs 模板文件 + 手动替换
- ✅ 自动 AI vs 手动 AI 交互
- ✅ 单文件维护 vs 多文件同步

#### [qt-cpp-unittest-framework](qt-cpp-unittest-framework/)（已过时）

**Purpose**: Generate Google Test framework with stub-ext mock tools and AI-assisted CMake configuration for Qt/C++ projects.

**When to use**: User requests setting up unit test infrastructure, generating autotest framework, or initializing Google Test framework for Qt/C++ CMake projects.

**Key features (v5.0.0)**:
- **AI-assisted CMakeLists.txt generation**: Analyzes project dependencies, structure, and includes to generate adaptive configuration
- **Universal directory structure support**: Adapts to actual project structure (components, modules, apps, application, src, libs, etc.)
- **Local stub-ext resources**: Bundled with skill, no external downloads required
- **Fixed process automation**: Scripts handle directories, stub tools, test runners, and prompt generation
- **Smart project detection**: Supports diverse source directory names and flat/nested structures
- **AI prompt templates**: Provides structured prompts for AI-based project analysis and CMake generation

**Resources**:
- `SKILL.md` - Complete skill documentation (v5.0.0)
- `setup-autotest-framework.sh` - Framework generation script (v5.0.0)
- `scripts/detect-project.sh` - Enhanced project detection (supports 9+ directory types)
- `scripts/copy-stubs.sh` - Stub tools copy
- `scripts/generate-cmake-utils.sh` - CMake utilities (outputs to autotests/cmake/)
- `scripts/generate-runner.sh` - Test runner generation
- `scripts/generate-readme.sh` - README generation
- `ai-prompts/analyze-project.md` - AI prompt for project analysis
- `ai-prompts/generate-cmake.md` - AI prompt for CMakeLists.txt generation
- `OPTIMIZATION_SUMMARY.md` - Detailed optimization summary and verification results
- `QUICK_START.md` - Quick start guide for users

**Usage**:
```bash
# Generate base framework
/path/to/qt-cpp-unittest-framework/setup-autotest-framework.sh -p /path/to/project

# Review AI prompts
cd /path/to/project/autotests
cat .ai_prompts/analyze-project.md    # See detected structure
cat .ai_prompts/generate-cmake.md       # See CMake generation rules

# Use AI to analyze and generate CMakeLists.txt
# (See QUICK_START.md for detailed steps)

# Run tests
./run-ut.sh
```

**v5.0.0 Improvements**:
- ✅ Removed hardcoded libs/plugins/services assumptions
- ✅ Added support for 9+ source directory types (application, apps, base, common, controls, components)
- ✅ Extended file extensions (.cc, .hpp, .cxx)
- ✅ Handles flat source structures (no subdirectories)
- ✅ Handles special cases (source directory has no submodules with sources)
- ✅ Moved UnitTestUtils.cmake to autotests/cmake/ (logical location)
- ✅ Enhanced exclusion rules (build, cmake, debian, doc*, assets, resources)
- ✅ AI-based CMakeLists.txt generation (adaptive to project)
- ✅ Comprehensive documentation (optimization summary, quick start guide)

**Supported Project Structures**:
- Standard: `src/module1/`, `src/module2/`
- Flat: `src/*.cpp`, `src/*.h`
- Functional: `application/*.cpp`, `application/module/`
- Type-based: `base/`, `common/`, `controls/`
- Component-based: `components/`, `modules/`
- Mixed: Multiple source directories in project root

**Known Limitations**:
- Test subdirectories (`autotests/module/`) not auto-created (requires AI generation)
- CMakeLists.txt files not auto-generated (requires AI execution)
- Multi-source directories detected (first one used primarily)
- Third-party dependencies detected by AI analysis (not script)

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

### Qt Translation Assistant Skills

#### [qt-translation-assistant](qt-translation-assistant/)

**Purpose**: Automated translation tool for Qt projects using AI models to translate TS (Translation Source) files with subagent architecture.

**When to use**: User requests translating Qt project localization files (TS files), automating translation workflows, or setting up multilingual support for Qt applications.

**Key features**:
- Smart parsing of TS files to identify incomplete translations
- Subagent architecture for improved performance and error isolation
- Support for multiple AI providers (OpenAI, Anthropic, DeepSeek, local servers)
- Batch processing for efficient translation of multiple strings
- Language-specific translation guidance (scripts, RTL, etc.)
- Consistency preservation across translations

**Architecture**:
- **Main Skill**: Handles TS file parsing and result writing
- **Translation Subagent**: Handles AI API calls independently
- **Coordinator**: Manages communication between main skill and subagent

**Resources**:
- `SKILL.md` - Skill documentation
- `translate.py` - Main script with subagent architecture
- `subagent/` - Translation subagent module
- `config_tool.py` - Interactive configuration tool
- `config_template.json` - Configuration template

**Usage**:
```bash
# Translate entire directory of TS files
python translate.py /path/to/ts/files/

# Translate specific file
python translate.py /path/to/ts/files/ /path/to/specific/file.ts

# With custom batch size
python translate.py --batch-size 20 /path/to/ts/files/

# Create configuration file
python translate.py --config

# Direct subagent usage
python -m subagent.translation_subagent --config config.json --strings "Hello" "World" --language zh-CN
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
