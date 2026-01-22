from datetime import datetime, timedelta
from thinking.models.thinking_entry import ThinkingEntry
import os

class WeeklyReviewService:
    """周度评审服务"""
    
    @staticmethod
    def get_weekly_entries(user_id, days=7):
        """获取最近N天的条目"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        entries = ThinkingEntry.query.filter(
            ThinkingEntry.user_id == user_id,
            ThinkingEntry.created_at >= cutoff_date
        ).order_by(ThinkingEntry.created_at.desc()).all()
        
        return entries
    
    @staticmethod
    def calculate_stats(entries):
        """计算统计数据"""
        total = len(entries)
        by_status = {}
        
        for entry in entries:
            status = entry.status
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            'total': total,
            'by_status': by_status,
            'gate_pass_count': by_status.get('评估中', 0) + by_status.get('已落地', 0),
            'gate_fail_count': by_status.get('已否决', 0)
        }
    
    @staticmethod
    def score_entry(entry, scores):
        """
        为条目打分
        scores: {impact, feasibility, evidence, cost}
        返回综合得分
        """
        impact = scores.get('impact', 5)
        feasibility = scores.get('feasibility', 5)
        evidence = scores.get('evidence', 5)
        cost = scores.get('cost', 5)
        
        # 综合得分 = (影响力 + 可行性 + 证据充分度) - 执行成本
        total = (impact + feasibility + evidence) - cost
        
        return {
            'entry_id': entry.id,
            'title': entry.title,
            'impact': impact,
            'feasibility': feasibility,
            'evidence': evidence,
            'cost': cost,
            'total_score': total
        }
    
    @staticmethod
    def generate_weekly_plan(entries, top_n=3):
        """
        生成周度计划
        entries: 已打分的条目列表 [{entry, scores}, ...]
        """
        # 按综合得分排序
        sorted_entries = sorted(
            entries,
            key=lambda x: x['total_score'],
            reverse=True
        )
        
        top_entries = sorted_entries[:top_n]
        
        # 生成Markdown
        content = f"""# 周度执行计划

**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本周Top {top_n}

"""
        
        for i, item in enumerate(top_entries, 1):
            content += f"""
### {i}. {item['title']}

**综合得分:** {item['total_score']}分
- 影响力: {item['impact']}/10
- 可行性: {item['feasibility']}/10
- 证据充分度: {item['evidence']}/10
- 执行成本: {item['cost']}/10

**目标:** {item.get('problem', '待定义')}

**验收标准:** {item.get('success_metric', '待定义')}

**风险与止损:** {item.get('constraints', '无')}

---
"""
        
        # 保存文件
        filename = f"weekly-plan-{datetime.now().strftime('%Y-%m-%d')}.md"
        filepath = os.path.join('docs/thinking', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
