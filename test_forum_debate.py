"""
测试ForumEngine辩论
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


def test_debate():
    """测试辩论功能"""
    app = create_test_app()
    
    with app.app_context():
        entry_id = 1000
        
        print("=" * 80)
        print("ForumEngine 辩论测试")
        print("=" * 80)
        
        # 执行辩论
        print("\n【执行辩论】对Top2受众簇进行多智能体评审...")
        debates = AudienceService.debate_clusters(entry_id, top_n=2)
        
        print(f"\n✅ 完成 {len(debates)} 个受众簇的辩论")
        
        # 显示辩论结果
        for i, debate in enumerate(debates, 1):
            print("\n" + "=" * 80)
            print(f"【辩论{i}】{debate['cluster_name']}")
            print("=" * 80)
            
            # 支持方
            support = debate['support']
            print(f"\n{support['icon']} {support['agent']}")
            print(f"   置信度: {support['confidence']:.0%}")
            print(f"   支持证据:")
            for evidence in support['support_evidence']:
                print(f"      - {evidence}")
            print(f"   核心优势:")
            for advantage in support['key_advantages']:
                print(f"      - {advantage}")
            
            # 反对方
            oppose = debate['oppose']
            print(f"\n{oppose['icon']} {oppose['agent']}")
            print(f"   置信度: {oppose['confidence']:.0%}")
            print(f"   反对证据:")
            for evidence in oppose['opposing_evidence']:
                print(f"      - {evidence}")
            print(f"   关键风险:")
            for risk in oppose['key_risks']:
                print(f"      - {risk}")
            
            # 主持人裁决
            decision = debate['decision']
            print(f"\n{decision['icon']} {decision['agent']}")
            print(f"   裁决: {decision['decision'].upper()}")
            print(f"   关键不确定性:")
            for uncertainty in decision['uncertainties']:
                print(f"      - {uncertainty}")
            print(f"   下一步行动:")
            for step in decision['next_steps']:
                print(f"      - {step}")
        
        # 保存辩论结果
        output_path = 'audience_debate_results.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(debates, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 80)
        print(f"✅ 辩论结果已保存: {output_path}")
        print("=" * 80)
        
        # 统计
        proceed_count = sum(1 for d in debates if d['decision']['decision'] == 'proceed')
        hold_count = sum(1 for d in debates if d['decision']['decision'] == 'hold')
        reject_count = sum(1 for d in debates if d['decision']['decision'] == 'reject')
        
        print(f"\n【辩论统计】")
        print(f"   继续 (proceed): {proceed_count}")
        print(f"   暂缓 (hold): {hold_count}")
        print(f"   拒绝 (reject): {reject_count}")
        
        print("\n" + "=" * 80)
        print("✅ ForumEngine辩论测试通过")
        print("=" * 80)


if __name__ == "__main__":
    test_debate()
