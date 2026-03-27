# Cursor

## 简介

Cursor 是目前最流行的 AI 原生代码编辑器，基于 VS Code 构建。被 NVIDIA、Stripe、OpenAI 等顶级公司的工程师广泛使用。

## 核心功能

### Agent 模式
- **Cloud Agents** - 云端自主运行，可并行处理多个任务
- **Composer 2** - 新一代代码生成引擎，支持跨文件大规模修改
- **自主开发** - 独立完成规划、编码、测试、部署全流程

### 编辑器功能
- **Tab 补全** - 智能代码补全，支持多行生成
- **Cmd+K 编辑** - 选中代码后通过自然语言描述修改
- **Chat 对话** - 与 AI 对话，询问代码问题、调试、解释
- **@符号引用** - 引用文件、文件夹、文档等作为上下文
- **Apply 功能** - 一键将 AI 代码应用到当前文件

### 项目配置
- **.cursorrules** - 项目级 AI 规则配置文件，定义编码规范和最佳实践
- **Rules for AI** - 自定义 AI 行为规则，控制代码风格和输出格式
- **.cursor/目录** - 项目配置目录，存储设置和规则

### 多平台集成
- **BugBot** - GitHub PR 自动代码审查
- **Slack 集成** - 在 Slack 中直接调用 Cursor
- **CLI 工具** - 命令行中的 AI 助手
- **Mobile Agent** - 移动端访问云端代理

## 核心特性

- **最新模型** - GPT-5.4、Opus 4.6、Gemini 3 Pro、Grok Code
- **代码库理解** - RAG 技术索引整个项目
- **隐私模式** - 代码不会被存储用于训练
- **Marketplace** - 丰富的插件生态
- **企业级** - SOC 2 认证，自托管 Cloud Agents

## 配置示例

### .cursorrules 示例
```
# 项目编码规范
- 使用 TypeScript
- 遵循 Airbnb 风格指南
- 所有函数必须有 JSDoc 注释
- 测试覆盖率 > 80%
```

## 最新动态

- **Mar 2026** - 自托管 Cloud Agents
- **Mar 2026** - Composer 2 发布
- **Feb 2026** - 自驾驶代码库研究预览

## 定价

- **Hobby（免费）** - 基础 AI 功能
- **Pro（$20/月）** - 无限快速请求，高级模型
- **Business（$40/用户/月）** - 团队管理，隐私控制

## 相关链接

- 官网：https://cursor.com
- 文档：https://docs.cursor.com
- 下载：https://cursor.com/download
- Marketplace：https://cursor.com/marketplace
- Rules 文档：https://docs.cursor.com/context/rules-for-ai
