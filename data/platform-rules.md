# 平台规则轻量层 · platform-rules

> 版本：V2.1 | 用途：为 M4 适配/发布与 `publish_package_gate` 提供单一、可核验的平台硬限制来源。
> 设计取舍：**轻量优先**。只记录会导致内容被拒/限流/违规的硬限制 + 核验来源 + 核验日期。**不做** `change_log` 版本机、不做强制 schema。
> 维护规则：每条规则带 `last_verified`；超过 90 天未核验，`publish_package_gate` 应将其标为 `medium` 提醒（非阻断）。

---

## 字段说明

| 字段 | 含义 |
|------|------|
| `platform` | 平台标识 |
| `hard_limits` | 硬限制（超出会被截断/拒绝/限流） |
| `forbidden_terms` | 平台敏感/导流违规词（示例，需按实际核验补充） |
| `soft_recommendations` | 软建议（不阻断，仅提醒） |
| `source_url` | 规则来源链接（官方优先） |
| `last_verified` | 最近一次人工核验日期 |

---

## 小红书 (xiaohongshu)

- **hard_limits**：标题 ≤ 20 字（超出折叠）；正文 ≤ 1000 字；图片 ≤ 18 张；话题标签建议 ≤ 20 个。
- **forbidden_terms**（示例，需核验）：站外引流词（"微信/公众号/加我"）、绝对化用词（"最/第一/100%"）、医疗功效断言。
- **soft_recommendations**：首行含关键词；正文每段 1–3 行；emoji 适量。
- **source_url**：（待补充官方社区规范链接）
- **last_verified**：2026-06-06（占位，需人工核验后更新）

## 公众号 (wechat)

- **hard_limits**：单篇正文无硬字数上限，但封面标题 ≤ 64 字；一天群发条数受订阅号/服务号限制。
- **forbidden_terms**（示例，需核验）：诱导分享/诱导关注话术、夸大医疗/金融收益。
- **soft_recommendations**：每段 ≤ 5 行；重点加粗；开头 30 字告知价值。
- **last_verified**：2026-06-06（占位，需人工核验后更新）

## 知乎 (zhihu)

- **hard_limits**：标题 ≤ 100 字；回答/文章无硬上限。
- **forbidden_terms**（示例，需核验）：站外导流、营销硬广。
- **soft_recommendations**：开头先给结论；增加数据与来源标注。
- **last_verified**：2026-06-06（占位，需人工核验后更新）

## 抖音 (douyin) / B站 (bilibili)

- **hard_limits**：视频标题/简介有平台上限（待核验具体字数）；封面与口播需符合社区规范。
- **forbidden_terms**（示例，需核验）：违规导流、绝对化用词、未标注的商业推广。
- **soft_recommendations**：前 3 秒留人；结尾 CTA。
- **last_verified**：2026-06-06（占位，需人工核验后更新）

---

> ⚠️ 本文件中的 `forbidden_terms` 与字数限制为初始占位，必须经一次人工核验并填入 `source_url` 后，`last_verified` 才视为可信。未核验项在 `publish_package_gate` 中按 `low/medium` 提醒处理。
