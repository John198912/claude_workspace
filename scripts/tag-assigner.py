#!/usr/bin/env python3
"""
Tag Assigner Script (降级自 Skill s-1.3.2)
V1.1: 纯规则匹配的标签分配，不消耗 LLM tokens。
仅在规则无法判断时返回 needs_llm=True，由 s-1.3.1 处理。
"""
import json
import re
from pathlib import Path

# 标签体系定义
DOMAIN_KEYWORDS = {
    "personal-growth": ["个人成长", "认知", "习惯", "情绪", "目标", "自律", "执行力", "时间管理"],
    "ai-technology": ["AI", "人工智能", "GPT", "大模型", "机器学习", "深度学习", "LLM", "Agent"],
    "business-model": ["商业", "变现", "获客", "定价", "一人公司", "个人品牌", "副业"],
    "psychology": ["心理", "认知偏差", "行为", "动机", "情感", "焦虑", "抑郁"],
    "philosophy": ["哲学", "存在主义", "斯多葛", "伦理", "认识论"],
    "education": ["教育", "学习", "教学", "课程", "导师"],
    "social-observation": ["社会", "职场", "996", "内卷", "代际"],
    "creation-methodology": ["写作", "创作", "内容策略", "叙事", "平台运营"],
    "career-development": ["职业", "转型", "技能迁移", "自由职业", "远程"],
    "productivity": ["效率", "工具", "自动化", "工作流", "知识管理"],
}

def assign_domain(title: str, content: str) -> dict:
    """基于关键词匹配分配领域标签"""
    text = f"{title} {content}".lower()
    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text)
        if score > 0:
            scores[domain] = score
    
    if not scores:
        return {"primary_domain": None, "confidence": "low", "needs_llm": True}
    
    sorted_domains = sorted(scores.items(), key=lambda x: -x[1])
    primary = sorted_domains[0]
    
    confidence = "high" if primary[1] >= 3 else "medium" if primary[1] >= 2 else "low"
    needs_llm = confidence == "low"
    
    return {
        "primary_domain": primary[0],
        "secondary_domains": [d[0] for d in sorted_domains[1:3]],
        "confidence": confidence,
        "needs_llm": needs_llm,
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python tag-assigner.py <note.md>")
        sys.exit(1)
    
    note_path = Path(sys.argv[1])
    content = note_path.read_text(encoding="utf-8")
    title = content.split("\n")[0].strip("# ").strip()
    
    result = assign_domain(title, content)
    print(json.dumps(result, ensure_ascii=False, indent=2))
