class RoutingService:
    """路由决策算法"""
    
    IMPACT_SCORES = {
        'small': 0,
        'medium': 2,
        'large': 4
    }
    
    DEPENDENCY_THRESHOLD = 5
    QUICK_THRESHOLD = 3
    STANDARD_THRESHOLD = 7
    
    @staticmethod
    def suggest_routing(entry):
        """
        基于规则的评分系统
        返回: {routing, score, reasons}
        """
        score = 0
        reasons = []
        
        # 1. 影响范围
        impact = RoutingService._assess_impact(entry)
        score += RoutingService.IMPACT_SCORES.get(impact, 0)
        reasons.append(f'影响范围: {impact}')
        
        # 2. 依赖数量
        dep_count = RoutingService._count_dependencies(entry)
        if dep_count > RoutingService.DEPENDENCY_THRESHOLD:
            score += 3
            reasons.append(f'依赖数量: {dep_count}')
        
        # 3. Gate警告数（从gate_reviews获取）
        warnings = RoutingService._get_gate_warnings(entry)
        score += warnings
        if warnings > 0:
            reasons.append(f'Gate警告: {warnings}个')
        
        # 4. 证据缺口
        if entry.evidence_needed:
            score += 1
            reasons.append('需要证据补强')
        
        # 5. 技术复杂度
        if entry.constraints and 'high_complexity' in entry.constraints:
            score += 2
            reasons.append('技术复杂度高')
        
        # 决策
        if score <= RoutingService.QUICK_THRESHOLD:
            routing = 'Quick'
        elif score <= RoutingService.STANDARD_THRESHOLD:
            routing = 'Standard'
        else:
            routing = 'Enterprise'
        
        return {
            'routing': routing,
            'score': score,
            'reasons': reasons
        }
    
    @staticmethod
    def _assess_impact(entry):
        """评估影响范围"""
        if not entry.target_segment:
            return 'small'
        
        target = entry.target_segment.lower()
        if 'small' in target or '个人' in target:
            return 'small'
        elif 'enterprise' in target or '企业' in target:
            return 'large'
        return 'medium'
    
    @staticmethod
    def _count_dependencies(entry):
        """统计依赖数量"""
        if not entry.dependencies:
            return 0
        return len([d.strip() for d in entry.dependencies.split(',') if d.strip()])
    
    @staticmethod
    def _get_gate_warnings(entry):
        """获取Gate警告数"""
        from thinking.models.gate_review import GateReview
        review = GateReview.query.filter_by(entry_id=entry.id)\
            .order_by(GateReview.reviewed_at.desc()).first()
        
        if not review or review.decision != 'pass':
            return 0
        
        warnings = 0
        if not review.human_dependency_pass:
            warnings += 1
        if not review.feedback_clean_pass:
            warnings += 1
        if not review.role_cost_pass:
            warnings += 1
        
        return warnings
