#!/usr/bin/env python3
"""
简单测试运行器 - 绕过 pytest/ROS 冲突
"""
import sys
sys.path.insert(0, '.')

from tests.test_gate_filters import TestGateFilters
from tests.test_routing_service import TestRoutingService
from tests.test_thinking_flow import TestThinkingFlow
from tests.test_security import TestSecurity
from tests.test_performance import TestPerformance
from tests.test_health import TestHealthCheck
from tests.test_operations import TestOperations

def run_tests():
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("🧪 SmartFish 单元测试运行器")
    print("=" * 60)
    
    # Gate Filters 测试
    print("\n📋 Gate Filters 测试:")
    test_gate = TestGateFilters()
    
    tests = [
        ('test_human_dependency_fail', test_gate.test_human_dependency_fail),
        ('test_human_dependency_warning', test_gate.test_human_dependency_warning),
        ('test_human_dependency_pass', test_gate.test_human_dependency_pass),
        ('test_value_self_evident_fail', test_gate.test_value_self_evident_fail),
        ('test_feedback_clean_fail', test_gate.test_feedback_clean_fail),
        ('test_role_cost_warning', test_gate.test_role_cost_warning),
    ]
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # Routing Service 测试
    print("\n📋 Routing Service 测试:")
    test_routing = TestRoutingService()
    
    tests = [
        ('test_assess_impact', test_routing.test_assess_impact),
        ('test_count_dependencies', test_routing.test_count_dependencies),
    ]
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # Thinking Flow 集成测试
    print("\n📋 Thinking Flow 集成测试:")
    test_flow = TestThinkingFlow()
    
    tests = [
        ('test_create_entry_with_context', lambda: (test_flow.setup_method(), test_flow.test_create_entry_with_context())[1]),
        ('test_gate_evaluation_with_context', lambda: (test_flow.setup_method(), test_flow.test_gate_evaluation_with_context())[1]),
        ('test_routing_decision_flow', test_flow.test_routing_decision_flow),
        ('test_database_transaction_rollback', lambda: (test_flow.setup_method(), test_flow.test_database_transaction_rollback())[1]),
        ('test_complete_workflow', lambda: (test_flow.setup_method(), test_flow.test_complete_workflow())[1]),
    ]
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # 安全测试
    print("\n📋 安全测试:")
    test_security = TestSecurity()
    
    tests = [
        ('test_xss_protection', test_security.test_xss_protection),
        ('test_sql_injection_protection', test_security.test_sql_injection_protection),
        ('test_input_validation_title_length', test_security.test_input_validation_title_length),
        ('test_input_validation_empty_string', test_security.test_input_validation_empty_string),
        ('test_unicode_handling', test_security.test_unicode_handling),
        ('test_special_characters', test_security.test_special_characters),
        ('test_rate_limiting_config', test_security.test_rate_limiting_config),
    ]
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # 性能测试
    print("\n📋 性能基准测试:")
    test_perf = TestPerformance()
    
    tests = [
        ('test_routing_assessment_performance', test_perf.test_routing_assessment_performance),
        ('test_gate_filter_performance', test_perf.test_gate_filter_performance),
        ('test_dependency_counting_performance', test_perf.test_dependency_counting_performance),
    ]
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # 健康检查测试
    print("\n📋 健康检查测试:")
    test_health = TestHealthCheck()
    
    tests = [
        ('test_health_endpoint', lambda: (test_health.setup_method(), test_health.test_health_endpoint())[1]),
        ('test_ready_endpoint', lambda: (test_health.setup_method(), test_health.test_ready_endpoint())[1]),
    ]
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # 运维功能测试
    print("\n📋 运维功能测试:")
    test_ops = TestOperations()
    
    tests = [
        ('test_logging_config', test_ops.test_logging_config),
        ('test_monitoring_config', test_ops.test_monitoring_config),
        ('test_docker_config', test_ops.test_docker_config),
    ]
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # 总结
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(run_tests())
