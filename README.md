# Deepin Skills

Deepin Skills 是为 Deepin 项目开发提供的一套 AI 辅助技能集合，涵盖 Qt/C++ 开发、翻译管理、Git 工作流、发布自动化和 GitHub 代码走查等领域。

## 安装与配置

### 1. 安装 OpenCode

```bash
# 安装脚本（推荐）
curl -fsSL https://install.opencode.ai | bash

# 或使用包管理器
npm install -g opencode-ai
```

### 2. 安装 OpenSkills

```bash
# 全局安装（推荐）
npm i -g openskills

# 验证安装
openskills --version
```

### 3. 安装 Superpowers ⭐ 推荐

Superpowers 是完整的软件开发工作流，为你的 AI 代理提供技能和指导。

```bash
# 克隆 Superpowers 仓库
git clone https://github.com/obra/superpowers ~/.config/opencode/superpowers

# 创建插件目录并创建符号链接
mkdir -p ~/.config/opencode/plugin
ln -sf ~/.config/opencode/superpowers/.opencode/plugin/superpowers.js \
     ~/.config/opencode/plugin/superpowers.js

# 重启 OpenCode 使插件生效
```

验证安装：
```bash
# 在 OpenCode 中使用 /skills 命令
# 如果能看到 superpowers:writing-skills，说明安装成功
```

### 4. 安装 Oh-My-OpenCode ⭐ 推荐

Oh-My-OpenCode 是最佳的智能体系统，提供 Sisyphus 代理、背景任务、LSP 支持等强大功能。

```bash
# 在 OpenCode 中，让 AI 代理自动安装
# 或按照官方文档手动安装
# 参考: https://github.com/code-yeongyu/oh-my-opencode
```

核心特性：
- **Sisyphus Agent** - 主代理，具备完整团队协作能力
- **多智能体协作** - Oracle、Librarian、Explore、Frontend UI/UX Engineer
- **背景任务** - 并行运行多个代理，提高效率
- **LSP & AST 工具** - 精准重构和代码搜索
- **Claude Code 兼容** - 完整的命令、技能、MCP 和 Hook 支持

### 5. 配置 OpenCode

启动 OpenCode 后，使用 `/connect` 配置 AI 提供商（如 Anthropic Claude、OpenAI 等）的 API 密钥。

### 6. 安装 Deepin Skills

```bash
# 全局安装（推荐 - 所有项目可用）
openskills install re2zero/deepin-skills --global

# 或安装到当前项目
openskills install re2zero/deepin-skills
```

### 7. 同步技能

```bash
openskills sync
```

## 推荐工具

### Superpowers

完整软件开发工作流，提供 TDD 技能创建、头脑风暴、调试等技能。

**使用方式**：
```
use find_skills tool to find superpowers:writing-skills to create a new skill
```

### Oh-My-OpenCode

智能体系统，让 AI 代理像专业开发团队一样工作。

**使用方式**：
- 包含 `ultrawork`（或 `ulw`）关键词自动启用所有功能
- 多代理并行处理任务
- 强制任务完成，不会中途放弃

## 使用技巧

### 技能仓库管理

```bash
# 全局安装（推荐）
openskills install re2zero/deepin-skills --global

# 更新技能
openskills update deepin-skills

# 查看已安装的技能
openskills list
```

1. **自然语言触发**：在 OpenCode 中直接用中文描述需求，AI 会自动配配合适的技能
   ```
   请为当前项目生成单元测试框架
   为 MyClass 创建单元测试
   ```

2. **显式调用技能**：使用 `/skills` 命令查看可用技能

3. **项目初始化**：首次使用时运行 `/init` 初始化项目配置

### Claude Skills 兼容性

本项目完全兼容 Claude Skills 系统，可在以下 AI 编程工具中使用：
- **OpenCode**（推荐）
- **Claude Code**
- **Cursor**
- **Windsurf**

通过 OpenSkills 统一管理，跨工具无缝切换。

## License

GPL-3.0-or-later
