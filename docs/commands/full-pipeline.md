# `/full-pipeline <topic>` — 全流程创作

> 平台中立命令定义 · 事实源：CLAUDE.md / CHANGELOG V1.2（V1.2 中增加事实核查步骤）
> 适配层：`.claude/commands/full-pipeline.md` 应为此文件的薄包装或符号链接

## 功能

从选题到分发的完整内容创作管线，覆盖 M1→M5 全部模块。

## 涉及模块

M1 → M2 → M3 → M4 → M5

## 品牌契约

全流程自 M2/M3 起使用品牌定位信息。创作时须读取 `data/brand/brand-canon.yaml` 获取活跃品牌口径，并在输出中保持一致。品牌口径以 brand-canon.yaml 为准，不得使用已被取代的旧版品牌文案。

## 执行流程

```
M1: 知识点积累（信息采集 → 深度思考 → 知识库入库）
  → M2: 选题策划（挖掘 → 验证 → 排期）
  → M3: 内容创作（定位 → 研究 → 大纲 → 初稿 → [迭代循环] → 风格校验 → 事实核查 → SEO → 归档）
  → M4: 多平台分发（切片 → 适配 → 发布前确认 → 互动）
```

### 自 V1.2 增加的完整步骤

```diff
- 事实核查（V1.1 无）
+ ... → 风格校验 → 事实核查（新增） → SEO 优化 → ...
```

## 人工确认节点

1. **大纲审核**（M3 节点）
2. **发布前确认**（M4 节点）

## 质量门（自动可阻断）

1. `workflow_consistency` — 流程完整性
2. `source_evidence` — 信息来源可靠性（M1）
3. `kb_publish` — 知识库发布质量（M1）
4. `content_quality` — 内容质量（M3）
5. `publish_package` — 发布包合规（M4）
6. `data_quality` — 数据质量与因果纪律（M5）

## 输出

合并所有子命令的产出物（见各命令文档），以 `data/pipeline/full-pipeline-{id}/` 归档。

## 依赖 Skill

全部 21 个核心 Skill + 按需调用扩展 Skill
