"""
推荐相关的MCP工具
"""

from fastmcp import FastMCP
from ...domain.services import RecommendationService


def register_recommendation_tools(server: FastMCP):
    """注册推荐相关工具"""
    recommendation_service = RecommendationService()

    @server.tool()
    async def what_to_eat(people_count: int):
        """
        不知道吃什么？根据人数直接推荐适合的菜品组合

        Args:
            people_count: 用餐人数，1-10之间的整数，会根据人数推荐合适数量的菜品

        Returns:
            推荐的菜品组合，包含荤菜和素菜
        """
        return await recommendation_service.what_to_eat(people_count)
