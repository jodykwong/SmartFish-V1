"""
痛点发现引擎

整合多数据源进行痛点发现、聚类分析和商业潜力评估。
"""

import os
import json
from typing import List, Dict, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from collections import defaultdict
from loguru import logger

from bmad_adapter import (
    BMADPainPointDiscovery, 
    PainPoint, 
    ValidationResult,
    DomainConfig
)


@dataclass
class ClusterResult:
    """聚类结果"""
    cluster_id: str
    theme: str                          # 聚类主题
    pain_points: List[PainPoint]        # 包含的痛点
    total_mentions: int = 0             # 总提及次数
    avg_sentiment: float = 0.0          # 平均情感得分
    commercial_score: float = 0.0       # 商业价值评分
    
    def to_dict(self) -> Dict:
        return {
            "cluster_id": self.cluster_id,
            "theme": self.theme,
            "pain_point_count": len(self.pain_points),
            "total_mentions": self.total_mentions,
            "avg_sentiment": self.avg_sentiment,
            "commercial_score": self.commercial_score
        }


class PainPointClusteringEngine:
    """痛点聚类引擎"""
    
    def __init__(self, similarity_threshold: float = 0.7):
        self.similarity_threshold = similarity_threshold
        
    def cluster_pain_points(self, pain_points: List[PainPoint]) -> List[ClusterResult]:
        """
        对痛点进行聚类分析
        
        Args:
            pain_points: 痛点列表
            
        Returns:
            聚类结果列表
        """
        if not pain_points:
            return []
            
        # 按领域和关键词分组
        domain_groups = defaultdict(list)
        for pp in pain_points:
            key = (pp.domain, tuple(sorted(pp.keywords[:2])))
            domain_groups[key].append(pp)
            
        clusters = []
        for i, ((domain, keywords), group) in enumerate(domain_groups.items()):
            cluster = ClusterResult(
                cluster_id=f"cluster_{i+1}",
                theme=f"{domain}: {', '.join(keywords)}",
                pain_points=group,
                total_mentions=sum(pp.mention_count for pp in group),
                avg_sentiment=sum(pp.sentiment_score for pp in group) / len(group),
                commercial_score=sum(pp.commercial_potential for pp in group) / len(group)
            )
            clusters.append(cluster)
            
        # 按商业价值排序
        clusters.sort(key=lambda x: x.commercial_score, reverse=True)
        
        return clusters
        
    def calculate_similarity(self, pp1: PainPoint, pp2: PainPoint) -> float:
        """计算两个痛点的相似度"""
        # 关键词重叠度
        kw1 = set(pp1.keywords)
        kw2 = set(pp2.keywords)
        
        if not kw1 or not kw2:
            return 0.0
            
        overlap = len(kw1 & kw2)
        total = len(kw1 | kw2)
        
        return overlap / total if total > 0 else 0.0


class CommercialPotentialAnalyzer:
    """商业潜力分析器"""
    
    def __init__(self):
        self.weights = {
            "frequency": 0.25,          # 提及频率
            "sentiment_intensity": 0.20, # 情感强度
            "user_diversity": 0.20,     # 用户多样性
            "urgency": 0.15,            # 紧迫性
            "solution_gap": 0.20        # 解决方案缺口
        }
        
    def analyze(self, pain_point: PainPoint) -> Dict:
        """
        分析痛点的商业潜力
        
        Returns:
            包含各维度评分和总分的字典
        """
        scores = {
            "frequency": self._score_frequency(pain_point),
            "sentiment_intensity": self._score_sentiment(pain_point),
            "user_diversity": self._score_diversity(pain_point),
            "urgency": self._score_urgency(pain_point),
            "solution_gap": self._score_solution_gap(pain_point)
        }
        
        # 加权总分
        total = sum(
            scores[k] * self.weights[k] 
            for k in scores
        )
        
        return {
            "pain_point_id": pain_point.id,
            "dimension_scores": scores,
            "weighted_total": total,
            "rating": self._get_rating(total),
            "recommendation": self._get_recommendation(total, scores)
        }
        
    def _score_frequency(self, pp: PainPoint) -> float:
        """评估提及频率"""
        return min(pp.mention_count / 30, 1.0)
        
    def _score_sentiment(self, pp: PainPoint) -> float:
        """评估情感强度 (越负面越高)"""
        return max(0, (1 - pp.sentiment_score) / 2)
        
    def _score_diversity(self, pp: PainPoint) -> float:
        """评估来源多样性"""
        return min(len(pp.sources) / 5, 1.0)
        
    def _score_urgency(self, pp: PainPoint) -> float:
        """评估紧迫性 (基于关键词)"""
        urgent_words = ["急", "立刻", "马上", "必须", "无法", "崩溃", "严重"]
        count = sum(
            1 for quote in pp.user_quotes 
            for word in urgent_words 
            if word in quote
        )
        return min(count / 3, 1.0)
        
    def _score_solution_gap(self, pp: PainPoint) -> float:
        """评估解决方案缺口"""
        # 简化版：假设负面情感意味着现有方案不足
        return max(0, (1 - pp.sentiment_score) / 2) * 0.8 + 0.2
        
    def _get_rating(self, score: float) -> str:
        """获取评级"""
        if score >= 0.8:
            return "极高潜力"
        elif score >= 0.6:
            return "高潜力"
        elif score >= 0.4:
            return "中等潜力"
        else:
            return "低潜力"
            
    def _get_recommendation(self, total: float, scores: Dict) -> str:
        """生成建议"""
        if total >= 0.7:
            return "强烈建议进入Phase 1深入验证"
        elif total >= 0.5:
            return "建议进一步调研用户付费意愿"
        else:
            return "建议继续观察或寻找其他痛点"


class PainPointDiscoveryEngine:
    """
    痛点发现引擎 - 整合发现、聚类和分析
    """
    
    def __init__(self, config_path: str = None):
        self.config = DomainConfig(config_path)
        self.discovery = BMADPainPointDiscovery(self.config)
        self.clustering = PainPointClusteringEngine()
        self.analyzer = CommercialPotentialAnalyzer()
        
        self.all_pain_points: List[PainPoint] = []
        self.clusters: List[ClusterResult] = []
        self.analysis_results: List[Dict] = []
        
    def run_discovery(self, domains: List[str] = None) -> Dict:
        """
        运行完整的痛点发现流程
        
        Args:
            domains: 要发现的领域列表，None表示所有领域
            
        Returns:
            发现结果摘要
        """
        logger.info("=== 开始痛点发现流程 ===")
        
        # 1. 确定要发现的领域
        all_domains = self.config.get_all_domains()
        target_domains = domains or list(all_domains.keys())
        
        # 2. 逐个领域发现痛点
        for domain in target_domains:
            logger.info(f"发现领域: {domain}")
            points = self.discovery.discover_pain_points(domain)
            self.all_pain_points.extend(points)
            
        # 3. 聚类分析
        logger.info("正在进行聚类分析...")
        self.clusters = self.clustering.cluster_pain_points(self.all_pain_points)
        
        # 4. 商业潜力分析
        logger.info("正在评估商业潜力...")
        for pp in self.all_pain_points:
            analysis = self.analyzer.analyze(pp)
            self.analysis_results.append(analysis)
            pp.commercial_potential = analysis["weighted_total"]
            
        # 5. 验证痛点
        validated = self._validate_all()
        
        return {
            "status": "success",
            "total_discovered": len(self.all_pain_points),
            "clusters_count": len(self.clusters),
            "validated_count": len(validated),
            "top_opportunities": self._get_top_opportunities(3),
            "timestamp": datetime.now().isoformat()
        }
        
    def _validate_all(self) -> List[PainPoint]:
        """验证所有痛点"""
        validated = []
        for pp in self.all_pain_points:
            result = self.discovery.validate_frequency(pp)
            if result.is_valid:
                validated.append(pp)
        return validated
        
    def _get_top_opportunities(self, n: int = 3) -> List[Dict]:
        """获取前N个商业机会"""
        sorted_points = sorted(
            self.all_pain_points,
            key=lambda x: x.commercial_potential,
            reverse=True
        )
        
        return [
            {
                "id": pp.id,
                "title": pp.title,
                "commercial_potential": pp.commercial_potential,
                "mention_count": pp.mention_count,
                "domain": pp.domain
            }
            for pp in sorted_points[:n]
        ]
        
    def save_results(self, output_dir: str = "_bmad-output") -> Dict[str, str]:
        """保存所有结果"""
        os.makedirs(output_dir, exist_ok=True)
        
        paths = {}
        
        # 保存原始痛点数据
        raw_path = os.path.join(output_dir, "pain-points-raw-data.json")
        with open(raw_path, 'w', encoding='utf-8') as f:
            json.dump({
                "pain_points": [pp.to_dict() for pp in self.all_pain_points],
                "generated_at": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        paths["raw_data"] = raw_path
        
        # 保存聚类结果
        cluster_path = os.path.join(output_dir, "clustering-results.json")
        with open(cluster_path, 'w', encoding='utf-8') as f:
            json.dump({
                "clusters": [c.to_dict() for c in self.clusters],
                "generated_at": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        paths["clusters"] = cluster_path
        
        # 保存商业分析
        analysis_path = os.path.join(output_dir, "commercial-analysis.json")
        with open(analysis_path, 'w', encoding='utf-8') as f:
            json.dump({
                "analyses": self.analysis_results,
                "generated_at": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        paths["analysis"] = analysis_path
        
        logger.info(f"结果已保存到: {output_dir}")
        return paths
        
    def get_summary_report(self) -> str:
        """生成摘要报告"""
        standards = self.config.get_validation_standards()
        
        validated = self._validate_all()
        top_opps = self._get_top_opportunities(5)
        
        report = f"""# 痛点发现摘要报告

## 发现概览
- **总发现痛点数**: {len(self.all_pain_points)}
- **验证通过数**: {len(validated)}
- **聚类数量**: {len(self.clusters)}

## 验证标准
- 最少痛点数: {standards.get('min_pain_points', 3)}
- 最少用户确认: {standards.get('min_user_confirmations', 3)}
- 最低付费意愿: {standards.get('min_payment_willingness', 0.3) * 100}%

## 商业机会TOP5
"""
        for i, opp in enumerate(top_opps, 1):
            report += f"{i}. **{opp['title']}** (潜力: {opp['commercial_potential']:.2f})\n"
            
        report += f"\n---\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return report


if __name__ == "__main__":
    print("=== 痛点发现引擎测试 ===\n")
    
    engine = PainPointDiscoveryEngine()
    
    # 运行发现 (仅测试一个领域)
    result = engine.run_discovery(["ai_chat_tools"])
    
    print(f"发现结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # 保存结果
    paths = engine.save_results()
    print(f"\n结果已保存: {paths}")
    
    # 打印摘要报告
    print("\n" + engine.get_summary_report())
