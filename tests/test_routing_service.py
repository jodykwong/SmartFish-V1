import pytest
from unittest.mock import Mock
from thinking.services.routing_service import RoutingService

class TestRoutingService:
    def test_quick_routing_small_impact(self):
        entry = Mock()
        entry.target_segment = 'small team'
        entry.dependencies = None
        entry.evidence_needed = None
        entry.constraints = None
        entry.id = 1
        
        result = RoutingService.suggest_routing(entry)
        
        assert result['routing'] == 'Quick'
        assert result['score'] <= 3
    
    def test_standard_routing_medium_impact(self):
        entry = Mock()
        entry.target_segment = 'medium company'
        entry.dependencies = 'dep1, dep2, dep3'
        entry.evidence_needed = 'some evidence'
        entry.constraints = None
        entry.id = 1
        
        result = RoutingService.suggest_routing(entry)
        
        assert result['routing'] in ['Standard', 'Quick']
        assert result['score'] > 0
    
    def test_enterprise_routing_large_impact(self):
        entry = Mock()
        entry.target_segment = 'enterprise'
        entry.dependencies = 'dep1, dep2, dep3, dep4, dep5, dep6'
        entry.evidence_needed = 'evidence'
        entry.constraints = 'high_complexity'
        entry.id = 1
        
        result = RoutingService.suggest_routing(entry)
        
        assert result['routing'] in ['Enterprise', 'Standard']
        assert result['score'] > 7
    
    def test_assess_impact(self):
        entry = Mock()
        
        entry.target_segment = 'small team'
        assert RoutingService._assess_impact(entry) == 'small'
        
        entry.target_segment = 'enterprise'
        assert RoutingService._assess_impact(entry) == 'large'
        
        entry.target_segment = 'medium company'
        assert RoutingService._assess_impact(entry) == 'medium'
    
    def test_count_dependencies(self):
        entry = Mock()
        
        entry.dependencies = None
        assert RoutingService._count_dependencies(entry) == 0
        
        entry.dependencies = 'dep1, dep2, dep3'
        assert RoutingService._count_dependencies(entry) == 3
