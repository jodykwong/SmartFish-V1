"""
测试受众聚类引擎
"""
import json
from audience_clustering_engine import AudienceClusteringEngine


def test_clustering():
    """测试聚类功能"""
    # 加载测试数据
    with open("prototype/test_data.json", 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # 初始化引擎
    engine = AudienceClusteringEngine()
    
    # 执行聚类
    clusters = engine.cluster(raw_data, max_clusters=5)
    
    # 输出结果
    print("=" * 80)
    print("受众聚类结果（完整版）")
    print("=" * 80)
    
    for i, cluster in enumerate(clusters, 1):
        result = cluster.to_dict()
        print(f"\n【簇{i}】{result['role']} - {result['scenario']} - {result['kpi_constraints'][0]}")
        print(f"  簇ID: {result['cluster_id']}")
        print(f"  证据数量: {result['score_card']['evidence_count']}")
        print(f"  核心痛点: {result['pain_points'][:2]}")
        print(f"  土办法: {result['workarounds']}")
        print(f"  付费信号: {result['payment_signals']}")
        print(f"  评分详情:")
        print(f"    - WTP: {result['score_card']['wtp_score']}")
        print(f"    - 痛苦高频: {result['score_card']['pain_frequency']}")
        print(f"    - Moat: {result['score_card']['moat_score']}")
        print(f"    - GTM: {result['score_card']['gtm_score']}")
        print(f"    - 总分: {result['score_card']['total_score']}")
        print(f"    - 置信度: {result['score_card']['confidence']}%")
    
    print("\n" + "=" * 80)
    print("✅ 聚类引擎测试通过")
    print("=" * 80)
    
    return clusters


if __name__ == "__main__":
    test_clustering()
