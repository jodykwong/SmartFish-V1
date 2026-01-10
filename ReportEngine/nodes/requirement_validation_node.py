"""
需求验证节点
Story 4-1: 需求验证节点
Story 4-2: 结论章节强制
"""
import re
from typing import Dict, List, Any, Optional
from loguru import logger


class RequirementValidationNode:
    """验证报告是否满足用户需求"""
    
    def __init__(self):
        self.conclusion_keywords = ['结论', '建议', '总结', '下一步', '行动']
    
    def validate(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证报告是否满足用户需求
        
        Args:
            state: 包含 user_query 和 report_ir 的状态字典
            
        Returns:
            验证结果字典
        """
        user_query = state.get('user_query', '')
        report_ir = state.get('report_ir', {})
        
        results = {
            'passed': True,
            'failures': [],
            'warnings': []
        }
        
        # 1. 数量要求检查
        quantity_check = self._check_quantity_requirement(user_query, report_ir)
        if quantity_check:
            results['failures'].append(quantity_check)
            results['passed'] = False
        
        # 2. 结论章节检查
        conclusion_check = self._check_conclusion_section(report_ir)
        if conclusion_check:
            results['failures'].append(conclusion_check)
            results['passed'] = False
        
        # 3. 数据来源检查（警告级别）
        source_check = self._check_data_sources(report_ir)
        if source_check:
            results['warnings'].append(source_check)
        
        return results
    
    def _check_quantity_requirement(self, query: str, report_ir: Dict) -> Optional[str]:
        """检查数量要求是否满足"""
        # 提取数量要求
        patterns = [
            r'(\d+)\s*个\s*(方向|方面|点|条|项|建议|机会)',
            r'(\d+)\s*(directions?|points?|items?|suggestions?)',
        ]
        
        required_count = None
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                required_count = int(match.group(1))
                break
        
        if required_count is None:
            return None
        
        # 统计实际输出数量
        actual_count = self._count_main_sections(report_ir)
        
        if actual_count < required_count:
            return f"数量不足: 要求 {required_count} 个，实际 {actual_count} 个"
        
        return None
    
    def _count_main_sections(self, report_ir: Dict) -> int:
        """统计主要章节数量"""
        chapters = report_ir.get('chapters', [])
        # 排除摘要和结论章节，统计主体内容章节
        main_chapters = [
            ch for ch in chapters 
            if not any(kw in ch.get('title', '') for kw in ['摘要', '结论', '总结', '附录'])
        ]
        return len(main_chapters)
    
    def _check_conclusion_section(self, report_ir: Dict) -> Optional[str]:
        """检查是否有结论章节"""
        chapters = report_ir.get('chapters', [])
        
        for chapter in chapters:
            title = chapter.get('title', '')
            if any(kw in title for kw in self.conclusion_keywords):
                # 检查结论章节是否有内容
                content = chapter.get('content', '')
                blocks = chapter.get('blocks', [])
                if content or blocks:
                    return None
                else:
                    return "结论章节为空"
        
        return "缺少结论章节"
    
    def _check_data_sources(self, report_ir: Dict) -> Optional[str]:
        """检查数据来源引用"""
        chapters = report_ir.get('chapters', [])
        chapters_without_sources = []
        
        for chapter in chapters:
            title = chapter.get('title', '')
            # 跳过摘要章节
            if '摘要' in title:
                continue
            
            content = str(chapter.get('content', ''))
            blocks = chapter.get('blocks', [])
            
            # 检查是否有来源引用
            has_source = (
                '[Source' in content or 
                '来源' in content or
                '数据来源' in content or
                any('[Source' in str(b) for b in blocks)
            )
            
            if not has_source:
                chapters_without_sources.append(title)
        
        if chapters_without_sources:
            return f"以下章节缺少数据来源引用: {', '.join(chapters_without_sources[:3])}"
        
        return None


def validate_report(user_query: str, report_ir: Dict) -> Dict[str, Any]:
    """便捷函数：验证报告"""
    validator = RequirementValidationNode()
    return validator.validate({
        'user_query': user_query,
        'report_ir': report_ir
    })
