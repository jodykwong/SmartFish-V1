"""
Audience Report Generator
受众分析报告生成器
"""
from datetime import datetime
from typing import List, Dict
from jinja2 import Template


class AudienceReportGenerator:
    """受众分析报告生成器"""
    
    @staticmethod
    def _load_template() -> str:
        """加载模板"""
        with open('ReportEngine/report_template/audience_first_report.md', 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def _prepare_data(clusters: List[Dict]) -> Dict:
        """准备模板数据"""
        # 提取平台列表
        platforms = set()
        all_evidence = []
        
        for cluster in clusters:
            for evidence in cluster.get('evidence_refs', []):
                platforms.add(evidence.get('platform', '未知'))
                all_evidence.append(evidence)
        
        # Top2
        top1 = clusters[0] if len(clusters) > 0 else {}
        top2 = clusters[1] if len(clusters) > 1 else {}
        
        top2_names = []
        if top1:
            top2_names.append(f"{top1['role']}-{top1['scenario']}")
        if top2:
            top2_names.append(f"{top2['role']}-{top2['scenario']}")
        
        return {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'platforms': ', '.join(platforms),
            'cluster_count': len(clusters),
            'top2_names': ', '.join(top2_names),
            'clusters': clusters,
            'top1': top1,
            'top2': top2,
            'all_evidence': all_evidence[:20]  # 最多20条证据
        }
    
    @staticmethod
    def _custom_filters():
        """自定义Jinja2过滤器"""
        def index_plus_1(value):
            return value + 1
        
        def first_three(items):
            return items[:3] if items else []
        
        def join_list(items, separator=", "):
            return separator.join(items) if items else ""
        
        return {
            'index_plus_1': index_plus_1,
            'first_three': first_three,
            'join': join_list
        }
    
    @classmethod
    def generate(cls, clusters: List[Dict]) -> str:
        """
        生成报告
        
        Args:
            clusters: 受众簇列表
        
        Returns:
            Markdown格式报告
        """
        # 加载模板
        template_str = cls._load_template()
        
        # 准备数据
        data = cls._prepare_data(clusters)
        
        # 渲染（简化版，不使用Jinja2复杂语法）
        report = template_str
        
        # 替换基础变量
        report = report.replace('{{date}}', data['date'])
        report = report.replace('{{platforms}}', data['platforms'])
        report = report.replace('{{cluster_count}}', str(data['cluster_count']))
        report = report.replace('{{top2_names}}', data['top2_names'])
        
        # 替换Top1/Top2
        if data['top1']:
            report = report.replace('{{top1.role}}', data['top1']['role'])
            report = report.replace('{{top1.scenario}}', data['top1']['scenario'])
            report = report.replace('{{top1.score_card.total_score}}', str(data['top1']['score_card']['total_score']))
            report = report.replace('{{top1.score_card.evidence_count}}', str(data['top1']['score_card']['evidence_count']))
        
        if data['top2']:
            report = report.replace('{{top2.role}}', data['top2']['role'])
            report = report.replace('{{top2.scenario}}', data['top2']['scenario'])
            report = report.replace('{{top2.score_card.total_score}}', str(data['top2']['score_card']['total_score']))
            report = report.replace('{{top2.score_card.evidence_count}}', str(data['top2']['score_card']['evidence_count']))
        
        # 生成簇列表（简化版）
        clusters_section = ""
        for i, cluster in enumerate(data['clusters'], 1):
            clusters_section += f"\n### 簇{i}: {cluster['role']} - {cluster['scenario']}\n\n"
            clusters_section += f"#### {i}.1 受众画像\n"
            clusters_section += f"- **角色**: {cluster['role']}\n"
            clusters_section += f"- **场景**: {cluster['scenario']}\n"
            clusters_section += f"- **KPI约束**: {', '.join(cluster['kpi_constraints'])}\n"
            clusters_section += f"- **证据数量**: {cluster['score_card']['evidence_count']}\n\n"
            
            clusters_section += f"#### {i}.2 核心痛点\n"
            for j, pain in enumerate(cluster['pain_points'][:5], 1):
                clusters_section += f"{j}. {pain}\n"
            clusters_section += "\n"
            
            if cluster['workarounds']:
                clusters_section += f"#### {i}.3 土办法\n"
                for work in cluster['workarounds'][:3]:
                    clusters_section += f"- {work}\n"
                clusters_section += "\n"
            
            clusters_section += f"#### {i}.4 评分卡\n"
            clusters_section += "| 维度 | 得分 | 说明 |\n"
            clusters_section += "|------|------|------|\n"
            sc = cluster['score_card']
            clusters_section += f"| 付费意愿 (WTP) | {sc['wtp_score']}/10 | 基于付费信号数量 |\n"
            clusters_section += f"| 痛苦高频 | {sc['pain_frequency']}/10 | 基于证据数量 |\n"
            clusters_section += f"| 护城河 (Moat) | {sc['moat_score']}/10 | 基于土办法复杂度 |\n"
            clusters_section += f"| GTM难度 | {sc['gtm_score']}/10 | 市场进入难度 |\n"
            clusters_section += f"| **总分** | **{sc['total_score']}/40** | 置信度: {sc['confidence']}% |\n\n"
            
            clusters_section += f"#### {i}.5 证据样本\n"
            for evidence in cluster['evidence_refs'][:3]:
                clusters_section += f"- **[{evidence['platform']}]** {evidence['author']}: {evidence['snippet']}\n"
            clusters_section += "\n---\n"
        
        # 替换簇列表占位符
        report = report.replace('{{#each clusters}}', clusters_section)
        report = report.replace('{{/each}}', '')
        
        # 生成证据附录
        evidence_section = ""
        for i, evidence in enumerate(data['all_evidence'], 1):
            evidence_section += f"**[{i}]** {evidence['platform']} - {evidence['author']} - {evidence.get('time', '')}\n"
            evidence_section += f"> {evidence['text']}\n\n"
        
        report = report.replace('{{#each all_evidence}}', evidence_section)
        
        # 清理未使用的模板标记
        import re
        report = re.sub(r'\{\{#if.*?\}\}', '', report)
        report = re.sub(r'\{\{/if\}\}', '', report)
        report = re.sub(r'\{\{.*?\}\}', '', report)
        
        return report
