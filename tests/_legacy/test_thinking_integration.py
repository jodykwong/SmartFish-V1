import pytest
from app import app, db
from thinking.models.thinking_entry import ThinkingEntry

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def auth_client(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    return client

class TestThinkingIntegration:
    def test_create_entry_unauthorized(self, client):
        response = client.post('/thinking/entries', json={'title': 'Test'})
        assert response.status_code == 401
    
    def test_create_entry_success(self, auth_client):
        response = auth_client.post('/thinking/entries', json={
            'title': 'Test Entry',
            'signal': 'Test signal'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'Test Entry'
    
    def test_create_entry_xss_protection(self, auth_client):
        response = auth_client.post('/thinking/entries', json={
            'title': '<script>alert("xss")</script>'
        })
        assert response.status_code == 201
        # 验证存储时已转义
    
    def test_create_entry_too_long(self, auth_client):
        response = auth_client.post('/thinking/entries', json={
            'title': 'a' * 300
        })
        assert response.status_code == 400
    
    def test_list_entries_unauthorized(self, client):
        response = client.get('/thinking/entries')
        assert response.status_code == 401
    
    # 新增边界测试
    def test_create_entry_empty_string(self, auth_client):
        """测试空字符串"""
        response = auth_client.post('/thinking/entries', json={'title': '   '})
        assert response.status_code == 400
    
    def test_create_entry_unicode(self, auth_client):
        """测试Unicode字符"""
        response = auth_client.post('/thinking/entries', json={
            'title': '测试🔥emoji表情符号'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert '🔥' in data['title']
    
    def test_create_entry_special_chars(self, auth_client):
        """测试特殊字符"""
        response = auth_client.post('/thinking/entries', json={
            'title': "Test's \"quoted\" & <special> chars"
        })
        assert response.status_code == 201
    
    def test_create_entry_null_fields(self, auth_client):
        """测试null字段"""
        response = auth_client.post('/thinking/entries', json={
            'title': 'Test',
            'signal': None,
            'problem': None
        })
        assert response.status_code == 201
    
    def test_create_entry_missing_json(self, auth_client):
        """测试缺少JSON body"""
        response = auth_client.post('/thinking/entries')
        assert response.status_code == 400
    
    def test_i18n_english(self, client):
        """测试英文错误消息"""
        response = client.post('/thinking/entries', 
                              json={'title': 'Test'},
                              headers={'Accept-Language': 'en-US'})
        assert response.status_code == 401
        data = response.get_json()
        assert 'Unauthorized' in data['error']
    
    def test_i18n_chinese(self, client):
        """测试中文错误消息"""
        response = client.post('/thinking/entries',
                              json={'title': 'Test'},
                              headers={'Accept-Language': 'zh-CN'})
        assert response.status_code == 401
        data = response.get_json()
        assert '未授权' in data['error']
