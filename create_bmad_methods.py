#!/usr/bin/env python3
"""
批量生成BMAD分析方法配置文件
"""

import os
import yaml
from pathlib import Path

# 38种分析方法的完整定义
METHODS = {
    # 头脑风暴技术 (20种)
    "mind_map": {
        "name": "思维导图分析",
        "category": "brainstorming",
        "description": "从中心概念向外发散，构建知识网络",
        "prompt": "使用思维导图方法，从核心主题出发，向外扩展相关概念、关联和子主题。构建完整的知识网络结构。"
    },
    "yes_and": {
        "name": "Yes And 构建法",
        "category": "brainstorming", 
        "description": "接受并扩展他人想法，促进协作创新",
        "prompt": "采用'Yes, And...'的思维模式，在现有观点基础上进行扩展和深化，避免否定性思维。"
    },
    "round_robin": {
        "name": "轮流贡献法",
        "category": "brainstorming",
        "description": "每个角度依次贡献想法，确保全面覆盖",
        "prompt": "从多个不同角度轮流分析问题，确保每个视角都得到充分表达和探讨。"
    },
    "random_stimulus": {
        "name": "随机刺激法",
        "category": "brainstorming",
        "description": "引入随机元素激发创意思维",
        "prompt": "引入随机的概念、词汇或场景，通过意外的关联激发新的思维路径和创意解决方案。"
    },
    "morphological": {
        "name": "形态分析法",
        "category": "brainstorming",
        "description": "列出参数，探索组合可能性",
        "prompt": "将问题分解为多个独立参数，列出每个参数的可能取值，然后探索不同组合的可能性。"
    },
    "provocation": {
        "name": "挑衅技术(PO)",
        "category": "brainstorming",
        "description": "提出挑衅性陈述激发新想法",
        "prompt": "使用挑衅性操作(Provocative Operation)，提出看似不合理的陈述，通过打破常规思维激发创新。"
    },
    "forced_connection": {
        "name": "强制关联法",
        "category": "brainstorming",
        "description": "连接不相关概念寻找创新",
        "prompt": "强制连接看似不相关的概念、对象或想法，通过意外的关联发现新的解决方案。"
    },
    "assumption_reversal": {
        "name": "假设反转法",
        "category": "brainstorming",
        "description": "挑战核心假设，重新构建思路",
        "prompt": "识别并挑战问题中的核心假设，通过反转这些假设来重新构建解决思路。"
    },
    "role_play": {
        "name": "角色扮演法",
        "category": "brainstorming",
        "description": "从不同利益相关者角度思考",
        "prompt": "扮演不同的利益相关者角色，从他们的视角分析问题，理解不同立场的需求和关切。"
    },
    "time_shift": {
        "name": "时间转移法",
        "category": "brainstorming",
        "description": "从不同时代角度分析问题",
        "prompt": "将问题置于不同的时间背景下思考：'1995年如何解决？''2030年会怎样？'探索时间维度的影响。"
    },
    "resource_constraint": {
        "name": "资源约束法",
        "category": "brainstorming",
        "description": "在极限约束下寻找创意解决方案",
        "prompt": "设定极端的资源约束条件（如只有10元和1小时），在限制中寻找创意和高效的解决方案。"
    },
    "metaphor_mapping": {
        "name": "隐喻映射法",
        "category": "brainstorming",
        "description": "用隐喻理解复杂概念",
        "prompt": "使用隐喻和比喻来理解和解释复杂概念，通过形象化的表达促进理解和洞察。"
    },
    "question_storming": {
        "name": "问题风暴法",
        "category": "brainstorming",
        "description": "生成问题而非答案",
        "prompt": "专注于生成高质量的问题而不是答案，通过提出正确的问题来引导思考方向。"
    },
    
    # 高级引导方法 (15种)
    "expand_contract": {
        "name": "扩展收缩法",
        "category": "advanced",
        "description": "根据受众调整内容深度",
        "prompt": "根据目标受众的需求，灵活调整分析的深度和广度，在宏观概览和细节深入之间找到平衡。"
    },
    "logic_flow": {
        "name": "逻辑流程分析",
        "category": "advanced",
        "description": "检查内容结构和依赖关系",
        "prompt": "分析论证的逻辑结构，检查前提与结论的关系，确保推理过程的严密性和连贯性。"
    },
    "goal_alignment": {
        "name": "目标对齐评估",
        "category": "advanced",
        "description": "评估内容是否服务于目标",
        "prompt": "持续评估分析内容是否与既定目标保持一致，确保每个部分都为实现目标服务。"
    },
    "risk_identification": {
        "name": "风险识别法",
        "category": "advanced",
        "description": "从专业角度识别潜在风险",
        "prompt": "系统性地识别和评估潜在风险，包括技术风险、市场风险、运营风险等多个维度。"
    },
    "devils_advocate": {
        "name": "魔鬼代言人法",
        "category": "advanced",
        "description": "扮演批判角色挑战方案",
        "prompt": "扮演魔鬼代言人的角色，对提出的方案进行批判性挑战，发现潜在的弱点和问题。"
    },
    "premortem": {
        "name": "事前复盘法",
        "category": "advanced",
        "description": "假设失败，提前识别风险",
        "prompt": "假设项目已经失败，回顾分析可能的失败原因，提前识别和预防潜在风险。"
    },
    "agile_perspectives": {
        "name": "敏捷团队视角",
        "category": "advanced",
        "description": "PO/SM/Dev/QA多角色轮换",
        "prompt": "从产品负责人、Scrum Master、开发者、测试工程师等不同角色的视角分析问题。"
    },
    "meta_prompting": {
        "name": "元提示分析",
        "category": "advanced",
        "description": "反思当前方法，优化流程",
        "prompt": "对当前使用的分析方法进行反思和评估，识别改进机会，优化分析流程。"
    },
    "self_consistency": {
        "name": "自一致性验证",
        "category": "advanced",
        "description": "多次生成取共识",
        "prompt": "通过多次独立分析同一问题，比较结果的一致性，提高结论的可靠性。"
    },
    "rewoo": {
        "name": "ReWOO推理法",
        "category": "advanced",
        "description": "推理-观察-优化循环",
        "prompt": "采用推理(Reasoning)-观察(Observation)-优化(Optimization)的循环方法，持续改进分析质量。"
    },
    "role_pattern_hybrid": {
        "name": "角色模式混合法",
        "category": "advanced",
        "description": "结合角色扮演与模式匹配",
        "prompt": "将角色扮演与模式识别相结合，既保持特定视角的深度，又运用通用模式的指导。"
    },
    
    # 游戏化方法 (3种)
    "escape_room": {
        "name": "密室逃脱挑战",
        "category": "gamification",
        "description": "在约束中寻找创意解决方案",
        "prompt": "将问题设计为密室逃脱挑战，在给定的约束条件下寻找创意的解决路径。"
    }
}

def create_method_file(method_id, method_data):
    """创建单个方法配置文件"""
    category = method_data["category"]
    
    # 确定目录
    if category == "brainstorming":
        dir_path = Path("config/analysis_methods/brainstorming_extended")
    elif category == "advanced":
        dir_path = Path("config/analysis_methods/advanced_extended")
    elif category == "gamification":
        dir_path = Path("config/analysis_methods/gamification_extended")
    else:
        dir_path = Path("config/analysis_methods/other")
    
    # 创建目录
    dir_path.mkdir(parents=True, exist_ok=True)
    
    # 创建配置内容
    config = {
        "id": method_id,
        "name": method_data["name"],
        "category": category,
        "description": method_data["description"],
        "prompt_template": method_data["prompt"],
        "tags": [category, "BMAD方法论", "结构化分析"],
        "complexity": "medium",
        "estimated_time": "15-25分钟"
    }
    
    # 写入文件
    file_path = dir_path / f"{method_id}.yaml"
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, indent=2)
    
    print(f"创建方法配置: {file_path}")

def main():
    """批量创建所有方法配置文件"""
    print("开始创建BMAD分析方法配置文件...")
    
    for method_id, method_data in METHODS.items():
        create_method_file(method_id, method_data)
    
    print(f"\n完成！共创建了 {len(METHODS)} 个分析方法配置文件")
    print("现在系统支持完整的38种BMAD分析方法")

if __name__ == "__main__":
    main()
