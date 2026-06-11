# Pipeline Manifest · 多版并存（最终：v9-ops 为通用主版）

> 流程：/full-pipeline（M1→M5）
> 素材源：hermes_workspace/reports/hotspot/topic_excavation/2026-06-05/ai-recursive-self-improvement/
> 演化：v2通用版 →（深度对话分化）→ v4(已有事业)/v6(还在探索) →（融合v4+v6）→ v7双视角显式版 →（隐性化）→ v8隐性版 →（三版v2+v4+v6融合+隐性化+ops落地）→ **v9-ops 通用主版**。

---

## 版本矩阵

| 版本 | 文件 | 受众 | 核心动作 | 论调 | 字数(中文) | 人群区分 |
|------|------|------|---------|------|------|------|
| v2 | draft-v2.md | 通用（混合） | 三件事 | 温和引导 | 3417 | 显式提及Marcus阶段 |
| v4 | draft-v3-marcus.md | 已有事业 | 月度收入审计 | 锋利诊断 | 5147 | 单视角(Marcus) |
| v6 | draft-v5-lily.md | 还在探索 | 三个月回顾 | 松绑 | 2907 | 单视角(Lily) |
| v7 | draft-v7-merged.md | 双视角融合(v4+v6) | 两件事+共享行动 | 温和诚实 | 6118 | 显式"如果你…" |
| v8 | draft-v8-implicit.md | 双视角(基于v7) | 一个问题+一个动作 | 隐性·偏文学 | 4482 | 隐性(分析段半显式) |
| **v9-ops** | draft-v9-ops.md | 通用主版(v2+v4+v6三版融合) | 一张纸·两栏·一个问题·定期重做 | 温和诚实·可落地 | ~6300 | 隐性(行动段零硬分组) |
| **v10-refined** | **draft-v10-refined.md** | **通用主版·精品压缩(v9压缩)** | **同上（紧凑版）** | **温和诚实·紧凑锐利** | **~5000** | **隐性(行动段零硬分组)** |

**v10-refined 是当前推荐的通用主版**：对 v9-ops 做 -20.5% 压缩（6309→5014字），节奏更紧凑；移除 Altman"幼虫"正文引语（遗留来源风险）；三版融合、隐性双视角、英文全翻译、ops行动脊柱完整保留。适用场景：公众号首发深度位 or 知乎专栏（紧凑更便于完读）；专项切片仍用 v4/v6 精准分发。v9 保留为完整版（如需更多论证展开）。

v2/v4/v6/v7/v8 全部保留不删——作为分化轨迹、专项触达版本和切片母稿。

> 质量门复核（v9 见 quality-gates/content_quality_gate_v9.json，v10 见 content_quality_gate_v10.json）：v9 独立 reviewer 初判 conditional，修复 1 项 high（48倍伪造归因）+ 1 项 low（Imas转述去引号）；驳回 reviewer 的 57.4% 误报。v10 进一步移除 Altman"幼虫"正文引语，0 blocker。**遗留（v4/v7/v8 仍存在，建议复用前清理）**：Anthropic"暂停"来源待确认。**48倍伪造仍残留在 v4/v7/v8 + 抖音切片中，建议一并清理。**

---

## v7 关键设计

| 设计要素 | 实现 |
|---------|------|
| 不使用"Marcus""Lily" | ✅ 零出现。使用"如果你已经有稳定收入""如果你还在找方向" |
| 英文引用全部翻译 | ✅ 5处英文引用，首次出现时全部中文翻译+原文 |
| 双视角区分 | S2 分叉 → S3 共用框架各自解读 → S4 共享硬事实 → S5 共用隐喻各自语境化 → S6 分叉工具但共享底层动作 |
| 两件事 | ①月度收入审计（已有事业）②三个月方向回顾（还在探索）③共享：保护廉价试错场 |

---

## 全流程产出

### M1 · 知识积累
| 文件 | 说明 |
|------|------|
| `p1-p4-deep-think.md` | P1-P4四层深度思考 |
| `knowledge-base/technology/...ai-recursive-self-improvement.md` | RSI五层证据 |
| `knowledge-base/mindset/...relational-sector-economics.md` | 关系性部门 |
| `knowledge-base/viewpoint/...cointelligence-to-coexistence.md` | Mollick叙事转折 |

### M2 · 选题策划
| 文件 | 说明 |
|------|------|
| `topic-mine-report.md` | 10选题池 |
| `topic-validation-report.md` | 9.3/10 |

### M3 · 内容创作（多版）
| 文件 | 版本 | 状态 |
|------|------|------|
| `draft-v1.md` | v1 | 初稿 |
| `draft-v2.md` | v2-final | 通用版 |
| `draft-v3-marcus.md` | v4-marcus | Marcus专项 |
| `draft-v5-lily.md` | v6-lily | Lily专项 |
| `draft-v7-merged.md` | v7-final | 双视角融合(显式) |
| `draft-v8-implicit.md` | v8-implicit | 双视角隐性版 |
| `draft-v9-ops.md` | **v9-ops** | **通用主版(三版融合)** |
| `draft-v10-refined.md` | **v10-refined** | **通用主版·精品压缩(推荐)** |
| `iteration-report.md / v3 / v5 / v7 / v8 / v9 / v10` | 七个迭代报告 | |
| `style-check-report.json / v3 / v5` | 风格校验 | |
| `quality-gates/` | content_quality ×(v2/v3/v5/v7/v9/v10) + publish_package ×2 | 全部 pass（v9/v10 修复后 pass） |

### M4 · 切片（18个）
- v2通用：6个（slice-001~006）
- v4 Marcus专版：4个（slice-007~010）
- v6 Lily专版：4个（slice-011~014）
- v7 融合版：待生成

### M5 · 数据反馈
| 文件 | 说明 |
|------|------|
| `review-framework.md` | KPIs+复盘框架 |
| `optimization-strategy.md` | 4洞察+3系统改进 |

---

## 质量门

| Gate | 版本 | 状态 |
|------|------|------|
| content_quality_gate | v2 | conditional pass |
| content_quality_gate_v3 | v4 | ✅ pass |
| content_quality_gate_v5 | v6 | ✅ pass |
| content_quality_gate_v7 | v7 | ✅ pass, 0 blockers |
| **content_quality_gate_v9** | **v9-ops** | **✅ pass（独立审查初判conditional→修复high+low后pass；2项流程级遗留来源待清理）** |
| **content_quality_gate_v10** | **v10-refined** | **✅ pass, 0 blockers（压缩版；48x伪造+Altman幼虫均已移除）** |

---

## 发布建议

- **首发**：v10-refined 精品压缩版（公众号/知乎）——三版融合、隐性双视角、~5000字紧凑更便于完读
- **备选**：v9-ops 完整版（如需要更多论证展开）
- **同日/次日**：v4 Marcus版知乎问答 + v6 Lily版小红书图文（专项精准触达）
- **抖音梯度释放**：v4/v6 各两条短口播，分3天
- **v2 通用版 / v8 隐性版**：作为轻量/备选版在即刻/微博分发
- **发布前**：清理 v9 的 2 项流程级遗留来源（Anthropic"暂停"、Altman"幼虫"），与各版口径一并处理
