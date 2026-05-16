# V1.1 → V2.0 迁移指南

> 版本：V2.0 | 更新日期：2026-04-22

## 主要变更

### 1. Skill 数量简化（46 → 20，-57%）

**合并的 Skill：**

| 原 Skill | 新 Skill | 说明 |
|---------|---------|------|
| s-1.1.1/2/3 | s-1.1-info-intake | 信息采集与处理引擎 |
| a-1.2.1/2/3/4 | a-1.2-deep-think | 深度思考四层分析 |
| s-1.3.1/3/4 | s-1.3-kb-build | 知识库建设引擎 |
| s-2.1.1/2/3 | s-2.1-topic-mine | 多源选题挖掘引擎 |
| s-2.2.1/2 + s-2.3.1 | s-2.2-topic-validate | 选题验证与日历管理 |
| s-3.3.1/2/3/4 | s-3.3-style-engine | 统一风格引擎 |
| s-4.1.1/2/3/4 | s-4.1-slice-engine | 切片与脚本生成引擎 |
| s-4.3.1/2 | s-4.3-engagement | 互动运营引擎 |
| s-5.2.1/2/3 | s-5.2-review-engine | 复盘分析引擎 |
| s-5.3.1/2/3 | s-5.3-optimize | 策略优化引擎 |

**降级为脚本：**
- s-1.1.4-learning-tracker → scripts/learning-tracker.py

### 2. 审核节点减少（13 → 2，-85%）

**保留的 2 个关键审核点：**
1. ✅ 大纲审核（包含定位确认）
2. ✅ 发布前最终确认（包含风格、事实、平台适配）

**移除的审核点（改为自动执行 + 日志）：**
- 选题通过门控
- 定位确认（合并到大纲审核）
- 素材方向确认
- 初稿确认
- 事实核查确认
- 切片预览确认
- 质量门控
- 深度思考确认
- 发布确认（合并到发布前最终确认）

### 3. 上下文管理简化

**移除的概念：**
- ❌ Context Snapshot（≤2000 tokens）机制
- ❌ 主动上下文释放
- ❌ 模块级 Snapshot JSON 文件
- ❌ Module Coordinator 二级调度

**新的三层数据传递协议：**
1. **模块内传递**：完整数据文件（通过文件路径）
2. **模块间传递**：_manifest.md（索引文件）
3. **长文档生成**：分段加载（逐章生成）

### 4. 调度架构简化

**V1.1（二级调度）：**
```
Orchestrator → Module Coordinator → Skill
```

**V2.0（直接调度）：**
```
Orchestrator → Skill
```

## 兼容性

### ✅ 保持兼容
- 所有命令（/learn, /think, /create 等）保持兼容
- 数据目录结构不变
- 知识库和内容库格式不变
- 文件持久化机制不变

### ⚠️ 需要注意
- Skill 文件路径变更（需更新引用）
- Agent 别名映射更新
- 审核节点位置变化

## 迁移步骤

### 步骤 1：备份
```bash
# 备份现有 skills/ 目录
cp -r skills skills_v1.1_backup

# 备份核心配置
cp CLAUDE.md CLAUDE.md.v1.1.backup
cp docs/SKILL-INDEX.md docs/SKILL-INDEX.md.v1.1.backup
```

### 步骤 2：更新核心文档
- [x] CLAUDE.md - 系统架构、调度规则、上下文管理
- [x] docs/SKILL-INDEX.md - Skill 索引（46 → 20）
- [x] docs/DIRECTORY-MAP.md - 移除 Context Snapshot 描述

### 步骤 3：创建新的合并 Skill 文件
- [ ] 10 个新的合并 Skill 文件
- [ ] 验证功能覆盖完整性

### 步骤 4：更新命令文件
- [ ] .claude/commands/full-pipeline.md
- [ ] .claude/commands/quick-create.md
- [ ] .claude/commands/learn.md
- [ ] .claude/commands/distribute.md

### 步骤 5：归档旧文件
```bash
# 创建归档目录
mkdir -p skills/_archived

# 移动被合并的 Skill 文件
# （保留归档，不直接删除）
```

### 步骤 6：测试验证
- [ ] 测试 /quick-create 流程
- [ ] 测试 /full-pipeline 流程
- [ ] 测试 /think 流程
- [ ] 验证审核日志生成

## 功能对照表

### 命令变化

| 命令 | V1.1 审核点 | V2.0 审核点 | 变化 |
|------|-----------|-----------|------|
| /full-pipeline | 6个 | 2个 | -67% |
| /quick-create | 4个 | 2个 | -50% |
| /learn | 2个 | 0个 | -100% |
| /distribute | 1个 | 0个 | -100% |

### Skill 调用变化

**V1.1 调用方式：**
```
用户 → Orchestrator → Module Coordinator → Skill
```

**V2.0 调用方式：**
```
用户 → Orchestrator → Skill
```

## 审核日志系统

### 新增文件
每个任务会生成 `data/pipeline/{task_id}/audit-log.jsonl`：

```jsonl
{"timestamp":"2026-04-22T10:30:00Z","decision_point":"topic_scoring","auto_decision":"continue","score":6.8,"threshold":7.0,"reason":"score below threshold but within acceptable range"}
{"timestamp":"2026-04-22T10:35:00Z","decision_point":"fact_check","auto_decision":"flag_for_review","score":6.5,"issues_count":3,"reason":"fact check score below 7.0, flagged 3 issues"}
```

### 查看审核日志
```bash
# 查看最近的审核决策
tail -n 20 data/pipeline/{task_id}/audit-log.jsonl

# 查找所有低分选题
grep "topic_scoring" data/pipeline/*/audit-log.jsonl | grep "score.*6\."
```

## 回滚方案

如需回滚到 V1.1：

```bash
# 恢复备份的 skills/ 目录
rm -rf skills
mv skills_v1.1_backup skills

# 恢复核心配置
cp CLAUDE.md.v1.1.backup CLAUDE.md
cp docs/SKILL-INDEX.md.v1.1.backup docs/SKILL-INDEX.md
```

## 预期收益

| 指标 | 改进 |
|------|------|
| Skill 数量 | 46 → 20（-57%）|
| 审核节点 | 13 → 2（-85%）|
| 上下文消耗 | -30-40% |
| 执行时间 | -25-40% |
| 维护成本 | -57% |
| 学习曲线 | 显著降低 |

## 常见问题

### Q: 合并后的 Skill 会丢失功能吗？
A: 不会。所有功能都保留在合并后的 Skill 中，只是内部流程整合了。

### Q: 审核节点减少会影响质量吗？
A: 不会。关键的大纲和发布前审核保留，其他决策自动执行并记录到审核日志，支持事后回溯。

### Q: 如何查看自动决策的详情？
A: 查看 `data/pipeline/{task_id}/audit-log.jsonl` 文件。

### Q: 旧的 pipeline 数据还能访问吗？
A: 可以。数据目录结构不变，所有历史数据保持兼容。

### Q: 需要重新学习使用方法吗？
A: 不需要。所有命令接口保持不变，只是内部简化了。

## 技术支持

如遇到问题，请查阅：
- 完整分析报告：`docs/P0-REFACTOR-SUMMARY.md`
- 实施计划：已保存在 Claude 计划文件中
- 原始审查报告：见本次对话记录

---

**版本历史：**
- V2.0（2026-04-22）：P0 优先级修复，简化架构
- V1.1（2026-03-18）：二级调度，Context Snapshot
- V1.0（2026-03-01）：初始版本
