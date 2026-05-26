# 笔记库目录 taxonomy

本文件供 `note-ingest` skill 在步骤 3 定位目标路径时使用。决策优先级：**已有同主题目录 > 下表默认 > 询问用户**。

## 顶层目录映射

| 内容类型 | 首选目录 | 子目录示例 |
|---------|---------|-----------|
| CLI、编辑器、构建/包管理工具 | `tools/{tool}/` | `tools/git/`、`tools/vim/`、`tools/cmake/` |
| AI 编程方法论、Agent、Prompt/Context/Harness | `ai coding/` | `ai coding/openspec/`、`ai coding/harness-engineering/` |
| AI/ML/DL/LLM 理论与框架 | `artificial intelligence/` | `large language model/`、`machine learning/` |
| 学习笔记、实验记录、读书摘要 | `study record/` | `machine learning/`、`rpc/`、`reading/` |
| 编程语言、算法、数据结构、设计模式 | `basic programming/` | `python/`、`c++/`、`shell/` |
| OS、网络、架构、中间件、Linux | `computer science/` | `linux/`、`engineering architecture/` |
| 个人实验、硬件、运动、媒体 | `play/` | `unraid/`、`sports/` |
| 生活、待办、杂项 | `others/` | `life/`、`todo/` |

## 决策树

```
内容是否关于某个具体 CLI/IDE/工具？
  ├─ 是 → tools/{tool}/（目录名与工具名一致，小写）
  └─ 否 → 是否 AI 编程/Agent 工程实践？
           ├─ 是 → ai coding/{topic}/
           └─ 否 → 是否 ML/AI 理论或论文式笔记？
                    ├─ 偏理论/综述 → artificial intelligence/
                    ├─ 偏实验/踩坑/读书 → study record/
                    └─ 否 → 是否语言/算法/基础编程？
                             ├─ 是 → basic programming/
                             └─ 否 → 是否 CS 基础/系统/架构？
                                      ├─ 是 → computer science/
                                      └─ 否 → 是否个人生活/玩物？
                                               ├─ 是 → play/ 或 others/
                                               └─ 否 → others/ 并询问用户
```

## `artificial intelligence/` vs `study record/`

| 信号 | 选 `artificial intelligence/` | 选 `study record/` |
|------|------------------------------|-------------------|
| 语气 | 概念梳理、框架对比、综述 | 个人学习路径、实验记录 |
| 结构 | 偏教材/百科 | 偏日记/项目笔记 |
| 示例 | Transformer 原理、RL 算法族 | Kaggle 实验、读书摘要 |

不确定时优先 `study record/`，除非内容明显是通用知识库条目。

## 文件名惯例

| 场景 | 文件名 | 说明 |
|------|--------|------|
| 工具用法笔记 | `usage.md` | 同目录已有则 **append**，不新建 |
| 工具安装/配置 | `install.md`、`config.md` | 与目录内已有文件对齐 |
| 专题长文/译文/外链整理 | `{source-or-topic}.md` | kebab-case，如 `xiaolin-coding-harness-engineering.md` |
| 系列索引 | `README.md` | 目录入口，链到子文章 |
| 问题排查 | `problems.md` 或 `troubleshoot.md` | 参照同目录已有命名 |

## 目录内结构范例

**工具目录**（`tools/git/`）：
```
tools/git/
├── usage.md      # 主笔记，新内容优先合并
└── gitignore.md  # 子主题独立文件
```

**主题目录**（`ai coding/harness-engineering/`）：
```
ai coding/harness-engineering/
├── README.md                              # 索引 + 概述
└── xiaolin-coding-harness-engineering.md  # 独立长文
```

新建主题目录时：若预计有多篇相关文章，同时创建 `README.md` 作为索引。

## 禁止写入的路径

- `index.html`、`openspec/`、`.cache/`、`.git/`、`.opencode/node_modules/`
- 非 Markdown 二进制（图片除外，应放与 md 同目录并使用相对路径）

## 路径命名注意

- 保持仓库既有目录名，含空格的路径不改为 kebab-case（如 `ai coding/`、`study record/`、`vs code/`）
- 新建子目录名用小写英文，多词用空格或连字符与同级目录风格一致
