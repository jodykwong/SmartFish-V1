"""
BMAD Method 2.0 Phase 0 验证工具适配器

此模块提供痛点发现和用户验证的核心功能，
整合SmartFish的舆情分析能力服务于BMAD验证流程。
"""

import os
import yaml
import json
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, field, asdict
from datetime import datetime
from loguru import logger

# 类型检查时导入（不会在运行时执行）
if TYPE_CHECKING:
    from QueryEngine.tools.search import TavilyNewsAgency, TavilyResponse


@dataclass
class PainPoint:
    """痛点数据结构"""
    id: str
    title: str                          # 痛点标题
    description: str                    # 痛点描述
    domain: str                         # 所属领域
    keywords: List[str]                 # 相关关键词
    user_quotes: List[str] = field(default_factory=list)  # 用户原话引用
    mention_count: int = 0              # 提及次数
    user_confirmations: int = 0         # 用户确认数
    sentiment_score: float = 0.0        # 情感得分 (-1到1)
    commercial_potential: float = 0.0   # 商业潜力 (0到1)
    sources: List[Dict] = field(default_factory=list)     # 数据来源
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ValidationResult:
    """验证结果数据结构"""
    pain_point_id: str
    is_valid: bool
    user_confirmations: int
    payment_willingness: float          # 付费意愿比例
    confidence_score: float             # 置信度
    feedback_summary: str               # 反馈摘要
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Quote:
    """用户引用数据结构"""
    text: str
    source: str
    url: Optional[str] = None
    date: Optional[str] = None
    sentiment: str = "neutral"


class DomainConfig:
    """领域配置管理类"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__), 
                "config", 
                "bmad_config.yaml"
            )
        self.config = self._load_config(config_path)
        
    def _load_config(self, path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"配置文件未找到: {path}，使用默认配置")
            return self._default_config()
            
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "validation": {
                "min_pain_points": 3,
                "min_user_confirmations": 3,
                "min_strong_confirmation": 5,
                "min_payment_willingness": 0.3
            },
            "domains": {
                "ai_chat_tools": {
                    "name": "AI聊天工具",
                    "keywords": ["Claude", "ChatGPT", "AI助手"],
                    "pain_keywords": ["上下文丢失", "多平台切换"]
                }
            }
        }
        
    def get_domain(self, domain_key: str) -> Optional[Dict]:
        """获取领域配置"""
        return self.config.get("domains", {}).get(domain_key)
        
    def get_all_domains(self) -> Dict:
        """获取所有领域配置"""
        return self.config.get("domains", {})
        
    def get_validation_standards(self) -> Dict:
        """获取验证标准"""
        return self.config.get("validation", {})


class BMADPainPointDiscovery:
    """
    BMAD痛点发现核心类
    
    负责:
    1. 通过搜索API发现潜在痛点
    2. 验证痛点频率和用户数量
    3. 提取用户原话引用
    4. 评估商业潜力
    
    数据源策略:
    1. DuckDuckGo (免费、通用)
    2. 社媒 MCP (免费、深度) - 小红书/微博/知乎/B站/抖音
    3. Tavily (付费备选)
    """
    
    def __init__(self, config: DomainConfig = None, use_mcp: bool = True):
        self.config = config or DomainConfig()
        self._search_client = None  # DuckDuckGo客户端
        self._mcp_router = None     # MCP数据源路由器
        self.use_mcp = use_mcp      # 是否启用MCP
        self.discovered_pain_points: List[PainPoint] = []
        
    @property
    def search_client(self):
        """使用 DuckDuckGo 免费搜索引擎（经验证与付费 API 效果相当）"""
        if self._search_client is None:
            try:
                from MediaEngine.tools.search import DuckDuckGoSearch
                self._search_client = DuckDuckGoSearch()
                logger.info("BMAD 痛点发现使用搜索引擎: DuckDuckGoSearch (免费)")
            except Exception as e:
                logger.error(f"初始化搜索客户端失败: {e}")
                raise
        return self._search_client
        
    @property
    def mcp_router(self):
        """MCP数据源路由器 (延迟初始化)"""
        if self._mcp_router is None and self.use_mcp:
            try:
                from mcp_clients import DataSourceRouter
                self._mcp_router = DataSourceRouter()
                self._init_mcp_clients()
                logger.info("BMAD 已启用 MCP 社交媒体数据源")
            except Exception as e:
                logger.warning(f"初始化MCP路由器失败: {e}，将仅使用DuckDuckGo")
                self.use_mcp = False
        return self._mcp_router
        
    def _init_mcp_clients(self):
        """初始化并注册所有MCP客户端"""
        if not self._mcp_router:
            return
            
        try:
            # 按优先级注册MCP客户端
            from mcp_clients.xiaohongshu import XiaohongshuMCPClient
            from mcp_clients.weibo import WeiboMCPClient
            from mcp_clients.zhihu import ZhihuMCPClient
            from mcp_clients.bilibili import BilibiliMCPClient
            from mcp_clients.douyin import DouyinMCPClient
            from mcp_clients.video_sum import VideoSumMCPClient
            
            clients = [
                (XiaohongshuMCPClient, True),   # 小红书，设为默认
                (WeiboMCPClient, False),
                (ZhihuMCPClient, False),
                (BilibiliMCPClient, False),
                (DouyinMCPClient, False),
                (VideoSumMCPClient, False),
            ]
            
            for client_class, is_default in clients:
                try:
                    client = client_class()
                    self._mcp_router.register_client(client, is_default=is_default)
                except Exception as e:
                    logger.warning(f"注册 {client_class.__name__} 失败: {e}")
                    
        except ImportError as e:
            logger.warning(f"MCP客户端模块导入失败: {e}")
        
    def discover_pain_points(
        self, 
        domain: str, 
        max_results: int = 50,
        platforms: List[str] = None
    ) -> List[PainPoint]:
        """
        发现指定领域的痛点
        
        数据源策略:
        1. DuckDuckGo 通用搜索 (公开网页)
        2. MCP 社交媒体搜索 (小红书/微博/知乎/B站/抖音) - 如果启用
        
        Args:
            domain: 领域键名 (如 'ai_chat_tools')
            max_results: 最大搜索结果数
            platforms: 指定MCP平台列表，默认使用配置的优先平台
            
        Returns:
            发现的痛点列表
        """
        domain_config = self.config.get_domain(domain)
        if not domain_config:
            logger.error(f"未找到领域配置: {domain}")
            return []
            
        logger.info(f"开始发现领域 [{domain_config.get('name', domain)}] 的痛点...")
        
        pain_points = []
        keywords = domain_config.get("keywords", [])
        pain_keywords = domain_config.get("pain_keywords", [])
        
        # 1. DuckDuckGo 通用搜索
        logger.info("[数据源1] DuckDuckGo 通用搜索...")
        for keyword in keywords[:3]:
            for pain_kw in pain_keywords[:5]:
                query = f"{keyword} {pain_kw} 问题 吐槽"
                
                try:
                    response = self.search_client.comprehensive_search(query, max_results=15)
                    pain_point = self._extract_pain_point(
                        response, domain, keyword, pain_kw
                    )
                    if pain_point:
                        pain_points.append(pain_point)
                except Exception as e:
                    logger.error(f"DuckDuckGo搜索失败 [{query}]: {e}")
        
        # 2. MCP 社交媒体搜索 (如果启用)
        if self.use_mcp and self.mcp_router:
            mcp_pain_points = self._discover_from_mcp(
                domain, keywords, pain_keywords, platforms
            )
            pain_points.extend(mcp_pain_points)
                    
        # 去重和聚类
        merged_points = self._merge_similar_pain_points(pain_points)
        self.discovered_pain_points.extend(merged_points)
        
        logger.info(f"发现 {len(merged_points)} 个痛点 (DuckDuckGo + MCP)")
        return merged_points
        
    def _discover_from_mcp(
        self,
        domain: str,
        keywords: List[str],
        pain_keywords: List[str],
        platforms: List[str] = None
    ) -> List[PainPoint]:
        """
        从MCP社交媒体平台发现痛点
        
        Args:
            domain: 领域
            keywords: 关键词列表
            pain_keywords: 痛点关键词列表
            platforms: 指定平台列表
            
        Returns:
            发现的痛点列表
        """
        pain_points = []
        
        # 获取要搜索的平台
        if platforms is None:
            platforms = self.mcp_router.get_priority_platforms(domain)
            
        logger.info(f"[数据源2] MCP 社交媒体搜索: {platforms}")
        
        for keyword in keywords[:2]:  # MCP搜索限制更严格
            for pain_kw in pain_keywords[:3]:
                query = f"{keyword} {pain_kw}"
                
                try:
                    # 多平台并行搜索
                    responses = self.mcp_router.search_platforms(
                        query, platforms, max_results=10
                    )
                    
                    for response in responses:
                        if response.success:
                            pain_point = self._extract_mcp_pain_point(
                                response, domain, keyword, pain_kw
                            )
                            if pain_point:
                                pain_points.append(pain_point)
                                
                except Exception as e:
                    logger.error(f"MCP搜索失败 [{query}]: {e}")
                    
        return pain_points
        
    def _extract_mcp_pain_point(
        self,
        response,  # MCPResponse
        domain: str,
        keyword: str,
        pain_keyword: str
    ) -> Optional[PainPoint]:
        """从MCP响应中提取痛点信息"""
        results = response.results
        if not results:
            return None
            
        # 提取用户引用
        quotes = []
        sources = []
        total_engagement = 0
        
        for result in results[:10]:
            if result.content:
                quotes.append(result.content[:200])
                sources.append({
                    "title": result.title,
                    "url": result.url,
                    "platform": result.platform,
                    "author": result.author,
                    "likes": result.likes,
                    "comments": result.comments
                })
                total_engagement += result.likes + result.comments * 2
                
        if not quotes:
            return None
            
        sentiment_score = self._calculate_sentiment(quotes)
        
        pain_point = PainPoint(
            id=f"pp_{domain}_{response.platform}_{len(self.discovered_pain_points) + 1}",
            title=f"{keyword} - {pain_keyword} ({response.platform})",
            description=response.answer or f"来自{response.platform}的用户反馈关于{keyword}的{pain_keyword}问题",
            domain=domain,
            keywords=[keyword, pain_keyword, response.platform],
            user_quotes=quotes[:5],
            mention_count=len(results),
            sentiment_score=sentiment_score,
            commercial_potential=min(total_engagement / 1000, 1.0),  # 基于互动量估算
            sources=sources
        )
        
        return pain_point
        
    def _extract_pain_point(
        self, 
        response,  # 支持 AnspireResponse/BochaResponse/DuckDuckGo 响应
        domain: str,
        keyword: str,
        pain_keyword: str
    ) -> Optional[PainPoint]:
        """从搜索结果中提取痛点信息（兼容多种搜索引擎响应）"""
        # 兼容不同的响应格式：webpages (Anspire/Bocha) 或 results (Tavily)
        results = getattr(response, 'webpages', None) or getattr(response, 'results', [])
        if not results:
            return None
            
        # 提取用户引用
        quotes = []
        sources = []
        
        for result in results[:10]:
            # 兼容不同字段名：snippet/content
            content = getattr(result, 'snippet', None) or getattr(result, 'content', '')
            if content:
                quotes.append(content[:200])
                sources.append({
                    "title": getattr(result, 'name', '') or getattr(result, 'title', ''),
                    "url": getattr(result, 'url', ''),
                    "date": getattr(result, 'date_last_crawled', None) or getattr(result, 'published_date', None)
                })
                
        if not quotes:
            return None
            
        # 计算情感得分 (简化版，后续可集成情感分析模型)
        sentiment_score = self._calculate_sentiment(quotes)
        
        # 获取 AI 摘要（如果可用）
        answer = getattr(response, 'answer', None) or f"用户反馈关于{keyword}的{pain_keyword}问题"
        
        pain_point = PainPoint(
            id=f"pp_{domain}_{len(self.discovered_pain_points) + 1}",
            title=f"{keyword} - {pain_keyword}",
            description=answer,
            domain=domain,
            keywords=[keyword, pain_keyword],
            user_quotes=quotes[:5],
            mention_count=len(results),
            sentiment_score=sentiment_score,
            sources=sources
        )
        
        return pain_point
        
    def _calculate_sentiment(self, texts: List[str]) -> float:
        """
        计算文本情感得分 (增强版)
        
        使用策略:
        1. 优先使用 SVM+XGBoost 集成模型 (准确率 80%+)
        2. 模型不可用时自动回退到关键词匹配
        
        Args:
            texts: 文本列表
            
        Returns:
            情感得分 (-1 到 1，负数表示负面情绪)
        """
        if not texts:
            return 0.0
            
        try:
            # 尝试使用增强型情感分析器
            from sentiment_analyzer import get_sentiment_analyzer
            analyzer = get_sentiment_analyzer()
            return analyzer.calculate_average_score(texts)
        except ImportError:
            logger.warning("无法导入增强型情感分析器，使用简化版")
            return self._calculate_sentiment_simple(texts)
        except Exception as e:
            logger.warning(f"增强型情感分析失败: {e}，使用简化版")
            return self._calculate_sentiment_simple(texts)
            
    def _calculate_sentiment_simple(self, texts: List[str]) -> float:
        """计算文本情感得分 (简化版，关键词匹配)"""
        negative_words = [
            "问题", "困难", "失败", "烦", "卡", "慢", "差", "难用", "吐槽", "垃圾",
            "崩溃", "bug", "闪退", "报错", "错误", "难受", "无语", "坑", "太烂",
            "卡顿", "延迟", "超时", "失望", "气死", "无奈"
        ]
        positive_words = [
            "好", "棒", "赞", "方便", "喜欢", "推荐", "满意", "完美", "优秀",
            "好用", "实用", "高效", "快速", "流畅", "稳定", "给力", "神器"
        ]
        
        neg_count = 0
        pos_count = 0
        
        for text in texts:
            for word in negative_words:
                neg_count += text.count(word)
            for word in positive_words:
                pos_count += text.count(word)
                
        total = neg_count + pos_count
        if total == 0:
            return 0.0
        return (pos_count - neg_count) / total
        
    def _merge_similar_pain_points(self, pain_points: List[PainPoint]) -> List[PainPoint]:
        """合并相似痛点 (简化版，基于关键词匹配)"""
        if not pain_points:
            return []
            
        merged = []
        used = set()
        
        for i, pp1 in enumerate(pain_points):
            if i in used:
                continue
                
            # 查找相似痛点
            for j, pp2 in enumerate(pain_points[i+1:], i+1):
                if j in used:
                    continue
                    
                # 如果有相同关键词，合并
                if set(pp1.keywords) & set(pp2.keywords):
                    pp1.user_quotes.extend(pp2.user_quotes[:3])
                    pp1.mention_count += pp2.mention_count
                    pp1.sources.extend(pp2.sources[:3])
                    used.add(j)
                    
            merged.append(pp1)
            used.add(i)
            
        return merged
        
    def validate_frequency(self, pain_point: PainPoint) -> ValidationResult:
        """
        验证痛点的频率和用户确认数
        
        Args:
            pain_point: 待验证的痛点
            
        Returns:
            验证结果
        """
        standards = self.config.get_validation_standards()
        min_confirmations = standards.get("min_user_confirmations", 3)
        
        # 基于提及次数估算用户确认数
        estimated_confirmations = min(pain_point.mention_count, 20)
        
        # 基于情感得分评估付费意愿 (负面情感越强，付费意愿可能越高)
        payment_willingness = max(0, (1 - pain_point.sentiment_score) * 0.5)
        
        is_valid = estimated_confirmations >= min_confirmations
        
        return ValidationResult(
            pain_point_id=pain_point.id,
            is_valid=is_valid,
            user_confirmations=estimated_confirmations,
            payment_willingness=payment_willingness,
            confidence_score=0.7 if is_valid else 0.3,
            feedback_summary=f"发现{estimated_confirmations}次提及，情感得分{pain_point.sentiment_score:.2f}"
        )
        
    def extract_user_quotes(self, pain_point: PainPoint) -> List[Quote]:
        """
        提取用户原话引用
        
        Args:
            pain_point: 痛点对象
            
        Returns:
            用户引用列表
        """
        quotes = []
        
        for i, text in enumerate(pain_point.user_quotes):
            source = pain_point.sources[i] if i < len(pain_point.sources) else {}
            
            quote = Quote(
                text=text,
                source=source.get("title", "未知来源"),
                url=source.get("url"),
                date=source.get("date"),
                sentiment="negative" if pain_point.sentiment_score < 0 else "neutral"
            )
            quotes.append(quote)
            
        return quotes
        
    def evaluate_commercial_potential(self, pain_point: PainPoint) -> float:
        """
        评估痛点的商业潜力
        
        Args:
            pain_point: 痛点对象
            
        Returns:
            商业潜力评分 (0-1)
        """
        # 评估因素
        factors = {
            "mention_frequency": min(pain_point.mention_count / 50, 1.0) * 0.3,
            "sentiment_intensity": abs(pain_point.sentiment_score) * 0.2,
            "source_diversity": min(len(pain_point.sources) / 10, 1.0) * 0.2,
            "quote_quality": min(len(pain_point.user_quotes) / 5, 1.0) * 0.3
        }
        
        potential = sum(factors.values())
        pain_point.commercial_potential = potential
        
        return potential
        
    def get_discovery_summary(self) -> Dict:
        """获取发现结果摘要"""
        if not self.discovered_pain_points:
            return {"status": "no_data", "pain_points": []}
            
        validated = [
            pp for pp in self.discovered_pain_points 
            if self.validate_frequency(pp).is_valid
        ]
        
        return {
            "status": "success",
            "total_discovered": len(self.discovered_pain_points),
            "validated_count": len(validated),
            "pain_points": [pp.to_dict() for pp in validated],
            "timestamp": datetime.now().isoformat()
        }
        
    def save_results(self, output_dir: str = "_bmad-output") -> str:
        """保存发现结果到文件"""
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, "pain-points-raw-data.json")
        
        data = {
            "discovery_summary": self.get_discovery_summary(),
            "pain_points": [pp.to_dict() for pp in self.discovered_pain_points],
            "generated_at": datetime.now().isoformat()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        logger.info(f"结果已保存到: {output_path}")
        return output_path


# 便捷函数
def discover_domain_pain_points(domain: str) -> List[PainPoint]:
    """便捷函数：发现指定领域的痛点"""
    discovery = BMADPainPointDiscovery()
    return discovery.discover_pain_points(domain)


def run_full_discovery() -> Dict:
    """运行完整的痛点发现流程"""
    discovery = BMADPainPointDiscovery()
    config = discovery.config
    
    all_domains = config.get_all_domains()
    
    for domain_key in all_domains.keys():
        logger.info(f"正在发现领域: {domain_key}")
        discovery.discover_pain_points(domain_key)
        
    summary = discovery.get_discovery_summary()
    discovery.save_results()
    
    return summary


if __name__ == "__main__":
    # 测试痛点发现
    print("=== BMAD Phase 0 痛点发现测试 ===\n")
    
    try:
        summary = run_full_discovery()
        print(f"\n发现痛点总数: {summary.get('total_discovered', 0)}")
        print(f"验证通过数: {summary.get('validated_count', 0)}")
        
        if summary.get('pain_points'):
            print("\n前3个痛点:")
            for pp in summary['pain_points'][:3]:
                print(f"  - {pp['title']}: {pp['description'][:50]}...")
                
    except Exception as e:
        print(f"测试失败: {e}")
