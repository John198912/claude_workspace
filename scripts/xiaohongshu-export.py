#!/usr/bin/env python3
"""
小红书内容导出助手
V2.0: 智能优化版 - 支持emoji添加、字数检查、Markdown清理、发布建议
"""

import re
import sys
import json
import os
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass


# 小红书平台限制配置
XHS_LIMITS = {
    'cover_max': 20,
    'cover_warning': 15,
    'body_min': 200,
    'body_optimal_min': 300,
    'body_optimal_max': 800,
    'body_warning_max': 1000,
    'tags_min': 8,
    'tags_optimal_min': 10,
    'tags_optimal_max': 15,
    'tags_max': 20,
}

# Emoji 关键词映射
EMOJI_MAP = {
    '思考': '🤔',
    '问题': '❓',
    '为什么': '❓',
    '重要': '⚠️',
    '注意': '💡',
    '建议': '✅',
    '方法': '📝',
    '技巧': '📝',
    '步骤': '📝',
    '结果': '🎯',
    '目标': '🎯',
    '数据': '📊',
    '统计': '📊',
    '时间': '⏰',
    '开始': '🚀',
    '启动': '🚀',
    'AI': '🤖',
    '人工智能': '🤖',
    '人': '👤',
    '个人': '👤',
    '工作': '💼',
    '职场': '💼',
    '学习': '📚',
    '读书': '📚',
    '成长': '🌱',
    '进步': '🌱',
    '成功': '✨',
    '收获': '✨',
    '失败': '💔',
    '结束': '🏁',
    '完成': '🏁',
    '第一': '1️⃣',
    '第二': '2️⃣',
    '第三': '3️⃣',
    '第四': '4️⃣',
    '第五': '5️⃣',
    '1': '1️⃣',
    '2': '2️⃣',
    '3': '3️⃣',
    '4': '4️⃣',
    '5': '5️⃣',
    '热爱': '❤️',
    '喜欢': '❤️',
    '价值': '💎',
    '财富': '💰',
    '赚钱': '💰',
    '自由': '🕊️',
    '独立': '🕊️',
}

# 热门标签库（用于补充）
POPULAR_TAGS = {
    '大话题': ['个人成长', '职场', '自我提升', '认知觉醒', '人生感悟'],
    '中话题': ['AI时代', '超级个体', '一人公司', '职业转型', '副业赚钱'],
    '小话题': ['内容创作', '写作技巧', '思维模型', '时间管理', '效率工具'],
}

# 内容类型关键词映射
CONTENT_TYPE_KEYWORDS = {
    '职场': ['工作', '职场', '裁员', '失业', '面试', '简历', '同事', '老板'],
    '成长': ['成长', '改变', '突破', '认知', '觉醒', '迷茫', '焦虑'],
    '方法': ['方法', '步骤', '技巧', '攻略', '指南', '教程', '怎么做'],
}


def get_publish_history_path():
    """获取发布历史文件路径"""
    history_dir = Path('data')
    history_dir.mkdir(parents=True, exist_ok=True)
    return history_dir / 'publish-history.json'


def load_publish_history():
    """加载发布历史"""
    history_path = get_publish_history_path()
    if history_path.exists():
        with open(history_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_publish_history(history):
    """保存发布历史"""
    history_path = get_publish_history_path()
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def check_publish_status(content_id: str) -> str:
    """检查内容发布状态"""
    history = load_publish_history()
    if content_id in history:
        last_publish = history[content_id]
        return f"已发布（上次：{last_publish.get('date', '未知')}）"
    return "草稿（未发布）"


def record_publish(content_id: str, platform: str = "小红书"):
    """记录发布"""
    history = load_publish_history()
    history[content_id] = {
        'date': datetime.now().isoformat(),
        'platform': platform,
        'published_at': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    save_publish_history(history)


def detect_content_type(text: str) -> str:
    """检测内容类型"""
    text = text.lower()
    scores = {}
    for content_type, keywords in CONTENT_TYPE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        scores[content_type] = score

    if max(scores.values()) == 0:
        return 'general'
    return max(scores, key=scores.get)


def get_publish_time_advice(content_type: str) -> dict:
    """根据内容类型获取发布时间建议"""
    advice_map = {
        '职场': {
            'primary': '08:00',
            'reason': '通勤时间，职场人群活跃',
            'alternatives': ['12:00', '18:00']
        },
        '成长': {
            'primary': '20:00',
            'reason': '睡前阅读时段，成长焦虑高发',
            'alternatives': ['21:00', '22:00']
        },
        '方法': {
            'primary': '12:00',
            'reason': '午休时间，适合收藏学习方法',
            'alternatives': ['13:00', '20:00']
        },
        'general': {
            'primary': '20:00',
            'reason': '晚间黄金时段',
            'alternatives': ['08:00', '12:00']
        }
    }
    return advice_map.get(content_type, advice_map['general'])


def add_smart_emoji(text: str, emoji_density: int = 4) -> str:
    """
    智能添加 emoji
    emoji_density: 每几句添加一个emoji
    """
    lines = text.split('\n')
    result_lines = []
    emoji_count = 0

    for i, line in enumerate(lines):
        if not line.strip():
            result_lines.append(line)
            continue

        # 检查是否需要添加 emoji
        if i % emoji_density == 0 and i > 0:
            # 查找匹配的 emoji
            added_emoji = False
            for keyword, emoji in EMOJI_MAP.items():
                if keyword in line and emoji not in line:
                    # 在段落开头添加 emoji
                    line = f"{emoji} {line}"
                    added_emoji = True
                    emoji_count += 1
                    break

        result_lines.append(line)

    return '\n'.join(result_lines)


def clean_markdown(text: str) -> str:
    """清理 Markdown 格式，保留小红书支持的格式"""
    # 保留加粗 **文本**，移除其他 Markdown

    # 临时保存加粗内容
    bold_pattern = r'\*\*(.*?)\*\*'
    bold_matches = re.findall(bold_pattern, text)
    for i, match in enumerate(bold_matches):
        text = text.replace(f'**{match}**', f'__BOLD_{i}__')

    # 移除标题符号
    text = re.sub(r'^###\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^##\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^#\s*', '', text, flags=re.MULTILINE)

    # 移除列表符号
    text = re.sub(r'^[-*]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)

    # 移除多余的 markdown 符号
    text = re.sub(r'`{3}.*?`{3}', '', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'\1', text)

    # 恢复加粗内容（小红书支持 **加粗**）
    for i, match in enumerate(bold_matches):
        text = text.replace(f'__BOLD_{i}__', f'**{match}**')

    # 清理多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def count_chinese_chars(text: str) -> int:
    """统计中文字符数（不含标点和空格）"""
    # 匹配中文字符
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)


def count_all_chars(text: str) -> int:
    """统计所有字符（含英文、数字）"""
    # 移除空白字符后统计
    return len(text.replace(' ', '').replace('\n', ''))


def parse_tags(hashtags_text: str) -> list:
    """解析标签，支持多种格式"""
    tags = []

    # 格式1: #标签1 #标签2
    if '#' in hashtags_text:
        tags = [t.strip() for t in hashtags_text.split('#') if t.strip()]
    # 格式2: 标签1 标签2（空格分隔）
    else:
        tags = [t.strip() for t in hashtags_text.split() if t.strip()]

    # 去重
    seen = set()
    unique_tags = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            unique_tags.append(tag)

    return unique_tags


def suggest_additional_tags(existing_tags: list) -> list:
    """根据现有标签建议补充标签"""
    existing_lower = [t.lower() for t in existing_tags]
    suggestions = []

    # 检查大话题覆盖
    has_big = any(tag in existing_lower for tag in POPULAR_TAGS['大话题'])
    if not has_big:
        suggestions.extend(POPULAR_TAGS['大话题'][:2])

    # 检查中话题覆盖
    has_medium = any(tag in existing_lower for tag in POPULAR_TAGS['中话题'])
    if not has_medium:
        suggestions.extend(POPULAR_TAGS['中话题'][:2])

    # 如果标签数量不足，补充小话题
    if len(existing_tags) < XHS_LIMITS['tags_optimal_min']:
        suggestions.extend(POPULAR_TAGS['小话题'][:2])

    # 过滤掉已存在的
    suggestions = [s for s in suggestions if s not in existing_lower]

    return suggestions[:3]  # 最多建议3个


def generate_cover_alternatives(title: str, cover_text: str) -> list:
    """生成备选封面文案"""
    alternatives = []

    # 提取核心关键词
    keywords = re.findall(r'[\u4e00-\u9fff]{2,6}', title + cover_text)
    keyword = keywords[0] if keywords else title[:6]

    # 方案A: 痛点型
    pain_point = f"总觉得自己{keyword}不够？"
    alternatives.append({
        'type': '痛点型',
        'text': pain_point,
        'sub': f"可能问题不在你，在{keyword}",
        'suitable_for': '引发好奇心和共鸣'
    })

    # 方案B: 数字型（如果内容中有数字）
    numbers = re.findall(r'\d+', cover_text)
    if numbers:
        num = numbers[0]
        alternatives.append({
            'type': '数字型',
            'text': f"{num}个{keyword}真相",
            'sub': "最后一个很多人不知道",
            'suitable_for': '收藏驱动'
        })

    # 方案C: 结论前置型
    conclusion = cover_text.split('。')[0][:12] if '。' in cover_text else cover_text[:12]
    alternatives.append({
        'type': '结论型',
        'text': conclusion,
        'sub': "看完这篇你就懂了",
        'suitable_for': '价值明确，适合深度内容'
    })

    return alternatives


def check_length_and_warn(cover: str, body: str, tags: list) -> dict:
    """检查长度并生成警告和建议"""
    warnings = []
    stats = {}

    # 封面字数检查
    cover_len = count_all_chars(cover)
    stats['cover'] = cover_len
    if cover_len > XHS_LIMITS['cover_max']:
        warnings.append(f"⚠️ 封面文案超长：{cover_len}字 / 限制{XHS_LIMITS['cover_max']}字")
    elif cover_len > XHS_LIMITS['cover_warning']:
        warnings.append(f"⚡ 封面文案接近上限：{cover_len}字 / 限制{XHS_LIMITS['cover_max']}字")

    # 正文字数检查
    body_len = count_chinese_chars(body)
    stats['body'] = body_len
    if body_len < XHS_LIMITS['body_min']:
        warnings.append(f"⚠️ 正文较短：{body_len}字 / 建议最少{XHS_LIMITS['body_min']}字")
    elif body_len < XHS_LIMITS['body_optimal_min']:
        warnings.append(f"💡 正文可再充实：{body_len}字 / 推荐{XHS_LIMITS['body_optimal_min']}-{XHS_LIMITS['body_optimal_max']}字")
    elif body_len > XHS_LIMITS['body_warning_max']:
        warnings.append(f"⚠️ 正文较长：{body_len}字 / 推荐控制在{XHS_LIMITS['body_optimal_max']}字以内")

    # 标签数量检查
    tag_count = len(tags)
    stats['tags'] = tag_count
    if tag_count < XHS_LIMITS['tags_min']:
        warnings.append(f"⚠️ 标签太少：{tag_count}个 / 建议最少{XHS_LIMITS['tags_min']}个")
    elif tag_count < XHS_LIMITS['tags_optimal_min']:
        warnings.append(f"💡 标签可补充：{tag_count}个 / 推荐{XHS_LIMITS['tags_optimal_min']}-{XHS_LIMITS['tags_optimal_max']}个")
    elif tag_count > XHS_LIMITS['tags_max']:
        warnings.append(f"⚠️ 标签太多：{tag_count}个 / 建议最多{XHS_LIMITS['tags_max']}个")

    return {'stats': stats, 'warnings': warnings}


def parse_slice_file(file_path: str) -> dict:
    """解析切片文件，提取 frontmatter 和内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 解析 frontmatter
    frontmatter = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            for line in fm_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"').strip("'")
            content = parts[2].strip()

    return {
        'frontmatter': frontmatter,
        'content': content
    }


def extract_sections(content: str) -> dict:
    """提取各部分内容"""
    sections = {
        'cover': '',
        'body': '',
        'hashtags': '',
        'design': ''
    }

    # 提取封面文案
    cover_match = re.search(r'## 封面文案.*?\n\n(>.*?)(?=\n\n##|\Z)', content, re.DOTALL)
    if cover_match:
        sections['cover'] = cover_match.group(1).replace('> ', '').replace('>', '').strip()

    # 提取正文
    body_match = re.search(r'## 正文.*?\n\n(.*?)(?=\n\n##|\Z)', content, re.DOTALL)
    if body_match:
        sections['body'] = body_match.group(1).strip()

    # 提取标签
    tags_match = re.search(r'## 标签.*?\n\n(.*?)(?=\n\n##|\Z)', content, re.DOTALL)
    if tags_match:
        sections['hashtags'] = tags_match.group(1).strip()

    # 提取设计指引
    design_match = re.search(r'## 设计指引.*?\n\n(.*?)(?=\n\n##|\Z)', content, re.DOTALL)
    if design_match:
        sections['design'] = design_match.group(1).strip()

    return sections


def format_for_xiaohongshu(sections: dict, title: str, content_id: str = "") -> str:
    """格式化为小红书发布格式（V2.0 增强版）"""

    # 1. 处理正文：清理 Markdown
    body = clean_markdown(sections['body'])

    # 2. 智能添加 emoji
    body = add_smart_emoji(body, emoji_density=4)

    # 3. 解析标签
    tags = parse_tags(sections['hashtags'])

    # 4. 长度检查和警告
    cover_text = sections['cover'] if sections['cover'] else title
    check_result = check_length_and_warn(cover_text, body, tags)
    stats = check_result['stats']
    warnings = check_result['warnings']

    # 5. 标签增强建议
    tag_suggestions = []
    if len(tags) < XHS_LIMITS['tags_optimal_min']:
        tag_suggestions = suggest_additional_tags(tags)

    # 6. 检测内容类型和发布时间建议
    content_type = detect_content_type(body + cover_text)
    time_advice = get_publish_time_advice(content_type)

    # 7. 生成备选封面
    cover_alternatives = generate_cover_alternatives(title, cover_text)

    # 8. 检查发布状态
    publish_status = check_publish_status(content_id) if content_id else "未知"

    # 构建输出
    output = []
    output.append("=" * 60)
    output.append("📱 小红书发布内容")
    output.append("=" * 60)
    output.append("")

    # 字数统计面板
    output.append("📊 【字数统计】")
    output.append("-" * 40)

    # 封面字数状态
    cover_status = "✅" if stats['cover'] <= XHS_LIMITS['cover_max'] else "❌"
    output.append(f"封面文案: {stats['cover']}字 / 限制{XHS_LIMITS['cover_max']}字 {cover_status}")

    # 正文字数状态
    if XHS_LIMITS['body_optimal_min'] <= stats['body'] <= XHS_LIMITS['body_optimal_max']:
        body_status = "✅"
    elif stats['body'] < XHS_LIMITS['body_min'] or stats['body'] > XHS_LIMITS['body_warning_max']:
        body_status = "❌"
    else:
        body_status = "⚡"
    output.append(f"正文内容: {stats['body']}字 / 推荐{XHS_LIMITS['body_optimal_min']}-{XHS_LIMITS['body_optimal_max']}字 {body_status}")

    # 标签数量状态
    if XHS_LIMITS['tags_optimal_min'] <= stats['tags'] <= XHS_LIMITS['tags_optimal_max']:
        tags_status = "✅"
    elif stats['tags'] < XHS_LIMITS['tags_min'] or stats['tags'] > XHS_LIMITS['tags_max']:
        tags_status = "❌"
    else:
        tags_status = "⚡"
    output.append(f"话题标签: {stats['tags']}个 / 推荐{XHS_LIMITS['tags_optimal_min']}-{XHS_LIMITS['tags_optimal_max']}个 {tags_status}")

    output.append(f"状态: {publish_status}")
    output.append(f"内容类型: {content_type}")
    output.append("")

    # 警告和建议
    if warnings:
        output.append("⚠️ 【优化建议】")
        output.append("-" * 40)
        for warning in warnings:
            output.append(f"  {warning}")
        if tag_suggestions:
            output.append(f"  💡 建议补充标签：{' '.join(['#' + t for t in tag_suggestions])}")
        output.append("")

    # 封面文案
    output.append("📝 【封面文案】（放在首图）")
    output.append("-" * 40)
    output.append(cover_text)
    output.append("")

    # 备选封面方案
    output.append("💡 【备选封面方案】")
    output.append("-" * 40)
    for i, alt in enumerate(cover_alternatives, 1):
        output.append(f"方案{i}（{alt['type']}）：{alt['text']}")
        output.append(f"  副标题：{alt['sub']}")
        output.append(f"  适合：{alt['suitable_for']}")
        output.append("")

    # 正文
    output.append("📝 【正文文案】（复制到发布框）")
    output.append("-" * 40)
    output.append(body)
    output.append("")

    # 标签
    output.append("🏷️ 【话题标签】（复制到文末）")
    output.append("-" * 40)
    output.append(' '.join([f"#{t}" for t in tags]))
    if tag_suggestions:
        output.append("")
        output.append("💡 可补充标签：" + ' '.join([f"#{t}" for t in tag_suggestions]))
    output.append("")

    # 发布时间建议
    output.append("⏰ 【发布建议】")
    output.append("-" * 40)
    output.append(f"最佳发布时间：{time_advice['primary']}（{time_advice['reason']}）")
    output.append(f"备选时间：{'、'.join(time_advice['alternatives'])}")
    output.append("")

    # 设计指引
    if sections['design']:
        output.append("🎨 【设计指引】")
        output.append("-" * 40)
        output.append(sections['design'])
        output.append("")

    # 检查清单
    output.append("=" * 60)
    output.append("✅ 发布前检查清单：")
    output.append(f"  □ 图片已准备（6-9张，3:4竖图）")
    output.append(f"  □ 首图包含封面文案（{stats['cover']}字，{cover_status}）")
    output.append(f"  □ 正文已复制（{stats['body']}字，{body_status}）")
    output.append(f"  □ 标签已添加（{stats['tags']}个，{tags_status}）")
    output.append(f"  □ 发布时间已设定（建议：{time_advice['primary']}）")
    if content_id:
        output.append(f"  □ 记录发布（运行：python scripts/xiaohongshu-export.py --record {content_id}）")
    output.append("=" * 60)

    return '\n'.join(output)


def export_single_file(file_path: str, output_dir: str = None, content_id: str = "") -> str:
    """导出单个切片文件为小红书格式"""
    data = parse_slice_file(file_path)
    sections = extract_sections(data['content'])
    title = data['frontmatter'].get('title', '未命名')

    # 从文件名或 frontmatter 获取 content_id
    if not content_id:
        content_id = data['frontmatter'].get('id', '')

    formatted = format_for_xiaohongshu(sections, title, content_id)

    # 保存到文件
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        base_name = Path(file_path).stem
        export_file = output_path / f"{base_name}-publish.txt"

        with open(export_file, 'w', encoding='utf-8') as f:
            f.write(formatted)

        return str(export_file)

    return formatted


def export_batch(slice_dir: str, output_dir: str = None, content_id: str = "") -> list:
    """批量导出目录下所有小红书切片"""
    slice_path = Path(slice_dir)
    if not slice_path.exists():
        raise FileNotFoundError(f"目录不存在: {slice_dir}")

    # 查找所有小红书切片文件
    xiaohongshu_files = list(slice_path.glob("*xiaohongshu*.md"))

    if not xiaohongshu_files:
        print(f"⚠️ 未在 {slice_dir} 中找到小红书切片文件")
        return []

    # 默认输出到同级目录的 publish-ready 文件夹
    if not output_dir:
        output_dir = slice_path / "publish-ready"

    exported = []
    for file in xiaohongshu_files:
        try:
            export_file = export_single_file(str(file), str(output_dir), content_id)
            exported.append({
                'source': str(file),
                'exported': export_file
            })
            print(f"✅ 已导出: {file.name}")
        except Exception as e:
            print(f"❌ 导出失败: {file.name} - {e}")

    return exported


def generate_publish_package(content_id: str) -> dict:
    """生成完整的发布包（包含所有平台）"""
    slices_dir = Path(f"content/slices/{content_id}")

    if not slices_dir.exists():
        return {"error": f"内容ID不存在: {content_id}"}

    # 导出小红书内容
    exported = export_batch(str(slices_dir), content_id=content_id)

    # 生成发布清单
    package = {
        "content_id": content_id,
        "generated_at": datetime.now().isoformat(),
        "xiaohongshu_exports": exported,
        "publish_ready_dir": str(slices_dir / "publish-ready")
    }

    return package


if __name__ == "__main__":
    import argparse
    import io

    # 修复 Windows 控制台编码问题
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(description="小红书内容导出助手 V2.0")
    parser.add_argument("input", nargs='?', help="输入文件或目录路径")
    parser.add_argument("--batch", "-b", action="store_true", help="批量模式（输入为目录）")
    parser.add_argument("--output", "-o", help="输出目录")
    parser.add_argument("--content-id", "-c", help="内容ID（生成完整发布包）")
    parser.add_argument("--record", "-r", help="记录发布历史（内容ID）")

    args = parser.parse_args()

    if args.record:
        # 记录发布
        record_publish(args.record)
        print(f"✅ 已记录发布: {args.record}")
    elif args.content_id and not args.input:
        # 生成完整发布包
        package = generate_publish_package(args.content_id)
        print(json.dumps(package, ensure_ascii=False, indent=2))
    elif args.batch:
        # 批量导出
        content_id = args.content_id or ""
        exported = export_batch(args.input, args.output, content_id)
        print(f"\n📦 共导出 {len(exported)} 个文件")
        print(f"📁 输出目录: {args.output or Path(args.input) / 'publish-ready'}")
    elif args.input:
        # 单文件导出并打印
        content_id = args.content_id or ""
        result = export_single_file(args.input, args.output, content_id)
        if args.output:
            print(f"✅ 已导出到: {result}")
        else:
            print(result)
    else:
        parser.print_help()
