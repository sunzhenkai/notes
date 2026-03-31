# 多语言指南

配置 OpenSpec 以英语以外的语言生成工件。

## 快速设置

将语言指令添加到你的 `openspec/config.yaml`：

```yaml
schema: spec-driven

context: |
  Language: Portuguese (pt-BR)
  All artifacts must be written in Brazilian Portuguese.

  # 你的其他项目上下文在下面...
  Tech stack: TypeScript, React, Node.js
```

就是这样。所有生成的工件现在都将使用葡萄牙语。

## 语言示例

### Portuguese (Brazil)

```yaml
context: |
  Language: Portuguese (pt-BR)
  All artifacts must be written in Brazilian Portuguese.
```

### Spanish

```yaml
context: |
  Idioma: Español
  Todos los artefactos deben escribirse en español.
```

### Chinese (Simplified)

```yaml
context: |
  语言：中文（简体）
  所有产出物必须用简体中文撰写。
```

### Japanese

```yaml
context: |
  言語：日本語
  すべての成果物は日本語で作成してください。
```

### French

```yaml
context: |
  Langue : Français
  Tous les artefacts doivent être rédigés en français.
```

### German

```yaml
context: |
  Sprache: Deutsch
  Alle Artefakte müssen auf Deutsch verfasst werden.
```

## 提示

### 处理技术术语

决定如何处理技术术语：

```yaml
context: |
  Language: Japanese
  Write in Japanese, but:
  - Keep technical terms like "API", "REST", "GraphQL" in English
  - Code examples and file paths remain in English
```

### 与其他上下文结合

语言设置与你的其他项目上下文一起工作：

```yaml
schema: spec-driven

context: |
  Language: Portuguese (pt-BR)
  All artifacts must be written in Brazilian Portuguese.

  Tech stack: TypeScript, React 18, Node.js 20
  Database: PostgreSQL with Prisma ORM
```

## 验证

要验证你的语言配置是否工作：

```bash
# 检查说明 - 应该显示你的语言上下文
openspec instructions proposal --change my-change

# 输出将包括你的语言上下文
```

## 相关文档

- [自定义指南](./customization.md) - 项目配置选项
- [工作流程指南](./workflows.md) - 完整工作流程文档
