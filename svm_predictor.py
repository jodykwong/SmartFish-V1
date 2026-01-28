"""
简化版 SVM 情感预测器

仅使用 SVM 模型进行情感预测，避免 XGBoost 依赖问题。
此文件是从原 WeiboSentiment_MachineLearning 模块简化而来。
"""

import os
import pickle
import re
import jieba
from typing import Tuple, List, Optional
from loguru import logger


def processing(text: str) -> str:
    """文本预处理"""
    # 清洗文本
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # 分词
    words = jieba.cut(text)
    return ' '.join(words)


class SimpleSVMPredictor:
    """
    简化版 SVM 情感预测器
    
    仅使用 SVM 模型，不依赖 XGBoost/LSTM/BERT 等复杂模型。
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        初始化预测器
        
        Args:
            model_path: SVM 模型文件路径
        """
        self.model = None
        self.vectorizer = None
        self._loaded = False
        
        if model_path:
            self.load_model(model_path)
            
    def load_model(self, model_path: str) -> bool:
        """
        加载 SVM 模型
        
        Args:
            model_path: 模型文件路径 (.pkl)
            
        Returns:
            是否加载成功
        """
        if not os.path.exists(model_path):
            logger.error(f"模型文件不存在: {model_path}")
            return False
            
        try:
            with open(model_path, 'rb') as f:
                data = pickle.load(f)
                
            if isinstance(data, dict):
                self.model = data.get('model')
                self.vectorizer = data.get('vectorizer')
            else:
                self.model = data
                # 尝试加载对应的 vectorizer
                vectorizer_path = model_path.replace('_model.pkl', '_vectorizer.pkl')
                if os.path.exists(vectorizer_path):
                    with open(vectorizer_path, 'rb') as f:
                        self.vectorizer = pickle.load(f)
                        
            self._loaded = True
            logger.info(f"[SVM] 模型加载成功: {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"[SVM] 模型加载失败: {e}")
            return False
            
    def predict_single(self, text: str) -> Tuple[int, float]:
        """
        预测单条文本情感
        
        Args:
            text: 待预测文本（可以是原始文本或已分词文本）
            
        Returns:
            (prediction, confidence)
            prediction: 1=正面, 0=负面
            confidence: 预测置信度 (0-1)
        """
        if not self._loaded:
            raise RuntimeError("模型未加载")
            
        # 预处理
        processed = processing(text)
        
        try:
            # 向量化
            if self.vectorizer:
                features = self.vectorizer.transform([processed])
            else:
                # 如果没有 vectorizer，假设模型可以直接处理文本
                features = [processed]
                
            # SVM 预测
            prediction = int(self.model.predict(features)[0])
            
            # 获取置信度
            if hasattr(self.model, 'predict_proba'):
                proba = self.model.predict_proba(features)[0]
                confidence = float(max(proba))
            elif hasattr(self.model, 'decision_function'):
                decision = self.model.decision_function(features)[0]
                # 将 decision function 转换为概率
                import math
                confidence = 1 / (1 + math.exp(-abs(decision)))
            else:
                confidence = 0.7  # 默认置信度
                
            return prediction, confidence
            
        except Exception as e:
            logger.warning(f"[SVM] 预测失败: {e}")
            return 0, 0.5
            
    def predict_batch(self, texts: List[str]) -> List[Tuple[int, float]]:
        """
        批量预测
        
        Args:
            texts: 待预测文本列表
            
        Returns:
            预测结果列表
        """
        return [self.predict_single(text) for text in texts]


# 全局单例
_svm_predictor = None


def get_svm_predictor(model_path: str = None) -> SimpleSVMPredictor:
    """获取 SVM 预测器单例"""
    global _svm_predictor
    
    if _svm_predictor is None:
        if model_path is None:
            # 默认模型路径
            model_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "SentimentAnalysisModel",
                "WeiboSentiment_MachineLearning",
                "model",
                "svm_model.pkl"
            )
        _svm_predictor = SimpleSVMPredictor(model_path)
        
    return _svm_predictor
