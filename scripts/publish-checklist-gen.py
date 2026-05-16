#!/usr/bin/env python3
"""
Publish Checklist Generator (降级自 Skill s-4.2.3)
V1.1: 发布清单基于模板生成，纯数据组装操作。
"""
import json
from datetime import datetime

PLATFORM_CHECKLIST = {
    "公众号": [
        "内容终稿确认", "标题(≤30字)确认", "封面图设计",
        "摘要/描述撰写", "标签设置", "原创声明",
        "发布时间设定", "评论区置顶内容", "关联往期文章",
    ],
    "知乎": [
        "内容终稿确认", "标题优化", "话题标签(≤5)",
        "关联问题", "专栏发布", "发布时间",
    ],
    "小红书": [
        "图片(6-9张)准备", "封面图文案", "正文文案(300-800字)",
        "话题标签(10-15)", "发布时间", "评论区互动预设",
    ],
    "B站": [
        "视频终审", "封面(高对比大字)", "标题", "简介",
        "标签", "分区选择", "发布时间",
    ],
    "抖音": [
        "视频终审", "封面文案", "标题/描述",
        "话题标签", "发布时间", "评论区预设",
    ],
}

def generate_checklist(content_title, platforms, publish_date=None):
    if not publish_date:
        publish_date = datetime.now().strftime("%Y-%m-%d")
    
    checklist = {"title": content_title, "date": publish_date, "platforms": {}}
    
    for platform in platforms:
        items = PLATFORM_CHECKLIST.get(platform, [])
        checklist["platforms"][platform] = [
            {"item": item, "done": False} for item in items
        ]
    
    return checklist

if __name__ == "__main__":
    import sys
    title = sys.argv[1] if len(sys.argv) > 1 else "示例内容"
    platforms = sys.argv[2:] if len(sys.argv) > 2 else list(PLATFORM_CHECKLIST.keys())
    result = generate_checklist(title, platforms)
    print(json.dumps(result, ensure_ascii=False, indent=2))
