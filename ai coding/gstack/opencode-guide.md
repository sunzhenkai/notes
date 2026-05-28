# GStack × OpenCode 使用教程

> 在 OpenCode 中使用 gstack 的快速上手指南。

---

## 一、安装

### 前置条件

- [OpenCode](https://opencode.ai) 已安装
- [Git](https://git-scm.com/) 已安装
- [Bun](https://bun.sh/) v1.0+ 已安装

### 安装 gstack

```bash
# 克隆并安装到 OpenCode
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/gstack
cd ~/gstack && ./setup --host opencode
```

技能安装到：`~/.config/opencode/skills/gstack-*/`

### 升级

```bash
cd ~/gstack && git pull && ./setup --host opencode
```

或在会话中直接使用 `/gstack-upgrade`。

---

## 二、项目配置

在项目根目录的配置文件中添加 gstack 技能列表。OpenCode 通常使用 `AGENTS.md` 或 `instructions.md`：

```markdown
## gstack

可用技能：/office-hours, /plan-ceo-review, /plan-eng-review, /plan-design-review,
/design-consultation, /design-shotgun, /design-html, /review, /ship, /land-and-deploy,
/canary, /benchmark, /browse, /qa, /qa-only, /design-review, /setup-browser-cookies,
/setup-deploy, /retro, /investigate, /document-release, /document-generate, /codex,
/cso, /autoplan, /careful, /freeze, /guard, /unfreeze, /gstack-upgrade, /learn.
```

---

## 三、常用技能速查

### 🎯 最常用的 6 个技能

| 技能 | 何时用 | 示例 |
|------|--------|------|
| `/office-hours` | 有新想法，不知道从哪开始 | "我想做个日程管理工具" → `/office-hours` |
| `/autoplan` | 想法明确，要快速出方案 | `/autoplan` 自动跑完 CEO + 设计 + 工程审查 |
| `/review` | 写完代码，要质量检查 | 在有改动的分支上 `/review` |
| `/qa` | 部署后要验证 | `/qa https://staging.myapp.com` |
| `/ship` | 准备发布 | `/ship` 自动测试 + 推送 + 开 PR |
| `/browse` | 需要看到真实页面 | `$B goto https://myapp.com` |

### 按场景选择

```
有新想法     → /office-hours → /autoplan
写完代码     → /review
发现 bug     → /investigate
要测试页面   → /qa
要发布       → /ship
要写文档     → /document-release
要安全审计   → /cso
```

---

## 四、实战工作流

### 工作流 1：从零开始做一个功能

```
1. /office-hours          ← 描述想法，六问重塑需求
2. /autoplan              ← 自动跑完所有审查，生成计划
3. [按计划实现代码]        ← 正常编码
4. /review                ← Staff Engineer 审查代码
5. /qa https://staging... ← 真实浏览器测试
6. /ship                  ← 测试 + 推送 + 开 PR
```

### 工作流 2：快速修复 bug

```
1. /investigate           ← 系统性根因分析（不改代码，先查原因）
2. [修复代码]
3. /review                ← 审查修复质量
4. /ship                  ← 发布
```

### 工作流 3：安全审计

```
1. /cso                   ← OWASP Top 10 + STRIDE 威胁模型
2. /review                ← 修复发现的问题
3. /ship                  ← 发布
```

### 工作流 4：并行开发（搭配 Conductor）

gstack 的流程化设计天然支持并行。10-15 个 Sprint 同时跑：

- Session 1：`/office-hours` 新想法
- Session 2：`/review` 已完成的 PR
- Session 3：`/qa` 测试 staging
- Session 4-15：各自在不同分支上实现功能

---

## 五、浏览器测试（/browse）

gstack 内置了真实 Chromium 浏览器，这是它区别于其他工具的核心能力之一。

### 基本操作

```bash
# 设置检查（每次会话第一次使用前跑一次）
$B status

# 导航
$B goto https://myapp.com

# 查看页面交互元素（推荐第一步）
$B snapshot -i

# 点击 / 填写
$B click @e3
$B fill @e4 "test@example.com"

# 截图
$B screenshot /tmp/page.png

# 读取控制台错误
$B console --errors

# 检查网络请求
$B network
```

### 验证部署

```bash
$B goto https://myapp.com
$B text                    # 页面加载了吗？
$B console                 # 有 JS 错误吗？
$B is visible ".hero"      # 关键元素在吗？
$B screenshot /tmp/check.png
```

### 响应式测试

```bash
$B responsive /tmp/layout  # 一次截图：手机 / 平板 / 桌面
```

### 注意事项

- `$B` 是浏览器的简写变量，由 gstack 自动配置
- 首次使用需要构建（约 10 秒），`./setup` 会自动处理
- 浏览器在 30 分钟空闲后自动关闭
- 会话间保持状态（cookies、tabs）

---

## 六、注意事项

### OpenCode 特有

1. **技能前缀**：默认技能无前缀（`/qa`、`/review`）。如需前缀可 `./setup --host opencode --prefix`，变为 `/gstack-qa`
2. **配置文件**：OpenCode 使用 `~/.config/opencode/` 目录，技能安装在 `~/.config/opencode/skills/` 下
3. **模型选择**：gstack 的 `/codex`（第二意见）在 OpenCode 中使用时，需要 OpenAI API Key
4. **Proactive 模式**：首次运行会问是否开启自动建议。说"stop suggesting"可以关闭

### 通用

1. **安装后重跑 setup**：每次 `git pull` 后建议重跑 `cd ~/gstack && ./setup --host opencode`
2. **Telemetry**：默认关闭，首次运行会询问
3. **Checkpoint 模式**：可选自动保存进度（`gstack-config set checkpoint_mode continuous`）
4. **卸载**：`cd ~/gstack && ./setup --uninstall` 或手动删除 `~/.config/opencode/skills/gstack-*/`

---

## 七、快速命令卡

```
# 安装
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/gstack
cd ~/gstack && ./setup --host opencode

# 升级
cd ~/gstack && git pull && ./setup --host opencode

# 最小可用流程
/office-hours → /autoplan → [编码] → /review → /ship

# 测试部署
/browse → $B goto <url> → $B snapshot -i → $B console

# 安全审计
/cso

# 周报
/retro
```

---

## 相关资源

- [gstack 概览](./README.md) — 完整的 gstack 介绍
- [gstack GitHub](https://github.com/garrytan/gstack) — 源码和文档
- [OpenCode 官网](https://opencode.ai) — OpenCode 官方
- [Conductor](https://conductor.build) — 并行 Sprint 管理
