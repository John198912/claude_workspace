#!/bin/bash

# 复制脚本：将今天生成的所有文件复制到目标目录
# 目标目录：D:\#news-info\0427

TARGET_DIR="D:\#news-info\0427"
SOURCE_BASE="D:\#WorkSpace\Antigravity\内容管理\ProjectFilesV1.1"

echo "开始复制文件到 ${TARGET_DIR}"
echo "================================"

# 创建目标目录结构
mkdir -p "${TARGET_DIR}/content/drafts"
mkdir -p "${TARGET_DIR}/knowledge-base/technology"
mkdir -p "${TARGET_DIR}/data/pipeline/think-20260425-hinton-ai-warning"

# 1. 复制三篇新创作的文章
echo "复制新创作的文章..."
cp "${SOURCE_BASE}/content/drafts/2026-04-26-hinton-warning-survival-line.md" "${TARGET_DIR}/content/drafts/"
cp "${SOURCE_BASE}/content/drafts/2026-04-26-transformation-window-guide.md" "${TARGET_DIR}/content/drafts/"
cp "${SOURCE_BASE}/content/drafts/2026-04-26-regulation-paradox.md" "${TARGET_DIR}/content/drafts/"

# 2. 复制更新的知识库文件
echo "复制知识库文件..."
cp "${SOURCE_BASE}/knowledge-base/technology/2026-04-25-hinton-ai-warning.md" "${TARGET_DIR}/knowledge-base/technology/"

# 3. 复制 pipeline 相关文件
echo "复制 pipeline 文件..."
cp -r "${SOURCE_BASE}/data/pipeline/think-20260425-hinton-ai-warning" "${TARGET_DIR}/data/pipeline/"

# 4. 复制更新的索引文件
echo "复制索引文件..."
cp "${SOURCE_BASE}/data/pipeline/_index.md" "${TARGET_DIR}/data/pipeline/"

echo "================================"
echo "复制完成！"
echo ""
echo "已复制的文件："
echo "1. 三篇新文章（content/drafts/）"
echo "   - 2026-04-26-hinton-warning-survival-line.md"
echo "   - 2026-04-26-transformation-window-guide.md"
echo "   - 2026-04-26-regulation-paradox.md"
echo ""
echo "2. 知识库文件（knowledge-base/technology/）"
echo "   - 2026-04-25-hinton-ai-warning.md"
echo ""
echo "3. Pipeline 完整目录（data/pipeline/think-20260425-hinton-ai-warning/）"
echo "   - _manifest.md"
echo "   - preparation-report.md"
echo "   - output/meta-material.md"
echo "   - output/prompts/*.md"
echo ""
echo "4. Pipeline 索引（data/pipeline/_index.md）"
