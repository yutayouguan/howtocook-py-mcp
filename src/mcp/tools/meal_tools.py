"""
膳食计划相关的MCP工具
"""

from typing import List, Optional
from fastmcp import FastMCP
from ...domain.services import MealService


def register_meal_tools(server: FastMCP):
    """注册膳食计划相关工具"""
    meal_service = MealService()

    @server.tool()
    async def recommend_meals(
        people_count: int,
        allergies: Optional[List[str]] = None,
        avoid_items: Optional[List[str]] = None,
    ):
        """
        根据用户的忌口、过敏原、人数智能推荐菜谱，创建一周的膳食计划

        Args:
            people_count: 用餐人数，1-10之间的整数
            allergies: 过敏原列表，如['大蒜', '虾']
            avoid_items: 忌口食材列表，如['葱', '姜']

        Returns:
            一周的膳食计划
        """
        return await meal_service.recommend_meals(people_count, allergies, avoid_items)
