# 关键节点独立审查协议 · QUALITY-GATES

> 版本：V2.1 | 更新日期：2026-06-06
> 定位：本文件是「独立质量门」的**唯一权威来源**。CLAUDE.md / SKILL-INDEX / USER-GUIDE / DIRECTORY-MAP 在涉及质量门时一律指向此处。

---

## 0. 设计原则（为什么不是 25 个常驻 reviewer）

本系统是**单人、低产量、且以思辨/解释型内容为主**的创作系统。因此：

1. **文档自洽优先**：先让协议、契约、路径自洽，再谈审查。否则只是把矛盾流程"自动化得更快"。
2. **只在关键节点设独立审查**：独立子 agent 只在会导致 **入库 / 发布 / 策略调整 / 事实可信度变化** 的节点触发。
3. **审查价值来自上下文隔离与阻断能力，而非 reviewer 数量**。
4. **区分主张类型**：`fact`（实证主张）才要求证据；`interpretation / metaphor / opinion`（解释/隐喻/观点）不强制证据——这是哲学随笔的合法表达，不得被"缺证据默认阻断"误杀。
5. **按需扩展**：只有当某类问题反复发生，才新增专门 reviewer。

---

## 1. Gate Policy（通用策略）

- **reviewer 不是常驻角色**，而是按产物触发的**临时、独立、只读子 agent**（用 Agent 工具以 fresh context 拉起）。
- reviewer **只读输入、不参与生成、不直接改稿**，只产出 `quality_gate_report`。
- 每个 gate 产出统一 `quality_gate_report`（schema：`data/schemas/quality_gate_report.schema.json`），落盘到
  `data/pipeline/{task_id}/quality-gates/{stage}-{gate}.json`。
- **阻断规则**：任一 `fatal` 或 `high` blocker 未清零 ⇒ `gate_status=blocked` ⇒ 禁止进入下游，由 Orchestrator 决定返工或人工介入。
- **`skip_with_warning` 的边界**：只能用于**非发布、非入库、非策略调整**的低风险流程（如 SEO 微调、风格自动改写跳过）。涉及 KB 入库/升级、发布、M5 策略结论的节点**禁止** `skip_with_warning`。
- **生成者自评不得作为通过依据**：同一生成 agent 的自查只能作为参考，gate 通过必须有独立 reviewer 报告（记录不同 `reviewer.agent_id` + `context_mode=fresh_independent`）。
- **可执行内核**：四类可被代码判定的阻断逻辑落在 `scripts/gatekeeper.py`，供 reviewer/Orchestrator 调用获得确定性裁决（见 §4）。

---

## 2. 六个关键 Gate

| Gate | 触发时机 | 审查对象 | 主要阻断项（fatal/high） |
|------|---------|---------|------------------------|
| `workflow_consistency_gate` | 文档/目录变更后、或定期 | 5 份核心文档 + 目录 + 命令入口 | 声明的命令目录/文件不存在；Skill 计数与花名册不符；声明路径不存在 |
| `source_evidence_gate` | M1 采集后、入库或深度思考前 | 信息源与事实主张 | 单来源未交叉验证却被当作 fact；来源等级不明/利益冲突未披露 |
| `kb_publish_gate` | 知识条目入库、或升级 `reviewed/core` 前 | 知识条目 | 未验证/单来源条目尝试升 `reviewed/core`；必填字段缺失 |
| `content_quality_gate` | M3 大纲、终稿、改写回归、事实核查（合并审查） | 大纲/终稿/改写后产物 | 改写后新增事实未复核；实证 claim 无来源；硬性事实错误 |
| `publish_package_gate` | M4 发布包生成后、导出/发布前 | 发布包（slice Markdown） | 正文为空/导出脚本读不到正文；缺必填分节；命中平台硬限制/违规词 |
| `data_quality_gate` | M5 复盘前、结论产出时 | 原始数据 + 复盘结论 | 缺样本/缺字段当 0 用；无 A/B 却输出 `causal` 结论 |

> 归因与实验审查**并入** `data_quality_gate`，不设独立 `attribution_experiment_auditor` 常驻 agent。
> 默认只允许输出 `descriptive` 或 `correlational` 结论；**只有存在明确 A/B 测试 schema 时才允许 `causal`**。

---

## 3. 各 Gate 细则

### 3.1 workflow_consistency_gate
- 可执行内核：`python3 scripts/check_consistency.py`（命令目录存在性、Skill 计数、声明路径存在性）。
- 阻断：linter 报 `FAIL` 即 `blocked`。

### 3.2 source_evidence_gate（M1，接入 s-1.1-info-intake）
- 检查：来源数量、来源等级（原始/二手）、作者与日期、利益冲突。
- 规则：单来源内容标 `unverified`，**可进入思考流但不得在 KB 标 fact**；多来源（≥2 独立）才可标 `verified`。
- `skip_with_warning`：禁止（入库相关）。

### 3.3 kb_publish_gate（M1，接入 s-1.3-kb-build）
- 规则：`unverified` 或单来源条目**最高停留在 `draft`**；升 `reviewed` 需 ≥2 独立来源或一次显式交叉核验；升 `core` 需 `reviewed` + 多次高价值引用。
- 可执行内核：`gatekeeper.validate_kb_entry()`。
- `skip_with_warning`：禁止。

### 3.4 content_quality_gate（M3，合并 outline/draft/rewrite-regression/fact-check）
- 合并原 outline_gate / draft_contract / rewrite_regression / fact_evidence 四个意图为**一个独立审查**，按内容性质裁剪：
  - 实证型内容：逐 fact claim 给 verdict；致命错误（编造数据）`fatal` 阻断。
  - 思辨/解释型内容：不强制证据账本，重点查"改写后是否悄悄新增了未复核的事实主张"。
- 改写回归：所有迭代/风格/SEO 改写后必跑一次本 gate 的回归检查（新增 claim 必须复核）。
- **人味儿回归（V2.3）**：改写回归判 AI 味时须按 `skills/m3-creation/s-3.4.2-ai-check/README.md` 的 **V2.0 方法论修正层**执行，而非旧的22特征全文盲扫：只审改动过的段 / 守住人写迹象白名单（口语毛边/跨度/具体细节不计 AI 味） / 多个信号聚集才判定 / 不要误伤作者原稿。原稿/口述稿润色适用 a-3.2.4-iterate 的「模式B·少动」纪律。
- `skip_with_warning`：仅限非事实性的风格/SEO 微调。

### 3.5 publish_package_gate（M4，接入 s-4.2.2-adapt + xiaohongshu-export.py）
- 契约：发布包必须符合 `data/schemas/publish_package.schema.json`（即导出脚本可读的 slice Markdown 分节）。
- 阻断：正文为空、缺 `## 正文`、未知平台无导出器、命中 `data/platform-rules.md` 硬限制。
- **公众号排版反炫技（V2.3）**：适配公众号时据 `skills/m4-distribution/s-4.2.2-adapt.md` 公众号段的**反炫技自检阈值**核对：callout 类视觉块 > 4 / 高亮 > 5 / emoji 标题 > 3 / 表格列 > 4 / 连续 6 章节同一 `①②③` 前缀 —— 超阈值的视觉元素计为“炫技扣分”，要求回砍后再通过。同时核对 `data/platform-rules.md` 的 `format_compat` 硬兼容事实（私有容器语法/Mermaid/半角标点等）。
- 可执行内核：`gatekeeper.validate_publish_package()` + `scripts/test_xiaohongshu_export.py`。
- `skip_with_warning`：禁止（发布相关）。

### 3.6 data_quality_gate（M5，接入 s-5.1.1/s-5.2/s-5.3）
- 数据质量：缺失/重复/口径/采集时间；缺失字段登记 `missing_fields`，禁止当 0。
- 结论分级：`descriptive | correlational | causal`；无 A/B 或实验设计 ⇒ 禁止 `causal`。
- 可执行内核：`gatekeeper.validate_review_conclusion()`。
- `skip_with_warning`：禁止（策略调整相关）。

---

## 4. 可执行内核（scripts/gatekeeper.py）

把四类可代码判定的阻断逻辑做成纯函数，供 reviewer/Orchestrator 调用，得到确定性 `(status, blockers)`：

| 函数 | 对应 Gate | 阻断条件（摘要） |
|------|----------|----------------|
| `validate_kb_entry(entry)` | kb_publish_gate | 目标状态 ∈ {reviewed, core} 且 来源 < 2 或 verified=False；必填字段缺失 |
| `validate_publish_package(pkg)` | publish_package_gate | body 为空；缺必填字段；platform 未知 |
| `validate_review_conclusion(c)` | data_quality_gate | conclusion_level=causal 且 无 ab_test 证据；is_imputed 且 causal |
| `validate_quality_gate_report(r)` | 通用 | 缺必填字段；存在 fatal/high blocker 但 status≠blocked |

> 这些函数是"可阻断"承诺的落地点。agent 驱动的语义审查（如解释 vs 事实的判别）仍由 reviewer 子 agent 完成，但**硬规则**由代码兜底，可被 `scripts/test_gatekeeper.py` 回归。

---

## 5. 必测阻断场景（最小集）

不为 6 门铺全量测试，先覆盖以下高风险场景（见 `scripts/test_gatekeeper.py` / `scripts/test_xiaohongshu_export.py` / `scripts/check_consistency.py`）：

1. 文档声明的命令目录/文件不存在 → `workflow_consistency_gate` FAIL。
2. 未验证/单来源条目尝试升 `reviewed/core` → `kb_publish_gate` blocked。
3. 自动改写后新增事实但未复核 → `content_quality_gate` blocked（语义，reviewer 判定 + 报告校验）。
4. 发布包正文为空 / 导出脚本读不到正文 → `publish_package_gate` blocked。
5. M5 缺样本/估算值却输出 `causal` 结论 → `data_quality_gate` blocked。
6. `quality_gate_report` 含 fatal/high blocker 却标 pass → 报告自身校验 blocked。

通过这些测试后，再考虑是否新增 gate。

---

## 版本历史
- **V2.1（2026-06-06）**：建立 6-gate 独立审查协议、轻量 `quality_gate_report`、可执行 gatekeeper 内核；归因审查并入 data_quality_gate；不建设 25 门常驻 reviewer。
