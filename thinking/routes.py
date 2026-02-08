from flask import Blueprint, request, jsonify, session, send_file, render_template
from markupsafe import escape
from thinking.services.entry_service import EntryService
from thinking.services.gate_service import GateService
from thinking.services.audience_service import AudienceService
from thinking.services.routing_service import RoutingService
from thinking.services.artifact_service import ArtifactService
from thinking.services.weekly_review_service import WeeklyReviewService
from thinking.services.task_service import TaskService
from thinking.services.zero_to_sold_service import ZeroToSoldService
from thinking.i18n import get_message
from thinking.rate_limit import init_limiter
import logging

logger = logging.getLogger(__name__)

thinking_bp = Blueprint('thinking', __name__, url_prefix='/thinking', template_folder='templates')

# 初始化速率限制器 (在 app 注册后调用)
limiter = None

def init_thinking_limiter(app):
    """在 app 注册后初始化限制器"""
    global limiter
    limiter = init_limiter(app)
    return limiter
gate_service = GateService()
artifact_service = ArtifactService()
weekly_review_service = WeeklyReviewService()
task_service = TaskService()
zts_service = ZeroToSoldService()

def get_lang():
    """获取请求语言"""
    return request.headers.get('Accept-Language', 'zh')[:2]

def get_current_user_id():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': get_message('unauthorized', get_lang())}), 401
    return user_id

@thinking_bp.route('/zero-to-sold', methods=['GET'])
def zero_to_sold_wizard():
    """Zero to Sold向导页面"""
    return render_template('zero_to_sold.html')

@thinking_bp.route('/entries', methods=['GET'])
def list_entries():
    user_id = get_current_user_id()
    if isinstance(user_id, tuple):
        return user_id
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    
    pagination = EntryService.list_entries(user_id, status, page)
    
    return jsonify({
        'entries': [e.to_dict() for e in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    })

@thinking_bp.route('/entries', methods=['POST'])
def create_entry():
    user_id = get_current_user_id()
    if isinstance(user_id, tuple):
        return user_id
    data = request.json
    lang = get_lang()
    
    if not data or not data.get('title'):
        return jsonify({'error': get_message('title_required', lang)}), 400
    
    # 输入验证
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'error': get_message('title_required', lang)}), 400
    if len(title) > 255:
        return jsonify({'error': get_message('title_too_long', lang)}), 400
    
    entry = EntryService.create_entry(user_id, data)
    return jsonify(entry.to_dict()), 201

@thinking_bp.route('/entries/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    user_id = get_current_user_id()
    if isinstance(user_id, tuple):
        return user_id
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': get_message('entry_not_found', get_lang())}), 404
    
    return jsonify(entry.to_dict())

@thinking_bp.route('/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    user_id = get_current_user_id()
    data = request.json
    
    entry = EntryService.update_entry(entry_id, user_id, data)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    return jsonify(entry.to_dict())

@thinking_bp.route('/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    user_id = get_current_user_id()
    
    if EntryService.delete_entry(entry_id, user_id):
        return '', 204
    
    return jsonify({'error': '条目不存在'}), 404


@thinking_bp.route('/entries/<int:entry_id>/gate', methods=['POST'])
def evaluate_gate(entry_id):
    """执行Gate检查"""
    user_id = get_current_user_id()
    
    # 验证条目所有权
    entry = EntryService.get_entry(entry_id, user_id)
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    data = request.json
    inputs = data.get('inputs', [])
    
    if len(inputs) != 4:
        return jsonify({'error': '需要提供4层过滤器的输入'}), 400
    
    try:
        result = gate_service.evaluate(entry_id, inputs)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@thinking_bp.route('/entries/<int:entry_id>/gate', methods=['GET'])
def get_gate_review(entry_id):
    """获取Gate审查记录"""
    user_id = get_current_user_id()
    
    # 验证条目所有权
    entry = EntryService.get_entry(entry_id, user_id)
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    review = gate_service.get_review(entry_id)
    if not review:
        return jsonify({'error': '未找到Gate审查记录'}), 404
    
    return jsonify(review.to_dict())


@thinking_bp.route('/entries/<int:entry_id>/routing', methods=['GET'])
def suggest_routing(entry_id):
    """获取路由建议"""
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    suggestion = RoutingService.suggest_routing(entry)
    return jsonify(suggestion)

@thinking_bp.route('/entries/<int:entry_id>/artifacts', methods=['POST'])
def generate_artifact(entry_id):
    """生成工件"""
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    # 检查Gate是否通过
    gate_review = gate_service.get_review(entry_id)
    if not gate_review or gate_review.decision != 'pass':
        return jsonify({'error': 'Gate检查未通过，无法生成工件'}), 400
    
    data = request.json
    artifact_type = data.get('type', 'tech-spec')
    
    if artifact_type not in ['tech-spec', 'product-brief', 'prd']:
        return jsonify({'error': '不支持的工件类型'}), 400
    
    try:
        artifact = artifact_service.generate_artifact(entry, artifact_type)
        return jsonify(artifact.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@thinking_bp.route('/entries/<int:entry_id>/artifacts', methods=['GET'])
def list_artifacts(entry_id):
    """获取条目的所有工件"""
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    artifacts = artifact_service.get_artifacts(entry_id)
    return jsonify([a.to_dict() for a in artifacts])

@thinking_bp.route('/artifacts/<int:artifact_id>/download', methods=['GET'])
def download_artifact(artifact_id):
    """下载工件"""
    from thinking.models.artifact import Artifact
    artifact = Artifact.query.get(artifact_id)
    
    if not artifact:
        return jsonify({'error': '工件不存在'}), 404
    
    return send_file(artifact.path, as_attachment=True)


@thinking_bp.route('/weekly-review', methods=['GET'])
def get_weekly_review():
    """获取周度评审数据"""
    user_id = get_current_user_id()
    days = request.args.get('days', 7, type=int)
    
    entries = weekly_review_service.get_weekly_entries(user_id, days)
    stats = weekly_review_service.calculate_stats(entries)
    
    return jsonify({
        'entries': [e.to_dict() for e in entries],
        'stats': stats
    })

@thinking_bp.route('/weekly-review/plan', methods=['POST'])
def generate_weekly_plan():
    """生成周度计划"""
    user_id = get_current_user_id()
    data = request.json
    
    # 获取打分数据
    scored_entries = data.get('entries', [])
    top_n = data.get('top_n', 3)
    
    if not scored_entries:
        return jsonify({'error': '请至少选择一个条目'}), 400
    
    # 补充完整条目信息
    for item in scored_entries:
        entry = EntryService.get_entry(item['entry_id'], user_id)
        if entry:
            item['title'] = entry.title
            item['problem'] = entry.problem
            item['success_metric'] = entry.success_metric
            item['constraints'] = entry.constraints
    
    try:
        filepath = weekly_review_service.generate_weekly_plan(scored_entries, top_n)
        return jsonify({
            'success': True,
            'filepath': filepath,
            'message': f'周度计划已生成: {filepath}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@thinking_bp.route('/entries/<int:entry_id>/research', methods=['POST'])
def create_research_task(entry_id):
    """创建研究任务"""
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    data = request.json
    engine = data.get('engine', 'QueryEngine')
    query = data.get('query', entry.evidence_needed)
    task_type = data.get('task_type', 'evidence_research')
    
    if not query:
        return jsonify({'error': '请提供查询内容'}), 400
    
    try:
        task = task_service.create_task(entry_id, engine, query, task_type)
        return jsonify(task.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@thinking_bp.route('/entries/<int:entry_id>/research', methods=['GET'])
def list_research_tasks(entry_id):
    """获取条目的所有研究任务"""
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    tasks = task_service.get_entry_tasks(entry_id)
    return jsonify([t.to_dict() for t in tasks])

@thinking_bp.route('/research/<int:task_id>', methods=['GET'])
def get_research_task(task_id):
    """获取研究任务详情"""
    task = task_service.get_task(task_id)
    
    if not task:
        return jsonify({'error': '任务不存在'}), 404
    
    return jsonify(task.to_dict())

@thinking_bp.route('/research/<int:task_id>/backfill', methods=['POST'])
def backfill_evidence(task_id):
    """回填证据到条目"""
    data = request.json
    entry_id = data.get('entry_id')
    
    if not entry_id:
        return jsonify({'error': '请提供entry_id'}), 400
    
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    result = task_service.backfill_evidence(task_id, entry_id)
    
    if result:
        return jsonify({'success': True, 'message': '证据已回填'})
    else:
        return jsonify({'error': '回填失败，任务可能未完成'}), 400


@thinking_bp.route('/entries/<int:entry_id>/problem-score', methods=['POST'])
def score_problem(entry_id):
    """问题强度评分"""
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    data = request.json
    importance = data.get('importance', 5)
    urgency = data.get('urgency', 5)
    
    result = zts_service.score_problem_intensity(importance, urgency)
    
    # 更新条目
    entry.problem_intensity_score = result['score']
    from app import db
    db.session.commit()
    
    return jsonify(result)

@thinking_bp.route('/entries/<int:entry_id>/interview-guide', methods=['POST'])
def generate_interview_guide(entry_id):
    """生成访谈脚本"""
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    try:
        filepath = zts_service.generate_interview_guide(entry)
        return jsonify({'success': True, 'filepath': filepath})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@thinking_bp.route('/entries/<int:entry_id>/market-research', methods=['POST'])
def generate_market_research(entry_id):
    """生成市场研究报告"""
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    data = request.json
    research_data = data.get('research_data', {})
    
    try:
        filepath = zts_service.generate_market_research(entry, research_data)
        return jsonify({'success': True, 'filepath': filepath})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@thinking_bp.route('/entries/<int:entry_id>/market-review', methods=['POST'])
def generate_market_review(entry_id):
    """生成市场转向复核"""
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    data = request.json
    review_data = data.get('review_data', {})
    
    try:
        filepath = zts_service.generate_market_review(entry, review_data)
        return jsonify({'success': True, 'filepath': filepath})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== Audience First API ====================

@thinking_bp.route('/entries/<int:entry_id>/audience-analysis', methods=['POST'])
def analyze_audiences(entry_id):
    """触发受众分析"""
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    data = request.json
    raw_data = data.get('raw_data', [])
    max_clusters = data.get('max_clusters', 5)
    
    try:
        clusters = AudienceService.analyze_audiences(entry_id, raw_data, max_clusters)
        return jsonify({
            'success': True,
            'cluster_count': len(clusters),
            'clusters': clusters
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@thinking_bp.route('/entries/<int:entry_id>/audience-clusters', methods=['GET'])
def get_audience_clusters(entry_id):
    """获取受众簇列表"""
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    try:
        clusters = AudienceService.get_clusters_by_entry(entry_id)
        return jsonify({
            'success': True,
            'clusters': clusters
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@thinking_bp.route('/entries/<int:entry_id>/audience-top', methods=['GET'])
def get_top_audiences(entry_id):
    """获取Top N受众簇"""
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    top_n = request.args.get('top_n', 2, type=int)
    
    try:
        clusters = AudienceService.get_top_clusters(entry_id, top_n)
        return jsonify({
            'success': True,
            'top_clusters': clusters
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@thinking_bp.route('/entries/<int:entry_id>/audience-report', methods=['GET'])
def get_audience_report(entry_id):
    """获取受众分析报告"""
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    try:
        report = AudienceService.generate_report(entry_id)
        return jsonify({
            'success': True,
            'report': report
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@thinking_bp.route('/entries/<int:entry_id>/audience-debate', methods=['POST'])
def debate_audience_clusters(entry_id):
    """对受众簇进行辩论"""
    user_id = get_current_user_id()
    entry = EntryService.get_entry(entry_id, user_id)
    
    if not entry:
        return jsonify({'error': '条目不存在'}), 404
    
    data = request.json or {}
    top_n = data.get('top_n', 2)
    
    try:
        debates = AudienceService.debate_clusters(entry_id, top_n=top_n)
        return jsonify({
            'success': True,
            'debates': debates
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
