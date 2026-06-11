# `/learn <input>` — 学习新内容并入库

> 平台中立命令定义 · 事实源：CLAUDE.md / CHANGELOG V1.2
> 适配层：`.claude/commands/learn.md` 应为此文件的薄包装或符号链接

## 功能

将外部输入（文章、笔记、对话摘要、网页内容）学习后写入知识库。

## 涉及模块

M1（s-1.1-info-intake → s-1.3-kb-build）

## 执行流程

```
用户输入 → s-1.1 信息采集与处理 → s-1.3 知识库建设
```

1. **s-1.1 信息采集与处理**：解析输入结构、提取核心信息、标注来源与置信度
2. **s-1.3 知识库建设**：将处理后的信息写入 `knowledge-base/{category}/{date}-{slug}.md`，含完整 YAML frontmatter

## 输出

- `knowledge-base/{category}/{date}-{slug}.md` — 知识条目文件
- 更新 `_manifest.md`（如适用）

## 质量门

- `source_evidence` gate：验证信息来源可靠性（M1 节点）

## 依赖 Skill

| Skill | 路径 |
|-------|------|
| s-1.1-info-intake | `skills/m1-knowledge/s-1.1-info-intake.md` |
| s-1.3-kb-build | `skills/m1-knowledge/s-1.3-kb-build.md` |
