import os
import hashlib
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from werkzeug.utils import secure_filename
from database import db
from thinking.models.artifact import Artifact

class ArtifactService:
    """工件生成服务"""
    
    TEMPLATE_DIR = 'docs/templates'
    OUTPUT_DIR = 'docs/thinking'
    
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(self.TEMPLATE_DIR))
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
    
    def generate_artifact(self, entry, artifact_type, user_name='User'):
        """
        生成工件
        artifact_type: tech-spec, product-brief, prd
        """
        # 加载模板
        template = self.env.get_template(f'{artifact_type}.md.j2')
        
        # 准备数据
        context = {
            'entry': entry,
            'user_name': user_name,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'routing_info': self._get_routing_info(entry)
        }
        
        # 渲染
        content = template.render(**context)
        
        # 保存
        filename = self._generate_filename(entry, artifact_type)
        filepath = os.path.join(self.OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 记录元数据
        artifact = Artifact(
            entry_id=entry.id,
            type=artifact_type,
            path=filepath,
            checksum=self._calculate_checksum(content)
        )
        db.session.add(artifact)
        db.session.commit()
        
        return artifact
    
    def _generate_filename(self, entry, artifact_type):
        """生成文件名"""
        date = datetime.now().strftime('%Y-%m-%d')
        slug = self._slugify(entry.title)
        return f'{date}_{slug}_{artifact_type}.md'
    
    def _slugify(self, text):
        """转换为URL友好的slug"""
        # 简化版：只保留字母数字和连字符
        import re
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text[:50]  # 限制长度
    
    def _calculate_checksum(self, content):
        """计算文件校验和"""
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _get_routing_info(self, entry):
        """获取路由信息"""
        from thinking.services.routing_service import RoutingService
        return RoutingService.suggest_routing(entry)
    
    def get_artifacts(self, entry_id):
        """获取条目的所有工件"""
        return Artifact.query.filter_by(entry_id=entry_id).all()
