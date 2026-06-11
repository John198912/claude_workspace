#!/usr/bin/env python3
"""gatekeeper.py · 关键节点质量门的可执行内核 (V2.1)

把四类「可被代码判定」的阻断逻辑做成纯函数，供 reviewer 子 agent / Orchestrator 调用，
得到确定性裁决 (status, blockers)。语义审查（事实 vs 解释的判别等）仍由独立 reviewer
子 agent 完成；这里只兜底硬规则，确保「可阻断」承诺有落地点，并可被 test_gatekeeper.py 回归。

协议见 docs/QUALITY-GATES.md。无第三方依赖，纯标准库。
"""
from __future__ import annotations

from typing import Any

# 与 data/schemas/*.schema.json 保持一致的已知平台集合
KNOWN_PLATFORMS = {
    "wechat", "xiaohongshu", "zhihu", "bilibili",
    "douyin", "jike", "weibo", "podcast",
}

KB_STATUSES = ("draft", "reviewed", "core")
CONCLUSION_LEVELS = ("descriptive", "correlational", "causal")
KB_REQUIRED_FIELDS = ("id", "title", "date", "category", "source", "status")


def _result(gate: str, blockers: list[dict]) -> dict:
    """fatal/high 任一未清零 => blocked。"""
    severe = [b for b in blockers if b.get("severity") in ("fatal", "high")]
    return {
        "gate": gate,
        "status": "blocked" if severe else ("conditional" if blockers else "pass"),
        "blockers": blockers,
    }


def _num_sources(entry: dict) -> int:
    sources = entry.get("sources")
    if isinstance(sources, int):
        return sources
    if isinstance(sources, (list, tuple, set)):
        return len([s for s in sources if s])
    # 单一来源字符串
    if isinstance(entry.get("source"), str) and entry["source"].strip():
        return 1
    return 0


def validate_kb_entry(entry: dict) -> dict:
    """kb_publish_gate: 未验证/单来源条目最高停留在 draft；升 reviewed/core 需 >=2 独立来源或显式核验。"""
    blockers: list[dict] = []
    target = entry.get("target_status", entry.get("status", "draft"))

    if target not in KB_STATUSES:
        blockers.append({"severity": "high",
                         "summary": f"未知目标状态 '{target}'，必须是 {KB_STATUSES}"})

    if target in ("reviewed", "core"):
        verified = bool(entry.get("verified", False))
        n = _num_sources(entry)
        if not verified and n < 2:
            blockers.append({
                "severity": "high",
                "summary": f"升级到 '{target}' 需 >=2 独立来源或显式交叉核验；"
                           f"当前 verified={verified}, sources={n}。未验证条目最高只能停留在 draft。",
            })
        missing = [f for f in KB_REQUIRED_FIELDS if not entry.get(f)]
        if missing:
            blockers.append({"severity": "high",
                             "summary": f"升级前必填字段缺失: {missing}"})
    return _result("kb_publish_gate", blockers)


def validate_publish_package(pkg: dict) -> dict:
    """publish_package_gate: 正文为空 / 缺必填字段 / 未知平台 => 阻断。"""
    blockers: list[dict] = []

    body = (pkg.get("body") or "").strip()
    if not body:
        blockers.append({"severity": "fatal",
                         "summary": "发布包正文(body)为空：导出脚本将读不到正文，禁止发布。"})

    for field in ("slice_id", "platform", "title"):
        val = pkg.get(field)
        is_empty = val is None or (isinstance(val, str) and not val.strip())
        if is_empty:
            blockers.append({"severity": "high", "summary": f"发布包缺必填字段: {field}"})

    platform = pkg.get("platform")
    if platform and platform not in KNOWN_PLATFORMS:
        blockers.append({
            "severity": "high",
            "summary": f"未知平台 '{platform}'：无对应导出器，禁止静默处理。已知平台 {sorted(KNOWN_PLATFORMS)}",
        })
    return _result("publish_package_gate", blockers)


def validate_review_conclusion(conclusion: dict) -> dict:
    """data_quality_gate: 无 A/B 实验禁 causal；含估算值禁 causal。"""
    blockers: list[dict] = []
    level = conclusion.get("conclusion_level", "descriptive")

    if level not in CONCLUSION_LEVELS:
        blockers.append({"severity": "high",
                         "summary": f"未知结论等级 '{level}'，必须是 {CONCLUSION_LEVELS}"})

    if level == "causal":
        has_ab = bool(conclusion.get("ab_test")) or bool(conclusion.get("experiment_design"))
        if not has_ab:
            blockers.append({
                "severity": "high",
                "summary": "输出 causal 结论但缺少 A/B 测试或实验设计证据。"
                           "默认只允许 descriptive / correlational。",
            })
        if conclusion.get("is_imputed"):
            blockers.append({"severity": "high",
                             "summary": "基于含估算/插补值(is_imputed=True)的数据不得输出 causal 结论。"})

    sample = conclusion.get("sample_size")
    if isinstance(sample, int) and sample < 1:
        blockers.append({"severity": "high",
                         "summary": f"样本量不足 (sample_size={sample})，无法支撑任何归因结论。"})
    return _result("data_quality_gate", blockers)


def validate_quality_gate_report(report: dict) -> dict:
    """通用: 报告自身的一致性校验。fatal/high 存在却标 pass => 阻断。"""
    blockers: list[dict] = []

    required = ("gate", "artifact", "reviewer", "gate_status", "blockers")
    missing = [f for f in required if f not in report]
    if missing:
        blockers.append({"severity": "high", "summary": f"报告缺必填字段: {missing}"})

    reviewer = report.get("reviewer", {})
    if reviewer.get("context_mode") != "fresh_independent":
        blockers.append({"severity": "high",
                         "summary": "reviewer.context_mode 必须为 'fresh_independent'（独立上下文审查）"})

    inner = report.get("blockers", []) or []
    has_severe = any(b.get("severity") in ("fatal", "high") for b in inner)
    if has_severe and report.get("gate_status") != "blocked":
        blockers.append({
            "severity": "fatal",
            "summary": f"存在 fatal/high blocker 却标 gate_status='{report.get('gate_status')}'："
                       "未清零的严重问题禁止 pass/conditional。",
        })
    return _result("quality_gate_report", blockers)


if __name__ == "__main__":
    # 冒烟自检
    demos = [
        ("kb 未验证升 core", validate_kb_entry(
            {"target_status": "core", "verified": False, "sources": ["x"],
             "id": "a", "title": "t", "date": "d", "category": "c", "source": "x", "status": "draft"})),
        ("空正文发布包", validate_publish_package(
            {"slice_id": "slice-001", "platform": "xiaohongshu", "title": "t", "body": "  "})),
        ("无AB的causal", validate_review_conclusion(
            {"conclusion_level": "causal", "sample_size": 3})),
        ("报告自相矛盾", validate_quality_gate_report(
            {"gate": "kb_publish_gate", "artifact": {"path": "x"},
             "reviewer": {"agent_id": "r1", "context_mode": "fresh_independent"},
             "gate_status": "pass", "blockers": [{"severity": "high", "summary": "x"}]})),
    ]
    for name, r in demos:
        print(f"[{r['status']:>11}] {name}: {len(r['blockers'])} blocker(s)")
