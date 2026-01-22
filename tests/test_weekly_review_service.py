import pytest
from unittest.mock import Mock
from thinking.services.weekly_review_service import WeeklyReviewService

class TestWeeklyReviewService:
    def test_calculate_stats(self):
        entries = [
            Mock(status='想法'),
            Mock(status='评估中'),
            Mock(status='评估中'),
            Mock(status='已否决'),
            Mock(status='已落地')
        ]
        
        stats = WeeklyReviewService.calculate_stats(entries)
        
        assert stats['total'] == 5
        assert stats['by_status']['想法'] == 1
        assert stats['by_status']['评估中'] == 2
        assert stats['by_status']['已否决'] == 1
        assert stats['by_status']['已落地'] == 1
        assert stats['gate_pass_count'] == 3  # 评估中 + 已落地
        assert stats['gate_fail_count'] == 1
    
    def test_score_entry(self):
        entry = Mock(id=1, title='Test Entry')
        
        scores = {
            'impact': 8,
            'feasibility': 7,
            'evidence': 6,
            'cost': 5
        }
        
        result = WeeklyReviewService.score_entry(entry, scores)
        
        assert result['entry_id'] == 1
        assert result['title'] == 'Test Entry'
        assert result['impact'] == 8
        assert result['feasibility'] == 7
        assert result['evidence'] == 6
        assert result['cost'] == 5
        assert result['total_score'] == 16  # (8+7+6) - 5
    
    def test_score_entry_defaults(self):
        entry = Mock(id=1, title='Test')
        
        result = WeeklyReviewService.score_entry(entry, {})
        
        # 默认都是5分
        assert result['total_score'] == 10  # (5+5+5) - 5
