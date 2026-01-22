from datetime import datetime
from database import db

class ResearchTask(db.Model):
    __tablename__ = 'research_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('thinking_entries.id'), nullable=False)
    engine = db.Column(db.String(50), nullable=False)  # Query/MindSpider/Insight/Report
    task_type = db.Column(db.String(50))  # evidence_research/word_of_mouth/market_turn_review
    query = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending/running/completed/failed
    result_path = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    retry_count = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'entry_id': self.entry_id,
            'engine': self.engine,
            'task_type': self.task_type,
            'query': self.query,
            'status': self.status,
            'result_path': self.result_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message
        }
