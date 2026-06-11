# `/style-learn <creator>` — 学习创作者风格

> 平台中立命令定义 · 事实源：CLAUDE.md / CHANGELOG V1.2
> 适配层：`.claude/commands/style-learn.md` 应为此文件的薄包装或符号链接

## 功能

分析指定创作者的写作风格，提取风格特征并存入风格档案。

## 涉及模块

M3.3（s-3.3-style-engine）

## 执行流程

```
创作者内容样本 → 风格特征提取 → 风格档案入库
```

1. 收集/获取创作者公开内容样本
2. 分析语言特征：句式长度、修辞偏好、语气、用词习惯
3. 分析结构特征：段落组织、标题风格、开头/结尾模式
4. 生成结构化风格档案并写入 `data/style-profiles/`

## 输出

- `data/style-profiles/{creator-slug}.json` — 风格档案文件
- 风格档案可用于后续 M3 创作的风格校验和改写参考

## 依赖 Skill

| Skill | 路径 |
|-------|------|
| s-3.3-style-engine | `skills/m3-creation/s-3.3-style-engine.md` |
