"""
测试报告生成
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


def test_report_generation():
    """测试报告生成"""
    app = create_test_app()
    
    with app.app_context():
        entry_id = 999
        
        print("=" * 80)
        print("测试报告生成")
        print("=" * 80)
        
        # 生成报告
        print("\n生成Audience First报告...")
        report = AudienceService.generate_report(entry_id)
        
        # 保存报告
        output_path = 'audience_first_report_test.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 报告已生成: {output_path}")
        print(f"✅ 报告长度: {len(report)} 字符")
        
        # 显示报告预览
        print("\n" + "=" * 80)
        print("报告预览（前500字符）:")
        print("=" * 80)
        print(report[:500])
        print("...")
        
        print("\n" + "=" * 80)
        print("✅ 报告生成测试通过")
        print("=" * 80)


if __name__ == "__main__":
    test_report_generation()
