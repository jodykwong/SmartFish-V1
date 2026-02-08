"""
Audience Service
受众分析服务
"""
from typing import List, Dict
from database import db
from thinking.models.audience_cluster import AudienceCluster, EvidenceRef
from audience_clustering_engine import AudienceClusteringEngine
from audience_report_generator import AudienceReportGenerator
from audience_debate_engine import AudienceDebateEngine


class AudienceService:
    """受众分析服务"""
    
    @staticmethod
    def analyze_audiences(entry_id: int, raw_data: List[Dict], max_clusters: int = 5) -> List[Dict]:
        """
        分析受众簇
        
        Args:
            entry_id: Thinking Entry ID
            raw_data: 原始数据列表
            max_clusters: 最大簇数量
        
        Returns:
            受众簇字典列表
        """
        # 1. 调用聚类引擎
        engine = AudienceClusteringEngine()
        cluster_results = engine.cluster(raw_data, max_clusters=max_clusters)
        
        # 2. 保存到数据库
        saved_clusters = []
        for cluster_dict in cluster_results:
            # cluster_results已经是字典列表
            # 创建数据库模型
            cluster = AudienceCluster.from_dict(cluster_dict, entry_id)
            db.session.add(cluster)
            db.session.flush()  # 获取cluster.id
            
            # 保存证据引用
            for evidence_data in cluster_dict.get('evidence_refs', []):
                evidence = EvidenceRef.from_dict(evidence_data, cluster.id)
                db.session.add(evidence)
            
            saved_clusters.append(cluster)
        
        db.session.commit()
        
        # 3. 返回结果
        return [c.to_dict() for c in saved_clusters]
    
    @staticmethod
    def get_clusters_by_entry(entry_id: int) -> List[Dict]:
        """
        获取指定Entry的受众簇
        
        Args:
            entry_id: Thinking Entry ID
        
        Returns:
            受众簇字典列表
        """
        clusters = AudienceCluster.query.filter_by(entry_id=entry_id).order_by(
            AudienceCluster.total_score.desc()
        ).all()
        
        return [c.to_dict() for c in clusters]
    
    @staticmethod
    def get_top_clusters(entry_id: int, top_n: int = 2) -> List[Dict]:
        """
        获取Top N受众簇
        
        Args:
            entry_id: Thinking Entry ID
            top_n: 返回数量
        
        Returns:
            Top N受众簇字典列表
        """
        clusters = AudienceCluster.query.filter_by(entry_id=entry_id).order_by(
            AudienceCluster.total_score.desc()
        ).limit(top_n).all()
        
        return [c.to_dict() for c in clusters]
    
    @staticmethod
    def generate_report(entry_id: int) -> str:
        """
        生成Audience First报告
        
        Args:
            entry_id: Thinking Entry ID
        
        Returns:
            Markdown格式报告
        """
        clusters = AudienceService.get_clusters_by_entry(entry_id)
        
        if not clusters:
            return "# 暂无受众分析数据\n\n请先执行受众分析。"
        
        report = AudienceReportGenerator.generate(clusters)
        return report
    
    @staticmethod
    def debate_clusters(entry_id: int, top_n: int = 2) -> List[Dict]:
        """
        对受众簇进行辩论
        
        Args:
            entry_id: Thinking Entry ID
            top_n: 辩论数量
        
        Returns:
            辩论结果列表
        """
        clusters = AudienceService.get_clusters_by_entry(entry_id)
        
        if not clusters:
            return []
        
        debates = AudienceDebateEngine.debate_top_clusters(clusters, top_n=top_n)
        return debates
