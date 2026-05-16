# ProjectFilesV1.1 系统使用指南

> 版本：V2.0 | 更新日期：2026-04-22
> 系统状态：✅ 完全可用

---

## 🚀 快速开始

### 系统概述

ProjectFilesV1.1 是一个完整的内容创作和知识管理系统，包含 5 个核心模块：

- **M1 知识积累**：学习、思考、知识库建设
- **M2 选题策划**：选题挖掘、验证、日历管理
- **M3 内容创作**：从大纲到终稿的完整创作流程
- **M4 多平台分发**：内容切片、平台适配
- **M5 数据反馈**：数据采集、复盘分析、策略优化

### 核心命令

| 命令 | 功能 | 预计耗时 | 审核节点 |
|------|------|---------|---------|
| `/learn <input>` | 学习新内容并入库 | 5-10分钟 | 0个 |
| `/think <input>` | 深度思考分析 | 10-15分钟 | 0个 |
| `/topic-mine` | 挖掘选题 | 5-10分钟 | 0个 |
| `/validate <topic>` | 验证选题 | 3-5分钟 | 0个 |
| `/quick-create <topic>` | 快速创作 | 15-30分钟 | 2个 |
| `/full-pipeline <topic>` | 完整创作流程 | 1.5-2.5小时 | 2个 |
| `/distribute <content>` | 多平台分发 | 10-15分钟 | 0个 |
| `/review <period>` | 数据复盘 | 5-10分钟 | 0个 |

---

## 📚 模块详细说明

### M1 · 知识积累

**核心 Skill：**
- `s-1.1-info-intake`：信息采集与处理引擎
- `a-1.2-deep-think`：深度思考四层分析引擎
- `s-1.3-kb-build`：知识库建设引擎

**使用场景：**
```bash
# 从 URL 学习
/learn https://example.com/article

# 从文本学习
/learn --text
# 然后粘贴文本内容

# 深度思考
/think "AI Agent 架构设计"

# 哲学分析
/analyze "创造力的本质"
```

**输出位置：**
- 知识条目：`knowledge-base/{category}/{date}-{slug}.md`
- 深度分析：`data/pipeline/think-{date}/preparation-report.md`
- 审核日志：`data/pipeline/{task_id}/audit-log.jsonl`

**V2.0 特性：**
- ✅ 自动入库，标记为 `pending_review`
- ✅ 无需人工确认，流程流畅
- ✅ 完整的审核日志记录

---

### M2 · 选题策划

**核心 Skill：**
- `s-2.1-topic-mine`：多源选题挖掘引擎
- `s-2.2-topic-validate`：选题验证与日历管理引擎

**使用场景：**
```bash
# 挖掘选题（全源）
/topic-mine

# 挖掘选题（指定来源）
/topic-mine --mode knowledge  # 从知识库
/topic-mine --mode trend      # 从热点
/topic-mine --mode pain       # 从痛点

# 验证选题
/validate "AI Agent 架构设计"

# 批量验证
/validate --batch
```

**输出位置：**
- 选题池：`data/topics/topics.json`
- 验证报告：`data/topics/validation/{date}-{slug}.json`
- 内容日历：`data/topics/calendar.md`

**V2.0 特性：**
- ✅ 自动评分和竞品分析
- ✅ 自动排期到日历
- ✅ 低分选题自动标记，不阻塞流程

---

### M3 · 内容创作

**核心 Skill：**
- `s-3.2.1-research`：素材研究
- `a-3.2.2-outline`：大纲设计
- `a-3.2.3-draft`：初稿撰写
- `a-3.2.4-iterate`：内容迭代
- `s-3.3-style-engine`：统一风格引擎
- `s-3.4.1-fact-check`：事实核查
- `s-3.2.5-seo`：SEO 优化

**使用场景：**

**快速创作（15-30分钟）：**
```bash
/quick-create "AI Agent 架构设计"

# 指定平台
/quick-create "AI Agent 架构设计" --platform wechat

# 跳过素材研究
/quick-create "AI Agent 架构设计" --skip-research
```

**完整流程（1.5-2.5小时）：**
```bash
/full-pipeline "AI Agent 架构设计"

# 使用已评分的选题
/full-pipeline --topic-id topic-001

# 指定平台
/full-pipeline "AI Agent 架构设计" --platforms wechat,zhihu
```

**输出位置：**
- 创作过程：`data/pipeline/create-{date}/`
- 终稿：`content/drafts/{date}-{slug}.md`
- 审核日志：`data/pipeline/{task_id}/audit-log.jsonl`

**V2.0 特性：**
- ✅ 审核节点：6个 → 2个（大纲审核 + 发布前确认）
- ✅ 自动风格检查和事实核查
- ✅ 问题自动标记到审核日志

**审核节点：**
1. **大纲审核**（必须）：确认内容结构和定位
2. **发布前最终确认**（必须）：综合检查所有维度

---

### M4 · 多平台分发

**核心 Skill：**
- `s-4.1-slice-engine`：切片与脚本生成引擎
- `s-4.2.2-adapt`：平台适配
- `s-4.3-engagement`：互动运营引擎

**使用场景：**
```bash
# 完整分发
/distribute content-20260422-001

# 指定平台
/distribute content-20260422-001 --platforms douyin,xiaohongshu

# 跳过视频
/distribute content-20260422-001 --skip-video

# 生成后编辑
/distribute content-20260422-001 --edit-slices
```

**输出位置：**
- 切片内容：`content/slices/{parent-id}/`
- 平台适配：`content/adapted/{parent-id}/`
- 发布清单：`content/publish-checklists/{id}.md`

**V2.0 特性：**
- ✅ 自动生成所有切片，无需预览确认
- ✅ 支持事后编辑（`/edit-slices`）
- ✅ 自动生成发布日历建议

---

### M5 · 数据反馈

**核心 Skill：**
- `s-5.1.1-data-collect`：数据采集
- `s-5.2-review-engine`：复盘分析引擎
- `s-5.3-optimize`：策略优化引擎

**使用场景：**
```bash
# 周期复盘
/review "2026-04"
/review "last_month"

# 单篇复盘
/review --content content-20260422-001

# 爆款分析
/review --mode hit --threshold top_10_percent

# 策略优化
/optimize --mode system  # 系统优化
/optimize --mode audience  # 受众更新
/optimize --mode brand  # 品牌健康
```

**输出位置：**
- 原始数据：`data/feedback/raw/`
- 分析报告：`data/feedback/reports/`
- 策略建议：`data/feedback/strategies/`

**V2.0 特性：**
- ✅ 自动采集和分析
- ✅ 完整的爆款模式识别
- ✅ 可执行的优化建议

---

## 🔄 典型工作流程

### 流程 1：日常学习

```bash
1. /learn <url>                    # 学习新内容
2. 查看知识条目                     # knowledge-base/{category}/
3. /kb-review --status pending_review  # 批量审核（可选）
```

### 流程 2：快速创作

```bash
1. /topic-mine                     # 挖掘选题
2. /validate <topic>               # 验证选题
3. /quick-create <topic>           # 快速创作
   → 审核大纲
   → 审核终稿
4. /distribute <content>           # 多平台分发
5. 发布内容
```

### 流程 3：深度创作

```bash
1. /topic-mine                     # 挖掘选题
2. /validate <topic>               # 验证选题
3. /full-pipeline <topic>          # 完整流程
   → 审核大纲
   → 审核终稿（综合检查）
4. /distribute <content>           # 多平台分发
5. 发布内容
6. /review <period>                # 数据复盘
```

### 流程 4：知识驱动创作

```bash
1. /think <topic>                  # 深度思考
2. 查看准备报告                     # data/pipeline/think-{date}/
3. /topic-mine --mode knowledge    # 从知识库挖掘选题
4. /full-pipeline --topic-id <id>  # 完整创作流程
5. /distribute <content>           # 多平台分发
```

---

## 📁 数据传递机制（V2.0）

### 三层架构

**层级 1：模块内传递（完整数据）**
- 模块内 Skill 之间传递完整数据文件
- 通过文件路径引用

**层级 2：模块间传递（索引文件）**
- 模块间通过 `_manifest.md` 索引文件传递
- 包含关键元数据和文件路径

**层级 3：长文档生成（分段加载）**
- 超长文档采用逐章生成和加载策略
- 按需加载特定章节

### _manifest.md 格式

```markdown
# 任务产物清单

## 任务信息
- Task ID: create-20260422-001
- 模块: M3 内容创作
- 状态: completed
- 创建时间: 2026-04-22T10:30:00Z

## 产出文件
- 素材包: research.json
- 大纲: outline.yaml
- 终稿: final.md

## 关键元数据
- 标题: AI Agent 架构设计
- 字数: 3500
- 质量分: 8.5/10

## 下游访问
- M4 分发: 读取 final.md
```

### audit-log.jsonl 格式

```jsonl
{"timestamp":"2026-04-22T10:30:00Z","decision_point":"topic_scoring","auto_decision":"continue","score":6.8,"threshold":7.0}
{"timestamp":"2026-04-22T10:35:00Z","decision_point":"fact_check","auto_decision":"flag_for_review","score":6.5,"issues_count":3}
```

**查看审核日志：**
```bash
# 查看特定任务的日志
cat data/pipeline/{task_id}/audit-log.jsonl

# 查看所有低分选题
grep "topic_scoring" data/pipeline/*/audit-log.jsonl | grep "score.*6\."

# 查看所有需要人工审核的决策
grep "flag_for_review" data/pipeline/*/audit-log.jsonl
```

---

## 🎯 V2.0 核心改进

### 审核节点优化

| 命令 | V1.1 | V2.0 | 改进 |
|------|------|------|------|
| /learn | 3个 | 0个 | -100% |
| /distribute | 1个 | 0个 | -100% |
| /quick-create | 4个 | 2个 | -50% |
| /full-pipeline | 6个 | 2个 | -67% |
| **总计** | **14个** | **4个** | **-71%** |

### 自动化提升

- ✅ 所有质量检查自动执行
- ✅ 问题自动标记到审核日志
- ✅ 低分内容自动标记，不阻塞流程
- ✅ 完整的可追溯性

### 用户体验改善

- ✅ 流程更流畅，减少中断
- ✅ 预计耗时平均减少 40-50%
- ✅ 保持质量检查完整性
- ✅ 支持事后审核和编辑

---

## 📖 参考文档

### 核心文档
- `CLAUDE.md`：系统配置（V2.0）
- `docs/SKILL-INDEX.md`：Skill 索引（20个核心Skill）
- `docs/DIRECTORY-MAP.md`：目录蓝图和数据传递协议

### 迁移文档
- `docs/MIGRATION-V2.md`：V2.0 迁移指南
- `docs/P0-FINAL-DELIVERY.md`：最终交付报告

### 命令文档
- `.claude/commands/learn.md`
- `.claude/commands/quick-create.md`
- `.claude/commands/full-pipeline.md`
- `.claude/commands/distribute.md`
- `.claude/commands/review.md`

---

## 🔧 故障排查

### 常见问题

**Q: 如何查看自动决策的详细信息？**
```bash
cat data/pipeline/{task_id}/audit-log.jsonl
```

**Q: 如何批量审核待审核的知识条目？**
```bash
grep -r "creation_status: pending_review" knowledge-base/
/kb-review --status pending_review
```

**Q: 如何编辑已生成的切片？**
```bash
/edit-slices <content_id>
```

**Q: 如何回滚到 V1.1？**
参考 `docs/MIGRATION-V2.md` 的回滚方案。

---

## 🎉 开始使用

系统已完全可用，你可以：

1. **从学习开始**：`/learn <url>`
2. **尝试快速创作**：`/quick-create "测试主题"`
3. **探索完整流程**：`/full-pipeline "测试主题"`
4. **查看文档**：参考上述参考文档

**祝你使用愉快！** 🚀

---

**版本历史：**
- V2.0（2026-04-22）：简化审核节点，新增审核日志系统
- V1.1（2026-03-18）：初始版本
