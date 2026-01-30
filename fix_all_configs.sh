#!/bin/bash
# 为所有引擎配置文件添加 OpenRouter 自动回退支持

ENGINES=("QueryEngine" "MediaEngine" "InsightEngine")

for ENGINE in "${ENGINES[@]}"; do
    CONFIG_FILE="${ENGINE}/utils/config.py"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "⚠️  $CONFIG_FILE 不存在，跳过"
        continue
    fi
    
    echo "🔧 修复 $CONFIG_FILE..."
    
    # 备份原文件
    cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
    
    # 使用 Python 脚本添加 OpenRouter 支持
    python3 << 'PYTHON_SCRIPT'
import sys
import re

config_file = sys.argv[1]
engine_name = sys.argv[2]

with open(config_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 检查是否已经有 OPENROUTER_API_KEY
if 'OPENROUTER_API_KEY' in content:
    print(f"✅ {config_file} 已经包含 OpenRouter 配置")
    sys.exit(0)

# 1. 添加 model_validator 导入
if 'from pydantic import' in content and 'model_validator' not in content:
    content = re.sub(
        r'from pydantic import ([^\\n]+)',
        r'from pydantic import \1, model_validator',
        content
    )

# 2. 在 Settings 类的第一个字段前添加 OpenRouter 配置
# 找到 class Settings 后的第一个字段定义
pattern = r'(class Settings\([^)]+\):[^\\n]+\\n(?:[^\\n]*"""[^"]*"""[^\\n]*\\n)?)'
replacement = r'''\1    # ================== 统一 OpenRouter 配置 ==================
    OPENROUTER_API_KEY: Optional[str] = Field(None, description="统一的 OpenRouter API Key")
    OPENROUTER_BASE_URL: str = Field("https://openrouter.ai/api/v1", description="OpenRouter API Base URL")
    
'''

content = re.sub(pattern, replacement, content)

# 3. 在 model_config 或 class Config 之前添加 model_validator
# 找到 model_config 或 class Config
validator_code = '''
    @model_validator(mode='after')
    def apply_openrouter_fallback(self):
        """
        如果设置了统一的 OPENROUTER_API_KEY，则未单独配置的引擎自动使用该 Key 和 Base URL。
        """
        if self.OPENROUTER_API_KEY:
            # 主引擎自动回退
            if not self.{ENGINE}_API_KEY:
                object.__setattr__(self, '{ENGINE}_API_KEY', self.OPENROUTER_API_KEY)
                object.__setattr__(self, '{ENGINE}_BASE_URL', self.OPENROUTER_BASE_URL)
        
        return self

'''.replace('{ENGINE}', engine_name.upper() + '_ENGINE')

# 在 model_config 或 class Config 前插入
if 'model_config' in content:
    content = re.sub(r'(\\n    model_config)', validator_code + r'\1', content)
elif 'class Config:' in content:
    content = re.sub(r'(\\n    class Config:)', validator_code + r'\1', content)

with open(config_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ {config_file} 修复完成")
PYTHON_SCRIPT
    python3 - "$CONFIG_FILE" "$ENGINE"
    
done

echo "🎉 所有引擎配置文件修复完成！"
