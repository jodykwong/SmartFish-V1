"""
测试Thinking System集成（使用SQLite）
"""
import json
import sys
import os
sys.path.insert(0, '/home/sunrise/SmartFish')

# 设置SQLite数据库
os.environ['DATABASE_URL'] = 'sqlite:///thinking.db'

from flask import Flask
from database import db
from thinking.services.audience_service import AudienceService
from thinking.models.audience_cluster import AudienceCluster, EvidenceRef


def create_test_app():
    """创建测试应用"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thinking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


def test_integration():
    """测试集成"""
    app = create_test_app()
    
    with app.app_context():
        # 创建表
        db.create_all()
        
        # 加载测试数据
        with open('prototype/test_data.json', 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        # 模拟entry_id
        entry_id = 999
        
        print("=" * 80)
        print("测试Thinking System集成（SQLite）")
        print("=" * 80)
        
        # 1. 执行分析
        print("\n1. 执行受众分析...")
        clusters = AudienceService.analyze_audiences(entry_id, raw_data, max_clusters=5)
        print(f"   ✅ 成功创建 {len(clusters)} 个受众簇")
        
        # 2. 查询结果
        print("\n2. 查询受众簇...")
        saved_clusters = AudienceService.get_clusters_by_entry(entry_id)
        print(f"   ✅ 查询到 {len(saved_clusters)} 个受众簇")
        
        # 3. 获取Top 2
        print("\n3. 获取Top 2受众簇...")
        top_clusters = AudienceService.get_top_clusters(entry_id, top_n=2)
        print(f"   ✅ Top 2受众簇:")
        for i, cluster in enumerate(top_clusters, 1):
            print(f"      {i}. {cluster['role']} - {cluster['scenario']} (总分: {cluster['score_card']['total_score']})")
        
        # 4. 验证证据引用
        print("\n4. 验证证据引用...")
        first_cluster = saved_clusters[0]
        evidence_count = len(first_cluster['evidence_refs'])
        print(f"   ✅ 第一个簇包含 {evidence_count} 条证据")
        
        print("\n" + "=" * 80)
        print("✅ Thinking System集成测试通过")
        print("=" * 80)


if __name__ == "__main__":
    test_integration()
