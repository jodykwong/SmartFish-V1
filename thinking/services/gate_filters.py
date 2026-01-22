from abc import ABC, abstractmethod
from enum import Enum

class GateResult(Enum):
    PASS = 'pass'
    WARNING = 'warning'
    FAIL = 'fail'

class GateFilter(ABC):
    @abstractmethod
    def evaluate(self, entry, user_input):
        """返回 (GateResult, reason)"""
        pass

class HumanDependencyFilter(GateFilter):
    """层1: 人性依赖过滤器"""
    
    def evaluate(self, entry, user_input):
        if user_input == 'strong_dependency':
            return (GateResult.FAIL, '强依赖他人意愿/行动/情绪')
        elif user_input == 'partial_dependency':
            return (GateResult.WARNING, '有一定依赖但可控')
        return (GateResult.PASS, '不依赖他人')

class ValueSelfEvidentFilter(GateFilter):
    """层2: 价值自证过滤器"""
    
    def evaluate(self, entry, user_input):
        if user_input == 'needs_explanation':
            return (GateResult.FAIL, '需要反复解释价值')
        return (GateResult.PASS, '价值自证')

class FeedbackCleanFilter(GateFilter):
    """层3: 反馈清洁度过滤器"""
    
    def evaluate(self, entry, user_input):
        if user_input == 'not_falsifiable':
            return (GateResult.FAIL, '反馈不可证伪')
        elif user_input == 'partially_quantifiable':
            return (GateResult.WARNING, '部分依赖主观判断')
        return (GateResult.PASS, '反馈可量化')

class RoleCostFilter(GateFilter):
    """层4: 角色消耗过滤器"""
    
    def evaluate(self, entry, user_input):
        if user_input == 'need_push':
            return (GateResult.WARNING, '需要推动事情发生')
        return (GateResult.PASS, '仅为判断负责')
