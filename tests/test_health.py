"""
健康检查端点测试
"""
import sys
sys.path.insert(0, '.')
import time

from tests.test_helpers import create_test_app

class TestHealthCheck:
    """健康检查测试"""
    
    def setup_method(self):
        """设置测试环境"""
        self.app = create_test_app()
        self.client = self.app.test_client()
    
    def test_health_endpoint(self):
        """测试 /health 端点"""
        start = time.perf_counter()
        response = self.client.get('/health')
        end = time.perf_counter()
        
        response_time = (end - start) * 1000  # ms
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert response_time < 100, f"响应时间 {response_time:.2f}ms > 100ms"
        
        print(f"✅ /health 端点正常 ({response_time:.2f}ms)")
    
    def test_ready_endpoint(self):
        """测试 /ready 端点"""
        with self.app.app_context():
            start = time.perf_counter()
            response = self.client.get('/ready')
            end = time.perf_counter()
            
            response_time = (end - start) * 1000  # ms
            
            assert response.status_code in [200, 503]
            data = response.get_json()
            assert 'status' in data
            assert 'checks' in data
            assert 'database' in data['checks']
            assert response_time < 100, f"响应时间 {response_time:.2f}ms > 100ms"
            
            print(f"✅ /ready 端点正常 ({response_time:.2f}ms, 状态: {data['status']})")

if __name__ == '__main__':
    print("=" * 60)
    print("🏥 健康检查端点测试")
    print("=" * 60)
    
    test = TestHealthCheck()
    
    print("\n📋 运行测试:")
    test.setup_method()
    test.test_health_endpoint()
    
    test.setup_method()
    test.test_ready_endpoint()
    
    print("\n" + "=" * 60)
    print("✅ 健康检查测试通过")
    print("=" * 60)
