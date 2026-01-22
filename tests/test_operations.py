"""
运维功能测试
"""
import sys
sys.path.insert(0, '.')

class TestOperations:
    """运维功能测试"""
    
    def test_logging_config(self):
        """测试日志配置"""
        from logging_config import JSONFormatter, setup_logging
        
        assert JSONFormatter is not None
        assert callable(setup_logging)
        print("✅ 日志配置存在")
    
    def test_monitoring_config(self):
        """测试监控配置"""
        from monitoring import init_metrics
        
        assert callable(init_metrics)
        print("✅ 监控配置存在")
    
    def test_docker_config(self):
        """测试 Docker 配置"""
        import os
        
        assert os.path.exists('docker-compose.prod.yml')
        assert os.path.exists('.env.prod.template')
        assert os.path.exists('deploy.sh')
        assert os.access('deploy.sh', os.X_OK)
        print("✅ Docker 配置完整")

if __name__ == '__main__':
    print("=" * 60)
    print("⚙️  运维功能测试")
    print("=" * 60)
    
    test = TestOperations()
    
    print("\n📋 运行测试:")
    test.test_logging_config()
    test.test_monitoring_config()
    test.test_docker_config()
    
    print("\n" + "=" * 60)
    print("✅ 运维功能测试通过")
    print("=" * 60)
