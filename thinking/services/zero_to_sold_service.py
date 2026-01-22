import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

class ZeroToSoldService:
    """Zero to Sold方法论服务"""
    
    TEMPLATE_DIR = 'docs/templates'
    OUTPUT_DIR = 'docs/thinking'
    
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(self.TEMPLATE_DIR))
    
    @staticmethod
    def score_problem_intensity(importance, urgency):
        """
        问题强度评分（Eisenhower框架）
        importance: 1-5
        urgency: 1-5
        返回: 1-25分 + 优先级标签
        """
        score = importance * urgency
        
        if score >= 20:
            priority = '重要且紧急'
            action = '优先处理'
        elif score >= 15:
            priority = '重要不紧急'
            action = '计划处理'
        elif score >= 10:
            priority = '紧急不重要'
            action = '委托或快速处理'
        else:
            priority = '不重要不紧急'
            action = '考虑放弃'
        
        return {
            'score': score,
            'importance': importance,
            'urgency': urgency,
            'priority': priority,
            'action': action
        }
    
    def generate_interview_guide(self, entry):
        """生成访谈脚本"""
        template = self.env.get_template('interview-guide.md.j2')
        
        context = {
            'entry': entry,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        content = template.render(**context)
        
        # 保存文件
        filename = f"{datetime.now().strftime('%Y-%m-%d')}_{self._slugify(entry.title)}_interview-guide.md"
        filepath = os.path.join(self.OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def generate_market_research(self, entry, research_data):
        """生成市场研究报告"""
        template = self.env.get_template('market-research.md.j2')
        
        context = {
            'entry': entry,
            'research_data': research_data,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        content = template.render(**context)
        
        # 保存文件
        filename = f"{datetime.now().strftime('%Y-%m-%d')}_{self._slugify(entry.title)}_market-research.md"
        filepath = os.path.join(self.OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def generate_market_review(self, entry, review_data):
        """生成市场转向复核"""
        template = self.env.get_template('market-review.md.j2')
        
        context = {
            'entry': entry,
            'review_data': review_data,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        content = template.render(**context)
        
        # 保存文件
        filename = f"{datetime.now().strftime('%Y-%m-%d')}_{self._slugify(entry.title)}_market-review.md"
        filepath = os.path.join(self.OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    @staticmethod
    def _slugify(text):
        """转换为URL友好的slug"""
        import re
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text[:50]
