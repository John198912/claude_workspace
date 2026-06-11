# 超级个体内容创作智能体群 · 更新日志

---

## V1.2 (2026-03-07)

基于 [ai-agent-team](https://github.com/Sunnyeung369/ai-agent-team) 项目的对比分析，进行了四项架构优化。

### 🆕 新增功能

#### 1. 事实核查环节（Fact-Checker）

新增独立的事实核查 Skill `s-3.4.1-fact-check`，在内容创作流程的风格校验之后、SEO 优化之前执行。

- **四个核查维度**：数据准确性 / 技术术语正确性 / 断言合理性 / 知识库交叉验证
- **评分机制**：基础 10 分，按问题严重度扣分，≥7 分通过
- **已集成到** `/full-pipeline` 和 `/validate content` 流程中

| 文件 | 变更 |
|------|------|
| `skills/m3-creation/s-3.4.1-fact-check.md` | 新建 |
| `.claude/commands/full-pipeline.md` | 插入核查步骤 + 审核节点 + 错误处理 |
| `.claude/commands/validate.md` | 终稿验证增加核查维度 |

#### 2. 快速创作模式 `/quick-create`

新增轻量级创作命令，跳过完整 M1→M5 流程中的非必要环节，**每步完成后需人工确认**。

```
步骤 1: 素材研究（精简）→ ⚠️ 人工确认
步骤 2: 快速大纲（3-5要点）→ ⚠️ 人工确认
步骤 3: 快速写作 → ⚠️ 人工确认
步骤 4: 风格快检（仅禁忌扫描）→ ⚠️ 人工确认
步骤 5: 输出
```

- 预计 30-60 分钟（vs `/full-pipeline` 的 2-4 小时）
- 支持 `--adapt <platforms>` 可选平台适配
- 适用于日常碎片化内容、时效性热点、试验性方向

| 文件 | 变更 |
|------|------|
| `.claude/commands/quick-create.md` | 新建 |
| `CLAUDE.md` | 工作流命令表增加 `/quick-create` |

#### 3. 三种灵活调用方式

在原有 Slash Command 基础上，新增两种更灵活的调用方式：

| 方式 | 语法示例 | 适用场景 |
|------|---------|---------|
| Slash Command | `/full-pipeline <topic>` | 复杂任务，完整流水线 |
| @角色 点名 | `@写手 基于这个大纲写初稿` | 单一任务，精准调度 |
| [任务:类型] | `[任务:写作] 写一篇关于...` | 快速匹配最佳 Agent 组合 |

支持 8 个常用角色点名 + 6 种任务类型自动路由。

#### 4. Agent 中文别名系统

为全部 15 个 Agent + 1 个新增 Skill 配置了直观的中文别名：

| 别名 | Agent | 别名 | Agent |
|------|-------|------|-------|
| 研究员 | A1.1 | 切片师 | A4.1 |
| 思考者 | A1.2 | 适配器 | A4.2 |
| 知识官 | A1.3 | 运营官 | A4.3 |
| 选题官 | A2.1 | 数据官 | A5.1 |
| 验证官 | A2.2 | 复盘师 | A5.2 |
| 日历官 | A2.3 | 策略师 | A5.3 |
| 体系师 | A3.1 | **核查员** | **s-3.4.1** |
| 写手 | A3.2 | | |
| 风格师 | A3.3 | | |

| 文件 | 变更 |
|------|------|
| `CLAUDE.md` | 新增三种调用方式章节 + Agent 别名映射表 |

### 📁 V1.2 文件变更汇总

```
ProjectFilesV1.1/
├── CLAUDE.md                                    [修改] +别名 +调用方式 +命令
├── .claude/commands/
│   ├── full-pipeline.md                         [修改] +事实核查步骤
│   ├── validate.md                              [修改] +核查维度
│   └── quick-create.md                          [新建] 快速创作命令
└── skills/m3-creation/
    └── s-3.4.1-fact-check.md                    [新建] 事实核查 Skill
```

### 🏗️ 架构变更

M3 模块新增事实核查能力：

```
M3 Coordinator (A3.1兼任)
  ├── A3.1 内容体系化
  ├── A3.2 写作引擎
  ├── A3.3 风格引擎
  └── s-3.4.1 事实核查 ← 新增
```

完整创作流程更新：

```
... → 风格校验 → [事实核查 ← 新增] → SEO 优化 → 切片 → 分发 → ...
```

---

## V2.2 (2026-06-12)

基于代码审查（claude-code-review）的优化迭代，解决开箱可用性、命令层入仓、死引用清理等关键问题。

### 🆕 新增

#### 1. 命令文档入仓 (P0-1)

平台中立的 10 个命令定义移至 `docs/commands/*.md`，.claude/commands/*.md 改为薄包装引用。

| 文件 | 说明 |
|------|------|
| `docs/commands/{learn,think,topic-mine,validate,create,quick-create,distribute,review,full-pipeline,style-learn}.md` | 10 个平台中立命令定义 |
| `.claude/commands/{同上}.md` | Claude Code 薄包装（引用 docs/commands/） |
| `docs/mcp-config.md` | MCP Server 配置说明与规划状态 |

#### 2. 质量门 reviewer 子代理定义 (P1-3)

| 文件 | 说明 |
|------|------|
| `.claude/agents/gate-reviewer.md` | 只读 review 子代理定义，对应 6 种质量门类型 |

#### 3. 配置模板入仓 (P1-4)

| 文件 | 说明 |
|------|------|
| `.claude/settings.json.template` | 不含敏感信息的 settings 模板 |
| `.claude/hooks/README.md` | 自动质量门触发钩子模板 |

### ✅ 修复

#### 1. 死引用与口径漂移 (P1-2)

- CLAUDE.md / AGENTS.md 中三种调用方式表全部从 V1.1 编号（A1.1, A2.2, s-3.3.4…）更新为 V2.1 ID
- SKILL-INDEX.md 历史表述从旧编号改为文字说明
- s-3.4.1-fact-check.md 中三处旧 s-3.3.4 引用更新为 s-3.3-style-engine
- s-3.4.1-fact-check.md 三处互斥阈值统一为 ≥8通过 / 7-7.9条件通过 / <7需修改（原表述含 ≥7、<8、<7 三种）
- 🗑️ 删除 `docs/USER-GUIDE.md`（已由 USER-GUIDE-V2.md 取代）

#### 2. 配置与路径修正

- `.gitignore` 从忽略整个 `.claude/` 改为仅忽略私有运行时目录，允许 commands/agents/settings 模板入仓
- MCP 配置表将 knowledge-db / data-analysis 状态从"自建"更新为"规划中，从未建成；当前降级…"
- 口径计数修正：Orchestrator "直接调度 20 个核心 Skill" → "21 个核心 Skill"

#### 3. check_consistency 增强

- 新增 V1.1 死编号（A1.1 ~ A5.3, s-3.3.4, s-3.3.6, USER-GUIDE.md）到 PHANTOM_REFS 扫描
- BRAND_ACTIVE_DOCS / BRAND_CONSUMER_DOCS 从 .claude/commands/ 更新为 docs/commands/
- 实测 check_consistency PASS ✅（零 FAIL）

### 📁 V2.2 文件变更汇总

```
Project/
├── .gitignore                                     [修改] 细粒度 .claude/ 忽略
├── CLAUDE.md                                      [修改] 死ID清理 + MCP表修正 + 口径计数
├── AGENTS.md                                      [修改] 同步 CLAUDE.md 变更
├── .claude/
│   ├── commands/{10 files}.md                     [新建] Claude Code 薄包装命令
│   ├── agents/gate-reviewer.md                    [新建] 质量门 reviewer 子代理定义
│   ├── settings.json.template                     [新建] 配置模板
│   └── hooks/README.md                            [新建] 自动质量门钩子模板
├── docs/
│   ├── commands/{10 files}.md                     [新建] 平台中立命令定义
│   ├── CHANGELOG.md                               [修改] +V2.2
│   ├── USER-GUIDE.md                              [删除] 已由 V2 取代
│   └── mcp-config.md                              [新建] MCP 状态说明
├── scripts/
│   └── check_consistency.py                       [修改] +幽灵引用扫描项
└── skills/m3-creation/
    └── s-3.4.1-fact-check.md                      [修改] 阈值统一 + s-3.3.4→s-3.3
```

## V1.1

初始版本。二级调度架构、5模块15Agent、Context Snapshot 机制、错误恢复与降级方案。
