# 归档的 Skill 文件说明

> 归档日期：2026-04-22
> 原因：V2.0 架构简化，这些 Skill 已合并为新的统一引擎

## 归档说明

本目录包含 V1.1 版本中被合并的原始 Skill 文件。这些文件已被整合到 V2.0 的新 Skill 中，但保留归档以供参考。

## 合并关系

### M1 知识积累（9个文件）

**合并为 s-1.1-info-intake.md：**
- s-1.1.1-info-monitor.md（信息监控）
- s-1.1.2-summarize.md（内容摘要）
- s-1.1.3-cross-validate.md（交叉验证）

**合并为 a-1.2-deep-think.md：**
- a-1.2.1-deconstruct.md（内容解构）
- a-1.2.2-expand.md（体系扩展）
- a-1.2.3-contextual-think.md（语境思辨）
- a-1.2.4-reflect.md（观点反思）

**合并为 s-1.3-kb-build.md：**
- s-1.3.1-note-gen.md（知识笔记）
- s-1.3.3-knowledge-graph.md（知识图谱）
- s-1.3.4-kb-health.md（库健康检查）

**降级为脚本：**
- s-1.1.4-learning-tracker.md → scripts/learning-tracker.py

### M2 选题策划（6个文件）

**合并为 s-2.1-topic-mine.md：**
- s-2.1.1-knowledge-topic.md（知识库选题）
- s-2.1.2-trend-topic.md（热点选题）
- s-2.1.3-pain-point-topic.md（痛点选题）

**合并为 s-2.2-topic-validate.md：**
- s-2.2.1-topic-scoring.md（选题评分）
- s-2.2.2-competitive-analysis.md（竞品分析）
- s-2.3.1-calendar.md（日历管理）

### M3 内容创作（4个文件）

**合并为 s-3.3-style-engine.md：**
- s-3.3.1-style-profile.md（风格建档）
- s-3.3.2-personal-style.md（个人风格）
- s-3.3.3-style-tags.md（风格标签）
- s-3.3.4-style-check.md（风格校验）

### M4 多平台分发（7个文件）

**合并为 s-4.1-slice-engine.md：**
- s-4.1.1-slice-strategy.md（切片策略）
- s-4.1.2-video-script.md（视频脚本）
- s-4.1.3-graphic-note.md（图文笔记）
- s-4.1.4-podcast-script.md（播客脚本）

**合并到 s-4.2.2-adapt.md：**
- s-4.2.1-platform-rules.md（平台规则）

**合并为 s-4.3-engagement.md：**
- s-4.3.1-comment-reply.md（评论回复）
- s-4.3.2-user-insight.md（用户洞察）

### M5 数据反馈（6个文件）

**合并为 s-5.2-review-engine.md：**
- s-5.2.1-single-review.md（单篇复盘）
- s-5.2.2-periodic-analysis.md（周期分析）
- s-5.2.3-hit-pattern.md（爆款识别）

**合并为 s-5.3-optimize.md：**
- s-5.3.1-system-optimize.md（系统优化）
- s-5.3.2-audience-update.md（受众更新）
- s-5.3.3-brand-health.md（品牌健康）

## 总计

- **归档文件总数**：26个
- **合并为新 Skill**：10个
- **降级为脚本**：1个

## 使用说明

这些归档文件仅供参考，不应在 V2.0 系统中使用。如需查看原始功能实现，可以参考这些文件。

如需使用相关功能，请使用新的合并 Skill：
- 参考 `docs/SKILL-INDEX.md` 查看新的 Skill 列表
- 参考 `docs/MIGRATION-V2.md` 查看迁移指南

## 回滚说明

如需回滚到 V1.1 版本：
1. 将这些文件移回原目录
2. 恢复 CLAUDE.md 和 SKILL-INDEX.md 的备份
3. 删除新创建的合并 Skill 文件

详见 `docs/MIGRATION-V2.md` 的回滚方案。

---

**归档版本**：V1.1
**当前版本**：V2.0
**归档日期**：2026-04-22
