#!/usr/bin/env python3
"""check_consistency.py · 文档/目录自洽 linter (V2.1)

workflow_consistency_gate 的可执行内核。检查：
  1. CLAUDE.md 工作流命令表里的每个命令都有 .claude/commands/{name}.md
  2. 文档声明「必须存在」的关键路径确实存在
  3. 核心文档不再残留已知幽灵引用（不存在的目录/文档/备份）
  4. SKILL-INDEX 如实披露 6 个扩展 Skill（花名册诚实）
  5. SOUL 品牌宪法与活跃工作流不发生旧口径漂移

退出码：0=PASS，1=FAIL。也可被 CI / pre-commit 直接调用。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CORE_DOCS = [
    "CLAUDE.md", "AGENTS.md",
    "docs/SKILL-INDEX.md", "docs/USER-GUIDE-V2.md", "docs/DIRECTORY-MAP.md",
]

# 文档现在承诺存在的静态产物
MUST_EXIST = [
    "docs/SOUL-CORE-INSIGHTS.md",
    "data/brand/brand-canon.yaml",
    "data/style-profiles/personal.json",
    "data/style-guides/README.md",
    "docs/QUALITY-GATES.md",
    "data/platform-rules.md",
    "data/schemas/quality_gate_report.schema.json",
    "data/schemas/feedback_raw_event.schema.json",
    "data/schemas/publish_package.schema.json",
    "scripts/gatekeeper.py",
]

# 历史幽灵引用：核心文档中若仍出现且目标不存在，即判 FAIL
PHANTOM_REFS = [
    "MIGRATION-V2.md",
    "P0-FINAL-DELIVERY.md",
    ".v1.1.backup",
    "skills_v1.1_backup",
    "skills/_archived",
    "skills/external/skills",
]

# 应被如实披露的扩展 Skill
EXTENSION_SKILLS = [
    "a-1.4.1-philosopher",
    "s-1.4-action-diagnostics",
    "s-2.0-business-validate",
    "s-2.3-pacing-strategy",
    "s-3.0-content-diagnostics",
    "s-3.4.2-ai-check",
]

# 活跃入口与工作流中不得继续使用的旧品牌口径。
# SOUL 宪法与 brand-canon 可在“retired/history”语境中提到旧口径，因此不列入扫描。
BRAND_ACTIVE_DOCS = [
    "CLAUDE.md",
    "AGENTS.md",
    "docs/USER-GUIDE-V2.md",
    ".claude/commands/create.md",
    ".claude/commands/quick-create.md",
    ".claude/commands/full-pipeline.md",
    ".claude/commands/topic-mine.md",
    ".claude/commands/validate.md",
    ".claude/commands/distribute.md",
    "skills/m2-topic/s-2.1-topic-mine.md",
    "skills/m2-topic/s-2.2-topic-validate.md",
    "skills/m3-creation/s-3.1.1-content-system.md",
    "skills/m3-creation/s-3.1.2-content-positioning.md",
    "skills/m3-creation/s-3.2.1-research.md",
    "skills/m3-creation/a-3.2.2-outline.md",
    "skills/m3-creation/a-3.2.3-draft.md",
    "skills/m3-creation/a-3.2.4-iterate.md",
    "skills/m3-creation/s-3.2.5-seo.md",
    "skills/m3-creation/s-3.3-style-engine.md",
    "skills/m4-distribution/s-4.2.2-adapt.md",
    "skills/m4-distribution/s-4.1-slice-engine.md",
    "skills/m4-distribution/s-4.3-engagement.md",
    "skills/m5-feedback/s-5.2-review-engine.md",
    "skills/m5-feedback/s-5.3-optimize.md",
]

RETIRED_BRAND_PATTERNS = [
    "AI能说一切，但不知道说什么。你知道。",
    "定位框架：有限性三角",
    "帮助个体利用AI技术打造超级个体/一人公司",
    "受众A：转型者 | **受众B**：学生/新手 | **受众C**：知识工作者",
    'target_audience: ["A"',
    'audience: ["A", "B", "C"]',
    "受众A",
    "受众B",
    "受众C",
]

BRAND_CONSUMER_DOCS = [
    ".claude/commands/create.md",
    ".claude/commands/quick-create.md",
    ".claude/commands/full-pipeline.md",
    ".claude/commands/topic-mine.md",
    ".claude/commands/validate.md",
    ".claude/commands/distribute.md",
    "skills/m2-topic/s-2.1-topic-mine.md",
    "skills/m2-topic/s-2.2-topic-validate.md",
    "skills/m3-creation/s-3.1.1-content-system.md",
    "skills/m3-creation/s-3.1.2-content-positioning.md",
    "skills/m3-creation/s-3.2.1-research.md",
    "skills/m3-creation/a-3.2.2-outline.md",
    "skills/m3-creation/a-3.2.3-draft.md",
    "skills/m3-creation/a-3.2.4-iterate.md",
    "skills/m3-creation/s-3.2.5-seo.md",
    "skills/m3-creation/s-3.3-style-engine.md",
    "skills/m4-distribution/s-4.2.2-adapt.md",
    "skills/m4-distribution/s-4.1-slice-engine.md",
    "skills/m4-distribution/s-4.3-engagement.md",
    "skills/m5-feedback/s-5.2-review-engine.md",
    "skills/m5-feedback/s-5.3-optimize.md",
]


def read(path: str) -> str:
    p = ROOT / path
    return p.read_text(encoding="utf-8") if p.exists() else ""


def check_commands(fails: list[str]) -> None:
    claude = read("CLAUDE.md")
    # 工作流命令表行形如:  | `/learn <input>` | ... |
    cmds = sorted(set(re.findall(r"\|\s*`/([a-z][a-z0-9-]*)", claude)))
    cmd_dir = ROOT / ".claude" / "commands"
    if not cmd_dir.is_dir():
        fails.append(f"[commands] 目录不存在: .claude/commands/ （CLAUDE.md 声明了 {len(cmds)} 个命令）")
        return
    for c in cmds:
        if not (cmd_dir / f"{c}.md").exists():
            fails.append(f"[commands] 命令 /{c} 在 CLAUDE.md 声明，但缺少 .claude/commands/{c}.md")


def check_must_exist(fails: list[str]) -> None:
    for rel in MUST_EXIST:
        if not (ROOT / rel).exists():
            fails.append(f"[must-exist] 文档承诺存在但缺失: {rel}")


def check_phantoms(fails: list[str]) -> None:
    for doc in CORE_DOCS:
        text = read(doc)
        if not text:
            continue
        for ref in PHANTOM_REFS:
            if ref in text and not (ROOT / ref).exists():
                fails.append(f"[phantom] {doc} 仍引用不存在的目标: '{ref}'")


def check_extension_disclosure(fails: list[str]) -> None:
    idx = read("docs/SKILL-INDEX.md")
    for sk in EXTENSION_SKILLS:
        on_disk = list(ROOT.glob(f"skills/**/{sk}*"))
        if on_disk and sk not in idx:
            fails.append(f"[roster] 扩展 Skill 存在于磁盘但 SKILL-INDEX 未披露: {sk}")


def check_brand_consistency(fails: list[str]) -> None:
    canon = read("data/brand/brand-canon.yaml")
    if canon:
        required = [
            "status: active_canonical",
            "role: 超级个体成长教练",
            "slogan: AI 是工具，哲学是地基，你才是杠杆的支点。",
            "model: staged_dual_core",
            "lily:",
            "marcus:",
            "id: ai_era_cognition",
            "id: self_construction",
            "id: personal_brand_narrative",
            "id: one_person_business",
            "id: philosophy_psychology_ground",
            "workflow_contracts:",
        ]
        for marker in required:
            if marker not in canon:
                fails.append(f"[brand] brand-canon.yaml 缺少关键标记: {marker}")

    for doc in BRAND_ACTIVE_DOCS:
        text = read(doc)
        if not text:
            fails.append(f"[brand] 活跃品牌文档不存在或为空: {doc}")
            continue
        for pattern in RETIRED_BRAND_PATTERNS:
            if pattern in text:
                fails.append(f"[brand] {doc} 仍残留旧品牌口径: {pattern}")

    for doc in BRAND_CONSUMER_DOCS:
        text = read(doc)
        if text and "data/brand/brand-canon.yaml" not in text:
            fails.append(f"[brand] {doc} 未声明读取品牌契约 data/brand/brand-canon.yaml")


def main() -> int:
    fails: list[str] = []
    check_commands(fails)
    check_must_exist(fails)
    check_phantoms(fails)
    check_extension_disclosure(fails)
    check_brand_consistency(fails)

    if fails:
        print("FAIL: 文档/目录自洽检查未通过\n")
        for f in fails:
            print("  - " + f)
        print(f"\n共 {len(fails)} 项问题。")
        return 1
    print("PASS: 文档/目录自洽检查通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
