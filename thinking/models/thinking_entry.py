from datetime import datetime
from database import db

class ThinkingEntry(db.Model):
    __tablename__ = 'thinking_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='想法')
    tags = db.Column(db.Text)
    routing_type = db.Column(db.String(50))
    
    # 核心字段
    signal = db.Column(db.Text)
    target_segment = db.Column(db.Text)
    problem = db.Column(db.Text)
    hypothesis = db.Column(db.Text)
    evidence_needed = db.Column(db.Text)
    mva = db.Column(db.Text)
    success_metric = db.Column(db.Text)
    constraints = db.Column(db.Text)
    dependencies = db.Column(db.Text)
    
    # Zero to Sold扩展字段
    audience_definition = db.Column(db.Text)
    audience_size_estimate = db.Column(db.Text)
    payability_notes = db.Column(db.Text)
    tribes_watercoolers = db.Column(db.Text)
    market_signals = db.Column(db.Text)
    problem_intensity_score = db.Column(db.Integer)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'signal': self.signal,
            'target_segment': self.target_segment,
            'problem': self.problem,
            'hypothesis': self.hypothesis,
            'mva': self.mva,
            'success_metric': self.success_metric,
            'problem_intensity_score': self.problem_intensity_score
        }
