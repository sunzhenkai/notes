# Aider

## 简介

Aider 是开源的 AI 结对编程命令行工具，在终端中与 AI 协作编辑代码。在 OpenRouter 上排名第一，是终端用户的首选 AI 编程工具。Aider 88% 的新代码由 Aider 自己编写。

## 核心功能

### 文件管理
- **/add** - 添加文件到聊天会话
- **/drop** - 从会话中移除文件
- **多文件编辑** - 同时编辑多个相关文件
- **自动上下文** - 自动拉取相关文件的上下文

### Git 集成
- **自动 commit** - 自动生成 git commit
- **语义化提交** - 生成语义化的 commit message
- **/undo** - 撤销 AI 的更改
- **diff 查看** - 清晰展示每次代码变更

### 代码操作
- **代码重构** - 批量重命名变量、函数等
- **测试生成** - 自动生成测试代码
- **代码库地图** - 自动创建整个代码库的地图
- **100+ 语言支持** - Python, JavaScript, Rust, Go, C++ 等

### 高级特性
- **图像支持** - 添加截图、设计图等视觉上下文
- **网页支持** - 添加网页作为参考文档
- **语音输入** - 语音命令进行编程
- **自动 Lint 和测试** - 每次修改后自动运行
- **Watch 模式** - 监听文件变化，自动响应
- **复制粘贴模式** - 与任何 Web Chat 配合使用
- **CONVENTIONS.md** - 指定编码规范

### 模型支持
- **Claude 3.7 Sonnet** - 效果最好
- **DeepSeek R1 & Chat V3** - 高性价比
- **OpenAI o1, o3-mini, GPT-4o** - OpenAI 系列
- **本地模型** - 支持 Ollama 等本地模型
- **75+ LLM 提供商** - 几乎所有主流模型

## 核心特性

- **完全开源** - Apache 2.0 许可，可自托管
- **终端原生** - 适合命令行用户，高效快捷
- **精确控制** - 清晰展示每次代码变更
- **轻量级** - 无需安装 IDE，适合服务器环境
- **隐私可控** - 可使用本地模型，代码不出境
- **88% 自身代码** - Aider 88% 的新代码由 Aider 自己编写

## 使用示例

```bash
# 安装
python -m pip install aider-install
aider-install

# 进入项目
cd /to/your/project

# 使用 Claude 3.7 Sonnet
aider --model sonnet --api-key anthropic=<key>

# 使用 DeepSeek
aider --model deepseek --api-key deepseek=<key>

# 添加文件
aider factorial.py

# 在聊天中使用
> Make a program that asks for a number and prints its factorial

# 添加文件
> /add file1.py file2.py

# 移除文件
> /drop file1.py

# 撤销更改
> /undo
```

## CONVENTIONS.md 示例

```markdown
# 编码规范

- 使用 4 空格缩进
- 函数名使用 snake_case
- 类名使用 PascalCase
- 所有公共函数必须有 docstring
```

## 统计数据

- **42.4k** GitHub Stars
- **5.7M+** 安装次数
- **15B** tokens/周
- **OpenRouter Top 20** 应用排名

## 定价

- **开源免费** - 软件本身完全免费
- **API 费用** - 需要自行承担 LLM API 费用

## 相关链接

- GitHub：https://github.com/Aider-AI/aider
- 官网：https://aider.chat
- 文档：https://aider.chat/docs
- 安装指南：https://aider.chat/docs/install.html
- 使用教程：https://aider.chat/docs/usage.html
- Discord：https://discord.gg/Y7X7bhMQFV
- LLM 排行榜：https://aider.chat/docs/leaderboards/
