#!/usr/bin/env python3
"""Lightweight regression tests for scripts/gatekeeper.py."""
from __future__ import annotations

from gatekeeper import (
    validate_kb_entry,
    validate_publish_package,
    validate_quality_gate_report,
    validate_review_conclusion,
)


def assert_status(name: str, result: dict, expected: str) -> None:
    actual = result["status"]
    assert actual == expected, f"{name}: expected {expected}, got {actual}: {result}"


def test_kb_upgrade_blocks_unverified_single_source() -> None:
    result = validate_kb_entry({
        "target_status": "reviewed",
        "verified": False,
        "sources": ["https://example.com/one"],
        "id": "kb-1",
        "title": "t",
        "date": "2026-06-06",
        "category": "viewpoint",
        "source": "https://example.com/one",
        "status": "draft",
    })
    assert_status("kb unverified upgrade", result, "blocked")


def test_empty_publish_package_blocks() -> None:
    result = validate_publish_package({
        "slice_id": "slice-001",
        "platform": "xiaohongshu",
        "title": "title",
        "body": "   ",
    })
    assert_status("empty publish package", result, "blocked")


def test_causal_without_ab_blocks() -> None:
    result = validate_review_conclusion({
        "conclusion_level": "causal",
        "sample_size": 10,
    })
    assert_status("causal without ab", result, "blocked")


def test_imputed_causal_blocks() -> None:
    result = validate_review_conclusion({
        "conclusion_level": "causal",
        "sample_size": 10,
        "ab_test": {"variant_a": "a", "variant_b": "b"},
        "is_imputed": True,
    })
    assert_status("imputed causal", result, "blocked")


def test_report_with_high_blocker_cannot_pass() -> None:
    result = validate_quality_gate_report({
        "gate": "publish_package_gate",
        "artifact": {"path": "content/slices/demo/slice-001-xhs-note.md"},
        "reviewer": {"agent_id": "reviewer-1", "context_mode": "fresh_independent"},
        "gate_status": "pass",
        "blockers": [{"severity": "high", "summary": "body empty"}],
    })
    assert_status("self-contradicting report", result, "blocked")


def test_valid_cases_pass() -> None:
    assert_status("kb verified", validate_kb_entry({
        "target_status": "reviewed",
        "verified": True,
        "sources": ["a", "b"],
        "id": "kb-2",
        "title": "t",
        "date": "2026-06-06",
        "category": "viewpoint",
        "source": "a",
        "status": "draft",
    }), "pass")
    assert_status("publish package", validate_publish_package({
        "slice_id": "slice-001",
        "platform": "xiaohongshu",
        "title": "title",
        "body": "正文",
    }), "pass")
    assert_status("causal with ab", validate_review_conclusion({
        "conclusion_level": "causal",
        "sample_size": 10,
        "ab_test": {"primary_metric": "save_rate"},
    }), "pass")


def main() -> None:
    tests = [
        test_kb_upgrade_blocks_unverified_single_source,
        test_empty_publish_package_blocks,
        test_causal_without_ab_blocks,
        test_imputed_causal_blocks,
        test_report_with_high_blocker_cannot_pass,
        test_valid_cases_pass,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")


if __name__ == "__main__":
    main()
