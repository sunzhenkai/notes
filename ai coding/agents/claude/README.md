# Claude (Anthropic)

## 简介

Claude 是 Anthropic 开发的 AI 助手，在编程任务上表现出色。最新的 **Claude Opus 4.6** 是目前最强大的编程模型。

## 核心功能

### Claude 对话助手
- **代码生成与编辑** - 生成高质量代码
- **代码审查与优化** - 分析代码问题，提供优化建议
- **调试助手** - 帮助定位和修复 bug
- **架构设计** - 协助系统设计和架构决策
- **Artifacts** - 在对话中创建可交互的代码、图表等内容
- **超长上下文** - 支持 200K tokens

### Claude Code
- **终端编程** - 命令行中的 AI 编程助手
- **CLAUDE.md** - 项目配置文件，自动读取并遵循项目规范
- **代码库理解** - 深度理解整个项目结构
- **文件编辑** - 直接编辑本地文件
- **Git 集成** - 自动生成 commit 和管理变更
- **MCP 支持** - Model Context Protocol，连接外部工具
- **自定义命令** - 创建可复用的工作流命令
- **Hooks** - 在操作前后运行 shell 命令
- **Agent SDK** - 构建自定义 Agent

### Claude Cowork
- **协作空间** - 团队共享的 AI 协作环境
- **知识管理** - 组织和共享团队知识

### 多平台支持
- **Terminal** - 全功能 CLI
- **VS Code** - IDE 扩展
- **Desktop** - 桌面应用
- **Web** - 浏览器使用
- **JetBrains** - JetBrains 插件
- **iOS** - 移动端支持

## 核心特性

- **Opus 4.6** - 最强大的编程和 Agent 模型
- **超强推理** - 在复杂编程任务上表现优异
- **200K 上下文** - 可处理大型代码库
- **Artifacts** - 实时预览生成的代码、图表、文档
- **多模态** - 支持图像输入
- **无广告** - 纯净的对话体验
- **安全性** - 注重 AI 安全，诚实可靠

## CLAUDE.md 配置示例

```markdown
# 项目规范

## 编码标准
- 使用 TypeScript 和 React
- 遵循函数式编程原则
- 所有组件必须有 PropTypes

## 架构决策
- 使用 Redux 进行状态管理
- API 调用统一放在 services 目录

## 测试要求
- 单元测试使用 Jest
- E2E 测试使用 Cypress
```

## 安装 Claude Code

```bash
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex

# Homebrew
brew install --cask claude-code
```

## 最新动态

- **Feb 2026** - Opus 4.6 发布
- **Jan 2026** - Claude on Mars (协助 NASA 火星车)
- **2026** - Claude Cowork 团队协作功能
- **2026** - 81K 用户调研

## 定价

- **Free** - 有限使用 Sonnet 和 Haiku
- **Pro（$20/月）** - 更高使用额度
- **Team（$25/用户/月）** - 团队协作功能
- **Max** - 最高级别个人计划
- **API** - Opus $15/1M input, $75/1M output; Sonnet $3/1M input, $15/1M output

## 相关链接

- 官网：https://claude.ai
- 产品页面：https://claude.com/product/overview
- API 文档：https://docs.anthropic.com
- 控制台：https://platform.claude.com
- Claude Code：https://claude.com/product/claude-code
- 文档：https://docs.anthropic.com/claude/docs/claude-code
