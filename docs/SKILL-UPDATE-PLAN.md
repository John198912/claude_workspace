# 批量更新 Skill 文件 - V2.0 协作接口统一

> 更新时间：2026-04-22
> 目的：移除 Context Snapshot 引用，统一为 V2.0 数据传递协议

## 需要更新的文件清单

### M3 内容创作（8个）
1. skills/m3-creation/s-3.1.1-content-system.md
2. skills/m3-creation/s-3.1.2-content-positioning.md
3. skills/m3-creation/s-3.2.1-research.md
4. skills/m3-creation/a-3.2.2-outline.md
5. skills/m3-creation/a-3.2.3-draft.md
6. skills/m3-creation/a-3.2.4-iterate.md
7. skills/m3-creation/s-3.4.1-fact-check.md
8. skills/m3-creation/s-3.2.5-seo.md

### M4 多平台分发（1个）
9. skills/m4-distribution/s-4.2.2-adapt.md

### M5 数据反馈（1个）
10. skills/m5-feedback/s-5.1.1-data-collect.md

### M1 知识积累（2个）
11. skills/m1-knowledge/a-1.2.5-dialogue-harvest.md
12. skills/m1-knowledge/a-1.4.1-philosopher.md

## 统一更新模板

### 旧的协作接口格式（需移除）

```yaml
## 协作接口

### 输入
- Context Snapshot: m1_output.json
- 其他输入...

### 输出
- Context Snapshot: m3_output.json
- 其他输出...
```

### 新的协作接口格式（V2.0）

```yaml
## 数据传递（V2.0）

### 输入
- **上游文件**：读取 `data/pipeline/{task_id}/xxx.json`
- **参数**：{具体参数}

### 输出
- **输出文件**：写入 `data/pipeline/{task_id}/yyy.json`
- **索引文件**：更新 `_manifest.md`

### 下游访问
- 下游 Skill 通过读取输出文件路径获取数据
- 跨模块访问通过 `_manifest.md` 获取元数据

## 协作接口

### 上游
- {上游 Skill 名称}

### 下游
- {下游 Skill 名称}

### 触发方式
- {触发命令或条件}
```

## 更新原则

1. **完全移除** Context Snapshot 相关描述
2. **添加** V2.0 数据传递说明
3. **保持** 原有功能描述不变
4. **统一** 格式和术语

## 批量更新策略

由于文件数量较多（12个），建议采用以下策略：

**方案 1：逐个手动更新（推荐）**
- 优点：精确控制，确保质量
- 缺点：耗时较长
- 适用：需要仔细审查每个文件

**方案 2：模板化批量更新**
- 优点：快速完成
- 缺点：可能需要后续微调
- 适用：文件格式统一

**方案 3：分批更新**
- 优点：平衡速度和质量
- 缺点：需要分多次完成
- 适用：当前场景（推荐）

## 分批更新计划

### 第一批：M3 核心创作流程（4个）
- a-3.2.2-outline.md
- a-3.2.3-draft.md
- a-3.2.4-iterate.md
- s-3.2.1-research.md

### 第二批：M3 辅助功能（4个）
- s-3.1.1-content-system.md
- s-3.1.2-content-positioning.md
- s-3.4.1-fact-check.md
- s-3.2.5-seo.md

### 第三批：M4/M5/M1（4个）
- s-4.2.2-adapt.md
- s-5.1.1-data-collect.md
- a-1.2.5-dialogue-harvest.md
- a-1.4.1-philosopher.md

## 预期完成时间

- 第一批：15-20分钟
- 第二批：15-20分钟
- 第三批：15-20分钟
- **总计**：45-60分钟

---

**当前状态：准备开始批量更新**
