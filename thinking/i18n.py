"""
国际化支持模块
"""

MESSAGES = {
    'zh': {
        'unauthorized': '未授权访问',
        'title_required': '标题不能为空',
        'title_too_long': '标题过长',
        'entry_not_found': '条目不存在',
        'gate_fail': 'Gate评估失败',
        'gate_pass': 'Gate评估通过',
    },
    'en': {
        'unauthorized': 'Unauthorized access',
        'title_required': 'Title is required',
        'title_too_long': 'Title is too long',
        'entry_not_found': 'Entry not found',
        'gate_fail': 'Gate evaluation failed',
        'gate_pass': 'Gate evaluation passed',
    }
}

def get_message(key, lang='zh'):
    """获取国际化消息"""
    return MESSAGES.get(lang, MESSAGES['zh']).get(key, key)
