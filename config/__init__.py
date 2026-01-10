"""
SmartFish 配置加载器
Story 1-1: 配置加载器
"""
import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional

class ConfigLoader:
    """单例配置加载器，启动时加载所有 YAML 配置"""
    
    _instance = None
    _templates: Dict[str, dict] = {}
    _methods: Dict[str, dict] = {}
    _loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> 'ConfigLoader':
        if cls._instance is None:
            cls._instance = cls()
        if not cls._loaded:
            cls._instance._load_all()
        return cls._instance
    
    def _load_all(self):
        """加载所有配置文件"""
        base_path = Path(__file__).parent
        
        # 加载模板元数据
        template_path = base_path / 'template_meta'
        if template_path.exists():
            self._templates = self._load_yaml_dir(template_path)
        
        # 加载分析方法配置
        methods_path = base_path / 'analysis_methods'
        if methods_path.exists():
            self._methods = self._load_yaml_dir(methods_path, recursive=True)
        
        ConfigLoader._loaded = True
    
    def _load_yaml_dir(self, dir_path: Path, recursive: bool = False) -> Dict[str, dict]:
        """加载目录下所有 YAML 文件"""
        result = {}
        pattern = '**/*.yaml' if recursive else '*.yaml'
        
        for yaml_file in dir_path.glob(pattern):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'id' in data:
                        result[data['id']] = data
            except Exception as e:
                print(f"Warning: Failed to load {yaml_file}: {e}")
        
        return result
    
    def get_templates(self) -> List[dict]:
        """获取所有模板元数据列表"""
        return list(self._templates.values())
    
    def get_template(self, template_id: str) -> Optional[dict]:
        """获取单个模板元数据"""
        return self._templates.get(template_id)
    
    def get_methods(self, category: Optional[str] = None) -> List[dict]:
        """获取分析方法列表，可按分类筛选"""
        methods = list(self._methods.values())
        if category:
            methods = [m for m in methods if m.get('category') == category]
        return methods
    
    def get_method(self, method_id: str) -> Optional[dict]:
        """获取单个分析方法"""
        return self._methods.get(method_id)
    
    def get_method_categories(self) -> List[str]:
        """获取所有方法分类"""
        categories = set(m.get('category') for m in self._methods.values() if m.get('category'))
        return sorted(list(categories))
    
    def reload(self):
        """重新加载配置（用于热更新）"""
        ConfigLoader._loaded = False
        self._templates = {}
        self._methods = {}
        self._load_all()


# 便捷函数
def get_config() -> ConfigLoader:
    """获取配置加载器实例"""
    return ConfigLoader.get_instance()


# 导出根目录 config.py 的 settings（延迟导入避免依赖问题）
def _import_settings():
    """延迟导入 settings"""
    try:
        import sys
        from pathlib import Path
        parent = Path(__file__).parent.parent
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        
        # 使用 importlib 避免命名冲突
        import importlib.util
        spec = importlib.util.spec_from_file_location("root_config", parent / "config.py")
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module.settings, module.Settings, module.reload_settings
    except Exception as e:
        print(f"Warning: Could not import settings from root config.py: {e}")
        return None, None, None

settings, Settings, reload_settings = _import_settings()
