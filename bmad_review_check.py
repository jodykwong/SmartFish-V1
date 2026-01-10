#!/usr/bin/env python3
"""
BMAD-METHOD Code Review 自动检查脚本
"""

import os
import re
from pathlib import Path

def check_bmad_integration():
    """检查BMAD方法论集成情况"""
    
    results = {
        "forum_host_bmad": False,
        "template_structure": False,
        "evidence_check": False,
        "validation_node": False,
        "agent_roles": False
    }
    
    # 检查Forum Host是否包含BMAD逻辑
    forum_host_path = Path("ForumEngine/llm_host.py")
    if forum_host_path.exists():
        content = forum_host_path.read_text()
        if "BMAD" in content or "定义阶段" in content:
            results["forum_host_bmad"] = True
    
    # 检查是否有BMAD模板
    template_dir = Path("ReportEngine/report_template/")
    if template_dir.exists():
        for template in template_dir.glob("*.md"):
            content = template.read_text()
            if "Executive Summary" in content or "执行摘要" in content:
                results["template_structure"] = True
                break
    
    # 检查证据校验机制
    report_engine_files = list(Path("ReportEngine/").rglob("*.py"))
    for file_path in report_engine_files:
        content = file_path.read_text()
        if "Source ID" in content or "来源" in content:
            results["evidence_check"] = True
            break
    
    # 检查验证节点
    validation_files = list(Path(".").rglob("*validation*.py"))
    if validation_files:
        results["validation_node"] = True
    
    # 检查Agent角色定义
    agent_files = [
        "QueryEngine/prompts/prompts.py",
        "InsightEngine/prompts/prompts.py", 
        "MediaEngine/prompts/prompts.py"
    ]
    
    for agent_file in agent_files:
        if Path(agent_file).exists():
            content = Path(agent_file).read_text()
            if "Market Researcher" in content or "Business Analyst" in content:
                results["agent_roles"] = True
                break
    
    return results

def generate_review_report(results):
    """生成审查报告"""
    
    print("=" * 50)
    print("BMAD-METHOD Code Review 结果")
    print("=" * 50)
    
    total_checks = len(results)
    passed_checks = sum(results.values())
    
    for check, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check}: {'PASS' if status else 'FAIL'}")
    
    print(f"\n总体评分: {passed_checks}/{total_checks} ({passed_checks/total_checks*100:.1f}%)")
    
    if passed_checks == total_checks:
        print("🎉 BMAD方法论集成完整！")
    else:
        print("⚠️  需要完善BMAD集成")
        print("\n建议优先处理:")
        for check, status in results.items():
            if not status:
                print(f"  - {check}")

if __name__ == "__main__":
    results = check_bmad_integration()
    generate_review_report(results)
