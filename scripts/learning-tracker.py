#!/usr/bin/env python3
"""
学习追踪脚本 - 从 s-1.1.4-learning-tracker.md 降级而来

功能：追踪学习进度与知识覆盖情况
用法：python scripts/learning-tracker.py [command]

命令：
  status              显示当前学习状态
  add <topic>         添加学习主题
  complete <topic>    标记主题为已完成
  report              生成学习报告
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 配置
DATA_DIR = Path("data/learning")
TRACKER_FILE = DATA_DIR / "learning-tracker.json"

def init_tracker():
    """初始化追踪器"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not TRACKER_FILE.exists():
        data = {
            "topics": [],
            "completed": [],
            "created_at": datetime.now().isoformat()
        }
        save_data(data)

def load_data():
    """加载追踪数据"""
    if not TRACKER_FILE.exists():
        init_tracker()
    with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """保存追踪数据"""
    with open(TRACKER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_topic(topic):
    """添加学习主题"""
    data = load_data()
    entry = {
        "topic": topic,
        "added_at": datetime.now().isoformat(),
        "status": "pending"
    }
    data["topics"].append(entry)
    save_data(data)
    print(f"✅ 已添加学习主题: {topic}")

def complete_topic(topic):
    """标记主题为已完成"""
    data = load_data()
    for item in data["topics"]:
        if item["topic"] == topic and item["status"] == "pending":
            item["status"] = "completed"
            item["completed_at"] = datetime.now().isoformat()
            data["completed"].append(item)
            save_data(data)
            print(f"✅ 已完成学习主题: {topic}")
            return
    print(f"❌ 未找到待完成的主题: {topic}")

def show_status():
    """显示当前学习状态"""
    data = load_data()
    pending = [t for t in data["topics"] if t["status"] == "pending"]
    completed = [t for t in data["topics"] if t["status"] == "completed"]

    print(f"\n📊 学习追踪状态")
    print(f"{'='*50}")
    print(f"待学习: {len(pending)} 个主题")
    print(f"已完成: {len(completed)} 个主题")
    print(f"完成率: {len(completed)/(len(pending)+len(completed))*100:.1f}%")

    if pending:
        print(f"\n📝 待学习主题:")
        for t in pending[:5]:
            print(f"  - {t['topic']}")
        if len(pending) > 5:
            print(f"  ... 还有 {len(pending)-5} 个")

def generate_report():
    """生成学习报告"""
    data = load_data()
    report_file = DATA_DIR / f"report-{datetime.now().strftime('%Y%m%d')}.md"

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"# 学习追踪报告\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## 统计\n\n")
        f.write(f"- 总主题数: {len(data['topics'])}\n")
        f.write(f"- 已完成: {len(data['completed'])}\n")
        f.write(f"- 待学习: {len(data['topics']) - len(data['completed'])}\n\n")

        f.write(f"## 已完成主题\n\n")
        for t in data['completed']:
            f.write(f"- {t['topic']} (完成于: {t.get('completed_at', 'N/A')})\n")

    print(f"✅ 报告已生成: {report_file}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "status":
        show_status()
    elif command == "add" and len(sys.argv) > 2:
        add_topic(sys.argv[2])
    elif command == "complete" and len(sys.argv) > 2:
        complete_topic(sys.argv[2])
    elif command == "report":
        generate_report()
    else:
        print(__doc__)
