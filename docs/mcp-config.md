# MCP Server 配置说明

> 本文档记录本工作流依赖的 MCP Server 配置与状态。
> 当前时间：2026-06-12

## 当前活跃的 MCP Server

以下 MCP Server 在 `~/.claude/settings.json`（全局）或项目级 `.claude/settings.json` 中配置：

| MCP Server | 实现 | 用途 | 状态 |
|------------|------|------|------|
| web-search | `@anthropic/mcp-server-brave-search` | 搜索/热点/竞品 | ✅ 活跃 |
| filesystem | `@anthropic/mcp-server-filesystem` | 读写文件 | ✅ 由 Claude Code 内置 |
| fetch | `@anthropic/mcp-server-fetch` | 网页抓取 | ✅ 由 Claude Code 内置 |

## 规划中的 MCP Server

以下两个 MCP Server 在文档中引用，但**尚未建成**（参见 [#3 未决问题](#3-未决问题)）：

### knowledge-db（向量检索）

- **声明位置**：CLAUDE.md MCP 配置表
- **文档引用**：MCP 表、降级方案（知识库检索超时 → 改用 web-search）
- **当前状态**：**规划中，从未建成**
- **降级路径**：
  - 知识库检索退化为 `grep -r` + 文件遍历（已在 skill 文件中定义）
  - 无向量检索能力，依赖文件名和 frontmatter 标签搜索
- **建议方案**：
  - 选项 A：轻量方案 — 用 `ripgrep` + frontmatter 标签过滤（无需建 server）
  - 选项 B：完整方案 — 用 `python3 -m pip install chromadb` 构建本地向量库 + `mcp-servers/knowledge-db/` MCP server

### data-analysis（运营数据查询）

- **声明位置**：CLAUDE.md MCP 配置表
- **文档引用**：MCP 表
- **当前状态**：**规划中，从未建成**
- **降级路径**：
  - M5 数据目前通过手工录入或脚本采集（具体方式待确认）
  - 无自动化数据管道
- **建议方案**：
  - 选项 A：用 `scripts/` 下的 Python 脚本处理 CSV/JSON 数据文件
  - 选项 B：构建 `mcp-servers/data-analysis/` 支持 SQL 查询分析

## MCP Server 配置示例

### 在 `.claude/settings.json` 中配置（全局）

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "sk-..."
  },
  "mcpServers": {
    "web-search": {
      "type": "command",
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-brave-search"],
      "env": {
        "BRAVE_SEARCH_API_KEY": "你的 Brave API 密钥"
      }
    }
  }
}
```

## 未决问题

1. mcp-servers/knowledge-db 与 data-analysis 是"曾存在已删"还是"从未建成"？
   - **结论**：从未建成。两个自建 server 目录在仓库中不存在，git 历史中也没有它们被删除的记录。它们自 V1.1 架构设计文档起就一直是"规划中"状态。
   - 影响：MCP 配置表应更新为标注"规划中"而非"自建"。
2. M5 平台数据的实际采集方式（手工录入 or 自动化工具）？
   - 待确认。data/pipeline 中未见 feedback 原始事件样本，data_quality_gate 实战表现未知。
3. 是否计划在 MCP 生态可用后再建设这两个 server？
   - 由仓库维护者决定。在当前阶段，降级路径足以覆盖核心工作流。
