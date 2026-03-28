# Cursor

## 简介

Cursor 是目前最流行的 AI 原生代码编辑器，基于 VS Code 构建。被 NVIDIA、Stripe、OpenAI 等顶级公司的工程师广泛使用。

**Cursor 本质不是 IDE + AI，而是一个可编程的 AI Agent 系统。**

---

## 核心能力架构（4层模型）

```
① 模型层（LLM）
② 上下文层（Rules / Memory / Agents.md）
③ 能力层（Skills）
④ 工具层（MCP）
```

**一句话总结：**
- **Rules = 约束 & 长期记忆**
- **Skills = 可复用能力模块**
- **MCP = 外部工具系统**

---

## 一、Rules（规则系统）——"长期记忆 + 行为约束"

### 1. 本质

Rules 是 Cursor 最核心能力之一，解决：
- 每次都要重复 prompt
- AI 风格不一致
- 不理解项目约定

**Rules = Prompt 工程化**

### 2. Rules 类型

#### （1）Project Rules（最重要）
- 存在：`.cursor/rules/*.mdc`
- 特点：
  - 跟代码库绑定
  - 可 version control
  - 支持作用域（目录级）

**用途：**
- 代码规范
- 架构约束
- 业务知识

#### （2）User Rules
- 全局规则（类似 ChatGPT 的 system prompt）
- 例如：
  - "回答用中文"
  - "写 Go 代码必须加 context"

#### （3）Agent / AGENTS.md（轻量替代）
- 用 markdown 定义 agent 行为
- 比 rules 更简单

#### （4）Memory（自动生成规则）
- 从聊天中自动提取规则
- 类似"隐式规则"

### 3. Rule 的执行机制

Rules 会被插入到 prompt 最前面（system context），并按策略加载：

| 类型 | 触发方式 |
|------|---------|
| Always | 永远加载 |
| Auto Attached | 按文件匹配 |
| Agent Requested | AI 自己决定 |
| Manual | 手动 @ |

### 4. .cursorrules 示例

```
# 项目编码规范
- 使用 TypeScript
- 遵循 Airbnb 风格指南
- 所有函数必须有 JSDoc 注释
- 测试覆盖率 > 80%
```

---

## 二、Skills（技能系统）——"可复用能力插件"

### 1. 本质

Skills 是一组"结构化 prompt + workflow"，让 AI 会做某件事。

**Skills = 函数化 Prompt / Playbook**

### 2. 官方内置技能

- `/code-review` → 代码审查
- `/test` → 生成单测
- `/fix-merge-conflicts` → 修复合并冲突
- `/pr` → 自动生成 PR

### 3. Skills 核心特点

| 特性 | 说明 |
|------|------|
| 按需加载 | 不像 rules 常驻 |
| 可组合 | 可以 chaining |
| 可复用 | 跨项目使用 |
| 任务导向 | 一次解决一个问题 |

### 4. 心智模型

- **Rules = "法律 / 公司制度"**
- **Skills = "员工技能包"**

或者：
- **Rules = "长期人格"**
- **Skills = "临时能力"**

---

## 三、MCP（Model Context Protocol）——"工具扩展系统"

### 1. 本质

MCP 是一种标准协议，用来把外部工具接入 AI。

**LLM + Tool = Agent**

### 2. 能做什么

通过 MCP，Cursor 可以直接：
- 调 GitHub
- 调 Figma
- 调数据库
- 调内部 API

### 3. MCP vs Skills（核心区别）

| 对比 | Skills | MCP |
|------|--------|-----|
| 本质 | Prompt | Tool |
| 是否执行代码 | ❌ | ✅ |
| 是否标准化 | ❌ | ✅ |
| 可跨平台 | 弱 | 强 |
| 是否有 schema | 无 | 有 |

### 4. MCP 核心价值

#### （1）结构化工具调用
- 参数 schema
- 返回格式
- 错误定义

**AI 不用猜怎么调用**

#### （2）安全性
- 权限控制
- 不暴露 token

#### （3）生态化
- 一次开发，多 agent 复用

### 5. 配置示例

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"]
    }
  }
}
```

---

## 四、三者关系（最重要总结）

### 1. 统一心智模型

```
Rules → 决定"怎么做"
Skills → 决定"做什么"
MCP → 决定"用什么工具做"
```

### 2. 类比现实世界

| 系统 | 类比 |
|------|------|
| Rules | 公司制度 |
| Skills | 员工技能 |
| MCP | 外部工具 / API |

### 3. 实际工作流

一个复杂任务："帮我修 bug 并提 PR"

执行链路：
```
Rules → 约束风格/架构
Skills → /fix-bug /pr workflow
MCP → 调 git / GitHub API
```

---

## 五、Cursor 真正的核心能力

### 1. 代码库理解能力
- 全局索引
- 跨文件推理

### 2. Agent 化执行
- 多步任务拆解
- 自动修改代码

### 3. Context Engineering（核心）

**Cursor 真正厉害的点：不是模型，而是上下文管理**

包括：
- Rules（显式）
- Memory（隐式）
- Skills（任务化）
- MCP（工具化）

---

## 六、其他核心功能

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

### 多平台集成
- **BugBot** - GitHub PR 自动代码审查
- **Slack 集成** - 在 Slack 中直接调用 Cursor
- **CLI 工具** - 命令行中的 AI 助手
- **Mobile Agent** - 移动端访问云端代理

---

## 核心特性

- **最新模型** - GPT-5.4、Opus 4.6、Gemini 3 Pro、Grok Code
- **代码库理解** - RAG 技术索引整个项目
- **隐私模式** - 代码不会被存储用于训练
- **Marketplace** - 丰富的插件生态
- **企业级** - SOC 2 认证，自托管 Cloud Agents

---

## 最新动态

- **Mar 2026** - 自托管 Cloud Agents
- **Mar 2026** - Composer 2 发布
- **Feb 2026** - 自驾驶代码库研究预览

---

## 定价

- **Hobby（免费）** - 基础 AI 功能
- **Pro（$20/月）** - 无限快速请求，高级模型
- **Business（$40/用户/月）** - 团队管理，隐私控制

---

## 相关链接

- 官网：https://cursor.com
- 文档：https://docs.cursor.com
- 下载：https://cursor.com/download
- Marketplace：https://cursor.com/marketplace
- Rules 文档：https://docs.cursor.com/context/rules-for-ai
- MCP 文档：https://modelcontextprotocol.io

---

## 总结

**Cursor 的本质：**
- Rules = Prompt 工程化
- Skills = 能力模块化
- MCP = 工具协议化

**一个可编程的 AI Agent 系统**
