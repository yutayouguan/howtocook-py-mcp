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

    @server.tool()
    async def search_recipes_by_ingredients(ingredients: list[str]):
        """
        根据现有食材搜索可以制作的菜谱

        Args:
            ingredients: 现有食材列表，如["鸡肉", "土豆", "胡萝卜"]

        Returns:
            包含指定食材的菜谱列表，按匹配度排序
        """
        return await recipe_service.search_recipes_by_ingredients(ingredients)

    @server.tool()
    async def filter_recipes_by_difficulty(difficulty: int):
        """
        按烹饪难度筛选菜谱

        Args:
            difficulty: 烹饪难度等级，1-5星（1=最简单，5=最复杂）

        Returns:
            指定难度等级的菜谱列表
        """
        return await recipe_service.filter_recipes_by_difficulty(difficulty)

    @server.tool()
    async def search_recipes_by_time(max_time_minutes: int):
        """
        按制作时间筛选菜谱

        Args:
            max_time_minutes: 最大制作时间（分钟），如30表示30分钟内能完成的菜

        Returns:
            在指定时间内能完成的菜谱列表
        """
        return await recipe_service.search_recipes_by_time(max_time_minutes)

    @server.tool()
    async def generate_shopping_list(recipe_names: list[str], people_count: int = 1):
        """
        根据菜谱生成购物清单

        Args:
            recipe_names: 菜谱名称列表，如["宫保鸡丁", "麻婆豆腐"]
            people_count: 用餐人数，用于调整食材用量

        Returns:
            按分类整理的购物清单，包含食材名称和用量
        """
        return await recipe_service.generate_shopping_list(recipe_names, people_count)
