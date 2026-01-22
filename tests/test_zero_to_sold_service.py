import pytest
from thinking.services.zero_to_sold_service import ZeroToSoldService

class TestZeroToSoldService:
    
    def test_score_problem_intensity_critical(self):
        """测试重要且紧急（20-25分）"""
        result = ZeroToSoldService.score_problem_intensity(5, 5)
        
        assert result['score'] == 25
        assert result['importance'] == 5
        assert result['urgency'] == 5
        assert result['priority'] == '重要且紧急'
        assert result['action'] == '优先处理'
    
    def test_score_problem_intensity_important(self):
        """测试重要不紧急（15-19分）"""
        result = ZeroToSoldService.score_problem_intensity(5, 3)
        
        assert result['score'] == 15
        assert result['priority'] == '重要不紧急'
        assert result['action'] == '计划处理'
    
    def test_score_problem_intensity_urgent(self):
        """测试紧急不重要（10-14分）"""
        result = ZeroToSoldService.score_problem_intensity(2, 5)
        
        assert result['score'] == 10
        assert result['priority'] == '紧急不重要'
        assert result['action'] == '委托或快速处理'
    
    def test_score_problem_intensity_low(self):
        """测试不重要不紧急（<10分）"""
        result = ZeroToSoldService.score_problem_intensity(2, 2)
        
        assert result['score'] == 4
        assert result['priority'] == '不重要不紧急'
        assert result['action'] == '考虑放弃'
    
    def test_score_boundary_values(self):
        """测试边界值"""
        # 最小值
        result_min = ZeroToSoldService.score_problem_intensity(1, 1)
        assert result_min['score'] == 1
        
        # 最大值
        result_max = ZeroToSoldService.score_problem_intensity(5, 5)
        assert result_max['score'] == 25
        
        # 边界20分
        result_20 = ZeroToSoldService.score_problem_intensity(4, 5)
        assert result_20['score'] == 20
        assert result_20['priority'] == '重要且紧急'
    
    def test_slugify(self):
        """测试slug转换"""
        assert ZeroToSoldService._slugify('Hello World') == 'hello-world'
        assert ZeroToSoldService._slugify('Test-123') == 'test-123'
        assert ZeroToSoldService._slugify('中文测试') == ''
        
        # 测试长度截断
        long_text = 'a' * 100
        assert len(ZeroToSoldService._slugify(long_text)) == 50
