from datetime import datetime
from database import db

class GateReview(db.Model):
    __tablename__ = 'gate_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('thinking_entries.id'), nullable=False)
    reviewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 四层过滤结果
    human_dependency_pass = db.Column(db.Boolean)
    value_self_evident_pass = db.Column(db.Boolean)
    feedback_clean_pass = db.Column(db.Boolean)
    role_cost_pass = db.Column(db.Boolean)
    
    # 决策结果
    decision = db.Column(db.String(20), nullable=False)  # pass/fail
    fail_level = db.Column(db.String(50))
    fail_reason = db.Column(db.Text)
    notes = db.Column(db.Text)
    version = db.Column(db.Integer, default=1)
    
    def to_dict(self):
        return {
            'id': self.id,
            'entry_id': self.entry_id,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'decision': self.decision,
            'fail_level': self.fail_level,
            'fail_reason': self.fail_reason,
            'results': {
                'layer1': self.human_dependency_pass,
                'layer2': self.value_self_evident_pass,
                'layer3': self.feedback_clean_pass,
                'layer4': self.role_cost_pass
            }
        }
