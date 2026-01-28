"""
情感分析增强模块

集成多种情感分析方法，支持：
1. 关键词匹配（基础版）
2. SVM/XGBoost 模型（准确率 80%+）
3. 可选的深度学习模型（LSTM/BERT）

使用策略：
- 默认使用 SVM+XGBoost 集成预测
- 模型不可用时回退到关键词匹配
"""

import os
import sys
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from loguru import logger

# 添加 SentimentAnalysisModel 路径
SENTIMENT_MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "SentimentAnalysisModel",
    "WeiboSentiment_MachineLearning"
)
if SENTIMENT_MODEL_PATH not in sys.path:
    sys.path.insert(0, SENTIMENT_MODEL_PATH)


class SentimentMethod(Enum):
    """情感分析方法枚举"""
    KEYWORD = "keyword"          # 关键词匹配
    SVM = "svm"                   # SVM 模型
    XGBOOST = "xgboost"          # XGBoost 模型
    ENSEMBLE = "ensemble"         # 集成预测 (SVM + XGBoost)
    LSTM = "lstm"                 # LSTM 深度学习
    BERT = "bert"                 # BERT 预训练模型


@dataclass
class SentimentResult:
    """情感分析结果"""
    score: float            # 情感得分 (-1 到 1)
    label: str              # 标签: "正面", "负面", "中性"
    confidence: float       # 置信度 (0 到 1)
    method: SentimentMethod # 使用的方法
    details: Optional[Dict] = None  # 详细信息


class EnhancedSentimentAnalyzer:
    """
    增强型情感分析器
    
    集成关键词匹配和机器学习模型，提供统一的情感分析接口。
    """
    
    # 扩展的负面关键词库
    NEGATIVE_KEYWORDS = [
        # 通用负面
        "问题", "困难", "失败", "烦", "卡", "慢", "差", "难用", "吐槽", "垃圾",
        "崩溃", "bug", "BUG", "闪退", "报错", "错误", "异常", "故障",
        # 用户体验
        "难受", "无语", "坑", "太烂", "辣鸡", "弱智", "智障", "迷惑", "无解",
        "反人类", "不友好", "不好用", "令人失望", "不推荐",
        # 性能问题
        "卡顿", "延迟", "超时", "断线", "掉线", "加载慢", "响应慢", "太慢",
        # 功能问题
        "缺失", "缺少", "没有", "找不到", "不支持", "不兼容", "限制",
        # 情绪表达
        "失望", "气死", "无奈", "绝望", "恶心", "讨厌", "厌恶", "愤怒",
        "后悔", "上当", "被坑", "退款", "投诉", "举报",
        # 服务问题
        "客服差", "态度差", "不回复", "踢皮球", "不解决", "敷衍",
    ]
    
    # 扩展的正面关键词库
    POSITIVE_KEYWORDS = [
        # 通用正面
        "好", "棒", "赞", "方便", "喜欢", "推荐", "满意", "完美", "优秀",
        "强大", "好用", "实用", "高效", "快速", "流畅", "稳定",
        # 用户体验
        "舒服", "舒适", "简洁", "清爽", "人性化", "易用", "简单",
        "漂亮", "美观", "精致",
        # 情绪表达
        "开心", "高兴", "惊喜", "感动", "感谢", "太棒了", "绝了",
        "给力", "牛", "神器", "真香",
        # 推荐意愿
        "安利", "种草", "五星", "五星好评", "必买", "必备",
        "强烈推荐", "值得", "超值",
    ]
    
    def __init__(
        self,
        default_method: SentimentMethod = SentimentMethod.ENSEMBLE,
        model_dir: str = None,
        load_models_on_init: bool = True
    ):
        """
        初始化情感分析器
        
        Args:
            default_method: 默认分析方法
            model_dir: 模型目录路径
            load_models_on_init: 是否在初始化时加载模型
        """
        self.default_method = default_method
        self.model_dir = model_dir or os.path.join(SENTIMENT_MODEL_PATH, "model")
        self._predictor = None
        self._models_loaded = False
        
        if load_models_on_init and default_method != SentimentMethod.KEYWORD:
            self._load_models()
            
    def _load_models(self) -> bool:
        """加载机器学习模型"""
        if self._models_loaded:
            return True
            
        try:
            # 使用简化版 SVM 预测器（避免 XGBoost 依赖问题）
            from svm_predictor import SimpleSVMPredictor
            
            svm_model_path = os.path.join(self.model_dir, "svm_model.pkl")
            
            if os.path.exists(svm_model_path):
                self._predictor = SimpleSVMPredictor(svm_model_path)
                if self._predictor._loaded:
                    self._models_loaded = True
                    logger.info("[情感分析] 已加载 SVM 模型 (简化版)")
                    return True
                    
            logger.warning("[情感分析] SVM 模型加载失败，将使用关键词匹配")
            return False
                
        except ImportError as e:
            logger.warning(f"[情感分析] 无法导入 SimpleSVMPredictor: {e}")
            return False
        except Exception as e:
            logger.error(f"[情感分析] 加载模型失败: {e}")
            return False
            
    def analyze(
        self,
        text: str,
        method: SentimentMethod = None
    ) -> SentimentResult:
        """
        分析单条文本的情感
        
        Args:
            text: 待分析文本
            method: 分析方法，默认使用初始化时指定的方法
            
        Returns:
            情感分析结果
        """
        method = method or self.default_method
        
        # 如果需要模型但模型不可用，回退到关键词
        if method != SentimentMethod.KEYWORD and not self._models_loaded:
            self._load_models()
            if not self._models_loaded:
                method = SentimentMethod.KEYWORD
                
        if method == SentimentMethod.KEYWORD:
            return self._analyze_by_keyword(text)
        elif method == SentimentMethod.ENSEMBLE:
            return self._analyze_by_ensemble(text)
        elif method in [SentimentMethod.SVM, SentimentMethod.XGBOOST]:
            return self._analyze_by_model(text, method.value)
        else:
            logger.warning(f"不支持的方法 {method}，使用关键词匹配")
            return self._analyze_by_keyword(text)
            
    def analyze_batch(
        self,
        texts: List[str],
        method: SentimentMethod = None
    ) -> List[SentimentResult]:
        """
        批量分析文本情感
        
        Args:
            texts: 待分析文本列表
            method: 分析方法
            
        Returns:
            情感分析结果列表
        """
        return [self.analyze(text, method) for text in texts]
        
    def calculate_average_score(self, texts: List[str]) -> float:
        """
        计算多条文本的平均情感得分
        
        Args:
            texts: 文本列表
            
        Returns:
            平均情感得分 (-1 到 1)
        """
        if not texts:
            return 0.0
            
        results = self.analyze_batch(texts)
        total_score = sum(r.score for r in results)
        return total_score / len(results)
        
    def _analyze_by_keyword(self, text: str) -> SentimentResult:
        """关键词匹配分析"""
        neg_count = sum(text.count(word) for word in self.NEGATIVE_KEYWORDS)
        pos_count = sum(text.count(word) for word in self.POSITIVE_KEYWORDS)
        
        total = neg_count + pos_count
        
        if total == 0:
            return SentimentResult(
                score=0.0,
                label="中性",
                confidence=0.5,
                method=SentimentMethod.KEYWORD,
                details={"neg_count": 0, "pos_count": 0}
            )
            
        score = (pos_count - neg_count) / total
        label = "正面" if score > 0.2 else ("负面" if score < -0.2 else "中性")
        confidence = min(abs(score) + 0.5, 1.0)
        
        return SentimentResult(
            score=score,
            label=label,
            confidence=confidence,
            method=SentimentMethod.KEYWORD,
            details={"neg_count": neg_count, "pos_count": pos_count}
        )
        
    def _analyze_by_model(self, text: str, model_type: str) -> SentimentResult:
        """使用SVM模型分析（简化版，只支持SVM）"""
        try:
            # SimpleSVMPredictor 使用 predict_single(text) 返回 (prediction, confidence)
            prediction, confidence = self._predictor.predict_single(text)
            score = confidence if prediction == 1 else -confidence
            label = "正面" if prediction == 1 else "负面"
            
            return SentimentResult(
                score=score,
                label=label,
                confidence=confidence,
                method=SentimentMethod.SVM,
                details={"prediction": prediction, "raw_confidence": confidence}
            )
                
        except Exception as e:
            logger.warning(f"模型预测失败: {e}，回退到关键词匹配")
            return self._analyze_by_keyword(text)
            
    def _analyze_by_ensemble(self, text: str) -> SentimentResult:
        """
        集成预测分析
        
        当前实现使用 SVM 模型。
        如果需要 XGBoost，请安装 libomp: brew install libomp
        """
        # 简化版只有 SVM，直接使用 SVM 预测
        return self._analyze_by_model(text, "svm")


# 全局单例
_sentiment_analyzer = None


def get_sentiment_analyzer() -> EnhancedSentimentAnalyzer:
    """获取情感分析器单例"""
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = EnhancedSentimentAnalyzer()
    return _sentiment_analyzer


def analyze_sentiment(text: str) -> SentimentResult:
    """
    分析文本情感（便捷函数）
    
    Args:
        text: 待分析文本
        
    Returns:
        情感分析结果
    """
    return get_sentiment_analyzer().analyze(text)


def calculate_sentiment_score(texts: List[str]) -> float:
    """
    计算情感得分（便捷函数）
    
    Args:
        texts: 文本列表
        
    Returns:
        平均情感得分 (-1 到 1)
    """
    return get_sentiment_analyzer().calculate_average_score(texts)
