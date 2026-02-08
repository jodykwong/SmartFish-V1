"""
Audience First 回归测试套件
完整功能验证
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


def test_regression():
    """回归测试"""
    app = create_test_app()
    
    with app.app_context():
        db.create_all()
        
        print("=" * 80)
        print("Audience First 回归测试套件")
        print("=" * 80)
        
        # 准备测试数据
        with open('prototype/test_data.json', 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        entry_id = 2000  # 新的entry_id避免冲突
        
        test_results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }
        
        # ==================== 测试1: 受众聚类 ====================
        print("\n【测试1】受众聚类引擎")
        try:
            clusters = AudienceService.analyze_audiences(entry_id, raw_data, max_clusters=5)
            
            # 验证点
            assert len(clusters) > 0, "应该生成至少1个受众簇"
            assert all('cluster_id' in c for c in clusters), "每个簇应该有cluster_id"
            assert all('role' in c for c in clusters), "每个簇应该有role"
            assert all('scenario' in c for c in clusters), "每个簇应该有scenario"
            assert all('score_card' in c for c in clusters), "每个簇应该有score_card"
            
            print(f"   ✅ 通过 - 生成{len(clusters)}个受众簇")
            test_results["passed"] += 1
        except Exception as e:
            print(f"   ❌ 失败 - {str(e)}")
            test_results["failed"] += 1
            test_results["errors"].append(f"测试1: {str(e)}")
        
        # ==================== 测试2: 数据持久化 ====================
        print("\n【测试2】数据库持久化")
        try:
            saved_clusters = AudienceService.get_clusters_by_entry(entry_id)
            
            # 验证点
            assert len(saved_clusters) > 0, "应该能查询到保存的簇"
            assert len(saved_clusters) == len(clusters), "保存的簇数量应该一致"
            
            # 验证证据引用
            first_cluster = saved_clusters[0]
            assert 'evidence_refs' in first_cluster, "应该有证据引用"
            assert len(first_cluster['evidence_refs']) > 0, "应该有至少1条证据"
            
            print(f"   ✅ 通过 - 查询到{len(saved_clusters)}个簇，证据完整")
            test_results["passed"] += 1
        except Exception as e:
            print(f"   ❌ 失败 - {str(e)}")
            test_results["failed"] += 1
            test_results["errors"].append(f"测试2: {str(e)}")
        
        # ==================== 测试3: Top N查询 ====================
        print("\n【测试3】Top N查询")
        try:
            top_clusters = AudienceService.get_top_clusters(entry_id, top_n=2)
            
            # 验证点
            assert len(top_clusters) <= 2, "Top2应该最多返回2个簇"
            assert len(top_clusters) > 0, "应该至少返回1个簇"
            
            # 验证排序
            if len(top_clusters) == 2:
                score1 = top_clusters[0]['score_card']['total_score']
                score2 = top_clusters[1]['score_card']['total_score']
                assert score1 >= score2, "应该按总分降序排列"
            
            print(f"   ✅ 通过 - Top2查询正常，排序正确")
            test_results["passed"] += 1
        except Exception as e:
            print(f"   ❌ 失败 - {str(e)}")
            test_results["failed"] += 1
            test_results["errors"].append(f"测试3: {str(e)}")
        
        # ==================== 测试4: 评分机制 ====================
        print("\n【测试4】评分机制")
        try:
            first_cluster = saved_clusters[0]
            sc = first_cluster['score_card']
            
            # 验证点
            assert 'wtp_score' in sc, "应该有WTP评分"
            assert 'pain_frequency' in sc, "应该有痛苦高频评分"
            assert 'moat_score' in sc, "应该有Moat评分"
            assert 'gtm_score' in sc, "应该有GTM评分"
            assert 'total_score' in sc, "应该有总分"
            assert 'confidence' in sc, "应该有置信度"
            
            # 验证总分计算
            calculated_total = sc['wtp_score'] + sc['pain_frequency'] + sc['moat_score'] + sc['gtm_score']
            assert abs(calculated_total - sc['total_score']) < 0.01, "总分计算应该正确"
            
            print(f"   ✅ 通过 - 评分卡完整，总分计算正确")
            test_results["passed"] += 1
        except Exception as e:
            print(f"   ❌ 失败 - {str(e)}")
            test_results["failed"] += 1
            test_results["errors"].append(f"测试4: {str(e)}")
        
        # ==================== 测试5: 报告生成 ====================
        print("\n【测试5】报告生成")
        try:
            report = AudienceService.generate_report(entry_id)
            
            # 验证点
            assert len(report) > 0, "报告不应该为空"
            assert "# Audience First 分析报告" in report, "应该有报告标题"
            assert "执行摘要" in report, "应该有执行摘要"
            assert "受众簇分析" in report, "应该有受众簇分析"
            assert "Top2 推荐" in report, "应该有Top2推荐"
            assert "90天验证计划" in report, "应该有验证计划"
            
            print(f"   ✅ 通过 - 报告生成成功，长度{len(report)}字符")
            test_results["passed"] += 1
        except Exception as e:
            print(f"   ❌ 失败 - {str(e)}")
            test_results["failed"] += 1
            test_results["errors"].append(f"测试5: {str(e)}")
        
        # ==================== 测试6: ForumEngine辩论 ====================
        print("\n【测试6】ForumEngine辩论")
        try:
            debates = AudienceService.debate_clusters(entry_id, top_n=2)
            
            # 验证点
            assert len(debates) > 0, "应该生成至少1个辩论结果"
            assert len(debates) <= 2, "Top2辩论应该最多2个"
            
            # 验证辩论结构
            first_debate = debates[0]
            assert 'support' in first_debate, "应该有支持方"
            assert 'oppose' in first_debate, "应该有反对方"
            assert 'decision' in first_debate, "应该有主持人裁决"
            
            # 验证决策
            decision = first_debate['decision']
            assert 'decision' in decision, "应该有决策结果"
            assert decision['decision'] in ['proceed', 'hold', 'reject'], "决策应该是有效值"
            assert 'uncertainties' in decision, "应该有不确定性列表"
            assert 'next_steps' in decision, "应该有下一步行动"
            
            print(f"   ✅ 通过 - 辩论生成成功，裁决为{decision['decision']}")
            test_results["passed"] += 1
        except Exception as e:
            print(f"   ❌ 失败 - {str(e)}")
            test_results["failed"] += 1
            test_results["errors"].append(f"测试6: {str(e)}")
        
        # ==================== 测试7: 数据完整性 ====================
        print("\n【测试7】数据完整性")
        try:
            # 验证痛点提取
            pain_points_count = sum(len(c['pain_points']) for c in saved_clusters)
            assert pain_points_count > 0, "应该提取到痛点"
            
            # 验证证据引用
            evidence_count = sum(len(c['evidence_refs']) for c in saved_clusters)
            assert evidence_count == len(raw_data), "证据数量应该等于原始数据数量"
            
            # 验证证据字段
            first_evidence = saved_clusters[0]['evidence_refs'][0]
            assert 'platform' in first_evidence, "证据应该有platform"
            assert 'author' in first_evidence, "证据应该有author"
            assert 'text' in first_evidence, "证据应该有text"
            assert 'snippet' in first_evidence, "证据应该有snippet"
            
            print(f"   ✅ 通过 - 痛点{pain_points_count}个，证据{evidence_count}条，字段完整")
            test_results["passed"] += 1
        except Exception as e:
            print(f"   ❌ 失败 - {str(e)}")
            test_results["failed"] += 1
            test_results["errors"].append(f"测试7: {str(e)}")
        
        # ==================== 测试8: 边界条件 ====================
        print("\n【测试8】边界条件")
        try:
            # 测试空数据
            empty_clusters = AudienceService.get_clusters_by_entry(9999)
            assert len(empty_clusters) == 0, "不存在的entry应该返回空列表"
            
            # 测试空报告
            empty_report = AudienceService.generate_report(9999)
            assert "暂无受众分析数据" in empty_report, "空数据应该返回提示信息"
            
            # 测试空辩论
            empty_debates = AudienceService.debate_clusters(9999)
            assert len(empty_debates) == 0, "空数据应该返回空辩论列表"
            
            print(f"   ✅ 通过 - 边界条件处理正确")
            test_results["passed"] += 1
        except Exception as e:
            print(f"   ❌ 失败 - {str(e)}")
            test_results["failed"] += 1
            test_results["errors"].append(f"测试8: {str(e)}")
        
        # ==================== 测试总结 ====================
        print("\n" + "=" * 80)
        print("回归测试总结")
        print("=" * 80)
        print(f"✅ 通过: {test_results['passed']}")
        print(f"❌ 失败: {test_results['failed']}")
        print(f"总计: {test_results['passed'] + test_results['failed']}")
        
        if test_results['failed'] > 0:
            print("\n失败详情:")
            for error in test_results['errors']:
                print(f"  - {error}")
        
        # 计算通过率
        total = test_results['passed'] + test_results['failed']
        pass_rate = (test_results['passed'] / total * 100) if total > 0 else 0
        
        print(f"\n通过率: {pass_rate:.1f}%")
        
        if pass_rate == 100:
            print("\n" + "=" * 80)
            print("🎉 所有测试通过！Audience First 功能完整且稳定")
            print("=" * 80)
        else:
            print("\n" + "=" * 80)
            print("⚠️  部分测试失败，需要修复")
            print("=" * 80)
        
        return test_results


if __name__ == "__main__":
    results = test_regression()
    sys.exit(0 if results['failed'] == 0 else 1)
