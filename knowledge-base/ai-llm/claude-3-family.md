# Claude Code

**分类**: AI/LLM
**来源**: https://code.claude.com/docs/llms.txt
**学习日期**: 2026-05-13
**质量分**: 9.5/10
**标签**: #Claude #Anthropic #Agent #Coding #MCP #Skills

---

## 核心概念

Claude Code 是 Anthropic 推出的 agentic 编程工具，可读取代码库、编辑文件、运行命令，并与开发工具集成。提供终端、IDE、桌面应用和浏览器版本。

### 安装方式

| 平台 | 安装命令 |
|------|----------|
| macOS/Linux | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Windows PowerShell | `irm https://claude.ai/install.ps1 \| iex` |
| Windows CMD | `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd` |
| Homebrew | `brew install --cask claude-code` |
| WinGet | `winget install Anthropic.ClaudeCode` |

---

## 核心能力

### 1. 自动化任务
- 写测试、修 lint 错误、解合并冲突、更新依赖、写发布说明
- 跨多文件规划、写代码、验证

### 2. Git 集成
- stage 变更、写 commit 消息、创建分支、打开 PR
- CI 集成：GitHub Actions、GitLab CI/CD

### 3. MCP (Model Context Protocol)
开放标准，连接 AI 工具与外部数据源：
- 读 Google Drive 设计文档
- 更新 Jira 工单
- 从 Slack 拉取数据
- 自定义工具

### 4. Skills 系统
打包可复用的工作流，如 `/review-pr`、`/deploy-staging`

### 5. Hooks
在关键节点运行 shell 命令：
- 每次编辑后自动格式化
- commit 前运行 lint

### 6. Subagents
- 生成多个 agent 同时处理不同子任务
- 主 agent 协调、分配、合并结果
- 支持并行和隔离的 worktree 会话

### 7. CLI 组合
```bash
# 分析日志
tail -200 app.log | claude -p "Slack me if you see any anomalies"
# CI 自动化翻译
claude -p "translate new strings into French and raise a PR"
```

### 8. Routines (定时任务)
- 在 Anthropic 管理的基础设施上运行，关机也继续
- 可按 schedule、API call、GitHub 事件触发
- Desktop 定时任务在本地机器运行

### 9. 多端同步
- Remote Control：从手机继续本地 session
- Channels：Telegram、Discord、iMessage、Webhooks 推入 session
- Web：云端运行，teleport 回终端
- `/desktop`：终端 session 可转到 Desktop app 做视觉 diff

---

## 产品矩阵

| 环境 | 说明 |
|------|------|
| Terminal CLI | 全功能命令行 |
| VS Code | 内联 diffs、@-mentions、plan review |
| Desktop | 并行 session、视觉 diff、定时任务、云 session |
| Web | 浏览器运行，无需本地 setup |
| JetBrains | IntelliJ/PyCharm/WebStorm 插件 |
| iOS | 移动端操作 |

---

## Agent SDK

用于构建自定义 agent，带完整控制权：
- 编排、工具访问、权限控制
- 详细参考：Python API、TypeScript API
- 支持 streaming、structured outputs、hooks、subagents

---

## 关键文档

| 文档 | 用途 |
|------|------|
| `/en/agent-sdk/overview` | SDK 总览 |
| `/en/mcp` | MCP 服务器配置 |
| `/en/skills` | 创建使用 Skills |
| `/en/sub-agents` | 子 agent |
| `/en/hooks-guide` | Hooks 自动化 |
| `/en/routines` | 定时任务 |
| `/en/agent-teams` | 多 agent 团队协作 |
| `/en/cli-reference` | CLI 完整参考 |
| `/en/best-practices` | 最佳实践 |

---

## 更新记录

- 2026-05-13: 更新为 Claude Code 完整文档，来源 code.claude.com
- 2026-04-22: 初始学习 Claude 3 family
