"""
Thinking System 集成测试
测试完整的创建→评估→路由流程
"""
import sys
sys.path.insert(0, '.')

from tests.test_helpers import create_test_app, get_authenticated_client
from thinking.services.entry_service import EntryService
from thinking.services.gate_service import GateService
from thinking.services.routing_service import RoutingService
from thinking.models.thinking_entry import ThinkingEntry
from database import db

class TestThinkingFlow:
    """完整流程集成测试"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.app = create_test_app()
        self.client = get_authenticated_client(self.app)
    
    def test_create_entry_with_context(self):
        """测试在 Flask context 中创建条目"""
        with self.app.app_context():
            # 准备数据
            user_id = 1
            data = {
                'title': '测试创业想法',
                'signal': '市场需求强烈',
                'target_segment': 'small team',
                'problem': '现有解决方案复杂',
                'hypothesis': '简化方案可行',
            }
            
            # 执行: 创建条目
            entry = EntryService.create_entry(user_id, data)
            
            # 验证
            assert entry is not None
            assert entry.title == '测试创业想法'
            assert entry.user_id == user_id
            
            print("✅ test_create_entry_with_context - 创建成功")
    
    def test_gate_evaluation_with_context(self):
        """测试在 Flask context 中进行 Gate 评估"""
        with self.app.app_context():
            # 准备: 创建条目
            user_id = 1
            data = {'title': 'Gate 测试条目'}
            entry = EntryService.create_entry(user_id, data)
            
            # 准备: Gate 输入
            user_inputs = [
                'no',  # 人性依赖: 无
                'self_evident',  # 价值自证: 是
                'falsifiable',  # 反馈清洁: 可证伪
                'no_push'  # 角色消耗: 无需推动
            ]
            
            # 执行: Gate 评估
            gate_service = GateService()
            result = gate_service.evaluate(entry.id, user_inputs)
            
            # 验证
            assert result['decision'] == 'pass'
            assert result['fail_level'] is None
            assert len(result['results']) == 4
            
            print(f"✅ test_gate_evaluation_with_context - 决策: {result['decision']}")
    
    def test_routing_decision_flow(self):
        """测试路由决策流程 - 仅测试逻辑，不访问数据库"""
        # 准备: 模拟条目
        class MockEntry:
            id = 1
            target_segment = 'small team'
            dependencies = 'dep1, dep2'
            evidence_needed = 'some evidence'
            constraints = None
        
        entry = MockEntry()
        
        # 执行: 测试影响评估 (不需要数据库)
        impact = RoutingService._assess_impact(entry)
        assert impact in ['small', 'medium', 'large']
        
        # 执行: 测试依赖计数
        dep_count = RoutingService._count_dependencies(entry)
        assert dep_count == 2
        
        print(f"✅ test_routing_decision_flow - 影响: {impact}, 依赖: {dep_count}")
    
    def test_database_transaction_rollback(self):
        """测试数据库事务回滚"""
        with self.app.app_context():
            # 准备: 创建条目
            user_id = 1
            data = {'title': '事务测试条目'}
            entry = EntryService.create_entry(user_id, data)
            entry_id = entry.id
            
            # 模拟失败的 Gate 评估
            user_inputs = [
                'strong_dependency',  # 人性依赖: 强依赖 (会失败)
                'self_evident',
                'falsifiable',
                'no_push'
            ]
            
            gate_service = GateService()
            result = gate_service.evaluate(entry_id, user_inputs)
            
            # 验证: 评估失败
            assert result['decision'] == 'fail'
            assert result['fail_level'] == 1
            
            # 验证: 条目状态已更新
            entry = ThinkingEntry.query.get(entry_id)
            assert entry.status == '已否决'
            
            print("✅ test_database_transaction_rollback - 事务正确处理")
    
    def test_complete_workflow(self):
        """测试完整工作流: 创建→评估→路由"""
        with self.app.app_context():
            # 1. 创建条目
            user_id = 1
            data = {
                'title': '完整流程测试',
                'target_segment': 'medium company',
                'dependencies': 'dep1, dep2, dep3',
            }
            entry = EntryService.create_entry(user_id, data)
            
            # 2. Gate 评估 (通过)
            user_inputs = ['no', 'self_evident', 'falsifiable', 'no_push']
            gate_service = GateService()
            gate_result = gate_service.evaluate(entry.id, user_inputs)
            
            assert gate_result['decision'] == 'pass'
            
            # 3. 路由决策
            impact = RoutingService._assess_impact(entry)
            dep_count = RoutingService._count_dependencies(entry)
            
            assert impact == 'medium'
            assert dep_count == 3
            
            # 4. 验证状态
            entry = ThinkingEntry.query.get(entry.id)
            assert entry.status == '评估中'
            
            print("✅ test_complete_workflow - 完整流程通过")

if __name__ == '__main__':
    print("=" * 60)
    print("🧪 Thinking System 集成测试 (完整版)")
    print("=" * 60)
    
    test = TestThinkingFlow()
    
    print("\n📋 运行测试:")
    
    test.setup_method()
    test.test_create_entry_with_context()
    
    test.setup_method()
    test.test_gate_evaluation_with_context()
    
    test.test_routing_decision_flow()
    
    test.setup_method()
    test.test_database_transaction_rollback()
    
    test.setup_method()
    test.test_complete_workflow()
    
    print("\n" + "=" * 60)
    print("✅ 所有集成测试通过")
    print("=" * 60)
