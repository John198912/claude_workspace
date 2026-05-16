#!/usr/bin/env python3
"""
Data Normalizer Script (降级自 Skill s-5.1.2)
V1.1: 多平台数据标准化，纯数据格式转换操作。
"""
import json
import uuid
from datetime import datetime

UNIFIED_SCHEMA = {
    "content_id": "",
    "title": "",
    "platform": "",
    "publish_date": "",
    "content_type": "",
    "topic_category": "",
    "style_tags": [],
    "metrics": {
        "reach": 0,
        "engagement_rate": 0.0,
        "save_rate": 0.0,
        "share_rate": 0.0,
        "completion_rate": 0.0,
        "follower_growth": 0,
    },
    "normalized_score": 0.0,
}

PLATFORM_WEIGHT = {
    "公众号": {"engagement": 0.3, "save": 0.2, "share": 0.3, "completion": 0.2},
    "知乎": {"engagement": 0.4, "save": 0.3, "share": 0.1, "completion": 0.2},
    "小红书": {"engagement": 0.2, "save": 0.4, "share": 0.2, "completion": 0.2},
    "B站": {"engagement": 0.2, "save": 0.2, "share": 0.1, "completion": 0.5},
    "抖音": {"engagement": 0.2, "save": 0.1, "share": 0.2, "completion": 0.5},
}

def normalize_score(metrics, platform):
    weights = PLATFORM_WEIGHT.get(platform, {"engagement": 0.25, "save": 0.25, "share": 0.25, "completion": 0.25})
    score = (
        metrics.get("engagement_rate", 0) * weights["engagement"]
        + metrics.get("save_rate", 0) * weights["save"]
        + metrics.get("share_rate", 0) * weights["share"]
        + metrics.get("completion_rate", 0) * weights["completion"]
    ) * 100
    return round(min(score, 10.0), 2)

def normalize_record(raw, platform):
    record = UNIFIED_SCHEMA.copy()
    record["content_id"] = raw.get("id", str(uuid.uuid4())[:8])
    record["title"] = raw.get("title", "")
    record["platform"] = platform
    record["publish_date"] = raw.get("date", datetime.now().strftime("%Y-%m-%d"))
    record["content_type"] = raw.get("type", "长文")
    record["metrics"] = raw.get("metrics", {})
    record["normalized_score"] = normalize_score(record["metrics"], platform)
    return record

if __name__ == "__main__":
    sample = {
        "id": "demo-001",
        "title": "测试内容",
        "date": "2026-03-01",
        "type": "长文",
        "metrics": {
            "reach": 5000,
            "engagement_rate": 0.08,
            "save_rate": 0.05,
            "share_rate": 0.03,
            "completion_rate": 0.65,
            "follower_growth": 50,
        }
    }
    result = normalize_record(sample, "公众号")
    print(json.dumps(result, ensure_ascii=False, indent=2))
