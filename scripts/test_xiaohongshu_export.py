#!/usr/bin/env python3
"""Lightweight regression tests for scripts/xiaohongshu-export.py."""
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "xiaohongshu-export.py"
spec = importlib.util.spec_from_file_location("xiaohongshu_export", SCRIPT)
assert spec and spec.loader
xhs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(xhs)


def write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def valid_slice(title: str = "标题") -> str:
    return f"""---
id: slice-001
platform: xhs
type: graphic
title: {title}
---

## 封面文案

> 封面

## 正文

这是一段可导出的正文。它不需要很长，但必须能被导出脚本准确读取。

## 标签

#AI #个人成长 #内容创作 #写作 #小红书 #认知 #效率 #学习 #转型 #方法
"""


def test_single_export_blocks_missing_body_section() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = write(Path(tmp) / "slice-001-xhs-note.md", """---
id: slice-001
platform: xhs
title: 标题
---

## 标签

#AI
""")
        try:
            xhs.export_single_file(str(path))
        except ValueError as exc:
            assert "publish_package_gate blocked" in str(exc)
        else:
            raise AssertionError("missing ## 正文 should block")


def test_single_export_blocks_empty_body() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = write(Path(tmp) / "slice-001-xiaohongshu-note.md", """---
id: slice-001
platform: xiaohongshu
title: 标题
---

## 正文


## 标签

#AI
""")
        try:
            xhs.export_single_file(str(path))
        except ValueError as exc:
            assert "正文(body)为空" in str(exc)
        else:
            raise AssertionError("empty body should block")


def test_batch_matches_xhs_filename() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root / "slice-001-xhs-note.md", valid_slice())
        exported = xhs.export_batch(str(root), str(root / "publish-ready"))
        assert len(exported) == 1
        assert Path(exported[0]["exported"]).exists()


def test_batch_matches_xiaohongshu_filename() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root / "slice-001-xiaohongshu-note.md", valid_slice())
        exported = xhs.export_batch(str(root), str(root / "publish-ready"))
        assert len(exported) == 1
        assert Path(exported[0]["exported"]).exists()


def main() -> None:
    tests = [
        test_single_export_blocks_missing_body_section,
        test_single_export_blocks_empty_body,
        test_batch_matches_xhs_filename,
        test_batch_matches_xiaohongshu_filename,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")


if __name__ == "__main__":
    main()
