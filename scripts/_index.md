# 脚本工具索引 · Scripts Index

> 更新时间：2026-03-14

| 文件 | 用途 | 调用场景 |
|------|------|---------|
| tag-assigner.py | 知识库条目自动标签分配 | s-1.3.1 入库时调用 |
| topic-pool-manager.py | 选题库（topics.json）增删改查 | s-2.2.1 评分后调用 |
| publish-checklist-gen.py | 生成多平台发布清单 | M4 分发流程末尾 |
| data-normalizer.py | 运营数据标准化处理 | s-5.1.1 数据采集后调用 |

所有脚本位于 `scripts/` 目录下，使用 Python 3 运行。
纯数据处理任务使用脚本而非 LLM，以节省 tokens。
