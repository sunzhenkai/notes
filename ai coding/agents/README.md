# AI Coding Agents 概览

> 本目录汇总了当前主流的 AI 编程助手和 Agent 工具。
> 最后更新：2026年3月

## 快速对比

| Agent | 类型 | 核心特性 | 定价 | 最适合 |
|-------|------|---------|------|--------|
| [Cursor](./cursor) | AI IDE | Cloud Agents、Composer 2、.cursorrules | Free ~ $40/月 | 端到端开发、团队协作 |
| [GitHub Copilot](./github-copilot) | 平台+插件 | Copilot Spaces、免费计划、多模型 | Free ~ $39/月 | VS Code 用户、企业团队 |
| [Claude](./claude) | 对话助手 | Opus 4.6、CLAUDE.md、Claude Code | Free ~ $200/月 | 复杂推理、长任务 |
| [ChatGPT](./chatgpt) | 对话助手 | GPT-4o/5、GPTs生态 | Free ~ $200/月 | 通用编程、学习 |
| [Windsurf](./windsurf) | AI IDE | Cascade Flow、实时预览 | Free ~ 企业 | 多文件编辑、前端开发 |
| [Aider](./aider) | CLI 工具 | 开源、Git集成、CONVENTIONS.md | 开源免费 | 终端用户、自动化 |
| [OpenCode](./opencode) | 开源 Agent | 131K+ Stars、多模型 | 开源免费 | 开发者、隐私优先 |
| [Replit Agent](./replit) | 云端 IDE | Agent 4、全栈生成 | Free ~ Pro | 快速原型、团队协作 |

## 分类说明

### AI IDE（AI 原生编辑器）

深度集成 AI 能力的代码编辑器，提供沉浸式的 AI 编程体验：

- **[Cursor](./cursor)** - 最流行的 AI 编辑器，支持 Cloud Agents、Composer 2、.cursorrules 配置
- **[Windsurf](./windsurf)** - Cascade Flow 功能强大，实时预览特色鲜明

### IDE 插件 + 平台

在现有 IDE 和平台中添加 AI 能力：

- **[GitHub Copilot](./github-copilot)** - 业界标准，深度 GitHub 集成，现在有免费计划

### 对话式助手

通过对话方式进行编程辅助：

- **[Claude](./claude)** - 推理能力最强，支持 CLAUDE.md 配置，Claude Code 终端工具
- **[ChatGPT](./chatgpt)** - 通用性强，生态丰富，GPTs 商店

### 命令行工具

在终端中使用的 AI 编程工具：

- **[OpenCode](./opencode)** - 131K+ Stars，多平台支持，免费模型
- **[Aider](./aider)** - 开源免费，终端原生，Git 集成，CONVENTIONS.md 配置

### 规范驱动开发

让 AI 编码助手在写代码前先对齐需求的规范框架：

- **[OpenSpec](../openspec)** - 轻量级 SDD 框架，支持 20+ AI 工具，Propose → Apply → Archive 工作流

### 工程方法论

围绕 AI Agent 构建约束、反馈和质量保障的方法论：

- **[Harness Engineering](../harness-engineering)** - 缰绳工程：Prompt → Context → Harness 三层递进，让 AI Agent 安全高效运行的系统工程实践

### Web 开发工具

基于浏览器的 AI 开发工具：

- **[Replit Agent](./replit)** - 云端 IDE，支持全栈应用快速生成

## 核心功能对比

### 项目配置文件

| 工具 | 配置文件 | 用途 |
|------|---------|------|
| Cursor | `.cursorrules` | 定义编码规范、最佳实践 |
| Claude Code | `CLAUDE.md` | 项目规范、架构决策、编码标准 |
| Aider | `CONVENTIONS.md` | 编码约定和风格指南 |

### 模型支持

| 工具 | Claude | GPT | Gemini | DeepSeek | 本地模型 |
|------|--------|-----|--------|----------|---------|
| Cursor | ✓ Opus 4.6 | ✓ GPT-5.4 | ✓ Gemini 3 | - | - |
| GitHub Copilot | ✓ | ✓ GPT-5 mini | ✓ | - | - |
| Claude Code | ✓ Opus 4.6 | - | - | - | - |
| Aider | ✓ 3.7 Sonnet | ✓ o3-mini | - | ✓ R1 & V3 | ✓ Ollama |
| OpenCode | ✓ | ✓ | ✓ | - | ✓ |

## 选择建议

### 🎯 日常开发首选
- **Cursor** 或 **Windsurf** - 如果想要 AI 深度集成到编辑器
- **GitHub Copilot Free** - 预算有限时的入门选择

### 💰 预算有限
- **GitHub Copilot Free** - 免费计划，功能足够入门
- **Aider** - 开源免费，只需 API 费用
- **OpenCode** - 开源免费，多模型支持

### 🧠 复杂任务
- **Claude Opus 4.6** - 超强推理，适合架构设计
- **Cursor Agent 模式** - 端到端自主开发

### ⌨️ 终端爱好者
- **OpenCode** - 多平台，免费模型，社区活跃
- **Aider** - CLI 原生，Git 集成，高度可控
- **Claude Code** - Anthropic 官方终端工具

### 🏢 企业团队
- **GitHub Copilot Business** - 团队管理成熟
- **Cursor Business** - 隐私控制完善，企业级功能
- **Windsurf Enterprise** - 支持自托管

### 🚀 快速原型
- **Replit Agent** - 云端快速开发，团队协作

### 🎨 前端开发
- **Windsurf** - 实时预览，Cascade 模式
- **Cursor/Windsurf** - 全栈前端开发

## 趋势与展望 (2026)

1. **Agent 化** - 从辅助工具到自主执行者的发展趋势
2. **多模型支持** - 越来越多的工具支持多种 LLM
3. **上下文增强** - RAG 技术让 AI 更好理解代码库
4. **开源化** - OpenCode、Aider 等开源工具越来越受欢迎
5. **免费计划** - GitHub Copilot Free 等免费计划降低门槛
6. **云端化** - Cloud Agents 允许可并行处理任务
7. **配置文件** - 项目级配置文件（.cursorrules、CLAUDE.md）成为标准

## 相关资源

- [Cursor 官方文档](https://docs.cursor.com)
- [GitHub Copilot 文档](https://docs.github.com/copilot)
- [Claude API 文档](https://docs.anthropic.com)
- [Claude Code 文档](https://docs.anthropic.com/claude/docs/claude-code)
- [Aider 文档](https://aider.chat/docs)
- [OpenCode GitHub](https://github.com/anomalyco/opencode)
- [Replit 文档](https://docs.replit.com)
- [Windsurf 文档](https://docs.windsurf.com)
- **[Cursor vs OpenCode 对比](./comparison-cursor-opencode.md)** ⭐ 新增
