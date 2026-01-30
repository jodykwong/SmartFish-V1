"""
BMAD Phase 0 验证报告生成器

生成痛点验证报告、商业机会分析和Phase 1进入评估。
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger

from bmad_adapter import PainPoint, DomainConfig
from pain_point_engine import PainPointDiscoveryEngine, ClusterResult
from user_validator import UserValidator, ValidationSummary


class BMADReportGenerator:
    """
    BMAD报告生成器
    
    生成以下报告:
    1. phase0-validation-report.md - 主要验证报告
    2. commercial-opportunity-analysis.md - 商业机会分析
    3. phase1-entry-assessment.md - Phase 1进入评估
    """
    
    def __init__(self, output_dir: str = "_bmad-output"):
        self.output_dir = output_dir
        self.config = DomainConfig()
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_validation_report(
        self,
        pain_points: List[PainPoint],
        clusters: List[ClusterResult],
        validations: Dict[str, ValidationSummary]
    ) -> str:
        """
        生成Phase 0验证报告
        
        Args:
            pain_points: 发现的痛点列表
            clusters: 聚类结果
            validations: 验证结果
            
        Returns:
            报告文件路径
        """
        standards = self.config.get_validation_standards()
        validated_count = sum(1 for v in validations.values() if v.is_validated)
        
        report = f"""# BMAD Phase 0 验证报告

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. 执行摘要

本报告记录了BMAD Method 2.0 Phase 0阶段的痛点发现与验证结果。

### 关键指标

| 指标 | 目标 | 实际 | 状态 |
|------|------|------|------|
| 发现痛点数 | ≥{standards.get('min_pain_points', 3)} | {len(pain_points)} | {'✅' if len(pain_points) >= standards.get('min_pain_points', 3) else '❌'} |
| 验证通过数 | ≥{standards.get('min_pain_points', 3)} | {validated_count} | {'✅' if validated_count >= standards.get('min_pain_points', 3) else '❌'} |
| 用户确认数 | 每痛点≥{standards.get('min_user_confirmations', 3)} | 见详情 | - |
| 付费意愿 | ≥{standards.get('min_payment_willingness', 0.3)*100:.0f}% | 见详情 | - |

---

## 2. 痛点发现详情

共发现 **{len(pain_points)}** 个痛点，聚类为 **{len(clusters)}** 个主题。

"""
        # 添加痛点详情
        for i, pp in enumerate(pain_points[:10], 1):
            validation = validations.get(pp.id)
            status = "✅ 验证通过" if validation and validation.is_validated else "⏳ 待验证"
            
            report += f"""### 2.{i} {pp.title}

- **领域**: {pp.domain}
- **状态**: {status}
- **提及次数**: {pp.mention_count}
- **商业潜力**: {pp.commercial_potential:.2f}
- **情感得分**: {pp.sentiment_score:.2f}

**用户原话摘录**:
"""
            for quote in pp.user_quotes[:3]:
                report += f'> "{quote[:100]}..."\n\n'
                
        report += """---

## 3. 聚类分析

"""
        for cluster in clusters[:5]:
            report += f"""### {cluster.theme}

- 包含痛点数: {len(cluster.pain_points)}
- 总提及次数: {cluster.total_mentions}
- 商业评分: {cluster.commercial_score:.2f}

"""

        report += """---

## 4. 验证结果汇总

"""
        for pp_id, summary in validations.items():
            report += f"""### {pp_id}

- 总响应数: {summary.total_responses}
- 确认用户: {summary.confirmed_users}
- 平均严重度: {summary.average_severity:.1f}/10
- 付费意愿比: {summary.payment_willing_ratio:.1%}
- 验证状态: {'✅ 通过' if summary.is_validated else '❌ 未通过'}
- 置信度: {summary.confidence_level}

**关键洞察**:
"""
            for insight in summary.key_insights:
                report += f"- {insight}\n"
            report += "\n"
            
        report += """---

## 5. 结论与建议

基于以上分析，请参阅 `phase1-entry-assessment.md` 了解Phase 1进入评估。

"""
        
        # 保存报告
        output_path = os.path.join(self.output_dir, "phase0-validation-report.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
        logger.info(f"验证报告已生成: {output_path}")
        return output_path
        
    def generate_opportunity_analysis(
        self,
        pain_points: List[PainPoint],
        validations: Dict[str, ValidationSummary]
    ) -> str:
        """生成商业机会分析报告"""
        
        # 按商业潜力排序
        sorted_points = sorted(
            pain_points,
            key=lambda x: x.commercial_potential,
            reverse=True
        )
        
        report = f"""# 商业机会分析

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. 商业机会排名

以下是按商业潜力排序的TOP痛点/机会:

"""
        for i, pp in enumerate(sorted_points[:5], 1):
            validation = validations.get(pp.id)
            payment_ratio = validation.payment_willing_ratio if validation else 0
            
            report += f"""### TOP {i}: {pp.title}

| 维度 | 评分 |
|------|------|
| 商业潜力 | {pp.commercial_potential:.2f}/1.0 |
| 用户痛感 | {abs(pp.sentiment_score):.2f}/1.0 |
| 付费意愿 | {payment_ratio:.1%} |
| 市场规模估算 | {'大' if pp.mention_count > 20 else '中' if pp.mention_count > 10 else '小'} |

**机会描述**: {pp.description}

**建议行动**:
"""
            if pp.commercial_potential >= 0.7:
                report += "- 🚀 立即进入Phase 1深入验证\n"
                report += "- 🎯 准备MVP原型设计\n"
            elif pp.commercial_potential >= 0.5:
                report += "- 📊 进一步收集用户反馈\n"
                report += "- 🔍 分析竞品解决方案\n"
            else:
                report += "- 👀 持续观察市场动态\n"
                report += "- 🔄 考虑pivot到相关痛点\n"
                
            report += "\n---\n\n"
            
        report += """## 2. 市场机会矩阵

```
高付费意愿
    │
    │   ★ 优先开发区
    │   
    ├────────────────────
    │
    │   ? 观察区
    │
    └────────────────────→ 高痛点频率
```

## 3. 建议优先级

1. **高优先级**: 商业潜力≥0.7 且付费意愿≥50%的痛点
2. **中优先级**: 商业潜力≥0.5 或付费意愿≥30%的痛点
3. **低优先级**: 其他痛点

"""
        
        output_path = os.path.join(self.output_dir, "commercial-opportunity-analysis.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
        logger.info(f"商业机会分析已生成: {output_path}")
        return output_path
        
    def generate_phase1_assessment(
        self,
        pain_points: List[PainPoint],
        validations: Dict[str, ValidationSummary]
    ) -> str:
        """生成Phase 1进入评估"""
        
        standards = self.config.get_validation_standards()
        
        # 检查各项标准
        min_pp = standards.get('min_pain_points', 3)
        min_confirm = standards.get('min_user_confirmations', 3)
        min_strong = standards.get('min_strong_confirmation', 5)
        min_payment = standards.get('min_payment_willingness', 0.3)
        
        validated = [v for v in validations.values() if v.is_validated]
        strong_confirm = [v for v in validations.values() if v.confirmed_users >= min_strong]
        high_payment = [v for v in validations.values() if v.payment_willing_ratio >= min_payment]
        
        criteria = {
            "发现≥3个痛点": len(pain_points) >= min_pp,
            "每痛点≥3用户确认": len(validated) >= min_pp,
            "至少1个痛点≥5用户确认": len(strong_confirm) >= 1,
            "≥30%用户付费意愿": len(high_payment) >= 1
        }
        
        all_passed = all(criteria.values())
        passed_count = sum(criteria.values())
        
        report = f"""# Phase 1 进入评估

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. 评估结论

### {'✅ 建议进入Phase 1' if all_passed else '⚠️ 暂不建议进入Phase 1'}

通过标准: **{passed_count}/4**

## 2. 标准检查清单

| 标准 | 状态 |
|------|------|
"""
        for criterion, passed in criteria.items():
            report += f"| {criterion} | {'✅' if passed else '❌'} |\n"
            
        report += f"""

## 3. 详细评估

### 3.1 痛点发现评估
- 目标: ≥{min_pp}个痛点
- 实际: {len(pain_points)}个痛点
- 状态: {'达标' if len(pain_points) >= min_pp else '未达标'}

### 3.2 用户确认评估
- 目标: 每痛点≥{min_confirm}用户确认
- 实际: {len(validated)}个痛点达标
- 状态: {'达标' if len(validated) >= min_pp else '未达标'}

### 3.3 强确认评估
- 目标: 至少1个痛点≥{min_strong}用户确认
- 实际: {len(strong_confirm)}个痛点达标
- 状态: {'达标' if len(strong_confirm) >= 1 else '未达标'}

### 3.4 付费意愿评估
- 目标: ≥{min_payment*100:.0f}%用户付费意愿
- 实际: {len(high_payment)}个痛点达标
- 状态: {'达标' if len(high_payment) >= 1 else '未达标'}

## 4. 下一步建议

"""
        if all_passed:
            report += """### 🚀 Phase 1 启动准备

1. **确定核心痛点**: 选择商业潜力最高的1-2个痛点作为主攻方向
2. **用户访谈**: 与确认用户进行深度访谈，了解详细需求
3. **竞品分析**: 分析现有解决方案的优劣势
4. **MVP设计**: 开始设计最小可行产品
5. **商业模式**: 初步规划定价策略和商业模式

"""
        else:
            report += """### 🔄 改进建议

1. **扩大数据源**: 增加更多平台的数据采集
2. **深化验证**: 进行更多用户调查
3. **优化关键词**: 调整搜索关键词以发现更多相关痛点
4. **考虑pivot**: 如果当前领域效果不佳，考虑转向其他领域

"""

        report += """---

*本评估基于BMAD Method 2.0 Phase 0验证标准*
"""
        
        output_path = os.path.join(self.output_dir, "phase1-entry-assessment.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
        logger.info(f"Phase 1评估已生成: {output_path}")
        return output_path
        
    def generate_all_reports(
        self,
        pain_points: List[PainPoint],
        clusters: List[ClusterResult],
        validations: Dict[str, ValidationSummary]
    ) -> Dict[str, str]:
        """生成所有报告"""
        
        paths = {
            "validation_report": self.generate_validation_report(
                pain_points, clusters, validations
            ),
            "opportunity_analysis": self.generate_opportunity_analysis(
                pain_points, validations
            ),
            "phase1_assessment": self.generate_phase1_assessment(
                pain_points, validations
            )
        }
        
        logger.info(f"所有报告已生成到: {self.output_dir}")
        return paths


if __name__ == "__main__":
    from bmad_adapter import PainPoint
    from user_validator import ValidationSummary
    from pain_point_engine import ClusterResult
    
    print("=== BMAD报告生成器测试 ===\n")
    
    # 创建测试数据
    test_pp = PainPoint(
        id="test_1",
        title="Claude上下文丢失",
        description="使用Claude时经常丢失对话上下文",
        domain="ai_chat_tools",
        keywords=["Claude", "上下文丢失"],
        mention_count=25,
        sentiment_score=-0.6,
        commercial_potential=0.75,
        user_quotes=["经常丢失上下文太烦了", "每次都要重新解释"]
    )
    
    test_validation = ValidationSummary(
        pain_point_id="test_1",
        total_responses=15,
        confirmed_users=12,
        average_severity=7.5,
        payment_willing_ratio=0.45,
        is_validated=True,
        confidence_level="中",
        key_insights=["高确认率", "中等付费意愿"]
    )
    
    test_cluster = ClusterResult(
        cluster_id="c1",
        theme="AI聊天工具: 上下文问题",
        pain_points=[test_pp],
        total_mentions=25,
        avg_sentiment=-0.6,
        commercial_score=0.75
    )
    
    # 生成报告
    generator = BMADReportGenerator()
    paths = generator.generate_all_reports(
        pain_points=[test_pp],
        clusters=[test_cluster],
        validations={"test_1": test_validation}
    )
    
    print("生成的报告:")
    for name, path in paths.items():
        print(f"  - {name}: {path}")
