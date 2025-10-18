"""
菜谱相关的MCP工具
"""

from fastmcp import FastMCP
from ...domain.services import RecipeService


def register_recipe_tools(server: FastMCP):
    """注册菜谱相关工具"""
    recipe_service = RecipeService()

    @server.tool()
    async def get_all_recipes():
        """
        获取所有菜谱

        Returns:
            所有菜谱的简化信息，只包含名称和描述
        """
        return await recipe_service.get_all_recipes()

    @server.tool()
    async def get_recipes_by_category(category: str):
        """
        根据分类获取菜谱

        Args:
            category: 菜谱分类，如"荤菜"、"素菜"、"汤羹"等

        Returns:
            指定分类的菜谱列表
        """
        return await recipe_service.get_recipes_by_category(category)

    @server.tool()
    async def get_recipe_details(recipe_name: str):
        """
        获取指定菜谱的详细做法

        Args:
            recipe_name: 菜谱名称，如"宫保鸡丁"、"麻婆豆腐"等

        Returns:
            菜谱的详细信息，包括食材、做法步骤、小贴士等
        """
        return await recipe_service.get_recipe_details(recipe_name)
