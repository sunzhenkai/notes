# MVP 开放问题与决策门

本文区分已经确定的架构决策、进入实现前必须确认的决策，以及可在真实 MVP 验证后再决定的事项。

## 已确定

| 决策 | 状态 | 理由 |
|------|------|------|
| 独立 Agent 应用依赖通用 Agent Library | **已决定** | 避免两套 Agent Loop 和行为漂移 |
| Library 以 npm package 交付 | **已决定** | 满足其他应用直接集成 |
| Library 不依赖 HTTP、Temporal 和具体存储 | **已决定** | 保持嵌入能力与基础设施无关 |
| 长任务由多个有界 Agent Slice 推进 | **已决定** | 支持恢复、取消、预算和 checkpoint |
| Workflow 只做确定性编排 | **已决定** | LLM、工具和 I/O 不可进入可重放逻辑 |
| Task 创建后固定 Definition 版本与 ExecutionTarget | **已决定** | 保证可重复、可审计且不可提权 |
| 长任务使用 at-least-once + 幂等 | **已决定** | 不做不现实的 exactly-once 承诺 |
| checkpoint/artifact 通过引用传递 | **已决定** | 避免大对象和敏感数据进入 Workflow/Event |

## 实现前决策门

这些问题不改变两个 MVP 的依赖方向，但会影响首个可运行版本的接口或部署。

| 问题 | 建议默认值 | 需要的证据 | 未决定的影响 |
|------|------------|------------|--------------|
| 首个普通 Library 宿主是什么 | 选现有 Node.js 后端或最小 CLI 宿主 | 一条真实 Agent Run 用例 | 无法验证 Library 是否真正可嵌入 |
| 首个长任务是什么 | 至少两个 Slice + 一次 Signal/等待 | 时长、外部系统、副作用和恢复目标 | 无法确定 MVP 2 的验收边界 |
| `AgentDefinition` 发布方式 | MVP 用版本化配置存储，只读加载 | 谁发布、如何回滚 | Task 版本固定机制不完整 |
| Task Store / Agent State Store | 先选团队已有关系库或 KV | 查询模式、数据量、保留期 | 状态 Owner 已知但实现端口未落定 |
| Artifact Store | 先选已有对象存储 | 文件大小、访问控制、保留期 | 大结果无法稳定引用 |
| ExecutionTarget 来源 | 可信服务配置映射 | 环境、Queue、capability、secret scope | Worker 路由与安全边界不完整 |
| checkpoint 最小 Schema | opaque ref + schema version | 首个任务恢复所需字段 | 跨版本恢复策略无法验证 |
| Event/Error 版本策略 | `schemaVersion` + 向后兼容增量字段 | 消费者类型和保留期 | Service/Library 升级可能破坏消费者 |

## MVP 验证后再决定

| 问题 | 触发条件 | 当前处理 |
|------|----------|----------|
| `RunAgentSliceActivity` 与 `ExecuteToolActivity` 粒度 | 出现高风险写工具、独立重试或高恢复成本 | 默认粗粒度 Slice |
| 是否实现 `scheduleTask` | 首个真实用例需要定时/周期触发 | 首版延后 |
| 是否引入 Sandbox | 需要 Shell、任意代码、浏览器或不可信依赖 | 未启用时明确拒绝 |
| Sandbox 技术选型 | 已确认隔离级别、启动延迟和成本目标 | 不提前选择 Kubernetes、microVM 或托管方案 |
| 单环境还是多环境 Worker | 需要隔离测试/生产或不同 capability | 先保留 ExecutionTarget，允许单环境部署 |
| Temporal Cluster / Namespace 策略 | 进入生产和多环境治理 | MVP 可使用共享 Cluster + 隔离 Namespace |
| 跨语言接入 | 出现非 Node.js 宿主 | 优先 HTTP Adapter，不重写 Agent Core |
| 多 Agent DAG / 协同 Workspace | 单 AgentTask 无法满足真实业务 | 不进入两个 MVP |
| 多 Harness 路由 | Pi 无法满足已量化场景 | RuntimeAdapter 保持可替换 |

## 运营与治理问题

以下事项不会阻塞架构文档，但在生产试运行前必须有 Owner：

- Task、Workflow History、Trace、Artifact 和长期 Memory 的保留期；
- 用户删除、租户隔离和敏感数据脱敏策略；
- 哪些 Tool 属于高风险写操作，哪些需要人工审批；
- 模型、Tool 和 Artifact 的成本配额及告警阈值；
- Definition、Policy、ExecutionTarget 的审批、发布和回滚流程；
- Task 卡死、状态不确定副作用和人工恢复的值班流程；
- Library 与独立应用的版本兼容窗口和升级顺序。

## 决策原则

1. 优先用一个真实任务提供证据，不为假设场景建设平台能力；
2. 安全能力缺失时拒绝高风险操作，不降级到更弱隔离；
3. 公共契约冻结语义而非厂商和部署细节；
4. 新能力默认作为外围 Provider，不反向侵入 Agent Library；
5. 如果未来独立应用需要承载不使用 Agent 的通用任务，应另建通用任务产品边界，而不是扩张本 MVP。

## 相关文档

- [MVP 总览](./README.md)
- [MVP 1：通用 Agent Library](./agent-library-mvp.md)
- [MVP 2：独立长任务 Agent 应用](./long-running-agent-app-mvp.md)
