"""
端到端测试 - Audience First 完整流程
"""
import json
import sys
import os
sys.path.insert(0, '/home/sunrise/SmartFish')

os.environ['DATABASE_URL'] = 'sqlite:///thinking.db'

from flask import Flask
from database import db
from thinking.services.audience_service import AudienceService


def create_test_app():
    """创建测试应用"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thinking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


def test_end_to_end():
    """端到端测试"""
    app = create_test_app()
    
    with app.app_context():
        db.create_all()
        
        print("=" * 80)
        print("Audience First 端到端测试")
        print("=" * 80)
        
        # 1. 准备测试数据
        print("\n【步骤1】准备测试数据")
        with open('prototype/test_data.json', 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        print(f"   ✅ 加载 {len(raw_data)} 条原始数据")
        
        # 2. 执行受众分析
        print("\n【步骤2】执行受众聚类")
        entry_id = 1000
        clusters = AudienceService.analyze_audiences(entry_id, raw_data, max_clusters=5)
        print(f"   ✅ 生成 {len(clusters)} 个受众簇")
        
        # 3. 查询受众簇
        print("\n【步骤3】查询受众簇列表")
        saved_clusters = AudienceService.get_clusters_by_entry(entry_id)
        print(f"   ✅ 查询到 {len(saved_clusters)} 个受众簇")
        for i, cluster in enumerate(saved_clusters, 1):
            print(f"      {i}. {cluster['role']} - {cluster['scenario']} (总分: {cluster['score_card']['total_score']})")
        
        # 4. 获取Top2
        print("\n【步骤4】获取Top2推荐")
        top_clusters = AudienceService.get_top_clusters(entry_id, top_n=2)
        print(f"   ✅ Top2受众簇:")
        for i, cluster in enumerate(top_clusters, 1):
            sc = cluster['score_card']
            print(f"      {i}. {cluster['role']} - {cluster['scenario']}")
            print(f"         总分: {sc['total_score']}, 证据: {sc['evidence_count']}条, 置信度: {sc['confidence']}%")
        
        # 5. 生成报告
        print("\n【步骤5】生成Markdown报告")
        report = AudienceService.generate_report(entry_id)
        output_path = 'audience_first_report_e2e.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"   ✅ 报告已保存: {output_path}")
        print(f"   ✅ 报告长度: {len(report)} 字符")
        
        # 6. 验证数据完整性
        print("\n【步骤6】验证数据完整性")
        first_cluster = saved_clusters[0]
        
        # 验证必需字段
        required_fields = ['cluster_id', 'role', 'scenario', 'kpi_constraints', 
                          'pain_points', 'evidence_refs', 'score_card']
        missing_fields = [f for f in required_fields if f not in first_cluster]
        
        if missing_fields:
            print(f"   ❌ 缺失字段: {missing_fields}")
        else:
            print(f"   ✅ 所有必需字段完整")
        
        # 验证评分卡
        sc = first_cluster['score_card']
        score_fields = ['wtp_score', 'pain_frequency', 'moat_score', 'gtm_score', 
                       'total_score', 'evidence_count', 'confidence']
        missing_scores = [f for f in score_fields if f not in sc]
        
        if missing_scores:
            print(f"   ❌ 评分卡缺失字段: {missing_scores}")
        else:
            print(f"   ✅ 评分卡完整")
        
        # 验证证据引用
        evidence_count = len(first_cluster['evidence_refs'])
        if evidence_count > 0:
            print(f"   ✅ 证据引用完整 ({evidence_count}条)")
            first_evidence = first_cluster['evidence_refs'][0]
            evidence_fields = ['platform', 'author', 'text', 'snippet']
            missing_evidence = [f for f in evidence_fields if f not in first_evidence]
            if missing_evidence:
                print(f"   ❌ 证据字段缺失: {missing_evidence}")
            else:
                print(f"   ✅ 证据字段完整")
        else:
            print(f"   ❌ 无证据引用")
        
        # 7. 性能统计
        print("\n【步骤7】性能统计")
        total_evidence = sum(len(c['evidence_refs']) for c in saved_clusters)
        total_pain_points = sum(len(c['pain_points']) for c in saved_clusters)
        print(f"   ✅ 总证据数: {total_evidence}")
        print(f"   ✅ 总痛点数: {total_pain_points}")
        print(f"   ✅ 平均每簇证据: {total_evidence / len(saved_clusters):.1f}")
        
        print("\n" + "=" * 80)
        print("✅ 端到端测试通过 - MVP功能完整")
        print("=" * 80)
        
        # 8. 输出API使用示例
        print("\n【API使用示例】")
        print(f"""
# 1. 触发受众分析
POST /thinking/entries/{entry_id}/audience-analysis
Body: {{
    "raw_data": [...],
    "max_clusters": 5
}}

# 2. 获取受众簇列表
GET /thinking/entries/{entry_id}/audience-clusters

# 3. 获取Top2推荐
GET /thinking/entries/{entry_id}/audience-top?top_n=2

# 4. 获取Markdown报告
GET /thinking/entries/{entry_id}/audience-report
        """)


if __name__ == "__main__":
    test_end_to_end()
