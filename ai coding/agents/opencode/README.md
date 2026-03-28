# OpenCode

## 简介

OpenCode 是目前最流行的开源 AI 编程 Agent，拥有 **131K+ GitHub Stars**。支持终端、桌面应用和 IDE，完全免费且开源。

**OpenCode 本质不是 IDE，而是一个 Agent Framework。**

---

## 核心能力架构（4层模型）

```
① 模型层（LLM）
② 上下文层（Context / Instructions）
③ Agent层（Task / Plan / Execution）
④ 工具层（Tool / Function Calling）
```

**一句话总结：**
- **Instructions = 行为约束**
- **Tasks/Plan = 任务规划**
- **Tools = 外部能力**

---

## 一、Instructions（指令系统）——"行为约束"

### 1. 本质

持久化 Prompt + Agent 行为定义，类似：
- system prompt
- 项目约束
- 行为规范

### 2. 形态

OpenCode 通常是：
- `instructions.md`
- 或 config 内定义 system prompt

### 3. 能力点

- 约束输出格式
- 约束编码风格
- 定义 agent 行为（比如：必须先分析再改代码）

---

## 二、Tasks / Plan（任务规划）——"任务拆解执行"

### 1. 本质

把复杂任务拆解成步骤，并执行。

### 2. 能力点

- 自动拆解任务（Plan）
- 多步骤执行（Chain-of-Thought / ReAct）
- 状态推进（step by step）

### 3. 示例

```text
用户：修复这个 bug

OpenCode：
1. 分析代码
2. 找问题
3. 提修改
4. 写 patch
5. 验证
```

---

## 三、Tools（工具系统）——"外部能力"

### 1. 本质

LLM 调用外部能力（函数 / API）。

### 2. 支持能力

- function calling
- shell 执行
- 文件操作
- HTTP API

### 3. 示例

```json
{
  "name": "read_file",
  "args": { "path": "main.go" }
}
```

---

## 四、Context（上下文系统）——"信息提供"

### 1. 本质

给模型提供"当前需要理解的信息"。

### 2. 包括

- 当前文件
- 选中代码
- 历史对话
- 检索内容（RAG）

---

## 五、Agent Runtime（核心差异点）

这是 OpenCode 很关键的一层：**真正的"Agent 执行引擎"**。

### 能力

- 循环执行（loop）
- tool 调用决策
- 状态管理
- 错误重试

---

## 核心特性

- **完全开源** - GitHub 开源，社区驱动
- **隐私优先** - 不存储任何代码或上下文数据
- **免费使用** - 基础功能完全免费
- **灵活部署** - 支持隐私敏感环境
- **社区活跃** - 800+ 贡献者，10,000+ commits
- **多模型** - 支持几乎所有主流 AI 模型

---

## 安装方式

```bash
# curl
curl -fsSL https://opencode.ai/install | bash

# npm
npm install -g opencode

# bun
bun install -g opencode

# brew
brew install opencode

# paru (Arch Linux)
paru -S opencode
```

---

## 使用场景

- 日常编程开发
- 代码审查
- 调试问题
- 学习新技术
- 团队协作
- 隐私敏感项目
- **自动修 bug**
- **批量改代码**
- **DevOps 自动化**
- **生成项目**

---

## 统计数据

- **131,000+** GitHub Stars
- **800+** Contributors
- **10,000+** Commits
- **5M+** 每月活跃开发者

---

## 定价

- **Free** - 开源免费，基础功能
- **Zen** - 优化模型服务（付费）
- **Enterprise** - 企业级支持和部署

---

## 相关链接

- 官网：https://opencode.ai
- GitHub：https://github.com/anomalyco/opencode
- 文档：https://opencode.ai/docs
- 下载：https://opencode.ai/download
- Discord：https://opencode.ai/discord
- X/Twitter：https://x.com/opencode
