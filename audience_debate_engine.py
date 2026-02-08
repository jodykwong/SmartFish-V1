"""
Audience Debate Engine
受众簇辩论引擎 - 基于BMad Party Model
"""
from typing import Dict, List
import json


class AudienceDebateEngine:
    """受众簇辩论引擎"""
    
    # 辩论角色配置（基于BMad Party Model）
    DEBATE_ROLES = {
        "supporter": {
            "name": "支持方 (Mary - 商业分析师)",
            "icon": "📊",
            "role": "论证受众簇值得投入",
            "focus": ["付费意愿证据", "市场规模", "竞争优势"],
            "prompt_template": """你是Mary，商业分析师。你需要论证这个受众簇值得投入。

受众簇信息：
- 角色：{role}
- 场景：{scenario}
- KPI：{kpi}
- 证据数量：{evidence_count}
- 核心痛点：{pain_points}
- 付费信号：{payment_signals}
- 总分：{total_score}

请从以下角度论证：
1. 付费意愿证据是否充分
2. 市场规模是否足够
3. 是否有竞争优势

输出JSON格式：
{{
    "support_evidence": ["证据1", "证据2"],
    "key_advantages": ["优势1", "优势2"],
    "confidence": 0.8
}}
"""
        },
        "opponent": {
            "name": "反对方 (Dr. Quinn - 问题解决专家)",
            "icon": "🔬",
            "role": "指出风险和不确定性",
            "focus": ["证据不足", "执行难度", "竞争风险"],
            "prompt_template": """你是Dr. Quinn，问题解决专家。你需要指出这个受众簇的风险和不确定性。

受众簇信息：
- 角色：{role}
- 场景：{scenario}
- KPI：{kpi}
- 证据数量：{evidence_count}
- 核心痛点：{pain_points}
- 土办法：{workarounds}
- 总分：{total_score}

请从以下角度质疑：
1. 证据是否不足
2. 执行难度是否过高
3. 是否存在竞争风险

输出JSON格式：
{{
    "opposing_evidence": ["风险1", "风险2"],
    "key_risks": ["风险1", "风险2"],
    "confidence": 0.6
}}
"""
        },
        "moderator": {
            "name": "主持人 (Bob - Scrum Master)",
            "icon": "🏃",
            "role": "综合双方观点做出裁决",
            "focus": ["不确定性", "下一步行动"],
            "prompt_template": """你是Bob，Scrum Master。你需要综合支持方和反对方的观点，做出裁决。

受众簇信息：
- 角色：{role}
- 场景：{scenario}
- 总分：{total_score}

支持方观点：
{support_view}

反对方观点：
{oppose_view}

请做出裁决：
1. 决策：proceed（继续）/ hold（暂缓）/ reject（拒绝）
2. 列出3个关键不确定性
3. 给出下一步行动建议

输出JSON格式：
{{
    "decision": "proceed",
    "uncertainties": ["不确定性1", "不确定性2", "不确定性3"],
    "next_steps": ["步骤1", "步骤2"]
}}
"""
        }
    }
    
    @staticmethod
    def _format_cluster_info(cluster: Dict) -> Dict:
        """格式化簇信息"""
        return {
            "role": cluster.get("role", ""),
            "scenario": cluster.get("scenario", ""),
            "kpi": ", ".join(cluster.get("kpi_constraints", [])),
            "evidence_count": cluster.get("score_card", {}).get("evidence_count", 0),
            "pain_points": "\n".join(cluster.get("pain_points", [])[:3]),
            "payment_signals": "\n".join(cluster.get("payment_signals", [])[:3]) or "无",
            "workarounds": "\n".join(cluster.get("workarounds", [])[:3]) or "无",
            "total_score": cluster.get("score_card", {}).get("total_score", 0)
        }
    
    @staticmethod
    def _simulate_llm_response(role: str, cluster_info: Dict, extra_context: Dict = None) -> Dict:
        """
        模拟LLM响应（简化版）
        实际使用时应调用真实LLM API
        """
        if role == "supporter":
            # 支持方逻辑
            evidence_count = cluster_info["evidence_count"]
            total_score = cluster_info["total_score"]
            
            support_evidence = []
            if evidence_count >= 2:
                support_evidence.append(f"证据充分：已收集{evidence_count}条用户原话")
            if total_score >= 15:
                support_evidence.append(f"评分较高：总分{total_score}/40，超过平均水平")
            if cluster_info["payment_signals"] != "无":
                support_evidence.append("存在付费信号：用户提及付费相关关键词")
            
            key_advantages = [
                f"痛点明确：{cluster_info['role']}在{cluster_info['scenario']}场景下的痛点清晰",
                f"KPI压力：{cluster_info['kpi']}是核心指标，用户有强烈改善需求"
            ]
            
            confidence = min(0.5 + evidence_count * 0.1, 0.9)
            
            return {
                "support_evidence": support_evidence,
                "key_advantages": key_advantages,
                "confidence": confidence
            }
        
        elif role == "opponent":
            # 反对方逻辑
            evidence_count = cluster_info["evidence_count"]
            
            opposing_evidence = []
            if evidence_count < 5:
                opposing_evidence.append(f"证据不足：仅{evidence_count}条证据，样本量偏小")
            if cluster_info["payment_signals"] == "无":
                opposing_evidence.append("无付费信号：用户未明确表达付费意愿")
            
            key_risks = [
                "市场规模未验证：需要更多数据确认市场容量",
                "竞争情况未知：需要调研现有解决方案",
                f"执行难度：{cluster_info['workarounds']}可能表明问题复杂度高"
            ]
            
            confidence = 0.7
            
            return {
                "opposing_evidence": opposing_evidence,
                "key_risks": key_risks,
                "confidence": confidence
            }
        
        elif role == "moderator":
            # 主持人逻辑
            support_view = extra_context.get("support_view", {})
            oppose_view = extra_context.get("oppose_view", {})
            
            # 简单决策逻辑
            support_conf = support_view.get("confidence", 0)
            oppose_conf = oppose_view.get("confidence", 0)
            
            if support_conf > 0.7 and len(support_view.get("support_evidence", [])) >= 2:
                decision = "proceed"
            elif support_conf < 0.5:
                decision = "reject"
            else:
                decision = "hold"
            
            uncertainties = [
                "市场规模需要进一步验证",
                "付费意愿需要用户访谈确认",
                "竞争格局需要深入调研"
            ]
            
            next_steps = [
                "进行10人用户访谈，验证痛点真实性",
                "制作简单落地页，测试转化率",
                "调研现有竞品，分析差异化空间"
            ]
            
            return {
                "decision": decision,
                "uncertainties": uncertainties,
                "next_steps": next_steps
            }
    
    @classmethod
    def debate_cluster(cls, cluster: Dict) -> Dict:
        """
        对受众簇进行辩论
        
        Args:
            cluster: 受众簇字典
        
        Returns:
            辩论结果
        """
        cluster_info = cls._format_cluster_info(cluster)
        
        # 1. 支持方发言
        support_view = cls._simulate_llm_response("supporter", cluster_info)
        
        # 2. 反对方发言
        oppose_view = cls._simulate_llm_response("opponent", cluster_info)
        
        # 3. 主持人裁决
        decision = cls._simulate_llm_response("moderator", cluster_info, {
            "support_view": support_view,
            "oppose_view": oppose_view
        })
        
        return {
            "cluster_id": cluster.get("cluster_id"),
            "cluster_name": f"{cluster.get('role')} - {cluster.get('scenario')}",
            "support": {
                "agent": cls.DEBATE_ROLES["supporter"]["name"],
                "icon": cls.DEBATE_ROLES["supporter"]["icon"],
                **support_view
            },
            "oppose": {
                "agent": cls.DEBATE_ROLES["opponent"]["name"],
                "icon": cls.DEBATE_ROLES["opponent"]["icon"],
                **oppose_view
            },
            "decision": {
                "agent": cls.DEBATE_ROLES["moderator"]["name"],
                "icon": cls.DEBATE_ROLES["moderator"]["icon"],
                **decision
            }
        }
    
    @classmethod
    def debate_top_clusters(cls, clusters: List[Dict], top_n: int = 2) -> List[Dict]:
        """
        对Top N受众簇进行辩论
        
        Args:
            clusters: 受众簇列表
            top_n: 辩论数量
        
        Returns:
            辩论结果列表
        """
        top_clusters = sorted(
            clusters, 
            key=lambda x: x.get("score_card", {}).get("total_score", 0),
            reverse=True
        )[:top_n]
        
        debates = []
        for cluster in top_clusters:
            debate_result = cls.debate_cluster(cluster)
            debates.append(debate_result)
        
        return debates
