# Harness Engineering 详解（小林coding）

> 来源：[小林coding《鹅厂面试官："你怎么看 Harness Engineering？"》](https://mp.weixin.qq.com/s/9cKWyTcK-BORuyn1JK4Ysw)
> 原文地址：<https://mp.weixin.qq.com/s/9cKWyTcK-BORuyn1JK4Ysw>
> 日期：2026 年 3-4 月

## 概述

Harness Engineering（驾驭工程/缰绳工程）是继 Prompt Engineering 和 Context Engineering 之后的 AI 工程第三阶段，核心是设计一整套包裹模型的运行环境，让模型在真实执行中"持续做对"一连串的事。

## 三阶段演进关系

| 阶段 | 核心问题 | 边界 |
|------|---------|------|
| **Prompt Engineering** | 怎么让模型"听懂"你想干啥 | 对"指令"的工程化 |
| **Context Engineering** | 怎么让模型"知道"该用什么信息 | 对"输入环境"的工程化 |
| **Harness Engineering** | 怎么让模型"持续做对"一连串的事 | 对"整个运行系统"的工程化 |

**三者是包含关系**：Prompt ⊂ Context ⊂ Harness

### 经典公式

```
Agent = Model + Harness
Harness = Agent − Model
```

## 起源

- **Mitchell Hashimoto**（2026.2.5 博客《My AI Adoption Journey》）首次提出：每次 Agent 犯错，花时间工程化一个方案让它永不再犯
- **OpenAI**（一周后官方博客《Harness engineering: leveraging Codex in an agent-first world》）：3 人团队，5 个月，0 行手写代码，产出 100 万行代码 + 1500 PR

## Harness 六层架构

按功能分三组：

### 输入侧（让模型看到正确的东西）

**第一层：上下文精细化管理**
- 核心问题：模型**这一轮**该看到什么？
- 关键：动态筛选而非一次塞满，结构化组织（固定规则 / 动态证据 / 中间结论三者分开）
- 概念：context rot（上下文腐化）——信息越多注意力越散
- 解法：just-in-time retrieval（按需抓取信息）

**第四层：记忆与状态的分层管理**
- 核心问题：模型**跨轮**该记住什么？
- 关键洞察：Agent 的状态不应放在上下文窗口里，而应**外化到文件系统**
- 三类记忆（生命周期不同）：任务状态（`today-progress.json`）→ 会话中间结果 → 长期记忆（`user-preferences.md` / `CLAUDE.md`）

### 动作侧（让模型做出正确的事）

**第二层：工具系统的可控调用**
- 核心问题：模型**用什么**动手？
- 三个要点：给哪些工具、何时用哪个、工具结果如何喂回模型
- 反常识：工具不是越多越好，OpenAI 砍掉大半后效果反而提升
- 相关概念：MCP（Model Context Protocol）标准化工具接口

**第三层：任务执行的全局编排**
- 核心问题：模型**下一步**该干啥？
- 本质：Agent = for 循环（思考 → 行动 → 观察 → 再思考），即 ReAct 模式
- 常见编排模式：Plan-and-Execute、Reflexion、Tree of Thoughts

### 校验侧（让模型知道对错 + 出错能爬起来）

**第五层：独立的评估与观测体系**
- 核心问题：模型**做得好不好**有没有尺子？
- **尺子（Eval 集）**：手写一批典型任务 + 标注正确答案，每次改动后跑一遍对比
- **量（Trace + 日志 + 指标）**：能看到每一步决策、工具调用、token 消耗
- 案例：LangChain Terminal Bench 从 52.8 → 66.5，排名 30+ → Top 5，靠的就是 Eval + trace

**第六层：约束校验与失败恢复机制**
- 核心问题：模型**出错了**能不能爬起来？
- 约束：硬编码到代码/linter，不依赖提示词（如"token 超过 10 万立刻停"）
- 校验：每步输出前后自动检查（格式校验、白名单检查）
- 恢复：每种典型失败都有明确恢复路径（限流→重试，发送失败→本地队列）

### 六层的实际用法

六层不是一次搭完的清单，而是一张**路标**——每次 Agent 犯错，修复落到哪一层：

| 现象 | 修复层 |
|------|--------|
| 漏掉某个上下文信息 | 第一层 |
| 总是用错工具 | 第二层 |
| 步骤乱 | 第三层 |
| 跨天记不住进度 | 第四层 |
| 无法判断做得好不好 | 第五层 |
| 一失败就崩溃 | 第六层 |

## 五大工程难题与原则

### 难题一：Agent 跑久了越走越偏

- **现象**：上下文焦虑（Context Anxiety）——模型感觉上下文快满，开始匆忙收尾、跳过验证，急于宣布完成
- **解法**：Context Reset（上下文重置）——丢旧窗口换新窗口，状态外化到文件系统（`claude-progress.txt`、`init.sh`、git history）
- **原则一**：**重启胜过修补，状态沉到文件里**

### 难题二：Agent 自评总偏乐观

- **现象**：让 Agent 自己评估自己，永远觉得干得不错
- **解法**：Anthropic 三角分工——Planner（规划）→ Generator（生成）→ Evaluator（验收），Evaluator 必须像 QA 一样真测
- **原则二**：**生产和验收必须分离，验收方要能摸到真实世界**

### 难题三：Agent 反复失败，工程师该干啥

- **核心转变**：工程师不写代码，而是：①拆解任务 ②补充环境缺失的能力 ③建立反馈链路
- **原则三**：**别问模型能不能更努力，要问环境还缺什么**

### 难题四：规范文件越写越长，Agent 反而更糊涂

- **现象**：把全部规范塞进 AGENTS.md，Agent 注意力稀释
- **解法**：AGENTS.md 从"百科全书"改为"目录页"（~100 行），详细内容拆到子文档，按需加载
- **原则四**：**规则文件宁缺毋滥，少即是多**

### 难题五：Agent 写的代码越堆越烂

- **现象**：AI slop（代码泔水）——Agent 模仿仓库已有代码模式，好的和坏的都复制；人力清理速度跟不上 Agent 产出
- **解法**：Golden Principles（黄金原则）固化人类经验 + 后台 Agent 定期扫描自动修复 PR（技术债每天小额还，不攒着集中还）
- **原则五**：**技术债不是攒一堆集中还，而是每天自动偿还一点**

### 反直觉发现：Agent 用"老技术"反而更稳

- 原因：组合性好、API 稳定、训练数据多
- 实践：OpenAI 主动选"boring"技术栈，宁愿自写小工具函数也不引入 Agent 看不懂的第三方包

## 五条原则口诀

> 重启胜过修补，生产验收分家，与其催模型不如改环境，规则宁缺毋滥，技术债天天还。

## 核心洞察

1. 同样用 Claude/GPT，团队效果差异不在模型，而在围绕模型搭的那套东西有没有做到位
2. 模型决定 Agent 天花板的**高度**，Harness 决定能不能**落地**
3. 工程师的价值转向：从"我一天写多少行代码"到"我能为 Agent 设计多好的运行环境"
4. AI 落地核心挑战：从"让模型更聪明"转向"让模型在真实世界稳定工作"

## 参考资料

- Mitchell Hashimoto, [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey)
- OpenAI, [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- LangChain, [Improving Deep Agents with harness engineering](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/)
- Cognition, [Rebuilding Devin for Claude Sonnet 4.5](https://cognition.ai/blog/devin-sonnet-4-5-lessons-and-challenges)
