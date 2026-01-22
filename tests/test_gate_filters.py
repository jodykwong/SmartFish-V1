import pytest
from thinking.services.gate_filters import (
    GateResult,
    HumanDependencyFilter,
    ValueSelfEvidentFilter,
    FeedbackCleanFilter,
    RoleCostFilter
)

class TestGateFilters:
    def test_human_dependency_fail(self):
        filter = HumanDependencyFilter()
        result, reason = filter.evaluate(None, 'strong_dependency')
        assert result == GateResult.FAIL
        assert '强依赖' in reason
    
    def test_human_dependency_warning(self):
        filter = HumanDependencyFilter()
        result, reason = filter.evaluate(None, 'partial_dependency')
        assert result == GateResult.WARNING
    
    def test_human_dependency_pass(self):
        filter = HumanDependencyFilter()
        result, reason = filter.evaluate(None, 'no')
        assert result == GateResult.PASS
    
    def test_value_self_evident_fail(self):
        filter = ValueSelfEvidentFilter()
        result, reason = filter.evaluate(None, 'needs_explanation')
        assert result == GateResult.FAIL
    
    def test_feedback_clean_fail(self):
        filter = FeedbackCleanFilter()
        result, reason = filter.evaluate(None, 'not_falsifiable')
        assert result == GateResult.FAIL
    
    def test_role_cost_warning(self):
        filter = RoleCostFilter()
        result, reason = filter.evaluate(None, 'need_push')
        assert result == GateResult.WARNING
