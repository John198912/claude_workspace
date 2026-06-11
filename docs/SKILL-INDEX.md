# Skill 统一索引 · SKILL-INDEX

> 版本：V2.1 | 更新日期：2026-06-06 | 总计：**21 个核心 Skill + 6 个扩展 Skill**
> 口径：核心 21（M1:4 / M2:2 / M3:9 / M4:3 / M5:3）+ 扩展 6（见文末「扩展 Skill」）。`*-enhancement.md` 为核心 Skill 的增强覆盖层，不单独计数。
> V2.1 变更：对齐花名册与磁盘实况；新增 6-gate 独立审查协议（见 `docs/QUALITY-GATES.md`）。
> V2.0 变更：简化架构，46→核心Skill，移除二级调度，减少人工审核节点。

---

## 版本变更说明

**V2.0（2026-04-22）- P0 优先级修复：**
- Skill 数量：46 → 20（-57%）
- 审核节点：13 → 2（-85%）
- 移除 Context Snapshot 机制
- 取消二级调度架构
- 版本演进详见：`docs/CHANGELOG.md`

---

## M1 · 知识积累（4个）

### 信息采集与处理

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **s-1.1-info-intake** | 信息采集与处理引擎 | 多源信息采集+摘要提取+交叉验证 | 外部输入 → a-1.2-deep-think |

**合并自：** s-1.1.1（信息监控）+ s-1.1.2（内容摘要）+ s-1.1.3（交叉验证）

文件路径：`skills/m1-knowledge/s-1.1-info-intake.md`

### 深度思考

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **a-1.2-deep-think** | 深度思考四层分析 | 解构+扩展+语境+反思（P1-P4） | s-1.1 / 用户输入 → a-1.2.5 |
| **a-1.2.5-dialogue-harvest** | 对话收割引擎 | 深度对话+三重输出（元素材/提示词/白皮书） | a-1.2 → s-1.3 / M3 |

**a-1.2 合并自：** a-1.2.1（内容解构）+ a-1.2.2（体系扩展）+ a-1.2.3（语境思辨）+ a-1.2.4（观点反思）

文件路径：
- `skills/m1-knowledge/a-1.2-deep-think.md`
- `skills/m1-knowledge/a-1.2.5-dialogue-harvest.md`（保留）

### 知识库建设

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **s-1.3-kb-build** | 知识库建设引擎 | 知识笔记+知识图谱+库健康检查 | a-1.2.5 / s-1.1 → 知识库 |

**合并自：** s-1.3.1（知识笔记）+ s-1.3.3（知识图谱）+ s-1.3.4（库健康检查）

文件路径：`skills/m1-knowledge/s-1.3-kb-build.md`

### 哲学分析（可选）

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **a-1.4.1-philosopher** | 哲学分析引擎 | 五阶分析·对话性假设 | 用户输入 / a-1.2.5 → s-1.3 / M3 |

文件路径：`skills/m1-knowledge/a-1.4.1-philosopher.md`（保留）

---

## M2 · 选题策划（2个）

### 选题挖掘

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **s-2.1-topic-mine** | 多源选题挖掘引擎 | 知识库选题+热点选题+痛点选题 | 知识库 / web-search → s-2.2 |

**合并自：** s-2.1.1（知识库选题）+ s-2.1.2（热点选题）+ s-2.1.3（痛点选题）

文件路径：`skills/m2-topic/s-2.1-topic-mine.md`

### 选题验证与日历

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **s-2.2-topic-validate** | 选题验证与日历管理 | 选题评分+竞品分析+日历排期 | s-2.1 → M3 |

**合并自：** s-2.2.1（选题评分）+ s-2.2.2（竞品分析）+ s-2.3.1（日历管理）

文件路径：`skills/m2-topic/s-2.2-topic-validate.md`

---

## M3 · 内容创作（9个）

### 内容体系与定位

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **s-3.1.1-content-system** | 内容体系框架 | 内容支柱与系列规划 | M2 → s-3.1.2 |
| **s-3.1.2-positioning** | 内容定位策略 | 单篇内容定位 | s-3.1.1 → a-3.2.2 |

文件路径：`skills/m3-creation/s-3.1.{N}-*.md`（保留）

### 写作流程

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **s-3.2.1-research** | 素材研究 | 创作前素材收集 | web-search → a-3.2.2 |
| **a-3.2.2-outline** | 大纲设计 | 结构化大纲生成 | s-3.2.1 → a-3.2.3 |
| **a-3.2.3-draft** | 初稿撰写 | 基于大纲写作初稿 | a-3.2.2 → a-3.2.4 |
| **a-3.2.4-iterate** | 迭代优化引擎 | 五轮迭代改稿 | a-3.2.3 → s-3.3 |
| **s-3.2.5-seo** | SEO 优化 | 搜索引擎优化 | a-3.2.4 → M4 |

文件路径：`skills/m3-creation/{a|s}-3.2.{N}-*.md`（保留）

### 风格与质量

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **s-3.3-style-engine** | 统一风格引擎 | 风格建档+个人风格+标签+校验 | a-3.2.4 → s-3.4.1 |
| **s-3.4.1-fact-check** | 事实核查 | 数据与引用验证 | s-3.3 → s-3.2.5 |

**s-3.3 合并自：** 旧版四个子 Skill（风格建档 + 个人风格 + 风格标签 + 风格校验）

文件路径：
- `skills/m3-creation/s-3.3-style-engine.md`
- `skills/m3-creation/s-3.4.1-fact-check.md`（保留）

---

## M4 · 多平台分发（3个）

### 内容切片

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **s-4.1-slice-engine** | 切片与脚本生成引擎 | 切片策略+视频脚本+图文笔记+播客脚本 | M3终稿 → s-4.2 |

**合并自：** s-4.1.1（切片策略）+ s-4.1.2（视频脚本）+ s-4.1.3（图文笔记）+ s-4.1.4（播客脚本）

文件路径：`skills/m4-distribution/s-4.1-slice-engine.md`

### 平台适配

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **s-4.2.2-adapt** | 多平台内容适配 | 各平台格式适配（含平台规则） | s-4.1 → 发布 |

**注：** s-4.2.1（平台规则）内容已合并到 s-4.2.2

文件路径：`skills/m4-distribution/s-4.2.2-adapt.md`（保留，需更新）

### 互动运营

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **s-4.3-engagement** | 互动运营引擎 | 评论回复+用户洞察 | 发布 → M5 |

**合并自：** s-4.3.1（评论回复）+ s-4.3.2（用户洞察）

文件路径：`skills/m4-distribution/s-4.3-engagement.md`

---

## M5 · 数据反馈（3个）

### 数据采集

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **s-5.1.1-data-collect** | 数据采集 | 多平台数据采集 | 平台API → s-5.2 |

文件路径：`skills/m5-feedback/s-5.1.1-data-collect.md`（保留）

### 复盘分析

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **s-5.2-review-engine** | 复盘分析引擎 | 单篇复盘+周期分析+爆款识别 | s-5.1.1 → s-5.3 |

**合并自：** s-5.2.1（单篇复盘）+ s-5.2.2（周期分析）+ s-5.2.3（爆款识别）

文件路径：`skills/m5-feedback/s-5.2-review-engine.md`

### 策略优化

| 编号 | 名称 | 职能 | 上游 → 下游 |
|------|------|------|------------|
| **s-5.3-optimize** | 策略优化引擎 | 系统优化+受众更新+品牌健康 | s-5.2 → 全模块 |

**合并自：** s-5.3.1（系统优化）+ s-5.3.2（受众更新）+ s-5.3.3（品牌健康）

文件路径：`skills/m5-feedback/s-5.3-optimize.md`

---

## 脚本工具

| 文件 | 用途 | 原 Skill |
|------|------|---------|
| `scripts/learning-tracker.py` | 学习进度追踪 | s-1.1.4（降级） |
| `scripts/tag-assigner.py` | 知识库标签自动分配 | — |
| `scripts/topic-pool-manager.py` | 选题库管理 | — |
| `scripts/publish-checklist-gen.py` | 发布清单生成 | — |
| `scripts/data-normalizer.py` | 数据标准化 | — |

详见 `scripts/_index.md`

---

## 依赖关系图（简化版）

```
用户输入
  ↓
M1: s-1.1 → a-1.2 → a-1.2.5 → s-1.3
  ↓
M2: s-2.1 → s-2.2
  ↓
M3: s-3.1.1 → s-3.1.2 → s-3.2.1 → a-3.2.2 → a-3.2.3 → a-3.2.4 → s-3.3 → s-3.4.1 → s-3.2.5
  ↓
M4: s-4.1 → s-4.2.2 → s-4.3
  ↓
M5: s-5.1.1 → s-5.2 → s-5.3
  ↓
反馈闭环 → M1/M2/M3
```

---

## 扩展 Skill（6个，可选）

> 这些 Skill 真实存在于磁盘且为 `Active`，是核心 21 之外的可选增强。多为 dbskill 集成或哲学/战略增强，按需调用。

| 编号 | 名称 | 职能 | 来源 | 文件路径 |
|------|------|------|------|---------|
| **a-1.4.1-philosopher** | 哲学分析引擎 | 五阶分析·对话性假设（齐泽克/拉康×维特根斯坦×福柯） | 自建 | `skills/m1-knowledge/a-1.4.1-philosopher.md` |
| **s-1.4-action-diagnostics** | 执行心理学诊断 | 行动/拖延诊断 | dbskill `/dbs-action` | `skills/m1-knowledge/s-1.4-action-diagnostics/README.md` |
| **s-2.0-business-validate** | 商业模式诊断 | 商业可行性验证 | dbskill `/dbs-diagnosis` | `skills/m2-topic/s-2.0-business-validate/README.md` |
| **s-2.3-pacing-strategy** | 慢即是快战略 | 非线性成长·长期内容战略 | 自建 | `skills/m2-topic/s-2.3-pacing-strategy.md` |
| **s-3.0-content-diagnostics** | 内容诊断 | 内容问题诊断 | dbskill `/dbs-content` | `skills/m3-creation/s-3.0-content-diagnostics/README.md` |
| **s-3.4.2-ai-check** | AI写作检测 | AI味检测（score>6.0 硬阻断） | dbskill `/dbs-ai-check` | `skills/m3-creation/s-3.4.2-ai-check/README.md` |

> 增强覆盖层（不计入花名册）：`a-1.2-deep-think-philosophy-enhancement.md`、`s-2.2-topic-validate-v2.5-enhancement.md`、`s-4.1-slice-engine-hook-enhancement.md`、`a-1.4-resources/`、`m4-distribution/xiaohongshu-title-templates.md`。

---

## 归档的 Skill（V1.1）

以下 V1.1 子 Skill 已合并进上述核心 Skill（通过 git 历史可追溯，仓内未保留 `_archived/` 目录）：

**M1（9个）：**
- s-1.1.1/2/3-*.md → s-1.1-info-intake.md
- a-1.2.1/2/3/4-*.md → a-1.2-deep-think.md
- s-1.3.1/3/4-*.md → s-1.3-kb-build.md
- s-1.1.4-learning-tracker.md → scripts/learning-tracker.py

**M2（5个）：**
- s-2.1.1/2/3-*.md → s-2.1-topic-mine.md
- s-2.2.1/2-*.md + s-2.3.1-*.md → s-2.2-topic-validate.md

**M3（4个）：**
- s-3.3.1/2/3/4-*.md → s-3.3-style-engine.md

**M4（6个）：**
- s-4.1.1/2/3/4-*.md → s-4.1-slice-engine.md
- s-4.2.1-*.md → 合并到 s-4.2.2-adapt.md
- s-4.3.1/2-*.md → s-4.3-engagement.md

**M5（6个）：**
- s-5.2.1/2/3-*.md → s-5.2-review-engine.md
- s-5.3.1/2/3-*.md → s-5.3-optimize.md

---

## 调用方式

### 1. Slash Command（推荐）
```
/learn <input>          # 调用 M1
/think <input>          # 调用 a-1.2 + a-1.2.5
/create <topic>         # 调用 M3 完整流程
/full-pipeline <topic>  # 调用 M1→M5 全流程
```

### 2. @角色点名
```
@研究员 <任务>          # 调用 s-1.1-info-intake
@思考者 <任务>          # 调用 a-1.2-deep-think
@写手 <任务>            # 调用 a-3.2.2/3/4
@风格师 <任务>          # 调用 s-3.3-style-engine
```

### 3. [任务:类型]
```
[任务:研究] <内容>      # 自动调用 s-1.1 + a-1.2
[任务:写作] <主题>      # 自动调用 M3 写作流程
[任务:分发] <内容>      # 自动调用 M4 分发流程
```

---

## 迁移与回滚

版本演进见 `docs/CHANGELOG.md`。回滚通过 git 进行（例：`git revert` 或 `git checkout <tag> -- <path>`），不再依赖手工 `.backup` 文件。

## 质量门

Skill 的产出在关键节点受独立审查门约束（入库/发布/策略/事实可信度变化）。协议见 `docs/QUALITY-GATES.md`。

---

**版本历史：**
- V2.1（2026-06-06）：花名册对齐磁盘（核心21+扩展6）；新增 6-gate 独立审查协议
- V2.0（2026-04-22）：简化架构，核心 Skill 合并
- V1.4（2026-03-18）：46个Skill，二级调度
- V1.0（2026-03-01）：初始版本
