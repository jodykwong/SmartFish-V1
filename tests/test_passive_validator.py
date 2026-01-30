"""
PassiveSignalMiner 和 PassiveValidator 单元测试

Issue #3 修复: 添加完整的单元测试覆盖
"""

import pytest
from user_validator import (
    PassiveSignalMiner,
    PassiveValidator,
    PassiveSignal,
    SignalResult,
    ValidationSummary
)
from bmad_adapter import PainPoint


class TestPassiveSignalMiner:
    """被动信号挖掘器测试"""
    
    def setup_method(self):
        self.miner = PassiveSignalMiner()
        
    # === 基本功能测试 ===
    
    def test_mine_signals_empty_content(self):
        """测试空内容输入"""
        result = self.miner.mine_signals("")
        assert result["payment_willingness"] == 0.0
        assert result["desperation_level"] == 0.0
        assert result["solution_seeking"] == 0.0
        assert len(result["payment_signals"]) == 0
        
    def test_mine_signals_no_match(self):
        """测试无匹配内容"""
        result = self.miner.mine_signals("今天天气真好")
        assert result["payment_willingness"] == 0.0
        assert result["desperation_level"] == 0.0
        
    def test_mine_signals_payment_detection(self):
        """测试付费意愿信号检测"""
        result = self.miner.mine_signals("我愿意付费购买这个功能")
        assert result["payment_willingness"] > 0.8
        assert len(result["payment_signals"]) >= 1
        assert result["payment_signals"][0].signal_type == "payment"
        
    def test_mine_signals_desperation_detection(self):
        """测试绝望程度信号检测"""
        result = self.miner.mine_signals("这个问题快把我逼死了，救命啊")
        assert result["desperation_level"] > 0.9
        assert len(result["desperation_signals"]) >= 2
        
    def test_mine_signals_solution_seeking_detection(self):
        """测试求解意愿信号检测"""
        result = self.miner.mine_signals("有没有能解决这个问题的工具？求推荐！")
        assert result["solution_seeking"] > 0.7
        assert len(result["solution_signals"]) >= 2
        
    def test_mine_signals_early_adopter_detection(self):
        """测试早期用户特征检测"""
        result = self.miner.mine_signals("我想试用一下beta版本")
        assert result["is_early_adopter"] is True
        
    # === Issue #1 修复验证: 多匹配上下文测试 ===
    
    def test_multiple_matches_get_correct_context(self):
        """测试多匹配项获取各自正确的上下文"""
        content = "开头：救命啊！中间一些普通文字填充。结尾：跪求帮忙！"
        result = self.miner.mine_signals(content)
        
        # 应该有两个绝望信号
        signals = result["desperation_signals"]
        assert len(signals) >= 2
        
        # 每个信号应该有不同的上下文
        contexts = [s.context for s in signals]
        assert "救命" in contexts[0] or "救命" in contexts[1]
        assert "跪求" in contexts[0] or "跪求" in contexts[1]
        
    # === Issue #2 修复验证: 长内容截断测试 ===
    
    def test_long_content_truncation(self):
        """测试超长内容被正确截断"""
        # 创建超过10KB的内容
        long_content = "a" * 5000 + "救命" + "b" * 6000
        result = self.miner.mine_signals(long_content)
        # 应该检测到信号（在前10KB内）
        assert result["desperation_level"] > 0
        
    def test_very_long_content_no_crash(self):
        """测试超长内容不会崩溃"""
        very_long = "愿意付费" * 10000  # 40KB内容
        result = self.miner.mine_signals(very_long)
        # 不应该崩溃，应该有结果
        assert "payment_willingness" in result
        
    # === 边缘情况测试 ===
    
    def test_special_characters(self):
        """测试包含特殊字符的内容"""
        result = self.miner.mine_signals("👍救命🔥愿意付费💰")
        assert result["desperation_level"] > 0
        assert result["payment_willingness"] > 0
        
    def test_unicode_content(self):
        """测试Unicode内容"""
        result = self.miner.mine_signals("日本語: 救命です！中文: 跪求帮忙")
        assert result["desperation_level"] > 0
        
    def test_platform_and_url_recorded(self):
        """测试平台和URL被正确记录"""
        result = self.miner.mine_signals(
            "愿意付费", 
            platform="xiaohongshu", 
            url="https://example.com"
        )
        signal = result["payment_signals"][0]
        assert signal.source_platform == "xiaohongshu"
        assert signal.source_url == "https://example.com"


class TestPassiveSignalMinerBatch:
    """批量挖掘测试"""
    
    def setup_method(self):
        self.miner = PassiveSignalMiner()
        
    def test_mine_batch_empty_list(self):
        """测试空列表输入"""
        result = self.miner.mine_batch([], "test_pp")
        assert result.total_content_count == 0
        assert result.payment_willingness_score == 0.0
        
    def test_mine_batch_multiple_contents(self):
        """测试多内容批量挖掘"""
        contents = [
            {"text": "愿意付费解决", "platform": "weibo"},
            {"text": "救命啊太难了", "platform": "zhihu"},
            {"text": "求推荐工具", "platform": "xiaohongshu"},
        ]
        result = self.miner.mine_batch(contents, "pp_1")
        assert result.total_content_count == 3
        assert result.payment_willingness_score > 0
        assert result.desperation_level > 0
        assert len(result.solution_seeking_signals) > 0


class TestPassiveValidator:
    """被动验证器测试"""
    
    def setup_method(self):
        self.validator = PassiveValidator()
        self.test_pain_point = PainPoint(
            id="test_pp_1",
            title="测试痛点",
            description="测试描述",
            domain="test",
            keywords=["test"]
        )
        
    def test_validate_insufficient_content(self):
        """测试内容不足的情况"""
        contents = [
            {"text": "愿意付费", "platform": "weibo"}
        ]
        summary = self.validator.validate_from_content(self.test_pain_point, contents)
        assert summary.is_validated is False  # 内容数不足10
        assert summary.confidence_level == "低"
        
    def test_validate_sufficient_signals(self):
        """测试信号充足的情况"""
        contents = [
            {"text": "愿意付费解决这个问题", "platform": "weibo"},
            {"text": "救命啊快崩溃了", "platform": "zhihu"},
            {"text": "多少钱能买到解决方案", "platform": "xiaohongshu"},
            {"text": "花钱也愿意解决", "platform": "weibo"},
            {"text": "跪求推荐工具", "platform": "zhihu"},
            {"text": "太难了受不了", "platform": "xiaohongshu"},
            {"text": "愿意付费使用", "platform": "weibo"},
            {"text": "急需解决这个问题", "platform": "zhihu"},
            {"text": "有没有能解决的工具", "platform": "xiaohongshu"},
            {"text": "这个问题逼死我了", "platform": "weibo"},
        ]
        summary = self.validator.validate_from_content(self.test_pain_point, contents)
        assert summary.total_content_analyzed == 10
        assert summary.desperation_level > 0.5
        assert summary.payment_willingness_score > 0.5
        
    def test_calculate_pain_point_score(self):
        """测试痛点评分计算"""
        contents = [
            {"text": "愿意付费解决", "platform": "weibo"},
            {"text": "救命啊", "platform": "zhihu"},
        ]
        self.validator.validate_from_content(self.test_pain_point, contents)
        score = self.validator.calculate_pain_point_score(self.test_pain_point.id)
        assert 0 <= score <= 1
        
    def test_get_validation_report(self):
        """测试验证报告生成"""
        contents = [{"text": "愿意付费", "platform": "weibo"}]
        self.validator.validate_from_content(self.test_pain_point, contents)
        report = self.validator.get_validation_report()
        
        assert "total_pain_points_analyzed" in report
        assert "validated_pain_points" in report
        assert "summaries" in report
        assert "scores" in report
        assert "timestamp" in report


class TestValidationSummary:
    """验证摘要测试"""
    
    def test_to_dict(self):
        """测试序列化"""
        summary = ValidationSummary(
            pain_point_id="pp_1",
            total_content_analyzed=10,
            signal_density=0.5,
            payment_willingness_score=0.8,
            desperation_level=0.7,
            is_validated=True,
            confidence_level="中",
            key_insights=["test insight"]
        )
        result = summary.to_dict()
        assert result["pain_point_id"] == "pp_1"
        assert result["is_validated"] is True
        assert "key_insights" in result


class TestSignalResult:
    """信号结果测试"""
    
    def test_to_dict(self):
        """测试序列化"""
        signal = PassiveSignal(
            signal_type="payment",
            signal_text="愿意付费",
            signal_score=0.9,
            source_platform="weibo"
        )
        result = SignalResult(
            pain_point_id="pp_1",
            total_content_count=1,
            payment_signals=[signal],
            desperation_signals=[],
            solution_seeking_signals=[],
            payment_willingness_score=0.9,
            desperation_level=0.0,
            is_early_adopter_target=False
        )
        serialized = result.to_dict()
        assert serialized["pain_point_id"] == "pp_1"
        assert len(serialized["payment_signals"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
