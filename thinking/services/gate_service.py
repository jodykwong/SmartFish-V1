from database import db
from thinking.models.gate_review import GateReview
from thinking.models.thinking_entry import ThinkingEntry
from thinking.services.gate_filters import (
    GateResult,
    HumanDependencyFilter,
    ValueSelfEvidentFilter,
    FeedbackCleanFilter,
    RoleCostFilter
)
import logging

logger = logging.getLogger(__name__)

class GateService:
    def __init__(self):
        self.filters = [
            HumanDependencyFilter(),
            ValueSelfEvidentFilter(),
            FeedbackCleanFilter(),
            RoleCostFilter()
        ]
        
        self.filter_names = [
            '人性依赖',
            '价值自证',
            '反馈清洁度',
            '角色消耗'
        ]
    
    def evaluate(self, entry_id, user_inputs):
        """
        评估Gate
        user_inputs: 4个输入，对应4层过滤器
        返回: {decision, fail_level, fail_reason, results, warnings}
        """
        entry = ThinkingEntry.query.get(entry_id)
        if not entry:
            raise ValueError('条目不存在')
        
        results = []
        warnings = []
        
        for i, (filter_obj, user_input) in enumerate(zip(self.filters, user_inputs)):
            result, reason = filter_obj.evaluate(entry, user_input)
            layer_num = i + 1
            
            results.append({
                'layer': layer_num,
                'name': self.filter_names[i],
                'result': result.value,
                'reason': reason
            })
            
            if result == GateResult.FAIL:
                # 任一层失败，立即否决
                logger.warning(f"Gate评估失败 - Entry {entry_id}, Layer {layer_num}: {reason}")
                try:
                    self._save_review(entry_id, results, 'fail', layer_num, reason)
                    self._update_entry_status(entry_id, '已否决')
                    db.session.commit()
                except Exception as e:
                    logger.error(f"保存Gate评估失败: {e}", exc_info=True)
                    db.session.rollback()
                    raise
                
                return {
                    'decision': 'fail',
                    'fail_level': layer_num,
                    'fail_reason': reason,
                    'results': results,
                    'warnings': []
                }
            
            if result == GateResult.WARNING:
                warnings.append({
                    'layer': layer_num,
                    'name': self.filter_names[i],
                    'reason': reason
                })
        
        # 全部通过
        logger.info(f"Gate评估通过 - Entry {entry_id}, Warnings: {len(warnings)}")
        try:
            self._save_review(entry_id, results, 'pass', None, None)
            self._update_entry_status(entry_id, '评估中')
            db.session.commit()
        except Exception as e:
            logger.error(f"保存Gate评估失败: {e}", exc_info=True)
            db.session.rollback()
            raise
        
        return {
            'decision': 'pass',
            'fail_level': None,
            'fail_reason': None,
            'results': results,
            'warnings': warnings
        }
    
    def _save_review(self, entry_id, results, decision, fail_level, fail_reason):
        """保存Gate审查记录"""
        # 安全获取结果，避免索引越界
        def get_pass_status(index):
            return results[index]['result'] != 'fail' if index < len(results) else None
        
        review = GateReview(
            entry_id=entry_id,
            human_dependency_pass=get_pass_status(0),
            value_self_evident_pass=get_pass_status(1),
            feedback_clean_pass=get_pass_status(2),
            role_cost_pass=get_pass_status(3),
            decision=decision,
            fail_level=f'层{fail_level}' if fail_level else None,
            fail_reason=fail_reason
        )
        db.session.add(review)
        db.session.commit()
        return review
    
    def _update_entry_status(self, entry_id, status):
        """更新条目状态"""
        entry = ThinkingEntry.query.get(entry_id)
        if entry:
            entry.status = status
            db.session.commit()
    
    def get_review(self, entry_id):
        """获取最新的Gate审查记录"""
        return GateReview.query.filter_by(entry_id=entry_id)\
            .order_by(GateReview.reviewed_at.desc())\
            .first()
