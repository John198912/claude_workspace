# `/review <period>` — 数据复盘

> 平台中立命令定义 · 事实源：CLAUDE.md / CHANGELOG V1.2
> 适配层：`.claude/commands/review.md` 应为此文件的薄包装或符号链接

## 功能

按时间周期对已发布的内容进行数据复盘分析。

## 涉及模块

M5（s-5.1.1 → s-5.2 → s-5.3）

## 执行流程

```
指定周期 → s-5.1.1 数据采集 → s-5.2 复盘分析 → s-5.3 策略优化
```

1. **s-5.1.1 数据采集**：收集指定周期内的平台数据（阅读量、互动率、转化等）
2. **s-5.2 复盘分析**：识别高/低表现内容，提取规律
3. **s-5.3 策略优化**：基于复盘结论调整内容策略

## 参数

- `<period>`：时间范围，例如 `上周`、`本月`、`2026-05`、`最近 7 天`

## 质量门

- `data_quality` gate：验证数据质量与因果结论纪律（M5 节点）
  - 因果纪律：无 A/B 或实验设计禁止输出 `causal` 结论
  - 结论分型：`descriptive | correlational | causal`

## 输出

- `data/pipeline/review-{id}/data-collection.md` — 采集数据
- `data/pipeline/review-{id}/review-report.md` — 复盘报告
- `data/pipeline/review-{id}/optimization-strategy.md` — 优化策略
- `data/pipeline/review-{id}/_manifest.md`

## 依赖 Skill

| Skill | 路径 |
|-------|------|
| s-5.1.1-data-collect | `skills/m5-feedback/s-5.1.1-data-collect.md` |
| s-5.2-review-engine | `skills/m5-feedback/s-5.2-review-engine.md` |
| s-5.3-optimize | `skills/m5-feedback/s-5.3-optimize.md` |
