"""
MCP客户端基类和通用工具

提供MCP (Model Context Protocol) 客户端的抽象基类，
支持统一的错误处理、重试机制和Cookie管理。
"""

import os
import json
import time
import subprocess
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from loguru import logger


@dataclass
class MCPSearchResult:
    """MCP搜索结果统一数据结构"""
    title: str
    content: str
    url: str
    platform: str  # xiaohongshu, weibo, zhihu, bilibili, douyin
    author: Optional[str] = None
    likes: int = 0
    comments: int = 0
    shares: int = 0
    published_date: Optional[str] = None
    raw_data: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass  
class MCPResponse:
    """MCP响应统一数据结构"""
    success: bool
    platform: str
    query: str
    results: List[MCPSearchResult] = field(default_factory=list)
    answer: Optional[str] = None  # AI摘要
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def webpages(self) -> List[MCPSearchResult]:
        """兼容bmad_adapter的webpages属性"""
        return self.results
    
    def to_dict(self) -> Dict:
        return {
            **asdict(self),
            "results": [r.to_dict() for r in self.results]
        }


class BaseMCPClient(ABC):
    """
    MCP客户端抽象基类
    
    所有社交媒体MCP客户端都需要继承此类并实现:
    - _init_server(): 初始化MCP服务器连接
    - _execute_tool(): 执行MCP工具调用
    - search(): 执行搜索
    """
    
    PLATFORM_NAME: str = "base"  # 子类需要覆盖
    
    def __init__(
        self, 
        max_retries: int = 3, 
        retry_delay: float = 1.0,
        timeout: int = 30,
        cookie_path: Optional[str] = None
    ):
        """
        初始化MCP客户端
        
        Args:
            max_retries: 最大重试次数
            retry_delay: 重试延迟(秒)
            timeout: 请求超时时间(秒)
            cookie_path: Cookie文件路径
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.cookie_path = cookie_path or self._default_cookie_path()
        self._server_process = None
        self._initialized = False
        
    def _default_cookie_path(self) -> str:
        """默认Cookie存储路径"""
        base_dir = os.path.join(os.path.dirname(__file__), "..", "config", "mcp_cookies")
        os.makedirs(base_dir, exist_ok=True)
        return os.path.join(base_dir, f"{self.PLATFORM_NAME}_cookies.json")
        
    @abstractmethod
    def _init_server(self) -> bool:
        """
        初始化MCP服务器连接
        
        Returns:
            是否初始化成功
        """
        pass
        
    @abstractmethod
    def _execute_tool(self, tool_name: str, args: Dict) -> Any:
        """
        执行MCP工具调用
        
        Args:
            tool_name: 工具名称
            args: 工具参数
            
        Returns:
            工具执行结果
        """
        pass
        
    @abstractmethod
    def search(self, query: str, max_results: int = 20) -> MCPResponse:
        """
        执行搜索
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            统一格式的搜索响应
        """
        pass
    
    def comprehensive_search(self, query: str, max_results: int = 20) -> MCPResponse:
        """
        综合搜索接口(兼容bmad_adapter)
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            统一格式的搜索响应
        """
        return self.search(query, max_results)
        
    def _retry_with_backoff(self, func, *args, **kwargs) -> Any:
        """
        带指数退避的重试机制
        
        Args:
            func: 要执行的函数
            *args, **kwargs: 函数参数
            
        Returns:
            函数执行结果
            
        Raises:
            Exception: 重试耗尽后抛出最后一次异常
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    logger.warning(
                        f"[{self.PLATFORM_NAME}] 请求失败 (尝试 {attempt + 1}/{self.max_retries}): {e}"
                        f"\n{delay}秒后重试..."
                    )
                    time.sleep(delay)
                    
        logger.error(f"[{self.PLATFORM_NAME}] 重试耗尽，最后错误: {last_exception}")
        raise last_exception
        
    def load_cookies(self) -> Optional[Dict]:
        """加载保存的Cookie"""
        try:
            if os.path.exists(self.cookie_path):
                with open(self.cookie_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 检查是否过期
                    if data.get("expires_at"):
                        expires = datetime.fromisoformat(data["expires_at"])
                        if expires < datetime.now():
                            logger.warning(f"[{self.PLATFORM_NAME}] Cookie已过期")
                            return None
                    return data.get("cookies")
        except Exception as e:
            logger.error(f"[{self.PLATFORM_NAME}] 加载Cookie失败: {e}")
        return None
        
    def save_cookies(self, cookies: Dict, expires_hours: int = 24):
        """保存Cookie"""
        try:
            expires_at = datetime.now()
            expires_at = expires_at.replace(hour=expires_at.hour + expires_hours)
            
            data = {
                "cookies": cookies,
                "platform": self.PLATFORM_NAME,
                "saved_at": datetime.now().isoformat(),
                "expires_at": expires_at.isoformat()
            }
            
            with open(self.cookie_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"[{self.PLATFORM_NAME}] Cookie已保存")
        except Exception as e:
            logger.error(f"[{self.PLATFORM_NAME}] 保存Cookie失败: {e}")
            
    def refresh_cookies(self) -> bool:
        """
        刷新Cookie (需要重新登录)
        子类可以覆盖此方法实现自动刷新
        
        Returns:
            是否刷新成功
        """
        logger.warning(f"[{self.PLATFORM_NAME}] 需要手动刷新Cookie")
        return False
        
    def is_ready(self) -> bool:
        """检查客户端是否就绪"""
        return self._initialized
        
    def health_check(self) -> Dict:
        """健康检查"""
        return {
            "platform": self.PLATFORM_NAME,
            "initialized": self._initialized,
            "cookie_valid": self.load_cookies() is not None,
            "timestamp": datetime.now().isoformat()
        }
        
    def close(self):
        """关闭客户端，释放资源"""
        if self._server_process:
            try:
                self._server_process.terminate()
                self._server_process.wait(timeout=5)
            except Exception as e:
                logger.error(f"[{self.PLATFORM_NAME}] 关闭服务器失败: {e}")
            finally:
                self._server_process = None
                self._initialized = False


class DataSourceRouter:
    """
    数据源路由器
    
    负责管理多个MCP客户端并根据配置选择合适的数据源
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化数据源路由器
        
        Args:
            config_path: 配置文件路径
        """
        self._clients: Dict[str, BaseMCPClient] = {}
        self._default_client: Optional[BaseMCPClient] = None
        self._config = self._load_config(config_path)
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置"""
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__), "..", "config", "bmad_config.yaml"
            )
        
        try:
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config.get("data_sources", {})
        except Exception as e:
            logger.warning(f"加载数据源配置失败: {e}")
            return {}
            
    def register_client(self, client: BaseMCPClient, is_default: bool = False):
        """
        注册MCP客户端
        
        Args:
            client: MCP客户端实例
            is_default: 是否设为默认客户端
        """
        self._clients[client.PLATFORM_NAME] = client
        if is_default:
            self._default_client = client
        logger.info(f"已注册数据源: {client.PLATFORM_NAME}")
        
    def get_client(self, platform: str) -> Optional[BaseMCPClient]:
        """获取指定平台的客户端"""
        return self._clients.get(platform)
        
    def search_all(self, query: str, max_results: int = 20) -> List[MCPResponse]:
        """
        在所有已注册平台上搜索
        
        Args:
            query: 搜索关键词
            max_results: 每个平台的最大结果数
            
        Returns:
            所有平台的搜索结果列表
        """
        results = []
        for platform, client in self._clients.items():
            try:
                response = client.search(query, max_results)
                results.append(response)
            except Exception as e:
                logger.error(f"[{platform}] 搜索失败: {e}")
                results.append(MCPResponse(
                    success=False,
                    platform=platform,
                    query=query,
                    error=str(e)
                ))
        return results
        
    def search_platforms(
        self, 
        query: str, 
        platforms: List[str],
        max_results: int = 20
    ) -> List[MCPResponse]:
        """
        在指定平台上搜索
        
        Args:
            query: 搜索关键词
            platforms: 平台列表
            max_results: 每个平台的最大结果数
            
        Returns:
            搜索结果列表
        """
        results = []
        for platform in platforms:
            client = self._clients.get(platform)
            if client:
                try:
                    response = client.search(query, max_results)
                    results.append(response)
                except Exception as e:
                    logger.error(f"[{platform}] 搜索失败: {e}")
                    results.append(MCPResponse(
                        success=False,
                        platform=platform,
                        query=query,
                        error=str(e)
                    ))
            else:
                logger.warning(f"平台未注册: {platform}")
        return results
        
    def get_priority_platforms(self, domain: str = None) -> List[str]:
        """
        获取优先搜索的平台列表(基于配置)
        
        Args:
            domain: 可选的领域过滤
            
        Returns:
            平台名称列表
        """
        # 默认优先级
        default_priority = ["xiaohongshu", "weibo", "zhihu", "bilibili", "douyin"]
        
        # 从配置获取
        if domain and domain in self._config:
            return self._config[domain].get("priority_platforms", default_priority)
            
        return self._config.get("priority_platforms", default_priority)
        
    def merge_results(self, responses: List[MCPResponse]) -> MCPResponse:
        """
        合并多个平台的搜索结果
        
        Args:
            responses: 搜索响应列表
            
        Returns:
            合并后的响应
        """
        all_results = []
        all_errors = []
        
        for resp in responses:
            if resp.success:
                all_results.extend(resp.results)
            else:
                all_errors.append(f"{resp.platform}: {resp.error}")
                
        # 按互动量排序
        all_results.sort(
            key=lambda x: x.likes + x.comments * 2 + x.shares * 3,
            reverse=True
        )
        
        return MCPResponse(
            success=len(all_results) > 0,
            platform="merged",
            query=responses[0].query if responses else "",
            results=all_results,
            error="; ".join(all_errors) if all_errors else None
        )
        
    def health_check_all(self) -> Dict:
        """所有客户端健康检查"""
        return {
            platform: client.health_check()
            for platform, client in self._clients.items()
        }
        
    def close_all(self):
        """关闭所有客户端"""
        for client in self._clients.values():
            client.close()
        self._clients.clear()


# 全局路由器实例
_router: Optional[DataSourceRouter] = None


def get_router() -> DataSourceRouter:
    """获取全局数据源路由器"""
    global _router
    if _router is None:
        _router = DataSourceRouter()
    return _router


def init_router(config_path: Optional[str] = None) -> DataSourceRouter:
    """初始化全局数据源路由器"""
    global _router
    _router = DataSourceRouter(config_path)
    return _router
