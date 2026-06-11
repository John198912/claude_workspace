# `/topic-mine` — 多源选题挖掘

> 平台中立命令定义 · 事实源：CLAUDE.md / CHANGELOG V1.2
> 适配层：`.claude/commands/topic-mine.md` 应为此文件的薄包装或符号链接

## 功能

从知识库、热点、竞品分析等多个来源挖掘选题，产出候选选题列表。

## 涉及模块

M1（知识积累）→ M2（s-2.1-topic-mine）

## 品牌契约

选题挖掘应参考 `data/brand/brand-canon.yaml` 中的内容支柱和受众定义，确保选题方向与品牌定位对齐。

## 执行流程

```
知识库扫描 → 热点识别 → 竞品分析 → 选题合并去重 → 选题池输出
```

1. 扫描 knowledge-base 中近期条目，识别潜在选题方向
2. 结合 web-search 识别当前热点话题
3. 分析竞品/同领域创作者的覆盖空白
4. 合并去重后输出候选选题列表

## 输出

- `data/pipeline/topic-mine-{id}/mining-report.md` — 挖掘报告
- `data/pipeline/topic-mine-{id}/candidate-topics.md` — 候选选题列表
- `data/pipeline/topic-mine-{id}/_manifest.md` — 文件索引
- 可选：更新 `data/topics/topics.json`

## 依赖 Skill

| Skill | 路径 |
|-------|------|
| s-2.1-topic-mine | `skills/m2-topic/s-2.1-topic-mine.md` |
