#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartFish 项目配置检查工具
检查所有必需的配置项是否已正确设置
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from dotenv import load_dotenv

# 加载 .env 文件
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

class ConfigChecker:
    """配置检查器"""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.passed = []
        
    def check_env_file(self) -> bool:
        """检查 .env 文件是否存在"""
        if not env_path.exists():
            self.issues.append("❌ .env 文件不存在，请从 .env.example 复制创建")
            return False
        self.passed.append("✅ .env 文件存在")
        return True
    
    def check_database_config(self) -> bool:
        """检查数据库配置"""
        db_host = os.getenv('DB_HOST', '')
        db_user = os.getenv('DB_USER', '')
        db_password = os.getenv('DB_PASSWORD', '')
        db_name = os.getenv('DB_NAME', '')
        
        # 检查是否使用默认占位符
        if db_host in ['your_db_host', '']:
            self.issues.append("❌ DB_HOST 未配置或使用默认值")
            return False
        if db_user in ['your_db_user', '']:
            self.issues.append("❌ DB_USER 未配置或使用默认值")
            return False
        if db_password in ['your_db_password', '']:
            self.issues.append("❌ DB_PASSWORD 未配置或使用默认值")
            return False
        if db_name in ['your_db_name', '']:
            self.issues.append("❌ DB_NAME 未配置或使用默认值")
            return False
            
        self.passed.append(f"✅ 数据库配置完整: {db_user}@{db_host}/{db_name}")
        return True
    
    def check_llm_config(self) -> bool:
        """检查 LLM 配置"""
        openrouter_key = os.getenv('OPENROUTER_API_KEY', '')
        
        # 检查统一的 OpenRouter 配置
        if openrouter_key and openrouter_key.startswith('sk-or-v1-'):
            self.passed.append(f"✅ OpenRouter API Key 已配置 (统一模式)")
            
            # 检查各引擎的模型配置
            engines = {
                'Insight Engine': 'INSIGHT_ENGINE_MODEL_NAME',
                'Media Engine': 'MEDIA_ENGINE_MODEL_NAME',
                'Query Engine': 'QUERY_ENGINE_MODEL_NAME',
                'Report Engine': 'REPORT_ENGINE_MODEL_NAME',
                'MindSpider': 'MINDSPIDER_MODEL_NAME',
                'Forum Host': 'FORUM_HOST_MODEL_NAME',
                'Keyword Optimizer': 'KEYWORD_OPTIMIZER_MODEL_NAME',
            }
            
            all_models_configured = True
            for engine_name, model_var in engines.items():
                model = os.getenv(model_var, '')
                if model:
                    self.passed.append(f"  ✅ {engine_name}: {model}")
                else:
                    self.warnings.append(f"  ⚠️ {engine_name} 模型未配置")
                    all_models_configured = False
            
            return all_models_configured
        else:
            # 检查各引擎是否单独配置
            self.warnings.append("⚠️ 未使用统一的 OpenRouter 配置，检查各引擎单独配置...")
            
            engines_config = {
                'Insight Engine': ('INSIGHT_ENGINE_API_KEY', 'INSIGHT_ENGINE_MODEL_NAME'),
                'Media Engine': ('MEDIA_ENGINE_API_KEY', 'MEDIA_ENGINE_MODEL_NAME'),
                'Query Engine': ('QUERY_ENGINE_API_KEY', 'QUERY_ENGINE_MODEL_NAME'),
                'Report Engine': ('REPORT_ENGINE_API_KEY', 'REPORT_ENGINE_MODEL_NAME'),
            }
            
            all_configured = True
            for engine_name, (key_var, model_var) in engines_config.items():
                key = os.getenv(key_var, '')
                model = os.getenv(model_var, '')
                
                if key and model:
                    self.passed.append(f"  ✅ {engine_name}: 已配置")
                else:
                    self.issues.append(f"  ❌ {engine_name}: API Key 或模型未配置")
                    all_configured = False
            
            return all_configured
    
    def check_search_tools(self) -> bool:
        """检查搜索工具配置"""
        tavily_key = os.getenv('TAVILY_API_KEY', '')
        search_type = os.getenv('SEARCH_TOOL_TYPE', 'AnspireAPI')
        anspire_key = os.getenv('ANSPIRE_API_KEY', '')
        bocha_key = os.getenv('BOCHA_WEB_SEARCH_API_KEY', '')
        
        has_search_tool = False
        
        if tavily_key and tavily_key.startswith('tvly-'):
            self.passed.append(f"✅ Tavily API Key 已配置")
            has_search_tool = True
        else:
            self.warnings.append("⚠️ Tavily API Key 未配置")
        
        if search_type == 'AnspireAPI':
            if anspire_key:
                self.passed.append(f"✅ Anspire API Key 已配置 (当前搜索工具)")
                has_search_tool = True
            else:
                self.warnings.append("⚠️ Anspire API Key 未配置，但被设为当前搜索工具")
        
        if search_type == 'BochaAPI':
            if bocha_key:
                self.passed.append(f"✅ Bocha API Key 已配置 (当前搜索工具)")
                has_search_tool = True
            else:
                self.warnings.append("⚠️ Bocha API Key 未配置，但被设为当前搜索工具")
        
        if not has_search_tool:
            self.warnings.append("⚠️ 没有配置任何搜索工具 API，部分功能可能受限")
        
        return has_search_tool
    
    def check_server_config(self) -> bool:
        """检查服务器配置"""
        host = os.getenv('HOST', '0.0.0.0')
        port = os.getenv('PORT', '5000')
        
        self.passed.append(f"✅ 服务器配置: {host}:{port}")
        return True
    
    def check_dependencies(self) -> bool:
        """检查依赖是否安装"""
        required_packages = [
            'flask',
            'openai',
            'pandas',
            'sqlalchemy',
            'pydantic',
            'python-dotenv',
            'loguru'
        ]
        
        missing = []
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing.append(package)
        
        if missing:
            self.issues.append(f"❌ 缺少依赖包: {', '.join(missing)}")
            self.issues.append("   请运行: pip install -r requirements.txt")
            return False
        
        self.passed.append(f"✅ 核心依赖包已安装")
        return True
    
    def run_all_checks(self) -> bool:
        """运行所有检查"""
        print("=" * 60)
        print("🐟 SmartFish 项目配置检查")
        print("=" * 60)
        print()
        
        checks = [
            ("环境文件", self.check_env_file),
            ("服务器配置", self.check_server_config),
            ("数据库配置", self.check_database_config),
            ("LLM 配置", self.check_llm_config),
            ("搜索工具配置", self.check_search_tools),
            ("依赖包", self.check_dependencies),
        ]
        
        all_passed = True
        for name, check_func in checks:
            print(f"检查 {name}...")
            result = check_func()
            if not result:
                all_passed = False
            print()
        
        # 输出结果
        print("=" * 60)
        print("📊 检查结果汇总")
        print("=" * 60)
        print()
        
        if self.passed:
            print("✅ 通过的检查项:")
            for item in self.passed:
                print(f"  {item}")
            print()
        
        if self.warnings:
            print("⚠️  警告项 (不影响启动，但可能影响部分功能):")
            for item in self.warnings:
                print(f"  {item}")
            print()
        
        if self.issues:
            print("❌ 错误项 (必须修复才能启动):")
            for item in self.issues:
                print(f"  {item}")
            print()
        
        print("=" * 60)
        
        if all_passed and not self.issues:
            print("🎉 配置检查通过！项目可以启动。")
            print()
            print("启动命令:")
            print("  python app.py")
            print()
            print("或使用 Docker:")
            print("  ./deploy.sh")
            print("=" * 60)
            return True
        else:
            print("⚠️  配置存在问题，请修复后再启动项目。")
            print()
            print("修复建议:")
            if not env_path.exists():
                print("  1. 复制配置文件: cp .env.example .env")
            if any("数据库" in issue for issue in self.issues):
                print("  2. 配置数据库连接信息 (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)")
            if any("LLM" in issue or "API" in issue for issue in self.issues):
                print("  3. 配置 LLM API Key:")
                print("     - 推荐: 使用 OpenRouter (https://openrouter.ai/keys)")
                print("     - 填写 OPENROUTER_API_KEY 即可自动配置所有引擎")
            if any("依赖" in issue for issue in self.issues):
                print("  4. 安装依赖: pip install -r requirements.txt")
            print("=" * 60)
            return False


def main():
    """主函数"""
    checker = ConfigChecker()
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
