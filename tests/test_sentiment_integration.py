"""
情感分析模块集成测试

测试 EnhancedSentimentAnalyzer 和 SimpleSVMPredictor 的功能。
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSentimentAnalyzerImports:
    """测试导入功能"""
    
    def test_import_sentiment_analyzer(self):
        """测试导入 sentiment_analyzer 模块"""
        from sentiment_analyzer import EnhancedSentimentAnalyzer, SentimentMethod, SentimentResult
        assert EnhancedSentimentAnalyzer is not None
        assert SentimentMethod is not None
        assert SentimentResult is not None
        
    def test_import_svm_predictor(self):
        """测试导入 svm_predictor 模块"""
        from svm_predictor import SimpleSVMPredictor, get_svm_predictor
        assert SimpleSVMPredictor is not None
        assert get_svm_predictor is not None
        
    def test_import_convenience_functions(self):
        """测试导入便捷函数"""
        from sentiment_analyzer import (
            analyze_sentiment,
            calculate_sentiment_score,
            get_sentiment_analyzer
        )
        assert analyze_sentiment is not None
        assert calculate_sentiment_score is not None
        assert get_sentiment_analyzer is not None


class TestSentimentMethod:
    """测试情感分析方法枚举"""
    
    def test_method_values(self):
        """测试方法枚举值"""
        from sentiment_analyzer import SentimentMethod
        
        assert SentimentMethod.KEYWORD.value == "keyword"
        assert SentimentMethod.SVM.value == "svm"
        assert SentimentMethod.XGBOOST.value == "xgboost"
        assert SentimentMethod.ENSEMBLE.value == "ensemble"


class TestSentimentResult:
    """测试情感分析结果数据类"""
    
    def test_create_result(self):
        """测试创建结果"""
        from sentiment_analyzer import SentimentResult, SentimentMethod
        
        result = SentimentResult(
            score=0.8,
            label="正面",
            confidence=0.9,
            method=SentimentMethod.SVM
        )
        
        assert result.score == 0.8
        assert result.label == "正面"
        assert result.confidence == 0.9
        assert result.method == SentimentMethod.SVM


class TestEnhancedSentimentAnalyzer:
    """测试增强型情感分析器"""
    
    def test_analyzer_init(self):
        """测试分析器初始化"""
        from sentiment_analyzer import EnhancedSentimentAnalyzer, SentimentMethod
        
        # 禁用模型加载以加速测试
        analyzer = EnhancedSentimentAnalyzer(
            default_method=SentimentMethod.KEYWORD,
            load_models_on_init=False
        )
        
        assert analyzer is not None
        assert analyzer.default_method == SentimentMethod.KEYWORD
        
    def test_keyword_analysis(self):
        """测试关键词匹配分析"""
        from sentiment_analyzer import EnhancedSentimentAnalyzer, SentimentMethod
        
        analyzer = EnhancedSentimentAnalyzer(
            default_method=SentimentMethod.KEYWORD,
            load_models_on_init=False
        )
        
        # 测试负面文本
        result = analyzer.analyze("这个软件太垃圾了，经常崩溃")
        assert result.label == "负面"
        assert result.score < 0
        assert result.method == SentimentMethod.KEYWORD
        
        # 测试正面文本
        result = analyzer.analyze("非常好用，强烈推荐")
        assert result.label == "正面"
        assert result.score > 0
        
    def test_batch_analysis(self):
        """测试批量分析"""
        from sentiment_analyzer import EnhancedSentimentAnalyzer, SentimentMethod
        
        analyzer = EnhancedSentimentAnalyzer(
            default_method=SentimentMethod.KEYWORD,
            load_models_on_init=False
        )
        
        texts = ["好用", "难用", "一般"]
        results = analyzer.analyze_batch(texts)
        
        assert len(results) == 3
        
    def test_average_score(self):
        """测试平均得分计算"""
        from sentiment_analyzer import EnhancedSentimentAnalyzer, SentimentMethod
        
        analyzer = EnhancedSentimentAnalyzer(
            default_method=SentimentMethod.KEYWORD,
            load_models_on_init=False
        )
        
        texts = ["好用", "难用"]
        avg = analyzer.calculate_average_score(texts)
        
        assert isinstance(avg, float)
        assert -1 <= avg <= 1


class TestSVMAnalysis:
    """测试 SVM 模型分析（如果模型可用）"""
    
    def test_svm_model_loading(self):
        """测试 SVM 模型加载"""
        from sentiment_analyzer import EnhancedSentimentAnalyzer, SentimentMethod
        
        analyzer = EnhancedSentimentAnalyzer(
            default_method=SentimentMethod.ENSEMBLE,
            load_models_on_init=True
        )
        
        # 无论模型是否加载成功，分析器都应该能工作
        result = analyzer.analyze("这是一个测试文本")
        assert result is not None
        assert result.label in ["正面", "负面", "中性"]
        
    def test_fallback_to_keyword(self):
        """测试回退到关键词匹配"""
        from sentiment_analyzer import EnhancedSentimentAnalyzer, SentimentMethod
        
        # 使用不存在的模型目录
        analyzer = EnhancedSentimentAnalyzer(
            default_method=SentimentMethod.ENSEMBLE,
            model_dir="/nonexistent/path",
            load_models_on_init=True
        )
        
        # 应该回退到关键词匹配
        result = analyzer.analyze("这个软件太垃圾了")
        assert result is not None
        assert result.label == "负面"
        assert result.method == SentimentMethod.KEYWORD


class TestConvenienceFunctions:
    """测试便捷函数"""
    
    def test_analyze_sentiment(self):
        """测试 analyze_sentiment 函数"""
        from sentiment_analyzer import analyze_sentiment
        
        result = analyze_sentiment("好用")
        assert result is not None
        assert result.label in ["正面", "负面", "中性"]
        
    def test_calculate_sentiment_score(self):
        """测试 calculate_sentiment_score 函数"""
        from sentiment_analyzer import calculate_sentiment_score
        
        score = calculate_sentiment_score(["好用", "难用"])
        assert isinstance(score, float)
        assert -1 <= score <= 1


class TestBMADIntegration:
    """测试与 BMAD Adapter 的集成"""
    
    def test_bmad_adapter_sentiment(self):
        """测试 BMAD Adapter 使用增强情感分析"""
        from bmad_adapter import BMADPainPointDiscovery
        
        adapter = BMADPainPointDiscovery()
        assert adapter is not None
        
        # 测试情感分析方法
        texts = ["这个软件太垃圾了", "非常好用"]
        score = adapter._calculate_sentiment(texts)
        
        assert isinstance(score, float)
        assert -1 <= score <= 1
