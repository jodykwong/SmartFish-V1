from datetime import datetime
from database import db

class Artifact(db.Model):
    __tablename__ = 'artifacts'
    
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('thinking_entries.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # tech-spec/product-brief/prd/etc
    path = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    checksum = db.Column(db.String(64))
    
    def to_dict(self):
        return {
            'id': self.id,
            'entry_id': self.entry_id,
            'type': self.type,
            'path': self.path,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
