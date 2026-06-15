#!/usr/bin/env python3
"""
公众号 HTML 一键导出助手 (V1.0)

将 s-4.2.2-adapt 产出的 wechat slice Markdown 转换为微信编辑器可直接粘贴的
内联样式 HTML。排版渲染由外部引擎 xiaohu-wechat-format 完成。

依赖: xiaohu-wechat-format 需独立安装到 ~/.claude/skills/xiaohu-wechat-format/
      (git clone https://github.com/xiaohuailabs/xiaohu-wechat-format.git)
      引擎自身需要: pip3 install markdown
"""

from __future__ import annotations

import os
import re
import sys
import io
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Optional

from gatekeeper import validate_publish_package

# ── 配置常量 ──────────────────────────────────────────────

# xiaohu 引擎默认安装路径
DEFAULT_ENGINE_HOME = Path.home() / ".claude" / "skills" / "xiaohu-wechat-format"

# 默认主题: newspaper（干净专业，匹配 SOUL 品牌调性）
# 其他可选: chinese, ink, github, sspai, magazine, wechat-native 等 30 种
DEFAULT_THEME = "newspaper"

# xiaohu format.py 输出根目录（引擎内部行为）
XIAOHU_OUTPUT_ROOT = Path("/tmp/wechat-format")

# SOUL 品牌主题色（供设计指引注入）
SOUL_BRAND_PRIMARY = "#1a1a2e"
SOUL_BRAND_ACCENT = "#e94560"


# ── 引擎定位 ──────────────────────────────────────────────

def find_engine_home() -> Path:
    """定位 xiaohu-wechat-format 引擎路径。"""
    env = os.environ.get("XIAOHU_FORMAT_HOME", "")
    if env:
        candidate = Path(env).expanduser().resolve()
        if candidate.is_dir():
            return candidate
        print(f"⚠️  XIAOHU_FORMAT_HOME={env} 指向的目录不存在，回退到默认路径")

    candidate = DEFAULT_ENGINE_HOME.expanduser().resolve()
    if candidate.is_dir():
        return candidate

    raise FileNotFoundError(
        f"未找到 xiaohu-wechat-format 排版引擎。\n"
        f"请先安装:\n"
        f"  git clone https://github.com/xiaohuailabs/xiaohu-wechat-format.git {DEFAULT_ENGINE_HOME}\n"
        f"  cp {DEFAULT_ENGINE_HOME}/config.example.json {DEFAULT_ENGINE_HOME}/config.json\n"
        f"  pip3 install markdown\n"
        f"或设置环境变量 XIAOHU_FORMAT_HOME 指向引擎目录。"
    )


def find_format_py(engine_home: Path) -> Path:
    """返回 format.py 的绝对路径。"""
    candidate = engine_home / "scripts" / "format.py"
    if not candidate.is_file():
        raise FileNotFoundError(
            f"引擎目录下未找到 scripts/format.py: {candidate}\n"
            f"请确认 xiaohu-wechat-format 仓库已完整克隆。"
        )
    return candidate


# ── 切片解析（复用 publish_package 契约） ────────────────

def parse_slice_file(file_path: str) -> dict:
    """解析切片文件，提取 frontmatter 和正文。"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    frontmatter = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            for line in fm_text.split("\n"):
                line = line.strip()
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip().strip('"').strip("'")
            body = parts[2].strip()

    return {"frontmatter": frontmatter, "content": body}


def extract_markdown_section(content: str, heading: str) -> str:
    """按二级标题提取 Markdown 分节内容。"""
    pattern = rf"^##\s*{re.escape(heading)}.*?\n(.*?)(?=^##\s+|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_sections(content: str) -> dict:
    """从 slice Markdown 提取 publish_package 分节。"""
    return {
        "cover": extract_markdown_section(content, "封面文案"),
        "body": extract_markdown_section(content, "正文"),
        "hashtags": extract_markdown_section(content, "标签"),
        "design": extract_markdown_section(content, "设计指引"),
    }


def normalize_platform(value: str) -> str:
    """标准化平台别名。"""
    value = (value or "").strip().lower()
    aliases = {"公众号": "wechat", "微信": "wechat", "wechat": "wechat"}
    return aliases.get(value, value)


def is_wechat_slice(file_path: Path) -> bool:
    """判断文件是否为公众号切片。"""
    name = file_path.name.lower()
    if "wechat" in name or "公众号" in name or "weixin" in name:
        return True
    try:
        data = parse_slice_file(str(file_path))
    except Exception:
        return False
    return normalize_platform(data["frontmatter"].get("platform", "")) == "wechat"


def build_publish_package(sections: dict, frontmatter: dict, title: str) -> dict:
    """构造 publish_package_gate 使用的轻量发布包。"""
    return {
        "slice_id": frontmatter.get("id", ""),
        "parent_id": frontmatter.get("parent_id", ""),
        "platform": normalize_platform(frontmatter.get("platform", "wechat")),
        "type": frontmatter.get("type", ""),
        "title": title,
        "cover": sections.get("cover", ""),
        "body": sections.get("body", ""),
        "hashtags": _parse_tags(sections.get("hashtags", "")),
        "design": sections.get("design", ""),
    }


def _parse_tags(hashtags_text: str) -> list:
    """解析标签文本。"""
    tags = []
    if "#" in hashtags_text:
        tags = [t.strip() for t in hashtags_text.split("#") if t.strip()]
    else:
        tags = [t.strip() for t in hashtags_text.split() if t.strip()]
    return tags


# ── 前置 Markdown 生成（为 xiaohu format.py 准备输入） ──

def build_format_input(sections: dict, frontmatter: dict, source_path: str) -> str:
    """
    将 slice Markdown 转换为 xiaohu format.py 可接受的纯 Markdown。

    规则:
    - 标题取自 frontmatter.title 作为 H1
    - ## 正文 作为主体
    - ## 设计指引 中关于排版的具体指令附在末尾（HTML 注释 + 设计提示）
    - 不得包含 YAML frontmatter
    - 不得包含 :::dialogue / :::callout 等私有容器语法
    """
    title = frontmatter.get("title", "未命名").strip()
    body = sections.get("body", "").strip()
    design = sections.get("design", "").strip()
    cover = sections.get("cover", "").strip()

    # 检查私有容器语法（s-4.2.2 规定不应出现，但兜底检测）
    _check_private_syntax(body, source_path)

    lines = []

    # 标题
    lines.append(f"# {title}")
    lines.append("")

    # 来源标注（HTML 注释，微信编辑器不可见）
    source_id = frontmatter.get("id", Path(source_path).stem)
    lines.append(f"<!-- SOUL 内容工作流 · {source_id} · {datetime.now().strftime('%Y-%m-%d')} -->")
    lines.append("")

    # 正文（主体）
    lines.append(body)
    lines.append("")

    # SOUL 品牌声明（HTML 注释）
    lines.append("<!--")
    lines.append("本文由 SOUL 内容创作工作流生成")
    lines.append("品牌: 超级个体成长教练 | AI 是工具，哲学是地基，你才是杠杆的支点")
    lines.append("-->")
    lines.append("")

    return "\n".join(lines)


def _check_private_syntax(text: str, source_path: str) -> None:
    """
    检测 slice 正文中是否包含 xiaohu 私有容器语法。
    这些语法在微信编辑器中原样显示，发布前必须剔除。
    """
    private_patterns = [
        (r"^:::\s*(dialogue|gallery|byline|stat|longimage|callout|note|tip|warning|important)",
         "私有容器语法"),
    ]
    for pattern, name in private_patterns:
        matches = re.findall(pattern, text, re.MULTILINE)
        if matches:
            print(
                f"⚠️  检测到 xiaohu 私有 {name} ({', '.join(matches)})，"
                f"将在微信编辑器中原样显示为裸文字。\n"
                f"   来源: {source_path}\n"
                f"   建议: 回到 s-4.2.2-adapt 用引用块/小标题替代，或手工删除。"
            )


# ── 排版引擎调用 ──────────────────────────────────────────

def run_xiaohu_format(
    format_py: Path,
    input_md: Path,
    theme: str,
    timeout: int = 60,
) -> Path:
    """
    调用 xiaohu format.py 将 Markdown 转为微信兼容 HTML。

    返回: 输出 HTML 文件的 Path
    """
    # 记录调用前的 /tmp/wechat-format/ 状态，用于检测新输出
    before = _list_xiaohu_output_dirs()

    cmd = [
        sys.executable, str(format_py),
        "--input", str(input_md),
        "--theme", theme,
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=format_py.parent.parent,  # 引擎根目录
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(
            f"format.py 执行超时 ({timeout}s)。\n"
            f"命令: {' '.join(cmd)}"
        )
    except FileNotFoundError:
        raise RuntimeError(
            f"无法调用 Python。请确认 python3 在 PATH 中。"
        )

    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        raise RuntimeError(
            f"format.py 执行失败 (退出码 {result.returncode})。\n"
            f"命令: {' '.join(cmd)}\n"
            f"stderr: {stderr}\n"
            f"stdout: {stdout}"
        )

    # 检测新生成的输出目录
    after = _list_xiaohu_output_dirs()
    new_dirs = [d for d in after if d not in before]

    if not new_dirs:
        # 可能 format.py 输出到了其他地方，尝试从 stdout 解析
        stdout = result.stdout.strip()
        if stdout:
            for line in stdout.splitlines():
                candidate = Path(line.strip())
                if candidate.is_dir():
                    new_dirs.append(candidate)

    if not new_dirs:
        raise RuntimeError(
            f"format.py 执行成功但未检测到输出目录。\n"
            f"stdout: {result.stdout}\n"
            f"{XIAOHU_OUTPUT_ROOT} 下未发现新目录。"
        )

    # 取最新的输出目录
    output_dir = new_dirs[-1]

    # 查找其中的 HTML 文件
    html_files = list(output_dir.glob("*.html"))
    if not html_files:
        raise RuntimeError(
            f"输出目录 {output_dir} 中未找到 HTML 文件。\n"
            f"目录内容: {list(output_dir.iterdir())}"
        )

    return html_files[0]


def _list_xiaohu_output_dirs() -> list[Path]:
    """列出 xiaohu format.py 输出根下的所有目录。"""
    if not XIAOHU_OUTPUT_ROOT.is_dir():
        return []
    return sorted(
        [p for p in XIAOHU_OUTPUT_ROOT.iterdir() if p.is_dir()],
        key=lambda p: p.stat().st_mtime,
    )


# ── 导出主流程 ────────────────────────────────────────────

def export_single_file(
    file_path: str,
    output_dir: Optional[str] = None,
    theme: str = DEFAULT_THEME,
    parent_id: str = "",
) -> str:
    """
    导出单个 wechat slice 为微信兼容 HTML。

    参数:
        file_path: slice Markdown 文件路径
        output_dir: 输出目录（默认 content/slices/{parent-id}/publish-ready/）
        theme: xiaohu 主题 ID
        parent_id: 母稿 ID（用于构建默认输出路径）

    返回: 输出 HTML 文件的绝对路径
    """
    source_path = Path(file_path).resolve()
    if not source_path.is_file():
        raise FileNotFoundError(f"slice 文件不存在: {file_path}")

    # 1. 解析
    data = parse_slice_file(str(source_path))
    data["frontmatter"]["source_path"] = str(source_path)
    sections = extract_sections(data["content"])
    title = data["frontmatter"].get("title", "未命名")

    # 2. 校验
    pkg = build_publish_package(sections, data["frontmatter"], title)
    result = validate_publish_package(pkg)
    if result["status"] == "blocked":
        reasons = "; ".join(
            b.get("summary", "未知问题") for b in result["blockers"]
        )
        raise ValueError(f"publish_package_gate blocked: {reasons}")

    # 3. 定位引擎
    engine_home = find_engine_home()
    format_py = find_format_py(engine_home)

    # 4. 生成前置 Markdown
    fmt_input = build_format_input(sections, data["frontmatter"], str(source_path))

    # 5. 写入临时 Markdown 文件（xiaohu format.py 需要文件输入）
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".md",
        prefix="soul-wechat-",
        encoding="utf-8",
        delete=False,
    ) as tmp:
        tmp.write(fmt_input)
        tmp_md_path = Path(tmp.name)

    try:
        # 6. 调用 xiaohu 排版引擎
        html_path = run_xiaohu_format(format_py, tmp_md_path, theme)

        # 7. 确定输出目录
        if output_dir:
            out_dir = Path(output_dir)
        else:
            pid = parent_id or data["frontmatter"].get("parent_id", "") or source_path.parent.name
            out_dir = source_path.parent / "publish-ready"
        out_dir.mkdir(parents=True, exist_ok=True)

        # 8. 复制 HTML 到正式输出路径
        base_name = source_path.stem
        dest = out_dir / f"{base_name}.html"
        shutil.copy2(html_path, dest)

        print(f"✅ 微信 HTML 已导出: {dest}")
        print(f"   主题: {theme}")
        print(f"   字数: {len(sections['body'])} 字符")
        print(f"   可直接复制 HTML 源码粘贴到微信公众号编辑器。")

        return str(dest)

    finally:
        # 清理临时 Markdown
        tmp_md_path.unlink(missing_ok=True)


def export_batch(
    slice_dir: str,
    output_dir: Optional[str] = None,
    theme: str = DEFAULT_THEME,
    parent_id: str = "",
) -> list:
    """批量导出目录下所有 wechat 切片。"""
    slice_path = Path(slice_dir)
    if not slice_path.exists():
        raise FileNotFoundError(f"目录不存在: {slice_dir}")

    wechat_files = [p for p in slice_path.glob("*.md") if is_wechat_slice(p)]

    if not wechat_files:
        print(f"⚠️  未在 {slice_dir} 中找到公众号切片文件")
        return []

    if not output_dir:
        output_dir = str(slice_path / "publish-ready")

    exported = []
    failures = []
    for file in wechat_files:
        try:
            out = export_single_file(str(file), output_dir, theme, parent_id)
            exported.append({"source": str(file), "exported": out})
            print(f"✅ 已导出: {file.name}")
        except Exception as e:
            failures.append({"source": str(file), "error": str(e)})
            print(f"❌ 导出失败: {file.name} — {e}")

    if failures:
        raise RuntimeError(
            f"{len(failures)} 个 wechat 切片导出失败:\n" +
            "\n".join(f"  - {f['source']}: {f['error']}" for f in failures)
        )

    return exported


# ── CLI ────────────────────────────────────────────────────

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="公众号 HTML 一键导出 · 调 xiaohu-wechat-format 外部排版引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  # 单文件导出
  python3 scripts/wechat-html-export.py content/slices/my-article/slice-001-wechat-article.md

  # 批量导出 + 指定主题
  python3 scripts/wechat-html-export.py content/slices/my-article/ --batch --theme chinese

  # 指定输出目录
  python3 scripts/wechat-html-export.py slice-001-wechat-article.md -o ./publish/

引擎安装:
  git clone https://github.com/xiaohuailabs/xiaohu-wechat-format.git ~/.claude/skills/xiaohu-wechat-format/
  cp ~/.claude/skills/xiaohu-wechat-format/config.example.json ~/.claude/skills/xiaohu-wechat-format/config.json
  pip3 install markdown

可选主题(30种): newspaper, chinese, ink, github, sspai, magazine, wechat-native,
  terracotta, bytedance, bauhaus, midnight, mint-fresh, sunset-amber, 等
默认主题: {DEFAULT_THEME}
        """,
    )
    parser.add_argument(
        "input", nargs="?", help="输入文件或目录路径"
    )
    parser.add_argument(
        "--batch", "-b", action="store_true",
        help="批量模式（输入为 slices 目录）"
    )
    parser.add_argument(
        "--output", "-o", help="输出目录"
    )
    parser.add_argument(
        "--theme", "-t", default=DEFAULT_THEME,
        help=f"排版主题 ID（默认: {DEFAULT_THEME}）"
    )
    parser.add_argument(
        "--parent-id", "-p", default="",
        help="母稿 ID（用于构建默认输出路径）"
    )
    parser.add_argument(
        "--engine-path", default="",
        help=f"xiaohu 引擎路径（默认: {DEFAULT_ENGINE_HOME}）"
    )
    parser.add_argument(
        "--list-themes", action="store_true",
        help="列出 xiaohu 引擎中的可用主题"
    )

    args = parser.parse_args()

    # 引擎路径覆盖
    if args.engine_path:
        os.environ["XIAOHU_FORMAT_HOME"] = args.engine_path

    # 列出主题
    if args.list_themes:
        try:
            engine_home = find_engine_home()
        except FileNotFoundError as e:
            print(f"❌ {e}", file=sys.stderr)
            sys.exit(1)
        themes_dir = engine_home / "themes"
        if themes_dir.is_dir():
            theme_files = sorted(themes_dir.glob("*.json"))
            print(f"可用主题 ({len(theme_files)}):")
            for tf in theme_files:
                print(f"  {tf.stem}")
        else:
            print("未找到 themes/ 目录")
        return

    if not args.input:
        parser.print_help()
        return

    try:
        if args.batch:
            exported = export_batch(
                args.input, args.output, args.theme, args.parent_id
            )
            if exported:
                print(f"\n📦 共导出 {len(exported)} 个 HTML 文件")
                print(f"📁 输出目录: {args.output or Path(args.input) / 'publish-ready'}")
        else:
            result = export_single_file(
                args.input, args.output, args.theme, args.parent_id
            )
            if not args.output:
                print(f"\n📁 输出文件: {result}")
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
