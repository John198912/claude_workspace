# `/create <topic>` — 创作内容（全流程）

> 平台中立命令定义 · 事实源：CLAUDE.md / CHANGELOG V1.2
> 适配层：`.claude/commands/create.md` 应为此文件的薄包装或符号链接

## 功能

基于选题执行完整创作流程：素材研究 → 大纲设计 → 初稿撰写 → 风格校验 → 事实核查 → SEO 优化 → 迭代优化。

## 涉及模块

M2（选题）→ M3（创作）

## 品牌契约

本命令使用品牌定位信息。创作时须读取 `data/brand/brand-canon.yaml` 获取活跃品牌口径，并在输出中保持一致。品牌口径以 brand-canon.yaml 为准，不得使用已被取代的旧版品牌文案。

## 执行流程

```
选题 → s-3.1.2 内容定位 → s-3.2.1 素材研究
  → a-3.2.2 大纲设计 → ⚠️ 人工确认（大纲审核）
  → a-3.2.3 初稿撰写 → [循环迭代 3-5 轮]
  → s-3.3 风格校验 → s-3.4.1 事实核查
  → s-3.2.5 SEO 优化 → a-3.2.4 迭代优化
  → s-3.1.1 内容体系化归档
```

### 人工确认节点

- **大纲审核**：Orchestrator 暂停，等待创作者确认大纲后方可进入初稿

### 质量门节点（自动可阻断）

- `content_quality` gate：在发布前对初稿进行质量独立审查
- `fact-check`：事实核查评分 ≥8 通过（见 s-3.4.1）

## 输出

- `data/pipeline/create-{id}/` — 完整管线产物
  - `positioning.yaml` — 定位
  - `research.md` — 素材研究
  - `outline.yaml` / `outline.md` — 大纲
  - `draft-v1.md` → `draft-vN.md` — 多轮初稿
  - `style-check-report.md` — 风格校验报告
  - `fact-check-report.md` — 事实核查报告
  - `seo-optimization.md` — SEO 优化
  - `iterate-report.md` — 迭代记录
  - `quality-gates/` — 质量门报告
  - `_manifest.md` — 文件索引

## 依赖 Skill

| Skill | 路径 |
|-------|------|
| s-3.1.2-content-positioning | `skills/m3-creation/s-3.1.2-content-positioning.md` |
| s-3.2.1-research | `skills/m3-creation/s-3.2.1-research.md` |
| a-3.2.2-outline | `skills/m3-creation/a-3.2.2-outline.md` |
| a-3.2.3-draft | `skills/m3-creation/a-3.2.3-draft.md` |
| a-3.2.4-iterate | `skills/m3-creation/a-3.2.4-iterate.md` |
| s-3.3-style-engine | `skills/m3-creation/s-3.3-style-engine.md` |
| s-3.4.1-fact-check | `skills/m3-creation/s-3.4.1-fact-check.md` |
| s-3.2.5-seo | `skills/m3-creation/s-3.2.5-seo.md` |
| s-3.1.1-content-system | `skills/m3-creation/s-3.1.1-content-system.md` |
