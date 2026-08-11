# MVP 开放问题与决策门

本文区分已经确定的产品决策、实现前必须确认的技术决策，以及在真实 MVP 验证后再决定的扩展能力。

## 已确定

| 决策 | 状态 | 理由 |
|------|------|------|
| Agent Application 依赖 Agent Library | **已决定** | 避免两套 Agent Loop 和行为漂移 |
| Agent Library 不依赖 UI、Task、数据库和 Worker | **已决定** | 保持可嵌入和可复用 |
| 设计阶段保持语言和框架无关 | **已决定** | 先冻结产品语义和适配契约 |
| 实现阶段只选择一种原生语言和 Binding | **已决定** | 避免首版同时建设多语言 Runtime |
| Pi 只作为候选 Harness Adapter | **已决定** | Application 和公共 API 不绑定 Pi |
| Skill 使用 Library 公共契约与 Registry | **已决定** | Skill 资产不依赖 Harness 私有 API |
| UI 是 Agent Application MVP 必选项 | **已决定** | 完成长任务产品操作闭环 |
| 首版 Task Runtime 使用持久化存储、Lease 和恢复扫描 | **已决定** | 满足简单管理与进程重启恢复 |
| 首版不使用 Temporal | **已决定** | 当前任务不需要复杂 Workflow |
| Task 由一个或多个有界 Agent Run 推进 | **已决定** | 支持取消、预算和 checkpoint |
| Task 执行采用 at-least-once + 幂等 | **已决定** | 不做不现实的 exactly-once 承诺 |
| checkpoint/artifact 通过引用传递 | **已决定** | 避免大对象和敏感数据进入 Task/Event |

## 实现前决策门

这些问题不改变产品架构，但会影响第一版代码、部署和数据模型。

| 问题 | 当前建议 | 需要的证据 | 未决定的影响 |
|------|----------|------------|--------------|
| 原生实现语言 | 根据首批宿主与 Harness SDK 选择一种 | 宿主技术栈、团队能力、Pi 集成成本 | 无法确定 package 与进程模型 |
| 首个 Harness 及准确上游 | Pi 候选，但需锁定仓库、包、版本和许可 | SDK/嵌入能力、Skill/Event/Session 行为 | Adapter 范围无法冻结 |
| Agent Binding | 同语言优先 Local Binding | Agent App 与 Library 是否同语言/同进程 | 决定是否需要 HTTP/RPC |
| Web UI 技术栈 | 选择团队已有方案 | 部署环境、设计系统、实时事件需求 | 不影响 UI 产品范围 |
| Application API 传输 | HTTP/JSON；事件可选 SSE、WebSocket 或轮询 | 客户端环境和断线恢复需求 | 影响实时事件实现 |
| Task Store | 优先关系数据库或团队已有可靠存储 | 并发量、事务、锁和部署约束 | Lease/乐观锁实现无法确定 |
| 首个真实 Task | 可 checkpoint、可中断恢复的中等任务 | 输入、时长、Tool、副作用和结果形式 | 无法验证恢复闭环 |
| `AgentDefinition` 发布方式 | 版本化配置，只读加载 | 谁发布、如何回滚 | Task 版本固定不完整 |
| Session/Checkpoint Store | opaque ref + schema version | Harness 恢复能力和状态大小 | 跨 Attempt 恢复无法验证 |
| Artifact Store | 复用已有对象存储或文件服务 | 大小、权限、保留期 | 大结果无法稳定引用 |
| Event/Error 版本策略 | schema version + 向后兼容增量字段 | UI 与外部消费者类型 | 升级可能破坏 Timeline |
| Lease 参数 | 有限 Lease + 定期 Heartbeat | 任务耗时和 Worker 故障检测目标 | 恢复速度和误抢占风险未知 |

## MVP 验证后再决定

| 问题 | 触发条件 | 当前处理 |
|------|----------|----------|
| Remote Binding / 多语言 SDK | 出现不同语言的真实宿主 | 首版只实现一种 Binding |
| Temporal 或 Workflow Engine | 复杂 Signal、Timer、分支、补偿或数天任务 | 首版数据库 Durable Worker |
| 定时/周期任务 | 出现明确 schedule 用例 | 首版延后 |
| 多 Harness 路由 | 首个 Harness 无法满足已量化场景 | 保留 HarnessPort，不实现路由平台 |
| Harness 原生 Session 恢复 | 首个 Adapter 能力确认 | 公共 CheckpointRef 保持 opaque |
| 独立 Tool Activity | 出现高风险写操作或独立恢复需求 | 首版由有界 Agent Run 执行 |
| Sandbox | 需要 Shell、任意代码、浏览器或不可信依赖 | 未启用时明确拒绝 |
| Sandbox 技术选型 | 已确认隔离级别、启动延迟和成本目标 | 不提前选择具体产品 |
| 多环境 Worker | 需要测试/生产隔离或不同 capability | 首版单一可信执行环境 |
| 多 Agent DAG / 协同 Workspace | 单 AgentTask 无法满足真实业务 | 不进入两个 MVP |
| 复杂聊天工作台 | 任务型 UI 无法满足用户操作 | 首版只做任务闭环 UI |

## 运营与治理问题

以下事项不阻塞设计，但在生产试运行前必须有 Owner：

- Task、Attempt、AgentEvent、Artifact 和长期 Session 的保留期；
- 用户删除、租户隔离和敏感数据脱敏策略；
- 哪些 Tool 属于高风险写操作，哪些需要人工审批；
- 模型、Tool 和 Artifact 的成本配额及告警阈值；
- AgentDefinition、Skill、Policy 和执行配置的审批、发布与回滚；
- Lease 卡死、状态不确定副作用和人工恢复的值班流程；
- Library、Harness Adapter 与 Application 的版本兼容窗口和升级顺序。

## 决策原则

1. 先冻结语言无关语义，再选择最适合首个宿主的实现栈；
2. 每个适配层只隔离真实变化点，不为假设中的框架创建大而全抽象；
3. 优先用一个真实 Task 提供证据，不为假设场景建设平台能力；
4. 安全能力缺失时拒绝高风险操作，不降级到更弱隔离；
5. 公共契约冻结语义而非厂商、框架和部署细节；
6. 新能力默认作为外围 Adapter/Provider，不反向侵入 Agent Library；
7. 如果未来 Application 需要承载不使用 Agent 的通用任务，应另建产品边界。

## 相关文档

- [MVP 总览](./README.md)
- [MVP 1：通用 Agent Library](./agent-library-mvp.md)
- [MVP 2：独立长任务 Agent Application](./long-running-agent-app-mvp.md)
