"""
用户验证模块 (BMAD 2.0 被动信号挖掘版)

根据 YC "How To Get Your First Users" 和 Zero to Sold 理论：
- 获取早期用户是"搜索问题"而非"说服问题"
- 互联网数据是被动数据，无法做主动调查
- 应从被动数据中挖掘付费意愿、绝望程度等信号

本模块从社交媒体内容中被动挖掘用户信号，替代传统问卷调查。
"""

import os
import json
import re
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from loguru import logger

from bmad_adapter import PainPoint, ValidationResult


@dataclass
class PassiveSignal:
    """被动信号数据结构"""
    signal_type: str        # payment, desperation, solution_seeking
    signal_text: str        # 匹配的原文
    signal_score: float     # 信号强度 0-1
    source_platform: str    # 来源平台
    source_url: Optional[str] = None
    context: str = ""       # 上下文


@dataclass
class SignalResult:
    """信号挖掘结果"""
    pain_point_id: str
    total_content_count: int
    payment_signals: List[PassiveSignal]
    desperation_signals: List[PassiveSignal]
    solution_seeking_signals: List[PassiveSignal]
    
    payment_willingness_score: float    # 付费意愿评分 0-1
    desperation_level: float            # 绝望程度 0-1
    is_early_adopter_target: bool       # 是否适合早期用户
    
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        result = asdict(self)
        result["payment_signals"] = [asdict(s) for s in self.payment_signals]
        result["desperation_signals"] = [asdict(s) for s in self.desperation_signals]
        result["solution_seeking_signals"] = [asdict(s) for s in self.solution_seeking_signals]
        return result


@dataclass
class ValidationSummary:
    """验证摘要 (被动版)"""
    pain_point_id: str
    total_content_analyzed: int
    signal_density: float           # 信号密度 (信号数/内容数)
    payment_willingness_score: float
    desperation_level: float
    is_validated: bool
    confidence_level: str
    key_insights: List[str]
    
    def to_dict(self) -> Dict:
        return asdict(self)


class PassiveSignalMiner:
    """
    被动信号挖掘器
    
    从社交媒体内容中挖掘用户真实需求信号，无需主动调查。
    
    信号类型:
    1. 付费意愿信号 - 用户表达愿意为解决方案付费的意愿
    2. 绝望程度信号 - 用户对问题的痛苦程度
    3. 求解意愿信号 - 用户主动寻求解决方案
    """
    
    # 付费意愿信号模式
    PAYMENT_SIGNALS = [
        (r"愿意付费", 0.9),
        (r"值多少钱", 0.8),
        (r"买了.*但", 0.7),
        (r"求推荐.*付费", 0.8),
        (r"多少钱.*能", 0.7),
        (r"花钱.*解决", 0.8),
        (r"试用.*付费", 0.7),
        (r"会员.*值", 0.6),
        (r"订阅.*划算", 0.6),
        (r"充值.*开通", 0.5),
    ]
    
    # 绝望程度信号模式
    DESPERATION_SIGNALS = [
        (r"逼死了", 0.95),
        (r"受不了", 0.9),
        (r"跪求", 0.95),
        (r"急需", 0.8),
        (r"救命", 0.95),
        (r"崩溃", 0.85),
        (r"快疯了", 0.9),
        (r"无语了", 0.7),
        (r"太难了", 0.6),
        (r"心态炸了", 0.85),
        (r"折腾.*好久", 0.7),
        (r"搞了.*天", 0.65),
        (r"绝望", 0.9),
        (r"无解", 0.8),
    ]
    
    # 求解意愿信号模式
    SOLUTION_SEEKING_SIGNALS = [
        (r"有没有.*能", 0.8),
        (r"求推荐", 0.9),
        (r"怎么解决", 0.85),
        (r"求.*方法", 0.8),
        (r"谁知道.*怎么", 0.75),
        (r"有什么.*工具", 0.7),
        (r"求.*教程", 0.6),
        (r"有没有.*替代", 0.75),
        (r"怎么才能", 0.7),
        (r"有没有更好的", 0.8),
    ]
    
    # 早期用户特征模式
    EARLY_ADOPTER_SIGNALS = [
        (r"试用", 0.7),
        (r"尝试", 0.6),
        (r"体验", 0.6),
        (r"测试版", 0.9),
        (r"beta", 0.9),
        (r"内测", 0.95),
        (r"新功能", 0.7),
        (r"新出的", 0.65),
    ]
    
    def __init__(self):
        self._compile_patterns()
        
    def _compile_patterns(self):
        """预编译正则表达式"""
        self._payment_patterns = [(re.compile(p), s) for p, s in self.PAYMENT_SIGNALS]
        self._desperation_patterns = [(re.compile(p), s) for p, s in self.DESPERATION_SIGNALS]
        self._solution_patterns = [(re.compile(p), s) for p, s in self.SOLUTION_SEEKING_SIGNALS]
        self._adopter_patterns = [(re.compile(p), s) for p, s in self.EARLY_ADOPTER_SIGNALS]
        
    def mine_signals(
        self, 
        content: str, 
        platform: str = "unknown",
        url: str = None
    ) -> Dict[str, Any]:
        """
        从单条内容中挖掘信号
        
        Args:
            content: 内容文本
            platform: 来源平台
            url: 来源URL
            
        Returns:
            信号挖掘结果字典
        """
        payment_signals = self._mine_pattern_signals(
            content, self._payment_patterns, "payment", platform, url
        )
        desperation_signals = self._mine_pattern_signals(
            content, self._desperation_patterns, "desperation", platform, url
        )
        solution_signals = self._mine_pattern_signals(
            content, self._solution_patterns, "solution_seeking", platform, url
        )
        
        # 计算综合评分
        payment_score = self._calculate_signal_score(payment_signals)
        desperation_score = self._calculate_signal_score(desperation_signals)
        solution_score = self._calculate_signal_score(solution_signals)
        
        # 判断是否为早期用户目标
        is_early_adopter = self._check_early_adopter(content)
        
        return {
            "payment_willingness": payment_score,
            "desperation_level": desperation_score,
            "solution_seeking": solution_score,
            "is_early_adopter": is_early_adopter,
            "payment_signals": payment_signals,
            "desperation_signals": desperation_signals,
            "solution_signals": solution_signals,
        }
        
    def _mine_pattern_signals(
        self,
        content: str,
        patterns: List[Tuple],
        signal_type: str,
        platform: str,
        url: str
    ) -> List[PassiveSignal]:
        """从内容中挖掘指定类型的信号"""
        # Issue #2 修复: 添加内容长度限制防止ReDoS
        MAX_CONTENT_LENGTH = 10000  # 10KB限制
        if len(content) > MAX_CONTENT_LENGTH:
            content = content[:MAX_CONTENT_LENGTH]
            
        signals = []
        
        for pattern, base_score in patterns:
            # Issue #1 修复: 使用finditer直接获取每个匹配的位置
            for match_obj in pattern.finditer(content):
                # 提取上下文 (匹配位置前后30字符)
                start = max(0, match_obj.start() - 30)
                end = min(len(content), match_obj.end() + 30)
                context = content[start:end]
                match_text = match_obj.group()
                    
                signal = PassiveSignal(
                    signal_type=signal_type,
                    signal_text=match_text,
                    signal_score=base_score,
                    source_platform=platform,
                    source_url=url,
                    context=context
                )
                signals.append(signal)
                
        return signals
        
    def _calculate_signal_score(self, signals: List[PassiveSignal]) -> float:
        """计算信号综合评分"""
        if not signals:
            return 0.0
        
        # 取最高分 + 信号数量加成
        max_score = max(s.signal_score for s in signals)
        count_bonus = min(len(signals) * 0.05, 0.2)  # 最多+0.2
        
        return min(max_score + count_bonus, 1.0)
        
    def _check_early_adopter(self, content: str) -> bool:
        """检查内容是否显示早期用户特征"""
        for pattern, _ in self._adopter_patterns:
            if pattern.search(content):
                return True
        return False
        
    def mine_batch(
        self, 
        contents: List[Dict[str, str]],
        pain_point_id: str = "unknown"
    ) -> SignalResult:
        """
        批量挖掘信号
        
        Args:
            contents: 内容列表，每项包含 {text, platform, url}
            pain_point_id: 关联的痛点ID
            
        Returns:
            SignalResult 综合结果
        """
        all_payment_signals = []
        all_desperation_signals = []
        all_solution_signals = []
        
        for item in contents:
            text = item.get("text", item.get("content", ""))
            platform = item.get("platform", "unknown")
            url = item.get("url")
            
            result = self.mine_signals(text, platform, url)
            
            all_payment_signals.extend(result["payment_signals"])
            all_desperation_signals.extend(result["desperation_signals"])
            all_solution_signals.extend(result["solution_signals"])
                
        # 计算综合评分
        total_count = len(contents)
        
        payment_score = self._calculate_signal_score(all_payment_signals)
        desperation_score = self._calculate_signal_score(all_desperation_signals)
        
        # 是否适合早期用户：信号密度足够高
        signal_count = len(all_payment_signals) + len(all_desperation_signals) + len(all_solution_signals)
        is_early_target = (
            signal_count >= 3 and 
            (desperation_score >= 0.7 or payment_score >= 0.5)
        )
        
        return SignalResult(
            pain_point_id=pain_point_id,
            total_content_count=total_count,
            payment_signals=all_payment_signals,
            desperation_signals=all_desperation_signals,
            solution_seeking_signals=all_solution_signals,
            payment_willingness_score=payment_score,
            desperation_level=desperation_score,
            is_early_adopter_target=is_early_target
        )


class PassiveValidator:
    """
    被动验证器 - 基于信号挖掘的用户需求验证
    
    验证标准 (新标准 - 被动挖掘):
    | 旧标准 (主动调查) | 新标准 (被动挖掘) |
    |------------------|------------------|
    | ≥3用户问卷确认    | ≥10条自然表达内容 |
    | 30%问卷付费意愿   | ≥3条付费意愿信号  |
    | 调查响应数量      | 绝望程度信号密度   |
    """
    
    # 验证阈值
    MIN_CONTENT_COUNT = 10      # 最少需要10条自然表达内容
    MIN_PAYMENT_SIGNALS = 3     # 最少3条付费意愿信号
    MIN_DESPERATION_SCORE = 0.5 # 绝望程度至少0.5
    
    def __init__(self):
        self.miner = PassiveSignalMiner()
        self.results: Dict[str, SignalResult] = {}
        self.summaries: Dict[str, ValidationSummary] = {}
        
    def validate_from_content(
        self,
        pain_point: PainPoint,
        contents: List[Dict[str, str]]
    ) -> ValidationSummary:
        """
        从内容批量验证痛点
        
        Args:
            pain_point: 痛点对象
            contents: 内容列表
            
        Returns:
            ValidationSummary 验证摘要
        """
        # 挖掘信号
        signal_result = self.miner.mine_batch(contents, pain_point.id)
        self.results[pain_point.id] = signal_result
        
        # 计算验证结果
        summary = self._calculate_validation(pain_point.id, signal_result)
        self.summaries[pain_point.id] = summary
        
        return summary
        
    def _calculate_validation(
        self, 
        pain_point_id: str, 
        result: SignalResult
    ) -> ValidationSummary:
        """计算验证结果"""
        total = result.total_content_count
        payment_count = len(result.payment_signals)
        desperation_count = len(result.desperation_signals)
        solution_count = len(result.solution_seeking_signals)
        
        total_signals = payment_count + desperation_count + solution_count
        signal_density = total_signals / total if total > 0 else 0
        
        # 判断是否验证通过
        is_validated = (
            total >= self.MIN_CONTENT_COUNT and
            payment_count >= self.MIN_PAYMENT_SIGNALS and
            result.desperation_level >= self.MIN_DESPERATION_SCORE
        )
        
        # 置信度
        if total >= 50 and total_signals >= 10:
            confidence = "高"
        elif total >= 20 and total_signals >= 5:
            confidence = "中"
        else:
            confidence = "低"
            
        # 关键洞察
        insights = self._extract_insights(result, signal_density)
        
        return ValidationSummary(
            pain_point_id=pain_point_id,
            total_content_analyzed=total,
            signal_density=signal_density,
            payment_willingness_score=result.payment_willingness_score,
            desperation_level=result.desperation_level,
            is_validated=is_validated,
            confidence_level=confidence,
            key_insights=insights
        )
        
    def _extract_insights(
        self, 
        result: SignalResult, 
        signal_density: float
    ) -> List[str]:
        """提取关键洞察"""
        insights = []
        
        if result.desperation_level >= 0.8:
            insights.append(f"🔥 高绝望程度: {result.desperation_level:.0%}，用户急需解决方案")
        elif result.desperation_level >= 0.5:
            insights.append(f"⚠️ 中等绝望程度: {result.desperation_level:.0%}")
            
        if result.payment_willingness_score >= 0.7:
            insights.append(f"💰 强付费意愿: 检测到{len(result.payment_signals)}条付费相关信号")
        elif result.payment_willingness_score >= 0.4:
            insights.append(f"💵 中等付费意愿: 检测到{len(result.payment_signals)}条付费相关信号")
            
        if signal_density >= 0.3:
            insights.append(f"📈 高信号密度: 每{1/signal_density:.1f}条内容包含一个需求信号")
            
        if result.is_early_adopter_target:
            insights.append("🎯 适合作为早期用户目标群体")
            
        if not insights:
            insights.append("需要更多数据以获得可靠洞察")
            
        return insights
        
    def calculate_pain_point_score(self, pain_point_id: str) -> float:
        """
        计算痛点综合评分 (新评分算法)
        
        评分权重:
        - 绝望程度: 40%
        - 付费信号: 30%
        - 求解意愿: 20%
        - 提及频率: 10%
        """
        result = self.results.get(pain_point_id)
        if not result:
            return 0.0
            
        desperation_score = result.desperation_level * 0.4
        payment_score = result.payment_willingness_score * 0.3
        
        # 求解意愿由信号数量归一化
        solution_count = len(result.solution_seeking_signals)
        solution_score = min(solution_count / 5, 1.0) * 0.2
        
        # 提及频率由内容总数归一化
        frequency_score = min(result.total_content_count / 50, 1.0) * 0.1
        
        total_score = desperation_score + payment_score + solution_score + frequency_score
        
        return round(total_score, 2)
        
    def get_validation_report(self) -> Dict:
        """获取验证报告"""
        return {
            "total_pain_points_analyzed": len(self.results),
            "validated_pain_points": sum(1 for s in self.summaries.values() if s.is_validated),
            "summaries": {k: v.to_dict() for k, v in self.summaries.items()},
            "scores": {k: self.calculate_pain_point_score(k) for k in self.results.keys()},
            "timestamp": datetime.now().isoformat()
        }
        
    def save_results(self, output_dir: str = "_bmad-output") -> str:
        """保存验证结果"""
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, "passive-validation-results.json")
        
        data = {
            "signal_results": {k: v.to_dict() for k, v in self.results.items()},
            "validation_report": self.get_validation_report(),
            "generated_at": datetime.now().isoformat()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        logger.info(f"验证结果已保存到: {output_path}")
        return output_path


# ============================================================
# 兼容性别名 (保留旧接口，但标记为弃用)
# ============================================================

class UserValidator(PassiveValidator):
    """
    用户验证器 (兼容性别名)
    
    ⚠️ 已弃用: 请使用 PassiveValidator 类
    """
    
    def __init__(self):
        import warnings
        warnings.warn(
            "UserValidator 已弃用，请使用 PassiveValidator 类",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__()


if __name__ == "__main__":
    from bmad_adapter import PainPoint
    
    print("=== BMAD 2.0 被动信号挖掘测试 ===\n")
    
    # 创建测试痛点
    test_pp = PainPoint(
        id="test_pp_1",
        title="Claude上下文丢失",
        description="使用Claude时经常丢失对话上下文",
        domain="ai_chat_tools",
        keywords=["Claude", "上下文丢失"]
    )
    
    # 模拟社媒内容
    test_contents = [
        {"text": "Claude用着用着上下文就丢了，快崩溃了，有没有什么工具能解决？", "platform": "xiaohongshu"},
        {"text": "愿意付费买一个能保持上下文的AI工具，受不了了", "platform": "weibo"},
        {"text": "跪求推荐一个上下文不会丢的AI助手", "platform": "zhihu"},
        {"text": "试用了很多AI工具，Claude的上下文管理太难了", "platform": "xiaohongshu"},
        {"text": "这个问题折腾好久了，花钱都愿意解决", "platform": "weibo"},
        {"text": "Claude挺好用的，就是上下文经常断", "platform": "bilibili"},
        {"text": "有没有更好的替代品？这个上下文丢失问题太烦了", "platform": "xiaohongshu"},
        {"text": "搞了3天了还是没解决，无语了", "platform": "zhihu"},
        {"text": "求推荐付费的解决方案，值多少钱都可以", "platform": "weibo"},
        {"text": "Claude的上下文管理需要改进", "platform": "bilibili"},
        {"text": "太难了，救命啊", "platform": "xiaohongshu"},
        {"text": "有没有能保持对话上下文的工具推荐？", "platform": "zhihu"},
    ]
    
    # 初始化被动验证器
    validator = PassiveValidator()
    
    # 验证痛点
    summary = validator.validate_from_content(test_pp, test_contents)
    
    print(f"验证结果:")
    print(f"  - 分析内容数: {summary.total_content_analyzed}")
    print(f"  - 信号密度: {summary.signal_density:.1%}")
    print(f"  - 付费意愿: {summary.payment_willingness_score:.0%}")
    print(f"  - 绝望程度: {summary.desperation_level:.0%}")
    print(f"  - 是否验证通过: {summary.is_validated}")
    print(f"  - 置信度: {summary.confidence_level}")
    print(f"  - 关键洞察:")
    for insight in summary.key_insights:
        print(f"    {insight}")
        
    # 计算综合评分
    score = validator.calculate_pain_point_score(test_pp.id)
    print(f"\n痛点综合评分: {score:.2f}")
    
    # 保存结果
    path = validator.save_results()
    print(f"\n结果已保存到: {path}")
