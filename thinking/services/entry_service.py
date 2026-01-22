from database import db
from thinking.models.thinking_entry import ThinkingEntry

class EntryService:
    @staticmethod
    def create_entry(user_id, data):
        entry = ThinkingEntry(
            user_id=user_id,
            title=data.get('title'),
            signal=data.get('signal'),
            target_segment=data.get('target_segment'),
            problem=data.get('problem'),
            hypothesis=data.get('hypothesis'),
            evidence_needed=data.get('evidence_needed'),
            mva=data.get('mva'),
            success_metric=data.get('success_metric'),
            constraints=data.get('constraints'),
            dependencies=data.get('dependencies')
        )
        db.session.add(entry)
        db.session.commit()
        return entry
    
    @staticmethod
    def get_entry(entry_id, user_id):
        return ThinkingEntry.query.filter_by(id=entry_id, user_id=user_id).first()
    
    @staticmethod
    def list_entries(user_id, status=None, page=1, per_page=20):
        query = ThinkingEntry.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        query = query.order_by(ThinkingEntry.created_at.desc())
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def update_entry(entry_id, user_id, data):
        entry = ThinkingEntry.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            return None
        
        for key, value in data.items():
            if hasattr(entry, key):
                setattr(entry, key, value)
        
        db.session.commit()
        return entry
    
    @staticmethod
    def delete_entry(entry_id, user_id):
        entry = ThinkingEntry.query.filter_by(id=entry_id, user_id=user_id).first()
        if entry:
            db.session.delete(entry)
            db.session.commit()
            return True
        return False
