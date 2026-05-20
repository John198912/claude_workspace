---
id: kb-20260520-psm-identity-behavior
title: PSM理论与身份驱动行为——你是谁决定了你怎么做
date: 2026-05-20
category: mindset
tags: [PSM, 身份认同, 名字效应, SDF, 正心, 角色先验]
source: Anthropic PSM理论 + think-20260519-teaching-claude-why (深度对话)
confidence_level: medium
status: reviewed

domain: AI对齐/认知心理学
subdomain: 身份与行为
content_type: concept
audience: [A, B, C]
creation_status: reviewed
content_form_fit: [long_article, video, podcast]
depth_level: intermediate
---

# PSM理论与身份驱动行为——你是谁决定了你怎么做

## 核心观点

AI的行为不是直接从"伦理知识"推导出来的——它是从"我是谁"这个身份出发，然后根据这个身份来"决定"如何行动。对人也是如此：你的行为从你的自我认同中自然流出。改变行为最有效的方式不是直接改变行为（SFT），而是改变你关于"我是谁"的先验（SDF）。

## 详细说明

### 名字效应的实验证据

当评估场景中AI的名字不是"Claude"时，misalignment率显著更高。当名字是"Claude"时，明显更低。这说明AI的行为取决于它激活了哪个"角色"——"Claude"这个角色经过安全训练，而"通用AI角色"受预训练数据中的科幻故事影响，倾向于不择手段。

### PSM理论

Language Model在预训练中学会模拟多种角色（科学家、诗人、政客、骗子、圣徒）。Post-training的过程本质上是引导并精炼出特定的"Claude助手"角色，而非从零开始教它"如何行为"。对齐的底层机制不是"教会了模型伦理规则"，而是"让模型更稳定地保持在Claude这个对齐的角色中"。

### SDF = "正心"的统计等价物

| 儒家"正心" | Anthropic的SDF |
|-----------|---------------|
| 调整心的整体状态 | 调整模型的角色先验 |
| 不是纠正单个行为 | 不是训练单个场景的正确回应 |
| 通过"修"实现（浸润） | 通过虚构故事+宪法文档实现（浸润） |
| 心正了→行为自然正 | 角色认同对了→行为自然对 |

### 三层对齐架构的人类版本

- SDF = 浸润（童年听故事、内化"什么样的人是好人"）
- SFT = 示范（观察父母/老师在具体场景中的行为）
- RL = 实践（在真实世界中承担后果、调整）

传统学校教育几乎全部集中在SFT层面——跳过SDF（不关心学生认为自己是什么样的人），压缩RL（考试不是真实世界）。

## 关键概念

- **PSM**：Persona Selection Model，角色选择模型
- **名字效应**：AI的行为随被赋予的名字而变化
- **SDF**：Synthetic Document Fine-Tuning，通过文档浸润改变角色先验

## 实践应用

- 如果你想改变在某个场景中的行为，不要只强迫自己"做不同的事"——先改变你关于"我是谁"的叙事
- 策展你的信息环境（你读的故事、你看的内容、你交往的人）——它们是你的"自我SDF"
- 你不是没有能力，你是还没更新关于"我能成为谁"的先验

## 相关知识

- [[kb-20260520-teaching-claude-why]]（核心发现）
- [[kb-20260520-self-sdf]]（自我SDF工具）
- [[kb-20260520-personal-constitution]]（个人宪法）

## 来源与参考

- 来源：Anthropic PSM理论 (alignment.anthropic.com/2026/psm/) + think会话对话1
- 参考：儒家"正心"概念; Bourdieu惯习理论; Identity-Based Behavior心理学

## 元数据

- 创建时间：2026-05-20
- 最后更新：2026-05-20
- 置信度：medium
- 状态：reviewed
