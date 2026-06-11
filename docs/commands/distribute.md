# `/distribute <content>` — 多平台分发

> 平台中立命令定义 · 事实源：CLAUDE.md / CHANGELOG V1.2
> 适配层：`.claude/commands/distribute.md` 应为此文件的薄包装或符号链接

## 功能

将已完成的创作内容切片、适配并分发到多个平台。

## 涉及模块

M3（内容准备）→ M4（分发）

## 品牌契约

分发的切片内容继承创作阶段的品牌口径。发布前确认应确保各平台切片内容与 `data/brand/brand-canon.yaml` 定义的不矛盾。

## 执行流程

```
内容 → s-4.1 切片与脚本生成 → s-4.2.2 平台适配 → ⚠️ 发布前确认 → s-4.3 互动运营
```

1. **s-4.1 切片引擎**：将长内容按平台特性切片（短视频脚本、图文卡片、问答等）
2. **s-4.2.2 平台适配**：按平台规则调整格式、语气、长度
3. **⚠️ 人工确认**：发布前最终确认（第二个也是最后一个必选人工节点）
4. **s-4.3 互动运营**：发布后互动策略（回复话术、跟进节奏）

## 人工确认节点

- **发布前确认**：Orchestrator 等待创作者确认所有切片内容后方可发布

## 质量门

- `publish_package` gate：验证发布包符合各平台规则（调用 `gatekeeper.validate_publish_package()`）
- 阻断条件：存在任何 fatal/high blocker 且未清零

## 输出

- `content/slices/{parent-id}/` — 切片文件
  - `slice-{seq}-{platform}-{type}.md`
  - `_manifest.md`
- `data/pipeline/create-{id}/distribution-plan.md` — 分发计划
- `data/pipeline/create-{id}/quality-gates/publish_package_gate.json` — 发布门报告

## 依赖 Skill

| Skill | 路径 |
|-------|------|
| s-4.1-slice-engine | `skills/m4-distribution/s-4.1-slice-engine.md` |
| s-4.2.2-adapt | `skills/m4-distribution/s-4.2.2-adapt.md` |
| s-4.3-engagement | `skills/m4-distribution/s-4.3-engagement.md` |
