"""
Audience Cluster Model
受众簇数据模型
"""
import json
from datetime import datetime
from typing import List, Dict, Optional
from database import db


# ScoreCard 作为内嵌数据，不需要单独的类


class AudienceCluster(db.Model):
    """受众簇 - SQLAlchemy模型"""
    __tablename__ = 'audience_clusters'
    
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('thinking_entries.id'), nullable=False)
    cluster_id = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(100))
    scenario = db.Column(db.String(200))
    kpi_constraints = db.Column(db.Text)  # JSON
    waterholes = db.Column(db.Text)  # JSON
    pain_points = db.Column(db.Text)  # JSON
    workarounds = db.Column(db.Text)  # JSON
    payment_signals = db.Column(db.Text)  # JSON
    wtp_score = db.Column(db.Float, default=0.0)
    pain_frequency = db.Column(db.Float, default=0.0)
    moat_score = db.Column(db.Float, default=0.0)
    gtm_score = db.Column(db.Float, default=0.0)
    total_score = db.Column(db.Float, default=0.0)
    evidence_count = db.Column(db.Integer, default=0)
    confidence = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    evidence_refs = db.relationship('EvidenceRef', backref='cluster', lazy=True, cascade='all, delete-orphan')
    
    @staticmethod
    def from_dict(data: Dict, entry_id: int) -> 'AudienceCluster':
        """从字典创建"""
        cluster = AudienceCluster(
            entry_id=entry_id,
            cluster_id=data['cluster_id'],
            role=data['role'],
            scenario=data['scenario'],
            kpi_constraints=json.dumps(data['kpi_constraints'], ensure_ascii=False),
            waterholes=json.dumps(data.get('waterholes', []), ensure_ascii=False),
            pain_points=json.dumps(data.get('pain_points', []), ensure_ascii=False),
            workarounds=json.dumps(data.get('workarounds', []), ensure_ascii=False),
            payment_signals=json.dumps(data.get('payment_signals', []), ensure_ascii=False)
        )
        
        # 评分卡
        if 'score_card' in data and data['score_card']:
            sc = data['score_card']
            cluster.wtp_score = sc.get('wtp_score', 0.0)
            cluster.pain_frequency = sc.get('pain_frequency', 0.0)
            cluster.moat_score = sc.get('moat_score', 0.0)
            cluster.gtm_score = sc.get('gtm_score', 0.0)
            cluster.total_score = sc.get('total_score', 0.0)
            cluster.evidence_count = sc.get('evidence_count', 0)
            cluster.confidence = sc.get('confidence', 0.0)
        
        return cluster
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'cluster_id': self.cluster_id,
            'role': self.role,
            'scenario': self.scenario,
            'kpi_constraints': json.loads(self.kpi_constraints) if self.kpi_constraints else [],
            'waterholes': json.loads(self.waterholes) if self.waterholes else [],
            'pain_points': json.loads(self.pain_points) if self.pain_points else [],
            'workarounds': json.loads(self.workarounds) if self.workarounds else [],
            'payment_signals': json.loads(self.payment_signals) if self.payment_signals else [],
            'score_card': {
                'wtp_score': self.wtp_score,
                'pain_frequency': self.pain_frequency,
                'moat_score': self.moat_score,
                'gtm_score': self.gtm_score,
                'total_score': self.total_score,
                'evidence_count': self.evidence_count,
                'confidence': self.confidence
            },
            'evidence_refs': [e.to_dict() for e in self.evidence_refs]
        }


class EvidenceRef(db.Model):
    """证据引用 - SQLAlchemy模型"""
    __tablename__ = 'evidence_refs'
    
    id = db.Column(db.Integer, primary_key=True)
    cluster_id = db.Column(db.Integer, db.ForeignKey('audience_clusters.id'), nullable=False)
    platform = db.Column(db.String(50))
    url = db.Column(db.Text)
    author = db.Column(db.String(100))
    time = db.Column(db.String(50))
    text = db.Column(db.Text)
    snippet = db.Column(db.Text)
    engagement = db.Column(db.Text)  # JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def from_dict(data: Dict, cluster_id: int) -> 'EvidenceRef':
        """从字典创建"""
        return EvidenceRef(
            cluster_id=cluster_id,
            platform=data.get('platform', ''),
            url=data.get('url', ''),
            author=data.get('author', ''),
            time=data.get('time', ''),
            text=data.get('text', ''),
            snippet=data.get('snippet', ''),
            engagement=json.dumps(data.get('engagement', {}), ensure_ascii=False)
        )
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'platform': self.platform,
            'url': self.url,
            'author': self.author,
            'time': self.time,
            'text': self.text,
            'snippet': self.snippet,
            'engagement': json.loads(self.engagement) if self.engagement else {}
        }
