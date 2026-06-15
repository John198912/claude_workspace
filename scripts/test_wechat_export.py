#!/usr/bin/env python3
"""Lightweight regression tests for scripts/wechat-html-export.py."""
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parent / "wechat-html-export.py"
spec = importlib.util.spec_from_file_location("wechat_html_export", SCRIPT)
assert spec and spec.loader
wx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wx)


def write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def valid_wechat_slice(title: str = "测试标题") -> str:
    return f"""---
id: slice-001
platform: wechat
type: article
title: {title}
parent_id: test-parent
---

## 封面文案

> 这是封面文案

## 正文

这是一段公众号正文。它包含多个段落和内容。

### 小标题一

这里是第一段正文内容，用于测试 HTML 导出功能。

### 小标题二

1. 有序列表项一
2. 有序列表项二
3. 有序列表项三

> 这是一段引用文本。

这是结尾段落。

## 标签

#AI #个人成长 #超级个体

## 设计指引

## 排版建议
- 手机优先，段落控制在5行以内
- 加粗重点词，每段不超过2处
"""


def test_engine_not_found_raises_clear_error() -> None:
    """引擎未安装时应抛出包含安装指引的清晰错误。"""
    # 同时覆盖环境变量和模块级默认路径，避免 fallback 到真实安装
    fake_home = "/tmp/nonexistent-xiaohu-engine-xyz"
    old_default = wx.DEFAULT_ENGINE_HOME
    wx.DEFAULT_ENGINE_HOME = Path(fake_home)
    try:
        with patch.dict("os.environ", {"XIAOHU_FORMAT_HOME": fake_home}):
            try:
                wx.find_engine_home()
            except FileNotFoundError as exc:
                msg = str(exc)
                assert "未找到" in msg or "git clone" in msg, f"错误信息应包含安装指引: {msg}"
            else:
                raise AssertionError("引擎缺失应抛出 FileNotFoundError")
    finally:
        wx.DEFAULT_ENGINE_HOME = old_default


def test_parse_slice_extracts_frontmatter_and_body() -> None:
    """切片解析应正确提取 frontmatter 和正文。"""
    md = valid_wechat_slice()
    data = wx.parse_slice_file.__wrapped__ if hasattr(wx.parse_slice_file, '__wrapped__') else wx.parse_slice_file
    # The function is imported as-is, not wrapped
    result = wx.parse_slice_file.__func__ if hasattr(wx.parse_slice_file, '__func__') else wx.parse_slice_file
    # Actually, it was imported via importlib, so it's a regular function
    result = wx.parse_slice_file.__call__  # no, this is the method wrapper
    # Let me just call it directly since it IS a regular function from importlib
    with tempfile.TemporaryDirectory() as tmp:
        path = write(Path(tmp) / "test.md", md)
        data = wx.parse_slice_file(str(path))
        assert data["frontmatter"]["id"] == "slice-001"
        assert data["frontmatter"]["platform"] == "wechat"
        assert "这是一段公众号正文" in data["content"]


def test_blocks_missing_body_section() -> None:
    """缺 ## 正文 的 slice 应被 gatekeeper 阻断。"""
    with tempfile.TemporaryDirectory() as tmp:
        path = write(Path(tmp) / "slice-001-wechat-article.md", """---
id: slice-001
platform: wechat
title: 测试标题
---

## 标签

#AI
""")
        try:
            wx.export_single_file(str(path))
        except ValueError as exc:
            assert "publish_package_gate blocked" in str(exc), f"应被阻断: {exc}"
        else:
            raise AssertionError("缺 ## 正文 应被 gatekeeper 阻断")


def test_blocks_empty_body() -> None:
    """空正文 slice 应被 gatekeeper 阻断。"""
    with tempfile.TemporaryDirectory() as tmp:
        path = write(Path(tmp) / "slice-001-wechat-article.md", """---
id: slice-001
platform: wechat
title: 测试标题
---

## 正文


## 标签

#AI
""")
        try:
            wx.export_single_file(str(path))
        except ValueError as exc:
            assert "正文" in str(exc) or "body" in str(exc).lower(), f"应提示正文为空: {exc}"
        else:
            raise AssertionError("空正文应被 gatekeeper 阻断")


def test_is_wechat_slice_by_platform() -> None:
    """按 frontmatter.platform=wechat 判定为公众号切片。"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root / "slice-001-wechat-article.md", valid_wechat_slice())
        assert wx.is_wechat_slice(root / "slice-001-wechat-article.md") is True


def test_is_wechat_slice_by_filename() -> None:
    """按文件名含 wechat 判定为公众号切片。"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root / "任意-wechat-图文.md", """---
id: s2
title: t
---

## 正文

你好
""")
        assert wx.is_wechat_slice(root / "任意-wechat-图文.md") is True


def test_build_format_input_no_private_syntax() -> None:
    """生成的 format.py 输入不应包含私有容器语法。"""
    sections = {"body": "## 测试\n\n正文内容。", "design": "", "cover": "", "hashtags": ""}
    frontmatter = {"id": "test-001", "title": "测试标题"}
    result = wx.build_format_input(sections, frontmatter, "/tmp/test.md")
    assert ":::" not in result, "不应包含 ::: 私有容器语法"
    assert "---" not in result, "不应包含 YAML frontmatter 定界符"
    assert "# 测试标题" in result, "应包含 H1 标题"
    assert "正文内容" in result, "应包含正文"


def test_private_syntax_warning() -> None:
    """检测到私有容器语法时应打印警告（不抛异常，只 warn）。"""
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        wx._check_private_syntax(":::dialogue\n你好\n:::\n", "/tmp/test.md")
        output = sys.stdout.getvalue()
        assert "dialogue" in output or "私有容器" in output, f"应打印警告: {output}"
    finally:
        sys.stdout = old_stdout


def test_normalize_platform_aliases() -> None:
    """平台别名应正确标准化。"""
    assert wx.normalize_platform("wechat") == "wechat"
    assert wx.normalize_platform("微信") == "wechat"
    assert wx.normalize_platform("公众号") == "wechat"
    assert wx.normalize_platform("xiaohongshu") == "xiaohongshu"


def main() -> None:
    tests = [
        ("test_engine_not_found_raises_clear_error", test_engine_not_found_raises_clear_error),
        ("test_parse_slice_extracts_frontmatter_and_body", test_parse_slice_extracts_frontmatter_and_body),
        ("test_blocks_missing_body_section", test_blocks_missing_body_section),
        ("test_blocks_empty_body", test_blocks_empty_body),
        ("test_is_wechat_slice_by_platform", test_is_wechat_slice_by_platform),
        ("test_is_wechat_slice_by_filename", test_is_wechat_slice_by_filename),
        ("test_build_format_input_no_private_syntax", test_build_format_input_no_private_syntax),
        ("test_private_syntax_warning", test_private_syntax_warning),
        ("test_normalize_platform_aliases", test_normalize_platform_aliases),
    ]
    failed = 0
    for name, test in tests:
        try:
            test()
            print(f"PASS {name}")
        except Exception as e:
            print(f"FAIL {name}: {e}")
            failed += 1
    if failed:
        print(f"\n{failed}/{len(tests)} tests FAILED")
        exit(1)
    print(f"\n{len(tests)}/{len(tests)} tests PASSED")


if __name__ == "__main__":
    main()
