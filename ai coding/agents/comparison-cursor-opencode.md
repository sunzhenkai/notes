# Cursor vs OpenCode 对比

> 深度架构对比：从功能到本质

---

## 一、架构哲学差异

| 维度 | Cursor | OpenCode |
|------|--------|----------|
| **定位** | AI IDE | Agent Framework |
| **核心** | Context Engineering | Agent Execution |
| **强项** | 理解代码 | 执行任务 |
| **抽象层** | 高 | 更底层 |
| **开源** | ❌ 闭源 | ✅ 完全开源 |

---

## 二、核心能力映射

### 1. 四层架构对比

| 层级 | Cursor | OpenCode |
|------|--------|----------|
| **① 模型层** | 多模型支持 | 多模型支持 |
| **② 上下文层** | Rules / Memory / Agents.md | Context / Instructions |
| **③ 能力层** | Skills | Tasks / Plan |
| **④ 工具层** | MCP | Tools / Function Calling |

---

### 2. 功能映射表

| 功能 | Cursor | OpenCode | 说明 |
|------|--------|----------|------|
| **行为约束** | Rules | Instructions | 定义 AI 行为规范 |
| **任务模板** | Skills | Tasks / Plan | 可复用工作流 |
| **外部能力** | MCP | Tools | 调用外部工具 |
| **上下文** | Rules + Codebase Index + Memory | Context | 理解项目信息 |
| **执行引擎** | Cursor Agent（隐式） | Agent Runtime（显式） | 自动执行任务 |

---

## 三、核心系统对比

### 1. Rules vs Instructions

| 对比项 | Cursor Rules | OpenCode Instructions |
|--------|-------------|----------------------|
| **存储位置** | `.cursor/rules/*.mdc` | `instructions.md` 或 config |
| **版本控制** | ✅ 支持 | ✅ 支持 |
| **作用域** | 目录级 | 全局 |
| **触发方式** | Always / Auto / Manual | 自动加载 |

**基本等价** ✅

---

### 2. Skills vs Tasks/Plan

| 对比项 | Cursor Skills | OpenCode Tasks |
|--------|--------------|---------------|
| **类型** | 静态技能 | 动态规划 |
| **示例** | `/fix`, `/test` | Plan + Execute |
| **执行方式** | 用户触发 | AI 自动规划 |
| **灵活性** | 固定流程 | 动态调整 |

**⚠️ 差异：**
- Cursor：**静态技能**（预定义）
- OpenCode：**动态规划**（AI 自动拆解）

---

### 3. MCP vs Tools

| 对比项 | Cursor MCP | OpenCode Tools |
|--------|-----------|---------------|
| **协议** | 标准协议 | 非统一协议 |
| **生态** | 丰富 | 灵活 |
| **Schema** | ✅ 有 | ⚠️ 可选 |
| **跨平台** | ✅ 强 | ⚠️ 弱 |

**⚠️ 差异：**
- Cursor：**标准化**（生态强）
- OpenCode：**灵活性**（自由度高）

---

### 4. Agent 能力

| 对比项 | Cursor | OpenCode |
|--------|--------|----------|
| **自动化程度** | 半自动（用户触发） | 全自动（loop） |
| **人在 loop** | ✅ 是 | ❌ 否 |
| **任务执行** | 辅助 | 自主 |

**⚠️ 最大差异**

---

## 四、执行流程对比

### 场景：修复 bug

#### Cursor 流程

```text
1. 用户触发（/fix）
2. 加载 Rules
3. 执行 Skill
4. 调 MCP（可选）
5. 输出修改
```

**特点：**
- ✅ 人在 loop 中
- ✅ 偏辅助
- ✅ 理解代码强

---

#### OpenCode 流程

```text
1. 接收任务
2. 自动规划（Plan）
3. 循环执行：
   - 分析
   - 调 tool
   - 修改
   - 验证
4. 完成任务
```

**特点：**
- ✅ AI 在 loop 中
- ✅ 偏自动化
- ✅ 执行任务强

---

## 五、核心本质总结

### Cursor 的本质

> **Context 驱动的 AI 编程系统**

**核心：**
- Rules（行为约束）
- Codebase 理解（RAG）
- Prompt Engineering

**一句话：让 AI 更懂你的代码**

---

### OpenCode 的本质

> **Tool + Planning 驱动的 Agent 系统**

**核心：**
- Task planning（任务规划）
- Tool calling（工具调用）
- Execution loop（执行循环）

**一句话：让 AI 能自己干活**

---

## 六、使用场景建议

### 适合 Cursor 的场景

| 场景 | 原因 |
|------|------|
| ✅ 写业务代码 | 理解代码强 |
| ✅ 重构 | 上下文理解好 |
| ✅ Code review | 代码分析强 |
| ✅ 本地开发 | IDE 集成好 |

---

### 适合 OpenCode 的场景

| 场景 | 原因 |
|------|------|
| ✅ 自动修 bug | 自动化强 |
| ✅ 批量改代码 | 批量执行好 |
| ✅ DevOps 自动化 | 工具调用强 |
| ✅ 生成项目 | 任务规划强 |

---

## 七、终极对比（一句话）

| 工具 | 定位 |
|------|------|
| **Cursor** | **"我帮你写"** |
| **OpenCode** | **"我帮你做"** |

---

## 八、工程建议：混合架构

结合实际项目（Go / 分布式 / gRPC），建议采用混合架构：

```text
Cursor → 本地开发（Rules + Code理解）
OpenCode → CI / 自动修复 / 自动PR
MCP → 打通 GitHub / 服务治理
```

### 混合架构优势

1. **Cursor** - 日常开发、代码理解
2. **OpenCode** - 自动化任务、批量操作
3. **MCP** - 工具集成、生态扩展

---

## 九、选择决策树

```
需要什么？
├─ 理解代码、辅助编程 → Cursor
├─ 自动执行、批量操作 → OpenCode
├─ 团队协作、企业级 → Cursor Business
└─ 隐私优先、免费 → OpenCode
```

---

## 相关链接

- [Cursor 文档](./cursor/README.md)
- [OpenCode 文档](./opencode/README.md)
- [Cursor 官网](https://cursor.com)
- [OpenCode GitHub](https://github.com/anomalyco/opencode)
