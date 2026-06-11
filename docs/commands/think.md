# `/think <input>` — 交互式深度思考（P1-P4 → 深度对话 → 三重输出）

> 平台中立命令定义 · 事实源：CLAUDE.md / CHANGELOG V1.2
> 适配层：`.claude/commands/think.md` 应为此文件的薄包装或符号链接

## 功能

对输入进行四层深度思考（P1→P4），随后进入开放式深度对话（a-1.2.5），最终产出三重输出。

## 涉及模块

M1（a-1.2.1 → a-1.2.2 → a-1.2.3 → a-1.2.4 → a-1.2.5）

## 执行流程

```
用户输入
  → a-1.2.1 第一层：现象描述（What）
  → a-1.2.2 第二层：结构分析（How）
  → a-1.2.3 第三层：本质追问（Why）
  → a-1.2.4 第四层：意义生成（So What）
  → [自动过渡] → a-1.2.5 深度对话 + 收割
```

### 对话风格规则

- 苏格拉底式追问，不急于给出答案
- 每轮以问题结尾，引导用户深入
- 适时引入哲学/心理学视角（如拉康、韩炳哲、有限性等）

### 三重输出

1. **思考报告**：P1-P4 的结构化分析记录
2. **收割产出**：从对话中提取的洞察、概念、选题种子
3. **行动建议**：基于思考的可操作下一步

> 详细对话风格、输出格式和逐章白皮书生成规则见 `skills/m1-knowledge/a-1.2.5-dialogue-harvest.md`

## 输出

- `data/pipeline/think-{id}/p1-p4-deep-think.md` — P1-P4 思考记录
- `data/pipeline/think-{id}/dialogue-harvest.md` — 对话收割产出
- `data/pipeline/think-{id}/_manifest.md` — 文件索引

## 质量门

- `workflow_consistency` gate：验证流程完整性

## 依赖 Skill

| Skill | 路径 |
|-------|------|
| a-1.2.1 → a-1.2.4 | 集成于 `skills/m1-knowledge/a-1.2-deep-think.md` |
| a-1.2.5-dialogue-harvest | `skills/m1-knowledge/a-1.2.5-dialogue-harvest.md` |
