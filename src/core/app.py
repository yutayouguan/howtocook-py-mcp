"""
HowToCook Python MCP 服务器主应用
"""

import logging
from fastmcp import FastMCP
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from .config import get_config
from ..mcp import (
    register_recipe_tools,
    register_meal_tools,
    register_recommendation_tools,
    register_api_resources,
)
from ..mcp import meal_planning_prompt, recipe_recommendation_prompt


def create_app() -> FastMCP:
    """创建并配置FastMCP应用实例"""

    # 获取应用配置
    config = get_config()

    # 配置日志系统
    logging.basicConfig(
        level=getattr(logging, config.logging.level), format=config.logging.format
    )
    logger = logging.getLogger(__name__)

    # 创建 FastMCP 服务器实例
    app = FastMCP(
        name=config.server.name,
        version=config.server.version,
        instructions=f"{config.server.description}。支持按分类查询菜谱、智能推荐菜品组合、制定膳食计划等功能。",
    )

    # 注册内置中间件
    app.add_middleware(ErrorHandlingMiddleware(include_traceback=True))
    app.add_middleware(RateLimitingMiddleware(max_requests_per_second=50))
    app.add_middleware(TimingMiddleware())
    app.add_middleware(LoggingMiddleware(include_payloads=False))

    # 注册工具
    register_recipe_tools(app)
    register_meal_tools(app)
    register_recommendation_tools(app)

    # 注册资源
    register_api_resources(app)

    # 注册提示模板
    @app.prompt("meal_planning_assistant")
    async def meal_planning_assistant_prompt(
        people_count: int,
        dietary_restrictions: list = None,
        cuisine_preferences: list = None,
        budget_level: str = "medium",
    ):
        """膳食计划助手提示模板"""
        return await meal_planning_prompt(
            people_count, dietary_restrictions, cuisine_preferences, budget_level
        )

    @app.prompt("recipe_recommendation")
    async def recipe_recommendation_assistant_prompt(
        occasion: str, cooking_time: int = None, skill_level: str = "beginner"
    ):
        """菜谱推荐提示模板"""
        return await recipe_recommendation_prompt(occasion, cooking_time, skill_level)

    logger.info(f"HowToCook MCP 服务器 v{config.server.version} 初始化完成")
    return app


# 创建应用实例
app = create_app()
