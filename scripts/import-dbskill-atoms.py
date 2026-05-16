#!/usr/bin/env python3
"""
dbskill 知识原子库导入脚本

功能:
1. 从 dbskill 仓库的 JSONL 文件导入知识原子
2. 转换为 Markdown + YAML frontmatter 格式
3. 实施质量过滤 (confidence_level)
4. 自动分类映射
5. 保持来源追溯性

使用:
    python scripts/import-dbskill-atoms.py --quarter 2025Q4
    python scripts/import-dbskill-atoms.py --quarter all --confidence high,medium
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
import re
import requests

# 配置
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/dontbesilent2025/dbskill/main"
ATOMS_BASE_PATH = "知识库/原子库"
OUTPUT_BASE = "knowledge-base/imported/dbskill/atoms"
LOG_FILE = "data/logs/dbskill-import-log.jsonl"

# 分类映射规则
CATEGORY_MAPPING = {
    "business": ["产品", "需求", "转化", "商业模式", "定价", "私域", "知识付费", "变现", "增长"],
    "technology": ["提示词", "智能体", "AI", "模型", "工具", "技术", "算法", "平台"],
    "mindset": ["认知", "心理", "哲学", "思维", "维特根斯坦", "阿德勒", "齐泽克"],
    "growth": ["个人成长", "执行", "行动", "学习", "习惯", "自律"],
    "viewpoint": ["观点", "方法论", "原则", "洞察", "反思", "批判"]
}

def map_to_category(topics):
    """根据主题标签映射到本地分类"""
    if not topics:
        return "viewpoint"  # 默认分类

    # 统计每个分类的匹配度
    scores = {cat: 0 for cat in CATEGORY_MAPPING.keys()}

    for topic in topics:
        for category, keywords in CATEGORY_MAPPING.items():
            if any(keyword in topic for keyword in keywords):
                scores[category] += 1

    # 返回得分最高的分类
    max_category = max(scores, key=scores.get)
    return max_category if scores[max_category] > 0 else "viewpoint"

def sanitize_filename(text, max_length=60):
    """清理文件名,移除非法字符"""
    # 移除或替换非法字符
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = text.strip('-')

    # 限制长度
    if len(text) > max_length:
        text = text[:max_length].rsplit('-', 1)[0]

    return text or "untitled"

def convert_atom_to_markdown(atom):
    """将 JSONL 原子转换为 Markdown + YAML frontmatter"""

    # 提取字段
    atom_id = atom.get("id", "unknown")
    knowledge = atom.get("knowledge", "")
    original = atom.get("original", "")
    url = atom.get("url", "")
    date = atom.get("date", "")
    topics = atom.get("topics", [])
    skills = atom.get("skills", [])
    content_type = atom.get("type", "insight")
    confidence = atom.get("confidence", "medium")

    # 映射分类
    category = map_to_category(topics)

    # 生成标题 (knowledge 前60字符)
    title = knowledge[:60] + ("..." if len(knowledge) > 60 else "")

    # 合并标签
    all_tags = list(set(topics + skills))

    # 生成文件名
    date_prefix = date.replace("-", "") if date else "unknown"
    filename_base = sanitize_filename(knowledge[:40])
    filename = f"{date_prefix}-{atom_id}-{filename_base}.md"

    # 构建 YAML frontmatter
    frontmatter = f"""---
id: {atom_id}
title: "{title}"
date: {date}
tags: {json.dumps(all_tags, ensure_ascii=False)}
category: {category}
source: {url}
source_type: "dbskill_atom"
confidence_level: {confidence}
status: reviewed
content_type: {content_type}
imported_from: "dbskill"
import_date: {datetime.now().strftime("%Y-%m-%d")}
---

"""

    # 构建 Markdown 内容
    content = f"""# {title}

## 知识陈述

{knowledge}

## 原始推文

> {original}

## 元数据

- **来源**: [{url}]({url})
- **发布日期**: {date}
- **主题标签**: {", ".join(topics)}
- **相关技能**: {", ".join(skills) if skills else "无"}
- **内容类型**: {content_type}
- **置信度**: {confidence}

## 使用说明

本知识原子来自 [@dontbesilent](https://github.com/dontbesilent2025/dbskill) 的推文提炼,遵循 CC BY-NC 4.0 许可证。

**适用场景**:
- M1 知识积累: 作为深度思考的参考素材
- M2 选题策划: 识别内容方向和受众痛点
- M3 内容创作: 提供观点和案例支撑

**注意事项**:
- 原子基于推文提炼,可能缺少完整上下文
- 部分案例具有时效性,使用时需验证
- 建议结合其他来源交叉验证
"""

    return frontmatter + content, filename, category

def fetch_jsonl_from_github(quarter):
    """从 GitHub 获取指定季度的 JSONL 文件"""
    if quarter == "all":
        filename = "atoms.jsonl"
    else:
        filename = f"atoms_{quarter}.jsonl"

    url = f"{GITHUB_RAW_BASE}/{ATOMS_BASE_PATH}/{filename}"

    print(f"正在获取: {url}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"❌ 获取失败: {e}")
        return None

def parse_jsonl(jsonl_text):
    """解析 JSONL 文本为原子列表"""
    atoms = []
    for line_num, line in enumerate(jsonl_text.strip().split('\n'), 1):
        if not line.strip():
            continue
        try:
            atom = json.loads(line)
            atoms.append(atom)
        except json.JSONDecodeError as e:
            print(f"[WARN] 第 {line_num} 行解析失败: {e}")

    return atoms

def filter_atoms(atoms, confidence_levels):
    """根据置信度过滤原子"""
    if not confidence_levels:
        return atoms

    allowed = set(confidence_levels)
    filtered = [atom for atom in atoms if atom.get("confidence") in allowed]

    print(f"[FILTER] 过滤结果: {len(atoms)} -> {len(filtered)} (保留 {len(filtered)/len(atoms)*100:.1f}%)")

    return filtered

def import_atoms(quarter, confidence_levels, dry_run=False):
    """导入知识原子"""

    # 获取 JSONL 数据
    jsonl_text = fetch_jsonl_from_github(quarter)
    if not jsonl_text:
        return False

    # 解析原子
    atoms = parse_jsonl(jsonl_text)
    print(f"[OK] 解析成功: {len(atoms)} 个原子")

    # 过滤
    atoms = filter_atoms(atoms, confidence_levels)

    if dry_run:
        print(f"[DRY RUN] 将导入 {len(atoms)} 个原子")
        # 显示前3个示例
        for i, atom in enumerate(atoms[:3], 1):
            print(f"\n示例 {i}:")
            print(f"  ID: {atom.get('id')}")
            print(f"  知识: {atom.get('knowledge')[:60]}...")
            print(f"  置信度: {atom.get('confidence')}")
            print(f"  主题: {', '.join(atom.get('topics', [])[:3])}")
        return True

    # 创建输出目录
    os.makedirs(OUTPUT_BASE, exist_ok=True)

    # 统计
    stats = {
        "total": len(atoms),
        "success": 0,
        "failed": 0,
        "by_category": {},
        "by_confidence": {},
        "by_type": {}
    }

    # 转换并写入
    for atom in atoms:
        try:
            markdown, filename, category = convert_atom_to_markdown(atom)

            # 创建分类子目录
            category_dir = os.path.join(OUTPUT_BASE, category)
            os.makedirs(category_dir, exist_ok=True)

            # 写入文件
            filepath = os.path.join(category_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown)

            # 更新统计
            stats["success"] += 1
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

            confidence = atom.get("confidence", "unknown")
            stats["by_confidence"][confidence] = stats["by_confidence"].get(confidence, 0) + 1

            content_type = atom.get("type", "unknown")
            stats["by_type"][content_type] = stats["by_type"].get(content_type, 0) + 1

        except Exception as e:
            print(f"[WARN] 导入失败 [{atom.get('id')}]: {e}")
            stats["failed"] += 1

    # 记录日志
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "quarter": quarter,
        "confidence_filter": confidence_levels,
        "stats": stats
    }

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    # 打印报告
    print(f"\n{'='*60}")
    print(f"[REPORT] 导入完成: {quarter}")
    print(f"{'='*60}")
    print(f"[OK] 成功: {stats['success']}")
    print(f"[FAIL] 失败: {stats['failed']}")
    print(f"\n[STATS] 按分类统计:")
    for cat, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")
    print(f"\n[STATS] 按置信度统计:")
    for conf, count in sorted(stats['by_confidence'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {conf}: {count}")
    print(f"\n[STATS] 按类型统计:")
    for ctype, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {ctype}: {count}")

    return True

def main():
    # 设置控制台编码为UTF-8
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(description="导入 dbskill 知识原子库")
    parser.add_argument("--quarter", default="2025Q4",
                       help="季度 (2024Q4, 2025Q1, 2025Q2, 2025Q3, 2025Q4, 2026Q1, all)")
    parser.add_argument("--confidence", default="high,medium",
                       help="置信度过滤 (high, medium, low, 逗号分隔)")
    parser.add_argument("--dry-run", action="store_true",
                       help="试运行,不实际写入文件")

    args = parser.parse_args()

    # 解析置信度过滤
    confidence_levels = [c.strip() for c in args.confidence.split(',') if c.strip()]

    print(f">> 开始导入 dbskill 知识原子")
    print(f"   季度: {args.quarter}")
    print(f"   置信度过滤: {', '.join(confidence_levels)}")
    print(f"   模式: {'DRY RUN' if args.dry_run else 'PRODUCTION'}")
    print()

    success = import_atoms(args.quarter, confidence_levels, args.dry_run)

    if success:
        print(f"\n[OK] 导入完成!")
        if not args.dry_run:
            print(f"[*] 输出目录: {OUTPUT_BASE}")
            print(f"[*] 日志文件: {LOG_FILE}")
    else:
        print(f"\n[ERROR] 导入失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
