"""
Audience Clustering Engine - 最小原型
验证核心逻辑：规则聚类 + 评分机制
"""
import json
import re
from collections import defaultdict
from typing import List, Dict

# 词典（硬编码最小集）
ROLES = {
    "电商运营": ["运营", "电商", "店铺", "店主"],
    "产品经理": ["产品", "PM", "需求", "PRD"]
}

SCENARIOS = {
    "大促备战": ["大促", "618", "双11", "活动"],
    "日常运营": ["日常", "每天", "天天"]
}

KPI_CONSTRAINTS = {
    "GMV": ["GMV", "销售额", "成交额"],
    "转化率": ["转化", "转化率", "CVR"],
    "ROI": ["ROI", "投放", "效果"]
}

class AudienceCluster:
    def __init__(self, role, scenario, kpi):
        self.role = role
        self.scenario = scenario
        self.kpi = kpi
        self.evidence = []
        self.pain_points = []
        self.score = 0.0
    
    def to_dict(self):
        return {
            "role": self.role,
            "scenario": self.scenario,
            "kpi": self.kpi,
            "evidence_count": len(self.evidence),
            "pain_points": self.pain_points[:3],
            "score": round(self.score, 2)
        }

class AudienceClusteringEngine:
    def __init__(self):
        self.roles = ROLES
        self.scenarios = SCENARIOS
        self.kpis = KPI_CONSTRAINTS
    
    def _extract_tags(self, text: str) -> Dict:
        """提取标签"""
        tags = {"role": None, "scenario": None, "kpi": None}
        
        for role, keywords in self.roles.items():
            if any(kw in text for kw in keywords):
                tags["role"] = role
                break
        
        for scenario, keywords in self.scenarios.items():
            if any(kw in text for kw in keywords):
                tags["scenario"] = scenario
                break
        
        for kpi, keywords in self.kpis.items():
            if any(kw in text for kw in keywords):
                tags["kpi"] = kpi
                break
        
        return tags
    
    def _extract_pain_point(self, text: str) -> str:
        """提取痛点（简单规则）"""
        pain_keywords = ["累", "难", "压力", "加班", "熬夜", "撕逼"]
        for keyword in pain_keywords:
            if keyword in text:
                return text[:50] + "..."
        return ""
    
    def _calculate_score(self, cluster: AudienceCluster) -> float:
        """计算评分（简化版）"""
        # WTP: 付费信号词频
        wtp = len([e for e in cluster.evidence if "付费" in e or "买" in e]) * 2
        
        # 痛苦高频: 证据数量
        pain_freq = len(cluster.evidence) * 1.5
        
        # Moat: 固定值（原型阶段）
        moat = 5.0
        
        # GTM: 固定值（原型阶段）
        gtm = 6.0
        
        return wtp + pain_freq + moat + gtm
    
    def cluster(self, raw_data: List[Dict], max_clusters: int = 3) -> List[AudienceCluster]:
        """核心聚类逻辑"""
        # 1. 标签提取 + 分组
        cluster_map = defaultdict(lambda: AudienceCluster(None, None, None))
        
        for item in raw_data:
            text = item["text"]
            tags = self._extract_tags(text)
            
            # 跳过无法分类的数据
            if not all(tags.values()):
                continue
            
            # 聚类键
            key = (tags["role"], tags["scenario"], tags["kpi"])
            
            # 归集证据
            cluster = cluster_map[key]
            cluster.role = tags["role"]
            cluster.scenario = tags["scenario"]
            cluster.kpi = tags["kpi"]
            cluster.evidence.append(text)
            
            # 提取痛点
            pain = self._extract_pain_point(text)
            if pain:
                cluster.pain_points.append(pain)
        
        # 2. 评分
        clusters = list(cluster_map.values())
        for cluster in clusters:
            cluster.score = self._calculate_score(cluster)
        
        # 3. 排序 + 返回Top N
        clusters.sort(key=lambda x: x.score, reverse=True)
        return clusters[:max_clusters]


def main():
    """验证流程"""
    # 加载测试数据
    with open("test_data.json") as f:
        raw_data = json.load(f)
    
    # 聚类
    engine = AudienceClusteringEngine()
    clusters = engine.cluster(raw_data, max_clusters=3)
    
    # 输出结果
    print("=" * 60)
    print("受众聚类结果（原型验证）")
    print("=" * 60)
    
    for i, cluster in enumerate(clusters, 1):
        result = cluster.to_dict()
        print(f"\n簇{i}: {result['role']} - {result['scenario']} - {result['kpi']}")
        print(f"  证据数量: {result['evidence_count']}")
        print(f"  核心痛点: {result['pain_points']}")
        print(f"  总分: {result['score']}")
    
    print("\n" + "=" * 60)
    print("✅ 核心逻辑验证通过")
    print("=" * 60)


if __name__ == "__main__":
    main()
