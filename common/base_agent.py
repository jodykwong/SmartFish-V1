"""
Base Agent 抽象类 - 消除代码重复

所有 Engine 的共同基类，提供统一的初始化和节点管理。
"""

import os
import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from loguru import logger

# 注意: LLMClient 由各 Engine 自己的模块提供
# 这里只定义接口，不导入具体实现

class BaseDeepSearchAgent(ABC):
    """Deep Search Agent 基类"""
    
    def __init__(self, config):
        """
        初始化 Deep Search Agent
        
        Args:
            config: 配置对象
        """
        self.config = config
        self.llm_client = self._initialize_llm()
        self.search_agency = self._initialize_search_agency()
        self._initialize_nodes()
        
        # 导入 State（延迟导入避免循环依赖）
        from importlib import import_module
        engine_name = self.__class__.__module__.split('.')[0]
        state_module = import_module(f'{engine_name}.state')
        self.state = state_module.State()
        
        os.makedirs(self.config.OUTPUT_DIR, exist_ok=True)
        
        logger.info(f"{self.get_agent_name()} 已初始化")
        logger.info(f"使用LLM: {self.llm_client.get_model_info()}")
        logger.info(f"搜索工具集: {self.get_search_agency_info()}")
    
    @abstractmethod
    def get_agent_name(self) -> str:
        """返回 Agent 名称"""
        pass
    
    @abstractmethod
    def get_search_agency_info(self) -> str:
        """返回搜索工具集信息"""
        pass
    
    @abstractmethod
    def _initialize_llm(self):
        """初始化 LLM 客户端（子类实现）"""
        pass
    
    @abstractmethod
    def _initialize_search_agency(self):
        """初始化搜索工具集（子类实现）"""
        pass
    
    def _initialize_nodes(self):
        """初始化处理节点（通用实现）"""
        from importlib import import_module
        engine_name = self.__class__.__module__.split('.')[0]
        nodes_module = import_module(f'{engine_name}.nodes')
        
        self.first_search_node = nodes_module.FirstSearchNode(self.llm_client)
        self.reflection_node = nodes_module.ReflectionNode(self.llm_client)
        self.first_summary_node = nodes_module.FirstSummaryNode(self.llm_client)
        self.reflection_summary_node = nodes_module.ReflectionSummaryNode(self.llm_client)
        self.report_formatting_node = nodes_module.ReportFormattingNode(self.llm_client)
    
    def _validate_date_format(self, date_str: str) -> bool:
        """
        验证日期格式是否为 YYYY-MM-DD
        
        Args:
            date_str: 日期字符串
            
        Returns:
            是否为有效格式
        """
        if not date_str:
            return False
        
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(pattern, date_str):
            return False
        
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
