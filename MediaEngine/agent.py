"""
Deep Search Agent主类
整合所有模块，实现完整的深度搜索流程
"""

from typing import Optional
from loguru import logger

from common.base_agent import BaseDeepSearchAgent
from .llms import LLMClient
from .tools import load_agent_from_config
from .utils import settings, Settings


class DeepSearchAgent(BaseDeepSearchAgent):
    """Media Engine Deep Search Agent"""
    
    def __init__(self, config: Optional[Settings] = None):
        """初始化 Media Agent"""
        super().__init__(config or settings)
    
    def get_agent_name(self) -> str:
        return "Media Agent"
    
    def get_search_agency_info(self) -> str:
        return f"{type(self.search_agency).__name__}"
    
    def _initialize_llm(self) -> LLMClient:
        """初始化LLM客户端"""
        return LLMClient(
            api_key=(self.config.MEDIA_ENGINE_API_KEY or self.config.MINDSPIDER_API_KEY),
            model_name=(self.config.MEDIA_ENGINE_MODEL_NAME or self.config.MINDSPIDER_MODEL_NAME),
            base_url=(self.config.MEDIA_ENGINE_BASE_URL or self.config.MINDSPIDER_BASE_URL),
        )
    
    def _initialize_search_agency(self):
        """初始化搜索工具集（自动选择可用的搜索引擎）"""
        return load_agent_from_config()


def create_agent(config: Optional[Settings] = None) -> DeepSearchAgent:
    """创建 Media Agent 实例"""
    return DeepSearchAgent(config)
