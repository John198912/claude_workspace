# dbskill 知识库导入说明

## 来源信息

**原始仓库**: https://github.com/dontbesilent2025/dbskill
**作者**: @dontbesilent
**许可证**: CC BY-NC 4.0 (Creative Commons Attribution-NonCommercial 4.0 International)
**导入日期**: 2026-04-30
**数据规模**: 4,176个知识原子 + 10份方法论文档 + 46个高频概念

## 许可证说明

根据 CC BY-NC 4.0 许可证:
- ✅ **个人使用/研究**: 无限制,无需署名
- ✅ **公开衍生作品**: 需注明来源
- ❌ **商业应用**: 需单独授权

本系统使用属于个人研究和内容创作用途,符合许可证要求。

## 数据结构

### 1. 知识原子库 (atoms/)

**来源**: `知识库/原子库/atoms.jsonl` (按季度分批导入)

**导入策略**:
- 优先导入: 2025Q1-Q4, 2026Q1 (最近5个季度)
- 质量过滤: 仅导入 confidence_level = "high" 或 "medium" 的原子
- 格式转换: JSONL → Markdown + YAML frontmatter

**字段映射**:
```yaml
id: {quarterly_id}              # 例: 2025Q4_001
title: {knowledge前60字符}       # 知识陈述摘要
date: {date}                    # 原始发布日期
tags: {topics} + {skills}       # 主题标签 + 技能标签
category: {自动映射}             # 映射到本地5大类
source: {url}                   # 原始推文链接
source_type: "dbskill_atom"     # 标识来源
confidence_level: {confidence}  # high/medium/low
status: "reviewed"              # 导入后状态
content_type: {type}            # principle/method/case/anti-pattern/insight/tool
original_tweet: {original}      # 原始推文文本(最多200字符)
imported_from: "dbskill"        # 来源标识
```

**分类映射规则**:
- 产品/需求/转化/商业模式 → `business`
- 提示词/智能体/AI工具 → `technology`
- 认知/心理/哲学 → `mindset`
- 个人成长/执行 → `growth`
- 观点/方法论 → `viewpoint`

### 2. 方法论文档 (methodologies/)

**来源**: `知识库/Skill知识包/`

**10份文档**:
- `action/` - 行动心理学 (2份)
  - `action_信号案例库.md`
  - `action_心理诊断框架.md`
- `benchmark/` - 竞品对标 (2份)
  - `benchmark_对标方法论.md`
  - `benchmark_平台运营知识.md`
- `content/` - 内容创作 (2份)
  - `content_内容创作方法论.md`
  - `content_平台特性与案例.md`
- `deconstruct/` - 概念解构 (2份)
  - `deconstruct_解构案例库.md`
  - `deconstruct_语言与概念框架.md`
- `diagnosis/` - 商业诊断 (2份)
  - `diagnosis_公理与诊断框架.md`
  - `diagnosis_问题消解案例库.md`

### 3. 高频概念词典 (concepts/)

**来源**: `知识库/高频概念词典.md`

**46个关键术语**,按频次排序:
- 产品 (593次)
- 提示词 (195次)
- 需求 (184次)
- 智能体 (163次)
- 对标 (119次)
- 知识付费 (104次)
- 转化 (74次)
- 私域 (70次)
- ...等

## 质量控制措施

### 导入过滤规则
1. **置信度过滤**: 仅导入 `confidence_level` 为 "high" 或 "medium" 的原子
2. **时效性优先**: 优先导入2025-2026年度数据(最新5个季度)
3. **去重检查**: 基于 `id` 字段去重
4. **来源追溯**: 所有条目保留原始 `url` 链接

### 人工审核流程
- **商业关键原子**: confidence="high" 且 type="principle" 的条目需人工复核
- **低置信度原子**: confidence="low" 的条目暂不导入,待后续评估
- **敏感内容**: 涉及具体产品/价格的案例需验证时效性

## 使用指南

### 查询知识原子
```bash
# 按主题查询
grep -r "tags: .*产品.*" knowledge-base/imported/dbskill/atoms/

# 按置信度查询
grep -r "confidence_level: high" knowledge-base/imported/dbskill/atoms/

# 按内容类型查询
grep -r "content_type: principle" knowledge-base/imported/dbskill/atoms/
```

### 集成到本地技能
- M1 (知识积累): 原子库作为 `s-1.1-info-intake` 的参考素材
- M2 (选题策划): 方法论文档指导 `s-2.1-topic-mine` 和 `s-2.2-topic-validate`
- M3 (内容创作): 内容创作方法论增强 `s-3.0-content-diagnostics`

### MCP 向量检索
导入完成后,运行以下命令更新向量索引:
```bash
# 重建知识库向量索引
python scripts/rebuild-knowledge-index.py --source dbskill
```

## 数据统计

### 按季度分布
- 2024Q4: ~700条
- 2025Q1: ~800条
- 2025Q2: ~850条
- 2025Q3: 240条
- 2025Q4: 257条
- 2026Q1: ~1,329条

### 按置信度分布 (预估)
- High: ~60%
- Medium: ~30%
- Low: ~10% (不导入)

### 按内容类型分布
- principle (原则): ~35%
- method (方法): ~25%
- case (案例): ~20%
- insight (洞察): ~15%
- anti-pattern (反模式): ~3%
- tool (工具): ~2%

## 维护说明

### 定期更新
- **频率**: 每季度检查一次上游仓库更新
- **增量导入**: 仅导入新增的季度文件
- **版本追踪**: 在 `data/logs/dbskill-import-log.jsonl` 记录每次导入

### 质量监控
- **定期抽查**: 每月随机抽查20条原子,验证质量和相关性
- **反馈循环**: 使用中发现的低质量原子标记为 `status: deprecated`
- **置信度调整**: 根据实际使用效果调整本地置信度评分

## 风险缓解

### 已实施措施
1. ✅ **来源隔离**: 单独目录存放,保持可追溯性
2. ✅ **许可证合规**: 添加 CC BY-NC 4.0 声明和来源归属
3. ✅ **质量过滤**: 置信度过滤机制
4. ✅ **分批导入**: 按季度分批,降低风险
5. ✅ **人工审核**: 关键原子需人工复核

### 潜在风险
- ⚠️ **时效性**: 部分案例可能过时(特别是2024年数据)
- ⚠️ **上下文缺失**: 推文原子可能缺少完整上下文
- ⚠️ **观点偏差**: 单一创作者视角,需结合其他来源

## 贡献者

**原始数据**: @dontbesilent (12,307条推文 → 4,176个知识原子)
**导入集成**: 超级个体内容创作智能体群 V2.5
**维护团队**: 本地系统 Orchestrator

---

**最后更新**: 2026-04-30
**数据版本**: dbskill v1.0 (截至2026年3月)
