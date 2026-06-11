# `.claude/hooks/` — 质量门自动触发钩子模板

> 本目录存放 Claude Code hooks 配置，用于在特定操作发生时自动执行质量门检查。
> 文件说明：复制需要的 `.template` 文件，去除后缀后生效。
> 参考文档：`https://docs.anthropic.com/en/docs/claude-code/hooks`

## 推荐的触发点

| Hook | 触发时机 | 推荐用途 |
|------|---------|---------|
| `PostToolUse` | Claude Code 执行工具之后 | 写入内容目录后自动触发质量门 |
| `Stop` | 会话结束前 | 运行 check_consistency 自检 |

### 示例：PostToolUse — 发布前自动运行 publish_package gate

创建 `.claude/hooks/PostToolUse`（可执行脚本）：

```bash
#!/bin/bash
# 当写入到 content/slices/ 下包含 publish-ready 的目录时，自动运行发布门检查

TOOL="$CLAUDE_TOOL_NAME"
ARGS="$CLAUDE_TOOL_INPUT"

if [[ "$TOOL" == "Write" || "$TOOL" == "Edit" ]]; then
  # 检查是否写入发布就绪目录
  if echo "$ARGS" | grep -q "publish-ready"; then
    echo "[质量门] 检测到发布文件写入，运行 publish_package gate..."

    # 提取 task_id（从文件路径）
    TASK_ID=$(echo "$ARGS" | grep -oP 'slices/\K[^/]+')

    if [ -n "$TASK_ID" ]; then
      python3 scripts/gatekeeper.py validate-publish-package \
        "data/pipeline/$TASK_ID/quality-gates/publish_package_gate.json" || {
        echo "[质量门] ⚠️ 发布门检查未通过，请修复 blocker 后重试"
        exit 1
      }
    fi
  fi
fi
```

### 示例：Stop — 会话结束自检

创建 `.claude/hooks/Stop`（可执行脚本）：

```bash
#!/bin/bash
# 会话结束时运行一致性检查

echo "=== 运行系统自检 ==="
python3 scripts/check_consistency.py 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "⚠️ 系统自检发现 $EXIT_CODE 项问题"
  echo "建议在下个会话中修复"
fi

exit 0
```

## 钩子使用注意事项

1. 钩子脚本必须是**可执行文件**（`chmod +x`）
2. 钩子脚本的 `exit 1` 会**阻断**当前操作——不要在生产流程中贸然启用阻断模式
3. 建议先在非阻断模式（仅记录日志，不 exit 1）下运行一段时间，确认规则无误后再启用阻断
4. 钩子脚本中可访问的环境变量见 Claude Code Hooks 文档
