# `/validate <topic>` — 选题验证与日历

> 平台中立命令定义 · 事实源：CLAUDE.md / CHANGELOG V1.2
> 适配层：`.claude/commands/validate.md` 应为此文件的薄包装或符号链接

## 功能

验证单个选题的价值、可操作性和受众匹配度，并排期。

## 涉及模块

M2（s-2.2-topic-validate）

## 品牌契约

选题验证应参考 `data/brand/brand-canon.yaml` 中的受众定义（Lily/Marcus），确保选题受众匹配度评估基于活跃品牌口径。

## 执行流程

```
选题 → 可操作性评估 → 受众匹配度 → 竞品差异化 → 价值评分 → 排期
```

1. **可操作性评估**：选题是否可转化为具体内容（素材可得性、创作路径清晰度）
2. **受众匹配度**：是否符合 Lily/Marcus 的核心关注
3. **竞品差异化**：同主题已有内容的覆盖程度
4. **价值评分**：综合打分（≥7 分入选）
5. **排期**：纳入内容日历

> 自 V1.2 起，终稿验证增加了事实核查维度（调用 s-3.4.1-fact-check）

## 输出

- `data/topics/topics.json` — 更新选题池
- `data/pipeline/validate-{id}/validation-report.md` — 验证报告
- `data/pipeline/validate-{id}/_manifest.md`

## 质量门

- `workflow_consistency` gate：验证流程完整性

## 依赖 Skill

| Skill | 路径 |
|-------|------|
| s-2.2-topic-validate | `skills/m2-topic/s-2.2-topic-validate.md` |
