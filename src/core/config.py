"""
HowToCook MCP 服务器配置
使用 dataclass 定义服务器的各种配置选项和常量
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass(frozen=True)
class ServerInfo:
    """服务器基本信息配置"""

    name: str = "howtocook-py-mcp"
    version: str = "0.2.0"
    description: str = "菜谱助手 MCP 服务 - 提供菜谱查询、推荐和膳食计划功能"


@dataclass(frozen=True)
class DataSourceConfig:
    """数据源配置"""

    recipes_url: str = "https://mp-bc8d1f0a-3356-4a4e-8592-f73a3371baa2.cdn.bspapp.com/all_recipes.json"


@dataclass(frozen=True)
class CacheConfig:
    """缓存系统配置"""

    enabled: bool = field(
        default_factory=lambda: os.getenv("CACHE_ENABLED", "true").lower() == "true"
    )
    ttl: int = field(
        default_factory=lambda: int(os.getenv("CACHE_TTL", "3600"))
    )  # 默认1小时


@dataclass(frozen=True)
class LoggingConfig:
    """日志系统配置"""

    level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@dataclass(frozen=True)
class PerformanceConfig:
    """性能相关配置"""

    max_concurrent_requests: int = field(
        default_factory=lambda: int(os.getenv("MAX_CONCURRENT_REQUESTS", "10"))
    )
    request_timeout: int = field(
        default_factory=lambda: int(os.getenv("REQUEST_TIMEOUT", "30"))
    )


@dataclass(frozen=True)
class RecommendationConfig:
    """推荐算法配置"""

    max_people_count: int = 10
    min_people_count: int = 1
    meat_types_priority: List[str] = field(
        default_factory=lambda: ["猪肉", "鸡肉", "牛肉", "羊肉", "鸭肉", "鱼肉"]
    )
    default_categories: List[str] = field(
        default_factory=lambda: ["水产", "早餐", "荤菜", "主食", "素菜", "甜品", "汤羹"]
    )
    fish_threshold_people: int = 8  # 超过8人时添加鱼类菜品


@dataclass(frozen=True)
class MealPlanConfig:
    """膳食计划配置"""

    weekdays: int = 5  # 工作日数量
    weekend_days: int = 2  # 周末天数
    breakfast_ratio: float = 0.2  # 早餐菜品比例
    lunch_ratio: float = 0.4  # 午餐菜品比例
    dinner_ratio: float = 0.4  # 晚餐菜品比例


@dataclass(frozen=True)
class ResourceConfig:
    """资源 URI 配置"""

    categories: str = "howtocook://categories"
    stats: str = "howtocook://stats"
    health: str = "howtocook://health"


@dataclass(frozen=True)
class PromptConfig:
    """提示模板配置"""

    meal_planning: str = "meal_planning_assistant"
    recipe_recommendation: str = "recipe_recommendation"


@dataclass(frozen=True)
class ServerConfig:
    """服务器运行配置"""

    host: str = field(default_factory=lambda: os.getenv("MCP_HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.getenv("MCP_PORT", "8000")))
    path: str = field(default_factory=lambda: os.getenv("MCP_PATH", "/mcp"))
    reload: bool = field(
        default_factory=lambda: os.getenv("MCP_RELOAD", "false").lower() == "true"
    )
    workers: int = field(default_factory=lambda: int(os.getenv("MCP_WORKERS", "1")))


@dataclass(frozen=True)
class AppConfig:
    """应用程序完整配置"""

    server: ServerInfo = field(default_factory=ServerInfo)
    server_config: ServerConfig = field(default_factory=ServerConfig)
    data_source: DataSourceConfig = field(default_factory=DataSourceConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    recommendation: RecommendationConfig = field(default_factory=RecommendationConfig)
    meal_plan: MealPlanConfig = field(default_factory=MealPlanConfig)
    resources: ResourceConfig = field(default_factory=ResourceConfig)
    prompts: PromptConfig = field(default_factory=PromptConfig)

    def to_dict(self) -> Dict[str, Any]:
        """
        将配置转换为字典格式

        Returns:
            Dict[str, Any]: 配置字典
        """
        return {
            "name": self.server.name,
            "version": self.server.version,
            "description": self.server.description,
            "data_source": {
                "recipes_url": self.data_source.recipes_url,
            },
            "cache": {
                "enabled": self.cache.enabled,
                "ttl": self.cache.ttl,
            },
            "logging": {
                "level": self.logging.level,
                "format": self.logging.format,
            },
            "performance": {
                "max_concurrent_requests": self.performance.max_concurrent_requests,
                "request_timeout": self.performance.request_timeout,
            },
            "recommendation": {
                "max_people_count": self.recommendation.max_people_count,
                "min_people_count": self.recommendation.min_people_count,
                "meat_types_priority": self.recommendation.meat_types_priority,
                "default_categories": self.recommendation.default_categories,
                "fish_threshold_people": self.recommendation.fish_threshold_people,
            },
            "meal_plan": {
                "weekdays": self.meal_plan.weekdays,
                "weekend_days": self.meal_plan.weekend_days,
                "breakfast_ratio": self.meal_plan.breakfast_ratio,
                "lunch_ratio": self.meal_plan.lunch_ratio,
                "dinner_ratio": self.meal_plan.dinner_ratio,
            },
            "resources": {
                "categories": self.resources.categories,
                "stats": self.resources.stats,
                "health": self.resources.health,
            },
            "prompts": {
                "meal_planning": self.prompts.meal_planning,
                "recipe_recommendation": self.prompts.recipe_recommendation,
            },
        }


# 全局配置实例
_config = AppConfig()


def get_config() -> AppConfig:
    """
    获取完整的应用配置对象

    Returns:
        AppConfig: 应用配置实例
    """
    return _config
