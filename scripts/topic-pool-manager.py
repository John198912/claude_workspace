#!/usr/bin/env python3
"""
Topic Pool Manager Script (降级自 Skill s-2.3.2)
V1.1: 选题库的状态流转和统计属于纯数据操作，不消耗 LLM tokens。
"""
import json
from pathlib import Path
from datetime import datetime, timedelta

TOPICS_FILE = "data/topics.json"

STATUS_FLOW = [
    "灵感种子", "待验证", "验证通过", "已排期", "创作中", "已发布", "已复盘"
]

def load_topics():
    p = Path(TOPICS_FILE)
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))

def save_topics(topics):
    Path(TOPICS_FILE).write_text(
        json.dumps(topics, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def get_stats(topics):
    stats = {s: 0 for s in STATUS_FLOW}
    for t in topics:
        s = t.get("status", "灵感种子")
        stats[s] = stats.get(s, 0) + 1
    
    total = len(topics)
    pipeline = stats.get("待验证", 0) + stats.get("验证通过", 0) + stats.get("已排期", 0)
    health = "健康" if pipeline >= 5 else "需补充" if pipeline >= 2 else "紧急补充"
    
    return {
        "total": total,
        "status_breakdown": stats,
        "pipeline_count": pipeline,
        "health": health,
    }

def find_expired(topics, days=30):
    cutoff = datetime.now() - timedelta(days=days)
    expired = []
    for t in topics:
        created = datetime.fromisoformat(t.get("created_at", datetime.now().isoformat()))
        if t.get("status") in ["灵感种子", "待验证"] and created < cutoff:
            expired.append(t)
    return expired

def advance_status(topics, topic_id, new_status):
    for t in topics:
        if t.get("id") == topic_id:
            old = t.get("status")
            t["status"] = new_status
            t["updated_at"] = datetime.now().isoformat()
            return {"id": topic_id, "old_status": old, "new_status": new_status}
    return None

if __name__ == "__main__":
    import sys
    topics = load_topics()
    
    if len(sys.argv) < 2 or sys.argv[1] == "stats":
        stats = get_stats(topics)
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    elif sys.argv[1] == "expired":
        expired = find_expired(topics)
        print(f"Found {len(expired)} expired topics")
        for t in expired:
            print(f"  - {t.get('title')} ({t.get('status')})")
