"""
Audience Clustering Engine
受众聚类引擎 - 规则聚类版本
"""
import yaml
import hashlib
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Optional, Tuple
from pathlib import Path


# 临时数据类（用于引擎内部）
class ClusterData:
    """临时簇数据"""
    def __init__(self, cluster_id: str, role: str, scenario: str, kpi: str):
        self.cluster_id = cluster_id
        self.role = role
        self.scenario = scenario
        self.kpi = kpi
        self.evidence_refs = []
        self.pain_points = []
        self.workarounds = []
        self.payment_signals = []
        self.score_card = {}
    
    def to_dict(self):
        return {
            'cluster_id': self.cluster_id,
            'role': self.role,
            'scenario': self.scenario,
            'kpi_constraints': [self.kpi],
            'waterholes': [],
            'pain_points': self.pain_points,
            'workarounds': self.workarounds,
            'payment_signals': self.payment_signals,
            'evidence_refs': self.evidence_refs,
            'score_card': self.score_card
        }


class AudienceClusteringEngine:
    """受众聚类引擎"""
    
    def __init__(self, config_dir: str = "config/audience_dictionaries"):
        self.config_dir = Path(config_dir)
        self.role_dict = self._load_yaml("roles.yaml")
        self.scenario_dict = self._load_yaml("scenarios.yaml")
        self.kpi_dict = self._load_yaml("kpi_constraints.yaml")
    
    def _load_yaml(self, filename: str) -> List[Dict]:
        """加载YAML词典"""
        path = self.config_dir / filename
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return list(data.values())[0]  # 获取第一个键的值
    
    def _extract_tags(self, text: str) -> Dict[str, Optional[str]]:
        """提取标签"""
        tags = {"role": None, "scenario": None, "kpi": None}
        
        # 角色匹配
        for item in self.role_dict:
            if any(kw in text for kw in item["keywords"]):
                tags["role"] = item["name"]
                break
        
        # 场景匹配
        for item in self.scenario_dict:
            if any(kw in text for kw in item["keywords"]):
                tags["scenario"] = item["name"]
                break
        
        # KPI匹配
        for item in self.kpi_dict:
            if any(kw in text for kw in item["keywords"]):
                tags["kpi"] = item["name"]
                break
        
        return tags
    
    def _extract_pain_points(self, text: str) -> List[str]:
        """提取痛点"""
        pain_keywords = ["累", "难", "压力", "加班", "熬夜", "撕逼", "痛苦", "困难", "麻烦"]
        pain_points = []
        
        for keyword in pain_keywords:
            if keyword in text:
                # 提取包含痛点关键词的句子片段
                pain_points.append(text[:80] + "..." if len(text) > 80 else text)
                break
        
        return pain_points
    
    def _extract_workarounds(self, text: str) -> List[str]:
        """提取土办法"""
        workaround_keywords = ["手动", "人工", "自己", "Excel", "表格", "复制粘贴"]
        workarounds = []
        
        for keyword in workaround_keywords:
            if keyword in text:
                workarounds.append(f"使用{keyword}处理")
                break
        
        return workarounds
    
    def _extract_payment_signals(self, text: str) -> List[str]:
        """提取付费信号"""
        payment_keywords = ["付费", "买", "购买", "订阅", "会员", "工具", "软件", "系统"]
        signals = []
        
        for keyword in payment_keywords:
            if keyword in text:
                signals.append(f"提及{keyword}")
        
        return signals
    
    def _calculate_score(self, cluster: ClusterData) -> Dict:
        """计算评分"""
        evidence_count = len(cluster.evidence_refs)
        
        # WTP: 付费信号数量 × 权重
        wtp_score = len(cluster.payment_signals) * 2.0
        
        # 痛苦高频: 证据数量 × 权重
        pain_frequency = evidence_count * 1.5
        
        # Moat: 土办法复杂度（简化版）
        moat_score = len(cluster.workarounds) * 1.0 + 5.0
        
        # GTM: 固定基础分（后续可优化）
        gtm_score = 6.0
        
        # 置信度: 基于证据数量
        confidence = min(evidence_count / 10.0, 1.0) * 100
        
        total_score = wtp_score + pain_frequency + moat_score + gtm_score
        
        return {
            'wtp_score': wtp_score,
            'pain_frequency': pain_frequency,
            'moat_score': moat_score,
            'gtm_score': gtm_score,
            'total_score': total_score,
            'evidence_count': evidence_count,
            'confidence': confidence
        }
    
    def _generate_cluster_id(self, role: str, scenario: str, kpi: str) -> str:
        """生成簇ID"""
        key = f"{role}_{scenario}_{kpi}"
        return hashlib.md5(key.encode()).hexdigest()[:8]
    
    def cluster(self, raw_data: List[Dict], max_clusters: int = 5) -> List[Dict]:
        """
        核心聚类逻辑
        
        Args:
            raw_data: 原始数据列表，每项包含 text, platform, author, time 等字段
            max_clusters: 最大簇数量
        
        Returns:
            排序后的受众簇字典列表
        """
        cluster_map = defaultdict(lambda: None)
        
        for item in raw_data:
            text = item.get("text", "")
            platform = item.get("platform", "未知")
            author = item.get("author", "匿名")
            time_str = item.get("time", "")
            
            # 标签提取
            tags = self._extract_tags(text)
            
            # 跳过无法分类的数据
            if not all(tags.values()):
                continue
            
            # 聚类键
            key = (tags["role"], tags["scenario"], tags["kpi"])
            
            # 初始化簇
            if cluster_map[key] is None:
                cluster_id = self._generate_cluster_id(*key)
                cluster_map[key] = ClusterData(
                    cluster_id=cluster_id,
                    role=tags["role"],
                    scenario=tags["scenario"],
                    kpi=tags["kpi"]
                )
            
            cluster = cluster_map[key]
            
            # 创建证据引用
            evidence = {
                'platform': platform,
                'url': item.get("url", ""),
                'author': author,
                'time': time_str,
                'text': text,
                'snippet': text[:100] + "..." if len(text) > 100 else text,
                'engagement': {}
            }
            cluster.evidence_refs.append(evidence)
            
            # 提取痛点
            pain_points = self._extract_pain_points(text)
            cluster.pain_points.extend(pain_points)
            
            # 提取土办法
            workarounds = self._extract_workarounds(text)
            cluster.workarounds.extend(workarounds)
            
            # 提取付费信号
            payment_signals = self._extract_payment_signals(text)
            cluster.payment_signals.extend(payment_signals)
        
        # 转换为列表
        clusters = [c for c in cluster_map.values() if c is not None]
        
        # 计算评分
        for cluster in clusters:
            cluster.score_card = self._calculate_score(cluster)
        
        # 排序
        clusters.sort(key=lambda x: x.score_card['total_score'], reverse=True)
        
        # 转换为字典
        return [c.to_dict() for c in clusters[:max_clusters]]
