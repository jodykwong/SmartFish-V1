"""
性能基准测试
测量关键操作的性能
"""
import sys
sys.path.insert(0, '.')
import time

from thinking.services.routing_service import RoutingService
from thinking.services.gate_filters import HumanDependencyFilter, GateResult

class TestPerformance:
    """性能基准测试"""
    
    def test_routing_assessment_performance(self):
        """测试路由评估性能 - 目标 < 10ms"""
        class MockEntry:
            id = 1
            target_segment = 'medium company'
            dependencies = 'dep1, dep2, dep3'
            evidence_needed = 'evidence'
            constraints = 'some constraints'
        
        entry = MockEntry()
        
        # 预热
        for _ in range(10):
            RoutingService._assess_impact(entry)
        
        # 基准测试
        start = time.perf_counter()
        iterations = 1000
        
        for _ in range(iterations):
            RoutingService._assess_impact(entry)
        
        end = time.perf_counter()
        avg_time = (end - start) / iterations * 1000  # ms
        
        assert avg_time < 10, f"性能不达标: {avg_time:.3f}ms > 10ms"
        print(f"✅ 路由评估性能: {avg_time:.3f}ms (目标 < 10ms)")
    
    def test_gate_filter_performance(self):
        """测试 Gate 过滤器性能 - 目标 < 5ms"""
        filter_obj = HumanDependencyFilter()
        
        # 预热
        for _ in range(10):
            filter_obj.evaluate(None, 'no')
        
        # 基准测试
        start = time.perf_counter()
        iterations = 1000
        
        for _ in range(iterations):
            filter_obj.evaluate(None, 'no')
        
        end = time.perf_counter()
        avg_time = (end - start) / iterations * 1000  # ms
        
        assert avg_time < 5, f"性能不达标: {avg_time:.3f}ms > 5ms"
        print(f"✅ Gate 过滤器性能: {avg_time:.3f}ms (目标 < 5ms)")
    
    def test_dependency_counting_performance(self):
        """测试依赖计数性能 - 目标 < 1ms"""
        class MockEntry:
            dependencies = 'dep1, dep2, dep3, dep4, dep5'
        
        entry = MockEntry()
        
        # 预热
        for _ in range(10):
            RoutingService._count_dependencies(entry)
        
        # 基准测试
        start = time.perf_counter()
        iterations = 10000
        
        for _ in range(iterations):
            RoutingService._count_dependencies(entry)
        
        end = time.perf_counter()
        avg_time = (end - start) / iterations * 1000  # ms
        
        assert avg_time < 1, f"性能不达标: {avg_time:.3f}ms > 1ms"
        print(f"✅ 依赖计数性能: {avg_time:.3f}ms (目标 < 1ms)")

if __name__ == '__main__':
    print("=" * 60)
    print("⚡ 性能基准测试")
    print("=" * 60)
    
    test = TestPerformance()
    
    print("\n📋 运行性能测试:")
    test.test_routing_assessment_performance()
    test.test_gate_filter_performance()
    test.test_dependency_counting_performance()
    
    print("\n" + "=" * 60)
    print("✅ 所有性能基准达标")
    print("=" * 60)
