from datetime import datetime
from database import db
from thinking.models.research_task import ResearchTask
from thinking.models.thinking_entry import ThinkingEntry
from thinking.celery_app import celery
import os
import json

class TaskService:
    """研究任务服务"""
    
    @staticmethod
    def create_task(entry_id, engine, query, task_type='evidence_research'):
        """创建研究任务"""
        task = ResearchTask(
            entry_id=entry_id,
            engine=engine,
            task_type=task_type,
            query=query,
            status='pending'
        )
        db.session.add(task)
        db.session.commit()
        
        # 提交到Celery队列
        execute_research_task.delay(task.id)
        
        return task
    
    @staticmethod
    def get_task(task_id):
        """获取任务"""
        return ResearchTask.query.get(task_id)
    
    @staticmethod
    def get_entry_tasks(entry_id):
        """获取条目的所有任务"""
        return ResearchTask.query.filter_by(entry_id=entry_id)\
            .order_by(ResearchTask.created_at.desc()).all()
    
    @staticmethod
    def backfill_evidence(task_id, entry_id):
        """回填证据到条目"""
        task = ResearchTask.query.get(task_id)
        if not task or task.status != 'completed':
            return None
        
        entry = ThinkingEntry.query.get(entry_id)
        if not entry:
            return None
        
        # 读取结果
        if task.result_path and os.path.exists(task.result_path):
            with open(task.result_path, 'r', encoding='utf-8') as f:
                result = f.read()
            
            # 回填到evidence_needed字段
            if entry.evidence_needed:
                entry.evidence_needed += f"\n\n## 补充证据 ({datetime.now().strftime('%Y-%m-%d')})\n\n{result}"
            else:
                entry.evidence_needed = result
            
            db.session.commit()
            return entry
        
        return None


@celery.task(bind=True, max_retries=3)
def execute_research_task(self, task_id):
    """
    执行研究任务（Celery异步任务）
    """
    task = ResearchTask.query.get(task_id)
    if not task:
        return {'error': 'Task not found'}
    
    try:
        # 更新状态
        task.status = 'running'
        db.session.commit()
        
        # 调用对应的Agent
        result = call_agent(task.engine, task.query)
        
        # 保存结果
        result_path = save_result(task.id, result)
        
        # 更新任务
        task.status = 'completed'
        task.result_path = result_path
        task.completed_at = datetime.utcnow()
        db.session.commit()
        
        return {'status': 'completed', 'result_path': result_path}
        
    except Exception as exc:
        task.status = 'failed'
        task.error_message = str(exc)
        task.retry_count += 1
        db.session.commit()
        
        # 重试
        if task.retry_count < 3:
            raise self.retry(exc=exc, countdown=60 * task.retry_count)
        
        return {'status': 'failed', 'error': str(exc)}


def call_agent(engine, query):
    """
    调用Agent（简化版）
    实际应该调用现有的QueryEngine/MindSpider等
    """
    # TODO: 集成实际的Agent
    # 这里返回模拟结果
    return {
        'engine': engine,
        'query': query,
        'results': [
            {'source': 'Example Source', 'content': 'Example evidence content'},
        ],
        'summary': f'Based on {engine} search for "{query}", found relevant evidence.'
    }


def save_result(task_id, result):
    """保存结果到文件"""
    os.makedirs('docs/research', exist_ok=True)
    
    filename = f'research-task-{task_id}.json'
    filepath = os.path.join('docs/research', filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return filepath
